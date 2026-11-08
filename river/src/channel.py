"""Silt/gravel reach, asymmetric banks, sorted bar and water with flow data."""
import math
import random
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import geometry as G
BED_TREE=None


def surface_z(p,x,y):
    if BED_TREE is not None:
        hit=BED_TREE.ray_cast(Vector((x,y,100)),Vector((0,0,-1)),120)[0]
        if hit is not None:return hit.z
    return p.bed(x,y)


def stone(b,x,y,z,r,rng,role='bank'):
    # Low-silhouette angular riprap, individual seating determined by terrain.
    n=7;phase=rng.random()*6.28;sx=rng.uniform(.8,1.3);sy=rng.uniform(.7,1.2)
    base=[(x+sx*r*math.cos(i*math.tau/n+phase),y+sy*r*math.sin(i*math.tau/n+phase),z-r*.22) for i in range(n)]
    top=[(x+sx*r*.7*math.cos(i*math.tau/n+phase),y+sy*r*.7*math.sin(i*math.tau/n+phase),z+r*rng.uniform(.32,.72)) for i in range(n)]
    v=rng.uniform(.60,1.05);b.loft([base,top],role,(v,v,v*.96,1))


def terrain(p,parent):
    global BED_TREE
    BED_TREE=None
    rt=G.root('RiverReach',parent=parent)
    b=G.Batch('BedBanksFloodplain',rt,'reach')
    us=[-8,-6,-4,-3,-2.3,-1.8,-1.5,-1.3,-1.15,-1.08,-1,-.94,-.87,-.78,-.66,-.5,-.3,0,.3,.5,.66,.78,.87,.94,1,1.05,1.10,1.16,1.25,1.4,1.7,2.3,3,4,6,8]
    ys=[-p.reach/2+i*2 for i in range(round(p.reach/2)+1)]
    rows=[]
    for y in ys:
        left=p.center(y)-p.halfwidth(y)
        xs=[p.center(y)+u*p.halfwidth(y) for u in us]+p.water_edges(y)
        xs += [s*(p.length/2+off) for s in (-1,1) for off in (-.01,.01,.89,.90,1.02,1.03)]
        xs += [-170,-155,155,170]
        if p.kind=='downtown':
            xs += [left-off for off in (.74,.76,1,1.12,4.2,4.44,4.46)]
            right=p.center(y)+p.halfwidth(y)
            xs += [right+off for off in (5,11,11.2,13.6)]
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
    for i in range(1150):
        y=rng.uniform(p.bar_y-26,p.bar_y+27);x=p.center(y)+p.outside*p.halfwidth(y)*rng.uniform(-1.04,-.49)
        z=surface_z(p,x,y)
        if z>p.water_z(y)-.32:stone(rocks,x,y,z,rng.uniform(.035,.14),rng)
    # Armored, keyed slope and toe at both abutments and each pier.
    for side in (-1,1):
        for i in range(460):
            x=side*rng.uniform(p.width*.40,p.length/2+3.0);y=rng.uniform(-9,9)
            if abs(x)>p.length/2-.8 and abs(y)<7:continue
            z=surface_z(p,x,y);stone(rocks,x,y,z+.04,rng.uniform(.16,.39),rng)
    for j in range(1,p.spans):
        xx=-p.length/2+j*p.span
        for i in range(170):
            x=xx+rng.uniform(-2.0,2.0);y=rng.uniform(-p.deck_width*.48,p.deck_width*.48)
            z=surface_z(p,x,y);stone(rocks,x,y,z+.06,rng.uniform(.15,.33),rng)
    rocks.finish()
    # Cutbank roots and flood debris are dead wood, not new tree species.
    debris=G.Batch('CutbankExposedRootsAndDrift',rt,'reach')
    for j in range(18):
        if p.kind=='downtown':continue
        y=p.bar_y-20+j*2.3;x=p.center(y)+p.halfwidth(y)*1.11;z=p.bed(x,y)
        for k in range(3):
            debris.tube([(x+.3,y,z+.15),(x-.10,y+.2,z-.2),(x-.45-k*.10,y+.2+k*.23,z-.9)],.018/(k+1),'wood',5)
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
    b=G.Batch('WaterSurface',parent,'water');ny=240;nx=20
    rows=[]
    for i in range(ny+1):
        y=-p.reach/2+i*p.reach/ny;l,r=p.water_edges(y)
        rows.append([(l+(r-l)*j/nx,y,p.water_z(y)+.006*math.sin(j*.9+y*.7)*math.exp(-((y-p.riffle_y)/10)**2)) for j in range(nx+1)])
    vs=[v for row in rows for v in row]
    fs=[(i*(nx+1)+j,i*(nx+1)+j+1,(i+1)*(nx+1)+j+1,(i+1)*(nx+1)+j) for i in range(ny) for j in range(nx)]
    b.geom(vs,fs,'water',smooth=True,up=True);ob=b.finish()
    flow=ob.data.attributes.new('_FLOW',type='FLOAT_VECTOR',domain='POINT')
    for v,a in zip(ob.data.vertices,flow.data):
        tx,ty=p.tangent(v.co.y);speed=p.speed(v.co.x,v.co.y);a.vector=(tx*speed,ty*speed,max(0,p.water_z(v.co.y)-surface_z(p,v.co.x,v.co.y)))
    # A real closed bottom/edge shell makes absorption scale with actual depth.
    volume=G.Batch('WaterVolumeClosure',parent,'water')
    def bottom(v):
        x,y,_=v
        return (x,y,min(surface_z(p,x,y)-.02,p.water_z(y)-.025))
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
        tx,ty=p.tangent(v.co.y);speed=p.speed(v.co.x,v.co.y)
        a.vector=(tx*speed,ty*speed,max(0,p.water_z(v.co.y)-surface_z(p,v.co.x,v.co.y)))
    foam=G.Batch('RiffleBrokenFoam',parent,'water');rng=random.Random(p.seed+31)
    for j in range(160):
        y=rng.gauss(p.riffle_y,3.5);l,r=p.water_edges(y);x=rng.uniform(l+.7,r-.7)
        length=rng.uniform(.07,.5);w=rng.uniform(.008,.028)
        foam.geom([(x-length/2,y,p.water_z(y)+.013),(x+length/2,y+.06,p.water_z(y)+.013),(x+length*.30,y+.06+w,p.water_z(y)+.014),(x-length*.4,y+w,p.water_z(y)+.014)],[(0,1,2,3)],'foam')
    foam.finish()
