"""Read-only library adapters; outputs are confined to school/build.

Accepted geometry/maps are reused where present. Missing local context is
rebuilt with the original generators. Existing library deliveries never change.
"""
import hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'school'


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
    # The car family supplies the vehicle shape. Its original source nodes are
    # reduced to uniform form finishes in context_export, not baked here.
    target=out/'context/car.blend'
    if not target.exists():
        cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'downtown/src/context_build.py'),'--','--kind','hatchback','--out',str(target)]
        with (out/'context-car.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    target=out/'context/shrub/source.blend'
    if not target.exists():
        cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'apartments/src/context_build.py'),'--','shrub']
        with (out/'context-shrub.log').open('w') as log:subprocess.run(cmd,cwd=LOCAL,stdout=log,stderr=subprocess.STDOUT,check=True)
    for kind in ('car','shrub'):
        target=out/'context'/f'{kind}.glb'
        if not target.exists() or target.stat().st_mtime<(LOCAL/'src/context_export.py').stat().st_mtime:
            cmd=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/context_export.py','--',kind]
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
