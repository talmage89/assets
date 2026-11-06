"""Cold model rebuild in an empty local workspace; compare export bytes.

The canonical outputs and their timestamps are never changed by this check.
"""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def snapshot(root):
 paths=list((root/'export').glob('*.gltf'))+list((root/'export').glob('*.bin'))+list((root/'export/textures').glob('*.png'))+list((root/'build/blocks').glob('*/block.glb'))
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
before=snapshot(Path('.'));assert before
workspace=Path('build/repeat-workspace');shutil.rmtree(workspace,ignore_errors=True);workspace.mkdir(parents=True)
parameters=Path('build/parameters.txt').read_text().split()
settings=dict(v.split('=') for v in parameters)
size=settings.get('size','4096');samples=settings.get('samples','1')
with Path('build/repeat-textures.log').open('w') as log:
 subprocess.run([sys.executable,str(HERE/'textures.py'),'source','--size',size],cwd=workspace,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run([str(HERE.parents[1]/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'textures.py'),'--','bake','--size',size,'--samples',samples],cwd=workspace,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run([sys.executable,str(HERE/'textures.py'),'ship'],cwd=workspace,stdout=log,stderr=subprocess.STDOUT,check=True)
with Path('build/repeat-build.log').open('w') as log:
 subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--out','build/downtown.blend'],stdout=log,stderr=subprocess.STDOUT,check=True,cwd=workspace)
after=snapshot(workspace);changed=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
report=dict(passed=not changed,files=len(before),changed=changed,hashes=after,scope='Cold procedural-field generation, GPU bake/downsample and model rebuild: glTF/bin/shared PNG and checkpoint GLB bytes; blend containers excluded')
Path('build/repeat.json').write_text(json.dumps(report,indent=2)+'\n');assert not changed,changed
print('REPEAT PASS',len(before),'geometry and shared-image files byte-identical after cold rebuild')
