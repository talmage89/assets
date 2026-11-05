"""Shared external-image glTFs, with canonical ground and shrub image URIs.

Every embedded PNG must match an authored shipped file byte for byte. Only
geometry is copied to each seed's .bin; no texture is re-encoded here.
"""
import argparse,copy,hashlib,json,struct
from pathlib import Path


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
 data=Path(path).read_bytes();off=12;doc=None;binary=b''
 while off<len(data):
  size,kind=struct.unpack_from('<II',data,off);chunk=data[off+8:off+8+size];off+=8+size
  if kind==0x4e4f534a:doc=json.loads(chunk)
  elif kind==0x004e4942:binary=chunk
 return doc,binary


def bundle(path):
 path=Path(path);doc=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for key in ('buffers','images') for r in doc.get(key,[]) if 'uri' in r]
 return hashlib.sha256(json.dumps({str(p):sha(p) for p in sorted(set(files))},sort_keys=True).encode()).hexdigest()


def part_materials(doc,metadata):
 parents={c:i for i,n in enumerate(doc['nodes']) for c in n.get('children',[])};rows={k:dict(materials=set(),draw_primitives=0) for k in metadata['triangles']}
 for i,node in enumerate(doc['nodes']):
  if 'mesh' not in node:continue
  owner=i
  while doc['nodes'][owner].get('name') not in rows and owner in parents:owner=parents[owner]
  name=doc['nodes'][owner].get('name');assert name in rows,(name,node.get('name'))
  primitives=doc['meshes'][node['mesh']]['primitives'];rows[name]['materials'].update(doc['materials'][p['material']]['name'] for p in primitives);rows[name]['draw_primitives']+=len(primitives)
 return {k:dict(materials=sorted(v['materials']),material_count=len(v['materials']),draw_primitives=v['draw_primitives'],triangles=metadata['triangles'][k]) for k,v in rows.items()}


def externalize(seed,source_root=Path('build/look')):
 source=source_root/f'station-{seed}.glb';doc,binary=read(source);out=Path(f'export/CommercialGas-{seed}.gltf');out.parent.mkdir(parents=True,exist_ok=True)
 folders=(Path('textures/ship'),Path('../ground/textures/ship'),Path('../shrubs/textures/ship'))
 paths=[p for folder in folders for p in folder.glob('*.png')];known={sha(p):p for p in paths};names={p.stem:p for p in paths};images=[]
 for im in doc['images']:
  view=doc['bufferViews'][im.pop('bufferView')];start=view.get('byteOffset',0);data=binary[start:start+view['byteLength']];digest=hashlib.sha256(data).hexdigest()
  candidate=names.get(im.get('name',''));chosen=candidate if candidate and sha(candidate)==digest else known.get(digest)
  assert chosen is not None,'Exporter changed image bytes: '+str(im)
  if chosen.parent==Path('textures/ship'):
   dest=out.parent/'textures'/chosen.name;dest.parent.mkdir(parents=True,exist_ok=True)
   if not dest.exists() or dest.read_bytes()!=data:dest.write_bytes(data)
   uri='textures/'+dest.name
  else:uri='../'+chosen.as_posix()
  im['uri']=uri;im.pop('mimeType',None);images.append(dict(uri=uri,sha256=digest,bytes=len(data)))
 used=sorted({a['bufferView'] for a in doc['accessors']});views=[];remap={};payload=bytearray()
 for old in used:
  payload.extend(b'\0'*(-len(payload)%4));v=copy.deepcopy(doc['bufferViews'][old]);start=v.get('byteOffset',0);data=binary[start:start+v['byteLength']]
  v['buffer']=0;v['byteOffset']=len(payload);payload.extend(data);remap[old]=len(views);views.append(v)
 for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
 doc['bufferViews']=views;doc['buffers']=[dict(uri=out.with_suffix('.bin').name,byteLength=len(payload))]
 out.with_suffix('.bin').write_bytes(payload);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
 metadata=json.loads(source.with_suffix('.json').read_text());metadata['delivery_bundle_sha256']=bundle(out);out.with_suffix('.json').write_text(json.dumps(metadata,indent=2))
 return dict(seed=seed,parts=part_materials(doc,metadata),triangles=metadata['triangles'],total_triangles=metadata['total_triangles'],gltf_bytes=out.stat().st_size,bin_bytes=len(payload),embedded_glb_bytes=source.stat().st_size,images=images,materials=len(doc['materials']),bundle_sha256=bundle(out))


def main(seeds,source_root):
 rows=[externalize(seed,source_root) for seed in seeds]
 # Publish the whole family once, including the two alternatives not used by
 # the default seed. Unchanged maps retain their original bytes.
 folder=Path('export/textures');folder.mkdir(parents=True,exist_ok=True)
 for old in folder.glob('T_CommercialTrim_*.png'):old.unlink()
 for p in Path('textures/ship').glob('T_Commercial*.png'):
  dst=folder/p.name;data=p.read_bytes()
  if not dst.exists() or dst.read_bytes()!=data:dst.write_bytes(data)
 Path('build/delivery.json').write_text(json.dumps(dict(rows=rows,new_images=18,new_gpu_mib=29,scope='External stock glTF; canonical ground and shrub image paths, byte-identical maps; compressed-memory estimate assumes 8bpp and full mips'),indent=2))
 for r in rows:print('DELIVERY',r['seed'],r['gltf_bytes']+r['bin_bytes'],'geometry bytes',r['materials'],'materials')


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--seeds',default='101,102,103,104');a.add_argument('--source-root',type=Path,default=Path('build/look'));a=a.parse_args();main(list(map(int,a.seeds.split(','))),a.source_root)
