"""Independent raw-accessor, fresh-import, surface and full-affine checkpoint audit."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
from interface import CLIPS
from semantics import check as semantics
from contacts import measure
from check import geometry,sweep

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/smg.blend');p.add_argument('--out',default='build/serialization.json')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
 bpy.ops.wm.open_mainfile(filepath=str(source));arm=bpy.data.objects['SMGArmature']
 assert bpy.context.scene['generator_sha256']==hashlib.sha256((Path(__file__).parent/'build.py').read_bytes()).hexdigest(),'Stale generator'
 source_geometry=geometry(arm);source_states=semantics(arm)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o]
 samples=[(name,i*.5) for name,s in CLIPS.items() for i in range(s['frames']*2+1)]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 expected=V.capture(arm,samples,sockets);surface_targets={}
 for name,s in CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,name,f);surface_targets[(name,f)]=V.surface_points(parts)
 mp=[o for o in parts if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')]
 spawns={}
 for variant,clip,f in [('loaded','Reload',46),('empty','ReloadEmpty',90)]:
  W.pose(arm,clip,f);visible=[o for o in mp if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
  spawns[variant]=(V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy())
 raw=GLB(source.with_suffix('.glb'));triangles=0
 for m in raw.json['meshes']:
  for prim in m['primitives']:
   triangles+=len(raw.accessor(prim['indices']))//3
   w=raw.accessor(prim['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
   assert np.all(np.sum(w>1e-6,axis=1)==1)
   n=raw.accessor(prim['attributes']['NORMAL']);xyz=raw.accessor(prim['attributes']['POSITION'])
   assert np.isfinite(n).all() and np.isfinite(xyz).all()
   assert np.max(abs(np.linalg.norm(n,axis=1)-1))<1e-5
 assert triangles==source_geometry['triangles'] and 30000<=triangles<=42000
 assert {a['name'] for a in raw.json['animations']}==set(CLIPS)
 assert len(raw.json['skins'])==1 and not raw.json.get('images')
 assert any(s['interpolation']=='STEP' for a in raw.json['animations'] for s in a['samplers'])
 normal_report=V.normal_direction(raw)
 arm=V.import_glb(source.with_suffix('.glb'));imported_states=semantics(arm);imported_geometry=geometry(arm,imported=True)
 imported_contacts=measure(arm);imported_motion=sweep(arm);assert imported_motion['passed'],'Imported clearance'
 affine=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];surfaces=[]
 for (clip,f),target in surface_targets.items():
  W.pose(arm,clip,f);error=V.surface_delta(target,V.surface_points(meshes));assert error<2e-5,(clip,f,error)
  surfaces.append(dict(clip=clip,frame=f,delta_m=error))
 result=dict(passed=True,stage='form checkpoint: no UV/bake/delivery-texture claim',
  triangles=triangles,materials=len(raw.json['materials']),texture_images=0,bytes=source.with_suffix('.glb').stat().st_size,
  source_geometry=source_geometry,source_states=source_states,imported_geometry=imported_geometry,
  imported_states=imported_states,imported_contacts=imported_contacts,imported_motion=imported_motion,
  affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),
  maximum_linear_delta=max(r['linear_delta'] for r in affine),posed_surface_samples=surfaces,
  normal_direction=normal_report,standalones={})
 for name in ('magazine_loaded','magazine_empty','cartridge','case'):
  path=source.parent/(name+'.glb');raw=GLB(path);normal=V.normal_direction(raw)
  tri=sum(len(raw.accessor(p['indices']))//3 for m in raw.json['meshes'] for p in m['primitives'])
  assert not raw.json.get('animations') and not raw.json.get('skins')
  V.import_glb(path);meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
  assert len(meshes)==1 and meshes[0].matrix_world.is_identity
  xyz=V.surface_points(meshes);lo=np.min(xyz,axis=0);hi=np.max(xyz,axis=0);size=hi-lo
  row=dict(triangles=tri,bytes=path.stat().st_size,dimensions_m=size.tolist(),fresh_import=True,normal_direction=normal)
  if name.startswith('magazine_'):
   target,xf=spawns[name.split('_')[1]];error=V.surface_delta(target,[tuple(xf@Vector(v)) for v in xyz])
   assert error<3e-6,(name,error);row['rotated_spawn_error_m']=error
  elif name=='case':
   assert tri<=700 and np.max(abs(size-np.array([.00992,.01916,.00992])))<.00005,(tri,size)
  else:assert tri<=700 and abs(size[1]-.02951)<.00005,(tri,size)
  result['standalones'][name]=row
 Path(a.out).write_text(json.dumps(result,indent=2))
 print('VERIFIED',triangles,len(affine),'full affine/intended samples; imported contacts/clearance; four detached outputs',flush=True)
if __name__=='__main__':main()
