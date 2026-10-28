"""Independent intended-state checks, raw GLB and fresh-import surface audit."""
import argparse,sys,json,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit.gltf import GLB
from kit import weapon as W,weapon_verify as V
from interface import CLIPS
from semantics import check as semantic_check

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/pistol.blend');p.add_argument('--out',default='build/serialization.json')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();glb=GLB(source.with_suffix('.glb'))
 bpy.ops.wm.open_mainfile(filepath=str(source));arm=bpy.data.objects['PistolArmature']
 source_semantics=semantic_check(arm)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 count=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts)
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 samples=[(name,i*.5) for name,spec in CLIPS.items() for i in range(spec['frames']*2+1)]
 expected=V.capture(arm,samples,sockets)
 surfaces={}
 for name,spec in CLIPS.items():
  for f in sorted({0,spec['frames'],*spec['events'].values(),*(t for t in (5.5,40,73,110.5) if t<spec['frames'])}):
   W.pose(arm,name,f);surfaces[(name,f)]=V.surface_points(parts)
 # Spawn matrices are full affine transforms, checked at an angled handoff.
 detached_expected={}
 magparts=[o for o in parts if o['bone'] in ('Magazine','Follower','TopRound','ReserveRound')]
 for variant,clip in [('loaded','Reload'),('empty','ReloadEmpty')]:
  W.pose(arm,clip,40)
  visible=[o for o in magparts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
  detached_expected[variant]=(V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy())
 actual_count=0
 for mesh in glb.json['meshes']:
  for prim in mesh['primitives']:
   actual_count+=len(glb.accessor(prim['indices']))//3
   weights=glb.accessor(prim['attributes']['WEIGHTS_0']);assert np.max(np.abs(weights.sum(axis=1)-1))<1e-6
   assert np.all(np.sum(weights>1e-6,axis=1)==1)
   normals=glb.accessor(prim['attributes']['NORMAL']);assert np.max(np.abs(np.linalg.norm(normals,axis=1)-1))<1e-5
 assert actual_count==count and 25000<=count<=35000,(actual_count,count)
 assert {a['name'] for a in glb.json['animations']}==set(CLIPS)
 assert any(s['interpolation']=='STEP' for a in glb.json['animations'] for s in a['samplers'])
 assert len(glb.json['skins'])==1 and not glb.json.get('images')
 normal=V.normal_direction(glb)
 arm=V.import_glb(source.with_suffix('.glb'))
 imported_semantics=semantic_check(arm)
 rows=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
 surface_rows=[]
 for (clip,frame),target in surfaces.items():
  W.pose(arm,clip,frame);error=V.surface_delta(target,V.surface_points(parts))
  assert error<2e-5,(clip,frame,error)
  surface_rows.append(dict(clip=clip,frame=frame,delta_m=error))
 result=dict(passed=True,stage='form checkpoint; constant materials, no delivery texture claim',
  triangles=count,glb_bytes=source.with_suffix('.glb').stat().st_size,materials=len(glb.json['materials']),
  source_semantics=source_semantics,imported_semantics=imported_semantics,normal_direction=normal,
  sampled_pose_count=len(rows),max_position_delta_m=max(r['position_delta_m'] for r in rows),
  max_linear_delta=max(r['linear_delta'] for r in rows),surface_poses=surface_rows,standalones={})
 for name in ('magazine_loaded','magazine_empty','case'):
  path=source.parent/(name+'.glb');data=GLB(path);normal=V.normal_direction(data)
  primitives=[p for m in data.json['meshes'] for p in m['primitives']]
  tri=sum(len(data.accessor(p['indices']))//3 for p in primitives)
  assert not data.json.get('skins') and not data.json.get('animations')
  V.import_glb(path);meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
  assert len(meshes)==1 and meshes[0].matrix_world.is_identity
  vertices=V.surface_points(meshes);lo=np.min(vertices,axis=0);hi=np.max(vertices,axis=0)
  record=dict(bytes=path.stat().st_size,triangles=tri,blender_dimensions_m=(hi-lo).tolist(),fresh_import=True,normal_direction=normal)
  if name.startswith('magazine'):
   target,spawn=detached_expected[name.split('_')[1]]
   spawned=[tuple(spawn@Vector(p)) for p in vertices]
   error=V.surface_delta(target,spawned);assert error<2e-6,(name,error)
   record['rotated_reload_spawn_error_m']=error;record['spawn_matrix']=[list(r) for r in spawn]
  else:
   assert tri<=400,tri
   assert np.max(np.abs(hi-lo-np.array([.00992,.01916,.00992])))<.00005
  result['standalones'][name]=record
 Path(a.out).write_text(json.dumps(result,indent=2));print('VERIFIED',count,'triangles;',len(rows),'semantic/affine poses; standalone fresh imports and rotated spawn')
if __name__=='__main__':main()
