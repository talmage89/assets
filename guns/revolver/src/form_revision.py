"""Compare the handoff with the form revision; serialization is separate.

The before path is the preserved, ignored handoff checkpoint, never a source
of replacement geometry. Native part/rig/socket/clip digests use repeat.py.
"""
import argparse,json,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).parent))
from repeat import snapshot
CHANGED={'Crane_PivotSupport','Frame_Forging','Barrel','Cylinder_Fluted','Extractor_Star','Extractor_Rod',
 'Ejector_Tip','TriggerGuard_ForgedBow','Trigger_Shoe','Hammer_Body',
 'Hammer_ThumbSpur','Hammer_Nose','Hammer_RestSeat','FiringPin_Bushing','FiringPin',
 'Grip_RubberMold','Grip_ScrewCup','Grip_ScrewCup.001','Grip_Screw','Grip_Screw.001',
 'Hammer_SpurRidge','Hammer_SpurRidge.001','Hammer_SpurRidge.002',
 'Hammer_SpurRidge.003','Hammer_SpurRidge.004'}
ROUND3_CHANGED={'Frame_Forging','Frame_Sideplate','Barrel','Crane_Yoke',
 'Hammer_Body','Hammer_ThumbSpur','FrontSight_PinnedRamp','FrontSight_Pin','RearSight_Leaf',
 'RearSight_NotchBody','RearSight_ElevationScrew','Latch_Thumbpiece','Latch_Screw','Grip_RubberMold',
 'Grip_Screw','Grip_Screw.001','Grip_ScrewCup','Grip_ScrewCup.001'}
def cylinder_forward(path):
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));o=bpy.data.objects['Cylinder_Fluted'];triangles=set()
 for face in o.data.polygons:
  vs=[o.data.vertices[i].co for i in face.vertices]
  if min(v.y for v in vs)>.04105:
   row=[tuple(round(c,9) for c in v) for v in vs]
   triangles.add(min(tuple(row[j:]+row[:j]) for j in range(3)))
 return triangles

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',required=True,type=Path);p.add_argument('--after',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
 p.add_argument('--round',type=int,choices=(2,3,4,5),default=2)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);left=snapshot(a.before);right=snapshot(a.after)
 changed=[k for k in left.keys()|right.keys() if left.get(k)!=right.get(k)]
 allowed={'Frame_Forging','Frame_Sideplate','Barrel','Hammer_Body','Extractor_Rod','Ejector_Tip'} if a.round==5 else {'Frame_Forging','Frame_Sideplate','Barrel','Hammer_Body'} if a.round==4 else ROUND3_CHANGED if a.round==3 else CHANGED
 unexpected=[k for k in changed if not k.startswith('mesh:') or k[5:] not in allowed]
 result=dict(passed=not unexpected,changed=sorted(changed),unexpected=unexpected,
  unchanged=sorted(k for k in left.keys()&right.keys() if left[k]==right[k]),
  note='Native positions, faces and ownership. Exact bones, socket frames and animation keys. All cylinder triangles forward of the extractor seat (Y > 41.05 mm) are compared independently; chamber floors retain their actual-surface checks.')
 forward_before=cylinder_forward(a.before);forward_after=cylinder_forward(a.after)
 result['cylinder_forward_triangles']=len(forward_after)
 result['cylinder_forward_differences']=len(forward_before^forward_after)
 result['passed'] &= forward_before==forward_after
 a.out.write_text(json.dumps(result,indent=2));assert result['passed'],result
 print('FORM REVISION: unchanged rig, sockets, clips, ammunition and speedloader;',len(result['unchanged']),'unchanged entries')
if __name__=='__main__':main()
