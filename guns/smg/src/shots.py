"""Relay 9 inspection cameras; exact optical frame for the aimed view."""
import math
C=(0,.06,.035)
SHOTS={
 'right':dict(location=(1.2,.61,.49),target=C,lens=63,aspect=2),
 'left':dict(location=(-1.16,.57,.45),target=C,lens=63,aspect=2),
 'raking_right':dict(location=(.93,.48,.38),target=C,lens=58,aspect=2,raking=1),
 'raking_left':dict(location=(-.88,-.43,.34),target=C,lens=58,aspect=2,raking=-1),
 'side':dict(location=(1.3,.06,.035),target=C,ortho=.76,aspect=2.55),
 'top':dict(location=(0,.06,1.3),target=(0,.06,0),ortho=.76,aspect=3.0,roll=math.pi/2),
 'front':dict(location=(0,1.3,.035),target=C,ortho=.30,aspect=1),
 'receiver':dict(location=(.45,.29,.25),target=(0,.065,.106),lens=70,aspect=1.65),
 'lower':dict(location=(-.28,.17,.15),target=(0,.044,.030),lens=65,aspect=1.4),
 'lower_raking_left':dict(location=(-.28,.18,.12),target=(0,.025,.020),lens=65,aspect=1.45,raking=-1),
 'lower_raking_right':dict(location=(.28,.18,.12),target=(0,.025,.020),lens=65,aspect=1.45,raking=1),
 'trigger':dict(location=(-.19,.11,.080),target=(0,.062,.025),lens=85,aspect=1.3),
 'case_mouth':dict(location=(.020,.050,.021),target=(0,.014,0),lens=78,aspect=1.25),
 'stock':dict(location=(-.42,-.42,.29),target=(0,-.174,.062),lens=67,aspect=1.65),
 'handguard':dict(location=(-.31,.40,.22),target=(0,.265,.093),lens=68,aspect=1.7),
 'sights':dict(location=(.14,-.20,.24),target=(0,-.012,.142),lens=75,aspect=1.4),
 'front_sight':dict(location=(.12,.51,.21),target=(0,.362,.134),lens=77,aspect=1.4),
 'handle':dict(location=(-.19,.35,.23),target=(-.012,.278,.126),lens=73,aspect=1.5),
 'locked':dict(location=(-.43,.42,.29),target=(0,.20,.106),lens=65,aspect=1.65,action='ReloadEmpty',frame=90),
 'locked_close':dict(location=(-.21,.29,.22),target=(-.009,.224,.129),lens=75,aspect=1.5,action='Charge',frame=50),
 'port_open':dict(location=(.17,.24,.40),target=(0,.137,.079),lens=78,aspect=1.5,action='Fire',frame=4),
 'magazine':dict(location=(.36,.36,.13),target=(0,.166,.012),lens=67,aspect=1.5,action='Reload',frame=23),
 'aimed':dict(location=(0,0,0),target=(0,1,0),aimed=True,lens=85,aspect=1.6),
 'mag_standalone':dict(location=(.27,.19,.15),target=(0,.018,-.09),lens=70,aspect=1),
 'mag_lips':dict(location=(.095,.083,.070),target=(0,0,0),lens=68,aspect=1.25),
 'cartridge':dict(location=(.060,-.065,.04),target=(0,.014,0),lens=70,aspect=1.4),
 'case':dict(location=(.038,-.060,.031),target=(0,.009,0),lens=70,aspect=1.25),
}
STRIP_SHOT=dict(location=(-.91,.64,.42),target=(0,.095,-.025),lens=43,aspect=1.25)
PHOTO_POSES={'right_photo':dict(raking=1),'locked_photo':dict(action='ReloadEmpty',frame=90)}
DEFAULT_SHOTS='right,left,side,top,front,raking_right,raking_left,receiver,lower,stock,handguard,sights,front_sight,handle,locked,locked_close,port_open,magazine,aimed,trigger,lower_raking_left,lower_raking_right'
RENDER_STAGE='form checkpoint / constant materials'
def floor_height(source):
 import bpy
 # Actual imported rest surfaces; the formed magazine floor must not clip
 # a fixed tabletop height. High-only sculpt helpers remain excluded.
 return min((o.matrix_world@v.co).z for o in bpy.context.scene.objects
  if o.type=='MESH' and not o.get('studio') and not o.get('bake_only')
  for v in o.data.vertices)-.0005
def configure_scene(scene,source):
 import bpy
 from mathutils import Vector
 for o in scene.objects:
  if o.name.startswith('HIGH_'):o.hide_render=True
  if o.type=='LIGHT':
   o.location.y+=.10;o.data.size_y*=2.2;o['baseline_energy']=o.data.energy
  if o.name.startswith('Studio black'):o.hide_render=True
 data=bpy.data.lights.new('Raking strip','AREA');data.shape='RECTANGLE';data.size=.025;data.size_y=.60;data.energy=16
 o=bpy.data.objects.new('Raking strip',data);scene.collection.objects.link(o);o.hide_render=True
 # A gray optical surround instead of the old black/transparent first-person view.
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.30

def prepare_shot(scene,shot):
 from mathutils import Vector
 if shot.get('action','').startswith('Fire') and 'time_s' in shot:
  x,y,z=shot['location'];shot['location']=(abs(x),y,z)
 scene.camera.data.dof.use_dof=bool(shot.get('aimed'))
 if shot.get('aimed'):
  scene.camera.data.dof.focus_distance=.4055;scene.camera.data.dof.aperture_fstop=85
 sign=shot.get('raking',0)
 for o in scene.objects:
  if o.type=='LIGHT' and 'baseline_energy' in o:o.data.energy=o['baseline_energy']*(.20 if sign else 1)
 strip=scene.objects['Raking strip'];strip.hide_render=not bool(sign)
 if sign:
  strip.location=(sign*.35,.10,.32)
  strip.rotation_euler=(Vector((0,.05,.08))-strip.location).to_track_quat('-Z','Y').to_euler()
