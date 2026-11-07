"""Rebuild deterministic checkpoint glTF/BIN/images and compare exact hashes."""
import hashlib,json,os,subprocess,sys
from pathlib import Path

def hashes():
    files=[p for p in sorted(Path('export').rglob('*')) if p.is_file() and p.suffix in ('.gltf','.bin','.png','.json')]+[Path('build/manifest.json')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

seeds=','.join(str(s['seed']) for s in json.loads(Path('build/manifest.json').read_text())['sites'])
before=hashes();Path('build/repeat-before.json').write_text(json.dumps(before,indent=2))
with Path('build/repeat.log').open('w') as log:subprocess.run([os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/Playground.blend','--seeds',seeds],check=True,stdout=log,stderr=subprocess.STDOUT)
after=hashes();changed=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];out=dict(passed=not changed,files=len(before),changed=changed,scope='Exact geometry, glTF metadata and generated quick images; no GPU texture bake exists at this checkpoint')
Path('build/repeat.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert not changed
