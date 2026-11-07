"""Fresh imported Type IV sections and full bearing footprint support.

The old center rays remain in check.py. These corner probes reject an edge
of a pad sticking out beyond a girder or a sole plate floating above concrete.
"""
import json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import import_file,bvh
import_file(Path('export/modules/PrestressedGirder24.gltf'));tree=bvh(bpy.context.scene.objects);sections=[]
for x in (-10,0,10):
 for z,nominal in ((.12,.6604),(.72,.2032),(1.30,.508)):
  a=tree.ray_cast(Vector((x,-1,z)),Vector((0,1,0)),2)[0];c=tree.ray_cast(Vector((x,1,z)),Vector((0,-1,0)),2)[0]
  assert a is not None and c is not None;(width:=c.y-a.y);assert abs(width-nominal)<.00002,(x,z,width)
  sections.append(dict(x_m=x,z_m=z,width_m=width))
import_file(Path('export/modules/Overpass.gltf'));allmeshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
girders=bvh([o for o in allmeshes if o.parent and o.parent.get('module_kind')=='bridge_girder']);rubber=bvh(allmeshes,{'Freeway_Form_Rubber'});steel=bvh(allmeshes,{'Freeway_Form_Steel'});concrete=bvh(allmeshes,{'Freeway_Form_Bridge'})
gaps=[];seatgaps=[]
for x in (-23.6,-.65,.65,23.6):
 for y in (-9.144,-6.096,-3.048,0,3.048,6.096,9.144):
  for dx in (-.32,0,.32):
   for dy in (-.27,.27):
    xx=x+dx;yy=y+dy;pad=rubber.ray_cast(Vector((xx,yy,6)),Vector((0,0,-1)),2)[0];assert pad is not None
    beam=girders.ray_cast(pad+Vector((0,0,.12)),Vector((0,0,-1)),.2)[0];assert beam is not None,('Overhanging pad',xx,yy)
    gaps.append(float(beam.z-pad.z))
    plate=steel.ray_cast(Vector((xx,yy,5.5684)),Vector((0,0,-1)),.06)[0];assert plate is not None
    seat=concrete.ray_cast(Vector((xx,yy,5.57)),Vector((0,0,-1)),.06)[0];assert seat is not None,('Unsupported plate',xx,yy)
    seatgaps.append(float(plate.z-seat.z))
assert max(abs(g) for g in gaps)<.002,gaps
assert max(abs(g) for g in seatgaps)<.00003,seatgaps
report=dict(girder_measured_sections=sections,bearing_footprint_probes=len(gaps),pad_top_to_girder_gap_m=dict(min=min(gaps),max=max(gaps)),steel_plate_to_concrete_pedestal_gap_m=dict(min=min(seatgaps),max=max(seatgaps)),scope='Actual imported flange/web sections and distributed bearing contact rays; camber allows under 2mm pad-top variation. Not load/strength testing.')
Path('build/bridge-audit.json').write_text(json.dumps(report,indent=2));print('BRIDGE AUDIT PASSED',report)
