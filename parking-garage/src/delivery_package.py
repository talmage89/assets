"""Canonical shared-image glTFs and exact embedded review GLBs.

No Blender scene participates in this step. Geometry buffers are copied
byte-for-byte; only the public buffer filename changes. Review GLBs embed
those buffers and the exact current external image payloads.
"""
import copy,hashlib,json,struct
from pathlib import Path


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def embed(path,out):
    doc=json.loads(path.read_text());assert len(doc['buffers'])==1
    binary=bytearray((path.parent/doc['buffers'][0].pop('uri')).read_bytes())
    for im in doc.get('images',[]):
        payload=(path.parent/im.pop('uri')).read_bytes();binary.extend(b'\0'*(-len(binary)%4))
        im.update(bufferView=len(doc['bufferViews']),mimeType='image/png')
        doc['bufferViews'].append(dict(buffer=0,byteOffset=len(binary),byteLength=len(payload)));binary.extend(payload)
    doc['buffers'][0]['byteLength']=len(binary);binary.extend(b'\0'*(-len(binary)%4))
    raw=json.dumps(doc,separators=(',',':')).encode();raw+=b' '*(-len(raw)%4)
    payload=struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(binary),0x004e4942)+binary
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)


def main():
    rows=[]
    for source in sorted(Path('export/lookdev').rglob('*.gltf')):
        relative=source.relative_to('export/lookdev')
        name=relative.name.replace('ParkingGarageLookSite','ParkingGarageSite').replace('ParkingGarageLook','ParkingGarage')
        dest=Path('export/final')/relative.with_name(name);dest.parent.mkdir(parents=True,exist_ok=True)
        doc=json.loads(source.read_text());original=copy.deepcopy(doc)
        binary=source.parent/doc['buffers'][0]['uri'];target=dest.with_suffix('.bin');target.write_bytes(binary.read_bytes())
        doc['buffers'][0]['uri']=target.name;dest.write_text(json.dumps(doc,separators=(',',':'))+'\n')
        restored=copy.deepcopy(doc);restored['buffers'][0]['uri']=original['buffers'][0]['uri'];assert restored==original
        # Both folders have the same depth; canonical shared image URIs retain
        # identity without a duplicate texture folder or image re-encoding.
        assert binary.read_bytes()==target.read_bytes()
        images={im['uri']:sha(dest.parent/im['uri']) for im in doc.get('images',[])}
        assert all((source.parent/u).resolve()==(dest.parent/u).resolve() for u in images)
        review=Path('build/final-glb')/dest.relative_to('export/final').with_suffix('.glb');embed(dest,review)
        raw=review.read_bytes();assert struct.unpack_from('<III',raw)==(0x46546c67,2,len(raw))
        size,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
        packed=json.loads(raw[20:20+size]);n,kind=struct.unpack_from('<II',raw,20+size);assert kind==0x004e4942
        data=raw[28+size:];assert len(data)==n
        assert data[:target.stat().st_size]==target.read_bytes()
        for im,uri in zip(packed.get('images',[]),images):
            view=packed['bufferViews'][im['bufferView']];start=view.get('byteOffset',0)
            assert hashlib.sha256(data[start:start+view['byteLength']]).hexdigest()==images[uri]
        rows.append(dict(source=str(source),gltf=str(dest),gltf_sha256=sha(dest),bin_sha256=sha(target),review_glb=str(review),review_glb_sha256=sha(review),review_glb_bytes=review.stat().st_size,images=images))
    Path('build/final-package.json').write_text(json.dumps(dict(passed=True,files=rows,geometry='Byte-identical copied BIN; shared external images embedded unchanged for GLB review'),indent=2)+'\n')
    print('FINAL PACKAGING PASS',len(rows),'external packages and embedded review GLBs',flush=True)


if __name__=='__main__':main()
