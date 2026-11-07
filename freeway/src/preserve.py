"""Freeze existing local deliveries once, before a freeway-only build."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    target=Path('build/existing-deliveries.json')
    if target.exists():return
    rows={}
    for family in ('ground','signals','street-signs','street-light','utility','fences','cars','houses','commercial','trees'):
        for p in (ROOT/family).rglob('*'):
            if p.is_file() and any(s in ('export','textures') for s in p.parts):rows[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(rows,indent=2));print('Preserved',len(rows),'existing output hashes')
if __name__=='__main__':main()
