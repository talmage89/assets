"""Measure every tee/cup flight and lane/link butt joint on source surfaces.

Separate from export serialization: stair tread planes and riser intervals are
read from mesh coordinates. Endpoint probes measure authored neighboring meshes.
"""
import json
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def measure(course):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();rows=[]
 def tree(ob):
  mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg);mesh.calc_loop_triangles()
  out=BVHTree.FromPolygons([ob.matrix_world@v.co for v in mesh.vertices],[tuple(t.vertices) for t in mesh.loop_triangles],all_triangles=True);bpy.data.meshes.remove(mesh);return out
 walks=[o for o in course.children_recursive if o.type=='MESH' and o.get('walking_surface')]
 # Test tee/cup branch joints against the actual union of route top faces,
 # including cases where two retained lanes share a piece of paving.
 route_vertices=[];route_faces=[]
 for path in walks:
  if not path.get('walk_rows'):continue
  data=bpy.data.meshes.new_from_object(path.evaluated_get(dg),depsgraph=dg);data.calc_loop_triangles();offset=len(route_vertices)
  route_vertices.extend(path.matrix_world@v.co for v in data.vertices)
  route_faces.extend(tuple(offset+k for k in t.vertices) for t in data.loop_triangles if t.normal.z>.5);bpy.data.meshes.remove(data)
 routes=BVHTree.FromPolygons(route_vertices,route_faces,all_triangles=True)
 for ob in walks:
  if ob.get('stair_risers',0):
   planes=[]
   for face in ob.data.polygons:
    if face.index in list(ob.get('stair_top_faces',[])) if 'stair_top_faces' in ob else face.normal.z>.8:
     points=[ob.matrix_world@ob.data.vertices[k].co for k in face.vertices];spread=max(q.z for q in points)-min(q.z for q in points)
     assert spread<1e-5,('Wedge stair tread',ob.name,spread)
     planes.append(sum(q.z for q in points)/len(points))
   planes=sorted(set(round(z,6) for z in planes));intervals=[b-a for a,b in zip(planes,planes[1:])]
   assert not intervals or max(intervals)-min(intervals)<2e-5,('Uneven risers',ob.name,intervals)
   rows.append(dict(walk=ob.name,tread_heights_m=planes,between_tread_rises_m=intervals,tread_plane_tolerance_m=1e-5))
  for end in (0,1):
   peer=ob.get('join_peer_'+str(end))
   if not peer:continue
   target=bpy.data.objects[peer];surface=tree(target);n=ob['walk_rows'];indices=(0,1) if end==0 else (2*n-2,2*n-1)
   probes=ob.get('join_probe_'+str(end))
   points=[Vector(probes[i:i+3]) for i in (0,3)] if probes is not None else [ob.data.vertices[k].co for k in indices]
   # Trimming may transfer a corner to another path; test the actual
   # shared walking surface across the join, rather than an old private edge.
   a,b=[ob.matrix_world@q for q in points];normal=Vector((-(b-a).y,(b-a).x,0)).normalized();gaps=[]
   for i in range(9):
    q=a.lerp(b,(i+.5)/9);hit=routes.ray_cast(Vector((q.x,q.y,20)),Vector((0,0,-1)),30)
    if hit[0] is None:
     # A ray exactly on a shared float32 edge can miss both triangles.
     for dx,dy in ((.00005,0),(-.00005,0),(0,.00005),(0,-.00005)):
      hit=routes.ray_cast(Vector((q.x+dx,q.y+dy,20)),Vector((0,0,-1)),30)
      if hit[0] is not None:break
    if hit[0] is None:
     hit=routes.find_nearest(q)
     assert hit[0] is not None and hit[3]<.002,('Missing joint walking surface',ob.name,list(q),hit[3])
    origin,plane_normal=hit[:2]
    for offset in (-.001,0,.001):
     point=q+normal*offset;point.z=origin.z-(plane_normal.x*(point.x-origin.x)+plane_normal.y*(point.y-origin.y))/plane_normal.z
     gaps.append(routes.find_nearest(point)[3])
   assert max(gaps)<.002,('Walk union has a gap/height break',ob.name,peer,max(gaps))
   rows.append(dict(walk=ob.name,end=end,neighbor=peer,actual_joint_union_max_gap_m=max(gaps),probes=len(gaps),scope='Nine samples through the central 89% of the butt line, each at -1/0/+1mm across it. Actual triangle planes and the combined walking surface, not serialization. Outline corners may be reassigned by trimming.'))
 for landing in walks:
  if landing.get('junction_start') is None:continue
  q=landing.data.vertices[0].co;r=landing.data.vertices[1].co;gaps=[]
  for endpoint in (q,r):
   choices=[v.co for v in landing.data.vertices if (v.co.xy-endpoint.xy).length<1e-5]
   gaps.append(min(routes.find_nearest(landing.matrix_world@point)[3] for point in choices))
  assert max(gaps)<.002,('Tee/cup landing no longer meets paving',landing.name,gaps)
  overlap_samples=0
  for face in landing.data.polygons:
   if face.normal.z<.5:continue
   q=landing.matrix_world@face.center;hit=routes.ray_cast(Vector((q.x,q.y,20)),Vector((0,0,-1)),30)
   if hit[0] is not None:
    overlap_samples+=1
    assert abs(q.z-hit[0].z)<.002,('Landing overlays another walk at a different height',landing.name,list(q),list(hit[0]))
  rows.append(dict(landing=landing.name,actual_front_edge_to_route_top_max_gap_m=max(gaps),landing_centers_over_existing_paving=overlap_samples))
 for support in course.children_recursive:
  if support.type!='MESH' or not support.get('landing_owner'):continue
  landing=bpy.data.objects[support['landing_owner']];surface=tree(landing);points=[support.matrix_world@((support.data.vertices[a].co+support.data.vertices[b].co)/2) for a,b in ((2,3),(6,7))];gaps=[surface.find_nearest(q)[3] for q in points]
  assert max(gaps)<1e-5,('Timber does not seat below landing',support.name,gaps)
  rows.append(dict(support=support.name,landing=landing.name,actual_contact_line_max_gap_m=max(gaps),samples=len(gaps)))
 quarry=[o for o in walks if o.name.startswith('Quarry stair tread')]
 if quarry:
  heights=[]
  for ob in quarry:
   mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg)
   heights.append(max((ob.matrix_world@v.co).z for v in mesh.vertices));bpy.data.meshes.remove(mesh)
  heights.sort();rises=[b-a for a,b in zip(heights,heights[1:])]
  assert max(rises)-min(rises)<1e-5,('Uneven quarry flight',rises)
  rows.append(dict(flight='Quarry stair',actual_tread_heights_m=heights,actual_between_tread_rises_m=rises))
 return dict(walking_meshes=len(walks),measurements=rows,scope=__doc__)
