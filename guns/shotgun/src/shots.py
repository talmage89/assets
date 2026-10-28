"""Shotgun-specific cameras; kit and family presentation stay unchanged."""
import math
from pathlib import Path
C=(0,.25,.0)
SHOTS={
 'right':dict(location=(1.52,.72,.53),target=C,lens=57,aspect=2.15),
 'left':dict(location=(-1.52,.69,.49),target=C,lens=57,aspect=2.15),
 'raking_right':dict(location=(.95,1.2,.44),target=(0,.25,.015),lens=55,aspect=1.9),
 'raking_left':dict(location=(-.95,1.2,.44),target=(0,.25,.015),lens=55,aspect=1.9),
 'receiver':dict(location=(.48,.33,.22),target=(0,.135,.048),lens=68,aspect=1.5),
 'guard':dict(location=(.22,.15,-.075),target=(0,.085,-.012),lens=78,aspect=1.5),
 'open':dict(location=(.40,.23,.16),target=(0,.167,.052),lens=80,aspect=1.5,action='Fire',frame=40),
 'underside':dict(location=(.24,.20,-.40),target=(0,.13,.015),lens=65,aspect=1.5,action='Reload',frame=28),
 'aimed':dict(location=(0,0,0),target=(0,1,0),aimed=True,lens=55,aspect=1.6),
 'muzzle':dict(location=(.10,.88,.12),target=(0,.696,.054),lens=75,aspect=1.3),
 'stock':dict(location=(-.32,-.55,.22),target=(0,-.11,-.01),lens=68,aspect=1.6),
 'forend':dict(location=(.42,.72,.18),target=(0,.46,.026),lens=75,aspect=1.6),
 'side':dict(location=(1.8,.217,-.006),target=(0,.217,-.006),ortho=1.07,aspect=3.3),
 'top':dict(location=(0,.217,1.5),target=(0,.217,0),ortho=1.07,aspect=3.3,roll=math.pi/2),
 'front':dict(location=(0,2,.0),target=(0,.217,.0),ortho=.24,aspect=1),
 'shell':dict(location=(.085,-.070,.065),target=(0,.027,0),lens=65,aspect=1.25),
 'shell_crimp':dict(location=(.040,.130,.045),target=(0,.047,0),lens=70,aspect=1.25),
 'hull':dict(location=(.085,.15,.080),target=(0,.035,0),lens=65,aspect=1.25),
 'hull_primer':dict(location=(.04,-.075,.035),target=(0,.020,0),lens=70,aspect=1.25),
}
STRIP_SHOT=dict(location=(.57,.43,.23),target=(0,.20,.02),lens=43,aspect=1.25)
PHOTO_POSES={'open_photo':dict(action='IdleOpen',frame=0)}
DEFAULT_SHOTS='right,left,receiver,open,underside,aimed,muzzle,stock,forend'
def floor_height(source):return -.012 if source.stem in ('shell','hull') else -.106
def configure_scene(sc,source):
 import bpy
 from mathutils import Vector
 # Long horizontal reflection cards, sized for the full long gun.
 for ob in sc.objects:
  if ob.type=='LIGHT':
   ob.data.energy*=1.2
   ob.location.y+=.18
   ob.data.size_y*=3.5
  if ob.name.startswith('HIGH_'):ob.hide_render=True
 d=bpy.data.lights.new('Inspection bounce','AREA');d.energy=8;d.shape='DISK';d.size=.25
 o=bpy.data.objects.new('Inspection bounce',d);sc.collection.objects.link(o);o.location=(.2,.15,-.22)
 o.rotation_euler=(Vector((0,.15,.01))-o.location).to_track_quat('-Z','Y').to_euler()
def prepare_shot(sc,shot):
 import bpy
 for ob in sc.objects:
  if ob.type=='MESH' and ob.get('asset_set')=='Shotgun':
   ob.hide_render=ob.get('bake_only',False)
for name,s in SHOTS.items():
 s['background']='transparent'
 if name not in ('shell','shell_crimp','hull','hull_primer'):
  for key in ('location','target'):
   x,y,z=s[key];s[key]=(x,y+.005,z-.016)
for key in ('location','target'):
 x,y,z=STRIP_SHOT[key];STRIP_SHOT[key]=(x,y+.005,z-.016)
