"""Exact byte comparison of independent raw form exports."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--expected',default='build/new/model.glb');p.add_argument('--actual',default='build/repeat-form.glb');p.add_argument('--out',default='build/repeat-form.json');a=p.parse_args()
x=Path(a.expected).read_bytes();y=Path(a.actual).read_bytes();result=dict(byte_identical=x==y,sha256=hashlib.sha256(x).hexdigest(),actual_sha256=hashlib.sha256(y).hexdigest())
Path(a.out).write_text(json.dumps(result,indent=2));print(result)
if x!=y:raise SystemExit('Repeated form GLB differs')
