"""Rebuild the original scripts, then compare every exported geometry/image byte."""
import hashlib,json,subprocess
from pathlib import Path

def snapshot():
 paths=list(Path('export').glob('*.gltf'))+list(Path('export').glob('*.bin'))+list(Path('export/textures').glob('*.png'))+list(Path('build/blocks').glob('*/block.glb'))
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
before=snapshot();assert before
with Path('build/repeat-build.log').open('w') as log:
 subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/downtown.blend'],stdout=log,stderr=subprocess.STDOUT,check=True)
after=snapshot();changed=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
report=dict(passed=not changed,files=len(before),changed=changed,hashes=after,scope='Exported glTF/bin/shared PNG and checkpoint GLB bytes; blend container bytes excluded')
Path('build/repeat.json').write_text(json.dumps(report,indent=2)+'\n');assert not changed,changed
print('REPEAT PASS',len(before),'geometry and shared-image files byte-identical')
