"""Read-only library context generation, all outputs confined to utility/build."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent
OUT=ASSET/'build/context';OUT.mkdir(parents=True,exist_ok=True)


def snapshots():
    result={}
    for directory in ('houses','ground','trees','cars','street-light','commercial'):
        for folder in ('export','textures'):
            for p in (ROOT/directory/folder).rglob('*'):
                if p.is_file():result[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def prepare():
    before=snapshots();rows=[]
    jobs=[('houses/src/build.py',['--type',t,'--seed',str(s),'--out',str(OUT/(t+'.blend'))])
          for t,s in [('builder_colonial',27),('ranch',12),('cape',31),('split',51)]]
    jobs += [('utility/src/context_build.py',['--role','pickup','--out',str(OUT/'pickup.blend')]),
             ('street-light/src/build.py',['--quality','game','--out',str(OUT/'light.blend')]),
             ('trees/src/build.py',['--quality','game','--out',str(OUT/'maple.blend')]),
             ('utility/src/context_build.py',['--out',str(OUT/'ground.blend')])]
    for source,args in jobs:
        output=Path(args[args.index('--out')+1])
        dependency_folders=[ROOT/Path(source).parts[0]/'src']
        if output.stem in ('pickup','ground'):dependency_folders.append(ROOT/('cars' if output.stem=='pickup' else 'ground')/'src')
        signature=hashlib.sha256(b''.join(p.read_bytes() for folder in dependency_folders for p in sorted(folder.glob('*.py')))+str([x.replace(str(ASSET),'ASSET') for x in args]).encode()).hexdigest()
        receipt=output.with_suffix('.recipe')
        if not output.exists() or not receipt.exists() or receipt.read_text()!=signature:
            with (OUT/(output.stem+'.log')).open('w') as log:
                subprocess.run([os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python',str(ROOT/source),'--',*args],cwd=ASSET,stdout=log,stderr=subprocess.STDOUT,check=True)
            receipt.write_text(signature)
        rows.append(dict(script=source,output=str(output.relative_to(ASSET)),sha256=hashlib.sha256(output.read_bytes()).hexdigest()))
        print('CONTEXT',source,flush=True)
    after=snapshots();assert before==after,'An existing delivery changed'
    (ASSET/'build/context.json').write_text(json.dumps(dict(context=rows,preserved_files=before,byte_identical=True),indent=2))


if __name__=='__main__':prepare()
