"""Keep an immutable receipt for pre-existing house and ground deliveries."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RECEIPT=ROOT/'build/commercial-resume/protected.json'

def run(capture=False):
 if capture and not RECEIPT.exists():
  RECEIPT.parent.mkdir(parents=True,exist_ok=True)
  rows={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for family in ('houses','ground') for folder in ('export','textures/ship') for p in (ROOT/family/folder).rglob('*') if p.is_file()}
  RECEIPT.write_text(json.dumps(rows,indent=2))
 rows=json.loads(RECEIPT.read_text());assert rows
 for name,digest in rows.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Protected delivery changed',name)
 out=ROOT/'commercial/build/preservation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(passed=True,files=len(rows),scope='Every pre-existing house/ground export, external buffer/image and shipped texture byte-identical to the pre-work receipt'),indent=2))
 print('PRESERVATION',len(rows),'files unchanged')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--capture',action='store_true');run(p.parse_args().capture)
