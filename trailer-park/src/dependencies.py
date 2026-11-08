"""Serial local native builds, plus immutable delivery snapshot."""
from pathlib import Path
import subprocess,hashlib,json,os,io,tarfile,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent


def ready(path):
    path=Path(path)
    if not path.is_file():return False
    if path.suffix!='.gltf':return True
    try:doc=json.loads(path.read_text())
    except (ValueError,OSError):return False
    return all(not row.get('uri') or row['uri'].startswith('data:') or (path.parent/row['uri']).is_file()
               for row in [*doc.get('images',[]),*doc.get('buffers',[])])


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
    jobs += [(f'houses/export/HearthfieldRanch-{seed}.gltf','houses',
              ['TYPE=ranch','RANCH_SEEDS=11,12,13,14,15,16'],['export']) for seed in range(11,17)]
    jobs.append(('commercial/export/CommercialGas-101.gltf','commercial',['SEEDS=101'],['export']))
    stage=ASSET/'build/library';missing=[j for j in jobs if not ready(ROOT/j[0])]
    if missing:
        stage.mkdir(parents=True,exist_ok=True)
        families=sorted({'kit',*[j[1].split('/')[0] for j in jobs]})
        absent=[family for family in families if not (stage/family).is_dir()]
        if absent:
            data=subprocess.check_output(['git','archive','HEAD',*absent],cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(stage,filter='data')
        # Transitive native builds resolve their own sibling paths in this
        # archive. Copy existing read-only inputs, never point a build at the
        # original outputs. Only absent private files are populated.
        for family in ('houses','ground','shrubs','trees','commercial'):
            for folder in ('export','textures/ship','textures/ranch-ship'):
                base=ROOT/family/folder
                if not base.is_dir():continue
                for source in base.rglob('*'):
                    if not source.is_file():continue
                    dest=stage/family/folder/source.relative_to(base)
                    if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    used={}
    for path,family,params,targets in jobs:
        selected=ROOT/path
        if not ready(selected):
            selected=stage/path
            if not ready(selected):
                with (stage/(family.replace('/','-')+'-export.log')).open('w') as log:
                    subprocess.run(['make','-j1',*params,*targets],cwd=stage/family,stdout=log,stderr=subprocess.STDOUT,check=True)
            if not ready(selected):raise FileNotFoundError(selected)
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
            commercial=ROOT/'commercial'
            if not (commercial/'textures/ship/graphics.json').is_file():commercial=ASSET/'build/library/commercial'
            link=stage/'textures'
            if link.is_symlink() and link.resolve()!=commercial/'textures':link.unlink()
            if not link.exists():link.symlink_to(commercial/'textures',target_is_directory=True)
            for family in ('ground','houses','shrubs','trees'):
                link=stage.parent/family
                source=ROOT/family
                relative=Path('textures/ship/T_HouseShingles_Normal.png') if family=='houses' else Path('export')/('Ground.glb' if family=='ground' else 'Shrubs.glb' if family=='shrubs' else 'RedMaple.glb')
                probe=source/relative
                if not probe.is_file():source=ASSET/'build/library'/family
                if link.is_symlink() and link.resolve()!=source:link.unlink()
                if not link.exists():link.symlink_to(source,target_is_directory=True)
            with (out/'strip.log').open('w') as log:
                subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python',str(commercial/'src/strip_build.py'),'--','--seeds','201','--out',str(out),'--look'],cwd=stage,stdout=log,stderr=subprocess.STDOUT,check=True)
            print('LOCAL NATIVE strip',flush=True);continue
        path=out/(kind+'.gltf')
        deps=list((ROOT/kind/'src').glob('*.py'))+[HERE/'native_build.py']
        if path.exists() and path.stat().st_mtime>=max(p.stat().st_mtime for p in deps):continue
        with (out/(kind+'.log')).open('w') as log:
            subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python',str(HERE/'native_build.py'),'--',kind],cwd=ASSET,stdout=log,stderr=subprocess.STDOUT,check=True)
        print('LOCAL NATIVE',kind,flush=True)
    Path('build/dependencies.json').write_text(json.dumps({str(p.relative_to(ASSET)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin','.png')},indent=2))

if __name__=='__main__':main()
