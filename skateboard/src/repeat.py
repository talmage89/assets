"""Compare independent rebuilds; never infer determinism from input constants."""
import hashlib,json
from pathlib import Path
files=['build/skateboard.glb','build/repeat.glb'];hashes=[hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files]
a=json.loads(Path('build/skateboard.json').read_text());b=json.loads(Path('build/repeat.json').read_text())
r=dict(passed=hashes[0]==hashes[1] and a['parts']==b['parts'],method='Independent factory-startup generation, exact GLB bytes and per-part counts',files=files,sha256=hashes)
Path('build/repeat-check.json').write_text(json.dumps(r,indent=2));print(r);assert r['passed']
