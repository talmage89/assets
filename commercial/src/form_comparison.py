"""Rebuild the accepted historical form locally, then compare fixed cameras.

The old scripts come from this repository's own Git history, never another
worktree. Temporary historical sources and symlinks stay under build/.
"""
import argparse,hashlib,io,json,os,shutil,subprocess,tarfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import sys
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.fonts import find_font
BASELINE='d8ba99e'
CASES={'shrubs':('landscape',(.10,.22,.90,.95)),
       'hose':('dispenser',(.08,.05,.65,1.0)),
       'store_front':('entry',(0,0,1,1)),
       'services':('services',(0,0,1,1)),
       'price_base':('sign',(.05,.56,.97,1.0)),
       'column_wrap':('column',(.05,.02,.96,1.0)),
       'rear_wall':('rear',(0,.18,1,.97))}


def baseline(blender):
 folder=Path('build/form-before');source=folder/'station-101.glb';record=folder/'baseline.json'
 if source.exists() and record.exists():return source
 destination=Path('build/historical-form');destination.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['git','-C',str(HERE.parents[1]),'archive',BASELINE,'commercial'])
 with tarfile.open(fileobj=io.BytesIO(data)) as tar:tar.extractall(destination,filter='data')
 repo=HERE.parents[1]
 for name in ('kit','ground'):
  target=destination/name
  if not target.exists():target.symlink_to(os.path.relpath(repo/name,target.parent),target_is_directory=True)
 historical=destination/'commercial';(historical/'build').mkdir(exist_ok=True)
 with Path('build/historical-form.log').open('w') as log:
  subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--seeds','101'],cwd=historical,stdout=log,stderr=subprocess.STDOUT,check=True)
 folder.mkdir(parents=True,exist_ok=True)
 for suffix in ('.glb','.json'):shutil.copyfile(historical/'build'/('station-101'+suffix),folder/('station-101'+suffix))
 record.write_text(json.dumps(dict(commit=BASELINE,archive_sha256=hashlib.sha256(data).hexdigest(),glb_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Own accepted historical scripts, built in this worktree build folder; current compatible kit/ground helpers'),indent=2))
 return source


def main(a):
 source=baseline(a.blender);out=Path('renders/form-before');names=','.join(dict.fromkeys(r[0] for r in CASES.values()))
 from context import recipe
 provenance=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {}
 digest=hashlib.sha256(source.read_bytes()).hexdigest()
 need=not all((out/(n+'.png')).exists() and (r:=provenance.get(n,{})).get('sha256')==digest and r.get('recipe_sha256')==recipe() and r.get('width')==a.width and r.get('samples')==a.samples for n in names.split(','))
 if need:
  cmd=[str(HERE.parents[1]/'kit/with_gpu.sh'),a.blender,'-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--source',str(source),'--out',str(out),'--shots',names,'--width',str(a.width),'--samples',str(a.samples)]
  with Path('build/form-before-render.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
 font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),21);rows=[];folder=Path('renders/form-fixes');folder.mkdir(parents=True,exist_ok=True)
 for name,(shot,roi) in CASES.items():
  paths=[out/(shot+'.png'),Path('renders/look-checkpoint')/(shot+'.png')];canvas=Image.new('RGB',(1600,670),(233,234,231));d=ImageDraw.Draw(canvas)
  for i,path in enumerate(paths):
   im=Image.open(path).convert('RGB');w,h=im.size;box=tuple(round(v*(w if j%2==0 else h)) for j,v in enumerate(roi));im=ImageOps.contain(im.crop(box),(780,610),Image.Resampling.LANCZOS)
   canvas.paste(im,(i*800+(800-im.width)//2,45+(610-im.height)//2));d.text((i*800+12,12),('Before / accepted form' if i==0 else 'After / exported shared PBR')+' / '+name,font=font,fill=(30,35,31))
  target=folder/(name+'-before-after.jpg');canvas.save(target,quality=94);rows.append(dict(case=name,shot=shot,normalized_crop=roi,images=[str(p) for p in paths],output=str(target)))
 Path('build/form-comparison.json').write_text(json.dumps(dict(baseline=BASELINE,rows=rows),indent=2));print('FORM_COMPARISON',len(rows),'fixed-camera before/after crops')


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--blender',default='blender');a.add_argument('--width',type=int,default=1440);a.add_argument('--samples',type=int,default=40);main(a.parse_args())
