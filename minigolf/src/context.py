"""Presentation-only native road construction, original town massing and foliage.

No existing asset is modified or exported. Course landscape placements are
listed separately from the glTF checkpoint's own construction budget.
"""
import importlib.util,math,sys,random
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
import geometry as F
from fixtures import roof
REPO=Path(__file__).resolve().parents[2]

def palette():
 for key,c in F.COLORS.items():
  m=bpy.data.materials.new('Context_'+key);m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=.85;F.M[key]=m

def native_ground(p):
 saved=list(sys.path);mods={k:sys.modules.pop(k,None) for k in ('dimensions','textures')}
 try:
  sys.path.insert(0,str(REPO/'ground/src'));spec=importlib.util.spec_from_file_location('_minigolf_ground',REPO/'ground/src/build.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 finally:
  sys.path[:]=saved
  for k,v in mods.items():
   sys.modules.pop(k,None)
   if v is not None:sys.modules[k]=v
 for a,b in (('Asphalt','asphalt'),('Concrete','concrete'),('Lawn','grass'),('GroundTrim','black')):g.MATS[a]=F.M[b]
 y=-p['lot'][1]/2-7.62
 for i in range(-18,19):
  rt=g.road('Context road',0);rt.location=(i*6.096,y,-.17);rt.rotation_euler.z=math.pi/2
 # Back side is an uninterrupted native street. The course side uses exact
 # interval cuts, so its driveway modules and walk openings have no gaps.
 for i in range(-36,37):
  x=i*3.048;rt=g.curb('Context native curb');rt.location=(x,y-4.1148,-.17);rt.rotation_euler.z=math.pi/2
  for dx in (-.762,.762):
   rt=g.sidewalk('Context native sidewalk');rt.location=(x+dx,y-6.096,-.17);rt.rotation_euler.z=math.pi/2
 intervals=[];cursor=-112
 for x in sorted(p['driveways']):intervals.append((cursor,x-3.048));cursor=x+3.048
 intervals.append((cursor,112))
 for start,end in intervals:
  a=start
  while a<end-1e-6:
   length=min(3.048,end-a);rt=g.curb('Context continuous native curb');rt.location=(a+length/2,y+4.1148,-.17);rt.rotation_euler.z=-math.pi/2;rt.scale.y=length/3.048;a+=length
  a=start
  while a<end-1e-6:
   length=min(1.524,end-a);rt=g.sidewalk('Context native front sidewalk');rt.location=(a+length/2,y+6.096,-.17);rt.rotation_euler.z=-math.pi/2;rt.scale.y=length/1.524;a+=length
 for x in p['driveways']:
  rt=g.curb('Context native driveway curb',cut=True);rt.location=(x,y+4.1148,-.17);rt.rotation_euler.z=-math.pi/2
  apron=F.root('Context driveway apron',(x,y,0))
  F.mesh('Driveway approach',[(-3.048,4.1148,-.1441),(3.048,4.1148,-.1441),(3.048,7.62,.015),(-3.048,7.62,.015)],[(0,1,2,3)],'concrete',apron,False)
 rt=F.root('Context terrain');F.box('Town grade',(0,-20,-.23),(500,400,.1),'grass',rt,0)
 return y

def planted_asset(path,rootname,placements):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));added=set(bpy.data.objects)-before
 root=next(o for o in added if o.name==rootname or o.name.startswith(rootname+'.'))
 keep={root,*root.children_recursive}
 for ob in added-keep:bpy.data.objects.remove(ob,do_unlink=True)
 # Use one linked mesh population, preserving own library material maps.
 meshes=[o for o in keep if o.type=='MESH'];triangles=0
 for o in meshes:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
 xf={o:root.matrix_world.inverted()@o.matrix_world for o in meshes}
 for index,(p,scale,yaw) in enumerate(placements):
  frame=Matrix.Translation(Vector(p))@Matrix.Rotation(yaw,4,'Z')@Matrix.Scale(scale,4)
  for old in meshes:
   ob=old.copy();ob.data=old.data;bpy.context.collection.objects.link(ob);ob.parent=None;ob.matrix_world=frame@xf[old];ob.name='Context '+rootname
 for ob in keep:bpy.data.objects.remove(ob,do_unlink=True)
 return dict(instances=len(placements),unique_triangles=triangles,placed_triangles=len(placements)*triangles,source=str(path.relative_to(REPO)))

def town(p,road_y):
 rng=random.Random(442);rt=F.root('Context original town')
 # Complete facades and roof depth keep the street from becoming a flat horizon.
 for i,x in enumerate(range(-84,85,14)):
  sub=F.root('Context house',(x,road_y-24,0),parent=rt);w=9.0+(i%3)*.5;d=8.2
  F.box('House volume',(0,0,1.5),(w,d,3.0),'ivory' if i%2 else 'rocklight',sub)
  roof(sub,'House roof',w+.5,d+.5,3.0,2.1,'navy' if i%2 else 'red')
  for xx in (-w*.33,w*.33):
   F.box('Window reveal',(xx,d/2+.02,1.65),(1.40,.1,1.35),'navy',sub)
   for ss in (-1,1):F.box('Window casing',(xx+ss*.76,d/2+.04,1.65),(.09,.10,1.55),'white',sub)
   F.box('Window mullion',(xx,d/2+.08,1.65),(.045,.08,1.35),'white',sub)
  F.box('House door',(0,d/2+.03,1.0),(.90,.1,2),'red',sub)
  for xx in (-.75,.75):F.box('Porch column',(xx,d/2+1,1.2),(.12,.12,2.4),'ivory',sub)
  F.box('Porch roof',(0,d/2+.6,2.5),(2.3,1.8,.14),'navy',sub)
  F.box('House path',(0,d/2+4,.01),(1.35,6,.045),'concrete',sub,0)
 # Low roadside shops and a garage at either end anchor a mixed suburban strip.
 for x in (-58,56):
  sub=F.root('Context small shops',(x,road_y-13,0),parent=rt)
  F.box('Shop shell',(0,0,2.0),(12,7,4),'brick',sub)
  F.box('Shop coping',(0,0,4.02),(12.2,7.2,.15),'concrete',sub)
  F.box('Shop glazing',(0,3.56,1.65),(9,.06,2.3),'glass',sub)
  for xx in range(-5,6,2):F.box('Shop pier',(xx,3.65,1.5),(.16,.25,3.0),'ivory',sub)
  F.box('Shop sign fascia',(0,3.7,3.2),(10,.3,.65),'navy',sub)
 # Wooden poles and slack spans complete the road horizon.
 for x in range(-90,91,24):
  F.cyl('Context utility pole',(x,road_y-8,0),(x,road_y-8,9.5),.12,'wood',rt,10)
  F.box('Context utility crossarm',(x,road_y-8,8.8),(2.2,.14,.18),'wood',rt)
  if x<78:
   for sy in (-.65,.65):F.tube('Context slack wire',[(x+24*j/16,road_y-8+sy,8.85-.7*math.sin(math.pi*j/16)) for j in range(17)],.012,'navy',rt,6)

def make(p):
 palette();road_y=native_ground(p);town(p,road_y);W,D=p['lot'];rng=random.Random(981)
 trees=[]
 for i in range(22):
  x=-100+i*9.5;y=road_y-32-rng.random()*15;trees.append(((x,y,0),rng.uniform(.70,1.2),rng.random()*math.tau))
 for s in (-1,1):
  for y in (-9,6,23):trees.append(((s*(W/2+3),y,0),rng.uniform(.68,.9),rng.random()*math.tau))
 for i in range(11):trees.append(((-W/2-9+i*(W+18)/10,D/2+9+rng.uniform(-2,3),0),rng.uniform(.72,1.0),rng.random()*math.tau))
 tree_proof=planted_asset(REPO/'trees/export/RedMaple.glb','RedMaple',trees)
 shrubs=[]
 for s in (-1,1):
  for y in (-12,-1,10,22):shrubs.append(((s*5.7,y,.025*max(0,y+9) if p['water'] else 0),.72,rng.random()*math.tau))
 for x in range(-16,17,4):shrubs.append(((x,-15.5,0),.8,rng.random()*math.tau))
 shrub_proof=planted_asset(REPO/'shrubs/export/Shrubs.glb','Boxwood',shrubs)
 return dict(road='ground/src/build.py: native road/curb/walk constructors, quick palette',town='original presentation-only house/shop massing',maple_instances=len(trees),boxwood_instances=len(shrubs),tree_geometry=tree_proof,shrub_geometry=shrub_proof,included_in_course_gltf=False)
