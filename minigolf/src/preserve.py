"""Read-only receipt for every pre-existing delivery and documentation file."""
import hashlib,json
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
    receipt=REPO/'minigolf/build/protected.json';receipt.parent.mkdir(parents=True,exist_ok=True)
    if not receipt.exists():
        files=[p for family in REPO.iterdir() if family.is_dir() and family.name!='minigolf' for folder in ('export','textures/ship','docs') for p in (family/folder).rglob('*') if p.is_file()]
        receipt.write_text(json.dumps({str(p.relative_to(REPO)):sha(p) for p in files},indent=2))
    rows=json.loads(receipt.read_text())
    for p,digest in rows.items():assert sha(REPO/p)==digest,p
    revision=REPO/'minigolf/build/revision-before/preserved.json'
    if revision.exists():
        for p,digest in json.loads(revision.read_text()).items():assert sha(REPO/p)==digest,p
    (receipt.parent/'preservation.json').write_text(json.dumps(dict(passed=True,files=len(rows)),indent=2))
    print('PRESERVATION',len(rows),'unchanged files')
if __name__=='__main__':check()
