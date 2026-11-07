"""Small batched family construction; uses kit normals and stock PBR export.

Each batch becomes one module mesh, with separate children for real leaves.
No global scene names, downloaded resources or machine-specific paths.
"""
import math
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
from kit import tiling

M = {}
ROOT = Path(__file__).resolve().parents[2]


def material(name, color, rough=.8, metal=0, emission=0, transmission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1)
    b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal
    b.inputs['Emission Color'].default_value=(*color,1);b.inputs['Emission Strength'].default_value=emission
    b.inputs['Transmission Weight'].default_value=transmission
    m['checkpoint_material']=True;m['tiling_vertex_tint']=False
    return m


def palette():
    M.clear()
    # Blender 5.2's importer expects all current settings sockets. The kit's
    # minimal AO group is sufficient for export but collides on a later import.
    # Complete that local scene interface, leaving the shared toolkit untouched.
    group=bpy.data.node_groups.get('glTF Material Output')
    if group is None:
        from io_scene_gltf2.blender.com.material_helpers import create_settings_group
        create_settings_group('glTF Material Output')
    else:
        existing={i.name for i in group.interface.items_tree}
        for key,default in (('Thickness',0),('Dispersion',0),('Iridescence Factor',0),('Iridescence Thickness Minimum',100)):
            if key not in existing:group.interface.new_socket(key,in_out='INPUT',socket_type='NodeSocketFloat').default_value=default
    for key,color,rough,metal in [('Concrete',(.34,.325,.29),.86,0),('Deck',(.27,.265,.245),.88,0),
         ('Steel',(.065,.074,.072),.48,.65),('Seal',(.022,.024,.023),.85,0),('Yellow',(.57,.33,.035),.58,0),
         ('Blue',(.025,.105,.20),.64,0),('White',(.73,.72,.65),.65,0),('Red',(.23,.028,.018),.6,0),
         ('Patch',(.25,.25,.23),.88,0)]:M[key]=material('Garage form '+key,color,rough,metal)
    M['Glass']=material('Garage form glass',(.88,.94,.95),.06,transmission=1)
    M['Light']=material('Garage form fluorescent',(.80,.74,.55),.4,emission=5)
    for key in ('Asphalt','Concrete','Lawn','GroundTrim'):
        if key=='Concrete':continue
        M[key]=tiling.material(key,ROOT/'ground/textures/ship',alpha=key=='GroundTrim')
    m=material('GroundParkingTrim form extension',(1,1,1),.75)
    t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(Path('textures/checkpoint/T_GroundParkingTrim_BaseColor.png').resolve()),check_existing=True)
    l=m.node_tree.links;p=m.node_tree.nodes.get('Principled BSDF');l.new(t.outputs['Color'],p.inputs['Base Color']);l.new(t.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
    M['Graphics']=m


def root(name, pos=(0,0,0), parent=None, **props):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o.location=pos
    for k,v in props.items():o[k]=v
    return o


class Mesh:
    def __init__(self,name,parent=None,xf=None):
        self.name=name;self.parent=parent;self.xf=xf or (lambda p:Vector(p));self.v=[];self.f=[];self.m=[];self.uv=[]
    def geom(self,vs,fs,mat='Concrete',uv=None):
        start=len(self.v);self.v.extend(tuple(self.xf(p)) for p in vs)
        for f in fs:
            self.f.append(tuple(start+i for i in f));self.m.append(mat);self.uv.append(uv)
    def box(self,p,s,mat='Concrete'):
        x,y,z=p;a,b,c=(q/2 for q in s)
        self.geom([(x+i*a,y+j*b,z+k*c) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))],
                  [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
    def prism(self,poly,delta,mat='Concrete'):
        n=len(poly);vs=poly+[tuple(Vector(p)+Vector(delta)) for p in poly]
        self.geom(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
    def beam(self,a,b,w,d=None,mat='Steel'):
        a,b=Vector(a),Vector(b);t=b-a;q=t.to_track_quat('Z','Y').to_matrix();h=(w/2,(d or w)/2,t.length/2)
        self.geom([(a+b)/2+q@Vector((i*h[0],j*h[1],k*h[2])) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
    def tube(self,pts,r,mat='Steel',n=8):
        vs=[]
        for j,p in enumerate(pts):
            t=Vector(pts[min(j+1,len(pts)-1)])-Vector(pts[max(j-1,0)]);t.normalize();u=t.cross(Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))).normalized();v=t.cross(u)
            vs.extend(Vector(p)+r*(u*math.cos(i*math.tau/n)+v*math.sin(i*math.tau/n)) for i in range(n))
        self.geom(vs,[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(pts)-1) for i in range(n)],mat)
    def quad(self,vs,rect=None,mat='GroundTrim'):
        if rect is None:rect=(.04,.81,.46,.95)
        a,b,c,d=rect;self.geom(vs,[(0,1,2,3)],mat,[(a,b),(c,b),(c,d),(a,d)])
    def finish(self):
        if not self.v:return None
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        keys=list(dict.fromkeys(self.m))
        for k in keys:me.materials.append(M[k])
        ob=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(ob);ob.parent=self.parent
        uv=me.uv_layers.new(name='UVMap')
        for p,key,coords in zip(me.polygons,self.m,self.uv):
            p.material_index=keys.index(key)
            axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
            for j,li in enumerate(p.loop_indices):
                v=me.vertices[me.loops[li].vertex_index].co
                uv.data[li].uv=coords[j] if coords else (v[axes[0]]/(6.096 if key=='Asphalt' else 3.048),v[axes[1]]/3.048)
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        ob['asset_set']='ParkingGarage';return ob


def clone(rt,name,pos=(0,0,0),yaw=0,parent=None,xf=None):
    obs=[rt,*rt.children_recursive];copies={o:o.copy() for o in obs}
    for o,c in copies.items():
        bpy.context.collection.objects.link(c);c.parent=copies.get(o.parent);c.name=name if o==rt else name+'__'+o.name
        c.matrix_basis=o.matrix_basis.copy()
        if xf and c.type=='MESH':
            c.data=c.data.copy()
            for v in c.data.vertices:v.co=xf(v.co)
            bm=bmesh.new();bm.from_mesh(c.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(c.data);bm.free();c.data.update()
    r=copies[rt];r.parent=parent;r.location=pos;r.rotation_euler=(0,0,math.radians(yaw));return r


def bounds(obs):
    bpy.context.view_layer.update();ps=[o.matrix_world@v.co for o in obs if o.type=='MESH' for v in o.data.vertices]
    return [[float(fn(v[i] for v in ps)) for i in range(3)] for fn in (min,max)]


def triangles(obs):return sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in obs if o.type=='MESH')
