"""Studio finals and exact socket view, always from the exported baked GLB."""
from pathlib import Path
import math
import bpy
from mathutils import Vector
from kit import studio
import shots as form
FINAL_STAGE=True
RENDER_STAGE='final exported BrackenL20 GLB / canonical 2048 PBR atlas'
SHOTS={**form.SHOTS,
 'hero':form.shot((1.45,.74,.48),(0,.225,-.012),53,2.65,action='Idle',frame=0),
 'hero_left':form.shot((-1.45,.68,.46),(0,.225,-.012),53,2.65,action='Idle',frame=0),
 'front':form.shot((0,1.5,-.020),(0,0,-.020),ortho=.26,aspect=1.3,action='Idle',frame=0),
 'back':form.shot((0,-1.5,-.02),(0,.20,-.02),ortho=.23,aspect=1.25,action='Idle',frame=0,plate_light=True),
 'butt_plate':form.shot((.14,-.50,.03),(0,-.253,-.05),58,1.4,action='Idle',frame=0,plate_light=True),
 'wrist':form.shot((.24,-.13,.13),(0,.018,.023),75,1.6,action='Idle',frame=0),
 'muzzle':form.shot((.13,.86,.10),(0,.690,.039),78,1.5,action='Idle',frame=0),
 'scale':form.shot((3.8,2.7,1.8),(.0,.10,.9),60,1,action='Idle',frame=0,scale=True),
}
for name,s in SHOTS.items():
 s.setdefault('exposure',-.15);s['background']='transparent'
DEFAULT_SHOTS='hero,hero_left,right,left,front,back,top,receiver,wrist,forend,sights,stock,open,aimed,scale,muzzle'
PHOTO_POSES={**form.PHOTO_POSES,'lever_rest_photo':dict(action='Idle',frame=0),'used_photo':dict(action='Idle',frame=0),'sight_photo':dict(action='Idle',frame=0)}
for pose in PHOTO_POSES.values():pose['exposure']=-.15
STRIP_SHOT={**form.STRIP_SHOT,'exposure':.0}
floor_height=form.floor_height

def configure_scene(scene,source):
 form.configure_scene(scene,source)
 # Suppress isolated indirect fireflies from the highly reflective action;
 # direct reflection-card highlights retain their full photographic range.
 scene.cycles.sample_clamp_indirect=2.0
 # Match the accepted Hearth 12 studio exactly. The old tall frontal cards
 # were calibrated to one oxide patch and made every grazing rub look white.
 # Shader roughness and color are judged in the same light as the precedent.
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.25,.25,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.15
 lighting={
  'Key softbox':((.65,.05,.72),38,.45,1.30),
  'Camera fill':((-.70,.12,.42),15,.55,1.10),
  'Right rim strip':((-.18,.90,.50),18,.10,1.0),
  'Left rim strip':((-.45,-.20,.35),7,.15,.80),
  'Overhead reflection card':((0,.22,.85),7,.32,1.0),
  'Lever top strip':((.05,.20,.8),0,.6,.15),
  'Lever action fill':((.32,.12,.26),0,.30,.30),
  'Lever rear edge':((-.24,-.35,.25),0,.3,.5),
 }
 for name,(location,power,width,height) in lighting.items():
  ob=scene.objects[name];ob.location=location;ob.data.energy=power;ob.data.size=width;ob.data.size_y=height
  ob.rotation_euler=(Vector((0,.22,0))-ob.location).to_track_quat('-Z','Y').to_euler()
 if Path(source).suffix=='.blend':
  for ob in scene.objects:
   if ob.name.startswith('Standalone_'):ob.hide_render=True
 roots=[o for o in scene.objects if not o.get('studio') and o.parent is None and o.type not in ('LIGHT','CAMERA')]
 placement=bpy.data.objects.new('Presentation placement',None);scene.collection.objects.link(placement)
 for ob in roots:ob.parent=placement
 for ob in studio.human():ob.hide_render=True;ob['human_scale']=True
 data=bpy.data.lights.new('Scale fill','AREA');data.energy=420;data.shape='DISK';data.size=3
 ob=bpy.data.objects.new('Scale fill',data);scene.collection.objects.link(ob)
 ob.location=(1,-2,3);ob.rotation_euler=(Vector((0,0,.9))-ob.location).to_track_quat('-Z','Y').to_euler();ob.hide_render=True
 data=bpy.data.lights.new('Butt plate card','AREA');data.energy=5;data.shape='RECTANGLE';data.size=.3;data.size_y=.4
 light=bpy.data.objects.new('Butt plate card',data);scene.collection.objects.link(light)
 light.location=(.12,-.55,.16);light.rotation_euler=(Vector((0,-.253,-.05))-light.location).to_track_quat('-Z','Y').to_euler();light.hide_render=True

def prepare_shot(scene,shot):
 form.prepare_shot(scene,shot)
 scale=shot.get('scale',False)
 placement=scene.objects['Presentation placement'];placement.location=(.50,0,1.03) if scale else (0,0,0)
 for ob in scene.objects:
  if ob.get('human_scale') or ob.name=='Scale fill':ob.hide_render=not scale
 scene.objects['Butt plate card'].hide_render=not shot.get('plate_light',False)
 bpy.context.view_layer.update()
