"""Round-two form gauges on actual source/imported triangle surfaces.

These are geometry measurements, independent of the authored profile values;
photo gauges and their perspective limits live in REFERENCE.md. The existing
48 construction records and unchanged-tolerance clip sweep remain separate.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V,motion
from contacts import part

def capture(path):
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
 else:V.import_glb(path.resolve())
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 def hit(name,origin,direction,maximum=.02):
  h=motion.surface(part(name))['tree'].ray_cast(Vector(origin),Vector(direction),maximum)
  assert h[0] is not None,(name,origin,direction)
  return h[0]
 def span(name,origin,axis):
  direction=Vector((0,0,0));direction[axis]=1
  a=hit(name,origin,-direction);b=hit(name,origin,direction)
  return dict(points_m=[list(a),list(b)],size_mm=(b[axis]-a[axis])*1000)
 hammer=span('Hammer_Body',(0,.010,.060),0)
 slot=span('Frame_Forging',(0,.010,.060),0)
 guard_width=span('TriggerGuard_ForgedBow',(0,.040,-.0078),0)
 guard_gauge=span('TriggerGuard_ForgedBow',(0,.040,-.0078),2)
 blade_width=span('Trigger_Shoe',(0,.031,.010),0)
 blade_depth=span('Trigger_Shoe',(0,.031,.010),1)
 spur_root=span('Hammer_Body',(0,-.004,.070),2)
 spur_tip=span('Hammer_Body',(0,-.0075,.072),2)
 spur_width=span('Hammer_Body',(0,-.005,.071),0)
 frame_spur_gauge=hit('Frame_Forging',(.005,.030,.066),(0,-1,0),.060)
 spur_rear=min(v.y for v in motion.surface(part('Hammer_Body'))['points'])
 past_frame=(frame_spur_gauge.y-spur_rear)*1000
 assert 15<past_frame<25,past_frame
 assert 5.5<spur_root['size_mm']<7.5 and 3.1<spur_tip['size_mm']<4.2
 assert 9.0<spur_width['size_mm']<10.4
 windows=[]
 for z,label in [(.0681,'top'),(.02825,'bottom')]:
  d=1 if label=='top' else -1
  frame=hit('Frame_Forging',(0,.060,z),(0,0,d))
  cylinder=hit('Cylinder_Fluted',(0,.060,z),(0,0,-d))
  windows.append(dict(region=label,frame_m=list(frame),cylinder_m=list(cylinder),gap_mm=abs(frame.z-cylinder.z)*1000))
 clearance=(slot['size_mm']-hammer['size_mm'])/2
 assert .10<clearance<.40,(hammer,slot)
 assert 8.2<guard_width['size_mm']<8.6 and 2.5<guard_gauge['size_mm']<3.1
 assert 6.8<blade_width['size_mm']<7.2 and 5.7<blade_depth['size_mm']<6.5
 assert all(.3<r['gap_mm']<.65 for r in windows),windows
 # Round-three construction: independent rays establish a recessed crown,
 # the swing-side passage and an opaque right shroud wall. The existing
 # sweep separately establishes that the passage actually clears the rod.
 crown=hit('Barrel',(.006,.190,.061),(0,-1,0))
 lip=hit('Barrel',(.0086,.190,.061),(0,-1,0))
 recess=(lip.y-crown.y)*1000
 assert 1.2<recess<1.7,(crown,lip,recess)
 release=span('Barrel',(-.004,.120,.049),2)
 assert 3.3<release['size_mm']<3.8,release
 rod=hit('Extractor_Rod',(.030,.120,.0482),(-1,0,0),.05)
 shroud=hit('Barrel',(.030,.120,.0482),(-1,0,0),.05)
 assert shroud.x>rod.x+.003,(rod,shroud)
 # Broad solid cheek beside the internal hammer pocket, from both sides.
 walls=[]
 for y in (.010,.022,.030):
  for z in (.050,.058):
   for side in (-1,1):
    p=hit('Frame_Forging',(side*.030,y,z),(-side,0,0),.06)
    assert side*p.x>.0042,(y,z,side,p)
    walls.append(list(p))
 plate=hit('Frame_Sideplate',(.030,.022,.050),(-1,0,0),.05)
 cheek=hit('Frame_Forging',(.030,.030,.050),(-1,0,0),.05)
 plate_step=abs(plate.x-cheek.x)*1000
 assert plate_step<.08,(plate,cheek,plate_step)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 counts={o.get('part_name',o.name):sum(len(f.vertices)-2 for f in o.data.polygons) for o in parts}
 active=[o for o in parts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 active_count=sum(counts[o.get('part_name',o.name)] for o in active)
 return dict(passed=True,staged_triangles=sum(counts.values()),active_triangles=active_count,
  unloaded_triangles=active_count-sum(counts[o.get('part_name',o.name)] for o in active if o['bone'].startswith('Live')),
  hammer_width=hammer,hammer_slot_width=slot,
  spur_root_side_thickness=spur_root,spur_near_tip_side_thickness=spur_tip,spur_transverse_width=spur_width,
  spur_past_frame_mm=past_frame,spur_frame_gauge_m=list(frame_spur_gauge),
  hammer_side_clearance_mm=clearance,guard_width=guard_width,guard_gauge=guard_gauge,
  trigger_width=blade_width,trigger_depth_at_z10=blade_depth,window_running_gaps=windows,
  crown_recess_mm=recess,crown_floor_m=list(crown),crown_lip_m=list(lip),
  shroud_release=release,right_shroud_first_hit_m=list(shroud),rod_hit_m=list(rod),
  solid_hammer_cheek_hits_m=walls,sideplate_to_adjacent_cheek_mm=plate_step,
  sideplate_hit_m=list(plate),adjacent_cheek_hit_m=list(cheek))

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 result=dict(passed=True,source=capture(a.source),imported=capture(a.source.with_suffix('.glb')))
 a.out.write_text(json.dumps(result,indent=2));print('FORM SURFACE GAUGES PASS',result['imported'])
if __name__=='__main__':main()
