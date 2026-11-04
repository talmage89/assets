"""Capture/compare all three accepted construction payloads before split edits.

Raw GLB hashes compare every byte in the same installed Blender version.
Accepted deliveries/maps/docs are read-only and independently SHA256 checked.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[1]), str(HERE)]
from build import build, save
from plan import generate

FIXTURE = HERE / 'split_baseline.json'
PROOFS = {'builder_colonial': (27, 2, 3, 6, 8, 14),
          'ranch': (11, 12, 13, 14, 15, 16), 'cape': (31, 32, 33, 34, 35, 36)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(capture=False):
    out = Path('build/split/regression')
    out.mkdir(parents=True, exist_ok=True)
    manifest = Path('build/split/accepted-files.json')
    if capture:
        files = sorted(Path('export').rglob('*')) + sorted(Path('docs').glob('*.jpg'))
        manifest.write_text(json.dumps({str(p): sha(p) for p in files if p.is_file()}, indent=2))
    rows = []
    for kind, seeds in PROOFS.items():
        for seed in seeds:
            bpy.ops.wm.read_factory_settings(use_empty=True)
            path = out / f'{kind}-{seed}.blend'
            report = save(build(generate(seed, house_type=kind)), path)
            rows.append(dict(type=kind, seed=seed, triangles=report['triangles'],
                             geometry_sha256=report['geometry_sha256'],
                             glb_sha256=sha(path.with_suffix('.glb'))))
    if capture:
        FIXTURE.write_text(json.dumps(rows, indent=2) + '\n')
    else:
        expected = json.loads(FIXTURE.read_text())
        assert rows == expected, [(a, b) for a, b in zip(rows, expected) if a != b]
    unchanged = {}
    if manifest.exists():
        for path, digest in json.loads(manifest.read_text()).items():
            assert sha(Path(path)) == digest, path
            unchanged[path] = digest
    result = dict(passed=True, capture=capture, rows=rows,
                  accepted_files_unchanged=unchanged,
                  scope='Exact construction vertices/names/counts and complete raw compact GLBs; accepted files independently hashed. No exporter-label normalization.')
    (out / ('capture.json' if capture else 'comparison.json')).write_text(json.dumps(result, indent=2))
    print('SPLIT_REGRESSION', len(rows), 'exact payloads;', len(unchanged), 'accepted files unchanged')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--capture', action='store_true')
    run(p.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []).capture)
