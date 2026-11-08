"""Serial local native builds, plus immutable delivery snapshot."""
from pathlib import Path
import subprocess,hashlib,json,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent


def main():
    out=ASSET/'build/native';out.mkdir(parents=True,exist_ok=True)
    for kind in ('shed','utility','playground'):
        path=out/(kind+'.gltf')
        deps=list((ROOT/kind/'src').glob('*.py'))+[HERE/'native_build.py']
        if path.exists() and path.stat().st_mtime>=max(p.stat().st_mtime for p in deps):continue
        with (out/(kind+'.log')).open('w') as log:
            subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python',str(HERE/'native_build.py'),'--',kind],cwd=ASSET,stdout=log,stderr=subprocess.STDOUT,check=True)
        print('LOCAL NATIVE',kind,flush=True)
    Path('build/dependencies.json').write_text(json.dumps({str(p.relative_to(ASSET)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin','.png')},indent=2))

if __name__=='__main__':main()
