"""Record immutable accepted outputs; never include new form/look-dev files."""
import hashlib,json
from pathlib import Path
from dependencies import snapshot

root=Path(__file__).resolve().parents[2];local=root/'parking-garage'
files=[p for base in ('export','textures/checkpoint') for p in (local/base).rglob('*') if p.is_file() and not any(part in ('form','lookdev') for part in p.relative_to(local).parts)]
dest=local/'build/lookdev/baseline.json';dest.parent.mkdir(parents=True,exist_ok=True)
if not dest.exists():dest.write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
data=json.loads(dest.read_text());assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in data.items())
print('ACCEPTED GARAGE FILES UNCHANGED',len(data))
external=local/'build/lookdev/preservation-external.json'
if not external.exists():external.write_text(json.dumps(snapshot(),indent=2)+'\n')
data=json.loads(external.read_text());assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in data.items())
print('EXISTING LIBRARY FILES UNCHANGED',len(data))
