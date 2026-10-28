"""Checkpoint cameras; all normal gun views show an explicit evaluated pose."""
import math
C=(0,.058,.012)
SHOTS={
 'hero':dict(location=(.36,.38,.24),target=C,lens=66,aspect=1.4),
 'side':dict(location=(.5,.062,.014),target=(0,.062,.014),ortho=.275,aspect=1.7),
 'left':dict(location=(-.5,.062,.014),target=(0,.062,.014),ortho=.275,aspect=1.7),
 'top':dict(location=(0,.062,.6),target=(0,.062,0),ortho=.275,aspect=1.8,roll=math.pi/2),
 'front':dict(location=(0,.60,.014),target=(0,.06,.014),ortho=.17,aspect=1.0),
 'rake_right':dict(location=(.38,-.29,.22),target=C,lens=66,aspect=1.4,raking=1),
 'rake_left':dict(location=(-.38,.35,.22),target=C,lens=66,aspect=1.4,raking=-1),
 'open':dict(location=(-.24,-.22,.16),target=(-.014,.06,.035),lens=68,aspect=1.4,action='Reload',frame=88),
 'star':dict(location=(-.23,-.22,.14),target=(-.023,.045,.032),lens=80,aspect=1.4,action='Reload',frame=58),
 'reload':dict(location=(-.30,-.30,.18),target=(-.03,.015,.022),lens=62,aspect=1.4,action='Reload',frame=142),
 'rear':dict(location=(.13,-.20,.18),target=(0,.035,.060),lens=75,aspect=1.4),
 'trigger_side':dict(location=(.14,.036,.014),target=(0,.036,.014),lens=75,aspect=1.3),
 'trigger_quarter':dict(location=(.16,.15,.065),target=(0,.038,.012),lens=80,aspect=1.3),
 'grip':dict(location=(.22,-.19,.045),target=(0,-.018,-.012),lens=55,aspect=1.3),
 'sights':dict(location=(.065,-.18,.15),target=(0,.048,.072),lens=70,aspect=1.4),
 'grip_left':dict(location=(-.22,-.19,.045),target=(0,-.018,-.012),lens=55,aspect=1.3),
 'hammer_cocked':dict(location=(.10,-.09,.11),target=(0,.006,.066),lens=65,aspect=1.3,action='IdleCocked',frame=0),
 'recoil_shield':dict(location=(-.14,.19,.11),target=(0,.036,.057),lens=72,aspect=1.3,action='Reload',frame=88),
 'lug_front':dict(location=(-.13,.28,.09),target=(0,.15,.056),lens=74,aspect=1.3),
 'muzzle':dict(location=(.045,.285,.083),target=(0,.181,.060),lens=72,aspect=1.3),
 'rear_sight':dict(location=(-.075,-.060,.132),target=(0,.044,.080),lens=75,aspect=1.3),
 'latch':dict(location=(-.135,-.020,.090),target=(-.010,.023,.053),lens=78,aspect=1.3,action='Reload',frame=88),
 'grip_seam':dict(location=(-.10,-.12,.080),target=(0,-.018,.035),lens=74,aspect=1.3),
 'shank':dict(location=(.15,.17,.030),target=(0,.088,.029),lens=75,aspect=1.3),
 'hammer_rest':dict(location=(-.10,-.065,.105),target=(0,-.002,.067),lens=70,aspect=1.3),
 'hammer_top':dict(location=(.035,-.050,.16),target=(0,-.002,.064),lens=75,aspect=1.3,action='IdleCocked',frame=0),
 'aimed':dict(location=(0,0,0),target=(0,1,0),lens=50,aspect=1.6,aimed=True),
 'cartridge':dict(location=(.045,-.055,.03),target=(0,.019,0),lens=65,aspect=1.4),
 'case':dict(location=(.040,.070,.03),target=(0,.018,0),lens=68,aspect=1.4),
 'cartridge_head':dict(location=(.018,-.065,.012),target=(0,.001,0),lens=70,aspect=1.4),
 'case_head':dict(location=(.018,-.065,.012),target=(0,.001,0),lens=70,aspect=1.4),
 'speedloader':dict(location=(.085,-.10,.065),target=(0,.003,0),lens=70,aspect=1.4),
}
for s in SHOTS.values():s.setdefault('action','Idle');s.setdefault('frame',0)
for n in ('cartridge','case','cartridge_head','case_head','speedloader'):SHOTS[n].pop('action',None)
DEFAULT_SHOTS='hero,side,left,top,front,rake_right,rake_left,open,star,reload,rear,trigger_side,trigger_quarter,grip,grip_left,sights,hammer_cocked,recoil_shield,lug_front,muzzle,rear_sight,latch,grip_seam,shank,hammer_rest,hammer_top,aimed'
STRIP_SHOT=dict(location=(-.38,-.30,.22),target=(-.01,.04,.02),lens=62,aspect=1.25)
PHOTO_POSES={'right_photo':dict(action='Idle',frame=0),'left_photo':dict(action='Idle',frame=0),
 'open_photo':dict(action='Reload',frame=88)}
def floor_height(source):return -.07
def configure_scene(scene,source):
 import bpy
 for ob in scene.objects:
  if ob.type=='LIGHT':ob['baseline_energy']=ob.data.energy
 data=bpy.data.lights.new('Raking inspection strip','AREA');data.shape='RECTANGLE'
 data.size=.025;data.size_y=.30;data.energy=6
 ob=bpy.data.objects.new('Raking inspection strip',data);scene.collection.objects.link(ob);ob.hide_render=True
 # A camera-visible gray card for the exact Socket_Eye view, behind the muzzle.
 from kit import model as M
 m=bpy.data.materials.new('Aim gray backdrop');m.use_nodes=True
 nt=m.node_tree;nt.nodes.clear();e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(.24,.24,.24,1)
 o=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],o.inputs['Surface'])
 card=M.box('Aim backdrop',(0,.35,.08),(2,.003,1.5),m,0);M.apply(card);card.hide_render=True
 def before_render(sc):
  if sc.get('exact_aim'):
   sc.render.film_transparent=False;card.hide_render=False
 bpy.app.handlers.render_pre.append(before_render)
def prepare_shot(scene,shot):
 from mathutils import Vector
 sign=shot.get('raking',0)
 for ob in scene.objects:
  if ob.type=='LIGHT' and 'baseline_energy' in ob:ob.data.energy=ob['baseline_energy']*(.10 if sign else 1)
 strip=scene.objects['Raking inspection strip'];strip.hide_render=not bool(sign)
 if sign:
  strip.location=(sign*.18,-.04,.17)
  strip.rotation_euler=(Vector((0,.05,.02))-strip.location).to_track_quat('-Z','Y').to_euler()
 scene['exact_aim']=bool(shot.get('aimed'));scene.objects['Aim backdrop'].hide_render=not scene['exact_aim']
