"""Record immutable accepted outputs; never include new form/look-dev files."""
import hashlib,json
from pathlib import Path
from dependencies import snapshot

root=Path(__file__).resolve().parents[2];local=root/'parking-garage'
files=[p for base in ('export','textures/checkpoint') for p in (local/base).rglob('*') if p.is_file() and not any(part in ('form','lookdev','final') for part in p.relative_to(local).parts)]
dest=local/'build/lookdev/baseline.json';dest.parent.mkdir(parents=True,exist_ok=True)
if not dest.exists():dest.write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
data=json.loads(dest.read_text())
# The owner explicitly permits regenerating these four historical site files.
# Only they embed native caches; modules/garages/maps retain their strict guard.
historical={f'parking-garage/export/sites/ParkingGarageSite-{s}.{ext}' for s in (101,202) for ext in ('gltf','bin')}
strict={p:h for p,h in data.items() if p not in historical}
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in strict.items())
print('ACCEPTED GARAGE FILES UNCHANGED',len(strict),'historical native-car sites may regenerate',len(historical))
external=local/'build/lookdev/preservation-external.json'
if not external.exists():external.write_text(json.dumps(snapshot(),indent=2)+'\n')
data=json.loads(external.read_text());assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in data.items())
print('EXISTING LIBRARY FILES UNCHANGED',len(data))
# Main may have delivered more families since the preceding checkpoint.
# Preserve that complete current inventory too; retain the older audit above.
current=local/'build/delivery-preservation.json'
if not current.exists():current.write_text(json.dumps(snapshot(),indent=2)+'\n')
data=json.loads(current.read_text());assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in data.items())
print('CURRENT LIBRARY FILES UNCHANGED',len(data))
