"""Snapshot/check other assets' existing delivery bytes in this worktree."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'build/skateboard-other-deliveries.json'
if '--snapshot' in sys.argv:
    files=[p for p in ROOT.rglob('*') if p.is_file() and not any(q in ('.git','build','refs','renders') for q in p.relative_to(ROOT).parts) and p.relative_to(ROOT).parts[0]!='skateboard' and (p.suffix.lower() in ('.glb','.gltf','.fbx') or 'textures' in p.parts or 'docs' in p.parts)]
    OUT.write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
expected=json.loads(OUT.read_text());errors=[]
for name,digest in expected.items():
    p=ROOT/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append(name)
assert not errors,errors
print('Unchanged other delivery files:',len(expected))
