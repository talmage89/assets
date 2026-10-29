"""Neutral export-only photography, exact Eye and real 1.8 m scale guide."""
from pathlib import Path
from shots import SHOTS as FORM_SHOTS,PHOTO_POSES,STRIP_SHOT,floor_height
from shots import configure_scene as form_scene,prepare_shot as form_shot
FINAL_STAGE=True
RENDER_STAGE='exported GLB / baked 2048 BaseColor, OpenGL Normal, ORM'
SHOTS={k:dict(v,exposure=-.30) for k,v in FORM_SHOTS.items()}
SHOTS.update({
 'hero':dict(location=(.32,.37,.20),target=(0,.057,.014),lens=68,aspect=1.4,action='Idle',frame=0,exposure=-.30),
 'hero_left':dict(location=(-.33,.37,.19),target=(0,.057,.014),lens=68,aspect=1.4,action='Idle',frame=0,exposure=-.30),
 'wear_front':dict(location=(-.28,.38,.19),target=(-.012,.055,.014),lens=68,aspect=1.4,action='Reload',frame=88,exposure=-.30),
 'rod_detail':dict(location=(-.20,.135,.040),target=(-.0344,.168,.0327),ortho=.044,aspect=1.5,action='Reload',frame=88,exposure=-.30),
 'lug_under':dict(location=(.045,.285,.018),target=(0,.177,.052),lens=72,aspect=1.3,roll=3.141592653589793,action='Idle',frame=0,exposure=-.30),
 'rear_slot':dict(location=(-.085,-.16,.22),target=(0,.008,.066),ortho=.060,aspect=1.3,action='Idle',frame=0,exposure=-.30),
 'back':dict(location=(0,-.6,.014),target=(0,.06,.014),ortho=.17,aspect=1,action='Idle',frame=0,exposure=-.30),
 'scale':dict(location=(.3,3.6,1.3),target=(.3,0,.9),ortho=2.1,aspect=1,action='Idle',frame=0,scale=True,exposure=-.10)})
DEFAULT_SHOTS='hero,hero_left,wear_front,side,front,back,top,open,star,reload,sights,grip,muzzle,shank,frame_bottom,hammer_rest,hammer_cocked,hammer_top,grip_seam,aimed,scale,rod_detail,lug_under,rear_slot'
PHOTO_POSES={k:dict(v,exposure=-.30) for k,v in PHOTO_POSES.items()}
PHOTO_POSES['used_photo']['room_light']=True
STRIP_SHOT=dict(STRIP_SHOT,exposure=-.30)

def configure_scene(scene,source):
 import bpy
 from kit import studio
 from mathutils import Vector
 # Presentation placement leaves all exported rig/socket frames untouched.
 roots=[o for o in scene.objects if not o.get('studio') and o.parent is None]
 placement=bpy.data.objects.new('Presentation placement',None);scene.collection.objects.link(placement)
 for ob in roots:ob.parent=placement
 form_scene(scene,source)
 for ob in studio.human():
  ob.location.x+=.65;ob.hide_render=True;ob['human_scale']=True
 for ob in scene.objects:
  if ob.type=='LIGHT':ob.data.color=(1,1,1)
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.22,.22,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.14
 for name,loc,power,w,h in [
  ('Key softbox',(.31,-.23,.42),6.5,.26,.38),
  ('Camera fill',(-.34,.02,.25),3.5,.30,.38),
  ('Right rim strip',(-.10,.34,.30),5.5,.055,.32),
  ('Left rim strip',(-.32,-.05,.28),1.5,.10,.30),
  ('Overhead reflection card',(0,.06,.48),.6,.16,.24)]:
  ob=scene.objects[name];ob.location=loc;ob.data.energy=power;ob.data.size=w;ob.data.size_y=h
  ob.rotation_euler=(Vector((0,.045,.02))-ob.location).to_track_quat('-Z','Y').to_euler()
  ob['baseline_energy']=power;ob['final_location']=loc
 data=bpy.data.lights.new('Scale fill','AREA');data.energy=250;data.shape='DISK';data.size=2.5
 ob=bpy.data.objects.new('Scale fill',data);scene.collection.objects.link(ob)
 ob.location=(1,-2,3);ob.rotation_euler=(Vector((0,0,.9))-ob.location).to_track_quat('-Z','Y').to_euler();ob.hide_render=True
 for sign in (-1,1):
  data=bpy.data.lights.new('Grip fill '+str(sign),'AREA');data.energy=6;data.specular_factor=.04;data.shape='RECTANGLE';data.size=.20;data.size_y=.22
  ob=bpy.data.objects.new(data.name,data);scene.collection.objects.link(ob);ob.location=(sign*.22,.16,.27)
  ob.visible_glossy=False
  ob.rotation_euler=(Vector((0,-.025,-.020))-ob.location).to_track_quat('-Z','Y').to_euler()
  ob['baseline_energy']=6;ob['final_location']=tuple(ob.location)

def prepare_shot(scene,shot):
 from mathutils import Vector
 form_shot(scene,shot)
 photo=bool(shot.get('room_light'))
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65 if photo else .14
 for ob in scene.objects:
  if ob.name.startswith('Studio black reflection flag'):ob.hide_render=photo or scene.render.engine=='BLENDER_EEVEE'
  if ob.type=='LIGHT' and 'final_location' in ob:ob.data.energy*=.35 if photo else 1
  if photo and ob.name.startswith('Grip fill'):ob.data.energy=26 if ob.name.endswith('-1') else 3
 if shot.get('raking'):scene.objects['Raking inspection strip'].data.energy=1.2
 scale=bool(shot.get('scale'));placement=scene.objects['Presentation placement']
 placement.location=(.20,0,1.02) if scale else (0,0,0)
 # Scale photography presents the full side length beside the silhouette.
 import math
 placement.rotation_euler.z=math.pi/2 if scale else 0
 scene.objects['Scale fill'].hide_render=not scale
 for ob in scene.objects:
  if ob.get('human_scale'):ob.hide_render=not scale
  if ob.type=='LIGHT' and 'final_location' in ob:
   ob.location=Vector(ob['final_location'])+Vector((0,0,1.02 if scale else 0))
 floor=scene.objects['Studio seamless'];floor.scale=(10,10,10) if scale else (1,1,1)
 floor.location.z=.020 if scale else floor_height(Path('export/revolver.glb'))
