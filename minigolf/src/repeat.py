"""Rebuild checkpoint files twice and compare delivered bytes, restoring nothing."""
import hashlib,json,subprocess
from pathlib import Path
files=[p for p in Path('export').rglob('*') if p.suffix in ('.gltf','.bin','.png')]
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with Path('build/repeat.log').open('w') as f:subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/course.blend'],stdout=f,stderr=subprocess.STDOUT,check=True)
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
assert before==after,{p:(h,after[p]) for p,h in before.items() if h!=after[p]}
Path('build/repeat.json').write_text(json.dumps(dict(passed=True,files=len(files),byte_identical=True),indent=2));print('REPEAT',len(files),'delivery files byte-identical')
