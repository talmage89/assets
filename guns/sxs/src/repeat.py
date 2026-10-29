"""Independent native rebuild audit; geometry, normals, rig, sockets and clips."""
import argparse,sys,json,hashlib
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def capture(path):
 bpy.ops.wm.open_mainfile(filepath=str(Path(path).resolve()));arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,None,0)
 rows={}
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and 'bone' in ob:
   vertices=[tuple(round(v,9) for v in p.co) for p in ob.data.vertices]
   faces=[]
   for f in ob.data.polygons:
    corners=[(vertices[ob.data.loops[j].vertex_index],tuple(round(v,5) for v in ob.data.corner_normals[j].vector)) for j in f.loop_indices]
    faces.append(min(corners[i:]+corners[:i] for i in range(len(corners))))
   rows['mesh:'+ob['part_name']]=digest(dict(vertices=sorted(vertices),faces=sorted(faces),bone=ob['bone']))
 for b in arm.data.bones:rows['bone:'+b.name]=digest(dict(parent=b.parent.name if b.parent else None,rest=[[round(v,8) for v in r] for r in b.matrix_local]))
 for ob in bpy.context.scene.objects:
  if ob.name.startswith('Socket_'):rows['socket:'+ob.name]=digest(dict(parent=ob.parent_bone,frame=[[round(v,8) for v in r] for r in ob.matrix_world]))
 for action in bpy.data.actions:
  rows['clip:'+action.name]=digest(sorted((fc.data_path,fc.array_index,[(tuple(round(v,8) for v in k.co),k.interpolation) for k in fc.keyframe_points]) for fc in W.fcurves(action)))
 return rows
def main():
 p=argparse.ArgumentParser();p.add_argument('--first',required=True);p.add_argument('--second',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);left=capture(a.first);right=capture(a.second)
 diffs=[k for k in left.keys()|right.keys() if left.get(k)!=right.get(k)]
 Path(a.out).write_text(json.dumps(dict(passed=not diffs,entries=len(left),differences=diffs,
  precision='positions 1 nm, normals 5 decimal vector components; exact key values/interpolation'),indent=2))
 assert not diffs,diffs;print('INDEPENDENT REBUILD PASS',len(left),'entries')
if __name__=='__main__':main()
