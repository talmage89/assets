"""Lossless external-image family delivery; common URIs across all assemblies.

Material state factors are explicit stock glTF. No runtime custom shader.
"""
import json,hashlib,struct,copy
from pathlib import Path

def read(path):
 data=Path(path).read_bytes();off=12;doc=None;binary=b''
 while off<len(data):
  size,kind=struct.unpack_from('<II',data,off);chunk=data[off+8:off+8+size];off+=8+size
  if kind==0x4e4f534a:doc=json.loads(chunk)
  elif kind==0x004e4942:binary=chunk
 return doc,binary

def write(path,doc,binary):
 j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*(-len(j)%4);binary+=b'\0'*(-len(binary)%4)
 payload=struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary
 Path(path).write_bytes(struct.pack('<III',0x46546c67,2,len(payload)+12)+payload)

def state_factors(path):
 d,b=read(path)
 for m in d.get('materials',[]):
  if m['name'].startswith('SharedLens_'):
   factor=.0007 if m['name'].endswith('Lit') else .012
   m['pbrMetallicRoughness']['baseColorFactor']=[factor,factor,factor,1]
   m['pbrMetallicRoughness']['metallicFactor']=0
   m['alphaMode']='MASK';m['alphaCutoff']=.5
   m['extras']=dict(state='lit' if m['name'].endswith('Lit') else 'off',base_factor=factor)
 write(path,d,b)

def externalize(source,out):
 doc,binary=read(source);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 known={hashlib.sha256(p.read_bytes()).hexdigest():p for p in Path('textures/ship').glob('*.png')}
 for im in doc.get('images',[]):
  v=doc['bufferViews'][im.pop('bufferView')];start=v.get('byteOffset',0);data=binary[start:start+v['byteLength']]
  digest=hashlib.sha256(data).hexdigest();p=known.get(digest)
  assert p is not None,('Image was re-encoded or unshared',im.get('name'),digest)
  dst=Path('export/textures')/p.name;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists() or dst.read_bytes()!=data:dst.write_bytes(data)
  im['uri']=('../textures/' if out.parent.name=='parts' else 'textures/')+p.name;im.pop('mimeType',None)
 used=sorted({a['bufferView'] for a in doc['accessors']});views=[];remap={};payload=bytearray()
 for old in used:
  payload.extend(b'\0'*(-len(payload)%4));v=copy.deepcopy(doc['bufferViews'][old]);start=v.get('byteOffset',0);data=binary[start:start+v['byteLength']]
  v['buffer']=0;v['byteOffset']=len(payload);payload.extend(data);remap[old]=len(views);views.append(v)
 for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
 doc['bufferViews']=views;doc['buffers']=[dict(uri=out.with_suffix('.bin').name,byteLength=len(payload))]
 out.with_suffix('.bin').write_bytes(payload);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
 return dict(file=str(out),json_bytes=out.stat().st_size,geometry_bytes=len(payload),materials=[m['name'] for m in doc['materials']],images=[im['uri'] for im in doc['images']])

def bundle(path):
 p=Path(path);d=json.loads(p.read_text());files=[p]+[p.parent/r['uri'] for key in ('buffers','images') for r in d.get(key,[]) if 'uri' in r]
 return hashlib.sha256(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(set(files))},sort_keys=True).encode()).hexdigest()

def main():
 rows=[externalize(Path(f'build/Signals-{seed}.glb'),Path(f'export/Signals-{seed}.gltf')) for seed in (201,202,203,204)]
 rows += [externalize(p,Path('export/parts')/(p.stem+'.gltf')) for p in sorted(Path('build/parts').glob('*.glb'))]
 for row in rows:row['bundle_sha256']=bundle(row['file'])
 maps=[dict(file=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(Path('export/textures').glob('*.png'))]
 Path('build/delivery.json').write_text(json.dumps(dict(rows=rows,maps=maps,shared_map_bytes=sum(r['bytes'] for r in maps),gpu_compressed_mips_mib=17.5),indent=2))
 print('DELIVERY',len(rows),'external glTFs;',sum(r['bytes'] for r in maps),'shared PNG bytes')
if __name__=='__main__':main()
