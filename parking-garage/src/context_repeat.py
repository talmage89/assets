"""Independently rebuild every local native context input, without GPU use."""
import hashlib,json,subprocess
from pathlib import Path
from dependencies import CONTEXT,LOCAL


def main():
    folder=Path('build/context-repeat');folder.mkdir(parents=True,exist_ok=True);rows=[]
    Path('build/context-repeat.json').unlink(missing_ok=True)
    for kind,(threads,expected) in CONTEXT.items():
        out=folder/(kind+'.glb')
        with (folder/(kind+'.log')).open('w') as log:
            subprocess.run(['blender','-t',str(threads),'-b','--factory-startup','--python-exit-code','1',
                '--python','src/context_build.py','--','--kind',kind,'--out',str(out)],cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
        canonical=Path('build/context')/(kind+'.glb')
        repeated=hashlib.sha256(out.read_bytes()).hexdigest();original=hashlib.sha256(canonical.read_bytes()).hexdigest()
        assert repeated==original==expected,(kind,original,repeated)
        rows.append(dict(kind=kind,threads=threads,bytes=out.stat().st_size,sha256=repeated,identical=True))
    Path('build/context-repeat.json').write_text(json.dumps(dict(passed=True,files=rows,scope='Independent native generators, full exported GLB bytes, no cached source mesh'),indent=2)+'\n')
    print('NATIVE CONTEXT REPEAT PASS',[(r['kind'],r['bytes']) for r in rows],flush=True)


if __name__=='__main__':main()
