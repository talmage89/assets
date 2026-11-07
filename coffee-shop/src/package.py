"""External image delivery, canonical reuse and content receipts."""
import copy
import hashlib
import json
import os
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def externalize(source,dest):
    from kit.gltf import GLB
    g=GLB(Path(source));d=g.json;dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    # Reused delivered maps keep their canonical family path. Only our new
    # quick sheet/host lettering is extracted locally, once across all seeds.
    known={}
    for folder in ['patio-set/textures/ship','street-furniture/export/textures','ground/textures/ship','commercial/export/textures','commercial/textures/ship','downtown/textures/ship','trees/textures/ship','shrubs/textures/ship','houses/textures/ship','cars/textures/ship','street-light/textures/ship']:
        for p in (REPO/folder).glob('*.png'):known[sha(p)]=p
    for folder in ('build/atlas','textures/ship'):
        for p in Path(folder).glob('*.png'):known[sha(p)]=p.resolve()
    # Standalone pieces and complete sites resolve the same image identities.
    folder=Path('export/textures');folder.mkdir(parents=True,exist_ok=True)
    for im in d.get('images',[]):
        v=d['bufferViews'][im.pop('bufferView')];a=v.get('byteOffset',0);payload=g.binary[a:a+v['byteLength']];digest=hashlib.sha256(payload).hexdigest();match=known.get(digest)
        if match and 'coffee-shop' not in match.parts:target=match
        else:
            name=match.name if match else im.get('name','HostGraphic')+'.png';target=folder/name
            if target.exists() and target.read_bytes()!=payload and not (match and name.startswith('T_CoffeeShop_')):raise ValueError(f'Canonical image conflict {name}')
            if not target.exists() or target.read_bytes()!=payload:target.write_bytes(payload)
        im['uri']=os.path.relpath(target.resolve(),dest.parent.resolve());im.pop('mimeType',None)
    used=sorted({a['bufferView'] for a in d.get('accessors',[]) if 'bufferView' in a});remap={};views=[];buf=bytearray()
    for old in used:
        buf.extend(b'\0'*(-len(buf)%4));v=copy.deepcopy(d['bufferViews'][old]);a=v.get('byteOffset',0);payload=g.binary[a:a+v['byteLength']];v.update(byteOffset=len(buf),buffer=0);buf.extend(payload);remap[old]=len(views);views.append(v)
    for a in d.get('accessors',[]):
        if 'bufferView' in a:a['bufferView']=remap[a['bufferView']]
    d['bufferViews']=views;d['buffers']=[dict(byteLength=len(buf),uri=dest.with_suffix('.bin').name)]
    # The kit compacts image/texture views after its initial material pass.
    # Fresh imports of several stock pieces can therefore leave otherwise
    # identical materials referring to the newly unified texture indices.
    # Collapse those exact states here; no mesh, texture or response changes.
    unique=[];lookup={};material_map={}
    for i,m in enumerate(d.get('materials',[])):
        key=json.dumps({k:v for k,v in m.items() if k!='name'},sort_keys=True)
        if key not in lookup:lookup[key]=len(unique);unique.append(m)
        material_map[i]=lookup[key]
    for mesh in d.get('meshes',[]):
        for primitive in mesh['primitives']:
            if 'material' in primitive:primitive['material']=material_map[primitive['material']]
    d['materials']=unique
    dest.with_suffix('.bin').write_bytes(buf);dest.write_text(json.dumps(d,separators=(',',':'))+'\n')
    return dict(gltf_bytes=dest.stat().st_size,bin_bytes=len(buf),images=[dict(uri=im['uri'],bytes=(dest.parent/im['uri']).stat().st_size,sha256=sha(dest.parent/im['uri'])) for im in d.get('images',[])],materials=len(d.get('materials',[])),primitives=sum(len(m['primitives']) for m in d['meshes']))


def bundle(path):
    path=Path(path);d=json.loads(path.read_text());files=[path]+[path.parent/v['uri'] for key in ('images','buffers') for v in d.get(key,[])];h=hashlib.sha256()
    for p in files:h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()
