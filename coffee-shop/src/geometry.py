"""Small batched construction meshes with atlas charts and physical stock."""
import math
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
from kit import model as G,tiling

LAYOUT={};MATS=[]
ROLES=[]
ALPHA=('mesh','vinyl','ring','spill','scuff','drip','crack','chalk_smear')


def palette(folder=Path('build/atlas')):
    import json
    global LAYOUT,MATS
    LAYOUT=json.loads((folder/'layout.json').read_text())
    # The stock 5.2 importer expects its complete settings interface when
    # importing a library piece into an existing atlas scene.
    from io_scene_gltf2.blender.com.material_helpers import create_settings_group
    if not bpy.data.node_groups.get('glTF Material Output'):create_settings_group('glTF Material Output')
    folder=Path('textures/ship') if Path('textures/ship/T_CoffeeShop_Normal.png').exists() else folder
    opaque=tiling.material('CoffeeShop',folder,tint=True);opaque.use_backface_culling=False
    glass=bpy.data.materials.new('CoffeeShop_Glass');glass.use_nodes=True
    p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.96,.98,.97,1);p.inputs['Transmission Weight'].default_value=1;p.inputs['Roughness'].default_value=.003;p.inputs['IOR'].default_value=1.5
    glass['tiling_vertex_tint']=False
    perforated=tiling.material('CoffeeShop',folder,alpha=True,tint=True);perforated.name='CoffeeShop_Cutout';perforated.use_backface_culling=False
    pbs=perforated.node_tree.nodes.get('Principled BSDF');links=perforated.node_tree.links;alpha_source=pbs.inputs['Alpha'].links[0].from_socket
    cutoff=perforated.node_tree.nodes.new('ShaderNodeMath');cutoff.operation='GREATER_THAN';cutoff.inputs[1].default_value=.45;links.new(alpha_source,cutoff.inputs[0]);links.new(cutoff.outputs[0],pbs.inputs['Alpha'])
    MATS=[opaque,glass,perforated];return MATS


def root(name,loc=(0,0,0),parent=None,**props):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc;o.parent=parent
    for k,v in props.items():o[k]=v
    return o


def socket(name,loc,parent,kind,**props):return root(name,loc,parent,socket_kind=kind,**props)


class Batch:
    def __init__(self,name,parent=None):
        self.name=name;self.parent=parent;self.v=[];self.f=[];self.uv=[];self.mat=[];self.smooth=[];self.roles=[]
    def geom(self,vs,fs,role='black',uv=None,smooth=False):
        n=len(self.v);self.v.extend(tuple(v) for v in vs)
        for f in fs:
            self.f.append(tuple(n+i for i in f));self.mat.append(1 if role=='glass' else 2 if role in ALPHA else 0);self.smooth.append(smooth);self.roles.append(role)
            if uv:self.uv.append(uv)
            else:
                a,b,c,d=LAYOUT.get(role,LAYOUT['black']);self.uv.append([(a,b),(c,b),(c,d),(a,d)][:len(f)] if len(f)<=4 else [((a+c)/2,(b+d)/2)]*len(f))
    def box(self,p,s,role='black'):
        x,y,z=p;a,b,c=(v/2 for v in s)
        vs=[(x+i*a,y+j*b,z+k*c) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        self.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role)
    def rounded(self,p,s,r,role='black',segments=3):
        # Rounded extrusion with separate small bevel rings and full gauge.
        x,y,z=p;w,d,h=s;r=min(r,w/2-.00001,d/2-.00001,h/2-.00001)
        rings=[]
        for zz,inset in ((-h/2,r*.3),(-h/2+r*.3,0),(h/2-r*.3,0),(h/2,r*.3)):
            rings.append([(x+a,y+b,z+zz) for a,b in G.rounded_rectangle(w-2*inset,d-2*inset,max(.00001,r-inset),segments)])
        self.loft(rings,role,smooth=True)
    def loft(self,rings,role='black',caps=True,closed=True,smooth=False):
        n=len(rings[0]);vs=[v for ring in rings for v in ring]
        fs=[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(rings)-1) for k in range(n if closed else n-1)]
        self.geom(vs,fs,role,smooth=smooth)
        if caps:self.geom(vs,[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))],role)
    def tube(self,pts,r,role='black',sides=8):
        pts=list(map(Vector,pts));rings=[]
        for i,p in enumerate(pts):
            t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized();u=t.cross(Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))).normalized();v=t.cross(u)
            rings.append([p+r*(u*math.cos(k*math.tau/sides)+v*math.sin(k*math.tau/sides)) for k in range(sides)])
        self.loft(rings,role,smooth=True)
    def cylinder(self,p,r,h,role='black',n=24):
        x,y,z=p;self.loft([[(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),z+zz) for i in range(n)] for zz in (-h/2,h/2)],role,smooth=True)
    def lathe(self,profile,role='black',n=24,center=(0,0)):
        self.loft([[(center[0]+r*math.cos(i*math.tau/n),center[1]+r*math.sin(i*math.tau/n),z) for i in range(n)] for z,r in profile],role,caps=False,smooth=True)
    def beam(self,a,b,w,d=None,role='black'):
        a,b=Vector(a),Vector(b);q=(b-a).to_track_quat('Z','Y').to_matrix();p=(a+b)/2
        vs=[p+q@Vector((i*w/2,j*(d or w)/2,k*(b-a).length/2)) for i,j,k in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        self.geom(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role)
    def print(self,verts,key):
        a,b,c,d=LAYOUT[key];self.geom(verts,[(0,1,2,3)],key,[(a,b),(c,b),(c,d),(a,d)])
    def panel(self,x,y,z,w,h,key):self.print([(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],key)
    def finish(self):
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
        for m in MATS:me.materials.append(m)
        uv=me.uv_layers.new(name='UVMap');tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');semantic=me.attributes.new(name='CafeRole',type='INT',domain='FACE')
        for p,mi,sm,coords,role in zip(me.polygons,self.mat,self.smooth,self.uv,self.roles):
            if role not in ROLES:ROLES.append(role)
            semantic.data[p.index].value=ROLES.index(role)
            p.material_index=mi;p.use_smooth=sm
            for j,li in enumerate(p.loop_indices):uv.data[li].uv=coords[j];tint.data[li].color=(1,1,1,1)
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='FIXED',ngon_method='EAR_CLIP');bm.to_mesh(me);bm.free();me.update()
        o=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(o);o.parent=self.parent;o['asset_set']='CoffeeShop';o['cafe_roles']=__import__('json').dumps(ROLES);return o


def descendants(o):return [o]+list(o.children_recursive)


def clone(source,name,position,parent=None,yaw=0):
    mapping={}
    for old in descendants(source):
        new=old.copy();new.name=name if old==source else name+'__'+old.name; bpy.context.collection.objects.link(new);mapping[old]=new
    for old,new in mapping.items():new.parent=mapping.get(old.parent,parent)
    ob=mapping[source];ob.location=position;ob.rotation_mode='XYZ';ob.rotation_euler=(0,0,math.radians(yaw));return ob
