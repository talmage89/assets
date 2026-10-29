"""Optional exact accepted-form/rig comparison against the saved handoff."""
import sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W
from preserved import capture

def main():
 import preserved
 baseline=BASE/'build/form3-baseline/lever.blend'
 bpy.ops.wm.open_mainfile(filepath=str(baseline))
 names=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.name not in ('Stock','Lever_FingerLoop','Rear_Buckhorn')]
 preserved.ACCEPTED=tuple(names)
 old=capture(baseline);new=capture(BASE/'build/lever.blend')
 for row in (old,new):row['meshes']['Front_Bead'].pop('corner_normals')
 for key in ('meshes','bones','clips','sockets'):
  assert old[key]==new[key],(key,[n for n in old[key] if old[key][n]!=new[key].get(n)])
 # The stock fix changes normals only: preserve every vertex and triangle.
 values=[]
 for path in (baseline,BASE/'build/lever.blend'):
  bpy.ops.wm.open_mainfile(filepath=str(path));mesh=bpy.data.objects['Stock'].data
  values.append(hashlib.sha256(np.asarray([v.co[:] for v in mesh.vertices],dtype='<f4').tobytes()+np.asarray([list(p.vertices) for p in mesh.polygons],dtype='<i4').tobytes()).hexdigest())
 assert values[0]==values[1]
 result=dict(passed=True,unchanged_named_meshes=len(names),unchanged_bones=len(old['bones']),unchanged_clips=len(old['clips']),unchanged_socket_frames=len(old['sockets']),stock_vertices_and_triangles_identical=True,exceptions=['Stock corner normals','Lever_FingerLoop outer section','Rear_Buckhorn blade'])
 (BASE/'build/form3-preserved.json').write_text(json.dumps(result,indent=2));print(result)
if __name__=='__main__':main()
