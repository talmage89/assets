"""Use main's native bridge factories without altering their fixed delivery.

The town retains the smaller cited Type III section. This adapter changes
section/length, bent stations and height without making columns elliptical.
Freeway's Type IV example, source files and canonical exports stay untouched.
"""
import importlib
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector
import geometry as G

_NATIVE=None
_BEARING=None


def native():
    global _NATIVE
    if _NATIVE is None:
        folder=str(Path(__file__).resolve().parents[2]/'freeway/src')
        names=('geom','plan','graphics','pieces');saved={n:sys.modules.get(n) for n in names}
        sys.path.insert(0,folder)
        try:
            for n in names:sys.modules.pop(n,None)
            modules={n:importlib.import_module(n) for n in names}
            _NATIVE=(modules['geom'],modules['pieces'])
        finally:
            sys.path.remove(folder)
            for n in names:
                sys.modules.pop(n,None)
                if saved[n] is not None:sys.modules[n]=saved[n]
    q,p=_NATIVE;q.M.clear()
    mapping={'Bridge':'bridge_concrete','Barrier':'bridge_concrete','Concrete':'concrete',
             'Steel':'zinc','DarkSteel':'steel','Rubber':'rubber','Joint':'rubber',
             'Wood':'wood','Yellow':'yellow','Drain':'steel','Asphalt':'asphalt'}
    q.M.update({a:G.M[b] for a,b in mapping.items()});q.LOOKDEV=False
    return q,p


def tag(root,parent=None):
    root.parent=parent;root['source_factory']='freeway/src/pieces.py on main'
    for ob in G.descendants(root):
        if ob.type=='MESH':ob['river_category']='bridge'
    return root


def uv_meters(mesh):
    mesh.update();uv=mesh.uv_layers.active
    for face in mesh.polygons:
        n=face.normal;axes=(0,1) if abs(n.z)>=max(abs(n.x),abs(n.y)) else ((1,2) if abs(n.x)>abs(n.y) else (0,2))
        for li in face.loop_indices:
            p=mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv=(p[axes[0]]/3.048,p[axes[1]]/3.048)


def girder(name,length,section,parent=None):
    q,p=native();old=p.GIRDER
    try:
        p.GIRDER=section;root=p.girder(name,length)
    finally:p.GIRDER=old
    mesh=next(o.data for o in root.children if o.type=='MESH');flat=length/24
    for v in mesh.vertices:
        t=(v.co.x+length/2)/length
        z=v.co.z-.018*math.sin(math.pi*t)
        u=max(0,min(1,(v.co.x+length/2-flat)/(length-2*flat)))
        v.co.z=z+.012*4*u*(1-u)
    uv_meters(mesh)
    mesh.normals_split_custom_set([face.normal for face in mesh.polygons for _ in face.loop_indices])
    for ob in root.children:
        if ob.type=='EMPTY':
            ob.location.x+=.26 if ob.location.x<0 else -.26
            ob.rotation_euler=(0,0,0);ob['socket_kind']='bearing'
    root['module']='TypeIII_Girder';root['length_m']=length
    return tag(root,parent)


def columns(name,width,height,parent=None):
    q,p=native();root=p.pier(name);mesh=next(o.data for o in root.children if o.type=='MESH')
    normals=[n.vector.copy() for n in mesh.corner_normals]
    source_top=7.10-1.3716-.15-.14;source_body=source_top-.98
    for v in mesh.vertices:
        if abs(v.co.x)<.8:
            station=min((-7,0,7),key=lambda y:abs(v.co.y-y))
            v.co.y+=station/7*(width*.29-7)
            v.co.z=(height-source_top+v.co.z) if v.co.z>=source_body-1e-5 else -1.3+(v.co.z+.05)/(source_body+.05)*(height-.98+1.3)
        else:
            v.co.y*=((width/2-.3)/9.9);v.co.z+=height-source_top
    uv_meters(mesh);mesh.normals_split_custom_set(normals)
    for ob in root.children:
        if ob.type=='EMPTY':ob.location.z=height;ob['socket_kind']='cap_top'
    feet=G.Batch(name+'__BuriedFootings',root)
    for y in (-width*.29,0,width*.29):feet.box((0,y,-1.42),(1.95,1.95,.36),'bridge_concrete')
    feet.finish();return tag(root,parent)


def parapet(name,length,parent=None):
    q,p=native();root=p.barrier(name+'__FreewayF',length,scupper=False)
    wrapper=G.root(name,parent=parent,module='Freeway_F_Parapet')
    root.parent=wrapper;root.rotation_euler.z=math.pi/2
    joints=G.Batch(name+'__EndSeals',wrapper)
    for s in (-1,1):joints.box((s*(length/2-.04),0,.81),(.012,.1524,.012),'rubber')
    joints.finish();tag(root,wrapper);return wrapper


def guardrail(name,length,parent=None):
    q,p=native();root=p.guardrail(name+'__FreewayEnd',length,terminal=True)
    wrapper=G.root(name,parent=parent,module='Freeway_GuardrailEnd')
    root.parent=wrapper;root.rotation_euler.z=math.pi/2
    tag(root,wrapper)
    return wrapper


def bearing_faces():
    """Extract one native three-layer assembly, before adapting its dimensions.

    Selection is spatial/material based on the actual native overpass mesh;
    no native face, profile or layer topology is copied into this script.
    Cached values contain no Blender IDs and survive clean scene resets.
    """
    global _BEARING
    if _BEARING is not None:return _BEARING
    q,p=native();root=p.bridge('NativeBearingExtraction')
    try:
        mesh=next(o.data for o in root.children if o.type=='MESH')
        roles={q.M['Bridge']:'bridge_concrete',q.M['Steel']:'zinc',q.M['Rubber']:'rubber'}
        found=[]
        for face in mesh.polygons:
            points=[mesh.vertices[i].co.copy() for i in face.vertices]
            material=mesh.materials[face.material_index]
            if material not in roles:continue
            if not all(.20<v.x<1.10 and abs(v.y)<.40 and 5.43<v.z<5.74 for v in points):continue
            found.append(([tuple(v) for v in points],roles[material]))
        assert len(found)==36,('Native bearing extraction',len(found))
        _BEARING=found
    finally:
        for ob in reversed(G.descendants(root)):bpy.data.objects.remove(ob,do_unlink=True)
    return _BEARING


def bearing(batch,x,y,z):
    faces=bearing_faces()
    bounds={role:(min(v[2] for ps,r in faces if r==role for v in ps),
                  max(v[2] for ps,r in faces if r==role for v in ps))
            for role in ('bridge_concrete','zinc','rubber')}
    heights={'bridge_concrete':(0,.20),'zinc':(.20,.22),'rubber':(.22,.30)}
    for points,role in faces:
        low,high=bounds[role];a,c=heights[role]
        adapted=[(x+(vx-.65)*(.56/.88),y+vy*(.70/.78),z+a+(vz-low)/(high-low)*(c-a)) for vx,vy,vz in points]
        batch.geom(adapted,[(0,1,2)],role)
