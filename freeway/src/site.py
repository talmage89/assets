"""Native library context, terrain interfaces and reusable placement helpers."""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
import geom as Q
from plan import *
ROOT=Path(__file__).resolve().parents[2]

def load(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    added=set(bpy.context.scene.objects)-before
    # glTF imports COLOR_0 as an active layer called Color. Assembly exports
    # deliberately select Tint; retain native house/commercial color through
    # this second import/export instead of silently dropping it. Wind data is
    # independent and must never become an albedo multiplier.
    for ob in added:
        if ob.type!='MESH':continue
        readers=[node for ma in ob.data.materials if ma and ma.use_nodes for node in ma.node_tree.nodes if node.type=='VERTEX_COLOR']
        if not readers:continue
        color=ob.data.color_attributes.active_color
        if color is None:continue
        color.name='Tint';ob.data.color_attributes.active_color=color
        for node in readers:node.layer_name='Tint'
    roots=sorted((o for o in added if o.parent not in added),key=lambda o:o.name)
    rt=Q.root('Template_'+Path(path).stem)
    for ob in roots:
        # Some imports add a global axis transform. Keep the world matrix.
        mat=ob.matrix_world.copy();ob.parent=rt;ob.matrix_world=mat
    return rt

def clone(src,name,loc=(0,0,0),yaw=0,parent=None):
    mapping={}
    for ob in [src,*src.children_recursive]:
        cp=ob.copy()
        if ob.type=='CURVE':cp.data=ob.data.copy()
        bpy.context.collection.objects.link(cp);mapping[ob]=cp
    for ob,cp in mapping.items():
        cp.parent=mapping.get(ob.parent,parent);cp.matrix_basis=ob.matrix_basis.copy()
    rt=mapping[src];rt.name=name;rt.location=loc;rt.rotation_euler=(0,0,math.radians(yaw));rt['placement_id']=name
    return rt

def delete(rt):
    bpy.data.batch_remove(ids=set([rt,*rt.children_recursive]))

def along(src,name,p,s,u,zoff=0,yaw=0,parent=None):
    point=p.xyz(s,u,zoff);a=math.degrees(math.atan2(p.frame(s)[1][0],p.frame(s)[1][1]))
    return clone(src,name,point,-a+yaw,parent)

def planted_truss(name,p,s,yaw=0):
    """Keep the truss level; found each unequal leg on actual graded earth."""
    from mathutils import Matrix
    from mathutils.bvhtree import BVHTree
    import pieces
    bpy.context.view_layer.update()
    earth=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Cut slopes and drainage'))
    tree=BVHTree.FromObject(earth,bpy.context.evaluated_depsgraph_get())
    point=Vector(p.xyz(s,0));angle=-(s/p.radius if p.radius else 0)+math.radians(yaw)
    rotation=Matrix.Rotation(angle,4,'Z');feet=[]
    for x in (-17.,17.):
        q=point+rotation@Vector((x,0,0));hit=tree.ray_cast(Vector((q.x,q.y,100)),Vector((0,0,-1)),200)[0]
        assert hit is not None
        feet.append(hit.z-point.z-.30)
    rt=pieces.truss(name,foot_bases=feet,foot_depth=.56);rt.location=point;rt.rotation_euler.z=angle
    return rt

def rail_run(lib,name,points):
    """Continuous 12 ft 6 in post-pitch panels with lap joints and vertical posts.

    Each copied mesh follows the local grade by shear, rather than pitching its
    posts or leaving horizontal stair steps between panels on the ramp.
    """
    points=list(map(Vector,points));lengths=[0.]
    for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+math.hypot(b.x-a.x,b.y-a.y))
    def sample(distance):
        for j in range(len(lengths)-1):
            if distance<=lengths[j+1]:
                t=(distance-lengths[j])/(lengths[j+1]-lengths[j]);return points[j].lerp(points[j+1],max(0,min(1,t)))
        return points[-1]
    result=[];segments=[(0.,7.62,'GuardrailEnd')]
    a=7.62
    while a+3.81<=lengths[-1]:segments.append((a,a+3.81,'WBeam'));a+=3.81
    for index,(a,b,kind) in enumerate(segments):
        middle=(a+b)/2;pt=sample(middle);delta=sample(min(lengths[-1],middle+.5))-sample(max(0,middle-.5));span=math.hypot(delta.x,delta.y)
        normal=Vector((delta.y,-delta.x,0)).normalized();pt+=normal*4.9;pt.z-=.12
        ob=clone(lib[kind],name+'_%03d'%index,pt,math.degrees(math.atan2(-delta.x,delta.y)));slope=delta.z/span
        for mesh in ob.children_recursive:
            if mesh.type!='MESH':continue
            mesh.data=mesh.data.copy();normals=[n.vector.copy() for n in mesh.data.corner_normals]
            for v in mesh.data.vertices:
                v.co.z+=v.co.y*slope
                if getattr(Q,'LOOKDEV',False) and index%29==11 and kind=='WBeam':v.co.x-=.055*math.sin(math.pi*(v.co.y+1.905)/3.81)**2
            if getattr(Q,'LOOKDEV',False) and index%29 in (12,13):
                mesh['maintenance']='replacement galvanized bay'
                attr=mesh.data.color_attributes.get('Tint')
                if attr:
                    for value in attr.data:value.color=(1.12,1.12,1.10,1)
            mesh.data.update()
            for f in mesh.data.polygons:f.use_smooth=True
            mesh.data.normals_split_custom_set([Vector((n.x,n.y-slope*n.z,n.z)).normalized() for n in normals])
        result.append(ob)
    return result

def town(p):
    from neighborhood import town as build_town
    return build_town(p)

def traffic(p):
    from neighborhood import traffic as build_traffic
    return build_traffic(p)

def terminal_signals(p):
    rt=Q.root('RampTerminalSignals',module_kind='signals');lib=load('build/context/Signal.glb')
    # Two arterial far-side mast pairs, plus a ramp-facing mast at each T.
    for side in (-1,1):
        x=side*p.terminal
        for j,(dx,y,yaw) in enumerate(((8.8,-10.0,90),(-8.8,10.,-90),(9.2,11.,0 if side>0 else 180))):
            clone(lib,'Terminal_'+str(side)+'_Mast'+str(j),(x+dx,y,7.35),yaw,rt)
    delete(lib);return rt

def row_fence(p):
    """ROW woven wire, native family convention: steel poles + alpha panel.

    A quick panel is used until the shared fence bake is available locally.
    No residential four-foot fabric is stretched into a freeway sound wall.
    """
    rt=Q.root('RightOfWayFence',module_kind='fence');b=Q.Batch('ROW posts and fabric',rt)
    for side in (-1,1):
        u=side*(106 if p.kind=='diamond' else 40.)
        runs=[(-p.length/2,-11.),(11.,p.length/2)] if p.kind=='diamond' else [(-p.length/2,p.length/2)]
        posts=seq(-p.length/2,p.length/2,3.048)
        if p.kind=='diamond':posts=[s for s in posts if abs(s)>=11]+[-11.,11.]
        for s in sorted(posts):
            x,y,z=p.xyz(s,u);z=7.0 if p.kind=='diamond' else 0
            b.tube([(x,y,z),(x,y,z+1.83)],.024,'Steel',4,caps=False)
        chain=seq(-p.length/2,p.length/2,6.096)
        for a,c in zip(chain,chain[1:]):
            spans=[(max(a,l),min(c,r)) for l,r in runs if min(c,r)>max(a,l)]
            for a,c in spans:
                x0,y0,_=p.xyz(a,u);x1,y1,_=p.xyz(c,u);z=7.0 if p.kind=='diamond' else 0
            # Original chain-link's physical 0.3048 m repeat, shared across
            # all placements. It represents manufacture, not repeated wear.
                b.face([(x0,y0,z+.06),(x1,y1,z+.06),(x1,y1,z+1.80),(x0,y0,z+1.80)],'Fence',uv=[(a/.3048,0),(c/.3048,0),(c/.3048,1.74/.3048),(a/.3048,1.74/.3048)])
        for h in (.06,1.80):
            stations=seq(-p.length/2,p.length/2,12.192)
            for l,r in runs:
                pts=[]
                for s in sorted({l,r,*[s for s in stations if l<s<r]}):
                    x,y,z=p.xyz(s,u);pts.append((x,y,(7.0 if p.kind=='diamond' else 0)+h))
                b.tube(pts,.0025,'DarkSteel',3)
    b.finish();return rt

def seq(a,b,step):
    n=math.ceil((b-a)/step);return [a+(b-a)*i/n for i in range(n+1)]
