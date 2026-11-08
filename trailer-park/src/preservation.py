"""Immutable sibling delivery receipt; never rebuilds sibling outputs."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FAMILIES=tuple(p.name for p in ROOT.iterdir() if p.is_dir() and p.name!='trailer-park' and (p/'Makefile').is_file())


def snapshot():
    files={}
    for family in FAMILIES:
        for p in (ROOT/family).rglob('*'):
            if p.is_file() and (p.suffix in ('.gltf','.glb','.bin') and 'export' in p.parts or p.suffix in ('.png','.jpg') and any(s in p.parts for s in ('ship','docs','export'))):
                files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return files


def main():
    path=Path('build/preserved.json');path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_text(json.dumps(snapshot(),indent=2));print('Captured immutable inputs')
    old=json.loads(path.read_text())
    for name,digest in old.items():
        p=ROOT/name;assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,('Changed existing delivery',name)
    expanded=Path('build/preserved-look.json')
    if not expanded.exists():expanded.write_text(json.dumps(snapshot(),indent=2))
    for name,digest in json.loads(expanded.read_text()).items():
        p=ROOT/name;assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,('Changed existing delivery',name)
    complete=Path('build/preserved-all.json')
    if not complete.exists():complete.write_text(json.dumps(snapshot(),indent=2))
    for name,digest in json.loads(complete.read_text()).items():
        p=ROOT/name;assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,('Changed existing delivery',name)
    all_files={**old,**json.loads(expanded.read_text()),**json.loads(complete.read_text())}
    round4=Path('build/preserved-round4.json')
    if round4.exists():
        for name,digest in json.loads(round4.read_text()).items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Changed delivery after main merge',name)
            all_files[name]=digest
    print('PRESERVED',len(all_files),'existing files;',len(old),'from the original checkpoint')

if __name__=='__main__':main()
