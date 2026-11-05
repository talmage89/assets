"""Before/after delivery fixes; accepted images have a verified historical source.

An existing accepted-round cache is validated byte for byte. A fresh checkout
can rebuild that cache from our own Git archive, using only current local kit
and immutable family deliveries. No other worktree is accessed.
"""
import argparse,hashlib,io,json,os,shutil,subprocess,tarfile,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from review import FONT
BASE='dba25d4'
CASES={'sunlight':('hero',(0,.12,1,.90)), 'paving':('above',(.15,.35,.85,.94)),
 'absorbed_oil':('asphalt',(0,0,1,1)), 'bark':('landscape',(.12,.40,.95,.95)),
 'impact_rust':('entry',(.53,.43,.73,.99)), 'diffusers':('canopy',(0,0,1,.78)),
 'runoff':('canopy',(0,.72,1,1)), 'blue_hour':('dusk',(0,0,1,1))}


def before(blender,width,samples):
 cache=HERE.parents[1]/'build/commercial-resume/accepted'
 required={shot for shot,roi in CASES.values()}
 if (cache/'manifest.json').exists():
  manifest=json.loads((cache/'manifest.json').read_text());assert manifest['commit']==BASE
  for shot in required:
   path=cache/'renders/look-checkpoint'/(shot+'.png');key=str(path.relative_to(cache))
   assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['files'][key]
  return cache/'renders/look-checkpoint'
 root=Path('build/accepted-history');root.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['git','-C',str(HERE.parents[1]),'archive',BASE,'commercial'])
 with tarfile.open(fileobj=io.BytesIO(data)) as tar:tar.extractall(root,filter='data')
 for family in ('kit','ground','houses','shrubs','trees'):
  path=root/family
  if not path.exists():path.symlink_to(os.path.relpath(HERE.parents[1]/family,path.parent),target_is_directory=True)
 old=root/'commercial';out=old/'renders/accepted'
 with Path('build/accepted-history.log').open('w') as log:
  subprocess.run(['make','SEEDS=101','export'],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
  subprocess.run([str(HERE.parents[1]/'kit/with_gpu.sh'),blender,'-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--source','export/CommercialGas-101.gltf','--out','renders/accepted','--shots',','.join(sorted(required)),'--width',str(width),'--samples',str(samples)],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
 return out


def main(a):
 old=before(a.blender,a.width,a.samples);folder=Path('renders/delivery-fixes');folder.mkdir(parents=True,exist_ok=True);rows=[]
 for name,(shot,roi) in CASES.items():
  paths=[old/(shot+'.png'),Path('renders/final')/(shot+'.png')];crops=[]
  for path in paths:
   im=Image.open(path).convert('RGB');w,h=im.size;box=tuple(round(v*(w if j%2==0 else h)) for j,v in enumerate(roi));crops.append(ImageOps.contain(im.crop(box),(780,800),Image.Resampling.LANCZOS))
  column=max(500,max(im.width for im in crops)+20);height=max(im.height for im in crops)+58
  canvas=Image.new('RGB',(column*2,height),'#e8e9e6');d=ImageDraw.Draw(canvas)
  for i,im in enumerate(crops):
   canvas.paste(im,(i*column+(column-im.width)//2,48));d.text((i*column+12,12),('Accepted previous look / ' if i==0 else 'Final export / ')+name,font=FONT,fill='#26352f')
  dst=folder/(name+'-before-after.jpg');canvas.save(dst,quality=94);rows.append(dict(case=name,shot=shot,crop=roi,source=[str(p) for p in paths],image_sha256=hashlib.sha256(dst.read_bytes()).hexdigest()))
 Path('build/revision-comparison.json').write_text(json.dumps(dict(baseline=BASE,rows=rows),indent=2));print('REVISION_COMPARISON',len(rows))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);main(p.parse_args())
