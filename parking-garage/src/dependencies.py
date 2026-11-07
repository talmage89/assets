"""Local-only original library rebuilds; preserve every existing delivery."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'parking-garage'


def snapshot():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for family in ROOT.iterdir() if family.is_dir() and family.name not in ('parking-garage','build','.git')
        for p in family.rglob('*') if p.is_file() and any(s in ('export','textures','docs') for s in p.relative_to(family).parts)}


def main():
    folder=LOCAL/'build/context';folder.mkdir(parents=True,exist_ok=True)
    receipt=LOCAL/'build/preservation.json'
    if not receipt.exists():receipt.write_text(json.dumps(snapshot(),indent=2)+'\n')
    for kind in ('downtown','commercial','hatchback','crossover'):
        out=folder/(kind+'.glb')
        if out.exists():continue
        with (folder/(kind+'.log')).open('w') as log:
            subprocess.run([str(LOCAL/'src/blender.sh'),'-b','--factory-startup','--python-exit-code','1',
                '--python',str(LOCAL/'src/context_build.py'),'--','--kind',kind,'--out',str(out)],check=True,stdout=log,stderr=subprocess.STDOUT,cwd=LOCAL)
    before=json.loads(receipt.read_text());after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h]
    assert not changed,changed
    (LOCAL/'build/dependencies.json').write_text(json.dumps(dict(preserved_files=len(before),passed=True),indent=2)+'\n')


if __name__=='__main__':main()
