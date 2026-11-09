"""Silt/gravel reach, asymmetric banks, sorted bar and water with flow data."""
import math
import random
import itertools
from functools import lru_cache
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import geometry as G
BED_TREE=None


@lru_cache(maxsize=32)
def wave_lanes(p):
    """Finite rough-bed chutes; each has its own crest spacing and start."""
    result=[]
    for i,(u,width,offset,spacing) in enumerate(((-.58,.055,-1.8,1.45),
            (-.16,.075,1.0,1.67),(.25,.05,-.7,1.92),(.62,.065,2.4,1.54))):
        result.append((p.center(p.riffle_y)+u*p.halfwidth(p.riffle_y),
                       p.width*width,offset+.18*math.sin(p.seed+i),spacing,i))
    return tuple(result)


def water_surface(p,x,y):
    u=(x-p.center(y))/p.halfwidth(y);height=0.
    # Short bowed crests decay through each chute. A single sinusoid spanning
    # the channel creates the regular transverse bars of an artificial weir.
    for cx,width,offset,spacing,phase in wave_lanes(p):
        cross=(x-cx)/width;envelope=math.exp(-cross*cross)
        if envelope<.002:continue
        for crest in range(3):
            station=offset+crest*spacing+.15*crest*crest
            bow=.28*math.sin(cross*1.6+phase)+.11*cross*cross
            along=y-p.riffle_y-station-bow
            amplitude=.09*.76**crest
            height+=envelope*amplitude*(math.exp(-(along/.43)**2)
                     -.42*math.exp(-((along-.62)/.63)**2))
    return p.water_z(y)+height*max(0,1-u*u)


def water_normal(p,x,y):
    d=.005;dx=(water_surface(p,x+d,y)-water_surface(p,x-d,y))/(2*d)
    dy=(water_surface(p,x,y+d)-water_surface(p,x,y-d))/(2*d)
    return Vector((-dx,-dy,1)).normalized()


def foam_streaks(p):
    """Convergent foam lanes behind the shoal, with continuous start stations.

    Fixed transverse rows make a ladder in an elevated view. Chutes follow
    the local standing-wave activity; individual tails advect downstream.
    """
    rng=random.Random(p.seed+31);result=[]
    for _ in range(15):
        cx,width,offset,spacing,phase=rng.choice(wave_lanes(p)[1:3])
        y=p.riffle_y+offset+rng.gauss(.3,1.3)
        x=cx+rng.gauss(0,width*.65)
        result.append((x,y,rng.uniform(1.8,6.2),rng.uniform(.28,.65)))
    return result


def surface_z(p,x,y):
    if BED_TREE is not None:
        hit=BED_TREE.ray_cast(Vector((x,y,100)),Vector((0,0,-1)),120)[0]
        if hit is not None:return hit.z
    return p.bed(x,y)


def stone(b,x,y,z,r,rng,role='riprap',water_z=0):
    # A quarried block is bounded by fracture planes, not a pointed top ring.
    # Six uneven primary cleavages and four corner breaks yield broad planar
    # facets. Each block's bedding is independently tilted and rotated.
    from mathutils import Matrix
    planes=[]
    for axis in range(3):
        for sign in (-1,1):
            n=Vector([rng.uniform(-.15,.15) for _ in range(3)]);n[axis]=sign
            planes.append((n.normalized(),rng.uniform(.62,1.0)))
    for signs in ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)):
        n=Vector([sign*rng.uniform(.85,1.15) for sign in signs]).normalized()
        planes.append((n,rng.uniform(.64,.92)))
    # Blast fragments have no common horizontal bedding after placement.
    rotation=(Matrix.Rotation(rng.random()*math.tau,3,'Z')
              @Matrix.Rotation(rng.uniform(-1.4,1.4),3,'Y')
              @Matrix.Rotation(rng.uniform(-1.4,1.4),3,'X'))
    local=[];sx=rng.uniform(.8,1.35);sy=rng.uniform(.7,1.2)
    for (a,da),(c,dc),(d,dd) in itertools.combinations(planes,3):
        determinant=a.dot(c.cross(d))
        if abs(determinant)<1e-6:continue
        point=(da*c.cross(d)+dc*d.cross(a)+dd*a.cross(c))/determinant
        if any(n.dot(point)>limit+1e-5 for n,limit in planes):continue
        local.append(point)
    # Grade by the actual fragment radius, not a plane's offset: nearly
    # parallel fractures must never produce meter-long shards from a 0.3m rock.
    radius=max(point.length for point in local);vertices=[]
    for point in local:
        point=rotation@Vector((point.x*sx,point.y*sy,point.z*.75))/radius
        vertices.append((x+r*point.x,y+r*point.y,z+r*point.z))
    if BED_TREE is not None:
        for vx,vy,vz in vertices:
            hit=BED_TREE.ray_cast(Vector((vx,vy,100)),Vector((0,0,-1)),120)[0]
            if hit is None or abs(hit.z-(z-.04))>r*1.05:return
    bm=bmesh.new()
    for point in vertices:bm.verts.new(point)
    bmesh.ops.convex_hull(bm,input=list(bm.verts));bm.normal_update()
    bmesh.ops.dissolve_limit(bm,angle_limit=.0001,verts=list(bm.verts),edges=list(bm.edges));bm.normal_update()
    floors={}
    for vertex in bm.verts:
        point=vertex.co
        hit=BED_TREE.ray_cast(Vector((point.x,point.y,100)),Vector((0,0,-1)),120)[0] if BED_TREE is not None else None
        floors[vertex]=hit.z if hit is not None else z-.04
    v=rng.uniform(.42,.68);brown=rng.random()
    faces=[]
    for face in bm.faces:
        if all(vertex.co.z<=floors[vertex]+.01 for vertex in face.verts):continue
        points=[tuple(vertex.co) for vertex in face.verts]
        first=min(range(len(points)),key=lambda i:points[i]);points=points[first:]+points[:first]
        faces.append(points)
    # BMesh face allocation order is not a seeded construction parameter.
    # Canonical cyclic starts and lexicographic ordering stabilize both the
    # exported indices and the per-fracture mineral variation across runs.
    for points in sorted(faces):
        variation=rng.uniform(.96,1.04)
        tint=(v*(1+.20*brown)*variation,v*1.04*variation,v*(1.13-.30*brown)*variation,1)
        b.geom(points,[tuple(range(len(points)))],role,tint)
    bm.free()


def terrain(p,parent):
    global BED_TREE
    BED_TREE=None
    rt=G.root('RiverReach',parent=parent)
    b=G.Batch('BedBanksFloodplain',rt,'reach')
    us=[-8,-6,-4,-3,-2.3,-1.8,-1.5,-1.3,-1.15,-1.10,-1.06,-1.03,-1,-.94,-.87,-.78,-.66,-.5,-.3,0,.3,.5,.66,.78,.87,.94,1,1.03,1.06,1.10,1.15,1.25,1.4,1.7,2.3,3,4,6,8]
    ys=[-p.reach/2+i*2 for i in range(round(p.reach/2)+1)]
    rows=[]
    for y in ys:
        left=p.center(y)-p.halfwidth(y)
        xs=[p.center(y)+u*p.halfwidth(y) for u in us]+p.water_edges(y)
        xs += [s*(p.length/2+off) for s in (-1,1) for off in (-.01,.01,.89,.90,1.02,1.03)]
        xs += [-170,-155,155,170]
        if p.kind=='downtown':
            for side in (-1,1):
                xs += [p.center(y)+side*(p.halfwidth(y)+off) for off in (.74,.76,1,1.12,4.2,4.44,4.46,4.6,7,11.5)]
        rows.append([(x,y,p.bed(x,y)) for x in sorted(xs)])
    for row0,row1 in zip(rows,rows[1:]):
        for j in range(len(row0)-1):
            vs=[row0[j],row0[j+1],row1[j+1],row1[j]]
            z=sum(v[2] for v in vs)/4;y=sum(v[1] for v in vs)/4
            u=(sum(v[0] for v in vs)/4-p.center(y))/p.halfwidth(y)
            role='grass' if abs(u)>1.16 and z>1.1 else 'bank'
            # Broad caused wetness: submerged bed, low wet bank, upper dry soil.
            wet=.48 if z<.12 else .67 if z<.60 else .85
            if role=='grass':
                v=.61+.13*math.sin(y*.067+u*1.7)+.07*math.sin(y*.31-u*.9)
                color=(v*.91,v,v*.72,1)
            else:color=(wet,wet*.98,wet*.90,1)
            b.geom(vs,[(0,1,2,3)],role,color,smooth=True,up=True)
    bed=b.finish()
    bm=bmesh.new();bm.from_mesh(bed.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bm.normal_update();bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0])
    bm.to_mesh(bed.data);bm.free();bed.data.update()
    BED_TREE=BVHTree.FromPolygons([v.co for v in bed.data.vertices],[list(f.vertices) for f in bed.data.polygons],all_triangles=True)
    rng=random.Random(p.seed);rocks=G.Batch('BarCobbleAndScourRiprap',rt,'reach')
    for i in range(800):
        y=rng.uniform(p.bar_y-26,p.bar_y+27);x=p.center(y)+p.outside*p.halfwidth(y)*rng.uniform(-1.04,-.49)
        z=surface_z(p,x,y)
        if z>p.water_z(y)-.32:stone(rocks,x,y,z,rng.uniform(.035,.14),rng,water_z=p.water_z(y))
    # Armored, keyed slope and toe at both abutments and each pier.
    for side in (-1,1):
        for i in range(390):
            if i<275:
                x=side*rng.uniform(p.length/2-4,p.length/2+6.5)
                y=rng.choice((-1,1))*rng.uniform(p.deck_width/2-.3,p.deck_width/2+6)
            else:
                x=side*rng.uniform(p.length/2-7,p.length/2-2)
                y=rng.uniform(-p.deck_width/2,p.deck_width/2)
            if abs(x)>p.length/2-.8 and abs(y)<6.8:continue
            z=surface_z(p,x,y);stone(rocks,x,y,z+.04,rng.uniform(.16,.45),rng,water_z=p.water_z(y))
    for j in range(1,p.spans):
        xx=-p.length/2+j*p.span
        for i in range(125):
            x=xx+rng.uniform(-2.0,2.0);y=rng.uniform(-p.deck_width*.48,p.deck_width*.48)
            z=surface_z(p,x,y);stone(rocks,x,y,z+.06,rng.uniform(.15,.33),rng,water_z=p.water_z(y))
    stones=rocks.finish();colors=stones.data.color_attributes['Tint']
    for loop,attribute in zip(stones.data.loops,colors.data):
        point=stones.data.vertices[loop.vertex_index].co;level=point.z-p.water_z(point.y)
        wet=.62+.38*min(1,max(0,level)/.45);algae=max(0,1-max(0,level)/.16)
        c=attribute.color;attribute.color=(c[0]*wet*(1-.16*algae),c[1]*wet,c[2]*wet*(1-.24*algae),c[3])
    # Cutbank roots and flood debris are dead wood, not new tree species.
    debris=G.Batch('CutbankExposedRootsAndDrift',rt,'reach')
    for j in range(18):
        if p.kind=='downtown':continue
        y=p.bar_y-20+j*2.3;x=p.center(y)+p.halfwidth(y)*1.11;z=p.bed(x,y)
        for k in range(3):
            debris.tube([(x+.3,y,z+.15),(x-.10,y+.2,z-.2),(x-.45-k*.10,y+.2+k*.23,z-.9)],.018/(k+1),'wood',5)
    if p.kind=='edge':
        sod=G.Batch('ErodedSodAndFloodWrack',rt,'reach')
        for i in range(42):
            y=rng.uniform(p.bar_y-27,p.bar_y+28);side=p.outside
            # Waterline recession exposes a steep soil face with separate
            # fallen turf slabs, rather than merely darkening an even ramp.
            x=p.center(y)+side*p.halfwidth(y)*rng.uniform(1.015,1.07)
            z=surface_z(p,x,y);w=rng.uniform(.24,.65);h=rng.uniform(.35,.95)
            pts=[(xx,yy,surface_z(p,xx,yy)+.035) for xx,yy in ((x-w,y-h),(x+w,y-h*.7),(x+w*.6,y+h),(x-w*.8,y+h*.6))]
            sod.geom(pts,[(0,1,2,3)],'grass',(.75,.76,.46,1),up=True)
            for j in range(2):
                a=(x,y,z+.08);c=(x-side*rng.uniform(.3,.8),y+rng.uniform(-.4,.4),z-rng.uniform(.2,.6))
                debris.tube([a,((a[0]+c[0])/2,a[1]+.1,a[2]-.12),c],rng.uniform(.013,.027),'wood',5)
        for i in range(220):
            y=rng.uniform(-146,146);side=rng.choice((-1,1))
            lo=p.halfwidth(y);hi=lo+10
            for _ in range(20):
                mid=(lo+hi)/2
                if p.bed(p.center(y)+side*mid,y)-p.water_z(y)>.8:hi=mid
                else:lo=mid
            x=p.center(y)+side*(lo+hi)/2;z=surface_z(p,x,y)
            debris.tube([(x,y,z+.018),(x+rng.uniform(-.10,.10),y+rng.uniform(.1,.45),z+.03)],rng.uniform(.005,.014),'wood',4)
        sod.finish()
    for j in range(1,p.spans):
        xx=-p.length/2+j*p.span
        tx,ty=p.tangent(0);cross=(ty,-tx)
        if p.pier=='columns':nx,ny=xx-tx*.60,-p.deck_width*.29-ty*.60
        else:nx,ny=xx-tx*p.deck_width*.83/2,-ty*p.deck_width*.83/2
        cx,cy=nx-tx*.115,ny-ty*.115
        pts=[(cx+a*cross[0]-tx*slack,cy+a*cross[1]-ty*slack,p.water_z(cy)+z)
             for a,slack,z in ((-.9,.04,.05),(0,0,.04),(.8,.03,.02))]
        debris.tube(pts,.13,'wood',9)
        for k in range(8):
            a=rng.uniform(-.78,.78);run=rng.uniform(.25,.85);sweep=rng.uniform(-.38,.38)
            x=cx+a*cross[0];y=cy+a*cross[1]
            debris.tube([(x,y,p.water_z(y)+.05),(x-tx*run+cross[0]*sweep,y-ty*run+cross[1]*sweep,p.water_z(y)+rng.uniform(-.01,.065))],rng.uniform(.012,.028),'wood',5)
    debris.finish()
    G.path('FlowCenterline',[(p.center(y),y,p.water_z(y)) for y in ys],rt,'flow',flow_direction='+Y',nominal_speed_m_s=.38)
    return rt


def water(p,parent):
    b=G.Batch('WaterSurface',parent,'water');nx=20
    # Resolve the 1.65m standing waves locally without spending triangles
    # along the entire calm 300m reach.
    ys=sorted(set([-p.reach/2+i*p.reach/120 for i in range(121)]+
                  [-80.,0.,40.,75.]+[p.riffle_y-9+i*.25 for i in range(73)]));ny=len(ys)-1
    rows=[]
    for y in ys:
        l,r=p.water_edges(y)
        rows.append([(l+(r-l)*j/nx,y,water_surface(p,l+(r-l)*j/nx,y)) for j in range(nx+1)])
    vs=[v for row in rows for v in row]
    fs=[(i*(nx+1)+j,i*(nx+1)+j+1,(i+1)*(nx+1)+j+1,(i+1)*(nx+1)+j) for i in range(ny) for j in range(nx)]
    for f in fs:
        coords=[vs[k] for k in f];x=sum(v[0] for v in coords)/4;y=sum(v[1] for v in coords)/4
        speed=p.speed(x,y)
        tx,ty=p.tangent(y)
        uv=[((vx*ty-vy*tx)/3.7,(vx*tx+vy*ty)/2.2) for vx,vy,vz in coords]
        b.geom(coords,[(0,1,2,3)],'water',uv=uv,smooth=True,up=True)
    ob=b.finish()
    flow=ob.data.attributes.new('_FLOW',type='FLOAT_VECTOR',domain='POINT')
    for v,a in zip(ob.data.vertices,flow.data):
        vx,vy=p.flow(v.co.x,v.co.y);a.vector=(vx,vy,max(0,p.water_z(v.co.y)-surface_z(p,v.co.x,v.co.y)))
    # A real closed bottom/edge shell makes absorption scale with actual depth.
    volume=G.Batch('WaterVolumeClosure',parent,'water')
    def bottom(v):
        x,y,_=v
        # A sampled bed offset can interpolate above the actual triangulated
        # bed between samples. Keep the invisible closing interface buried;
        # camera/shadow paths still meet the real bed at its physical depth.
        return (x,y,p.water_z(y)-3.5)
    for row in (rows[0],rows[-1]):
        for a,c in zip(row,row[1:]):volume.geom([a,c,bottom(c),bottom(a)],[(0,1,2,3)],'water')
    for side in (0,-1):
        for a,c in zip(rows,rows[1:]):
            a,c=a[side],c[side];volume.geom([a,c,bottom(c),bottom(a)],[(0,1,2,3)],'water')
    volume.geom([bottom(v) for v in vs],[tuple(reversed(f)) for f in fs],'water',smooth=True)
    closure=volume.finish()
    # One closed shell is required for the medium stack to follow real depth.
    # Separate top/bottom objects lose that relationship in Cycles transmission.
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);closure.select_set(True)
    bpy.context.view_layer.objects.active=ob;bpy.ops.object.join()
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
    flow=ob.data.attributes.get('_FLOW')
    for v,a in zip(ob.data.vertices,flow.data):
        vx,vy=p.flow(v.co.x,v.co.y)
        a.vector=(vx,vy,max(0,p.water_z(v.co.y)-surface_z(p,v.co.x,v.co.y)))
    water_tree=BVHTree.FromPolygons([v.co for v in ob.data.vertices],[list(f.vertices) for f in ob.data.polygons],all_triangles=True)
    foam=G.Batch('RiffleBrokenFoam',parent,'water');rng=random.Random(p.seed+31)
    for j,(x,y,length,width) in enumerate(foam_streaks(p)):
        segments=24
        tx,ty=p.tangent(y)
        for k in range(segments):
            t0=k/segments;t1=(k+1)/segments
            if rng.random()<.08:continue
            coords=[]
            for t,sign in ((t0,-1),(t0,1),(t1,1),(t1,-1)):
                wobble=.44*math.sin(t*(4+j%3)+j*.71)+.12*math.sin(t*13+j)
                w=width*(.12+.88*math.sin(math.pi*t))*(.7+.3*math.sin(t*17+j))
                yy=y+ty*length*t-tx*(wobble+sign*w)
                xx=x+p.center(yy)-p.center(y)+ty*(wobble+sign*w)
                hit=water_tree.ray_cast(Vector((xx,yy,p.water_z(yy)+1)),Vector((0,0,-1)),3)[0]
                if hit is None:break
                coords.append((xx,yy,hit.z+.004))
            if len(coords)!=4:continue
            foam.geom(coords,[(0,1,2,3)],'foam',uv=foam_chart(j%4,t0,t1))
    # Intermittent curling foam/eddy lines in the sheltered pier wakes.
    for i in range(1,p.spans):
        xx=-p.length/2+i*p.span
        for j in range(75):
            t=rng.uniform(0,math.tau);radius=rng.uniform(.7,2.5)
            x=xx+math.cos(t)*radius;y=p.deck_width/2+1.2+math.sin(t)*radius*.7
            if not p.water_edges(y)[0]<x<p.water_edges(y)[1]:continue
            foam.geom([(x,y,p.water_z(y)+.003),(x+.12*math.sin(t),y-.12*math.cos(t),p.water_z(y)+.003),(x+.12*math.sin(t)+.025,y-.12*math.cos(t),p.water_z(y)+.003)],[(0,1,2)],'foam',uv=foam_chart(j%4)[:3])
    foam.finish()


def foam_chart(k,t0=0,t1=1):
    u=(k%2)*.25;v=.625-(k//2)*.125
    a=v+.002+.121*t0;b=v+.002+.121*t1
    return [(u+.002,a),(u+.248,a),(u+.248,b),(u+.002,b)]
