"""Compare both accepted house types to the pre-Cape construction bytes.

The fixture was captured before Cape dispatch or construction edits. Accepted
exports, shared images and portfolio docs are independently hashed if present.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import generate
from regression_payload import provenance_normalized_hash


def main(out):
    out.mkdir(parents=True,exist_ok=True);rows=[]
    for expected in json.loads((HERE/'cape_baseline.json').read_text()):
        bpy.ops.wm.read_factory_settings(use_empty=True);path=out/f"{expected['type']}-{expected['seed']}.blend"
        actual=save(build(generate(expected['seed'],house_type=expected['type'])),path)
        row=dict(type=expected['type'],seed=expected['seed'],geometry_sha256=actual['geometry_sha256'],triangles=actual['triangles'],glb_sha256=hashlib.sha256(path.with_suffix('.glb').read_bytes()).hexdigest())
        raw_hash=row['glb_sha256'];normalized,generator=provenance_normalized_hash(path.with_suffix('.glb'))
        row['glb_sha256']=normalized
        assert row==expected,(row,expected)
        row.update(raw_glb_sha256=raw_hash,exporter_generator=generator,normalization='Exporter provenance label only; complete remaining payload compared')
        rows.append(row)
    manifest=Path('build/cape/accepted-files.json');files={}
    if manifest.exists():
        baseline=json.loads(manifest.read_text())
        for p,h in baseline.items():
            assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
            files[p]=h
    result=dict(passed=True,rows=rows,accepted_files_unchanged=files,scope='Exact source vertex/name/count digest and complete compact construction payload after exporter-label normalization; accepted existing delivered files/maps/docs compared independently when available')
    (out/'comparison.json').write_text(json.dumps(result,indent=2));print('CAPE_REGRESSION',len(rows),'construction payloads match after exporter-label normalization;',len(files),'accepted files unchanged')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/cape/regression'));main(p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []).out)
