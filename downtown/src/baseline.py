"""Reproduce the accepted caf80a6 cameras and exported appearance locally.

Historical scripts are read from our own git history. Only generated context,
references and source libraries are reused; no other delivery is rebuilt.
"""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1440);a=p.parse_args()
REVISION='caf80a6'
CASES={'midwest':('corner','storefront','ghost','cornice_profile','hero','dusk'),'northeast':('foster','iron_detail')}
out=Path('build/accepted-workspace');source=out/'downtown';source.mkdir(parents=True,exist_ok=True)
needed=[source/'renders'/('matches' if r=='northeast' else 'checkpoint')/r/(n+'.png') for r,names in CASES.items() for n in names]
if all(f.exists() and Image.open(f).width==a.width for f in needed):
 print('BEFORE retained accepted native evidence');sys.exit(0)
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',REVISION,'--','downtown/src','downtown/Makefile'],cwd=ROOT,text=True).splitlines()
for name in paths:
 target=out/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(subprocess.check_output(['git','show',REVISION+':'+name],cwd=ROOT))
for folder in ROOT.iterdir():
 if folder.is_dir() and folder.name not in ('downtown','build','.git'):
  link=out/folder.name
  if not link.exists():link.symlink_to(os.path.relpath(folder,link.parent),target_is_directory=True)
ref=source/'refs'
if not ref.exists():ref.symlink_to(os.path.relpath(Path('refs').resolve(),ref.parent),target_is_directory=True)
# These original context files are generated from unchanged source recipes.
if Path('build/context').exists():
 shutil.copytree('build/context',source/'build/context',dirs_exist_ok=True,ignore=shutil.ignore_patterns('blocks'))
def run(cmd,label):
 with (out/(label+'.log')).open('w') as log:subprocess.run(cmd,cwd=source,stdout=log,stderr=subprocess.STDOUT,check=True)
run(['make','BLENDER='+str(ROOT/'downtown/src/blender.sh'),'model','context'],'build')
for r,names in CASES.items():
 if r=='northeast':
  run([sys.executable,'src/matches.py'],'cameras')
  from proof_cameras import iron_detail
  path=source/'build/cameras.json';cameras=json.loads(path.read_text());cameras['iron_detail']=iron_detail();path.write_text(json.dumps(cameras,indent=2))
  extra=['--camera-file','build/cameras.json'];folder='renders/matches'
 else:extra=[];folder='renders/checkpoint'
 run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--region',r,'--shots',','.join(names),'--out',folder,'--width',str(a.width),'--samples','32',*extra],r)
assert all(f.exists() and Image.open(f).width==a.width for f in needed)
print('BEFORE rebuilt accepted source, maps, exports and eight native views',REVISION)
