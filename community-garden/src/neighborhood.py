"""Package the native neighborhood with shared external image identities.

Only this family's exports/cache are written. Native delivery files stay
read-only; their packed images are losslessly externalized when necessary.
"""
import hashlib,json,os,shutil
from pathlib import Path
import bpy


def digest(path):
    p=Path(path);d=json.loads(p.read_text());files=[p]+[p.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[]) if r.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(f.read_bytes()).digest() for f in files)).hexdigest()


def export(path,repo):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    canonical={}
    for folder in (Path('textures/checkpoint'),Path('build/context/chain'),repo/'ground/textures/ship',Path('textures/context')):
        for p in folder.glob('*.png'):canonical[hashlib.sha256(p.read_bytes()).hexdigest()]=p.resolve()
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',
        export_extras=True,export_animations=False,export_tangents=True,export_attributes=True,
        export_vertex_color='NONE',export_image_format='AUTO',export_texture_dir='site-cache')
    doc=json.loads(path.read_text());rows=[]
    for row in doc.get('images',[]):
        copied=path.parent/row['uri'];data=copied.read_bytes();sha=hashlib.sha256(data).hexdigest();target=canonical.get(sha)
        if target is None:
            target=Path('textures/context')/('T_Native_'+sha[:20]+'.png');target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data);target=target.resolve();canonical[sha]=target
        rows.append(dict(image=row.get('name'),sha256=sha,path=os.path.relpath(target,Path.cwd()),bytes=len(data)))
        row['uri']=os.path.relpath(target,path.parent.resolve());row.pop('mimeType',None)
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n');shutil.rmtree(path.parent/'site-cache',ignore_errors=True)
    return rows
