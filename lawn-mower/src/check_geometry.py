"""Physical measurements on the actual finalized game geometry, independent of export."""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.assembly import distance
from mathutils import Vector

def points(name):
 o=bpy.data.objects[name];dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);m=e.to_mesh();v=[o.matrix_world@p.co for p in m.vertices];e.to_mesh_clear();return v

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));bpy.context.view_layer.update()
 errors=[];wheels={}
 def gate(ok,msg):
  if not ok:errors.append(msg)
 for k in ('FL','FR','RL','RR'):
  center=bpy.data.objects['Wheel_'+k].matrix_world.translation;vs=points('Tire '+k)
  radius=max(math.hypot(v.y-center.y,v.z-center.z) for v in vs);ground=min(v.z for v in vs)
  s=-1 if k.endswith('L') else 1
  tire_inner=min(s*v.x for v in vs)
  supports=[v for prefix in ('Axle height carrier ','Wheel outrigger return ','Spring height adjust lever ','Height lever grip ') for v in points(prefix+k)]
  support_outer=max(s*v.x for v in supports);axial=tire_inner-support_outer
  want=.0889 if k[0]=='F' else .1016
  wheels[k]=dict(center_m=list(center),diameter_m=2*radius,ground_min_m=ground,axial_support_gap_m=axial,proof='Axial separation holds at all wheel angles; axle/hub bore checked separately')
  gate(abs(radius-want)<1e-5,k+' diameter');gate(abs(ground)<.0005,k+' ground');gate(axial>.008,k+' tire support clearance')
 deck_center=bpy.data.objects['MowerBody'].matrix_world.translation
 blade=points('21 inch mulching blade');reach=max(math.hypot(v.x-deck_center.x,v.y-deck_center.y) for v in blade)
 deck=points('Deep drawn 2mm deck with rolled hem')
 # The cut chamber at blade height is the vertical drawn wall; side/rear outlets
 # have no opposing wall and cannot reduce the remaining wall's minimum radius.
 walls=[math.hypot(v.x-deck_center.x,(v.y-deck_center.y)/1.10) for v in deck if .058<v.z<.121]
 wall=min(walls);gap=wall-reach
 width=max(v.x for v in blade)-min(v.x for v in blade)
 gate(abs(width-.5334)<1e-5,'blade width');gate(gap>.007,'rotating blade/deck radial clearance')
 bag=bpy.data.objects['Sewn grass catcher textile'];bm=bmesh.new();bm.from_mesh(bag.data);opening=sum(1 for e in bm.edges if e.is_boundary);bm.free();gate(opening>0,'bag inlet is open')
 bail=bpy.data.objects['OperatorBail'];rest=bail.matrix_basis.copy();bail.matrix_basis=rest@Matrix.Rotation(math.radians(bail['range_degrees'][0]),4,'X');bpy.context.view_layer.update()
 heldgap,heldmethod=distance(bpy.data.objects['Operator presence steel bail'],bpy.data.objects['Cushioned operator grip']);gate(heldgap<.002,'held bail reaches the grip');bail.matrix_basis=rest;bpy.context.view_layer.update()
 origin_bounds=[v for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o for v in points(o.name)]
 lo=[min(v[k] for v in origin_bounds) for k in range(3)];hi=[max(v[k] for v in origin_bounds) for k in range(3)]
 gate(abs((lo[0]+hi[0])/2)<.002 and abs((lo[1]+hi[1])/2)<.002,'footprint origin is centered')
 out=dict(passed=not errors,source=a.source,scope='Physical game surfaces; GLB serialization is the separate delivery check',wheels=wheels,bag_opening_boundary_edges=opening,held_bail_grip_gap_m=heldgap,held_bail_method=heldmethod,blade=dict(width_m=width,maximum_corner_radius_m=reach,chamber_minimum_radius_m=wall,radial_clearance_lower_bound_m=gap),bounds_m=dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)]),errors=errors)
 Path(a.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
 if errors:raise RuntimeError('Mower physical check failed')
if __name__=='__main__':main()
