"""Measure roof/house clearance to the actual exported curved ROW fence."""
import json,math,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import import_file,vertices,meshes
from plan import plan

p=plan(202)
def lateral(v):return p.radius-math.hypot(p.radius-v.x,v.y)
import_file('export/Freeway-202.gltf')
fence=next(o for o in bpy.context.scene.objects if o.name=='RightOfWayFence')
fence_outer=max(abs(lateral(v)) for v in vertices(meshes(fence)))
import_file('export/Town-202.gltf')
houses=[o for o in bpy.context.scene.objects if str(o.get('placement_id','')).startswith('House_')]
gaps=[]
for house in houses:
    points=vertices(meshes(house));assert points,house.name
    gap=min(abs(lateral(v)) for v in points)-fence_outer
    assert gap>.5,('House enters ROW fence envelope',house.name,gap)
    gaps.append(dict(house=house.name,minimum_lateral_envelope_gap_m=gap))
report=dict(houses=len(houses),measured_fence_outer_lateral_m=fence_outer,
            minimum_house_envelope_clearance_m=min(r['minimum_lateral_envelope_gap_m'] for r in gaps),
            houses_checked=gaps,
            scope='Actual imported roof/wall envelope vertices against actual curved fence radial envelope; conservative lateral test, not parcel title or swept foliage clearance.')
Path('build/context-audit.json').write_text(json.dumps(report,indent=2));print('CONTEXT AUDIT PASSED',report['houses'],report['minimum_house_envelope_clearance_m'])
