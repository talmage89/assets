"""Exact six-colonial construction and GLB comparison against the frozen parent.

The six parent hashes were captured before adding the type interface and are
checked in as the regression fixture. Never modifies another checkout.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import generate,PROOF_SEEDS


def main(a):
 baseline=json.loads((HERE/'colonial_baseline.json').read_text());rows=[];a.out.mkdir(parents=True,exist_ok=True)
 for expected in baseline:
  bpy.ops.wm.read_factory_settings(use_empty=True);path=a.out/f"colonial-{expected['seed']}.blend"
  actual=save(build(generate(expected['seed'])),path)
  result=dict(seed=expected['seed'],geometry_sha256=actual['geometry_sha256'],triangles=actual['triangles'],glb_sha256=hashlib.sha256(path.with_suffix('.glb').read_bytes()).hexdigest())
  assert result==expected,(result,expected);rows.append(result)
 report=dict(passed=True,rows=rows,scope='Exact vertex/name digest, triangle count, and complete compact checkpoint GLB bytes; shared maps are never written by ranch builds')
 (a.out/'comparison.json').write_text(json.dumps(report,indent=2));print('COLONIAL_BYTE_COMPARISON',len(rows),'exact')


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/ranch/colonial-regression'));main(p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []))
