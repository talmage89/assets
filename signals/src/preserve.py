"""Hash existing deliveries without rebuilding or touching them."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];RECEIPT=ROOT/'build/signals-preservation.json'
def run():
 if not RECEIPT.exists():
  rows={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for base in ROOT.iterdir() if base.is_dir() and base.name not in ('signals','build','.git') for kind in ('export','textures/ship') for p in (base/kind).rglob('*') if p.is_file() and p.name!='ArterialCheckpoint.glb'}
  RECEIPT.write_text(json.dumps(rows,indent=2))
 rows=json.loads(RECEIPT.read_text())
 for name,digest in rows.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
 out=ROOT/'signals/build/preservation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(passed=True,files=len(rows),receipt=str(RECEIPT.relative_to(ROOT))),indent=2))
 print('PRESERVATION',len(rows),'existing delivery files unchanged')
if __name__=='__main__':run()
