"""Read-only library context generation, all outputs confined to utility/build."""
import hashlib,json,os,subprocess,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent
OUT=ASSET/'build/context';OUT.mkdir(parents=True,exist_ok=True)


def file_sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def snapshots():
    result={}
    for directory in ('houses','ground','trees','cars','street-light','commercial'):
        for folder in ('export','textures'):
            for p in (ROOT/directory/folder).rglob('*'):
                if p.is_file():result[str(p.relative_to(ROOT))]=file_sha(p)
    return result


def prepare():
    before=snapshots();rows=[]
    # Every generated path is under this worktree's utility/build. Existing
    # public family exports may be absent; that is not a preservation proof.
    surface_stage=OUT/'house-surfaces';surface_stage.mkdir(parents=True,exist_ok=True)
    fields_receipt=surface_stage/'fields.recipe'
    fields_key=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'houses/src').glob('*.py')))).hexdigest()
    if not fields_receipt.exists() or fields_receipt.read_text()!=fields_key:
        with (OUT/'house-fields.log').open('w') as log:
            for args in (['source','--size','2048'],['filter-source']):
                subprocess.run(['python3',str(ROOT/'houses/src/bake_family.py'),*args],cwd=surface_stage,stdout=log,stderr=subprocess.STDOUT,check=True)
        fields_receipt.write_text(fields_key)
    ground_fields=OUT/'ground-fields'
    if not (ground_fields/'T_Asphalt_BaseColor.png').exists():
        with (OUT/'ground-fields.log').open('w') as log:
            subprocess.run(['python3',str(ROOT/'ground/src/textures.py'),'source','--out',str(ground_fields),'--size','2048'],stdout=log,stderr=subprocess.STDOUT,check=True)
    # The car's source finds generated markings beside its own code. A scratch
    # source copy keeps even those implicit paths inside utility/build.
    library=OUT/'library';car_source=library/'cars/src';car_source.mkdir(parents=True,exist_ok=True)
    for p in (ROOT/'cars/src').glob('*'):
        if p.is_file():shutil.copy2(p,car_source/p.name)
    if not (library/'kit').exists():(library/'kit').symlink_to(ROOT/'kit',target_is_directory=True)
    with (OUT/'car-markings.log').open('w') as log:
        subprocess.run(['python3',str(car_source/'markings.py'),str(library/'cars/build/markings')],stdout=log,stderr=subprocess.STDOUT,check=True)
    jobs=[('houses/src/build.py',['--type',t,'--seed',str(s),'--out',str(OUT/(t+'.blend'))])
          for t,s in [('builder_colonial',27),('ranch',12),('cape',31),('split',51)]]
    jobs += [('cars/src/build.py',['--quality','game','--out',str(OUT/'pickup.blend')]),
             ('street-light/src/build.py',['--quality','game','--out',str(OUT/'light.blend')]),
             ('trees/src/build.py',['--quality','game','--out',str(OUT/'maple.blend')]),
             ('trees/src/build.py',['--quality','game','--species','oak','--out',str(OUT/'oak.blend')]),
             ('utility/src/context_build.py',['--out',str(OUT/'ground.blend')])]
    for source,args in jobs:
        output=Path(args[args.index('--out')+1])
        dependency_folders=[ROOT/Path(source).parts[0]/'src']
        if output.stem in ('pickup','ground'):dependency_folders.append(ROOT/('cars' if output.stem=='pickup' else 'ground')/'src')
        signature=hashlib.sha256(b''.join(p.read_bytes() for folder in dependency_folders for p in sorted(folder.glob('*.py')))+str([x.replace(str(ASSET),'ASSET') for x in args]).encode()).hexdigest()
        receipt=output.with_suffix('.recipe')
        if not output.exists() or not receipt.exists() or receipt.read_text()!=signature:
            with (OUT/(output.stem+'.log')).open('w') as log:
                script=car_source/'build.py' if source=='cars/src/build.py' else ROOT/source
                subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(script),'--',*args],cwd=ASSET,stdout=log,stderr=subprocess.STDOUT,check=True)
            receipt.write_text(signature)
        rows.append(dict(script=source,output=str(output.relative_to(ASSET)),sha256=file_sha(output)))
        print('CONTEXT',source,flush=True)
    for typ in ('builder_colonial','ranch','cape','split'):
        output=OUT/(typ+'-look.blend');signature=hashlib.sha256((file_sha(OUT/(typ+'.blend'))+file_sha(HERE/'context_finish.py')+fields_key).encode()).hexdigest()
        receipt=output.with_suffix('.recipe')
        if not output.exists() or not receipt.exists() or receipt.read_text()!=signature:
            with (OUT/(typ+'-look.log')).open('w') as log:
                subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(HERE/'context_finish.py'),'--','--type',typ,'--source',str(OUT/(typ+'.blend')),'--out',str(output)],cwd=surface_stage,stdout=log,stderr=subprocess.STDOUT,check=True)
            receipt.write_text(signature)
        rows.append(dict(script='houses original look-development',output=str(output.relative_to(ASSET)),sha256=file_sha(output)))
    after=snapshots();assert before==after,'An existing delivery changed'
    (ASSET/'build/context.json').write_text(json.dumps(dict(context=rows,preserved_files=before,byte_identical=True),indent=2))


if __name__=='__main__':prepare()
