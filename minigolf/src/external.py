"""External image identities: one canonical copy per family across every seed."""
import hashlib,json,os
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]

def share(path):
 path=Path(path);doc=json.loads(path.read_text());folders=[REPO/'minigolf/textures/ship',REPO/'ground/textures/ship',REPO/'fences/textures/ship',REPO/'shrubs/textures/ship',REPO/'trees/textures/ship',REPO/'trees/textures/oak/ship']
 known={hashlib.sha256(p.read_bytes()).digest():p for folder in folders for p in folder.glob('*.png')};rows=[]
 for im in doc.get('images',[]):
  source=path.parent/im['uri'];data=source.read_bytes();digest=hashlib.sha256(data).digest();target=known.get(digest)
  assert target is not None,('Unrecognized image payload',im['uri'])
  im['uri']=os.path.relpath(target,path.parent);im.pop('mimeType',None);rows.append(dict(uri=im['uri'],sha256=digest.hex(),bytes=len(data)))
 path.write_text(json.dumps(doc,separators=(',',':'))+'\n');path.with_suffix('.images.json').write_text(json.dumps(rows,indent=2));return rows

def bundle(path):
 path=Path(path)
 if path.suffix=='.glb':return hashlib.sha256(path.read_bytes()).hexdigest()
 doc=json.loads(path.read_text());files=[path]+[path.parent/q['uri'] for k in ('buffers','images') for q in doc.get(k,[]) if 'uri' in q]
 return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
