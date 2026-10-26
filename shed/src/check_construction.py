"""Measure built surfaces independently of GLB serialization."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
def vertices(prefix):
 return [o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix) for v in o.data.vertices]
def bounds(prefix):
 vs=vertices(prefix);assert vs,prefix
 return ([min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)])
flo,fhi=bounds('Floor plywood sheet');rlo,rhi=bounds('PT rim joist');hlo,hhi=bounds('Double 2x6 door header')
jack=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Door jack stud')]
left=max(v.x for o in jack for v in [o.matrix_world@v.co for v in o.data.vertices] if v.x<0)
right=min(v.x for o in jack for v in [o.matrix_world@v.co for v in o.data.vertices] if v.x>0)
roof=vertices('Roof plywood sheathing 1');ridge=min(v.z for v in roof if abs(v.x)<1e-5);eave=min(v.z for v in roof);span=max(v.x for v in roof)
values=dict(floor_width_m=fhi[0]-flo[0],floor_depth_m=rhi[1]-rlo[1],deck_sheet_depth_m=fhi[1]-flo[1],deck_height_m=fhi[2],door_clear_width_m=right-left,door_clear_height_m=hlo[2]-fhi[2],structural_ridge_m=ridge,roof_pitch=(ridge-eave)/span)
expected=dict(floor_width_m=2.4384,floor_depth_m=3.048,deck_sheet_depth_m=3.047,deck_height_m=.24765,door_clear_width_m=1.524,door_clear_height_m=1.9805,structural_ridge_m=2.99085,roof_pitch=.5)
errors=[k for k,v in values.items() if abs(v-expected[k])>1e-5]
report=dict(passed=not errors,measurements=values,method='world-space vertices of finalized game surfaces',errors=errors)
Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report))
assert not errors,errors
