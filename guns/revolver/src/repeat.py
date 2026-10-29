"""Independent procedural rebuild comparison of native geometry, rig and clips."""
import sys,json,argparse,hashlib
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(Path(path).resolve()))
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,None,0)
 result={}
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and 'bone' in ob:
   coords=[tuple(round(v,10) for v in p.co) for p in ob.data.vertices]
   triangles=[]
   for f in ob.data.polygons:
    row=[coords[i] for i in f.vertices];row=min(row[i:]+row[:i] for i in range(len(row)));triangles.append(row)
   result['mesh:'+ob['part_name']]=digest(dict(vertices=sorted(coords),faces=sorted(triangles),bone=ob['bone'],
    materials=[m.name for m in ob.data.materials],groups=[g.name for g in ob.vertex_groups]))
 for b in arm.data.bones:
  result['bone:'+b.name]=digest(dict(parent=b.parent.name if b.parent else None,matrix=[[round(v,8) for v in r] for r in b.matrix_local]))
 for ob in bpy.context.scene.objects:
  if ob.name.startswith('Socket_'):
   result['socket:'+ob.name]=digest(dict(parent_bone=ob.parent_bone,matrix=[[round(v,8) for v in r] for r in ob.matrix_world]))
 for action in bpy.data.actions:
  rows=[]
  for fc in W.fcurves(action):
   rows.append((fc.data_path,fc.array_index,[(tuple(round(v,8) for v in k.co),k.interpolation) for k in fc.keyframe_points]))
  result['clip:'+action.name]=digest(sorted(rows))
 return result
def main():
 p=argparse.ArgumentParser();p.add_argument('--first',required=True);p.add_argument('--second',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);left=snapshot(a.first);right=snapshot(a.second)
 differences=[k for k in left.keys()|right.keys() if left.get(k)!=right.get(k)]
 Path(a.out).write_text(json.dumps(dict(passed=not differences,entries=len(left),differences=differences,
  method='native positions to 0.1 nm, oriented faces, rigid ownership, rest rig, sockets and exact clip keys; independent rebuild'),indent=2))
 assert not differences,differences
 print('PROCEDURAL REPEAT PASS',len(left),'entries')
if __name__=='__main__':main()
