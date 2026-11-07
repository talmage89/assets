"""Serial native-resolution correction renders and unchanged-camera pairs."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from render_batch import gpu_command,HERE
NAMES=['classic-hero','adventure-hero','adventure-above','waterfall','pond','tee','border']
def pairs():
 out=Path('renders/fixes');rows=[]
 for name in NAMES:
  before=Path('build/revision-before/lookdev')/(name+'.png');after=out/('after-'+name+'.png')
  if not before.exists() or not after.exists():continue
  a,b=Image.open(before).convert('RGB'),Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
  im=Image.new('RGB',(a.width*2,a.height+36),(230,230,220));im.paste(a,(0,36));im.paste(b,(a.width,36));d=ImageDraw.Draw(im);d.text((12,10),'4f39d4f / BEFORE',fill='black');d.text((a.width+12,10),'CORRECTION / EXTERNAL glTF',fill='black');im.save(out/(name+'-pair.jpg'),quality=94)
  rows.append(dict(name=name,before=str(before),after=str(after),panel_width=a.width,scope='Tee-relative unchanged camera' if name in ('tee','border') else 'Unchanged world camera and lighting'))
 Path('build/fix-crops.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--shots');p.add_argument('--samples',type=int,default=24);a=p.parse_args()
 chosen=a.shots.split(',') if a.shots else NAMES
 for seed in (71,92):
  names=[n for n in chosen if (71 if n.startswith('classic-') else 92)==seed]
  if not names:continue
  subprocess.run(gpu_command(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'fix_views.py'),'--','--shots',','.join(names),'--samples',str(a.samples)]),check=True)
 pairs()
