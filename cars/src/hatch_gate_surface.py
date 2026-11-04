"""Fair the gate's shallow draw in its physical X/Z chart.

The radial control-net fit sampled the 47 mm hollow too sparsely. Its evaluated
parent carries up to 3.6 mm of draw error and a wavering reflection, even at high
density. Use the original continuous die field in that local run. Blend back
to the held parent at the lamps, perimeter and lower hem; retain every cut.
"""
import math
import bpy,bmesh
from mathutils import Vector
from hatch_body import section_field,smoothstep
from hatch_reference_surface import field


def apply(b):
    ob=bpy.data.objects['Liftgate outer'];me=ob.data
    matrix=ob.matrix_world;inverse=matrix.inverted();nm=matrix.to_3x3().transposed()
    parent=field();cache={}
    def surface(x,z):
        key=(round(x,7),round(z,7))
        if key in cache:return cache[key]
        p,n,_=parent((x,3,z),(0,-1,0))
        w=(1-smoothstep(.54,.635,abs(x)))*smoothstep(.650,.695,z)*(1-smoothstep(.945,.982,z))
        lo,hi=1.8,2.3
        for _ in range(30):
            y=(lo+hi)/2
            if section_field((x,y,z))>0:hi=y
            else:lo=y
        y=p.y+w*((lo+hi)/2-p.y)
        cache[key]=(y,p.y);return cache[key]
    def normal(x,z):
        h=.00015
        dx=(surface(x+h,z)[0]-surface(x-h,z)[0])/(2*h)
        dz=(surface(x,z+h)[0]-surface(x,z-h)[0])/(2*h)
        return Vector((-dx,1,-dz)).normalized()
    saved=me.attributes.new('H120 gate held normals','FLOAT_VECTOR','CORNER')
    for r,n in zip(saved.data,me.corner_normals):r.vector=n.vector
    role=me.attributes.get('hatch_outer_skin')
    if role is None:
        role=me.attributes.new('hatch_outer_skin','INT','FACE')
        for f in me.polygons:role.data[f.index].value=int(f.index<ob['outer_skin_faces'])
    maximum=0
    for v in me.vertices:
        p=matrix@v.co
        if not (-.636<p.x<.636 and .650<p.z<.982):continue
        y,py=surface(p.x,p.z);delta=y-py;maximum=max(maximum,abs(delta))
        p.y+=delta;v.co=inverse@p
    bm=bmesh.new();bm.from_mesh(me);outer=bm.faces.layers.int['hatch_outer_skin'];candidates=[]
    for e in bm.edges:
        if len(e.link_faces)!=2 or not all(f[outer] for f in e.link_faces):continue
        a,c=[matrix@v.co for v in e.verts];p=(a+c)/2
        if not (abs(p.x)<.54 and .73<p.z<.94) or e.calc_length()<.018:continue
        angle=normal(p.x,p.z).angle((normal(a.x,a.z)+normal(c.x,c.z)).normalized())
        if angle>math.radians(.15):candidates.append((angle,e))
    bm.edges.index_update();limit=128 if b.high else 64;added=0
    for angle,e in sorted(candidates,key=lambda r:(-r[0],r[1].index))[:limit]:
        a,c=e.verts;p=matrix@((a.co+c.co)/2);p.y=surface(p.x,p.z)[0]
        _,v=bmesh.utils.edge_split(e,a,.5);v.co=inverse@p;added+=1
    bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3]);bm.to_mesh(me);bm.free()
    saved=me.attributes['H120 gate held normals'];role=me.attributes['hatch_outer_skin'];custom=[]
    for f in me.polygons:
        for li in f.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co;old=saved.data[li].vector.copy()
            if -.636<p.x<.636 and .650<p.z<.982 and f.use_smooth:
                n=nm@normal(p.x,p.z)
                custom.append(n if role.data[f.index].value else -n if old.dot(n)<-.5 else old)
            else:custom.append(old)
    me.normals_split_custom_set(custom);me.attributes.remove(saved)
    ob['gate_fairing_max_m']=maximum;ob['gate_reflection_samples']=added
    print('H120_GATE_FAIR',maximum,'m; added samples',added,flush=True)
