"""Fit irregular sediment/scuff cards to imported mesh surfaces.

No repeat bands are baked into the tile: deposition follows the gutter toe;
scuffs follow parking turns; isolated repairs/oil belong to chosen road bays.
"""
import math,random
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from dimensions import *
from textures import RECTS


def apply_weather():
    rng=random.Random(39281);mat=next(m for m in bpy.data.materials if m.name.startswith('GroundTrim'))
    report=[]
    def emit(name,verts,faces,uvs,kind):
        me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat)
        ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);uv=me.uv_layers.new(name='UVMap')
        for p,row in zip(me.polygons,uvs):
            for li,v in zip(p.loop_indices,row):uv.data[li].uv=v
        ob['surface_kind']='GroundTrim';ob['decal_cause']=kind
        report.append(dict(name=name,kind=kind,triangles=len(faces),offset_m=DECAL_OFFSET+.001 if kind=='sediment' else DECAL_OFFSET))
    def card(name,verts,kind,shape=(2,2),window=None):
        w,h=shape;faces=[];uvs=[];u0,v0,u1,v1=RECTS[kind]
        if window:
            a,b,c,d=window;u0,u1=u0+a*(u1-u0),u0+c*(u1-u0);v0,v1=v0+b*(v1-v0),v0+d*(v1-v0)
        for j in range(h-1):
            for i in range(w-1):
                a=j*w+i;fs=[(a,a+1,a+w+1),(a,a+w+1,a+w)]
                for f in fs:
                    faces.append(f);uvs.append([(u0+((k//w)/(h-1) if kind in ('sediment','seal') else (k%w)/(w-1))*(u1-u0),v0+((k%w)/(w-1) if kind in ('sediment','seal') else (k//w)/(h-1))*(v1-v0)) for k in f])
        emit(name,verts,faces,uvs,kind)
    # Independently aged bays: a minority of irregular sealed splits, with
    # parked-engine drips near the curb rather than paired spots in every lane.
    road_rng=random.Random(80419)
    roads=[ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.parent and ob.parent.get('module','').startswith('Road_Straight') and 'Manhole' not in ob.parent.get('module','')]
    for ob in sorted(roads,key=lambda o:o.name):
        ob.data.calc_loop_triangles()
        points=[ob.matrix_world@v.co for v in ob.data.vertices]
        tris=[tuple(t.vertices) for t in ob.data.loop_triangles if ob.data.materials[t.material_index].name=='Asphalt']
        if not tris:continue
        bvh=BVHTree.FromPolygons(points,tris,all_triangles=True)
        def fit(x,y,offset):
            p=ob.matrix_world@Vector((x,y,1));hit,_,_,_=bvh.ray_cast(p,Vector((0,0,-1)))
            if hit is None:raise RuntimeError('Unfitted road weather '+ob.name)
            return tuple(hit+Vector((0,0,offset)))
        if road_rng.random()<.27:
            transverse=road_rng.random()<.35
            cx=road_rng.uniform(-1.3,1.3);cy=road_rng.uniform(-.6,.6)
            if not transverse:cx=road_rng.choice((-1,1))*road_rng.uniform(1.9,2.45)
            length=road_rng.uniform(2.4,4.8);phase=road_rng.uniform(0,6.28)
            centers=[]
            for j in range(33):
                t=j/32;along=(t-.5)*length
                bend=.15*math.sin(t*7+phase)+.045*math.sin(t*29+phase)+road_rng.uniform(-.018,.018)
                centers.append(Vector((cx+along,cy+bend)) if transverse else Vector((cx+bend,cy+along)))
            vertices=[]
            for j,p in enumerate(centers):
                tangent=(centers[min(j+1,32)]-centers[max(0,j-1)]).normalized();n=Vector((tangent.y,-tangent.x))
                for side in (-1,1):
                    v=p+n*(side*.105);vertices.append(fit(v.x,v.y,.003))
            card('Irregular_seal_'+ob.name,vertices,'seal',(2,len(centers)))
        for side in (-1,1):
            if road_rng.random()>.32:continue
            cx=side*road_rng.uniform(2.95,3.25);cy=road_rng.uniform(-1.9,1.9)
            sx=road_rng.uniform(.30,.65);sy=road_rng.uniform(.45,1.3)
            vertices=[fit(cx+x*sx,cy+y*sy,.004) for y in (-.5,.5) for x in (-.5,.5)]
            # Different fragments of the shared drip graphic, sometimes flipped.
            window=road_rng.choice(((0,0,.46,1),(.40,0,1,1),(1,1,0,0)))
            card('Parked_oil_'+ob.name+str(side),vertices,'oil',window=window)
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('surface_kind')!='Concrete' or 'WalkCorner' in ob.name or 'Curb' not in ob.name and not ob.name.startswith('Corner_'):continue
        # The inlet's structural opening is deliberately empty. Do not bridge
        # it with a sediment sheet or ray-fit deposits onto its basin floor.
        if 'Inlet_' in ob.name:
            if 'depressed_gutter' not in ob.name:continue
            ob.data.calc_loop_triangles()
            # Copy the clipped actual pan triangles, rather than bridging its
            # diagonals with a coarser grid. Keep the original 3 mm offset and
            # true atlas meters, including at the depressed gutter's twist.
            for sign in (-1,1):
                lo,hi=sorted((sign*.46,sign*(BAY/2-.004)));verts=[];faces=[];uvs=[]
                u0,v0,u1,v1=RECTS['sediment']
                for tri in ob.data.loop_triangles:
                    if ob.data.materials[tri.material_index].name!='Concrete':continue
                    poly=[ob.data.vertices[i].co.copy() for i in tri.vertices]
                    for axis,limit,greater in ((0,-.25,True),(0,-.014,False),(1,lo,True),(1,hi,False)):
                        clipped=[]
                        for p,q in zip(poly,poly[1:]+poly[:1]):
                            inside=p[axis]>=limit if greater else p[axis]<=limit
                            other=q[axis]>=limit if greater else q[axis]<=limit
                            if inside:clipped.append(p)
                            if inside!=other:clipped.append(p.lerp(q,(limit-p[axis])/(q[axis]-p[axis])))
                        poly=clipped
                    for j in range(1,len(poly)-1):
                        points=[poly[0],poly[j],poly[j+1]]
                        if (points[1]-points[0]).cross(points[2]-points[0]).length<1e-8:continue
                        first=len(verts);verts.extend(tuple(ob.matrix_world@p+Vector((0,0,.003))) for p in points)
                        faces.append((first,first+1,first+2))
                        uvs.append([(u0+((.4 if sign<0 else 0)+(p.y-lo)/3.048)*(u1-u0),v0+(p.x+.25)/.236*(v1-v0)) for p in points])
                emit('Inlet_flow_'+str(sign),verts,faces,uvs,'sediment')
            continue
        # Near-continuous damp low line; washouts and local grit interrupt it.
        if rng.random()<.07 and not ('_0_0' in ob.name or '_0_1' in ob.name or ob.name.startswith('Corner_')):continue
        corner='Corner_' in ob.name and 'WalkCorner' not in ob.name
        points=[ob.matrix_world@v.co for v in ob.data.vertices]
        ob.data.calc_loop_triangles();bvh=BVHTree.FromPolygons(points,[tuple(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
        qs=(-.25,-.132,-.014)
        if corner:
            start=0;end=24
            a0=start*math.pi/48;a1=end*math.pi/48
            # Include EVERY geometric joint station. The radial factor keeps
            # new joint stations on the original polygonal curb, not a circle.
            angles={}
            for vertex in ob.data.vertices:
                x,y=vertex.co.x,vertex.co.y;r=math.hypot(x,y)
                if abs(r-(RADIUS+GUTTER))>.005:continue
                t=math.atan2(-y,-x)
                if a0-1e-6<=t<=a1+1e-6:angles[round(t,8)]=(t,r/(RADIUS+GUTTER))
            rows=sorted(angles.values(),reverse=True);vertices=[]
            for t,factor in rows:
                # Keep ray probes just inside the open tangent ends.
                t=max(.00001,min(math.pi/2-.00001,t))
                for q in qs:
                    r=(RADIUS-q)*factor
                    p=ob.matrix_world@Vector((-r*math.cos(t),-r*math.sin(t),1))
                    hit,normal,_,_=bvh.ray_cast(p,Vector((0,0,-1)))
                    if hit is None:raise RuntimeError('Unfitted corner deposit '+ob.name)
                    vertices.append(tuple(hit+Vector((0,0,DECAL_OFFSET+.001))))
            card('Flow_sediment_'+ob.name,vertices,'sediment',(3,len(rows)))
        else:
            half=(LENGTH if 'Driveway' in ob.name else BAY)/2
            y0=-half+.004;y1=half-.004
            # Include every joint/flare row before ray fitting. Interpolating
            # over a narrow recess can otherwise put the card BELOW the slab.
            rows=sorted(set([y0+(y1-y0)*j/16 for j in range(17)]+[float(v.co.y) for v in ob.data.vertices if y0<v.co.y<y1]))
            loc=[]
            for y in rows:
                for q in qs:
                    p=ob.matrix_world@Vector((q,y,1));hit,normal,_,_=bvh.ray_cast(p,Vector((0,0,-1)))
                    if hit is None:raise RuntimeError('Unfitted sediment '+ob.name)
                    loc.append(tuple(hit+Vector((0,0,DECAL_OFFSET+.001))))
            card('Flow_sediment_'+ob.name,loc,'sediment',(3,len(rows)))
            if rng.random()<.28 and 'Ramp' not in ob.name:
                # Curb scuffs lie on the battered face, with a measured geometric offset.
                pts=[]
                cy=rng.choice((-1,1))*rng.uniform(.6,.9)
                for y,z in [(cy-.45,.035),(cy+.45,.035),(cy+.45,.075),(cy-.45,.075)]:
                    p=ob.matrix_world@Vector((-.3,y,z));direction=ob.matrix_world.to_3x3()@Vector((1,0,0))
                    hit,normal,_,_=bvh.ray_cast(p,direction)
                    if hit is None:break
                    pts.append(tuple(hit-direction*DECAL_OFFSET))
                if len(pts)==4:card('Parking_scuff_'+ob.name,[pts[1],pts[0],pts[2],pts[3]],'scuff')
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('surface_kind')!='Concrete' or not ('_Walk' in ob.name and '_slab' in ob.name) or 'Corner' in ob.name:continue
        if rng.random()>.36:continue
        # Faint, broken damp/soil staining where runoff meets the planting edge.
        y0=rng.uniform(-.7,-.25);y1=rng.uniform(.25,.7);vertices=[]
        ob.data.calc_loop_triangles()
        points=[ob.matrix_world@v.co for v in ob.data.vertices]
        bvh=BVHTree.FromPolygons(points,[tuple(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
        for y in (y0,-.012,-.005,-.0015875,.0015875,.005,.012,y1):
            for x in (.013,rng.uniform(.22,.38)):
                p=ob.matrix_world@Vector((x,y,1));hit,normal,_,_=bvh.ray_cast(p,Vector((0,0,-1)))
                if hit is None:raise RuntimeError('Unfitted sidewalk stain '+ob.name)
                vertices.append(tuple(hit+Vector((0,0,DECAL_OFFSET))))
        card('Planter_damp_'+ob.name,vertices,'stain',(2,8))
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or not ob.parent or ob.parent.get('module')!='Driveway_Slab' or '_slab1__' not in ob.name:continue
        ob.data.calc_loop_triangles();points=[ob.matrix_world@v.co for v in ob.data.vertices]
        tree=BVHTree.FromPolygons(points,[tuple(t.vertices) for t in ob.data.loop_triangles if ob.data.materials[t.material_index].name=='Concrete'],all_triangles=True)
        for j,(cx,cy,sx,sy) in enumerate(((1.5,0,.70,.48),(1.1,.17,.18,.20),(1.82,-.17,.24,.15))):
            vertices=[]
            for y in (-.5,.5):
                for x in (-.5,.5):
                    p=ob.matrix_world@Vector((cx+x*sx,cy+y*sy,1));hit,_,_,_=tree.ray_cast(p,Vector((0,0,-1)))
                    if hit is None:raise RuntimeError('Parked driveway oil support')
                    vertices.append(tuple(hit+Vector((0,0,.003))))
            card('Driveway_parked_engine_'+str(j)+ob.name,vertices,'oil')
    return report
