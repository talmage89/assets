"""Final GLB-only neutral studio; exact Eye camera and real 1.8 m scale."""
import math
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
from shots import SHOTS as FORM_SHOTS,floor_height,STRIP_SHOT
FINAL_STAGE=True
RENDER_STAGE='final exported GLB with canonical baked 2048 PBR maps'
DEFAULT_SHOTS='hero,hero_right,front,side,back,top,receiver,controls,rear_sight,front_sight,gas_muzzle,wood,grip_stock,grip_detail,trigger,open,aimed,magazine,scale'
SHOTS={**FORM_SHOTS,
 'smg_hero':dict(location=(-1.16,.57,.45),target=(0,.06,.035),lens=63,aspect=2),
 'hero':dict(location=(-1.62,.76,.55),target=(0,.15,.020),lens=60,aspect=2),
 'hero_right':dict(location=(1.62,.76,.55),target=(0,.15,.020),lens=60,aspect=2),
 'back':dict(location=(0,-1.3,.035),target=(0,.15,.020),ortho=.30,aspect=1,rear_light=True),
 'scale':dict(location=(3.8,3.6,1.9),target=(.15,.15,.90),lens=62,aspect=1,scale=True),
 'retainer':dict(location=(-.13,.52,.14),target=(0,.363,.066),lens=95,aspect=1.4),
 'retainer_side':dict(location=(-.22,.398,.10),target=(0,.363,.068),lens=100,aspect=1.2,daylight=-1),
}
for name,shot in SHOTS.items():
 shot['exposure']=-.15
 if name not in ('mag_standalone','mag_lips','cartridge','case','case_mouth'):
  shot.setdefault('action','Idle');shot.setdefault('frame',0)
 else:shot['shell_light']=name in ('cartridge','case','case_mouth');shot['mouth_light']=name=='case_mouth'
from shots import PHOTO_POSES as FORM_PHOTO_POSES
PHOTO_POSES={name:dict(pose,daylight=1 if 'right' in name else -1) for name,pose in FORM_PHOTO_POSES.items()}
from photo_matches import MATCHES
for name,description in MATCHES.items():
 PHOTO_POSES.setdefault(name,{})
 PHOTO_POSES[name]['daylight']=1 if description['location'][0]>0 else -1
PHOTO_POSES['retainer_photo']=dict(diagnostic_isolate=['Handguard_Retainer363','Handguard_SlingMount','Handguard_SlingLoop'],daylight=1,front_component=True)
for shot in PHOTO_POSES.values():shot.setdefault('action','Idle');shot.setdefault('frame',0)
STRIP_SHOT={**STRIP_SHOT,'exposure':-.15}

def configure_scene(scene,source):
 import bpy
 from mathutils import Vector
 from kit import studio
 scene['dense_source']=source.suffix=='.blend'
 if source.suffix=='.glb' and source.name=='ak.glb':
  from delivery import split_imported
  split_imported(scene,BASE/'build/delivery/finalized.blend')
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
 setup={'Key softbox':((.60,.15,.78),35,.55,1.25),
 'Camera fill':((-.65,.22,.45),15,.65,1.1),
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
 if shot.get('diagnostic_prefixes'):
  shot['diagnostic_isolate']=[o.get('part_name',o.name) for o in scene.objects if o.type=='MESH' and any(o.get('part_name',o.name).startswith(p) for p in shot['diagnostic_prefixes'])]
 for ob in scene.objects:
  if ob.type=='MESH' and ob.get('asset_set'):
   ob.hide_render=bool(ob.get('bake_only')) or bool(shot.get('diagnostic_isolate') and ob.get('part_name',ob.name) not in shot['diagnostic_isolate'])
 scene['socket_gray']=bool(aimed)
 scene['scale_shot']=bool(isscale)
 scene['hide_detached_mag']=bool(shot.get('hide_detached_mag') or shot.get('action')=='ReloadEmpty' and 'time_s' not in shot)
 scene.camera.data.dof.use_dof=bool(aimed)
 if aimed:scene.camera.data.dof.focus_distance=.659;scene.camera.data.dof.aperture_fstop=85
 placement=scene.objects['Presentation placement'];placement.location=(.80,0,1.02) if isscale else (0,0,0)
 bpy.context.view_layer.update()
 floor=scene.objects['Studio seamless'];floor.scale=(10,10,10) if isscale else (1,1,1);floor.location.z=0 if isscale else scene['source_floor']
 floor.rotation_euler.z=math.pi if isscale else 0
 scene.objects['Scale fill'].hide_render=not isscale
 bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.8 if shot.get('daylight') else .18
 for ob in scene.objects:
  if ob.get('human_scale'):ob.hide_render=not isscale
  if ob.get('bake_only') or ob.name in ('Case_Proof','Cartridge_Proof') or (ob.name.startswith('HIGH_') and not scene.get('dense_source')):ob.hide_render=True
  if ob.name.startswith('Studio black'):ob.hide_render=True
  if ob.type!='LIGHT' or 'final_energy' not in ob:continue
  ob.location=ob['final_location'];ob.data.energy=ob['final_energy'];ob.data.size,ob.data.size_y=ob['final_size']
  if shot.get('daylight'):
   sign=shot['daylight']
   if ob.name=='Key softbox':ob.location=(sign*.8,.22,.62);ob.data.energy=32;ob.data.size=1.2;ob.data.size_y=1.2
   elif ob.name=='Camera fill':ob.location=(-sign*.7,.22,.50);ob.data.energy=10;ob.data.size=1.0;ob.data.size_y=1.3
   else:ob.data.energy=0
  if shot.get('front_component'):
   if ob.name=='Key softbox':ob.location=(.15,.78,.32);ob.data.energy=32
   elif ob.name=='Camera fill':ob.location=(-.20,.70,.20);ob.data.energy=12
   else:ob.data.energy=0
  if shot.get('shell_light'):
   sign=1 if shot.get('mouth_light') else -1
   if ob.name=='Key softbox':ob.location=(.10,sign*.10,.15);ob.data.energy=.35;ob.data.size=.12;ob.data.size_y=.15
   elif ob.name=='Camera fill':ob.location=(-.06,sign*.12,.05);ob.data.energy=.225;ob.data.size=.14;ob.data.size_y=.12
   elif ob.name=='Right rim strip':ob.location=(.03,-sign*.13,.12);ob.data.energy=.45;ob.data.size=.08;ob.data.size_y=.14
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
  target=Vector((0,.364,.075)) if shot.get('front_component') else Vector((0,.025,0)) if shot.get('shell_light') else Vector((0,.06,1.02 if isscale else .06))
  ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
