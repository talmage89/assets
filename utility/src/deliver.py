"""External glTF family packages: lossless, one canonical trio of PNGs."""
import argparse,copy,hashlib,json,struct,shutil
from pathlib import Path


def read(path):
    raw=Path(path).read_bytes();offset=12;doc=None;binary=b''
    while offset<len(raw):
        length,kind=struct.unpack_from('<II',raw,offset);value=raw[offset+8:offset+8+length];offset+=8+length
        if kind==0x4e4f534a:doc=json.loads(value)
        elif kind==0x004e4942:binary=value
    return doc,binary


def bundle(path):
    path=Path(path);doc=json.loads(path.read_text());paths=[path]+[path.parent/r['uri'] for k in ('images','buffers') for r in doc.get(k,[]) if 'uri'in r]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in sorted(set(paths)))).hexdigest()


def externalize(stem,out):
    source=Path('build')/(stem+'.glb');doc,binary=read(source);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    canonical={hashlib.sha256(p.read_bytes()).hexdigest():p for p in Path('textures/ship').glob('T_Utility_*.png')}
    images=[]
    for image in doc.get('images',[]):
        view=doc['bufferViews'][image.pop('bufferView')];offset=view.get('byteOffset',0);payload=binary[offset:offset+view['byteLength']]
        digest=hashlib.sha256(payload).hexdigest();assert digest in canonical,('Reencoded image',image)
        p=canonical[digest];dest=out.parent/'textures'/p.name;dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists() or dest.read_bytes()!=payload:dest.write_bytes(payload)
        image.pop('mimeType',None);image['uri']='textures/'+p.name
        images.append(dict(uri=image['uri'],sha256=digest,bytes=len(payload)))
    payload=bytearray();views=[];remap={}
    for old in sorted({a['bufferView'] for a in doc['accessors']}):
        payload.extend(b'\0'*(-len(payload)%4));view=copy.deepcopy(doc['bufferViews'][old]);start=view.get('byteOffset',0)
        data=binary[start:start+view['byteLength']];view.update(buffer=0,byteOffset=len(payload));payload.extend(data);remap[old]=len(views);views.append(view)
    for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
    doc['bufferViews']=views;doc['buffers']=[dict(uri=out.with_suffix('.bin').name,byteLength=len(payload))]
    out.with_suffix('.bin').write_bytes(payload);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    metadata=json.loads(source.with_suffix('.json').read_text());out.with_suffix('.json').write_text(json.dumps(metadata,indent=2))
    parts={}
    for node in doc['nodes']:
        if 'mesh' not in node:continue
        primitives=doc['meshes'][node['mesh']]['primitives']
        parts[node['name']]=dict(materials=sorted({doc['materials'][p['material']]['name'] for p in primitives}),draw_primitives=len(primitives),
                                triangles=sum(doc['accessors'][p['indices']]['count']//3 for p in primitives))
    return dict(source=str(source),delivery=str(out),bundle_sha256=bundle(out),gltf_bytes=out.stat().st_size,bin_bytes=len(payload),embedded_glb_bytes=source.stat().st_size,
                triangles=metadata['total_triangles'],parts=parts,images=images,materials=len(doc.get('materials',[])))


def main():
    rows=[externalize('utility','export/UtilityParts.gltf')]
    rows += [externalize('street-'+str(seed),f'export/UtilityStreet-{seed}.gltf') for seed in (101,102,103,104)]
    unique={i['uri']:i for r in rows for i in r['images']}
    Path('build/delivery.json').write_text(json.dumps(dict(rows=rows,shared_images=list(unique.values()),compressed_mipmapped_texture_mib=16,
        scope='Three 2048 8bpp maps with full mip chains; geometry counted separately; conductor scalar materials allocate no maps'),indent=2))
    for row in rows:print('DELIVERED',row['delivery'],row['triangles'],row['gltf_bytes']+row['bin_bytes'],'geometry bytes',row['materials'],'materials')


if __name__=='__main__':main()
