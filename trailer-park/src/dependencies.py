"""Serial local native builds, plus immutable delivery snapshot."""
from pathlib import Path
import subprocess,hashlib,json,os,io,tarfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent


def canonical_inputs():
    """Missing native deliveries rebuild in an isolated source archive.

    A cold clone may spend time on the original families' GPU bakes. Warm
    accepted deliveries are never regenerated or opened for writing.
    """
    jobs=[('ground/export/Ground.glb','ground',[],['export/Ground.glb']),
          ('houses/export/Hearthfield-2.gltf','houses',['SEEDS=2,27'],['export']),
          ('houses/export/Hearthfield-27.gltf','houses',['SEEDS=2,27'],['export']),
          ('trees/export/RedMaple.glb','trees',[],['export/RedMaple.glb']),
          ('trees/export/PinOak.glb','trees',['SPECIES=oak'],['export/PinOak.glb']),
          ('shrubs/export/Shrubs.glb','shrubs',[],['export/Shrubs.glb']),
          ('fences/export/WoodPrivacy.glb','fences',[],['export/WoodPrivacy.glb']),
          ('fences/chain-link/export/ChainLink.glb','fences/chain-link',[],['export/ChainLink.glb']),
          ('mailbox/export/Mailbox.glb','mailbox',[],['export/Mailbox.glb']),
          ('trash-cart/export/TrashCart.glb','trash-cart',[],['export/TrashCart.glb']),
          ('patio-set/export/PatioSet.glb','patio-set',[],['export/PatioSet.glb']),
          ('gas-grill/export/GasGrill.glb','gas-grill',[],['export/GasGrill.glb']),
          ('cars/export/AlderC150.glb','cars',['BODY=pickup'],['export/AlderC150.glb']),
          ('cars/export/AlderX220.glb','cars',['BODY=suv'],['export/AlderX220.glb']),
          ('cars/export/AlderH120.glb','cars',['BODY=hatch'],['export/AlderH120.glb'])]
    stage=ASSET/'build/library';missing=[j for j in jobs if not (ROOT/j[0]).is_file()]
    if missing and not (stage/'kit').exists():
        stage.mkdir(parents=True,exist_ok=True)
        families=sorted({'kit',*[j[1].split('/')[0] for j in jobs]})
        data=subprocess.check_output(['git','archive','HEAD',*families],cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(stage,filter='data')
    used={}
    for path,family,params,targets in jobs:
        selected=ROOT/path
        if not selected.exists():
            selected=stage/path
            if not selected.exists():
                with (stage/(family.replace('/','-')+'-export.log')).open('w') as log:
                    subprocess.run(['make','-j1',*params,*targets],cwd=stage/family,stdout=log,stderr=subprocess.STDOUT,check=True)
            if not selected.exists():raise FileNotFoundError(selected)
        used[path]=dict(resolved=str(selected.relative_to(ROOT)),sha256=hashlib.sha256(selected.read_bytes()).hexdigest())
    (ASSET/'build/library-inputs.json').write_text(json.dumps(used,indent=2))


def main():
    out=ASSET/'build/native';out.mkdir(parents=True,exist_ok=True)
    canonical_inputs()
    for kind in ('shed','utility','playground','strip'):
        if kind=='strip':
            path=out/'strip-201.glb'
            if path.exists():continue
            stage=ASSET/'build/commercial-context';stage.mkdir(parents=True,exist_ok=True)
            if not (stage/'textures').exists():(stage/'textures').symlink_to(ROOT/'commercial/textures',target_is_directory=True)
            for family in ('ground','houses','shrubs','trees'):
                link=stage.parent/family
                if not link.exists():link.symlink_to(ROOT/family,target_is_directory=True)
            with (out/'strip.log').open('w') as log:
                subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python',str(ROOT/'commercial/src/strip_build.py'),'--','--seeds','201','--out',str(out),'--look'],cwd=stage,stdout=log,stderr=subprocess.STDOUT,check=True)
            print('LOCAL NATIVE strip',flush=True);continue
        path=out/(kind+'.gltf')
        deps=list((ROOT/kind/'src').glob('*.py'))+[HERE/'native_build.py']
        if path.exists() and path.stat().st_mtime>=max(p.stat().st_mtime for p in deps):continue
        with (out/(kind+'.log')).open('w') as log:
            subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python',str(HERE/'native_build.py'),'--',kind],cwd=ASSET,stdout=log,stderr=subprocess.STDOUT,check=True)
        print('LOCAL NATIVE',kind,flush=True)
    Path('build/dependencies.json').write_text(json.dumps({str(p.relative_to(ASSET)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin','.png')},indent=2))

if __name__=='__main__':main()
