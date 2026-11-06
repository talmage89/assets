"""Cold model rebuild in an empty local workspace; compare export bytes.

The canonical outputs and their timestamps are never changed by this check.
"""
import hashlib,json,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent

def snapshot(root):
 paths=list((root/'export').glob('*.gltf'))+list((root/'export').glob('*.bin'))+list((root/'export/textures').glob('*.png'))+list((root/'build/blocks').glob('*/block.glb'))
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
before=snapshot(Path('.'));assert before
workspace=Path('build/repeat-workspace');shutil.rmtree(workspace,ignore_errors=True);workspace.mkdir(parents=True)
with Path('build/repeat-build.log').open('w') as log:
 subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/downtown.blend'],stdout=log,stderr=subprocess.STDOUT,check=True,cwd=workspace)
after=snapshot(workspace);changed=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
report=dict(passed=not changed,files=len(before),changed=changed,hashes=after,scope='Cold rebuild: glTF/bin/shared PNG and checkpoint GLB bytes; blend container bytes excluded')
Path('build/repeat.json').write_text(json.dumps(report,indent=2)+'\n');assert not changed,changed
print('REPEAT PASS',len(before),'geometry and shared-image files byte-identical after cold rebuild')
