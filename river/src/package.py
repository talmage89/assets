"""External glTF sharing original library image identities; build GLBs stay local."""
import copy
import hashlib
import json
import os
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
KNOWN=None


def compact_attributes(d,binary):
    """Keep exact positions, omit regenerable tangents and unused UV layers.

    Colors use core glTF normalized bytes. Normalized signed-byte normals use
    KHR_mesh_quantization; consumers renormalize them. No silhouette is changed.
    """
    import numpy as np
    data=bytearray(binary);converted={}
    def texcoords(value):
        if isinstance(value,dict):
            result={value.get('texCoord',0)} if 'index' in value else set()
            for v in value.values():result.update(texcoords(v))
            return result
        if isinstance(value,list):return set().union(*(texcoords(v) for v in value))
        return set()
    for mesh in d['meshes']:
        for pr in mesh['primitives']:
            attrs=pr['attributes'];attrs.pop('TANGENT',None)
            used=texcoords(d['materials'][pr['material']])
            for key in list(attrs):
                if key.startswith('TEXCOORD_') and int(key.split('_')[1]) not in used:attrs.pop(key)
            for key in ('NORMAL','COLOR_0'):
                if key not in attrs:continue
                old=attrs[key]
                if old in converted:attrs[key]=converted[old];continue
                a=d['accessors'][old];view=d['bufferViews'][a['bufferView']]
                assert a['componentType']==5126
                n={'VEC3':3,'VEC4':4}[a['type']]
                values=np.ndarray((a['count'],n),dtype='<f4',buffer=binary,
                    offset=view.get('byteOffset',0)+a.get('byteOffset',0),
                    strides=(view.get('byteStride',n*4),4))
                signed=key=='NORMAL';scale=127 if signed else 255
                packed=np.zeros((a['count'],4),dtype='i1' if signed else 'u1')
                packed[:,:n]=np.rint(np.clip(values,-1 if signed else 0,1)*scale)
                data.extend(b'\0'*(-len(data)%4));offset=len(data);data.extend(packed.tobytes())
                ai=len(d['accessors']);converted[old]=ai;attrs[key]=ai
                d['accessors'].append(dict(bufferView=len(d['bufferViews']),componentType=5120 if signed else 5121,
                    normalized=True,count=a['count'],type=a['type']))
                d['bufferViews'].append(dict(buffer=0,byteOffset=offset,byteLength=packed.nbytes,byteStride=4,target=34962))
    # Unreferenced source accessors must not keep their old buffers alive.
    used=sorted({v for me in d['meshes'] for pr in me['primitives'] for v in [pr['indices'],*pr['attributes'].values()]})
    remap={old:i for i,old in enumerate(used)};d['accessors']=[d['accessors'][i] for i in used]
    for me in d['meshes']:
        for pr in me['primitives']:
            pr['indices']=remap[pr['indices']];pr['attributes']={k:remap[v] for k,v in pr['attributes'].items()}
    for key in ('extensionsUsed','extensionsRequired'):
        d.setdefault(key,[])
        if 'KHR_mesh_quantization' not in d[key]:d[key].append('KHR_mesh_quantization')
    return data


def share_geometry(d,binary):
    """Exact payload interning, including material variants of linked meshes.

    Blender exports duplicate accessors for object-material overrides. Preserve
    every bit of vertex/normal/UV/index data while referencing each payload once.
    Node transforms and object extras remain independent.
    """
    used=sorted({v for me in d['meshes'] for pr in me['primitives'] for v in [pr['indices'],*pr['attributes'].values()]})
    remap={old:i for i,old in enumerate(used)};d['accessors']=[d['accessors'][i] for i in used]
    for me in d['meshes']:
        for pr in me['primitives']:
            pr['indices']=remap[pr['indices']];pr['attributes']={k:remap[v] for k,v in pr['attributes'].items()}
    packed=bytearray();views=[];view_map={};seen={}
    used={a['bufferView'] for a in d['accessors'] if 'bufferView' in a}
    for index in sorted(used):
        view=d['bufferViews'][index];start=view.get('byteOffset',0)
        payload=binary[start:start+view['byteLength']]
        schema={k:v for k,v in view.items() if k not in ('buffer','byteOffset','name')}
        key=(json.dumps(schema,sort_keys=True),hashlib.sha256(payload).digest())
        if key not in seen:
            packed.extend(b'\0'*(-len(packed)%4));schema.update(buffer=0,byteOffset=len(packed))
            seen[key]=len(views);views.append(schema);packed.extend(payload)
        view_map[index]=seen[key]
    accessors=[];accessor_map={};seen={}
    for index,old in enumerate(d['accessors']):
        value=copy.deepcopy(old);value.pop('name',None)
        if 'bufferView' in value:value['bufferView']=view_map[value['bufferView']]
        key=json.dumps(value,sort_keys=True)
        if key not in seen:seen[key]=len(accessors);accessors.append(value)
        accessor_map[index]=seen[key]
    meshes=[];mesh_map={};seen={}
    for index,old in enumerate(d['meshes']):
        value=copy.deepcopy(old)
        for pr in value['primitives']:
            pr['indices']=accessor_map[pr['indices']]
            pr['attributes']={k:accessor_map[v] for k,v in pr['attributes'].items()}
        key=json.dumps({k:v for k,v in value.items() if k!='name'},sort_keys=True)
        if key not in seen:seen[key]=len(meshes);meshes.append(value)
        mesh_map[index]=seen[key]
    for node in d['nodes']:
        if 'mesh' in node:node['mesh']=mesh_map[node['mesh']]
    d.update(bufferViews=views,accessors=accessors,meshes=meshes)
    return packed


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def presentation_recipe():
    paths=('river/src/render.py','river/src/views.py','river/src/materials.py','freeway/src/foliage_adapter.py')
    return {p:sha(REPO/p) for p in paths}


def camera_signature(definition):
    return {k:definition[k] for k in ('location','target','lens','roll','aspect') if k in definition}


def externalize(source,dest):
    from kit.gltf import GLB
    g=GLB(Path(source));d=copy.deepcopy(g.json);dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    global KNOWN
    known=KNOWN if KNOWN is not None else {}
    # Search only existing original maps, never download or synthesize substitutes.
    for folder in ([] if KNOWN is not None else sorted(REPO.iterdir())):
        if not folder.is_dir() or folder.name in ('.git','build','river'): continue
        for sub in ('textures','export','build/context'):
            for p in sorted((folder/sub).rglob('*.png')):
                known.setdefault(sha(p),p)
    KNOWN=known
    local=Path('export/textures');local.mkdir(parents=True,exist_ok=True)
    authored={sha(p):p.name for p in Path('textures/checkpoint').glob('*.png')}
    for im in d.get('images',[]):
        v=d['bufferViews'][im.pop('bufferView')];a=v.get('byteOffset',0)
        data=g.binary[a:a+v['byteLength']];digest=hashlib.sha256(data).hexdigest()
        target=known.get(digest)
        if target is None:
            target=local/authored.get(digest,digest[:16]+'.png')
            if not target.exists() or target.read_bytes()!=data:target.write_bytes(data)
        im.pop('mimeType',None);im['uri']=os.path.relpath(target.resolve(),dest.parent.resolve())
    for ma in d.get('materials',[]):
        if ma.get('name')=='River_paint_yellow':ma['pbrMetallicRoughness']['baseColorFactor']=[.9,.66,.08,1]
        if ma.get('name')=='River_bank_cards':ma.update(alphaMode='MASK',alphaCutoff=.40)
    from storage import compact
    binary=share_geometry(d,compact(d,compact_attributes(d,g.binary)))
    d['buffers']=[dict(byteLength=len(binary),uri=dest.with_suffix('.bin').name)]
    dest.with_suffix('.bin').write_bytes(binary);dest.write_text(json.dumps(d,separators=(',',':'))+'\n')
    return dict(gltf_bytes=dest.stat().st_size,bin_bytes=len(binary),
                materials=len(d.get('materials',[])),images=[dict(uri=im['uri'],sha256=sha(dest.parent/im['uri']),bytes=(dest.parent/im['uri']).stat().st_size) for im in d.get('images',[])])


def bundle(path):
    path=Path(path);d=json.loads(path.read_text());h=hashlib.sha256()
    for p in [path]+[path.parent/v['uri'] for key in ('buffers','images') for v in d.get(key,[])]:
        h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()
