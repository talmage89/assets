"""Independent raw GLB and fresh-import serialization; never form acceptance."""
import json,sys,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
import interface
from check import meshes,bounds,contacts,ALLOW
from kit import motion
BASE=Path(__file__).resolve().parents[1]

def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/lmg.blend'));arm=bpy.data.objects['HarrowArmature']
 samples=[]
 for n,s in interface.CLIPS.items():
  times={0,s['frames'],*s['events'].values()}
  for a,b in zip(sorted(times),sorted(times)[1:]):times.add((a+b)/2)
  samples.extend((n,float(f)) for f in sorted(times))
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 expected=V.capture(arm,samples,sockets);surface={}
 for n,f in [('Idle',0),('Fire',4),('Reload',60),('BipodDeploy',84),('BeltEnd',12)]:
  W.pose(arm,n,f);surface[n,f]=V.surface_points(meshes(arm))
 raw=GLB(BASE/'build/lmg.glb');normal=V.normal_direction(raw)
 assert {a['name'] for a in raw.json['animations']}==set(interface.CLIPS)
 assert len(raw.json['materials'])==1,'One checkpoint material required'
 assert not raw.json.get('images'),'Unbaked checkpoint must not imply final textures'
 durations={}
 for a in raw.json['animations']:
  d=max(float(raw.accessor(s['input']).max()) for s in a['samplers']);durations[a['name']]=d
  assert abs(d-interface.CLIPS[a['name']]['frames']/60)<2e-6
 for m in raw.json['meshes']:
  for p in m['primitives']:
   if 'WEIGHTS_0' not in p['attributes']:continue
   w=raw.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
   assert np.all(np.sum(w>1e-6,axis=1)==1),'Rigid visual parts need exactly one owner'
 arm=V.import_glb(BASE/'build/lmg.glb');affine=V.compare(arm,expected,position_tolerance_m=3e-5,linear_tolerance=.001)
 differences=[]
 for (n,f),q in surface.items():
  W.pose(arm,n,f);d=V.surface_delta(q,V.surface_points(meshes(arm)));assert d<3e-5,(n,f,d)
  differences.append(dict(clip=n,frame=f,surface_delta_m=d))
 # Different displayed belt owners must actually move their own mesh, not just
 # their bone: this detects shared-deform-data ownership corruption.
 W.pose(arm,'Idle',0);centers=[]
 for i in range(17):
  o=next(o for o in meshes(arm) if o.name.startswith(f'Belt_Round_{i:02d}'))
  lo,hi=bounds(o);centers.append((lo+hi)/2)
 assert min(np.linalg.norm(b-a) for a,b in zip(centers,centers[1:]))>.010
 fit=contacts(arm)
 swept=motion.sweep_clips(arm,list(interface.CLIPS),step_frames=1,tolerance_m=.0002,allow=ALLOW)
 r=dict(passed=swept['passed'] and all(x['passed'] for x in fit),imported_contacts=fit,imported_motion=swept,scope='Serialization only; geometric fit is separate',
  normal_direction=normal,durations_s=durations,affine_samples=len(affine),
  max_position_delta_m=max(v['position_delta_m'] for v in affine),
  max_linear_delta=max(v['linear_delta'] for v in affine),surface_samples=differences,
  bytes=(BASE/'build/lmg.glb').stat().st_size,material_count=len(raw.json['materials']))
 (BASE/'build/serialization.json').write_text(json.dumps(r,indent=2));print('ROUND TRIP',r['passed'],len(affine),'affine samples',r['max_position_delta_m'],'m maximum delta')
 assert r['passed'],'See build/serialization.json'
if __name__=='__main__':main()
