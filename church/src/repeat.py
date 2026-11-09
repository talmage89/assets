"""Deterministic own geometry/maps; native library files remain immutable."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent


def main():
    stage=ASSET/'build/repeat';shutil.rmtree(stage,ignore_errors=True);(stage/'build').mkdir(parents=True)
    log=ASSET/'build/repeat.log'
    with log.open('w') as out:
        subprocess.run([sys.executable,str(HERE/'textures.py')],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(HERE/'build.py'),'--','--no-sites'],cwd=stage,stdout=out,stderr=subprocess.STDOUT,check=True)
    compared=[];errors=[]
    for path in sorted((stage/'export').rglob('*.bin')):
        accepted=ASSET/path.relative_to(stage);same=path.read_bytes()==accepted.read_bytes()
        compared.append(dict(file=str(path.relative_to(stage)),bytes=path.stat().st_size,exact=same))
        if not same:errors.append(str(accepted))
    for path in (stage/'textures/ship').glob('*.png'):
        accepted=ASSET/path.relative_to(stage);same=path.read_bytes()==accepted.read_bytes()
        compared.append(dict(file=str(path.relative_to(stage)),bytes=path.stat().st_size,exact=same))
        if not same:errors.append(str(accepted))
    receipt=dict(passed=not errors,scope='Own church/range/module geometry BIN, analytic craft/glass/letter PNG and garden-summer lawn recipe/map bytes; imported car/tree inputs are covered by immutable library hashes, not regenerated here.',files=compared,errors=errors)
    (ASSET/'build/repeat.json').write_text(json.dumps(receipt,indent=2))
    assert not errors,errors
    print('PASS',len(compared),'deterministic geometry/map payloads,',sum(r['bytes'] for r in compared),'bytes')


if __name__=='__main__':main()
