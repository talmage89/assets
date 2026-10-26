"""Independent basin ground, wet-rim contact and actual water clearance checks."""
import sys,json,argparse,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy
from mathutils import Vector
from kit.motion import surface
from kit.assembly import distance
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
body=next(o for o in bpy.context.scene.objects if o.name.startswith('Thin molded'))
water=next(o for o in bpy.context.scene.objects if o.name.startswith('Water surface'))
bs=surface(body);ws=surface(water);errors=[]
water_min=min(v.z for v in ws['points']);water_max=max(v.z for v in ws['points'])
if max(abs(water_min-.140),abs(water_max-.140))>1e-5:errors.append('Fill plane is not 140 mm')
clear=[]
for v in ws['points']:
 r=math.hypot(v.x,v.y)
 if r<.5:continue
 direction=Vector((v.x,v.y,0)).normalized();hit=bs['tree'].ray_cast(v,direction,.04)
 if hit[0] is None:errors.append('Water edge has no surrounding wall')
 else:clear.append(hit[3])
if clear and min(clear)<.0005:errors.append('Water intersects molded wall')
floor=bs['tree'].ray_cast(Vector((0,0,water_min)),Vector((0,0,-1)),.20)
floor_gap=water_min-floor[0].z if floor[0] else None
if floor_gap is None or not .13<floor_gap<.14:errors.append('Water floor separation wrong')
clippings=[]
for ob in bpy.context.scene.objects:
 if not ob.name.startswith('Wet rim grass'):continue
 d,method=distance(ob,body);clippings.append(dict(name=ob.name,distance_m=d,method=method))
 if d>.0003:errors.append('Floating grass clipping '+ob.name)
minimum=min(v.z for v in bs['points']);ground=[v for v in bs['points'] if abs(v.z-minimum)<1e-6]
center=Vector(((min(v.x for v in ground)+max(v.x for v in ground))/2,(min(v.y for v in ground)+max(v.y for v in ground))/2,minimum))
origin_error=(center-bpy.data.objects['KiddiePool'].matrix_world.translation).length
if abs(minimum)>1e-6 or origin_error>1e-5:errors.append('Basin ground/origin mismatch')
# Body gauge is measured across the actual flute crest and valley at mid-height.
gauges=[]
for k in range(24):
 theta=k*math.tau/24;direction=Vector((math.cos(theta),math.sin(theta),0));start=direction*.72;start.z=.150
 outer=bs['tree'].ray_cast(start,-direction,.08)
 if outer[0] is None:errors.append('Missing outer wall');continue
 inner=bs['tree'].ray_cast(outer[0]-direction*.00001,-direction,.02)
 if inner[0] is None:errors.append('Missing inner wall');continue
 gauges.append((outer[0]-inner[0]).length)
if gauges and not .0014<min(gauges)<.0022:errors.append('Wall gauge inconsistent')
result=dict(passed=not errors,source=a.source,scope='Actual evaluated physical surfaces; GLB serialization is checked separately',measurements=dict(ground_z_m=minimum,footprint_origin_error_m=origin_error,water_height_min_m=water_min,water_height_max_m=water_max,water_edge_clearance_min_m=min(clear) if clear else None,water_edge_clearance_max_m=max(clear) if clear else None,edge_rays=len(clear),floor_gap_m=floor_gap,wall_gauge_min_m=min(gauges) if gauges else None,wall_gauge_max_m=max(gauges) if gauges else None,wall_rays=len(gauges),grass_contacts=clippings),errors=errors)
Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['passed'],'Construction failure'
