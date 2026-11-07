"""Presentation-only town instances; every mesh comes from original generators."""
import json,math
from pathlib import Path
import bpy
from mathutils import Vector
from geometry import Batch,pivot
from plan import opposite_seed
from pavement import CONCRETE,ASPHALT,tint
from kit import model as G
BLOCK_CACHE={}


def instance_block(path,location,yaw,name):
 key=str(Path(path).resolve())
 if key in BLOCK_CACHE:
  old=BLOCK_CACHE[key];mapping={o:o.copy() for o in old}
  for a,o in mapping.items():bpy.context.collection.objects.link(o);o.parent=mapping.get(a.parent)
  obs=set(mapping.values())
 else:
  before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=key);obs=set(bpy.data.objects)-before;BLOCK_CACHE[key]=list(obs)
 root=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(root)
 for ob in obs:
  if ob.parent is None:ob.parent=root
 root.location=location;root.rotation_euler.z=math.radians(yaw)
 for ob in list(obs)+[root]:ob['town_group']=name
 return list(obs)+[root]


def setting(p,mats,append,rows,street):
 BLOCK_CACHE.clear()
 W=p['width'];D=max(l['depth'] for l in p['lots']);walk=p['walk'];road=p['road_width'];far=-2*walk-road
 src=Path('build/context/blocks')/(p['region']+'-'+str(opposite_seed(p['seed'],p['region'])))/'block.glb';obs=[]
 # The opposing row is a genuinely different seeded block face. The next
 # intersection and its corner fronts continue the street through the horizon.
 obs+=instance_block(src,(0,far,0),180,'Opposite block')
 obs+=instance_block(src,(W+road+2*walk,0,0),0,'Next block')
 obs+=instance_block(src,(W+road+2*walk,far,0),180,'Next opposite block')
 # A second commercial street behind each alley closes the town's backdrop.
 # Existing mesh data is instanced, so this adds no delivery geometry/maps.
 for j,xx in enumerate((0,W+road+2*walk,-W-road-2*walk)):
  obs+=instance_block(src,(xx,D+19,0),0,'Rear district '+str(j))
  obs+=instance_block(src,(xx,far-D-19,0),180,'Far district '+str(j))
 root=pivot('Town setting',(0,0,0));b=Batch('Town streets',root,mats);b.color_at=lambda v,r,c:tint(v,r,c,p)
 b.box((80,-walk-road/2,-.203),(400,road,.095),'Roof',ASPHALT)
 for lo,hi in ((-160,-W/2-2*walk-road),(W/2+2*walk+road,300)):
  for yy in (far+walk/2,-walk/2):b.box(((lo+hi)/2,yy,-.075),(hi-lo,walk,.15),'Mineral',CONCRETE)
 for side in (-1,1):
  xx=side*(W/2+walk+road/2)
  b.box((xx,0,-.206),(road,420,.095),'Roof',ASPHALT)
  for off in (-1,1):b.box((xx+off*(road/2+walk/2),0,-.077),(walk,420,.15),'Mineral',CONCRETE)
 # Neighborhood grades support the original house foundations at Z=0.
 for yy in (D+156.01,far-D-156.01):
  b.box((45,yy,-.11),(420,150,.22),'Mineral',(.095,.13,.055))
 for yy in (D+74,far-D-74):
  b.box((45,yy,-.203),(420,8,.095),'Roof',ASPHALT)
 for yy in (D+79.5,far-D-79.5):
  b.box((45,yy,-.075),(420,3,.15),'Mineral',CONCRETE)
 for yy in (D+12,far-D-12):b.box((45,yy,-.203),(420,8,.095),'Roof',ASPHALT)
 for yy in (D+17.5,far-D-17.5):b.box((45,yy,-.075),(420,3,.15),'Mineral',CONCRETE)
 for yy in (D+65,far-D-65):b.box((45,yy,-.08),(420,7,.16),'Roof',(.083,.080,.071))
 # Things left by tenants: entry planters, crates and folding menu boards.
 for lot in p['lots']:
  if lot['index']%2:
   x=lot['x']+lot['width']*.34
   b.box((x,-.44,.26),(.46,.43,.52),'Finish',(.11,.085,.05))
   for j in range(7):
    t=j*math.tau/7;b.beam((x,-.44,.50),(x+.18*math.cos(t),-.44+.18*math.sin(t),.78+.12*(j%2)),.05,.018,color=(.075,.13,.045))
   for j in range(2):b.box((x-.60,-.40,.14+j*.26),(.48,.40,.24),'Finish',(.22,.16,.08))
  if lot['tenant'] in ('diner','pharmacy'):
   x=lot['x']+lot['width']*.10
   for sy in (-1,1):
    for dx in (-.27,.27):b.beam((x+dx,-.95+sy*.30,.01),(x+dx,-.95,.91),.035,color=(.11,.09,.065))
   b.box((x,-1.13,.57),(.50,.035,.60),'Finish',(.022,.029,.025))
   for j in range(4):b.box((x,-1.151,.73-j*.08),(.26-.035*(j%2),.002,.010),'Finish',(.53,.51,.43))
 built=b.finish();obs += [root,built]
 spots=street['parking']
 for i,k in enumerate([i for i in range(len(spots)) if i%2==0][:7]):
  s=spots[k];obs+=append(rows[('pickup','crossover','hatchback')[i%3]],(s['x'],s['y'],-.1524),s['yaw'])
  if i%2:
   obs+=append(rows[('hatchback','pickup','crossover')[i%3]],(s['x']+2,far+walk+1.35,-.1524),-90)
 # Trees leave the nearest storefront and cornice legible. Both walks continue.
 for i,pos in enumerate(street['pits']):
  obs+=append(rows['maple'],pos,25*i,.43)
  obs+=append(rows['light'],(pos[0]+2.2,pos[1]-.35,0))
  obs+=append(rows['maple'],(pos[0]+5,far+walk-1,0),65+i*23,.30 if i<2 else .43)
  obs+=append(rows['light'],(pos[0]+6,far+walk-.65,0),180)
 for i in range(11):
  xx=-W*1.4+i*26
  obs+=append(rows['house'],(xx,D+90,0),0)
  obs+=append(rows['maple'],(xx+11,D+82,0),i*31,.68)
  obs+=append(rows['house'],(xx,far-D-90,0),180)
  for yy in (D+114,far-D-114):obs+=append(rows['maple'],(xx+5,yy,0),i*53,.70+.04*(i%3))
 return obs


def light_rooms(p,dusk):
 # Only actual fixtures receive light objects; shared glTF emission remains.
 for m in bpy.data.materials:
  if 'Downtown_Interior' in m.name and m.use_nodes:
   m.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=6.0 if dusk else .13
 for i,l in enumerate(p['lots']):
  if l['tenant']=='vacant':continue
  light=bpy.data.lights.new('Shop fixture '+str(i),'AREA');light.energy=210 if dusk else 170;light.shape='RECTANGLE';light.size=3;light.size_y=1.8;light.specular_factor=0;light.transmission_factor=0;light.color=(1,.68,.35)
  ob=bpy.data.objects.new(light.name,light);bpy.context.collection.objects.link(ob);ob.visible_glossy=False;ob.visible_transmission=False;ob.visible_camera=False;ob.location=(l['x'],2.6,l['floor_first']-1.5)
  ob.rotation_euler=Vector((0,-.5,-1)).to_track_quat('-Z','Y').to_euler()
