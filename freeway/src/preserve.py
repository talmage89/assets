"""Freeze existing local deliveries once, before a freeway-only build."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    target=Path('build/existing-deliveries.json')
    session=Path('build/session-preservation.json')
    if not session.exists():
        all_files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for family in ROOT.iterdir() if family.is_dir() and family.name not in ('freeway','.git','build') for p in family.rglob('*') if p.is_file() and any(x in ('export','textures','docs') for x in p.relative_to(family).parts)}
        session.parent.mkdir(parents=True,exist_ok=True);session.write_text(json.dumps(all_files,indent=2))
    if target.exists():return
    rows={}
    for family in ('ground','signals','street-signs','street-light','utility','fences','cars','houses','commercial','trees'):
        for p in (ROOT/family).rglob('*'):
            if p.is_file() and any(s in ('export','textures') for s in p.parts):rows[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(rows,indent=2));print('Preserved',len(rows),'existing output hashes')
if __name__=='__main__':main()
