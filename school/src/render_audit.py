"""Require every final view/pair to name the current exported package."""
import hashlib,json
from pathlib import Path
from PIL import Image
def digest(path):
    doc=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for key in ('buffers','images') for r in doc.get(key,[])]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()

SHOTS=('hero','above','plan','rear','windows','entry','gym','door','roof','scale','blacktop','front','side','accepted_hero')


def main():
    rows={}
    for seed in (101,102,103):
        package=Path('export')/f'Campus-{seed}.gltf'
        expected=digest(package)
        folder=Path('renders/final')/str(seed);receipts=json.loads((folder/'provenance.json').read_text())
        for shot in SHOTS:verify(folder,shot,receipts[shot],expected,rows)
    folder=Path('renders/final-matches');receipts=json.loads((folder/'provenance.json').read_text())
    for name,seed in [('gym',103),('ribbon',102),('walk',101)]:verify(folder,name,receipts[name],digest(Path('export')/f'Campus-{seed}.gltf'),rows)
    folder=Path('renders/eevee/101');receipt=json.loads((folder/'provenance.json').read_text())['hero'];verify(folder,'hero',receipt,digest(Path('export/Campus-101.gltf')),rows)
    assert receipt['engine']=='BLENDER_EEVEE'
    Path('build/render-audit.json').write_text(json.dumps(dict(passed=True,views=rows,scope='Current package hashes and required exported views. Visual acceptance is a separate recorded manual review.'),indent=2));print('FINAL RENDER AUDIT PASS',len(rows),'current exported views')


def verify(folder,name,row,expected,rows):
    path=folder/(name+'.png');im=Image.open(path)
    here=Path(__file__).resolve().parent
    recipe=hashlib.sha256(b''.join((here/f).read_bytes() for f in ('render.py','neighborhood.py'))).hexdigest()
    assert row['package_sha256']==expected,(path,'stale export')
    assert row['presentation_recipe_sha256']==recipe,(path,'stale presentation')
    assert row['source'].startswith('export/') and 'exported external glTF' in row['stage'],(path,'not a delivery view')
    assert im.width==row['width'] and im.width>=1400,(path,'resolution')
    rows[str(path)]=dict(package_sha256=expected,image_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pixels=im.size,engine=row['engine'])

if __name__=='__main__':main()
