"""Export-only finals, daylight comparisons and neutral real-scale presentation."""
import math
from pathlib import Path
from shots import SHOTS as FORM_SHOTS,floor_height,PHOTO_POSES,STRIP_SHOT
FINAL_STAGE=True
RENDER_STAGE='final exported GLB with baked 2048 PBR maps'
DEFAULT_SHOTS='hero,hero_left,front,side,back,top,receiver,wrist,forend,aimed,open,scale'
SHOTS={**FORM_SHOTS,
 'trigger_right':dict(location=(.22,.086,-.014),target=(0,.086,-.014),ortho=.065,aspect=1.5,trigger_light=True),
 'trigger_quarter':dict(location=(.20,.14,.040),target=(0,.086,-.014),ortho=.060,aspect=1.5,trigger_light=True),
 'trigger_pulled':dict(location=(.22,.086,-.014),target=(0,.086,-.014),ortho=.065,aspect=1.5,trigger_light=True,action='Fire',frame=2),
 'hero':dict(location=(1.45,.77,.53),target=(0,.247,-.008),lens=51,aspect=3.0),
 'hero_left':dict(location=(-1.45,.72,.49),target=(0,.247,-.008),lens=51,aspect=3.0),
 'back':dict(location=(0,-1.5,-.010),target=(0,.20,-.010),ortho=.24,aspect=1,rear_light=True),
 'wrist':dict(location=(.26,-.13,.10),target=(0,-.016,-.007),lens=75,aspect=1.5),
 'aimed':dict(location=(0,0,0),target=(0,1,0),aimed=True,
              lens=36/(2*math.tan(math.radians(70)/2)),aspect=16/9,horizontal_fov_degrees=70),
 'aimed_socket':dict(location=(0,0,0),target=(0,1,0),aimed=True,
              lens=36/(2*math.tan(math.radians(70)/2)),aspect=16/9,horizontal_fov_degrees=70),
 'pad':dict(location=(.25,-.43,.055),target=(0,-.247,-.055),lens=78,aspect=1.4),
 'muzzle_under':dict(location=(.16,.86,-.08),target=(0,.690,.038),lens=75,aspect=1.3,muzzle_under_light=True),
 'scale':dict(location=(3.8,3.6,1.9),target=(.15,.15,.90),lens=62,aspect=1.0,scale=True),
}
for name,s in SHOTS.items():
 s['exposure']=-.15;s['background']='transparent'
 if name=='underside':s['under_light']=True
 if name not in ('shell','shell_crimp','hull','hull_primer'):
  s.setdefault('action','Idle');s.setdefault('frame',0)
 if name in ('shell','shell_crimp','hull','hull_primer'):
  s['shell_light']=True;s['mouth_light']=name in ('shell_crimp','hull')
PHOTO_POSES={**PHOTO_POSES,'right_photo':dict(action='Idle',frame=0,daylight=1,exposure=-.15),
 'left_photo':dict(action='Idle',frame=0,daylight=-1,exposure=-.15),
 'open_photo':dict(action='IdleOpen',frame=0,daylight=1,exposure=-.15),
 'used_photo':dict(action='Idle',frame=0,daylight=1,exposure=-.15)}
PHOTO_POSES['wood_photo']=dict(action='Idle',frame=0,daylight=1,exposure=-.15)
STRIP_SHOT={**STRIP_SHOT,'exposure':-.15}

def configure_scene(scene,source):
 import bpy
 from mathutils import Vector
 from kit import studio
 roots=[o for o in scene.objects if not o.get('studio') and o.parent is None]
 placement=bpy.data.objects.new('Presentation placement',None);scene.collection.objects.link(placement)
 for ob in roots:ob.parent=placement
 scene['presentation_source']=str(source)
 for ob in studio.human():
  ob.location.x+=.60;ob.hide_render=True;ob['human_scale']=True
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.25,.25,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.15
 # Camera-only gray studio surround. The existing world still illuminates
 # steel unchanged; the aimed image no longer exports a transparent black sky.
 nt=scene.world.node_tree;old=nt.nodes['Background']
 camera_bg=nt.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=(.15,.16,.17,1)
 path=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader')
 nt.links.new(path.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(old.outputs[0],mix.inputs[1])
 nt.links.new(camera_bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs['Surface'])
 # The shared renderer sets transparency for animated shots immediately before
 # rendering. Override only the two socket stills, locally, after that setting.
 def aimed_backdrop(render_scene,*_):
  if render_scene.get('socket_studio_backdrop'):
   render_scene.render.film_transparent=False
   camera=render_scene.camera;eye=render_scene.objects['Socket_Eye'].matrix_world
   assert (camera.matrix_world.translation-eye.translation).length<1e-7
   for camera_axis,socket_axis in (((0,0,-1),(0,1,0)),((0,1,0),(0,0,1))):
    actual=(camera.matrix_world.to_3x3()@Vector(camera_axis)).normalized()
    expected=(eye.to_3x3()@Vector(socket_axis)).normalized()
    assert (actual-expected).length<1e-7
   assert camera.data.shift_y==0 and camera.data.shift_x==0
   assert abs(math.degrees(camera.data.angle_x)-70)<1e-4
   print('EXACT SOCKET CAMERA: position, forward, up, zero shift, 70 degrees; opaque gray',flush=True)
 bpy.app.handlers.render_pre.append(aimed_backdrop)
 setup={
  'Key softbox':((.65,.05,.72),38,.45,1.30),
  'Camera fill':((-.70,.12,.42),15,.55,1.1),
  'Right rim strip':((-.18,.90,.50),18,.10,1.0),
  'Left rim strip':((-.45,-.20,.35),7,.15,.80),
  'Overhead reflection card':((0,.22,.85),7,.32,1.0),
 }
 for name,(loc,power,w,h) in setup.items():
  ob=scene.objects[name];ob.location=loc;ob.data.color=(1,1,1)
  ob.data.energy=power;ob.data.size=w;ob.data.size_y=h
  ob.rotation_euler=(Vector((0,.22,0))-ob.location).to_track_quat('-Z','Y').to_euler()
  ob['final_energy']=power;ob['final_location']=loc;ob['final_size']=(w,h)
 data=bpy.data.lights.new('Scale fill','AREA');data.energy=380;data.shape='DISK';data.size=3
 light=bpy.data.objects.new('Scale fill',data);scene.collection.objects.link(light)
 light.location=(1,-2,3);light.rotation_euler=(Vector((0,0,.9))-light.location).to_track_quat('-Z','Y').to_euler();light.hide_render=True

def prepare_shot(scene,shot):
 from mathutils import Vector
 import bpy
 isscale=shot.get('scale',False)
 placement=scene.objects['Presentation placement'];placement.location=(.80,0,1.02) if isscale else (0,0,0)
 bpy.context.view_layer.update()
 scene.camera.data.shift_y=shot.get('shift_y',0)
 scene['socket_studio_backdrop']=bool(shot.get('aimed'))
 if shot.get('first_person'):
  # A 12 mm cheek-weld variation for the photographic first-person view.
  # This moves only the studio camera: the delivered socket and rig stay intact.
  eye=scene.objects['Socket_Eye'].matrix_world
  muzzle=scene.objects['Socket_Muzzle'].matrix_world
  shot['location']=tuple(eye.translation+eye.to_3x3()@Vector((0,0,shot['eye_height_offset_m'])))
  shot['target']=tuple(muzzle.translation+muzzle.to_3x3()@Vector((0,-.011,.0156)))
 floor=scene.objects['Studio seamless'];floor.scale=(10,10,10) if isscale else (1,1,1)
 source=Path(scene['presentation_source']);floor.location.z=.020 if isscale else floor_height(source)
 scene.objects['Scale fill'].hide_render=not isscale
 for ob in scene.objects:
  if ob.get('human_scale'):ob.hide_render=not isscale
  if ob.get('bake_only'):ob.hide_render=True
  if source.suffix=='.blend' and ob.name.startswith('Standalone_'):ob.hide_render=True
  if ob.type!='LIGHT' or 'final_energy' not in ob:continue
  ob.location=ob['final_location'];ob.data.energy=ob['final_energy'];ob.data.size,ob.data.size_y=ob['final_size']
  if shot.get('daylight'):
   sign=shot['daylight']
   if ob.name=='Key softbox':
    ob.location=(sign*.8,.22,.62);ob.data.energy=40;ob.data.size=1.2;ob.data.size_y=1.2
   elif ob.name=='Camera fill':
    ob.location=(-sign*.7,.22,.50);ob.data.energy=12;ob.data.size=1.0;ob.data.size_y=1.3
   else:ob.data.energy=0
  if shot.get('shell_light'):
   sign=1 if shot.get('mouth_light') else -1
   if ob.name=='Key softbox':
    ob.location=(.10,sign*.10,.15);ob.data.energy=1.4;ob.data.size=.12;ob.data.size_y=.15
   elif ob.name=='Camera fill':
    ob.location=(-.06,sign*.12,.05);ob.data.energy=.9;ob.data.size=.14;ob.data.size_y=.12
   elif ob.name=='Right rim strip':
    ob.location=(.03,-sign*.13,.12);ob.data.energy=1.8;ob.data.size=.08;ob.data.size_y=.14
   else:ob.data.energy=0
  if shot.get('rear_light'):
   if ob.name=='Key softbox':
    ob.location=(.20,-.70,.42);ob.data.energy=45;ob.data.size=.40;ob.data.size_y=.60
   elif ob.name=='Camera fill':
    ob.location=(-.40,-.60,.15);ob.data.energy=20;ob.data.size=.40;ob.data.size_y=.50
   else:ob.data.energy=0
  if shot.get('under_light'):
   if ob.name=='Key softbox':
    ob.location=(.20,.0,-.30);ob.data.energy=8;ob.data.size=.25;ob.data.size_y=.40
   elif ob.name=='Camera fill':
    ob.location=(-.25,.10,-.20);ob.data.energy=3;ob.data.size=.35;ob.data.size_y=.40
   else:ob.data.energy=0
  if shot.get('aimed') or shot.get('first_person'):
   if ob.name=='Key softbox':
    ob.location=(.65,-.30,.60);ob.data.energy=16;ob.data.size=.50;ob.data.size_y=.70
   elif ob.name=='Camera fill':
    ob.location=(-.65,-.20,.35);ob.data.energy=4;ob.data.size=.50;ob.data.size_y=.70
   else:ob.data.energy=0
  if shot.get('muzzle_under_light'):
   if ob.name=='Key softbox':
    ob.location=(.30,.75,-.30);ob.data.energy=8;ob.data.size=.25;ob.data.size_y=.35
   elif ob.name=='Camera fill':
    ob.location=(-.30,.60,-.15);ob.data.energy=3;ob.data.size=.30;ob.data.size_y=.50
   else:ob.data.energy=0
  if shot.get('trigger_light'):
   sign=1 if shot['location'][0]>0 else -1
   if ob.name=='Key softbox':
    ob.location=(sign*.15,.22,.10);ob.data.energy=2;ob.data.size=.12;ob.data.size_y=.20
   elif ob.name=='Camera fill':
    ob.location=(-sign*.16,.12,.04);ob.data.energy=1;ob.data.size=.14;ob.data.size_y=.16
   elif ob.name=='Right rim strip':
    ob.location=(-sign*.12,-.01,.10);ob.data.energy=.7;ob.data.size=.06;ob.data.size_y=.15
   else:ob.data.energy=0
  if isscale:ob.location+=Vector((0,0,1));ob.data.energy*=1.5
  target=Vector((0,.690,.045)) if shot.get('muzzle_under_light') else (Vector((0,-.20,-.035)) if shot.get('rear_light') else (
   Vector((0,.13,.010)) if shot.get('under_light') else (
   Vector((0,.025,0)) if shot.get('shell_light') else Vector((0,.22,1.02 if isscale else 0)))))
  if shot.get('trigger_light'):target=Vector((0,.086,-.014))
  ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
