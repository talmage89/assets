"""Lossless embedded review mirrors of the external-image game packages."""
import hashlib,json,struct
from pathlib import Path


def mirror(path):
    path=Path(path);doc=json.loads(path.read_text());assert len(doc['buffers'])==1
    data=bytearray((path.parent/doc['buffers'][0]['uri']).read_bytes())
    source_digest=hashlib.sha256(path.read_bytes()+data).hexdigest();images=[]
    for im in doc.get('images',[]):
        q=path.parent/im['uri'];blob=q.read_bytes();images.append(hashlib.sha256(blob).hexdigest())
        data.extend(b'\0'*(-len(data)%4));offset=len(data);data.extend(blob)
        view=len(doc.setdefault('bufferViews',[]));doc['bufferViews'].append(dict(buffer=0,byteOffset=offset,byteLength=len(blob)))
        im.pop('uri');im.update(bufferView=view,mimeType='image/png' if blob.startswith(b'\x89PNG') else 'image/jpeg')
    doc['buffers']=[dict(byteLength=len(data))];data.extend(b'\0'*(-len(data)%4))
    payload=json.dumps(doc,separators=(',',':')).encode();payload+=b' '*(-len(payload)%4)
    binary=struct.pack('<III',0x46546c67,2,28+len(payload)+len(data))+struct.pack('<II',len(payload),0x4e4f534a)+payload+struct.pack('<II',len(data),0x004e4942)+data
    out=Path('build/embedded')/(path.stem+'.glb');out.parent.mkdir(parents=True,exist_ok=True)
    if not out.exists() or out.read_bytes()!=binary:out.write_bytes(binary)
    receipt=dict(source=str(path),gltf_and_geometry_sha256=source_digest,image_sha256=images,glb_sha256=hashlib.sha256(binary).hexdigest(),bytes=len(binary),scope='Lossless container packing; geometry and shipping image bytes unchanged')
    out.with_suffix('.json').write_text(json.dumps(receipt,indent=2));return out
