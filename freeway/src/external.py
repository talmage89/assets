"""External glTF image identity and deterministic source/bundle reporting."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def share(path):
    path=Path(path);d=json.loads(path.read_text())
    folders=[ROOT/'ground/textures/ship',ROOT/'cars/textures/ship',ROOT/'cars/textures/hatch/ship',ROOT/'cars/textures/suv/ship',ROOT/'houses/export/textures',ROOT/'trees/textures/ship',ROOT/'trees/textures/oak/ship',ROOT/'commercial/textures/ship',ROOT/'commercial/export/textures',Path('textures/checkpoint').resolve()]
    known={sha(p):p for folder in folders for p in folder.glob('*.png')}
    shared=Path('export/shared');shared.mkdir(parents=True,exist_ok=True);rows=[]
    for im in d.get('images',[]):
        p=path.parent/im['uri'];h=sha(p);dest=known.get(h)
        if dest is None:
            # Native GLB-only context maps and quick signal graphics have one
            # content-addressed copy shared by every freeway file/seed.
            dest=shared/(h[:20]+'.png')
            if not dest.exists():dest.write_bytes(p.read_bytes())
        im['uri']=os.path.relpath(dest.resolve(),path.parent.resolve());im.pop('mimeType',None)
        rows.append(dict(uri=im['uri'],sha256=h,bytes=dest.stat().st_size))
    for mesh in d.get('meshes',[]):
        for prim in mesh['primitives']:
            mat=d['materials'][prim['material']]
            if mat.get('extras',{}).get('tiling_vertex_tint') is not True:
                # Context's existing material-generated vertex color must remain
                # if its actual shader consumes it. Only form constants opt out.
                if mat.get('name','').startswith('Freeway_Form_') or mat.get('name','')=='Freeway_Checkpoint_Signs':prim['attributes'].pop('COLOR_0',None)
    for mat in d.get('materials',[]):
        if mat.get('name','').startswith('FreewayFenceForm'):
            mat['alphaMode']='MASK';mat['alphaCutoff']=.40;mat['doubleSided']=True
    path.write_text(json.dumps(d,separators=(',',':'))+'\n')
    # The exporter needed these temporary copies only while writing its JSON.
    # All delivered URIs now point at canonical maps or the shared hash cache.
    import shutil
    shutil.rmtree(path.parent/'staging',ignore_errors=True)
    return rows

def bundle(path):
    path=Path(path);d=json.loads(path.read_text());paths=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[]) if 'uri' in r]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in paths)).hexdigest()
