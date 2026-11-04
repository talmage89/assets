"""Independent raw glTF/image/chart audit and fresh-import surface comparison.

Overlap is intentional in repeated masonry/paving and guarded finish cells.
This checks every actual triangle's chart, area, density and unit normals;
construction/contact and motion remain separate in check.py.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy,numpy as np
from mathutils.kdtree import KDTree
from kit.gltf import GLB
from kit.image_io import read_png
from deliver import bundle
from textures import SETS


def raw_file(path):
 raw=object.__new__(GLB);raw.json=json.loads(path.read_text());raw.binary=(path.parent/raw.json['buffers'][0]['uri']).read_bytes();raw.parents={c:i for i,n in enumerate(raw.json['nodes']) for c in n.get('children',[])};return raw


def weighted(rows):
 rows=sorted(rows);v=np.array([r[0] for r in rows]);w=np.cumsum([r[1] for r in rows]);w/=w[-1]
 return dict(zip(('p10','median','p90'),map(float,np.interp((.1,.5,.9),w,v))))


def check(seed):
 path=Path(f'export/CommercialGas-{seed}.gltf');raw=raw_file(path);d=raw.json;meta=json.loads(path.with_suffix('.json').read_text())
 assert len(raw.binary)==d['buffers'][0]['byteLength'];counts=[];normal_error=0;zero=0;density={};chart_errors=[];image_rows=[]
 for im in d['images']:
  assert 'uri' in im and 'bufferView' not in im
  p=(path.parent/im['uri']).resolve();assert p.is_file()
  from PIL import Image
  image_size=Image.open(p).size
  image_rows.append(dict(uri=im['uri'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=list(image_size),bytes=p.stat().st_size))
 for me in d['meshes']:
  count=0
  for pr in me['primitives']:
   attrs=pr['attributes'];xyz=raw.accessor(attrs['POSITION']);normals=raw.accessor(attrs['NORMAL']);uv=raw.accessor(attrs['TEXCOORD_0']);ix=raw.accessor(pr['indices']).reshape(-1,3)
   assert np.isfinite(xyz).all() and np.isfinite(uv).all();count+=len(ix)
   normal_error=max(normal_error,float(abs(np.linalg.norm(normals,axis=1)-1).max()))
   pa=xyz[ix];tc=uv[ix];area=np.linalg.norm(np.cross(pa[:,1]-pa[:,0],pa[:,2]-pa[:,0]),axis=1)/2
   assert float(area.min())>1e-12,('Degenerate geometry',me['name'])
   du=tc[:,1]-tc[:,0];dv=tc[:,2]-tc[:,0];ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
   zero+=int((ua<1e-14).sum());mat=d['materials'][pr['material']];name=mat['name'];tex=mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
   size=2048
   if tex:
    im=d['images'][d['textures'][tex['index']]['source']];p=path.parent/im['uri']
    from PIL import Image
    size=Image.open(p).width
   vals=np.sqrt(ua/area)*size;density.setdefault(name,[]).extend(zip(map(float,vals),map(float,area)))
   if name=='CommercialTrim':
    # Every triangle stays within one finish strip, including its 8px guards.
    lo=tc[:,:,1].min(axis=1);hi=tc[:,:,1].max(axis=1);g=8/2048
    row=np.floor((lo+hi)*4).astype(int)
    bad=(lo<row/8+g-1e-6)|(hi>(row+1)/8-g+1e-6)
    if bad.any():chart_errors.append((me['name'],name,int(bad.sum())))
   if name in ('CommercialEquipment','CommercialWear','CommercialPriceLED') or name.startswith('Commercial') and name.endswith('Lamp'):
    lo=tc.min(axis=1);hi=tc.max(axis=1);cell=np.floor((lo+hi)/2*np.array((4,8))).astype(int);g=8/2048
    bad=(lo<cell/np.array((4,8))+g-1e-6).any(axis=1)|(hi>(cell+1)/np.array((4,8))-g+1e-6).any(axis=1)
    if bad.any():chart_errors.append((me['name'],name,int(bad.sum())))
   if name.startswith('CommercialGraphics'):assert 'COLOR_0' not in attrs,'Ink must survive without glTF emission vertex tint'
  counts.append(count)
 assert normal_error<1e-5;assert zero==0,('Zero-area UVs',seed,zero);assert not chart_errors,chart_errors
 placed=sum(counts[n['mesh']] for n in d['nodes'] if 'mesh' in n);assert placed==meta['total_triangles']
 # Actual local reusable-module counts include their real moving leaves.
 assert meta['triangles']['Store']<=45000 and meta['triangles']['Canopy']<=18000
 assert all(v<=6000 for k,v in meta['triangles'].items() if k.startswith('Dispenser_'))
 bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/look/station-{seed}.blend').resolve()));bpy.context.view_layer.update()
 source=[tuple(o.matrix_world@v.co) for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
 frames={o.name:np.array(o.matrix_world) for o in bpy.context.scene.objects if o.get('pivot_axis') or o.get('socket_kind') or o.get('detachable')}
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
 actual=[tuple(o.matrix_world@v.co) for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
 def tree(points):
  result=KDTree(len(points))
  for i,p in enumerate(points):result.insert(p,i)
  result.balance();return result
 t=tree(actual);s=tree(source);forward=max(t.find(p)[2] for p in source);reverse=max(s.find(p)[2] for p in actual)
 frame_error=max(float(abs(np.array(bpy.data.objects[n].matrix_world)-m).max()) for n,m in frames.items())
 assert max(forward,reverse)<2e-5 and frame_error<1e-5,(seed,forward,reverse,frame_error)
 return dict(seed=seed,passed=True,placed_triangles=placed,unique_mesh_triangles=sum(counts),per_part=meta['triangles'],materials=len(d['materials']),mesh_primitives=sum(len(m['primitives']) for m in d['meshes']),gltf_bytes=path.stat().st_size,bin_bytes=len(raw.binary),normal_length_max_error=normal_error,degenerate_uv_triangles=zero,chart_guard_errors=chart_errors,density_px_m={k:weighted(v) for k,v in density.items()},source_to_import_max_m=forward,import_to_source_max_m=reverse,pivot_socket_matrix_max_error=frame_error,images=image_rows,bundle_sha256=bundle(path))


def maps():
 rows=[]
 from PIL import Image
 for p in sorted(Path('export/textures').glob('T_Commercial*.png')):
  im=Image.open(p);error=None
  if '_Normal' in p.name:
   a=read_png(p);error=float(abs(np.linalg.norm(a*2-1,axis=2)-1).max());assert error<.008,(p,error)
  assert p.read_bytes()==(Path('textures/ship')/p.name).read_bytes()
  rows.append(dict(file=p.name,size=list(im.size),bytes=p.stat().st_size,gpu_mib=im.width*im.height*4/3/1048576,normal_length_max_error=error))
 assert len(rows)==17 and abs(sum(r['gpu_mib'] for r in rows)-(39+2/3))<1e-6
 return rows


def reuse(seeds):
 bpy.ops.wm.read_factory_settings(use_empty=True);seen={};steps=[]
 for seed in seeds+[seeds[0]]:
  bpy.ops.import_scene.gltf(filepath=str(Path(f'export/CommercialGas-{seed}.gltf').resolve()));current={}
  for im in bpy.data.images:
   if im.source!='FILE' or not im.filepath:continue
   p=str(Path(bpy.path.abspath(im.filepath)).resolve());assert p not in current;current[p]=im.as_pointer()
   if p in seen:assert seen[p]==im.as_pointer(),'Importer duplicated canonical images'
   seen[p]=im.as_pointer()
  steps.append(dict(seed=seed,shared_image_identities=len(current)))
 return dict(passed=True,unique_images=len(seen),steps=steps,scope='Actual same-scene Blender image identity, including repeat station; engine still needs canonical-URI caching')


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--seeds',default='101,102,103,104');a=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);seeds=list(map(int,a.seeds.split(',')))
 rows=[check(s) for s in seeds];result=dict(passed=True,rows=rows,maps=maps(),new_gpu_mib=39+2/3,image_reuse=reuse(seeds),scope='Raw serialization, chart/normal/density/image proof and fresh import; physical construction/motion separately in checks.json')
 Path('build/delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY_CHECK',[(r['seed'],r['placed_triangles'],r['unique_mesh_triangles']) for r in rows])
