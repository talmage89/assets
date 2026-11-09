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
    paths += [p for p in Path('build/town').rglob('*') if p.is_file() and p.suffix in ('.json','.gltf','.bin','.png') and not p.is_symlink()]
    paths += sorted(Path('build/bank-fields').rglob('*.png'))
    paths += [Path('build/photo-calibration.json')]+sorted(Path('build/photo-balanced').glob('*.png'))
    if Path('build/delivery.json').exists():
        paths += [Path('build/delivery.json')]+sorted(Path('docs').glob('*.jpg'))
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def main():
    before=hashes()
    with Path('build/repeat.log').open('w') as f:
        subprocess.run(['python3','src/bank_fields.py','prepare'],stdout=f,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['python3','src/matches.py','--prepare'],stdout=f,stderr=subprocess.STDOUT,check=True)
        subprocess.run(shlex.split(os.environ.get('BLENDER','blender -t 1'))+['-b','--factory-startup','--python-exit-code','1',
            '--python','src/native_town.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
        subprocess.run(shlex.split(os.environ.get('BLENDER','blender -t 1'))+['-b','--factory-startup','--python-exit-code','1',
            '--python','src/build.py','--','--out','build/repeat.blend'],stdout=f,stderr=subprocess.STDOUT,check=True)
        if Path('build/delivery.json').exists():
            subprocess.run(['python3','src/delivery.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
    after=hashes();changed=[p for p in sorted(set(before)|set(after)) if after.get(p)!=before.get(p)]
    Path('build/repeat.json').write_text(json.dumps(dict(passed=not changed,files=len(before),changed=changed),indent=2)+'\n')
    if changed:raise ValueError(('Repeat mismatch',changed))
    print('RIVER_EXACT_REPEAT_PASS',len(before))


if __name__=='__main__':main()
