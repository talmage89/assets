"""PD C9 viewpoints and poses. No family renderer contains pistol dimensions."""
import math
CENTER=(0,.043,.008)
SHOTS={
'case':dict(location=(.032,-.028,.024),target=(0,.008,0),lens=65,aspect=1.35),
'mag_standalone':dict(location=(.14,.10,.04),target=(0,-.014,-.041),lens=70,aspect=1.1),
'right':dict(location=(.32,.32,.16),target=CENTER,lens=66,aspect=1.35),
'left':dict(location=(-.32,.29,.15),target=CENTER,lens=66,aspect=1.35),
'aimed':dict(location=(0,0,0),target=(0,1,0),lens=45,aspect=1.6,aimed=True),
'grip_guard':dict(location=(-.16,.085,.035),target=(0,.018,.003),lens=70,aspect=1.35),
'open_right':dict(location=(.49,.16,.14),target=(0,.025,.010),lens=72,aspect=1.5,action='IdleOpen',frame=0),
'partial':dict(location=(.28,.23,.15),target=(0,.04,.04),lens=80,aspect=1.4,action='Charge',frame=20),
'returning':dict(location=(.28,.23,.15),target=(0,.04,.04),lens=80,aspect=1.4,action='ReloadEmpty',frame=115),
'hero':dict(location=(.32,.32,.21),target=CENTER,lens=66,aspect=1.35),
'side':dict(location=(-.5,.043,.008),target=CENTER,ortho=.224,aspect=1.5),
'top':dict(location=(0,.043,.6),target=(0,.043,0),ortho=.224,aspect=1.5,roll=math.pi/2),
'front':dict(location=(0,.65,.008),target=CENTER,ortho=.165,aspect=1),
'locked':dict(location=(.28,.29,.19),target=(0,.025,.012),lens=64,aspect=1.35,action='FireLast',frame=15),
'rear':dict(location=(.16,-.25,.17),target=(0,-.008,.038),lens=75,aspect=1.35),
'magazine':dict(location=(.31,.25,.17),target=(0,.012,-.027),lens=59,aspect=1.25,action='Reload',frame=28),
}
for name,clip,frame in [('pose_idle','Idle',0),('pose_fire','Fire',5),('pose_last','FireLast',15),
   ('pose_reload','Reload',28),('pose_empty','ReloadEmpty',73),('pose_release','ReloadEmpty',113),
   ('pose_inspect','Inspect',42),('pose_charge','Charge',25)]:
 SHOTS[name]=dict(location=(.34,.25,.18),target=(0,.01,-.025),lens=57,aspect=1.3,action=clip,frame=frame)

def floor_height(source):
 return -.00305 if source.stem=="case" else (-.0946 if source.stem.startswith("magazine") else -.0541)

STRIP_SHOT=dict(location=(.37,.21,.12),target=(0,.008,-.045),lens=54,aspect=1.25)

PHOTO_POSES={'open_photo':dict(action='IdleOpen',frame=0)}
DEFAULT_SHOTS='hero,side,top,front,locked,rear,magazine'

SHOTS.update({
 'rake_right':dict(location=(.34,.26,.13),target=(0,.04,.012),lens=68,aspect=1.4,raking=1),
 'rake_left':dict(location=(-.32,-.23,.13),target=(0,.035,.008),lens=68,aspect=1.4,raking=-1),
 'mag_rear':dict(location=(.12,-.18,.035),target=(0,-.014,-.041),lens=70,aspect=1.1),
})

def configure_scene(scene,source):
 import bpy
 for ob in scene.objects:
  if ob.type=='LIGHT':ob['baseline_energy']=ob.data.energy
 data=bpy.data.lights.new('Mold inspection strip','AREA');data.shape='RECTANGLE'
 data.size=.018;data.size_y=.28;data.energy=5
 strip=bpy.data.objects.new('Mold inspection strip',data);scene.collection.objects.link(strip)
 strip.hide_render=True

def prepare_shot(scene,shot):
 from mathutils import Vector
 sign=shot.get('raking',0)
 for ob in scene.objects:
  if ob.type=='LIGHT' and 'baseline_energy' in ob:ob.data.energy=ob['baseline_energy']*(.12 if sign else 1)
 strip=scene.objects['Mold inspection strip'];strip.hide_render=not bool(sign)
 if sign:
  strip.location=(sign*.20,-.08,.16)
  strip.rotation_euler=(Vector((0,.045,.018))-strip.location).to_track_quat('-Z','Y').to_euler()
