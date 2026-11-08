"""External glTF sharing original library image identities; build GLBs stay local."""
import copy
import hashlib
import json
import os
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
KNOWN=None


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def externalize(source,dest):
    from kit.gltf import GLB
    g=GLB(Path(source));d=copy.deepcopy(g.json);dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    global KNOWN
    known=KNOWN if KNOWN is not None else {}
    # Search only existing original maps, never download or synthesize substitutes.
    for folder in ([] if KNOWN is not None else sorted(REPO.iterdir())):
        if not folder.is_dir() or folder.name in ('.git','build','river'): continue
        for sub in ('textures','export/textures','build/context'):
            for p in sorted((folder/sub).rglob('*.png')):
                known.setdefault(sha(p),p)
    KNOWN=known
    local=Path('export/textures');local.mkdir(parents=True,exist_ok=True)
    for im in d.get('images',[]):
        v=d['bufferViews'][im.pop('bufferView')];a=v.get('byteOffset',0)
        data=g.binary[a:a+v['byteLength']];digest=hashlib.sha256(data).hexdigest()
        target=known.get(digest)
        if target is None:
            target=local/(im.get('name','image')+'.png')
            if target.exists() and target.read_bytes()!=data:target=local/(digest[:16]+'.png')
            if not target.exists():target.write_bytes(data)
        im.pop('mimeType',None);im['uri']=os.path.relpath(target.resolve(),dest.parent.resolve())
    for ma in d.get('materials',[]):
        if ma.get('name')=='River_paint_yellow':ma['pbrMetallicRoughness']['baseColorFactor']=[.9,.66,.08,1]
        if ma.get('name')=='River_bank_cards':ma.update(alphaMode='MASK',alphaCutoff=.40)
    used=sorted({a['bufferView'] for a in d.get('accessors',[]) if 'bufferView' in a})
    binary=bytearray();views=[];mapping={}
    for old in used:
        v=copy.deepcopy(d['bufferViews'][old]);a=v.get('byteOffset',0)
        binary.extend(b'\0'*(-len(binary)%4));payload=g.binary[a:a+v['byteLength']]
        v.update(byteOffset=len(binary),buffer=0);binary.extend(payload);mapping[old]=len(views);views.append(v)
    for a in d.get('accessors',[]):
        if 'bufferView' in a:a['bufferView']=mapping[a['bufferView']]
    d['bufferViews']=views;d['buffers']=[dict(byteLength=len(binary),uri=dest.with_suffix('.bin').name)]
    dest.with_suffix('.bin').write_bytes(binary);dest.write_text(json.dumps(d,separators=(',',':'))+'\n')
    return dict(gltf_bytes=dest.stat().st_size,bin_bytes=len(binary),
                materials=len(d.get('materials',[])),images=[dict(uri=im['uri'],sha256=sha(dest.parent/im['uri']),bytes=(dest.parent/im['uri']).stat().st_size) for im in d.get('images',[])])


def bundle(path):
    path=Path(path);d=json.loads(path.read_text());h=hashlib.sha256()
    for p in [path]+[path.parent/v['uri'] for key in ('buffers','images') for v in d.get(key,[])]:
        h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()
