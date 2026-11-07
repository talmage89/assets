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
 from kit.tiling import material
 for name in ('Asphalt','Concrete','Lawn'):
  folder=REPO/'ground/textures/ship'
  if (folder/f'T_{name}_BaseColor.png').exists():g.MATS[name]=material(name,folder)
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
 rt=F.root('Context terrain');F.box('Town grade',(0,-20,-.23),(10000,10000,.1),'grass',rt,0)
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
 # Actual library construction, built in minigolf/build/context. No copied
 # house-box substitutes and no changes to another family's deliveries.
 proof=[];base=REPO/'minigolf/build/context'
 proof.append(planted_asset(base/'strip/strip-201.glb','StripCenter_201',[((12,road_y-30,0),1,math.pi)]))
 proof.append(planted_asset(base/'station/station-101.glb','Station_101',[((-55,road_y-27,0),1,math.pi)]))
 proof.append(planted_asset(base/'house.glb','House',[((x,road_y-53,0),1,math.pi) for x in (-30,0,29,57)]))
 for name,positions in (('AlderC150',[(-11,road_y-2,0),(17,road_y+2,0),(-14,-p['lot'][1]/2+10,0)]),('AlderS240',[(42,road_y-2,0),(12,-p['lot'][1]/2+10,0)])):
  proof.append(planted_asset(REPO/'cars/export'/f'{name}.glb',name,[(q,1,math.pi/2) for q in positions]))
 proof.append(planted_asset(REPO/'street-light/export/StreetLight.glb','StreetLight',[((x,road_y-6.4,0),1,0) for x in (-72,-24,24,72)]))
 utility(p,road_y)
 return proof

def utility(p,road_y):
 # Use library pole/hardware constructors in an isolated import namespace;
 # source scalar finish is adequate at background distance. No family bake.
 saved=list(sys.path);folder=REPO/'utility/src';names={q.stem for q in folder.glob('*.py')};previous={key:sys.modules.pop(key,None) for key in names}
 try:
  sys.path.insert(0,str(folder));import construction,plan as utility_plan
  mapping=dict(Wood='wood',Endgrain='wood',Steel='metal',Porcelain='ivory',Polymer='navy',Paint='white',Cable='black',Aluminum='metal',Guard='yellow',Recess='black',Vine='grass')
  construction.M.update({k:F.M[v] for k,v in mapping.items()})
  construction.Assembly.finish=lambda self:self.root
  rt=F.root('Context library utility')
  for i,x in enumerate(range(-90,91,30)):
   spec=utility_plan.pole_spec(kind='transformer' if i==3 else 'tangent',seed=100+i);spec['light']=False
   part=construction.pole('Context library pole',spec);part.root.location=(x,road_y-8,0)
   if x<90:
    for yy in (-.85,0,.85):F.tube('Catenary roadside conductor',[(x+30*j/24,road_y-8+yy,10.4-1.15*math.sin(math.pi*j/24)) for j in range(25)],.009,'metal',rt,6)
 finally:
  sys.path[:]=saved
  for key in names:
   sys.modules.pop(key,None)
   if previous[key] is not None:sys.modules[key]=previous[key]

def make(p):
 palette();road_y=native_ground(p);town_proof=town(p,road_y);W,D=p['lot'];rng=random.Random(981+p['seed'])
 trees=[]
 for i in range(22):
  x=-100+i*9.5;y=road_y-32-rng.random()*15;trees.append(((x,y,0),rng.uniform(.70,1.2),rng.random()*math.tau))
 for s in (-1,1):
  for y in (-9,6,23):trees.append(((s*(W/2+3),y,0),rng.uniform(.68,.9),rng.random()*math.tau))
 for i in range(11):trees.append(((-W/2-9+i*(W+18)/10,D/2+9+rng.uniform(-2,3),0),rng.uniform(.72,1.0),rng.random()*math.tau))
 tree_proof=planted_asset(REPO/'trees/export/RedMaple.glb','RedMaple',trees[::2])
 oak_proof=planted_asset(REPO/'trees/export/PinOak.glb','PinOak',trees[1::2])
 shrubs=[]
 for s in (-1,1):
  for i,y in enumerate((-9,-1,7,16,22)):
   x=s*(5.1 if p['water'] else 1.0)+rng.uniform(-.4,.4);shrubs.append(((x,y,.065*max(0,y+7) if p['water'] else 0),rng.uniform(.65,1.15),rng.random()*math.tau))
  for y in (-7,4,15):shrubs.append(((s*(W/2-3),y,.065*max(0,y+7) if p['water'] else 0),rng.uniform(.80,1.25),rng.random()*math.tau))
 for x in range(-16,17,4):shrubs.append(((x,-15.5,0),.8,rng.random()*math.tau))
 if p['water']:
  from plan_check import envelope
  envelopes=[envelope(h) for h in p['holes']]
  def inside(poly,q):
   return all((b[0]-a[0])*(q[1]-a[1])-(b[1]-a[1])*(q[0]-a[0])>=0 for a,b in zip(poly,poly[1:]+poly[:1]))
  # Irregular planted masses fill the common beds. Keep foliage footprints
  # out of playing lanes, the water corridor and the circuit's walking band.
  for j in range(500):
   if len(shrubs)>=68:break
   x=rng.uniform(-21,21);y=rng.uniform(-10,25)
   if (x/21)**2+((y-7)/19)**2>1 or (abs(x)<5 and -8<y<16):continue
   radial=math.sqrt((x/17.25)**2+((y-7)/14.85)**2)
   if abs(radial-1)<.085:continue
   if any(any(inside(poly,(x+dx,y+dy)) for dx,dy in ((0,0),(.75,0),(-.75,0),(0,.75),(0,-.75))) for poly in envelopes):continue
   if any(math.dist((x,y),q[0][:2])<1.0 for q in shrubs):continue
   shrubs.append(((x,y,.015+.065*max(0,y+7)),rng.uniform(.68,1.2),rng.random()*math.tau))

 hydrangeas=[((q[0][0]+1.1,q[0][1]+.5,q[0][2]),q[1]*.7,q[2]) for q in shrubs[::3]]
 hydrangea_proof=planted_asset(REPO/'shrubs/export/Shrubs.glb','Hydrangea',hydrangeas)
 shrub_proof=planted_asset(REPO/'shrubs/export/Shrubs.glb','Boxwood',shrubs)
 return dict(road='ground/src/build.py: native road/curb/walk constructors, quick palette',town=town_proof,hydrangea_geometry=hydrangea_proof,maple_instances=len(trees),boxwood_instances=len(shrubs),tree_geometry=tree_proof,oak_geometry=oak_proof,shrub_geometry=shrub_proof,included_in_course_gltf=False)
