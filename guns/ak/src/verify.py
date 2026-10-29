"""Independent serialization, imported construction and detached spawn audit."""
import argparse,json,sys,io,hashlib
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
from interface import CLIPS
from check import geometry,contacts,semantics,sweep,meshes
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/ak.blend');p.add_argument('--out',default='build/serialization.json');p.add_argument('--diagnostic',action='store_true');p.add_argument('--step',type=float,default=.5)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source).resolve()
 bpy.ops.wm.open_mainfile(filepath=str(path));arm=bpy.data.objects['R39Armature'];source_geometry=geometry(arm)
 samples=[(n,i*.5) for n,s in CLIPS.items() for i in range(s['frames']*2+1)]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 expected=V.capture(arm,samples,sockets);targets={}
 for n,s in CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,n,f);targets[n,f]=V.surface_points(meshes(arm))
 magazine=[o for o in meshes(arm) if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')];spawns={}
 for state,clip in [('loaded','Reload'),('empty','ReloadEmpty')]:
  W.pose(arm,clip,56);visible=[o for o in magazine if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
  spawns[state]=V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy()
 raw=GLB(path.with_suffix('.glb'));normal=V.normal_direction(raw)
 assert {x['name'] for x in raw.json['animations']}==set(CLIPS)
 assert len(raw.json['skins'])==1 and len(raw.json.get('images',[]))==1
 assert sum('normalTexture' in m for m in raw.json['materials'])==3
 payload=raw.image(0);assert Image.open(io.BytesIO(payload)).size==(2048,2048)
 texture=dict(size=[2048,2048],bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest(),kind='original geometry-only tangent normal')
 durations={}
 for animation in raw.json['animations']:
  duration=max(float(raw.accessor(s['input']).max()) for s in animation['samplers'])
  assert abs(duration-CLIPS[animation['name']]['frames']/60)<1e-6
  durations[animation['name']]=duration
 assert any(s['interpolation']=='STEP' for a in raw.json['animations'] for s in a['samplers'])
 for m in raw.json['meshes']:
  for p in m['primitives']:
   w=raw.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
   assert np.all(np.sum(w>1e-6,axis=1)==1)
   n=raw.accessor(p['attributes']['NORMAL']);assert np.isfinite(n).all()
   assert np.max(abs(np.linalg.norm(n,axis=1)-1))<1e-5
 arm=V.import_glb(path.with_suffix('.glb'));affine=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 imported_geometry=geometry(arm,True);imported_contacts=contacts(arm);states=semantics(arm)
 motion=sweep(arm,a.step);surface=[]
 for (n,f),target in targets.items():
  W.pose(arm,n,f);error=V.surface_delta(target,V.surface_points(meshes(arm)));assert error<2e-5,(n,f,error)
  surface.append(dict(clip=n,frame=f,delta_m=error))
 result=dict(passed=motion['passed'] and not imported_geometry['nonmanifold'] and all(r['passed'] for r in imported_contacts),
  stage='form round 2 / geometric normal with inspection constants',texture=texture,clip_durations_s=durations,source_geometry=source_geometry,imported_geometry=imported_geometry,
  imported_contacts=imported_contacts,imported_semantics=states,imported_motion=motion,normal_direction=normal,
  affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),
  maximum_linear_delta=max(r['linear_delta'] for r in affine),surface_samples=surface,standalones={})
 for name in ('magazine_loaded','magazine_empty','cartridge','case'):
  f=path.parent/(name+'.glb');r=GLB(f);norm=V.normal_direction(r)
  tri=sum(len(r.accessor(p['indices']))//3 for m in r.json['meshes'] for p in m['primitives'])
  assert not r.json.get('skins') and not r.json.get('animations')
  V.import_glb(f);parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==1
  xyz=V.surface_points(parts);size=(np.max(xyz,axis=0)-np.min(xyz,axis=0)).tolist()
  row=dict(triangles=tri,bytes=f.stat().st_size,dimensions_m=size,normal_direction=norm,fresh_import=True)
  if name.startswith('magazine_'):
   assert len(r.json.get('images',[]))==1 and r.image(0)==payload,'Detached magazine changed the shared form normal'
   target,xf=spawns[name.split('_')[1]];error=V.surface_delta(target,[tuple(xf@Vector(p)) for p in xyz]);assert error<3e-6
   row['full_rotated_spawn_delta_m']=error
  result['standalones'][name]=row
 Path(a.out).write_text(json.dumps(result,indent=2));print('ROUND TRIP',result['passed'],len(affine),'samples')
 if not a.diagnostic:assert result['passed'],'See '+a.out
if __name__=='__main__':main()
