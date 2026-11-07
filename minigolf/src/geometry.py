"""Construction helpers using the kit's mesh vocabulary.

Source roles carry original UV/baked look development during finalize().
The initial role colors also support fast source-form inspection.
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
 'water':(.94,.98,.99),'glass':(.08,.12,.13),'foam':(.65,.69,.61),'stonepaint':(.40,.41,.36),'fallwater':(.24,.32,.28),'clothred':(.32,.024,.016),'clothivory':(.58,.55,.43)}
M={};PRINTS={};PRINT_LAYOUTS={};PRINT_OBJECTS=[];FONT=None

def setup():
 global FONT
 FONT=find_font('DejaVu Sans','Bold')
 out=Path('export/textures');out.mkdir(parents=True,exist_ok=True)
 for name,c in COLORS.items():
  mat=bpy.data.materials.new('Quick_'+name);mat.use_nodes=True
  b=mat.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=.85
  if name=='metal':b.inputs['Metallic'].default_value=.9;b.inputs['Roughness'].default_value=.30
  M[name]=mat
 for name in ('T_Minigolf_Quick_BaseColor.png','T_Minigolf_Quick_ORM.png','T_Minigolf_Quick_Graphics.png'):
  (out/name).unlink(missing_ok=True)

def root(name,loc=(0,0,0),yaw=0,parent=None,kind=None):
 ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.parent=parent
 ob.location=loc;ob.rotation_euler.z=math.radians(yaw);ob['module_kind']=kind or name;ob['module']=True
 return ob

def own(ob,parent,solid=True):
 ob.parent=parent;ob['solid']=solid;return ob

def atlas_repeat_cells(data,tile,axes):
 """Split course-atlas skins at their physical repeat, retaining silhouette."""
 bm=bmesh.new();bm.from_mesh(data)
 for axis in axes:
  lo=min(v.co[axis] for v in bm.verts);hi=max(v.co[axis] for v in bm.verts)
  for j in range(math.floor(lo/tile)+1,math.ceil(hi/tile)):
   point=[0.,0.,0.];normal=[0.,0.,0.];point[axis]=j*tile;normal[axis]=1
   bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=point,plane_no=normal)
 # Float32 plane intersections can leave sub-micrometre corner slivers at
 # metre-scale coordinates. Merge below 0.01 mm before export, not in checks.
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-5)
 bm.to_mesh(data);bm.free();data.update()

def box(name,p,size,mat,parent,r=.002,seg=1):
 ob=G.box(name,p,size,M[mat],r,seg)
 # Per-face projection uses geometric bevel normals. Acute-corner tangent
 # precision is independently checked and repaired at export.
 for mod in ob.modifiers:
  if mod.type=='BEVEL':mod.harden_normals=False
 return own(ob,parent)
def mesh(name,vs,fs,mat,parent,solid=True):return own(G.mesh(name,vs,fs,M[mat]),parent,solid)
def cyl(name,a,b,r,mat,parent,n=12):return own(G.smooth(G.cylinder(name,a,b,r,M[mat],n)),parent)
def tube(name,pts,r,mat,parent,sides=8):return own(G.smooth(G.tube(name,pts,r,M[mat],sides=sides)),parent)
def beam(name,a,b,w,d,mat,parent,edge_radius=.002):
 a,b=Vector(a),Vector(b);ob=box(name,(a+b)/2,(w,d,(b-a).length),mat,parent,edge_radius)
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
 rng=random.Random(seed);x,y,z=p;w,d,h=size;detailed=max(size)>1.3;n=24 if detailed else (10 if h>.12 else 6)
 loops=[]
 fracture=[1+.08*math.sin(i*math.tau/n*3+seed)+.045*math.sin(i*math.tau/n*7+seed*.7)+rng.uniform(-.024,.024) for i in range(n)]
 profile=((0,.85),(.12,.94),(.22,1),(.32,.93),(.38,.95),(.43,.80),(.56,.86),(.62,.76),(.73,.82),(.80,.65),(.90,.70),(.96,.60),(1,.62)) if detailed else ((0,.88),(.22,1),(.62,.82),(1,.15))
 for k,(height,fac) in enumerate(profile):
  ring=[]
  for i in range(n):
   a=i*math.tau/n;ca,sa=math.cos(a),math.sin(a)
   xx=math.copysign(abs(ca)**.45,ca) if detailed else ca;yy=math.copysign(abs(sa)**.45,sa) if detailed else sa
   radius=fac*fracture[i]*(1+(.07*math.sin(a*3+height*6+seed) if detailed else 0))
   zz=height+(.026*math.sin(a*3+seed)+.017*math.sin(a*7+height*9+seed) if k else 0)
   ring.append((x+w*.5*(radius*xx+.065*math.sin(height*8+seed)*height),y+d*.5*(radius*yy+.045*math.cos(height*9+seed)*height),z+h*zz))
  loops.append(ring)
 ob=own(G.smooth(G.loft(name,loops,M[mat]),32),parent)
 ob['rock_seed']=seed
 if detailed:
  mod=ob.modifiers.new('Soft carved shotcrete transitions','SUBSURF');mod.levels=1;mod.render_levels=1
  dec=ob.modifiers.new('Retain outcrop silhouette budget','DECIMATE');dec.ratio=.67
 return ob

def rockwall(name,points,width,height,parent,seed=0,mat='rocklight',closed=False):
 """Continuous carved shell with recessed beds and irregular broken cap."""
 import random
 rng=random.Random(seed);n=len(points);vs=[]
 jitter=[rng.uniform(-.035,.035) for _ in points]
 for i,p in enumerate(points):
  a=Vector(points[(i-1)%n] if closed or i else points[0]);b=Vector(points[(i+1)%n] if closed or i<n-1 else points[-1]);d=(b-a).normalized();normal=Vector((-d.y,d.x,0))
  for side in (-1,1):
   for j,(f,spread) in enumerate(((0,.88),(.38,1),(.44,.80),(.75,.85),(1,.58))):
    off=width*.5*spread+jitter[i]+.018*math.sin(i*2.7+j)
    q=Vector(p)+normal*side*off;vs.append((q.x,q.y,p[2]+height*f+(jitter[i] if j else 0)))
 fs=[]
 for i in range(n if closed else n-1):
  a=i*10;b=((i+1)%n)*10
  for side in (0,5):
   for j in range(4):fs.append((a+side+j,b+side+j,b+side+j+1,a+side+j+1))
  fs.append((a+4,b+4,b+9,a+9))
 if not closed:fs.extend(((0,1,2,3,4,9,8,7,6,5),tuple((n-1)*10+j for j in (5,6,7,8,9,4,3,2,1,0))))
 ob=G.smooth(mesh(name,vs,fs,mat,parent),34)
 if name=='Continuous mortared pond coping':ob['rock_seed']=seed
 return ob

def ball(name,p,r,mat,parent,sides=12,rings=6):
 profile=[(-r,0)]+[(r*math.sin(-math.pi/2+i*math.pi/rings),r*math.cos(-math.pi/2+i*math.pi/rings)) for i in range(1,rings)]+[(r,0)]
 ob=own(G.smooth(G.lathe(name,profile,M[mat],sides),60),parent);ob.location=p;return ob

def text(parent,string,p,w,h,vertical=True):
 # Shared original graphics; geometry is a single correctly faced quad.
 key=string if string.startswith('@pylon:') else string+'|'+format(w/h,'.5f')
 if key not in PRINTS:PRINTS[key]=len(PRINTS);PRINT_LAYOUTS[key]=(string,w/h)
 x,y,z=p
 vs=[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)] if vertical else [(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)]
 ob=mesh('Graphic '+string,vs,[(0,1,2,3)],'ivory',parent,False);ob['graphic']=key
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
 regular=[key for key in PRINTS if not key.startswith('@pylon:')];pylons=[key for key in PRINTS if key.startswith('@pylon:')]
 assert len(regular)<=52 and len(pylons)<=2,(len(regular),len(pylons))
 canvas=Image.new('RGB',(1024,1024),(227,217,180));d=ImageDraw.Draw(canvas);charts={};ink=(23,51,43)
 for i,key in enumerate(regular):
  label,aspect=PRINT_LAYOUTS[key];x,y=(i%4)*256,(i//4)*64;charts[key]=(x,y,256,64)
  if label=='SCORE':
   d.text((x+7,y+4),'BRAMBLE / CAIRN',font=ImageFont.truetype(FONT,10),fill=ink)
   for j in range(19):d.line((x+5+j*13,y+23,x+5+j*13,y+58),fill=ink,width=1)
   for yy in (23,38,58):d.line((x+5,y+yy,x+239,y+yy),fill=ink,width=1)
   for j in range(18):d.text((x+7+j*13,y+25),str(j+1),font=ImageFont.truetype(FONT,8),fill=ink)
  else:
   # Precompensate the chart for its physical panel aspect; do not stretch
   # normal lettering into extremely wide, flattened pylon type.
   font=ImageFont.truetype(FONT,64);box=font.getbbox(label);gw,gh=box[2]-box[0],box[3]-box[1]
   mask=Image.new('L',(gw,gh));ImageDraw.Draw(mask).text((-box[0],-box[1]),label,font=font,fill=255)
   ratio=(gw/gh)*((256-8.192)/(64-8.192))/aspect;tw=min(238,round(48*ratio));th=min(48,round(tw/ratio));mask=mask.resize((tw,th),Image.Resampling.LANCZOS)
   canvas.paste(ink,(x+(256-tw)//2,y+(64-th)//2),mask)
 for i,key in enumerate(pylons):
  x,y=i*512,832;charts[key]=(x,y,512,192);name=PRINT_LAYOUTS[key][0].split(':',1)[1].upper()
  d.rectangle((x+7,y+7,x+505,y+185),outline=ink,width=2)
  d.ellipse((x+24,y+25,x+70,y+77),fill=ink);d.arc((x+16,y+72,x+79,y+96),0,180,fill=ink,width=3)
  font=ImageFont.truetype(FONT,36)
  while font.getlength(name)>406:font=ImageFont.truetype(FONT,font.size-1)
  d.text((x+89,y+50),name,font=font,anchor='lm',fill=ink)
  d.line((x+24,y+102,x+488,y+102),fill=ink,width=2)
  d.text((x+256,y+128),'MINIATURE GOLF',font=ImageFont.truetype(FONT,35),anchor='mm',fill=ink)
  d.text((x+256,y+165),'18 HOLES  •  OPEN LATE',font=ImageFont.truetype(FONT,23),anchor='mm',fill=ink)
 path=Path('textures/ship/T_Minigolf_Graphics_BaseColor.png');canvas.save(path)
 from look import materials
 atlas,states=materials()
 graphics=image_material('Minigolf_Graphics',path)
 lit_graphics=graphics.copy();lit_graphics.name='Minigolf_LitGraphics';bsdf=lit_graphics.node_tree.nodes.get('Principled BSDF');tex=next(n for n in lit_graphics.node_tree.nodes if n.type=='TEX_IMAGE');lit_graphics.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Emission Color']);bsdf.inputs['Emission Strength'].default_value=2

 water=M['water'];p=water.node_tree.nodes['Principled BSDF'];p.inputs['Roughness'].default_value=.12;p.inputs['Transmission Weight'].default_value=.42;p.inputs['IOR'].default_value=1.333
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  if not ob.data.vertices:
   bpy.data.objects.remove(ob,do_unlink=True);continue
  data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.data=data;ob.modifiers.clear()
  if ob.get('water_skin'):
   atlas_repeat_cells(data,2.,(0,1))
  if ob.get('flow_sheet'):
   data.shade_smooth();data.set_sharp_from_angle(angle=math.radians(65))
  if 'rock_seed' in ob:
   atlas_repeat_cells(data,2.,(0,1,2));ob['stone_uv_m']=2.
   data.shade_smooth();data.set_sharp_from_angle(angle=math.radians(65))
  bm=bmesh.new();bm.from_mesh(data)
  if ob.get('buried_walk_bottom'):
   bm.normal_update();bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z<-.2],context='FACES')
  bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free()
  uv=data.uv_layers.get('UVMap') or data.uv_layers.new(name='UVMap')
  graphic=ob.get('graphic')
  if graphic:
   gx,gy,gw,gh=charts[graphic];u=gx/1024;v=1-(gy+gh)/1024
   # Triangle vertices refer to authored plane coordinates.
   axis=2 if max(v.co.z for v in data.vertices)-min(v.co.z for v in data.vertices)>.001 else 1
   a=min(v.co.x for v in data.vertices);b=max(v.co.x for v in data.vertices);c=min(v.co[axis] for v in data.vertices);dd=max(v.co[axis] for v in data.vertices)
   for loop in data.loops:
    q=data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(u+.004+(q.x-a)/(b-a)*(gw/1024-.008),v+.004+(q[axis]-c)/(dd-c)*(gh/1024-.008))
   owner=ob.parent
   while owner and not owner.name.startswith('RoadSign'):owner=owner.parent
   data.materials.clear();data.materials.append(lit_graphics if owner else graphics)
  else:
   from look import assign
   assign(ob,atlas,states)
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
