"""Independent round-two measurements: mirrors, rear features and hidden backs."""
import argparse,json,hashlib,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from hatch_check import bounds,points,mesh_tree
from hatch_fairness import field

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--diagnostic',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update()
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Hatch']
 skins=[o for o in obs if o.get('part_category') in ['body','doors','glass','pillars','fascia']]
 ray=field(skins);tree=mesh_tree(skins);errors=[];backs={}
 for ob in obs:
  if not ob.get('allow_boundary'):continue
  bm=bmesh.new();bm.from_mesh(ob.data);edges=[e for e in bm.edges if e.is_boundary]
  bad=sum(len(e.link_faces) not in (1,2) for e in bm.edges)
  role=bm.faces.layers.int.get('hatch_outer_skin')
  exposed=sum(any(f[role] for f in e.link_faces) for e in edges) if role else len(edges)
  backs[ob.name]=dict(boundary_edges=len(edges),invalid_edges=bad,boundaries_on_outer_skin=exposed,removed_hidden_triangles=ob['removed_hidden_triangles'],scope='Face-role audit proves every open edge is on a retained gauge return, never on the painted outer skin')
  if bad or exposed:errors.append(ob.name+' hidden-back boundary')
  bm.free()
 mirrors={}
 def intersections(left,right):
  target=mesh_tree([right]);ps=points(left);hits=[]
  for e in left.data.edges:
   aa,bb=[ps[i] for i in e.vertices];delta=bb-aa
   if delta.length<1e-7:continue
   hit,_,_,distance=target.ray_cast(aa,delta.normalized(),delta.length)
   if hit is not None and 1e-6<distance<delta.length-1e-6:hits.append(list(hit))
  return hits
 for suffix in ['L','R']:
  cap=bpy.data.objects['Mirror housing_'+suffix];ps=points(cap);bb=bounds([cap]);pane=points(bpy.data.objects['Mirror pane_'+suffix])
  plane=max(p.y for p in pane);rear=[p for p in pane if p.y>plane-.00001]
  silhouette=[]
  for q in ps:
   hit=tree.ray_cast(Vector((.001,q.y,3)),Vector((0,0,-1)),4)[0]
   if hit is not None:silhouette.append(q.z-hit.z)
  door=mesh_tree([bpy.data.objects['Door F_'+suffix]])
  sail=bpy.data.objects['Mirror sail_'+suffix];distance=min(door.find_nearest(q)[3] for q in points(sail))
  contact=intersections(sail,bpy.data.objects['Door F_'+suffix])
  shoe=bpy.data.objects['Mirror mounting shoe_'+suffix]
  cap_contact=intersections(shoe,cap)
  mirrors[suffix]=dict(bounds_m=bb,bottom_m=bb['min'][2],center_m=[(lo+hi)/2 for lo,hi in zip(bb['min'],bb['max'])],rear_glass_plane_y_m=plane,rear_glass_planarity_m=max(abs(p.y-plane) for p in rear),maximum_above_body_side_profile_m=max(silhouette),sail_nearest_door_distance_m=distance,owner=cap.parent.name)
  mirrors[suffix].update(sail_door_surface_intersections_m=contact,shoe_housing_surface_intersections_m=cap_contact)
  if not(.220<=bb['size'][0]<=.260 and .130<=bb['size'][2]<=.160 and .100<=bb['size'][1]<=.130):errors.append(suffix+' mirror dimensions')
  if max(silhouette)>.001:errors.append(suffix+' mirror above hood/cowl silhouette')
  if not contact or not cap_contact:errors.append(suffix+' mirror support surface intersection absent')
 rear=[]
 for x in [.30,.50,.70]:
  samples=[]
  for z in [.55,.565,.58,.595,.61,.625,.64]:
   q,n,part=ray((x,3,z),(0,-1,0));samples.append(dict(point_m=list(q),normal=list(n),normal_angle_degrees=math.degrees(math.atan2(n.z,n.y)),part=part))
  rear.append(dict(x_m=x,samples=samples,normal_turn_60mm_degrees=abs(samples[5]['normal_angle_degrees']-samples[1]['normal_angle_degrees'])))
 diffuser=bpy.data.objects['Diffuser opening'];raw=list(diffuser['well_mouth_samples']);mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
 guides=list(diffuser['aperture_samples']);nu=diffuser['form_columns'];bottom=[Vector(guides[i:i+3]) for i in range(0,nu*3,3)]
 fascia=bpy.data.objects['Rear molded fascia'];low=min(p.z for p in points(fascia) if abs(p.x)<.70)
 report=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),scope='Actual fixed-stamping boundaries, mirror solids and rear mesh rays; no moving-clearance claim',hidden_back_boundaries=backs,hidden_triangles_removed=sum(r['removed_hidden_triangles'] for r in backs.values()),mirrors=mirrors,mirror_span_m=bounds([o for o in obs if o.get('part_category')=='mirrors'])['size'][0],bumper_upper_crease=rear,diffuser_lower_edge_z_range_m=[min(p.z for p in bottom),max(p.z for p in bottom)],lower_turn_height_m=max(p.z for p in mouth)-low,errors=errors,passed=not errors)
 Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
 if errors and not a.diagnostic:raise AssertionError(errors)
if __name__=='__main__':main()
