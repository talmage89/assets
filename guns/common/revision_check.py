"""Read-only weapon revision proof: named meshes, rig, sockets and clip keys.

Requires a separately rebuilt baseline blend. No source geometry is replaced.
"""
import argparse,bpy,sys,json,numpy as np
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));from kit import weapon as W
p=argparse.ArgumentParser();p.add_argument('--before',required=True,type=Path);p.add_argument('--after',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);old,new,out=a.before,a.after,a.out
def capture(path):
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));arm=next(o for o in bpy.data.objects if o.type=='ARMATURE');W.pose(arm,None,0)
 meshes={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or o.get('bake_only'):continue
  canonical=lambda vs:min(tuple(vs[i:]+vs[:i]) for i in range(len(vs)))
  corner_map={}
  for face in o.data.polygons:
   key=canonical(list(face.vertices))
   for i in face.loop_indices:corner_map[(key,o.data.loops[i].vertex_index)]=o.data.corner_normals[i].vector[:]
  meshes[o.name]=dict(corner_map=corner_map,canonical_faces=sorted(canonical(list(f.vertices)) for f in o.data.polygons),positions=np.array([v.co[:] for v in o.data.vertices]),polygons=[tuple(f.vertices) for f in o.data.polygons],
    normals=np.array([n.vector[:] for n in o.data.corner_normals]),bone=o.get('bone'),matrix=[list(r) for r in o.matrix_world])
 bones={b.name:dict(parent=b.parent.name if b.parent else None,matrix=[list(r) for r in b.matrix_local]) for b in arm.data.bones}
 sockets={o.name:dict(parent=o.parent.name if o.parent else None,bone=o.parent_bone,matrix=[list(r) for r in o.matrix_world]) for o in bpy.context.scene.objects if o.name.startswith('Socket_')}
 clips={}
 for t in arm.animation_data.nla_tracks:
  action=t.strips[0].action;curves=[]
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for f in bag.fcurves:curves.append((f.data_path,f.array_index,[(tuple(k.co),k.interpolation) for k in f.keyframe_points]))
  clips[t.name]=curves
 return meshes,bones,sockets,clips
A=capture(old);B=capture(new);assert A[1:]==B[1:],'Rig, socket or clips changed';assert set(A[0])==set(B[0])
changed=[];same=[];normalmax=0.
for name,a in A[0].items():
 b=B[0][name]
 if name in ('Trigger_Shoe','Trigger_SafetyBlade'):
  changed.append(dict(part=name,before=len(a['polygons']),after=len(b['polygons'])));continue
 assert np.array_equal(a['positions'],b['positions']),(name,'positions')
 assert a['canonical_faces']==b['canonical_faces'],(name,'triangles or winding')
 assert a['bone']==b['bone'] and a['matrix']==b['matrix'],(name,'bind')
 assert a['corner_map'].keys()==b['corner_map'].keys()
 error=max(np.linalg.norm(np.array(a['corner_map'][key])-np.array(b['corner_map'][key])) for key in a['corner_map']);normalmax=max(normalmax,float(error));assert error<.0006,(name,error)
 same.append(name)
out.write_text(json.dumps(dict(passed=True,changed=changed,unchanged_meshes=same,unchanged_mesh_count=len(same),
 rig_sockets_clips_identical=True,max_unchanged_normal_vector_delta=normalmax),indent=2));print('GEOMETRY IDENTITY',len(same),'unchanged meshes; rig/sockets/clips identical;',changed)
