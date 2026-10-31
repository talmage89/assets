"""Final GLB-only neutral studio; exact Eye camera and real 1.8 m scale."""
import math
from pathlib import Path
from shots import SHOTS as FORM_SHOTS,floor_height,STRIP_SHOT
FINAL_STAGE=True
RENDER_STAGE='final exported GLB with canonical baked 2048 PBR maps'
DEFAULT_SHOTS='hero,hero_right,front,side,back,top,receiver,handle,sights,front_sight,lower,aimed,locked,scale'
SHOTS={**FORM_SHOTS,
 'projection_lower':dict(location=(-.24,.16,.09),target=(0,.045,.044),lens=80,aspect=1.4),
 'projection_barrel':dict(location=(-.17,.57,.18),target=(0,.386,.095),lens=80,aspect=1.4),
 'hero':dict(location=(-1.16,.57,.45),target=(0,.06,.035),lens=63,aspect=2),
 'hero_right':dict(location=(1.2,.61,.49),target=(0,.06,.035),lens=63,aspect=2),
 'back':dict(location=(0,-1.3,.035),target=(0,.06,.035),ortho=.30,aspect=1,rear_light=True),
 'scale':dict(location=(3.8,3.6,1.9),target=(.15,.15,.90),lens=62,aspect=1,scale=True),
}
for name,shot in SHOTS.items():
 shot['exposure']=-.15
 if name not in ('mag_standalone','mag_lips','cartridge','case','case_mouth'):
  shot.setdefault('action','Idle');shot.setdefault('frame',0)
 else:shot['shell_light']=name in ('cartridge','case','case_mouth');shot['mouth_light']=name=='case_mouth'
PHOTO_POSES={'right_photo':dict(daylight=1),'left_photo':dict(daylight=-1),
 'locked_photo':dict(daylight=-1,action='ReloadEmpty',frame=90,hide_detached_mag=True),'trigger_photo':dict(daylight=-1),
 'used_photo':dict(daylight=-1)}
for shot in PHOTO_POSES.values():shot.setdefault('action','Idle');shot.setdefault('frame',0)
PHOTO_POSES['paint_issued_photo']=dict(daylight=-1,action='ReloadEmpty',frame=90,hide_detached_mag=True,paint_photo='paint_issued_photo')
PHOTO_POSES['paint_studio_photo']=dict(daylight=-1,action='Idle',frame=0)
for _name in ['paint_studio_photo', 'locked_photo']:
 PHOTO_POSES[_name]['paint_photo']=_name
STRIP_SHOT={**STRIP_SHOT,'exposure':-.15}

def configure_scene(scene,source):
 import bpy
 from mathutils import Vector
 from kit import studio
 placement=bpy.data.objects.new('Presentation placement',None);scene.collection.objects.link(placement)
 for ob in [o for o in scene.objects if not o.get('studio') and o.parent is None and o!=placement]:ob.parent=placement
 for ob in studio.human():ob.location.x+=.60;ob.hide_render=True;ob['human_scale']=True
 nt=scene.world.node_tree;bg=nt.nodes['Background'];bg.inputs['Color'].default_value=(.25,.25,.25,1);bg.inputs['Strength'].default_value=.18
 camera_bg=nt.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=(.18,.19,.20,1)
 path=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader')
 nt.links.new(path.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(bg.outputs[0],mix.inputs[1]);nt.links.new(camera_bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs['Surface'])
 def gray_socket(sc,*_):
  if sc.get('scale_shot'):
   sc.render.film_transparent=False;sc.objects['Studio seamless'].hide_render=False
   sc.camera.data.clip_end=200
  if sc.get('hide_detached_mag'):
   arm=next((o for o in sc.objects if o.type=='ARMATURE'),None)
   if arm:
    # Freeze this one presentation pose so render-time animation evaluation
    # cannot restore the offscreen, removed magazine. The delivery is untouched.
    saved={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
    arm.animation_data.action=None
    for b in arm.pose.bones:b.matrix_basis=saved[b.name]
    arm.pose.bones['Magazine'].scale=(0,0,0);bpy.context.view_layer.update()
  if sc.get('socket_gray'):
   sc.render.film_transparent=False;eye=sc.objects['Socket_Eye'].matrix_world;cam=sc.camera
   assert (cam.matrix_world.translation-eye.translation).length<1e-7
   assert ((cam.matrix_world.to_3x3()@Vector((0,0,-1))).normalized()-(eye.to_3x3()@Vector((0,1,0))).normalized()).length<1e-7
 bpy.app.handlers.render_pre.append(gray_socket)
 setup={'Key softbox':((.60,.15,.78),18,.55,1.25),
 'Camera fill':((-.65,.22,.45),4,.65,1.1),
 'Right rim strip':((-.18,.85,.55),13,.14,1.0),
 'Left rim strip':((-.45,-.20,.35),5,.15,.70),
 'Overhead reflection card':((0,.15,.75),5,.30,.8)}
 for name,(loc,power,width,height) in setup.items():
  ob=scene.objects[name];ob.location=loc;ob.data.color=(1,1,1);ob.data.energy=power;ob.data.size=width;ob.data.size_y=height
  ob['final_location']=loc;ob['final_energy']=power;ob['final_size']=(width,height)
 data=bpy.data.lights.new('Scale fill','AREA');data.energy=1000;data.shape='DISK';data.size=3
 light=bpy.data.objects.new('Scale fill',data);scene.collection.objects.link(light);light.location=(0,-3,6);light.rotation_euler=(Vector((0,0,.9))-light.location).to_track_quat('-Z','Y').to_euler();light.hide_render=True;light.visible_camera=False
 scene['source_floor']=floor_height(source)

def prepare_shot(scene,shot):
 import bpy
 from mathutils import Vector
 isscale=shot.get('scale',False);aimed=shot.get('aimed',False)
 scene['socket_gray']=bool(aimed)
 scene['scale_shot']=bool(isscale)
 scene['hide_detached_mag']=bool(shot.get('hide_detached_mag') or shot.get('action')=='ReloadEmpty' and 'time_s' not in shot)
 scene.camera.data.dof.use_dof=bool(aimed)
 if aimed:scene.camera.data.dof.focus_distance=.4055;scene.camera.data.dof.aperture_fstop=85
 placement=scene.objects['Presentation placement'];placement.location=(.80,0,1.02) if isscale else (0,0,0)
 bpy.context.view_layer.update()
 floor=scene.objects['Studio seamless'];floor.scale=(10,10,10) if isscale else (1,1,1);floor.location.z=0 if isscale else scene['source_floor']
 floor.rotation_euler.z=math.pi if isscale else 0
 scene.objects['Scale fill'].hide_render=not isscale
 bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.8 if shot.get('daylight') else .045
 for ob in scene.objects:
  if ob.get('human_scale'):ob.hide_render=not isscale
  if ob.get('bake_only') or ob.name in ('Case_Proof','Cartridge_Proof') or ob.name.startswith('HIGH_'):ob.hide_render=True
  if ob.name.startswith('Studio black'):ob.hide_render=True
  if ob.type!='LIGHT' or 'final_energy' not in ob:continue
  ob.location=ob['final_location'];ob.data.energy=ob['final_energy'];ob.data.size,ob.data.size_y=ob['final_size']
  if shot.get('daylight'):
   sign=shot['daylight']
   if ob.name=='Key softbox':ob.location=(sign*.8,.22,.62);ob.data.energy=32;ob.data.size=1.2;ob.data.size_y=1.2
   elif ob.name=='Camera fill':ob.location=(-sign*.7,.22,.50);ob.data.energy=10;ob.data.size=1.0;ob.data.size_y=1.3
   else:ob.data.energy=0
  if shot.get('shell_light'):
   sign=1 if shot.get('mouth_light') else -1
   if ob.name=='Key softbox':ob.location=(.10,sign*.10,.15);ob.data.energy=1.4;ob.data.size=.12;ob.data.size_y=.15
   elif ob.name=='Camera fill':ob.location=(-.06,sign*.12,.05);ob.data.energy=.9;ob.data.size=.14;ob.data.size_y=.12
   elif ob.name=='Right rim strip':ob.location=(.03,-sign*.13,.12);ob.data.energy=1.8;ob.data.size=.08;ob.data.size_y=.14
   else:ob.data.energy=0
  if shot.get('rear_light'):
   if ob.name=='Key softbox':ob.location=(.20,-.70,.42);ob.data.energy=25
   elif ob.name=='Camera fill':ob.location=(-.40,-.60,.15);ob.data.energy=12
   else:ob.data.energy=0
  if aimed:
   if ob.name=='Key softbox':ob.location=(.65,-.30,.60);ob.data.energy=14
   elif ob.name=='Camera fill':ob.location=(-.65,-.20,.35);ob.data.energy=5
   else:ob.data.energy=0
  if isscale:ob.location+=Vector((0,0,1));ob.data.energy*=1.5
  target=Vector((0,.025,0)) if shot.get('shell_light') else Vector((0,.06,1.02 if isscale else .06))
  ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()

# Photo light rigs apply only to their calibrated views; the family studio serves heroes and GIFs.
_prepare_paint_base=prepare_shot
def prepare_shot(scene,shot):
 _prepare_paint_base(scene,shot)
 from guns.common.paint_review import apply_lights
 apply_lights(scene,shot,Path(__file__).resolve().parents[1])
