"""Build missing older types only; never rewrite an accepted local delivery."""
from pathlib import Path
import hashlib,json
import subprocess
colonial=[Path(f'export/Hearthfield-{s}.gltf') for s in (27,2,3,6,8,14)]
ranch=[Path(f'export/HearthfieldRanch-{s}.gltf') for s in range(11,17)]
cape=[Path(f'export/HearthfieldCape-{s}.gltf') for s in range(31,37)]
accepted=json.loads(Path('src/split_legacy_hashes.json').read_text())
products=[Path(name) for name in accepted if not name.startswith('docs/')]
present=[p for p in products if p.exists()]
# Never replace a partially available accepted delivery. A cold clone has no
# generated old products at all; its exporter patch version can differ from
# the handoff's, so capture its own explicit baseline after rebuilding.
if present:
    missing=[str(p) for p in products if not p.exists()]
    assert not missing,('Incomplete accepted older delivery; restore missing files before export',missing)
else:
    for kind in ('builder_colonial','ranch','cape'):
        subprocess.run(['make','TYPE='+kind,'export'],check=True)
    hashes={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in accepted}
    baseline=Path('build/split/delivery/cold-legacy-baseline.json');baseline.parent.mkdir(parents=True,exist_ok=True)
    baseline.write_text(json.dumps(dict(sha256=hashes,scope='No accepted generated products were present. Rebuilt all three older types; preserve these exact files throughout split delivery. Different exporter patch versions may change provenance bytes.'),indent=2))
assert all(p.exists() for p in colonial+ranch+cape)
print('SPLIT_LEGACY: all 18 accepted exports available')
