"""Actual imported house envelopes, narrow parcels and reused town instances."""
import json,math,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import import_file,vertices,meshes
from plan import plan
from mathutils import Vector
from mathutils.kdtree import KDTree
result={}
for seed in (101,202):
 p=plan(seed)
 def lateral(v):return p.radius-math.hypot(p.radius-v.x,v.y) if p.radius else v.x
 def station(v):return math.atan2(v.y,p.radius-v.x)*p.radius if p.radius else v.y
 import_file(f'export/Freeway-{seed}.gltf')
 fence=next(o for o in bpy.context.scene.objects if o.name=='RightOfWayFence')
 fence_vertices=vertices(meshes(fence));fence_outer=max(abs(lateral(v)) for v in fence_vertices)
 arterial_clearance=None
 if seed==101:
  arterial_clearance=min(abs(v.y) for v in fence_vertices)-10.668
  assert arterial_clearance>.25,('ROW fence blocks arterial or sidewalk',arterial_clearance)
 import_file(f'export/Town-{seed}.gltf')
 terrain=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Neighborhood streets driveways alleys and parcels'))
 yard_points=vertices([terrain]);tree=KDTree(len(yard_points))
 for i,v in enumerate(yard_points):tree.insert(v,i)
 tree.balance()
 metadata=json.loads(Path(f'build/scene-{seed}.json').read_text())['context']['placements']
 lots={r['name']:r for r in metadata if r['kind']=='house'};gaps=[];margins=[];frontages=[];depths=[]
 for name,row in lots.items():
  house=bpy.data.objects[name];points=vertices(meshes(house));assert points,name
  gap=min(abs(lateral(v)) for v in points)-fence_outer
  assert gap>.5,('House enters ROW fence envelope',name,gap)
  us=[lateral(v) for v in points];ss=[station(v) for v in points]
  u0,u1=row['parcel_us'];s0,s1=row['parcel_stations']
  margin=min(min(us)-u0,u1-max(us),min(ss)-s0,s1-max(ss))
  # A clipped irregular native roof has its own overhang. These tests compare
  # actual imported surfaces, not just an origin within a nominal lot.
  assert margin>-.20,('House outside reserved lot',name,margin,row)
  corners={}
  for u in (u0,u1):
   for s in (s0,s1):
    target=Vector(p.xyz(s,u));target.z=(7 if seed==101 else 0)+.004
    hit,index,distance=tree.find(target);assert distance<.001,(name,'Missing actual parcel corner',distance)
    corners[u,s]=hit
  front=u1 if row['yaw']>0 else u0
  actual_frontage=(corners[front,s1]-corners[front,s0]).length
  actual_depth=((corners[u1,s0]-corners[u0,s0]).length+(corners[u1,s1]-corners[u0,s1]).length)/2
  assert abs(actual_frontage-row['frontage_m'])<.005,(name,actual_frontage,row['frontage_m'])
  assert abs(actual_depth-row['depth_m'])<.001,(name,actual_depth)
  gaps.append(gap);margins.append(margin);frontages.append(actual_frontage);depths.append(actual_depth)
 assert min(frontages)>=50*.3048-.12 and max(frontages)<=60*.3048+.12,(seed,min(frontages),max(frontages))
 doc=json.loads(Path(f'export/Town-{seed}.gltf').read_text())
 refs=[n['mesh'] for n in doc['nodes'] if 'mesh' in n]
 trees=sum(r['kind']=='tree' for r in metadata)
 result[str(seed)]=dict(houses=len(lots),trees=trees,apartments=sum(r['kind']=='apartment' for r in metadata),measured_fence_outer_lateral_m=fence_outer,measured_fence_to_arterial_edge_clearance_m=arterial_clearance,minimum_house_envelope_clearance_m=min(gaps),minimum_house_to_parcel_margin_m=min(margins),measured_frontage_m_range=[min(frontages),max(frontages)],measured_depth_m_range=[min(depths),max(depths)],mesh_instances=len(refs),unique_meshes=len(set(refs)),scope='Actual imported roof/wall envelopes against actual fence and reserved lots. Frontages and depths are measured between actual exported parcel corners, associated by lot metadata; offset-curve station scale is compensated. No cadastral, foliage sweep or architectural certification.')
Path('build/context-audit.json').write_text(json.dumps(result,indent=2));print('CONTEXT AUDIT PASSED',result)
