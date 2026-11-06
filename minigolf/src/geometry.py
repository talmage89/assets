"""Checkpoint construction helpers using the kit's mesh vocabulary.

Quick swatches deliberately have no manufactured texture or aging shaders.
These are diagnostic external images, replaced during the later look gate.
"""
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
COLORS={
 'carpet':(.018,.225,.055),'carpet2':(.020,.155,.055),'carpet3':(.070,.235,.035),
 'concrete':(.48,.46,.40),'brick':(.30,.095,.055),'mortar':(.20,.195,.17),
 'wood':(.22,.155,.080),'rock':(.27,.255,.215),'rocklight':(.38,.35,.285),
 'red':(.38,.035,.022),'ivory':(.68,.64,.50),'navy':(.02,.06,.10),'white':(.71,.73,.68),
 'black':(.012,.017,.017),'metal':(.32,.34,.33),'rubber':(.012,.015,.014),
 'soil':(.065,.048,.025),'grass':(.12,.18,.045),'asphalt':(.065,.069,.070),
 'yellow':(.67,.37,.025),'leaf':(.22,.14,.035),'liner':(.017,.022,.018),
 'water':(.025,.13,.12),'glass':(.08,.12,.13),'foam':(.65,.69,.61)}
M={};PRINTS={};PRINT_OBJECTS=[];FONT=None

def srgb(v):return 12.92*v if v<=.0031308 else 1.055*v**(1/2.4)-.055

def setup():
 global FONT
 FONT=find_font('DejaVu Sans','Bold')
 out=Path('export/textures');out.mkdir(parents=True,exist_ok=True)
 color=Image.new('RGB',(256,256));orm=Image.new('RGB',(256,256))
 for i,(name,c) in enumerate(COLORS.items()):
  x,y=(i%8)*32,(i//8)*32
  ImageDraw.Draw(color).rectangle((x,y,x+31,y+31),fill=tuple(round(255*srgb(v)) for v in c))
  ImageDraw.Draw(orm).rectangle((x,y,x+31,y+31),fill=(255,80 if name=='metal' else 215,230 if name=='metal' else 0))
  mat=bpy.data.materials.new('Quick_'+name);mat.use_nodes=True
  b=mat.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=.85
  if name=='metal':b.inputs['Metallic'].default_value=.9;b.inputs['Roughness'].default_value=.30
  M[name]=mat
 color.save(out/'T_Minigolf_Quick_BaseColor.png');orm.save(out/'T_Minigolf_Quick_ORM.png')

def root(name,loc=(0,0,0),yaw=0,parent=None,kind=None):
 ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.parent=parent
 ob.location=loc;ob.rotation_euler.z=math.radians(yaw);ob['module_kind']=kind or name;ob['module']=True
 return ob

def own(ob,parent,solid=True):
 ob.parent=parent;ob['solid']=solid;return ob

def box(name,p,size,mat,parent,r=.002,seg=1):return own(G.box(name,p,size,M[mat],r,seg),parent)
def mesh(name,vs,fs,mat,parent,solid=True):return own(G.mesh(name,vs,fs,M[mat]),parent,solid)
def cyl(name,a,b,r,mat,parent,n=12):return own(G.smooth(G.cylinder(name,a,b,r,M[mat],n)),parent)
def tube(name,pts,r,mat,parent,sides=8):return own(G.smooth(G.tube(name,pts,r,M[mat],sides=sides)),parent)
def beam(name,a,b,w,d,mat,parent):
 a,b=Vector(a),Vector(b);ob=box(name,(a+b)/2,(w,d,(b-a).length),mat,parent)
 ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def socket(parent,name,p,kind):
 ob=root(parent.name+'__'+name,p,parent=parent);ob['module']=False;ob['socket_kind']=kind;return ob

def ring(name,c,r,ri,z0,z1,mat,parent,n=32):
 x,y=c;vs=[(x+rad*math.cos(i*math.tau/n),y+rad*math.sin(i*math.tau/n),z) for z,rad in ((z0,r),(z1,r),(z1,ri),(z0,ri)) for i in range(n)]
 fs=[(j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i) for j in range(4) for i in range(n)]
 return mesh(name,vs,fs,mat,parent)

def rock(name,p,size,parent,seed=0,mat='rock'):
 # Asymmetric stratified polyhedron, not stretched spheres. Flat bedding ledges
 # and offset crowns retain sedimentary construction under raking light.
 import random
 rng=random.Random(seed);x,y,z=p;w,d,h=size;n=9
 loops=[]
 for k,(height,fac) in enumerate(((0,.88),(.18,1),(.54,.83),(.78,.74),(1,.38))):
  loops.append([(x+w*.5*(fac*rng.uniform(.86,1.1)*math.cos(i*math.tau/n)+k*.025),y+d*.5*fac*rng.uniform(.88,1.1)*math.sin(i*math.tau/n),z+h*(height+rng.uniform(-.04,.04) if k else 0)) for i in range(n)])
 return own(G.smooth(G.loft(name,loops,M[mat]),48),parent)

def ball(name,p,r,mat,parent):
 profile=[(-r,0)]+[(r*math.sin(-math.pi/2+i*math.pi/6),r*math.cos(-math.pi/2+i*math.pi/6)) for i in range(1,6)]+[(r,0)]
 ob=own(G.smooth(G.lathe(name,profile,M[mat],12),60),parent);ob.location=p;return ob

def text(parent,string,p,w,h,vertical=True):
 # Shared original graphics; geometry is a single correctly faced quad.
 if string not in PRINTS:PRINTS[string]=len(PRINTS)
 x,y,z=p
 vs=[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)] if vertical else [(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)]
 ob=mesh('Graphic '+string,vs,[(0,1,2,3)],'ivory',parent,False);ob['graphic']=string
 PRINT_OBJECTS.append(ob);return ob

def image_material(name,bc,orm=None):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;nt=mat.node_tree;b=nt.nodes['Principled BSDF']
 t=nt.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(Path(bc).resolve()),check_existing=True);nt.links.new(t.outputs['Color'],b.inputs['Base Color'])
 b.inputs['Roughness'].default_value=.80
 if orm:
  t=nt.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(Path(orm).resolve()),check_existing=True);t.image.colorspace_settings.name='Non-Color'
  sep=nt.nodes.new('ShaderNodeSeparateColor');nt.links.new(t.outputs['Color'],sep.inputs[0]);nt.links.new(sep.outputs[1],b.inputs['Roughness']);nt.links.new(sep.outputs[2],b.inputs['Metallic'])
 return mat

def finalize():
 assert len(PRINTS)<=64,len(PRINTS)
 canvas=Image.new('RGB',(1024,1024),(231,221,184));d=ImageDraw.Draw(canvas)
 for s,i in PRINTS.items():
  x,y=(i%4)*256,(i//4)*64
  font=ImageFont.truetype(FONT,37)
  while d.textbbox((0,0),s,font=font)[2]>242:font=ImageFont.truetype(FONT,font.size-1)
  d.rectangle((x,y,x+255,y+63),fill=(227,217,180));d.text((x+128,y+31),s,font=font,anchor='mm',fill=(23,51,43))
 path=Path('export/textures/T_Minigolf_Quick_Graphics.png');canvas.save(path)
 atlas=image_material('Minigolf_Quick','export/textures/T_Minigolf_Quick_BaseColor.png','export/textures/T_Minigolf_Quick_ORM.png')
 graphics=image_material('Minigolf_Graphics',path)
 water=M['water'];p=water.node_tree.nodes['Principled BSDF'];p.inputs['Roughness'].default_value=.12;p.inputs['Transmission Weight'].default_value=.42;p.inputs['IOR'].default_value=1.333
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.data=data;ob.modifiers.clear()
  bm=bmesh.new();bm.from_mesh(data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free()
  uv=data.uv_layers.get('UVMap') or data.uv_layers.new(name='UVMap')
  graphic=ob.get('graphic')
  if graphic:
   i=PRINTS[graphic];u=(i%4)*.25;v=1-(i//4+1)/16
   # Triangle vertices refer to authored plane coordinates.
   axis=2 if max(v.co.z for v in data.vertices)-min(v.co.z for v in data.vertices)>.001 else 1
   a=min(v.co.x for v in data.vertices);b=max(v.co.x for v in data.vertices);c=min(v.co[axis] for v in data.vertices);dd=max(v.co[axis] for v in data.vertices)
   for loop in data.loops:
    q=data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(u+.004+(q.x-a)/(b-a)*.242,v+.004+(q[axis]-c)/(dd-c)*(.0625-.008))
   data.materials.clear();data.materials.append(graphics)
  elif data.materials and data.materials[0]==water:pass
  else:
   for poly in data.polygons:
    key=data.materials[poly.material_index].name.removeprefix('Quick_');i=list(COLORS).index(key)
    for li in poly.loop_indices:uv.data[li].uv=((i%8+.5)/8,1-(i//8+.5)/8)
    poly.material_index=0
   data.materials.clear();data.materials.append(atlas)
 # Consolidate only static immediate children of module roots. Moving empties
 # are separate owners; contacts remain named in source-check report beforehand.
 bpy.context.view_layer.update()
 parents={o.parent for o in bpy.context.scene.objects if o.type=='MESH'}
 for parent in sorted(parents,key=lambda x:x.name if x else ''):
  obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==parent]
  if not obs:continue
  bpy.ops.object.select_all(action='DESELECT')
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0]
  if len(obs)>1:bpy.ops.object.join()
  ob=bpy.context.object;ob.name=(parent.name if parent else 'Course')+'__Mesh'
  xf=ob.matrix_basis.copy();ob.data.transform(xf);ob.matrix_basis=Matrix.Identity(4)
 return atlas,graphics
