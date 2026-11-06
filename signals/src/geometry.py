"""Construction helpers wrapping kit geometry; shared baked trim assignment."""
import math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from kit import model as G
import surfaces
M={};COMPONENTS={}
def mat(name,col,rough=.6,metal=0):
 m=bpy.data.materials.get(name)
 if m:return m
 m=bpy.data.materials.new(name);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 m['trim_role']=name.replace('Form_','');return m
def image_mat(name,path,emit=0,alpha=False,dark=False,emission_path=None):
 m=bpy.data.materials.new(name);m.use_nodes=True;ns=m.node_tree.nodes;ls=m.node_tree.links;p=ns.get('Principled BSDF')
 im=ns.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
 color=im.outputs['Color']
 if dark:
  mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.005,.005,.005,1);ls.new(color,mix.inputs[1]);color=mix.outputs[0]
 ls.new(color,p.inputs['Base Color']);p.inputs['Roughness'].default_value=.30
 if alpha:ls.new(im.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
 if emit:
  em=color
  if emission_path:
   node=ns.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(emission_path.resolve()),check_existing=True);em=node.outputs['Color']
  ls.new(em,p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=emit
 return m
def palette(graphics):
 M.clear();COMPONENTS.clear();surfaces.setup()
 for name,c,r,met in [('zinc',(.25,.28,.28),.65,.8),('green',(.025,.065,.047),.68,.25),('black',(.009,.012,.012),.65,0),('bronze',(.065,.048,.03),.64,.3),('yellow',(.64,.37,.009),.62,0),('inside',(.004,.006,.007),.7,0),('steel',(.27,.29,.29),.42,.9),('white',(.69,.70,.66),.76,0),('concrete',(.32,.33,.30),.94,0),('cabinet',(.31,.34,.34),.55,.78),('rubber',(.008,.009,.008),.9,0),('border',(.72,.49,.008),.5,0)]:
  M[name]=mat('Form_'+name,c,r,met)
 M['off'],M['lit']=surfaces.lenses(graphics)
 M['names']=image_mat('SharedNames',Path('textures/ship/T_Signals_Names.png'))
 M['r10']=mat('Form_r10',(.5,.5,.5))
 M['panel']=mat('Form_panel',(.1,.1,.1));M['record']=mat('Form_record',(.5,.5,.5))
 return M
def root(name,p=(0,0,0),parent=None,kind=None,yaw=0):
 o=G.pivot(name,p);o.parent=parent;o.rotation_euler.z=math.radians(yaw)
 o['part_kind']=kind or name;return o
def own(o,rt):
 o.parent=rt
 if o.type=='MESH':
  ident=int.from_bytes(hashlib.sha256(o.name.encode()).digest()[:4],'little')&0x7fffffff
  assert ident not in COMPONENTS or COMPONENTS[ident]==o.name
  COMPONENTS[ident]=o.name
  attr=o.data.attributes.get('Construction') or o.data.attributes.new(name='Construction',type='INT',domain='FACE')
  for f in attr.data:f.value=ident
  # Resolve manufacturing bevels before projecting trims. Blender bevel UV
  # interpolation can differ by an ULP between clean processes. Mesh geometry
  # is deterministic; assigning from its resolved surfaces removes that drift.
  G.apply(o)
  surfaces.assign(o)
 return o
def box(name,p,sz,ma,rt,r=.002):return own(G.box(name,p,sz,M.get(ma,ma),r,1),rt)
def cyl(name,a,b,r,ma,rt,n=12):return own(G.cylinder(name,a,b,r,M.get(ma,ma),n),rt)
def tube(name,pts,r,ma,rt,n=8):return own(G.tube(name,pts,r,M.get(ma,ma),n),rt)
def mesh(name,vs,fs,ma,rt):return own(G.mesh(name,vs,fs,M.get(ma,ma)),rt)
def profile(name,pts,lo,hi,ma,rt,axis='Y'):
 return own(G.profile(name,pts,lo,hi,M.get(ma,ma),axis=axis),rt)
def quad(name,p,w,h,ma,rt,rect=(0,0,1,1)):
 x,y,z=p;o=G.plane_uv(name,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],M.get(ma,ma))
 uv=o.data.uv_layers.active;u0,v0,u1,v1=rect
 for f in o.data.polygons:
  for li in f.loop_indices:
   a,b=uv.data[li].uv;uv.data[li].uv=(u0+a*(u1-u0),v0+b*(v1-v0))
 return own(o,rt)
def bolt(name,p,d,r,ma,rt):
 # The washer and hex head are real game geometry; fine threads wait for normal.
 a=Vector(p);d=Vector(d).normalized()
 cyl(name+'_washer',a,a+d*r*.28,r*1.8,ma,rt,12)
 return cyl(name+'_hex',a+d*r*.28,a+d*r*1.25,r*1.5,ma,rt,6)
def ring(name,z,r0,r1,h,ma,rt,n=24,center=(0,0)):
 return own(G.lathe(name,[(z,r0),(z,r1),(z+h,r1),(z+h,r0)],M.get(ma,ma),n,center=center,closed=True),rt)
def join_fixed(rt):
 """Consolidate only direct fixed meshes; separate lenses/pivots survive."""
 objs=[o for o in rt.children if o.type=='MESH' and not o.get('signal_lens')]
 if not objs:return
 bpy.context.view_layer.update()
 for o in objs:G.apply(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=objs[0];o.name=rt.name+'__Fixed'
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 return o
def finalize_meshes():
 for o in list(bpy.context.scene.objects):
  if o.type!='MESH':continue
  G.apply(o)
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(o.data);bm.free()
  o.data.calc_loop_triangles()
  mod=o.modifiers.new('Game triangles','TRIANGULATE');G.apply(o)
  if o.get('signal_kind') in ('red','yellow','green','red_arrow','yellow_arrow','green_arrow'):
   # Analytic molded cover normals on the accepted eight-triangle crown.
   # The angular reflection changes continuously without silhouette triangles.
   pts=[v.co for v in o.data.vertices];cx=(min(v.x for v in pts)+max(v.x for v in pts))/2;cz=(min(v.z for v in pts)+max(v.z for v in pts))/2
   for f in o.data.polygons:f.use_smooth=True
   o.data.normals_split_custom_set_from_vertices([Vector(((v.co.x-cx)/.24,-1,(v.co.z-cz)/.24)).normalized() for v in o.data.vertices])
def tri(rt):return sum(len(o.data.loop_triangles) for o in rt.children_recursive if o.type=='MESH')
