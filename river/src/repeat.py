"""Exact deterministic geometry/texture/manifest repeat; excludes blend containers."""
import hashlib
import json
import os
import shlex
import subprocess
from pathlib import Path


def hashes():
    paths=sorted(Path('export').rglob('*'))+sorted(Path('textures/checkpoint').glob('*.png'))
    paths+=sorted(Path('build').glob('River*.json'))+sorted(Path('build/pieces').glob('*.json'))+[Path('build/manifest.json')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def main():
    before=hashes()
    with Path('build/repeat.log').open('w') as f:
        subprocess.run(shlex.split(os.environ.get('BLENDER','blender'))+['-b','-t','1','--factory-startup','--python-exit-code','1',
            '--python','src/build.py','--','--out','build/repeat.blend'],stdout=f,stderr=subprocess.STDOUT,check=True)
    after=hashes();changed=[p for p in before if after.get(p)!=before[p]]
    Path('build/repeat.json').write_text(json.dumps(dict(passed=not changed,files=len(before),changed=changed),indent=2)+'\n')
    if changed:raise ValueError(('Repeat mismatch',changed))
    print('RIVER_EXACT_REPEAT_PASS',len(before))


if __name__=='__main__':main()
