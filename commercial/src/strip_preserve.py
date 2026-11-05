"""Immutable receipt for deliveries already present when strip work begins."""
import hashlib,json
from pathlib import Path
REPO=Path(__file__).resolve().parents[2];receipt=REPO/'build/strip-look/protected.json'
if not receipt.exists():
    receipt.parent.mkdir(parents=True,exist_ok=True)
    rows={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for family in ('commercial','houses','ground') for folder in ('export','textures/ship','docs') for p in (REPO/family/folder).rglob('*') if p.is_file() and 'CommercialStrip-' not in p.name and 'T_StripSigns_' not in p.name}
    receipt.write_text(json.dumps(rows,indent=2)+'\n')
rows=json.loads(receipt.read_text())
for p,digest in rows.items():assert hashlib.sha256((REPO/p).read_bytes()).hexdigest()==digest,('Protected delivery changed',p)
out=REPO/'commercial/build/strip-look/preservation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(passed=True,files=len(rows),scope='Every delivery/doc file present at receipt capture is byte-identical; new dependency rebuilds are excluded from this historical claim.'),indent=2)+'\n')
print('STRIP PRESERVATION',len(rows),'existing files byte-identical')
