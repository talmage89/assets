"""Exact repeat of deterministic geometry/packages, retaining baked shared maps."""
import hashlib,json,os,subprocess,shutil,sys
from pathlib import Path


def snapshot():
    family=json.loads(Path('build/family.json').read_text());paths=[]
    for row in family.values():
        path=Path(row['gltf']);paths.extend((path,path.with_suffix('.bin')))
        paths.extend((path.parent/im['uri']).resolve() for im in json.loads(path.read_text()).get('images',[]))
    paths.extend((Path('export/CivicPieces.gltf'),Path('export/CivicPieces.bin')))
    paths.extend(Path('build/context').glob('*.glb'));paths.extend(Path('build/context').glob('*.json'))
    folder=Path('textures/shared/downtown/build')
    paths.extend(folder.glob('blocks/midwest/*.glb'));paths.extend(folder.glob('blocks/midwest/*.json'))
    paths.extend((folder/'town.json',Path('build/family.json'),Path('build/modules.json'),Path('build/dependencies.json')))
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    before=snapshot();log=Path('build/repeat.log')
    baseline=Path('build/repeat-before');baseline.mkdir(exist_ok=True)
    for path in Path('export').glob('*'):
        if path.suffix in ('.gltf','.bin'):shutil.copyfile(path,baseline/path.name)
    # Force all owned native adapters and the downtown presentation cache to
    # regenerate at the same paths; canonical library deliveries stay read-only.
    cache_before=Path('build/repeat-context-before');cache_before.mkdir(exist_ok=True)
    caches=list(Path('build/context').glob('*.glb'))+[Path('textures/shared/downtown/build/blocks/midwest/block.glb')]
    for path in caches:shutil.copyfile(path,cache_before/path.name);path.unlink()
    with Path('build/repeat-context.log').open('w') as f:
        subprocess.run([sys.executable,'src/prepare.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
    with log.open('w') as f:subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
    after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h]
    result=dict(passed=not changed,files=len(before),changed=changed,scope='Exact glTF/BIN, manifests, owned native context caches and canonical images; fresh serial Blender rebuilds; shared GPU maps retained and independently rebaked by check-texture-repeat. Native cars are read-only deliveries, not generated caches. Debug blends are not byte-stable runtime artifacts.')
    Path('build/repeat.json').write_text(json.dumps(result,indent=2)+'\n');print('CIVIC REPEAT',result);assert result['passed'],changed


if __name__=='__main__':main()
