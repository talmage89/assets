"""Rebuild original shared recipes locally; never alter another delivery."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'civic'


def snapshot():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for family in ROOT.iterdir() if family.is_dir() and family.name not in ('civic','build','.git')
        for p in family.rglob('*') if p.is_file() and any(s in ('export','textures','docs') for s in p.relative_to(family).parts)}


def run(cmd,cwd,log):
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w') as f:subprocess.run(list(map(str,cmd)),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)


def main():
    out=LOCAL/'build';out.mkdir(exist_ok=True)
    receipt=out/'preservation.json'
    if not receipt.exists():receipt.write_text(json.dumps(snapshot(),indent=2)+'\n')
    blender=os.environ.get('BLENDER','blender')
    # Missing commercial/downtown deliveries are generated into civic-owned
    # recipe folders. Identical original fields, bakes and filtering, no edits.
    for family in ('downtown','commercial'):
        folder=LOCAL/'textures/shared'/family;folder.mkdir(parents=True,exist_ok=True)
        script=ROOT/family/'src/textures.py'
        if not (folder/'textures/ship/textures.json').exists():
            if not (folder/'build/procedural/fields.json').exists():
                run([sys.executable,script,'source','--size','4096'],folder,out/f'{family}-source.log')
            run([ROOT/'kit/with_gpu.sh',blender,'-b','-t','4','--factory-startup','--python-exit-code','1','--python',script,'--','bake','--size','4096','--samples','1'],folder,out/f'{family}-bake.log')
            run([sys.executable,script,'ship'],folder,out/f'{family}-ship.log')
    context=out/'context';context.mkdir(exist_ok=True)
    # Context block uses the same baked maps, not the source fallback palette.
    town=LOCAL/'textures/shared/downtown'
    if not (town/'build/blocks/midwest/block.glb').exists():
        run([blender,'-b','-t','4','--factory-startup','--python-exit-code','1','--python',ROOT/'downtown/src/build.py','--','--seed','411','--region','midwest','--count','5','--out','build/town.blend'],town,out/'context-town.log')
    for kind,script,args in (
        ('house',ROOT/'school/src/neighborhood_build.py',['houses','--house-type','ranch','--seed','41']),
        ('utility',ROOT/'school/src/neighborhood_build.py',['utility']),
        ('furniture',ROOT/'skatepark/src/context_build.py',['furniture'])):
        target=context/(kind+'.glb')
        if target.exists():continue
        run([blender,'-b','-t','4','--factory-startup','--python-exit-code','1','--python',script,'--',*args,'--out',target],LOCAL,out/f'context-{kind}.log')
    before=json.loads(receipt.read_text());after=snapshot()
    changed=[p for p,h in before.items() if after.get(p)!=h]
    assert not changed,changed
    (out/'dependencies.json').write_text(json.dumps(dict(preserved_files=len(before),passed=True),indent=2)+'\n')


if __name__=='__main__':main()
