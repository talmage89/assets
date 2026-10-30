"""Checkpoint cameras in the family +Y-forward frame."""
from pathlib import Path
SHOTS={
 'hero':dict(location=(-1.30,1.05,.68),target=(0,.15,.045),lens=50,aspect=1.85),
 'raking_right':dict(location=(1.05,.86,.40),target=(0,.17,.07),lens=60,aspect=1.85),
 'side':dict(location=(2,.19,.085),target=(0,.19,.085),ortho=1.18,aspect=2.7),
 'left':dict(location=(-2,.19,.085),target=(0,.19,.085),ortho=1.18,aspect=2.7),
 'top':dict(location=(0,.19,2),target=(0,.19,.06),ortho=1.18,aspect=2.7,roll=1.5707963267948966),
 'front':dict(location=(0,2,.08),target=(0,.13,.08),ortho=.39,aspect=1.15),
 'cover_open':dict(location=(-.38,.025,.50),target=(-.012,.13,.16),lens=55,action='Reload',frame=64,aspect=1.35),
 'rear_sight':dict(location=(.18,-.23,.29),target=(0,-.012,.157),lens=75,aspect=1.35),
 'barrel_handle':dict(location=(-.36,.52,.32),target=(.015,.295,.133),lens=65,aspect=1.6),
 'front_sight':dict(location=(.19,.68,.24),target=(0,.535,.139),lens=75,aspect=1.35),
 'charging_handle':dict(location=(.39,.06,.24),target=(.023,.14,.087),lens=70,aspect=1.6),
 'trigger':dict(location=(.30,.038,.027),target=(0,.038,.027),lens=100,aspect=1.35),
 'lower_raking':dict(location=(-.25,.17,.05),target=(0,.018,-.003),lens=65,aspect=1.35),
 'furniture':dict(location=(.48,-.46,.28),target=(0,-.15,.05),lens=65,aspect=1.5),
 'handguard':dict(location=(-.25,.51,.13),target=(0,.36,.075),lens=60,aspect=1.5),
 'bipod':dict(location=(-.60,.80,.06),target=(0,.47,-.14),ortho=.60,action='BipodDeploy',frame=84,aspect=1.2),
 'belt':dict(location=(-.32,-.03,.24),target=(-.055,.17,.05),lens=65,aspect=1.25),
 'box':dict(location=(-.32,.38,.04),target=(0,.164,-.065),lens=70,aspect=1.25),
 'aimed':dict(location=(0,-.0975,.176),target=(0,1,.176),lens=20,aspect=1.65,aimed=True,action='Idle',frame=0),
}
DEFAULT_SHOTS=','.join(SHOTS)
PHOTO_POSES={'right_photo':dict(action='BipodDeploy',frame=84),'left_photo':dict(action='BipodDeploy',frame=84),'open_photo':dict(action='Reload',frame=64),'trigger_photo':dict(action='Idle',frame=0),'belt_photo':dict(action='BipodDeploy',frame=84)}
STRIP_SHOT=dict(location=(-.95,.70,.49),target=(0,.14,.01),lens=56,aspect=1.4)
RENDER_STAGE='unbaked form checkpoint / exported GLB'
def floor_height(source):return -.50
# Every posed view must request Idle: the rest rig stores all reusable belt
# templates at one common origin and its complete Idle pose lays them out.
for shot in SHOTS.values():shot.setdefault('action','Idle');shot.setdefault('frame',0)

def configure_scene(scene,source):
 import bpy
 for ob in scene.objects:
  if ob.name.startswith(('Studio seamless','Studio black')):ob.hide_render=True
 # Camera-only gray background keeps aimed evidence opaque without changing
 # reflection/illumination from the procedural studio environment.
 nt=scene.world.node_tree;old=nt.nodes['Background'];out=nt.nodes['World Output']
 cam=nt.nodes.new('ShaderNodeBackground');cam.inputs['Color'].default_value=(.23,.23,.23,1);cam.inputs['Strength'].default_value=1
 path=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader')
 nt.links.new(path.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(old.outputs[0],mix.inputs[1]);nt.links.new(cam.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
 def opaque(sc):
  sc.render.film_transparent=False;bpy.data.objects['Studio seamless'].hide_render=True
 bpy.app.handlers.render_pre.append(opaque)
SHOTS.update({
 'cartridge':dict(location=(.085,-.09,.055),target=(0,.026,0),lens=75,aspect=1.35),
 'case':dict(location=(.065,.09,.045),target=(0,.026,0),lens=75,aspect=1.35),
 'link':dict(location=(.05,-.065,.04),target=(-.005,.017,0),lens=80,aspect=1.35),
 'box_loaded':dict(location=(-.33,.33,.18),target=(0,0,-.07),lens=70,aspect=1.25),
 'box_empty':dict(location=(-.33,.33,.18),target=(0,0,-.07),lens=70,aspect=1.25),
})
