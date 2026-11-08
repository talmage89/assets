"""Immutable sibling delivery receipt; never rebuilds sibling outputs."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FAMILIES=('houses','apartments','ground','fences','shed','mailbox','trash-cart','utility','street-light','trees','shrubs','cars','school','playground','coffee-shop')


def snapshot():
    files={}
    for family in FAMILIES:
        for p in (ROOT/family).rglob('*'):
            if p.is_file() and (p.suffix in ('.gltf','.glb','.bin') and 'export' in p.parts or p.suffix in ('.png','.jpg') and ('ship' in p.parts or 'docs' in p.parts)):
                files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return files


def main():
    path=Path('build/preserved.json');path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_text(json.dumps(snapshot(),indent=2));print('Captured immutable inputs')
    old=json.loads(path.read_text())
    for name,digest in old.items():
        p=ROOT/name;assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,('Changed existing delivery',name)
    print('PRESERVED',len(old),'existing files')

if __name__=='__main__':main()
