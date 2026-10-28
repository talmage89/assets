"""Strict texture-only revision proof against an accepted local export snapshot.

Every non-image buffer byte and delivery JSON field must match. Only image
payload lengths and the resulting buffer offsets/length may change.
"""
import argparse,copy,hashlib,json,struct
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
class GLB:
 def __init__(self,path):
  raw=path.read_bytes();magic,version,length=struct.unpack_from('<III',raw)
  assert magic==0x46546c67 and version==2 and length==len(raw)
  offset=12
  while offset<len(raw):
   size,kind=struct.unpack_from('<II',raw,offset);chunk=raw[offset+8:offset+8+size]
   if kind==0x4e4f534a:self.json=json.loads(chunk)
   elif kind==0x004e4942:self.binary=chunk
   offset+=8+size

def compare(before,after):
 assert {p.name for p in before.glob('*.glb')}=={p.name for p in after.glob('*.glb')}
 result={}
 for path in sorted(before.glob('*.glb')):
  old,new=GLB(path),GLB(after/path.name)
  image_views={i['bufferView'] for i in old.json['images']}
  assert len(old.json['bufferViews'])==len(new.json['bufferViews'])
  payload=[]
  for i,(a,b) in enumerate(zip(old.json['bufferViews'],new.json['bufferViews'])):
   if i in image_views:continue
   def data(glb,row):
    start=row.get('byteOffset',0);return glb.binary[start:start+row['byteLength']]
   x,y=data(old,a),data(new,b)
   assert x==y,(path.name,'changed non-image buffer',i)
   payload.append(x)
  docs=[]
  for glb in (old,new):
   doc=copy.deepcopy(glb.json)
   for buffer in doc['buffers']:buffer['byteLength']=0
   for view in doc['bufferViews']:view.pop('byteOffset',None)
   for i in image_views:doc['bufferViews'][i]['byteLength']=0
   docs.append(doc)
  assert docs[0]==docs[1],(path.name,'changed delivery JSON')
  result[path.name]=dict(non_image_bytes_identical=True,delivery_json_identical=True,
   non_image_bytes=sum(map(len,payload)),non_image_sha256=hashlib.sha256(b''.join(payload)).hexdigest())
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--before',required=True,type=Path)
 p.add_argument('--after',type=Path,default=BASE/'export');p.add_argument('--out',type=Path,default=BASE/'build/delivery-identity.json')
 a=p.parse_args();result=compare(a.before,a.after);a.out.write_text(json.dumps(result,indent=2))
 print('IDENTICAL GEOMETRY, RIG AND DELIVERY:',', '.join(result))
