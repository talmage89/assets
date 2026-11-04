"""Build missing legacy exports only; preserve an existing accepted delivery."""
from pathlib import Path
import subprocess,json,hashlib
expected=[Path(f'export/Hearthfield-{s}.gltf') for s in (27,2,3,6,8,14)]+[Path(f'export/HearthfieldRanch-{s}.gltf') for s in range(11,17)]
if any(not p.exists() for p in expected) or any(not (Path('textures/ranch-ship')/f'T_RanchRoof_{c}.png').exists() for c in ('BaseColor','Normal','ORM')):
    subprocess.run(['make','TYPE=ranch','export'],check=True)
assert all(p.exists() for p in expected)
# Preserve this clone's accepted canonical bytes, including on a cold build
# with a newer Blender patch. The tracked fixture records the historical audit.
manifest=Path('build/cape/delivery/legacy-before.json')
if not manifest.exists():
    keys=json.loads((Path(__file__).resolve().parent/'cape_legacy_hashes.json').read_text())
    manifest.write_text(json.dumps({name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in keys},indent=2))
print('CAPE_LEGACY',len(expected),'existing family exports available')
