"""Presentation from existing local library exports; never included in signal GLBs."""
import math,hashlib,json
from pathlib import Path
import bpy
from geometry import root,box,M
from kit.tiling import world_uv
from plan import *
ROOT=Path(__file__).resolve().parents[2]
def load(path):
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
 added=set(bpy.context.scene.objects)-before
 return {o.name:o for o in added if o.parent not in added},added
def clone(source,name,loc,yaw=0):
 obs=[source,*source.children_recursive];cop={}
 for o in obs:
  cp=o.copy();bpy.context.collection.objects.link(cp);cop[o]=cp
 for o,cp in cop.items():
  cp.parent=cop.get(o.parent);cp.matrix_basis=o.matrix_basis.copy();cp.name=name+'__'+o.name
 r=cop[source];r.location=loc;r.rotation_mode='XYZ';r.rotation_euler=(0,0,math.radians(yaw));return r
def ground():
 native,old=load(ROOT/'ground/export/Ground.glb')
 arterial,old2=load(ROOT/'ground/export/ArterialCheckpoint.glb')
 def place(lib,kind,name,loc=(0,0,0),yaw=0):return clone(lib[kind],name,loc,yaw)
 place(arterial,'Road_Arterial_Intersection','ArterialJunction')
 for turn in range(4):
  angle=turn*90
  for kind in ('Curb_Corner','Sidewalk_Corner','Lawn_CornerStrip','Lawn_CornerYard'):
   place(native,kind,f'Ground_{kind}_{turn}',xy(CORE,CORE,angle),angle)
  for i in range(14):
   y=CORE+(i+.5)*6.096
   place(arterial,'Road_Arterial_3Lane',f'Road{turn}_{i}',xy(0,y,angle),angle)
   # End the solid turn pocket at 90 ft; the checkpoint keeps a generous approach.
   if i<5:place(arterial,'Markings_Arterial_Lanes',f'LaneLines{turn}_{i}',xy(0,y,angle),angle+180)
   for side in (-1,1):
    syaw=angle+(180 if side<0 else 0)
    for j in range(2):
     yy=CORE+i*6.096+(j+.5)*3.048
     kind='Curb_Ramp' if i==0 and j==0 else 'Curb_Straight'
     place(native,kind,f'Curb{turn}_{side}_{i}_{j}',xy(side*FACE,yy,angle),syaw)
     if i!=0 or j!=0:place(native,'Lawn_Strip',f'Verge{turn}_{side}_{i}_{j}',xy(side*(FACE+.1524),yy,angle),syaw)
    if i==0:place(native,'Sidewalk_Ramp',f'Ramp{turn}_{side}',xy(side*(FACE+.1524),CROSS,angle),syaw)
    for j in range(4):
     if i==0 and j<2:continue
     place(native,'Sidewalk_A',f'Walk{turn}_{side}_{i}_{j}',xy(side*(FACE+.1524+1.8288),CORE+i*6.096+(j+.5)*1.524,angle),syaw)
  place(arterial,'Markings_Arterial_Crosswalk',f'Crosswalk{turn}',xy(0,CROSS,angle),angle)
  place(arterial,'Markings_Arterial_Stop',f'Stop{turn}',xy(0,STOP,angle),angle+180)
  for i in range(2):
   place(arterial,'Markings_Arterial_LeftArrow',f'Left{turn}_{i}',xy(0,STOP+5+i*10,angle),angle+180)
   place(arterial,'Markings_Arterial_ThroughArrow',f'Through{turn}_{i}',xy(-LANE,STOP+5+i*10,angle),angle+180)
  for x in (0,-LANE):
   place(arterial,'Decal_DetectorLoop',f'Detector{turn}_{x}',xy(x,STOP+2.7,angle),angle)
 # Use native lawn materials, with untinted display; the texture allocation is shared.
 lawn=next(m for m in bpy.data.materials if m.name=='Lawn')
 from kit import model as G
 for sx in (-1,1):
  for sy in (-1,1):
   x0=FACE+.1524+1.8288+1.524
   vs=[(sx*x,sy*y,.168) for x,y in [(CORE,CORE),(120,CORE),(120,120),(CORE,120)]]
   o=G.mesh('Neighborhood lawn',vs,[(0,1,2,3)],lawn);world_uv(o,3.048)
   colors=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
   for v in colors.data:v.color=(1,1,1,1)
   for axis in range(2):
    vs=[(sx*x,sy*y,.168) for x,y in ([(x0,CORE),(CORE,CORE),(CORE,120),(x0,120)] if axis==0 else [(CORE,x0),(120,x0),(120,CORE),(CORE,CORE)])]
    o=G.mesh('Walk-side lawn',vs,[(0,1,2,3)],lawn);world_uv(o,3.048)
    colors=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
    for v in colors.data:v.color=(1,1,1,1)
 for o in old|old2:bpy.data.objects.remove(o,do_unlink=True)
 # The added standing pads replace sod at the walk, rather than covering
 # grass cards. Only placed copies change; the Ground library stays untouched.
 pads=[]
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and 'APS_Landing_' in ob.name:
   pts=[ob.matrix_world@v.co for v in ob.data.vertices]
   pads.append((min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)))
 import bmesh
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or not ob.name.startswith('Verge'):continue
  pts=[ob.matrix_world@v.co for v in ob.data.vertices]
  bounds=(min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts))
  touched=[r for r in pads if bounds[0]<r[1] and bounds[1]>r[0] and bounds[2]<r[3] and bounds[3]>r[2]]
  if not touched:continue
  ob.data=ob.data.copy()
  for v in ob.data.vertices:v.co.z-=.003
  bm=bmesh.new();bm.from_mesh(ob.data);remove=[]
  for face in bm.faces:
   if 'Foliage' not in ob.data.materials[face.material_index].name:continue
   pts=[ob.matrix_world@v.co for v in face.verts]
   if any(min(p.x for p in pts)<r[1]+.015 and max(p.x for p in pts)>r[0]-.015 and min(p.y for p in pts)<r[3]+.015 and max(p.y for p in pts)>r[2]-.015 for r in touched):remove.append(face)
  if remove:bmesh.ops.delete(bm,geom=remove,context='FACES')
  bm.to_mesh(ob.data);bm.free()
def context(seed):
 provenance=[]
 def library(relative):
  path=ROOT/relative;lib,old=load(path)
  base=root('LibraryContext_'+path.stem)
  for ob in lib.values():ob.parent=base
  provenance.append(dict(source=relative,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  return base,old|{base}
 libraries={}
 cases=[
  ('houses/export/HearthfieldRanch-11.gltf',(-23,24,.168),90),
  ('houses/export/HearthfieldCape-31.gltf',(24,29,.168),-90),
  ('houses/export/HearthfieldSplit-51.gltf',(-24,-29,.168),90),
  ('houses/export/HearthfieldRanch-11.gltf',(24,-28,.168),-90),
  ('cars/export/AlderC150.glb',(LANE,-17.0,.112),180),
  ('cars/export/AlderC150.glb',(-LANE,24,.112),0),
  ('cars/export/AlderC150.glb',(23,LANE,.112),-90)]
 for i,(rel,loc,yaw) in enumerate(cases):
  if rel not in libraries:libraries[rel]=library(rel)
  base,_=libraries[rel];clone(base,'Context_'+str(i),loc,yaw)
 # Original native tree geometry is instanced, with different layouts per town.
 for i,(x,y) in enumerate(((-17,15),(17,17),(-19,-15),(19,-18),(-27,42),(31,-45),(-44,24),(45,32),(-30,-48),(24,48))):
  rel='trees/export/PinOak.glb' if (i+seed)%2 else 'trees/export/RedMaple.glb'
  if rel not in libraries:libraries[rel]=library(rel)
  base,_=libraries[rel];clone(base,'ContextTree_'+str(i),(x+(seed-201)*.7,y,.168),i*47)
 for base,objs in libraries.values():
  for o in objs:bpy.data.objects.remove(o,do_unlink=True)
 return provenance

def audit_ground():
 """Actual ray intersections catch ignored native quaternion/Euler rotations."""
 from mathutils import Vector
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();rows=[]
 for turn in range(4):
  for x in (-8.2,-6.5,-4.7,0,4.7,6.5,8.2):
   p=xy(x,CORE+7,turn*90,50)
   ok,hit,n,idx,ob,_=bpy.context.scene.ray_cast(dg,Vector(p),Vector((0,0,-1)))
   assert ok,('Ground hole',turn,x)
   assert -.01<hit.z<.22,('Ground height',ob.name,hit.z)
   assert n.z>.8,('Ground normal',ob.name,tuple(n))
   rows.append(dict(turn=turn,transverse_m=x,mesh=ob.name,height_m=hit.z))
 Path('build/ground-placement.json').write_text(json.dumps(dict(passed=True,method='28 actual source-surface vertical intersections across four native-module approaches',samples=rows),indent=2))
 return rows
