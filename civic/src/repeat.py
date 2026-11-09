"""Exact repeat of deterministic geometry/packages, retaining baked shared maps."""
import hashlib,json,os,subprocess
from pathlib import Path


def snapshot():
    family=json.loads(Path('build/family.json').read_text());paths=[]
    for row in family.values():
        path=Path(row['gltf']);paths.extend((path,path.with_suffix('.bin')))
        paths.extend((path.parent/im['uri']).resolve() for im in json.loads(path.read_text()).get('images',[]))
    paths.extend((Path('export/CivicPieces.gltf'),Path('export/CivicPieces.bin')))
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    before=snapshot();log=Path('build/repeat.log')
    with log.open('w') as f:subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
    after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h]
    result=dict(passed=not changed,files=len(before),changed=changed,scope='Exact glTF/BIN and canonical image repeat; geometry rebuilt in a clean Blender scene; shared GPU maps retained, not rebaked')
    Path('build/repeat.json').write_text(json.dumps(result,indent=2)+'\n');print('CIVIC REPEAT',result);assert result['passed'],changed


if __name__=='__main__':main()
