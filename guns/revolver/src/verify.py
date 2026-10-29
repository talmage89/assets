"""Fresh GLB import, affine/semantic preservation and detached spawn frames."""
import sys,argparse,json,hashlib
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
from semantics import check as semantics
from contacts import measure
from interface import CLIPS
from parameters import generator_digest
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/revolver.blend');p.add_argument('--out',default='build/serialization.json')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();path=source.with_suffix('.glb')
 bpy.ops.wm.open_mainfile(filepath=str(source));arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
 assert arm['generator_sha256']==generator_digest(),'Source is stale relative to current modeling scripts'
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 source_semantics=semantics(arm);sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 samples=[(name,i/2) for name,spec in CLIPS.items() for i in range(spec['frames']*2+1)]
 expected=V.capture(arm,samples,sockets)
 targets={}
 for clip,s in CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values(),s['frames']/2}):
   W.pose(arm,clip,f);targets[(clip,f)]=V.surface_points(parts)
 W.pose(arm,'Idle',0)
 actual=[o for o in parts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 points=np.array(V.surface_points(actual));bounds=[points.min(axis=0).tolist(),points.max(axis=0).tolist()]
 measured={}
 for name in ('Barrel','Cylinder_Fluted','Grip_RubberMold'):
  ob=next(o for o in parts if o['part_name']==name);v=np.array(V.surface_points([ob]))
  measured[name]=dict(bounds_m=[v.min(axis=0).tolist(),v.max(axis=0).tolist()],dimensions_mm=((v.max(axis=0)-v.min(axis=0))*1000).tolist())
 W.pose(arm,'ReloadSingle',96)
 single_round=(V.surface_points([o for o in parts if o['bone']=='InsertRound']),bpy.data.objects['Socket_Round'].matrix_world.copy())
 spawn={}
 for name,bone,clip,frame in [('cartridge','Live0','Idle',0),('case','Case0','IdleAfter6',0),('speedloader_loaded','LoaderGuide','Reload',142)]:
  W.pose(arm,clip,frame)
  owners=('LoaderBody','LoaderRelease',*('LoaderRound'+str(i) for i in range(6))) if name.startswith('speedloader') else (bone,)
  spawn[name]=(V.surface_points([o for o in parts if o['bone'] in owners]),arm.matrix_world@arm.pose.bones[bone].matrix)
 glb=GLB(path);prims=[p for m in glb.json['meshes'] for p in m['primitives']]
 triangles=sum(len(glb.accessor(p['indices']))//3 for p in prims)
 assert not glb.json.get('images'),'Checkpoint must not imply a final atlas'
 assert {x['name'] for x in glb.json['animations']}==set(CLIPS)
 for p in prims:
  w=glb.accessor(p['attributes']['WEIGHTS_0']);assert np.max(np.abs(w.sum(axis=1)-1))<1e-6
  assert np.all((w>1e-6).sum(axis=1)==1)
  n=glb.accessor(p['attributes']['NORMAL']);assert np.max(np.abs(np.linalg.norm(n,axis=1)-1))<1e-5
 normal=V.normal_direction(glb);arm=V.import_glb(path)
 imported_semantics=semantics(arm);contacts=measure(arm);assert contacts['passed'],contacts
 affine=V.compare(arm,expected,position_tolerance_m=3e-6,linear_tolerance=.001)
 imported_parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 surfaces=[]
 for (clip,frame),target in targets.items():
  W.pose(arm,clip,frame);error=V.surface_delta(target,V.surface_points(imported_parts))
  assert error<3e-6,(clip,frame,error)
  surfaces.append(dict(clip=clip,frame=frame,error_m=error))
 result=dict(passed=True,stage='form checkpoint; unbaked quick materials',triangles=triangles,
  materials=len(glb.json['materials']),textures=0,glb_bytes=path.stat().st_size,
  bones=len(arm.data.bones),sockets=len(sockets),parts=len(parts),measured_parts=measured,
  sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bounds_m=bounds,dimensions_mm=((np.array(bounds[1])-bounds[0])*1000).tolist(),
  normal_direction=normal,source_semantics=source_semantics,imported_semantics=imported_semantics,
  imported_contacts=contacts,affine_samples=len(affine),max_position_error_m=max(r['position_delta_m'] for r in affine),
  max_linear_error=max(r['linear_delta'] for r in affine),surface_poses=surfaces,standalones={})
 for name,(target,xf) in spawn.items():
  item=source.parent/(name+'.glb');data=GLB(item);normals=V.normal_direction(data)
  V.import_glb(item);meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
  assert len(meshes)==1 and meshes[0].matrix_world.is_identity
  vertices=V.surface_points(meshes);world=[xf@Vector(v) for v in vertices]
  error=V.surface_delta(target,world);assert error<3e-6,(name,error)
  v=np.array(vertices);dims=(v.max(axis=0)-v.min(axis=0))*1000
  if name=='cartridge':assert abs(dims[1]-40.20)<.03 and abs(dims[0]-11.12)<.03,dims
  if name=='case':assert abs(dims[1]-32.80)<.05 and abs(dims[0]-11.12)<.03,dims
  result['standalones'][name]=dict(triangles=sum(len(data.accessor(p['indices']))//3 for m in data.json['meshes'] for p in m['primitives']),
   bytes=item.stat().st_size,dimensions_mm=dims.tolist(),posed_spawn_error_m=error,normals=normals)
  if name=='cartridge':
   target,round_socket=single_round
   error=V.surface_delta(target,[round_socket@Vector(v) for v in vertices]);assert error<3e-6,error
   result['standalones'][name]['single_reload_spawn_error_m']=error
 Path(a.out).write_text(json.dumps(result,indent=2));print('SERIALIZATION PASS',triangles,'triangles;',len(affine),'affine samples')
if __name__=='__main__':main()
