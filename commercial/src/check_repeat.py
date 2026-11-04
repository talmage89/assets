"""Independent factory-startup byte repeat and fixed-geometry brand swap."""
import argparse,hashlib,json,subprocess
from pathlib import Path


def brand_geometry(path):
 import numpy as np
 from deliver import read
 doc,binary=read(path)
 def accessor(index):
  a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']];dt=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
  return np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
 triangles=[]
 for mesh in doc['meshes']:
  for p in mesh['primitives']:
   ix=accessor(p['indices']).reshape(-1,3);position=accessor(p['attributes']['POSITION']);normal=accessor(p['attributes']['NORMAL']);rows=np.concatenate((position,normal),1)[ix]
   # Cyclic rotation preserves winding while ignoring vertex/index order.
   for t in rows:
    candidates=[np.roll(t,k,axis=0).ravel() for k in range(3)];triangles.append(min(candidates,key=lambda r:tuple(r)))
 arr=np.array(triangles);order=np.lexsort(arr.T[::-1]);arr=arr[order]
 frames={n['name']:{k:n[k] for k in ('translation','rotation','scale') if k in n} for n in doc['nodes'] if 'name' in n}
 images=[]
 for im in doc['images']:
  v=doc['bufferViews'][im['bufferView']];start=v.get('byteOffset',0);images.append(hashlib.sha256(binary[start:start+v['byteLength']]).hexdigest())
 return hashlib.sha256(arr.tobytes()).hexdigest(),frames,sorted(images)


def main(blender='blender',look=False,swap=False):
 out=Path('build/repeat');out.mkdir(parents=True,exist_ok=True)
 with Path('build/repeat.log').open('w') as log:
  subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--seeds','101','--out',str(out/'station-101.blend')]+(['--look'] if look else []),stdout=log,stderr=subprocess.STDOUT,check=True)
 a=Path('build/look/station-101.glb' if look else 'build/station-101.glb');b=out/a.name
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 result=dict(seed=101,scope='Separate factory-startup build; byte equality includes geometry, node frames, material state and original embedded maps. Not a GPU bake repeat.',baseline_sha256=sha(a),repeat_sha256=sha(b),bytes=a.stat().st_size)
 result['passed']=result['baseline_sha256']==result['repeat_sha256']
 Path('build/repeat-check.json').write_text(json.dumps(result,indent=2))
 assert result['passed'],'Nondeterministic default station export'
 if swap:
  assert look
  folder=Path('build/brand-swap');folder.mkdir(parents=True,exist_ok=True);plan=folder/'variant.json';plan.write_text(json.dumps(dict(brand='latchline')))
  with Path('build/brand-swap.log').open('w') as log:subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--look','--seeds','101','--plan',str(plan),'--out',str(folder/'station-101.blend')],stdout=log,stderr=subprocess.STDOUT,check=True)
  original=brand_geometry(a);variant=brand_geometry(folder/'station-101.glb');assert original==variant,'Brand changed actual geometry, frame or shared image bytes'
  Path('build/brand-swap-check.json').write_text(json.dumps(dict(passed=True,oriented_geometry_sha256=original[0],frames_checked=len(original[1]),shared_embedded_images=len(original[2]),scope='Both original brands, equal oriented positions/normals and node frames, exact shared PNG payloads; UV/vertex ink selection may change'),indent=2))
 print('REPEAT byte-identical',result['bytes'],'bytes',result['baseline_sha256'])


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--look',action='store_true');p.add_argument('--brand-swap',action='store_true');a=p.parse_args();main(a.blender,a.look,a.brand_swap)
