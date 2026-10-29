"""Asset-owned inspection cameras, including the exact optical socket."""
import math
C=(0,.150,.015)
SHOTS={
 'right':dict(location=(1.45,.64,.48),target=C,lens=60,aspect=2.0),
 'left':dict(location=(-1.45,.64,.48),target=C,lens=60,aspect=2.0),
 'side':dict(location=(1.5,.155,.008),target=(0,.155,.008),ortho=.97,aspect=2.8),
 'top':dict(location=(0,.155,1.5),target=(0,.155,0),ortho=.97,aspect=3.0,roll=math.pi/2),
 'front':dict(location=(0,1.5,.010),target=(0,.155,.010),ortho=.33,aspect=1),
 'raking_right':dict(location=(1.15,-.39,.42),target=(0,.14,.03),lens=48,aspect=2,raking=1),
 'raking_left':dict(location=(-1.15,-.39,.42),target=(0,.14,.03),lens=48,aspect=2,raking=-1),
 'receiver':dict(location=(.45,.40,.27),target=(0,.08,.075),lens=65,aspect=1.6),
 'cover_rear':dict(location=(.16,-.22,.26),target=(0,.065,.10),lens=65,aspect=1.6),
 'controls':dict(location=(.30,.26,.15),target=(.015,.055,.053),lens=75,aspect=1.6),
 'trigger':dict(location=(.18,.09,.07),target=(0,.033,.025),lens=95,aspect=1.2),
 'trigger_side':dict(location=(.25,.032,.026),target=(0,.032,.026),lens=115,aspect=1.2),
 'wood':dict(location=(-.30,.32,.26),target=(0,.29,.075),lens=85,aspect=1.6),
 'grip_stock':dict(location=(-.42,-.40,.23),target=(0,-.155,.025),lens=67,aspect=1.65),
 'grip_detail':dict(location=(.18,.09,.01),target=(0,-.008,.01),lens=95,aspect=1.1),
 'rear_sight':dict(location=(.12,.08,.23),target=(0,.208,.121),lens=80,aspect=1.4),
 'front_sight':dict(location=(.12,.70,.21),target=(0,.55,.115),lens=82,aspect=1.4),
 'front_sight_rear':dict(location=(-.12,.39,.17),target=(0,.552,.106),lens=95,aspect=1.2),
 'gas_muzzle':dict(location=(-.25,.77,.20),target=(0,.48,.092),lens=78,aspect=1.8),
 'open':dict(location=(.28,.30,.27),target=(0,.13,.078),lens=80,aspect=1.6,action='Charge',frame=32),
 'aimed':dict(location=(0,0,0),target=(0,1,0),lens=75,aspect=1.6,aimed=True),
 'magazine':dict(location=(.27,.35,.16),target=(0,.175,-.035),lens=72,aspect=1.3),
 'mag_standalone':dict(location=(.26,.18,.08),target=(0,.012,-.085),lens=48,aspect=1.1),
 'mag_lips':dict(location=(.10,.035,.10),target=(0,-.027,0),lens=85,aspect=1.2),
 'cartridge':dict(location=(.07,-.09,.05),target=(0,.027,0),lens=73,aspect=1.5),
 'case':dict(location=(.065,-.085,.04),target=(0,.020,0),lens=82,aspect=1.4),
 'case_mouth':dict(location=(.025,.08,.026),target=(0,.025,0),lens=95,aspect=1.4),
}
STRIP_SHOT=dict(location=(.95,.45,.30),target=(0,.17,-.045),lens=42,aspect=1.25)
for name,frame in [('selector_safe',0),('selector_auto',18),('selector_semi',36)]:
 SHOTS[name]=dict(SHOTS['controls'],action='Selector',frame=frame)
for name,frame in [('front_lug_seated',132),('front_lug_rock',120),('front_lug_hook',112)]:
 SHOTS[name]=dict(location=(-.10,.125,.035),target=(0,.166,.067),lens=100,aspect=1.3,
  action='Reload',frame=frame,diagnostic_isolate=['Magazine_FrontLug','Receiver_FrontLugSlot','Receiver_FrontLugBridge-1','Receiver_FrontLugBridge1'])
SHOTS['rear_catch_seated']=dict(location=(.10,.12,.015),target=(0,.095,.043),lens=100,aspect=1.3,
 diagnostic_isolate=['Magazine_RearCatch','MagRelease_VisualCatch','MagRelease_Paddle','Release_Housing'])
SHOTS['carrier_seated']=dict(location=(.12,.13,.15),target=(0,.185,.100),lens=100,aspect=1.3,
 diagnostic_isolate=['Carrier_SeatingFace','Front_InsertUpperShoulder','Carrier_Body'])
PHOTO_POSES={}
DEFAULT_SHOTS='right,left,side,top,front,raking_right,raking_left,receiver,cover_rear,controls,trigger,trigger_side,wood,grip_stock,grip_detail,rear_sight,front_sight,front_sight_rear,gas_muzzle,open,aimed,magazine'
RENDER_STAGE='form round 2 / geometric normal bake with constant inspection finish'
def floor_height(source):
 import bpy
 return min((o.matrix_world@v.co).z for o in bpy.context.scene.objects if o.type=='MESH' and not o.get('bake_only') and not o.get('studio') for v in o.data.vertices)-.001
def configure_scene(scene,source):
 import bpy
 for o in scene.objects:
  if o.name.startswith('HIGH_'):o.hide_render=True
  if o.type=='LIGHT':o['baseline_energy']=o.data.energy
  if o.name.startswith('Studio black'):o.hide_render=True
 data=bpy.data.lights.new('Raking strip','AREA');data.shape='RECTANGLE';data.size=.025;data.size_y=.8;data.energy=22
 ob=bpy.data.objects.new('Raking strip',data);scene.collection.objects.link(ob);ob.hide_render=True
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.25,.25,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
def prepare_shot(scene,shot):
 from mathutils import Vector
 for ob in scene.objects:
  if ob.type=='MESH' and ob.get('asset_set'):
   ob.hide_render=bool(ob.get('bake_only')) or bool(shot.get('diagnostic_isolate') and ob.get('part_name',ob.name) not in shot['diagnostic_isolate'])
 for ob in scene.objects:
  if ob.type=='LIGHT' and 'baseline_energy' in ob:ob.data.energy=ob['baseline_energy']*(.22 if shot.get('raking') else 1)
 strip=scene.objects['Raking strip'];sign=shot.get('raking',0);strip.hide_render=not bool(sign)
 if sign:
  strip.location=(sign*.4,.1,.38);strip.rotation_euler=(Vector((0,.08,.08))-strip.location).to_track_quat('-Z','Y').to_euler()
 scene.camera.data.dof.use_dof=False
