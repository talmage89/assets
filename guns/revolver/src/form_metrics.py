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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 counts={o.get('part_name',o.name):sum(len(f.vertices)-2 for f in o.data.polygons) for o in parts}
 active=[o for o in parts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 active_count=sum(counts[o.get('part_name',o.name)] for o in active)
 return dict(passed=True,staged_triangles=sum(counts.values()),active_triangles=active_count,
  unloaded_triangles=active_count-sum(counts[o.get('part_name',o.name)] for o in active if o['bone'].startswith('Live')),
  hammer_width=hammer,hammer_slot_width=slot,
  hammer_side_clearance_mm=clearance,guard_width=guard_width,guard_gauge=guard_gauge,
  trigger_width=blade_width,trigger_depth_at_z10=blade_depth,window_running_gaps=windows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 result=dict(passed=True,source=capture(a.source),imported=capture(a.source.with_suffix('.glb')))
 a.out.write_text(json.dumps(result,indent=2));print('ROUND TWO SURFACE GAUGES PASS',result['imported'])
if __name__=='__main__':main()
