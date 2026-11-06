"""Externalize canonical baked images without changing their bytes."""
import copy,hashlib,json
from pathlib import Path


def externalize(source,out):
 from kit.gltf import GLB
 g=GLB(source);doc=g.json;binary=g.binary;out=Path(out);folder=out.parent/'textures';folder.mkdir(parents=True,exist_ok=True)
 known={hashlib.sha256(p.read_bytes()).hexdigest():p for base in ('textures/ship','build/signs') for p in Path(base).glob('*.png')};names=[]
 for im in doc['images']:
  view=doc['bufferViews'][im.pop('bufferView')];a=view.get('byteOffset',0);data=binary[a:a+view['byteLength']];key=hashlib.sha256(data).hexdigest();assert key in known,im
  name=known[key].name;dest=folder/name
  if not dest.exists() or dest.read_bytes()!=data:dest.write_bytes(data)
  im['uri']='textures/'+name;names.append(name)
 used=sorted({a['bufferView'] for a in doc['accessors']});remap={};views=[];output=bytearray()
 for old in used:
  output.extend(b'\0'*(-len(output)%4));v=copy.deepcopy(doc['bufferViews'][old]);a=v.get('byteOffset',0);data=binary[a:a+v['byteLength']];v['byteOffset']=len(output);v['buffer']=0;output.extend(data);remap[old]=len(views);views.append(v)
 for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
 doc['bufferViews']=views;doc['buffers']=[dict(byteLength=len(output),uri=out.with_suffix('.bin').name)]
 out.with_suffix('.bin').write_bytes(output);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
 return doc


def bundle_hash(path):
 path=Path(path);doc=json.loads(path.read_text());h=hashlib.sha256()
 for p in [path]+[path.parent/r['uri'] for key in ('buffers','images') for r in doc.get(key,[])]:
  h.update(p.name.encode());h.update(p.read_bytes())
 return h.hexdigest()
