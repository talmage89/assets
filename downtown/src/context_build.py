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
 import pickup_spec as S,body
 body.build(b)
elif a.kind=='crossover':
 import suv_spec as S,suv_body
 suv_body.build(b)
else:
 import hatch_spec as S,hatch_body
 hatch_body.build(b)
wheels.build(b,S)
# Flat, cheap checkpoint materials preserve distinct glass/tires/paint.
for m in list(bpy.data.materials):
 if not m.users:continue
 if not m.use_nodes:continue
 p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if p:
  # Procedural source materials can remain; no bake or export is requested.
  p.inputs['Emission Strength'].default_value=0
bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
