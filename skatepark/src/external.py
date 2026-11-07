"""Canonical external image identities; embedded files are build artifacts only."""
import hashlib,json,os
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]

def share_images(path):
    path=Path(path);doc=json.loads(path.read_text())
    folders=[REPO/'skatepark/textures/ship',REPO/'ground/textures/ship',REPO/'trees/textures/ship',REPO/'trees/textures/oak/ship',REPO/'fences/chain-link/textures/ship']
    candidates=[p for folder in folders for p in folder.glob('*.png')]
    known={hashlib.sha256(p.read_bytes()).digest():p for p in candidates}
    rows=[]
    for row in doc.get('images',[]):
        source=path.parent/row['uri'];data=source.read_bytes();digest=hashlib.sha256(data).digest();target=known.get(digest)
        assert target is not None,('No canonical map for',row['uri'])
        row['uri']=os.path.relpath(target,REPO/'skatepark/export/final');row.pop('mimeType',None)
        rows.append(dict(uri=row['uri'],sha256=digest.hex(),bytes=len(data)))
    path.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    path.with_suffix('.images.json').write_text(json.dumps(rows,indent=2))
    return rows

def bundle(path):
    path=Path(path);doc=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in doc.get(k,[]) if r.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
