"""Presentation-only native road construction, original town massing and foliage.

No existing asset is modified or exported. Course landscape placements are
listed separately from the glTF checkpoint's own construction budget.
"""
import importlib.util,json,math,sys,random
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
import geometry as F
import landscape
import paths
from fixtures import roof
REPO=Path(__file__).resolve().parents[2]

def texture_cost():
 """Count unique decoded maps in the assembled review scene, including core."""
 import hashlib,io
 from PIL import Image
 materials={m for ob in bpy.context.scene.objects if ob.type=='MESH' for m in ob.data.materials if m and m.use_nodes}
 images={n.image for m in materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image};unique={}
 for image in images:
  raw=bytes(image.packed_file.data) if image.packed_file else Path(bpy.path.abspath(image.filepath)).read_bytes()
  with Image.open(io.BytesIO(raw)) as decoded:
   rgba=decoded.convert('RGBA');digest=hashlib.sha256(rgba.tobytes()).hexdigest();size=list(rgba.size)
  if digest in unique:
   unique[digest]['name']=min(unique[digest]['name'],image.name);continue
  unique[digest]=dict(name=image.name,size=size,pixel_sha256=digest,compressed_mip_mib=math.prod(size)*4/3/1024**2)
 rows=sorted(unique.values(),key=lambda q:(q['name'],q['pixel_sha256']))
 return dict(unique_images=len(rows),compressed_mip_mib=sum(r['compressed_mip_mib'] for r in rows),basis='8 bpp block compression and full mip chains, decoded-pixel deduplication; includes core course and all native context, assumes engine image sharing',images=rows)

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
 for name in ('Asphalt','Concrete','Lawn','GroundTrim'):
  folder=REPO/'ground/textures/ship'
  if (folder/f'T_{name}_BaseColor.png').exists():g.MATS[name]=material(name,folder,alpha=(name=='GroundTrim'))
 y=-p['lot'][1]/2-7.62
 for i in range(-18,19):
  rt=g.road('Context road',0);rt.location=(i*6.096,y,-.17);rt.rotation_euler.z=math.pi/2
 # Back side is an uninterrupted native street. The course side uses exact
 # interval cuts, so its driveway modules and walk openings have no gaps.
 for i in range(-36,37):
  x=i*3.048;rt=g.curb('Context native curb');rt.location=(x,y-4.1148,-.17);rt.rotation_euler.z=-math.pi/2
  for dx in (-.762,.762):
   rt=g.sidewalk('Context native sidewalk');rt.location=(x+dx,y-6.096,-.17);rt.rotation_euler.z=-math.pi/2
 intervals=[];cursor=-112
 for x in sorted(p['driveways']):intervals.append((cursor,x-3.048));cursor=x+3.048
 intervals.append((cursor,112))
 for start,end in intervals:
  a=start
  while a<end-1e-6:
   length=min(3.048,end-a);rt=g.curb('Context continuous native curb');rt.location=(a+length/2,y+4.1148,-.17);rt.rotation_euler.z=math.pi/2;rt.scale.y=length/3.048;a+=length
  a=start
  while a<end-1e-6:
   length=min(1.524,end-a);rt=g.sidewalk('Context native front sidewalk');rt.location=(a+length/2,y+6.096,-.17);rt.rotation_euler.z=math.pi/2;rt.scale.y=length/1.524;a+=length
 for x in p['driveways']:
  rt=g.curb('Context native driveway curb',cut=True);rt.location=(x,y+4.1148,-.17);rt.rotation_euler.z=math.pi/2
  apron=F.root('Context driveway apron',(x,y,0))
  F.mesh('Driveway approach',[(-3.048,4.1148,-.1441),(3.048,4.1148,-.1441),(3.048,7.62,.015),(-3.048,7.62,.015)],[(0,1,2,3)],'concrete',apron,False)
 rt=F.root('Context terrain')
 from kit.tiling import world_uv
 def lawn(name,points):
  winding=(points[1][0]-points[0][0])*(points[2][1]-points[0][1])-(points[1][1]-points[0][1])*(points[2][0]-points[0][0]);face=(0,1,2,3) if winding>0 else (3,2,1,0)
  ob=F.mesh(name,points,[face],'grass',rt,False);ob.data.materials.clear();ob.data.materials.append(g.MATS['Lawn']);world_uv(ob,3.048)
 W,D=p['lot']
 regions=[(-5000,5000,-5000,y-7.62),(-5000,-W/2,y+7.62,5000),(W/2,5000,y+7.62,5000),(-W/2,W/2,D/2,5000)]
 for x0,x1,lo,hi in regions:lawn('Town yard support',[(x0,lo,-.005),(x1,lo,-.005),(x1,hi,-.005),(x0,hi,-.005)])
 for side in (-1,1):
  for start,end in (intervals if side==1 else [(-112,112)]):lawn('Native curb-to-walk grass verge',[(start,y+side*4.2672,-.0176),(end,y+side*4.2672,-.0176),(end,y+side*6.096,0),(start,y+side*6.096,0)])
 return y

def planted_asset(path,rootname,placements):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));added=set(bpy.data.objects)-before
 # All native shrub growth seeds bind the same delivered three-map set.
 for material in {m for o in added if o.type=='MESH' for m in o.data.materials if m}:
  if not material.use_nodes:continue
  for node in material.node_tree.nodes:
   if node.type=='TEX_IMAGE' and node.image:
    for channel in ('BaseColor','Normal','ORM'):
     name='T_Shrubs_'+channel
     if node.image.name.startswith(name):
      shared=next((im for im in bpy.data.images if im.name==name or im.name==name+'.png'),None)
      if shared is not None:node.image=shared
 root=next(o for o in added if o.name==rootname or o.name.startswith(rootname+'.'))
 geometry_seed=root.get('geometry_seed','canonical family seed')
 keep={root,*root.children_recursive}
 for ob in added-keep:bpy.data.objects.remove(ob,do_unlink=True)
 # Use one linked mesh population, preserving own library material maps.
 meshes=[o for o in keep if o.type=='MESH'];triangles=0
 for o in meshes:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
 xf={o:root.matrix_world.inverted()@o.matrix_world for o in meshes}
 for index,placement in enumerate(placements):
  p,scale,yaw=placement[:3];roll=placement[3] if len(placement)>3 else 0
  frame=Matrix.Translation(Vector(p))@Matrix.Rotation(yaw,4,'Z')@Matrix.Rotation(roll,4,'Y')@Matrix.Scale(scale,4)
  for old in meshes:
   ob=old.copy();ob.data=old.data;bpy.context.collection.objects.link(ob);ob.parent=None;ob.matrix_world=frame@xf[old];ob.name='Context '+rootname
 for ob in keep:bpy.data.objects.remove(ob,do_unlink=True)
 return dict(instances=len(placements),unique_triangles=triangles,placed_triangles=len(placements)*triangles,source=str(path.relative_to(REPO)),source_root=rootname,geometry_seed=geometry_seed,placements=[dict(position_blender_m=list(q[0]),uniform_scale=q[1],yaw_blender_z_radians=q[2],roll_blender_y_radians=q[3] if len(q)>3 else 0) for q in placements])

def town(p,road_y):
 # Actual library construction, built in minigolf/build/context. No copied
 # house-box substitutes and no changes to another family's deliveries.
 proof=[];base=REPO/'minigolf/build/context'
 proof.append(planted_asset(base/'strip/strip-201.glb','StripCenter_201',[((12,road_y-30,0),1,math.pi)]))
 proof.append(planted_asset(base/'station/station-101.glb','Station_101',[((-55,road_y-27,0),1,math.pi)]))
 proof.append(planted_asset(base/'house.glb','House',[((x,road_y-53,0),1,math.pi) for x in (-30,57)]+[((x,p['lot'][1]/2+27,0),1,math.pi) for x in (18,-76)]))
 proof.append(planted_asset(base/'house-ranch.glb','House',[((0,road_y-53,0),1,math.pi),((-18,p['lot'][1]/2+24,0),1,math.pi)]))
 proof.append(planted_asset(base/'house-cape.glb','House',[((29,road_y-53,0),1,math.pi),((-46,p['lot'][1]/2+26,0),1,math.pi)]))
 road_z=.00635+(3.6576-2)/48-.17
 for name,positions in (('AlderC150',[(-11,road_y-2,road_z),(17,road_y+2,road_z),(-14,-p['lot'][1]/2+10,.0355)]),('AlderS240',[(42,road_y-2,road_z),(12,-p['lot'][1]/2+10,.0355)])):
  proof.append(planted_asset(REPO/'cars/export'/f'{name}.glb',name,[(q,1,-math.copysign(math.pi/2,q[1]-road_y) if q[2]<0 else math.pi,-math.atan(1/48) if q[2]<0 else 0) for q in positions]))
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
 for i in range(23):trees.append(((-110+i*10,D/2+7+rng.uniform(-1,2),0),rng.uniform(.65,1.05),rng.random()*math.tau))
 # Younger native understory breaks the distant horizon beneath mature crowns.
 for i in range(29):trees.append(((-105+i*7.5,D/2+2+rng.uniform(0,3),0),rng.uniform(.32,.48),rng.random()*math.tau))
 tree_proof=planted_asset(REPO/'trees/export/RedMaple.glb','RedMaple',trees[::2])
 oak_proof=planted_asset(REPO/'trees/export/PinOak.glb','PinOak',trees[1::2])
 from plan import center,halfwidth,local
 from plan_check import envelope
 envelopes=[envelope(h) for h in p['holes']];walks=[];fixture_centers=[]
 for h in p['holes']:
  walks.append(paths.lane(h))
  if h['fixture']:
   cx,cy=center(h,.49);fixture_centers.append((local(h,cx,cy)[:2],2.4 if h['fixture']=='castle' else 1.5))
 if not p['water']:walks.extend(paths.links(p))
 else:walks.extend(q[1] for q in paths.adventure_links(p))
 def inside(poly,q):return all((b[0]-a[0])*(q[1]-a[1])-(b[1]-a[1])*(q[0]-a[0])>=0 for a,b in zip(poly,poly[1:]+poly[:1]))
 def segment(q,a,b):
  dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/max(1e-9,dx*dx+dy*dy)));return math.dist(q,(a[0]+t*dx,a[1]+t*dy))
 def safe(x,y,radius=.60):
  if p['water'] and abs(x)<5 and -8<y<16:return False
  if any(any(inside(poly,(x+radius*math.cos(a),y+radius*math.sin(a))) for a in (j*math.tau/8 for j in range(8))) for poly in envelopes):return False
  if any(segment((x,y),a,b)<.762+radius for line in walks for a,b in zip(line,line[1:])):return False
  if any(math.dist((x,y),q)<r+radius for q,r in fixture_centers):return False
  if p['water'] and abs(math.sqrt((x/17.25)**2+((y-7)/14.85)**2)-1)<.10:return False
  return True
 shrubs=[]
 def add(x,y,scale=None,radius=.60):
  if safe(x,y,radius):shrubs.append(((x,y,.024+(.065*max(0,y+7) if p['water'] else 0)),scale or rng.uniform(.68,1.15),rng.random()*math.tau))
 for spec in landscape.beds(p):
  x,y=spec['center'];rx,ry=spec['radii']
  if spec['name'].startswith('Perimeter'):
   for yy in (-7,4,15):add(x,yy)
  elif spec['name'].startswith('Entry'):
   for j in range(5):add(x+rx*(j/4*1.5-.75),y+rng.uniform(-.1,.1),.8 if p['water'] else .4,.60 if p['water'] else .30)
  else:
   for j in range(6):add(x+rng.uniform(-.3,.3),y+ry*(j/5*1.6-.8),rng.uniform(.65,.9))
 if p['water']:
  for side in (-1,1):
   for yy in (-9,-1,7,16,22):add(side*5.1+rng.uniform(-.4,.4),yy)
 if p['water']:
  # Irregular planted masses fill the common beds. Keep foliage footprints
  # out of playing lanes, the water corridor and the circuit's walking band.
  for j in range(500):
   if len(shrubs)>=68:break
   x=rng.uniform(-21,21);y=rng.uniform(-10,25)
   if (x/21)**2+((y-7)/19)**2>1 or (abs(x)<5 and -8<y<16):continue
   if any(math.dist((x,y),q[0][:2])<1.0 for q in shrubs):continue
   add(x,y)
 else:
  boundary=paths.court(p)
  for j in range(600):
   if len(shrubs)>=44:break
   x=rng.uniform(-21,17);y=rng.uniform(-12,21)
   if not inside(boundary,(x,y)):continue
   if any(math.dist((x,y),q[0][:2])<1.35 for q in shrubs):continue
   add(x,y)

 dx,dy=(.45,.35) if p['water'] else (.3,.15)
 hydrangeas=[((q[0][0]+dx,q[0][1]+dy,q[0][2]),q[1]*.7,q[2]) for q in shrubs[::3] if safe(q[0][0]+dx,q[0][1]+dy,.45)]
 hydrangea_proof=planted_asset(REPO/'shrubs/export/Shrubs.glb','Hydrangea',hydrangeas)
 shrub_proof=[]
 for index,seed in enumerate((None,811,829)):
  path=REPO/'shrubs/export/Shrubs.glb' if seed is None else REPO/f'minigolf/build/context/boxwood-{seed}/variant.glb'
  shrub_proof.append(planted_asset(path,'Boxwood',shrubs[index::3]))
 proof=dict(road='ground/src/build.py: native road/curb/walk constructors and canonical PBR maps',town=town_proof,hydrangea_geometry=hydrangea_proof,maple_instances=len(trees[::2]),oak_instances=len(trees[1::2]),boxwood_instances=len(shrubs),placement_seed=981+p['seed'],tree_geometry=tree_proof,oak_geometry=oak_proof,shrub_geometry=shrub_proof,included_in_course_gltf=False)
 proof['assembled_texture_allocation']=texture_cost()
 # Preserve reusable native-instance placement, rather than baking the town
 # and every repeated plant into each core course GLB. Paths are clone-relative.
 Path(f'export/Minigolf-{p["seed"]}-context.json').write_text(json.dumps(dict(scope='Companion native-library instance recipe; source paths relative to clone root, positions in Blender meters/Z-up. Roads and utility construction remain in src/context.py.',**proof),indent=2))
 return proof
