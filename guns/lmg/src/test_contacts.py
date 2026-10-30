"""Touching coplanar-land regression, plus a lifted negative case."""
import sys,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as M
from check import surface_gap
bpy.ops.wm.read_factory_settings(use_empty=True)
mat=bpy.data.materials.new('Contact regression')
a=M.box('Inner footprint',(0,0,0),(.032,.048,.008),mat,0)
b=M.box('Outer footprint',(0,0,.006),(.040,.040,.004),mat,0)
bpy.context.view_layer.update();near=surface_gap(a,b)
b.location.z+=.001;bpy.context.view_layer.update();far=surface_gap(a,b)
assert near[0]<1e-6 and far[0]>.0009,(near,far)
result=dict(touching_land_gap_m=near,lifted_land_gap_m=far,passed=True)
out=Path(__file__).resolve().parents[1]/'build/contact-negative.json'
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2))
print('CONTACT REGRESSION',result)
