"""Local-only original library rebuilds; preserve every existing delivery."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'parking-garage'
CONTEXT={
    'downtown':(2,'e5c9853c0e95981151e82c7742c73a91332bb3ce65a8061c59b3f9e46afdb0bc'),
    'commercial':(2,'d69066cbc85bb8bd64a82963792354fc3cd5c63afc5eae3ac8275efcff73d471'),
    'hatchback':(4,'18436abe2fbde7a2bcdcbe1ee45959dc7b48e6f8f291ca94b57250b39da892b4'),
    'crossover':(4,'a9926128e7b30cb24cdeba4d8203eaab317094b4cc5d24acc73877298f15d6ef'),
}


def snapshot():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for family in ROOT.iterdir() if family.is_dir() and family.name not in ('parking-garage','build','.git')
        for p in family.rglob('*') if p.is_file() and any(s in ('export','textures','docs') for s in p.relative_to(family).parts)}


def main():
    folder=LOCAL/'build/context';folder.mkdir(parents=True,exist_ok=True)
    receipt=LOCAL/'build/preservation.json'
    if not receipt.exists():receipt.write_text(json.dumps(snapshot(),indent=2)+'\n')
    for kind,(threads,expected) in CONTEXT.items():
        out=folder/(kind+'.glb')
        if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()==expected:continue
        # Use an explicit evaluation profile: near-degenerate native gauge
        # topology is sensitive to worker count. Accepted hashes also prevent
        # silently replacing a historical input when its recipe diverges.
        with (folder/(kind+'.log')).open('w') as log:
            subprocess.run(['blender','-t',str(threads),'-b','--factory-startup','--python-exit-code','1',
                '--python',str(LOCAL/'src/context_build.py'),'--','--kind',kind,'--out',str(out)],check=True,stdout=log,stderr=subprocess.STDOUT,cwd=LOCAL)
        actual=hashlib.sha256(out.read_bytes()).hexdigest()
        assert actual==expected,('Native recipe does not reproduce accepted input',kind,actual,expected)
    before=json.loads(receipt.read_text());after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h]
    assert not changed,changed
    (LOCAL/'build/dependencies.json').write_text(json.dumps(dict(preserved_files=len(before),passed=True),indent=2)+'\n')


if __name__=='__main__':main()
