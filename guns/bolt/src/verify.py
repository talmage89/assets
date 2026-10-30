"""Fresh-import serialization, intended-state and detachable-spawn checks."""
import argparse,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
from interface import CLIPS
from semantics import check
from optical import passage
from feed_audit import case_frame
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/bolt.blend');p.add_argument('--out',default='build/serialization.json')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);source=Path(a.source).resolve();data=GLB(source.with_suffix('.glb'))
 bpy.ops.wm.open_mainfile(filepath=str(source));arm=bpy.data.objects['B24Armature'];source_states=check(arm)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 samples=[(clip,i*.5) for clip,spec in CLIPS.items() for i in range(spec['frames']*2+1)]
 expected=V.capture(arm,samples,sockets);surfaces={}
 for clip,spec in CLIPS.items():
  for frame in sorted({0,spec['frames'],*spec['events'].values()}):
   W.pose(arm,clip,frame);surfaces[(clip,frame)]=V.surface_points(parts)
 magparts=[o for o in parts if o['bone'] in ('Magazine','Follower','TopRound','ReserveRound')];detached={}
 for state,clip,frame in [('loaded','Reload',62),('empty','ReloadEmpty',100)]:
  W.pose(arm,clip,frame)
  visible=[o for o in magparts if min(abs(x) for x in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
  detached[state]=(V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy())
 case_spawn=case_frame(arm)
 case_points=V.surface_points([o for o in parts if o.name.startswith('CycleCase_')])
 count=sum(len(data.accessor(p['indices']))//3 for m in data.json['meshes'] for p in m['primitives'])
 assert 40000<=count<=50000,count
 assert {x['name'] for x in data.json['animations']}==set(CLIPS)
 assert len(data.json['skins'])==1 and not data.json.get('images')
 assert any(n.get('extras',{}).get('interface_version')=='1.2.0' for n in data.json['nodes'])
 for m in data.json['meshes']:
  for p in m['primitives']:
   w=data.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
   assert np.all((w>1e-6).sum(axis=1)==1)
 normal=V.normal_direction(data)
 arm=V.import_glb(source.with_suffix('.glb'));imported_states=check(arm)
 rows=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 mesh=[o for o in bpy.context.scene.objects if o.type=='MESH'];errs=[]
 optical=passage(mesh,bpy.data.objects['Socket_Eye'].matrix_world.translation)
 for (clip,frame),points in surfaces.items():
  W.pose(arm,clip,frame);d=V.surface_delta(points,V.surface_points(mesh));assert d<2e-5,(clip,frame,d)
  errs.append(dict(clip=clip,frame=frame,error_m=d))
 out=dict(passed=True,triangles=count,bytes=source.with_suffix('.glb').stat().st_size,
  materials=len(data.json['materials']),stage='form checkpoint; unbaked constants',
  source_semantics=source_states,imported_semantics=imported_states,normal_direction=normal,optical_passage=optical,
  affine_samples=len(rows),max_position_delta_m=max(r['position_delta_m'] for r in rows),
  max_linear_delta=max(r['linear_delta'] for r in rows),surface_samples=errs,standalones={})
 for name in ('magazine_loaded','magazine_empty','case'):
  path=source.parent/(name+'.glb');d=GLB(path);n=V.normal_direction(d)
  tri=sum(len(d.accessor(p['indices']))//3 for m in d.json['meshes'] for p in m['primitives'])
  assert not d.json.get('skins') and not d.json.get('animations')
  V.import_glb(path);mesh=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=V.surface_points(mesh)
  lo=np.min(points,axis=0);hi=np.max(points,axis=0)
  row=dict(triangles=tri,bytes=path.stat().st_size,size_m=(hi-lo).tolist(),normal_direction=n,fresh_import=True)
  if name=='case':
   assert tri<=800,tri
   error=V.surface_delta(case_points,[tuple(case_spawn@Vector(v)) for v in points])
   assert error<2e-6,('case physics spawn',error);row['physics_handoff_spawn_error_m']=error
  else:
   target,spawn=detached[name.split('_')[1]];error=V.surface_delta(target,[tuple(spawn@Vector(v)) for v in points])
   assert error<2e-6,(name,error);row['rotated_spawn_error_m']=error
  out['standalones'][name]=row
 Path(a.out).write_text(json.dumps(out,indent=2));print('VERIFIED',count,len(rows),'affine/semantic poses, standalone spawn and winding')
if __name__=='__main__':main()
