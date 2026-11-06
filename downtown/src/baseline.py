"""Rebuild native before crops from the accepted 889d811 source when absent.

No second worktree is touched. The six review views live inside build/before;
only the historical downtown scripts and a read-only kit symlink are staged.
Caller holds the shared GPU lock for all child Blender processes.
"""
import argparse,json,os,subprocess,sys
from PIL import Image
p=argparse.ArgumentParser();p.add_argument("--width",type=int,default=1440);args=p.parse_args()
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
needed=['checkpoint/midwest/'+n+'.png' for n in ('storefront','window','cornice','corner','rear')]+['matches/northeast/foster.png']
out=Path('build/before');out.mkdir(parents=True,exist_ok=True)
if all((out/'renders'/p).exists() and Image.open(out/'renders'/p).width==args.width for p in needed):
 print('BEFORE existing native checkpoint evidence retained');sys.exit(0)
source=Path('build/baseline/downtown/src');source.mkdir(parents=True,exist_ok=True)
paths=subprocess.check_output(['git','ls-tree','-r','--name-only','889d811','--','downtown/src'],cwd=ROOT,text=True).splitlines()
for p in paths:
 if p.endswith('.py'):(source/Path(p).name).write_bytes(subprocess.check_output(['git','show','889d811:'+p],cwd=ROOT))
link=source.parents[1]/'kit'
if not link.exists():link.symlink_to(os.path.relpath(ROOT/'kit',link.parent),target_is_directory=True)
refs=out/'refs'
if not refs.exists():refs.symlink_to(os.path.relpath(Path('refs').resolve(),refs.parent),target_is_directory=True)
def call(script,args,name):
 with (out/(name+'.log')).open('w') as log:subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str((source/script).resolve()),'--',*args],cwd=out,stdout=log,stderr=subprocess.STDOUT,check=True)
call('build.py',['--out','build/downtown.blend'],'model')
call('render.py',['--region','midwest','--shots','storefront,window,cornice,corner,rear','--out','renders/checkpoint','--width',str(args.width),'--samples','32'],'midwest')
with (out/'camera.log').open('w') as log:subprocess.run([sys.executable,str((source/'matches.py').resolve())],cwd=out,stdout=log,stderr=subprocess.STDOUT,check=True)
call('render.py',['--region','northeast','--shots','foster','--camera-file','build/cameras.json','--out','renders/matches','--width',str(args.width),'--samples','32'],'foster')
assert all((out/'renders'/p).exists() and Image.open(out/'renders'/p).width==args.width for p in needed)
print('BEFORE rebuilt six native historical views from 889d811')
