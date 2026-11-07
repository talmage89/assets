"""Rebuild the accepted look checkpoint from this clone's history, when absent.

Only our own tracked scripts are read. No other checkout is accessed. The
accepted bytes are retained under build/ for same-camera appearance evidence.
"""
from pathlib import Path
import hashlib,json,os,subprocess
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'skateboard';OUT=ASSET/'build/accepted';SCRIPTS=ASSET/'build/accepted-src'
REV='b0939d8'
def run(*args):subprocess.run(list(map(str,args)),cwd=ASSET,check=True)
OUT.mkdir(parents=True,exist_ok=True);SCRIPTS.mkdir(parents=True,exist_ok=True)
for name in ('build.py','spec.py','lookdev.py','graphics.py','prepare_low.py','config.py'):
    source=subprocess.check_output(['git','show',f'{REV}:skateboard/src/{name}'],cwd=ROOT,text=True)
    source=source.replace('ROOT=Path(__file__).resolve().parents[2]',"ROOT=next(p for p in Path(__file__).resolve().parents if (p/'kit/model.py').is_file())")
    source=source.replace("sys.path.insert(0,str(Path(__file__).resolve().parents[2]))","sys.path.insert(0,str(next(p for p in Path(__file__).resolve().parents if (p/'kit/model.py').is_file())))")
    (SCRIPTS/name).write_text(source)
blender=[os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python']
def blend(script,*args):
    run(ROOT/'kit/with_gpu.sh',*blender,script,'--',*args)
for state in ('season','beat'):
    export=OUT/'export'/f'{state}.glb'
    if export.exists():continue
    if not (OUT/'art/new-grip.png').exists():run('python3',SCRIPTS/'graphics.py','--out',OUT/'art')
    work=OUT/state;work.mkdir(parents=True,exist_ok=True)
    blend(SCRIPTS/'build.py','--state',state,'--out',work/'model.blend')
    blend(SCRIPTS/'prepare_low.py','--source',work/'model.blend','--out',work/'low.blend')
    blend(ROOT/'kit/finalize.py','--source',work/'low.blend','--out',work/'finalized.blend','--report',work/'uv.json','--config',SCRIPTS/'config.py','--size',2048,'--target-density',3000,'--margin',.002)
    blend(SCRIPTS/'lookdev.py','--source',work/'model.blend','--out',work/'high.blend','--palette',work/'palette.json','--art',OUT/'art')
    blend(ROOT/'kit/bake.py','--low',work/'finalized.blend','--high',work/'high.blend','--out',work/'bake','--asset','Skateboard','--config',SCRIPTS/'config.py','--size',4096,'--samples',24)
    run('python3',ROOT/'kit/downsample.py','--source',work/'bake','--out',OUT/'textures'/state,'--asset','Skateboard','--size',2048)
    blend(ROOT/'kit/export.py','--source',work/'finalized.blend','--textures',OUT/'textures'/state,'--out',export,'--asset','Skateboard','--config',SCRIPTS/'config.py','--report',work/'export.json')
(OUT/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT/'export').glob('*.glb')},indent=2))
print('Accepted checkpoint preserved/rebuilt:',REV)
