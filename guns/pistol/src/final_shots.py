"""Final C9 views, neutral procedural lighting and an actual 1.8 m scale cue."""
import math
from pathlib import Path
from shots import SHOTS as FORM_SHOTS, floor_height, PHOTO_POSES, STRIP_SHOT
FINAL_STAGE=True
RENDER_STAGE='final exported GLB with baked 2048 PBR maps'
DEFAULT_SHOTS='hero,hero_left,front,side,back,top,rear_sights,grip_texture,port_hood,markings,aimed,locked,scale,hand_frame'
SHOTS={**FORM_SHOTS,
 'trigger_right':dict(location=(.22,.047,.014),target=(0,.047,.014),ortho=.052,aspect=1.3,trigger_light=True,action='Idle',frame=0,exposure=-.15),
 'trigger_quarter':dict(location=(.18,.15,.065),target=(0,.047,.014),ortho=.055,aspect=1.3,trigger_light=True,action='Idle',frame=0,exposure=-.15),
 'trigger_pulled':dict(location=(.22,.047,.014),target=(0,.047,.014),ortho=.052,aspect=1.3,trigger_light=True,action='Fire',frame=2,exposure=-.15),
 'hero':dict(location=(.32,.29,.155),target=(0,.043,.009),lens=67,aspect=1.42,exposure=-.15),
 'hero_left':dict(location=(-.30,.28,.15),target=(0,.043,.008),lens=67,aspect=1.42,exposure=-.15),
 'side':dict(location=(-.5,.043,.008),target=(0,.043,.008),ortho=.220,aspect=1.42,exposure=-.15),
 'front':dict(location=(0,.65,.010),target=(0,.043,.010),ortho=.160,aspect=1,exposure=-.15),
 'back':dict(location=(0,-.65,.010),target=(0,.043,.010),ortho=.160,aspect=1,exposure=-.15),
 'top':dict(location=(0,.043,.65),target=(0,.043,0),ortho=.220,aspect=1.42,roll=math.pi/2,exposure=-.15),
 'rear_sights':dict(location=(.125,-.23,.15),target=(0,-.009,.054),lens=80,aspect=1.42,exposure=-.15),
 'grip_texture':dict(location=(-.175,.095,.057),target=(0,-.003,-.012),lens=76,aspect=1.25,exposure=-.15),
 'port_hood':dict(location=(.19,.24,.19),target=(0,.049,.057),lens=88,aspect=1.42,exposure=-.15),
 'markings':dict(location=(-.22,.16,.115),target=(0,.041,.047),lens=90,aspect=1.42,exposure=-.15),
 'locked':dict(location=(.32,.27,.16),target=(0,.027,.010),lens=68,aspect=1.42,action='IdleOpen',frame=0,exposure=-.15),
 'scale':dict(location=(2.6,3.2,1.65),target=(-.17,0,.90),lens=68,aspect=.80,scale=True,exposure=-.15),
 'hand_frame':dict(location=(.40,.36,.17),target=(.015,.04,.035),ortho=.255,aspect=1,
                   hand_frame=True,guide_length_m=.190,exposure=-.15),
 'mag_standalone':dict(location=(.17,.13,.055),target=(0,-.013,-.044),lens=65,aspect=1.1,exposure=-.15),
 'mag_rear':dict(location=(.12,-.18,.035),target=(0,-.014,-.044),lens=62,aspect=1.1,exposure=-.15),
 'case':dict(location=(.032,-.028,.024),target=(0,.008,0),lens=65,aspect=1.35,exposure=-.15),
 'case_mouth':dict(location=(.025,.044,.026),target=(0,.010,0),lens=65,aspect=1.35,exposure=-.15),
}
PHOTO_POSES={**PHOTO_POSES,'right_photo':dict(daylight=1,exposure=-.15),
 'open_photo':dict(action='IdleOpen',frame=0,daylight=1,exposure=-.15),
 'left_photo':dict(daylight=-1,exposure=-.15)}
STRIP_SHOT={**STRIP_SHOT,'exposure':-.15}

def configure_scene(scene,source):
 import bpy
 from kit import studio
 # Parent only for presentation placement. The exported rig stays untouched.
 roots=[o for o in scene.objects if not o.get('studio') and o.parent is None]
 placement=bpy.data.objects.new('Presentation placement',None);scene.collection.objects.link(placement)
 for ob in roots:ob.parent=placement
 scene['presentation_source']=str(source)
 humans=studio.human()
 for ob in humans:
  ob.location.x+=.68;ob.hide_render=True;ob['human_scale']=True
 # A hand-length dimension frame is a presentation guide, not a hand-fit claim.
 from kit import model as G
 material=studio.studio_mat('190 mm guide',(.10,.105,.10),.8)
 guide=[G.cylinder('Hand-length guide',(.110,.020,-.056),(.110,.020,.134),.00022,material,12)]
 for z in (-.056,.134):
  guide.append(G.cylinder('Guide end tick',(.110,.016,z),(.110,.024,z),.00022,material,12))
 from kit.fonts import find_font
 data=bpy.data.curves.new('Hand-length label','FONT');data.body='190 mm';data.size=.006
 data.align_x='CENTER';data.align_y='CENTER';data.font=bpy.data.fonts.load(find_font('Noto Sans','Regular'))
 label=bpy.data.objects.new('Hand-length label',data);scene.collection.objects.link(label)
 label.location=(.135,.020,.039);label.data.materials.append(material);guide.append(label)
 for ob in guide:ob['hand_guide']=True;ob['studio']=True;ob.hide_render=True
 for ob in scene.objects:
  if ob.type=='LIGHT':
   ob.data.color=(1,1,1);ob['studio_energy']=ob.data.energy
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.22,.22,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.12
 # Broad neutral cards distinguish rough black metal from warmer satin polymer.
 setup={
  'Key softbox':((.31,-.23,.42),6.5,.26,.38),
  'Camera fill':((-.34,.02,.25),3.5,.30,.38),
  'Right rim strip':((-.10,.34,.30),5.5,.055,.32),
  'Left rim strip':((-.32,-.05,.28),1.5,.10,.30),
  'Overhead reflection card':((0,.06,.48),.6,.16,.24),
 }
 from mathutils import Vector
 for name,(loc,power,w,h) in setup.items():
  ob=scene.objects[name];ob.location=loc;ob.data.energy=power;ob.data.size=w;ob.data.size_y=h
  ob.rotation_euler=(Vector((0,.035,.010))-ob.location).to_track_quat('-Z','Y').to_euler()
  ob['final_energy']=power;ob['final_location']=loc
  ob['final_size']=(w,h)
 data=bpy.data.lights.new('Scale fill','AREA');data.energy=300;data.shape='DISK';data.size=2.5
 light=bpy.data.objects.new('Scale fill',data);scene.collection.objects.link(light)
 light.location=(1,-2,3);light.rotation_euler=(Vector((0,0,.9))-light.location).to_track_quat('-Z','Y').to_euler()
 light.hide_render=True

def prepare_shot(scene,shot):
 from mathutils import Vector
 import bpy
 placement=scene.objects['Presentation placement'];placement.location=(.08,0,1.02) if shot.get('scale') else (0,0,0)
 floor=scene.objects['Studio seamless']
 source=Path(scene['presentation_source'])
 floor.scale=(10,10,10) if shot.get('scale') else (1,1,1)
 floor.location.z=.020 if shot.get('scale') else floor_height(source)
 scene.objects['Scale fill'].hide_render=not shot.get('scale',False)
 for ob in scene.objects:
  if ob.get('human_scale'):ob.hide_render=not shot.get('scale',False)
  if ob.get('hand_guide'):ob.hide_render=not shot.get('hand_frame',False)
 if shot.get('hand_frame'):
  scene.objects['Hand-length label'].rotation_euler=(Vector(shot['target'])-Vector(shot['location'])).to_track_quat('-Z','Y').to_euler()
 for ob in scene.objects:
  if ob.type!='LIGHT' or 'final_energy' not in ob:continue
  ob.location=ob['final_location'];ob.data.energy=ob['final_energy']
  ob.data.size,ob.data.size_y=ob['final_size']
  if shot.get('daylight'):
   sign=shot['daylight']
   if ob.name=='Key softbox':
    ob.location=(sign*.38,.03,.26);ob.data.energy=8.0;ob.data.size=.65;ob.data.size_y=.55
   elif ob.name=='Camera fill':
    ob.location=(-sign*.35,.03,.20);ob.data.energy=3.0;ob.data.size=.55;ob.data.size_y=.5
   else:ob.data.energy=0
  if shot.get('trigger_light'):
   sign=1 if shot['location'][0]>0 else -1
   if ob.name=='Key softbox':
    ob.location=(sign*.15,.18,.12);ob.data.energy=2;ob.data.size=.12;ob.data.size_y=.20
   elif ob.name=='Camera fill':
    ob.location=(-sign*.16,.10,.07);ob.data.energy=1;ob.data.size=.14;ob.data.size_y=.16
   elif ob.name=='Right rim strip':
    ob.location=(-sign*.12,-.05,.10);ob.data.energy=.7;ob.data.size=.06;ob.data.size_y=.15
   else:ob.data.energy=0
  if shot.get('scale'):
   ob.location+=Vector((0,0,1));ob.data.energy*=1.5
  ob.rotation_euler=(Vector((0,.035,1.02 if shot.get('scale') else .010))-ob.location).to_track_quat('-Z','Y').to_euler()
