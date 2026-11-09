"""Read-only library adapters; outputs are confined to school/build.

Accepted geometry/maps are reused where present. Missing local context is
rebuilt with the original generators. Existing library deliveries never change.
"""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'school'
sys.path.insert(0,str(ROOT))
from kit.blender_command import with_threads


def car_cache(kind,target,log_path):
    """Build only this native car; invalidate caches made before threads=1."""
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    policy=target.with_suffix('.threads')
    if target.exists() and policy.exists() and policy.read_text()=='1\n':return
    command=[os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python',str(ROOT/'downtown/src/context_build.py'),'--','--kind',kind,'--out',str(target)]
    with Path(log_path).open('w') as log:
        subprocess.run(with_threads(command,1),cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    policy.write_text('1\n')


def snapshot():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
      for family in ROOT.iterdir() if family.is_dir() and family.name not in ('school','.git','build')
      for p in family.rglob('*') if p.is_file() and any(x in ('export','textures','docs') for x in p.relative_to(family).parts)}


def main():
    out=LOCAL/'build';out.mkdir(exist_ok=True)
    preserve=out/'preservation.json'
    before=json.loads(preserve.read_text()) if preserve.exists() else snapshot()
    preserve.write_text(json.dumps(before,indent=2))
    # Follow the apartment dependency convention: invoke an original pipeline
    # only for a missing canonical input. Existing deliveries are never rebuilt
    # speculatively. Its own Make rules acquire the GPU lock for any bake.
    jobs=[('ground',[f'textures/ship/T_{n}_{c}.png' for n in ('Asphalt','Concrete','Lawn') for c in ('BaseColor','Normal','ORM')],['textures/ship/.stamp']),
          ('fences/chain-link',[f'textures/ship/T_ChainLink_{c}.png' for c in ('BaseColor','Normal','ORM')],['export/ChainLink.glb']),
          ('trees',['export/RedMaple.glb'],['export/RedMaple.glb']),
          ('trees',['export/PinOak.glb'],['SPECIES=oak','export/PinOak.glb'])]
    for family,required,args in jobs:
        if all((ROOT/family/name).exists() for name in required):continue
        with (out/('dependency-'+family.replace('/','-')+'-'+Path(required[0]).stem+'.log')).open('w') as log:
            subprocess.run(['make','-C',str(ROOT/family),*args,'BLENDER=blender -t 4'],stdout=log,stderr=subprocess.STDOUT,check=True)
    for family in ('ground','chain','furniture','light'):
        target=out/'context'/f'{family}.glb';target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():continue
        # Same adapter already used for the municipal park. This creates
        # school-owned modules from the unchanged library sources.
        cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'skatepark/src/context_build.py'),'--',family,'--out',str(target)]
        with (out/f'context-{family}.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    # Reuse the Commercial family bake, built by its unchanged original graph
    # only if a required canonical map is missing.
    if not all((ROOT/'commercial/textures/ship'/f'T_Commercial{r}_{c}.png').exists() for r in ('CMU','Brick','Concrete','Equipment') for c in ('BaseColor','Normal','ORM')):
        with (out/'dependency-commercial.log').open('w') as log:
            subprocess.run(['make','-C',str(ROOT/'commercial'),'textures','BLENDER=blender -t 4'],stdout=log,stderr=subprocess.STDOUT,check=True)
    if not all((ROOT/'houses/textures/ranch-ship'/f'T_RanchBrick_{kind}_{channel}.png').exists() for kind in ('buff','tan') for channel in ('BaseColor','Normal','ORM')):
        with (out/'dependency-buff-brick.log').open('w') as log:
            subprocess.run(['python3','src/ranch_bake.py','source','--size','4096'],cwd=ROOT/'houses',stdout=log,stderr=subprocess.STDOUT,check=True)
            subprocess.run([str(ROOT/'kit/with_gpu.sh'),os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(LOCAL/'src/bake_shared.py')],cwd=ROOT/'houses',stdout=log,stderr=subprocess.STDOUT,check=True)
            for kind in ('buff','tan'):
                if all((ROOT/'houses/textures/ranch-ship'/f'T_RanchBrick_{kind}_{channel}.png').exists() for channel in ('BaseColor','Normal','ORM')):continue
                subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source','textures/ranch-bake','--out','textures/ranch-ship','--asset','RanchBrick_'+kind,'--size','512'],cwd=ROOT/'houses',stdout=log,stderr=subprocess.STDOUT,check=True)
    for kind in ('houses','utility'):
        target=out/'context'/f'{kind}.glb'
        if not target.exists():
            cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/neighborhood_build.py','--',kind,'--out',str(target)]
            with (out/f'context-{kind}.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    for style,seed in (('ranch',41),('cape',53)):
        target=out/'context'/f'houses-{style}.glb'
        if not target.exists():
            cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/neighborhood_build.py','--','houses','--house-type',style,'--seed',str(seed),'--out',str(target)]
            with (out/f'context-houses-{style}.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    # Preserve the native source instance for presentation. The old form-only
    # GLB adapter remains rebuildable but is no longer used in the look views.
    target=out/'context/car.blend'
    car_cache('hatchback',target,out/'context-car.log')
    for kind in ('pickup','crossover'):
        target=out/'context'/('car-'+kind+'.blend')
        car_cache(kind,target,out/('context-'+kind+'.log'))
    target=out/'context/shrub/source.blend'
    if not target.exists():
        cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'apartments/src/context_build.py'),'--','shrub']
        with (out/'context-shrub.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    for kind in ('car','shrub'):
        target=out/'context'/f'{kind}.glb'
        if not target.exists() or target.stat().st_mtime<(LOCAL/'src/context_export.py').stat().st_mtime or (kind=='car' and target.stat().st_mtime<(out/'context/car.blend').stat().st_mtime):
            cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/context_export.py','--',kind]
            if kind=='car':cmd=with_threads(cmd,1)
            with (out/f'context-{kind}-export.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    # The analytic library shrub maps are shared delivery inputs, rather than
    # glTF dependencies on disposable source folders under build/.
    shared=LOCAL/'textures/checkpoint';shared.mkdir(parents=True,exist_ok=True)
    for image in (out/'context/shrub/shrubs/textures/analytic').glob('T_Shrubs_*.png'):
        target=shared/image.name
        if not target.exists() or target.read_bytes()!=image.read_bytes():target.write_bytes(image.read_bytes())
    after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h];assert not changed,changed
    (out/'dependencies.json').write_text(json.dumps(dict(preserved_files=len(before),passed=True,stage='form context; existing delivery byte preservation'),indent=2))

if __name__=='__main__':main()
