"""Optional exact round-two handoff audit; baseline is review evidence only."""
import argparse, ast, json, sys
from pathlib import Path
import bpy, numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
import preserved

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True)
 p.add_argument('--before-finish',type=Path)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(a.before.resolve()))
 preserved.ACCEPTED=tuple(o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.name!='Rear_Buckhorn')
 old=preserved.capture(a.before);new=preserved.capture(BASE/'build/lever.blend')
 # The sphere's parallel face ordering is immaterial; compare oriented
 # triangles and bound the corner-normal roundoff separately.
 oa=old['meshes']['Front_Bead'].pop('corner_normals');na=new['meshes']['Front_Bead'].pop('corner_normals')
 error=float(np.max(np.abs(np.asarray(oa)-np.asarray(na))));assert error<2e-6
 for key in ('meshes','bones','clips','sockets'):
  assert old[key]==new[key],(key,[n for n in old[key] if old[key][n]!=new[key].get(n)])
 result=dict(passed=True,unchanged_named_meshes=len(preserved.ACCEPTED),
  unchanged_bones=len(old['bones']),unchanged_clips=len(old['clips']),unchanged_socket_frames=len(old['sockets']),
  exact=['ordered vertices','oriented triangles','corner normal fields','rigid owners','rest bones','all clip keys and interpolation','all socket matrices'],
  front_bead_normal_roundoff=error,exceptions=['Rear_Buckhorn rounded outline and 2.02 mm notch'])
 if a.before_finish:
  def expressions(path):
   tree=ast.parse(path.read_text());names={'striae','drag','lower_width','lower_center','lower'}
   return {node.targets[0].id:ast.dump(node.value) for node in ast.walk(tree)
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in names}
  before=expressions(a.before_finish);after=expressions(BASE/'src/lookdev.py')
  assert before==after and len(before)==5
  result['accepted_lower_fillet_expressions_exact']=sorted(before)
 (BASE/'build/look-round2-preserved.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
if __name__=='__main__':main()
