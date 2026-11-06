"""Use existing source generators with a complete temporary form palette.

The car form entry points omit later detail roles; the full Build constructor
provides them. This adapter never edits any car script or delivery.
"""
import argparse,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--kind');p.add_argument('--out');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
sys.path[:0]=[str(ROOT/'cars/src'),str(ROOT)]
from build import Build
import wheels
bpy.ops.wm.read_factory_settings(use_empty=True);b=Build(False,detail=False)
for key,col in {'frame':(.025,.028,.027),'steel':(.19,.20,.18),'chrome':(.45,.46,.44),'lamp':(.40,.42,.40),'red':(.34,.018,.012),'amber':(.42,.18,.013),'black':(.015,.018,.017),'interior':(.065,.060,.050),'paint':(.22,.28,.25)}.items():
 m=bpy.data.materials.new('Context '+key);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.48;b.m[key]=m
for key in ('plastic','dark_chrome','badge','drl','grille','headlight','brake','caliper','cloth','seat_side','headliner','interior_light','rear_glass','side_glass','privacy','mirror','red_lens','tire_L','tire_R'):
 b.m[key]=b.m['glass'] if 'glass' in key or key=='privacy' else b.m['rubber'] if key.startswith('tire') else b.m['chrome'] if key in ('mirror','badge') else b.m['frame']
if a.kind=='pickup':
 import pickup_spec as S,body as body_module
elif a.kind=='crossover':
 import suv_spec as S,suv_body as body_module
else:
 import hatch_spec as S,hatch_body as body_module
b.root.name=getattr(S,'NAME',{'pickup':'AlderC150','crossover':'AlderX220','hatchback':'AlderH120'}[a.kind])
b.asset_set=getattr(S,'ASSET_SET',b.asset_set)
# The original vehicle source shaders need rest coordinates but no downloaded
# image, private car delivery or changes to any car-family file.
from kit import vehicle_materials as V
axles=(S.FRONT_AXLE,S.REAR_AXLE)
col={'pickup':(.055,.12,.16),'crossover':(.20,.22,.19),'hatchback':(.27,.055,.025)}[a.kind]
b.m['body']=V.paint('Context original '+a.kind+' paint',col,.30,axles,front=-S.LENGTH/2,rear=S.LENGTH/2,refined=True)
for key,c,kind in [('wheel',(.45,.47,.47),'alloy'),('chrome',(.55,.57,.57),'chrome'),('rubber',(.012,.013,.014),'rubber'),('bumper',(.018,.02,.021),'plastic')]:
 b.m[key]=V.manufactured('Context '+a.kind+' '+key,c,kind,.25,axles,refined=True)
b.m['glass']=V.glazing('Context '+a.kind+' windshield',(.18,.25,.26))
for key in ('rear_glass','side_glass','privacy'):b.m[key]=b.m['glass']
for key in ('tire_L','tire_R'):b.m[key]=b.m['rubber']
b.detail=True
body_module.build(b)
wheels.build(b,S)
# Original exterior construction supplies actual optics, grilles and mirrors
# for parked foreground cars. Blank plate/dealer surfaces carry no real marks.
from collections import defaultdict
b.m['lens']=V.glazing('Context clear lamp lens',(.96,.98,.98))
b.m['red_lens']=V.lamp('Context red lens',(.30,.008,.005),0,.25)
b.m['rear_cover']=b.m['red_lens'];b.m['brakelight']=V.lamp('Context rear phosphor',(.35,.008,.004),0)
b.m['drl']=V.lamp('Context white signature',(.82,.84,.80),0);b.m['headlight']=b.m['drl']
b.m['dark_chrome']=V.manufactured('Context satin dark metal',(.12,.14,.15),'chrome',.20,axles,refined=True)
b.m['gloss_black']=b.m['frame'];b.m['grille']=b.m['frame'];b.m['grille_bar']=b.m['dark_chrome']
b.m['plate']=V.manufactured('Context blank plate',(.63,.64,.61),'plastic',0,axles);b.m['dealer']=b.m['plate']
b.m=defaultdict(lambda:b.m['frame'],b.m)
if a.kind=='pickup':import exterior as exterior_module
elif a.kind=='crossover':import suv_exterior as exterior_module
else:import hatch_exterior as exterior_module
exterior_module.build(b)
# Flat, cheap checkpoint materials preserve distinct glass/tires/paint.
for m in list(bpy.data.materials):
 if not m.users:continue
 if not m.use_nodes:continue
 p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if p:
  # Procedural source materials can remain; no bake or export is requested.
  p.inputs['Emission Strength'].default_value=0
bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
