"""Local-only original library rebuilds; preserve every existing delivery."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'parking-garage'
sys.path.insert(0,str(ROOT))
from kit.blender_command import with_threads
CONTEXT={
    'downtown':(2,'e5c9853c0e95981151e82c7742c73a91332bb3ce65a8061c59b3f9e46afdb0bc'),
    'commercial':(2,'d69066cbc85bb8bd64a82963792354fc3cd5c63afc5eae3ac8275efcff73d471'),
    'hatchback':(1,'18436abe2fbde7a2bcdcbe1ee45959dc7b48e6f8f291ca94b57250b39da892b4'),
    'crossover':(1,'a9926128e7b30cb24cdeba4d8203eaab317094b4cc5d24acc73877298f15d6ef'),
}


def snapshot():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for family in ROOT.iterdir() if family.is_dir() and family.name not in ('parking-garage','build','.git')
        for p in family.rglob('*') if p.is_file() and any(s in ('export','textures','docs') for s in p.relative_to(family).parts)}


def build_context(kind,folder,reuse=True):
    """Reject native outliers, never relax a threshold or substitute geometry.

    Each attempt runs the unchanged native recipe. Both rejected and accepted
    hashes/measurements survive; three failures stop the build.
    """
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    threads,expected=CONTEXT[kind];out=folder/(kind+'.glb');car=kind in ('hatchback','crossover');attempts=[]
    history_path=folder/(kind+'-history.json')
    history=json.loads(history_path.read_text()) if history_path.exists() else []
    policy=out.with_suffix('.threads')
    for attempt in range(3 if car else 1):
        audit=len(history)
        valid=reuse and out.exists() and (car or hashlib.sha256(out.read_bytes()).hexdigest()==expected)
        if car:valid=valid and policy.exists() and policy.read_text()=='1\n'
        if not valid:
            with (folder/f'{kind}-{audit}.log').open('w') as log:
                command=['blender','-t',str(threads),'-b','--factory-startup','--python-exit-code','1',
                    '--python',str(LOCAL/'src/context_build.py'),'--','--kind',kind,'--out',str(out)]
                if car:command=with_threads(command,1)
                subprocess.run(command,check=True,stdout=log,stderr=subprocess.STDOUT,cwd=LOCAL)
        actual=hashlib.sha256(out.read_bytes()).hexdigest()
        if not car:
            assert actual==expected,('Native town recipe differs',kind,actual,expected)
            return dict(kind=kind,threads=threads,bytes=out.stat().st_size,actual_sha256=actual,identical=True,passed=True)
        result=folder/f'{kind}-tolerance-{audit}.json'
        with (folder/f'{kind}-tolerance-{audit}.log').open('w') as log:
            worker=subprocess.run(['blender','-t','2','-b','--factory-startup','--python-exit-code','1',
                '--python','src/context_guard.py','--','--source',str(out),'--baseline',
                f'src/{kind}-surface.json','--out',str(result)],cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT)
        assert result.exists(),('Surface audit failed without a receipt',kind,worker.returncode)
        measured=json.loads(result.read_text());entry=dict(attempt=attempt,audit=audit,reused_cached=valid,**measured)
        attempts.append(entry);history.append(entry)
        history_path.write_text(json.dumps(history,indent=2)+'\n')
        (folder/(kind+'-attempts.json')).write_text(json.dumps(attempts,indent=2)+'\n')
        print('NATIVE INPUT',kind,'ACCEPT' if measured['passed'] else 'REJECT',measured,flush=True)
        if worker.returncode==0 and measured['passed']:
            policy.write_text('1\n')
            return dict(kind=kind,threads=threads,bytes=out.stat().st_size,history_receipt=str(history_path),attempts=attempts,**measured)
        rejected=folder/'rejected';rejected.mkdir(exist_ok=True)
        out.rename(rejected/f'{kind}-{audit}-{actual}.glb');reuse=False
    raise AssertionError(('Native context failed three fixed-tolerance attempts',kind,attempts))


def main():
    folder=LOCAL/'build/context';folder.mkdir(parents=True,exist_ok=True)
    receipt=LOCAL/'build/preservation.json'
    if not receipt.exists():receipt.write_text(json.dumps(snapshot(),indent=2)+'\n')
    rows=[build_context(kind,folder) for kind in CONTEXT]
    before=json.loads(receipt.read_text());after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h]
    assert not changed,changed
    (LOCAL/'build/dependencies.json').write_text(json.dumps(dict(preserved_files=len(before),passed=True,inputs=rows),indent=2)+'\n')


if __name__=='__main__':main()
