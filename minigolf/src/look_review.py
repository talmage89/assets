"""Local review contact sheets and tonal receipts; never writes docs/."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def contact(paths,dest,tile=600):
 paths=list(paths);width=tile*3;cell=round(tile*.72)+30;out=Image.new('RGB',(width,cell*((len(paths)+2)//3)),(224,224,215));d=ImageDraw.Draw(out)
 for i,p in enumerate(paths):
  im=Image.open(p).convert('RGB');im.thumbnail((tile,cell-30));x=i%3*tile;y=i//3*cell;out.paste(im,(x,y+30));d.text((x+7,y+7),p.stem,fill=(20,30,24))
 out.save(dest,quality=90)

def main():
 files=sorted(Path('renders/lookdev').glob('*.png'));assert files,'No GLB renders'
 contact(files,'renders/lookdev/contact.jpg');values={}
 for p in files:
  a=np.asarray(Image.open(p).convert('RGB'),dtype=float)/255;y=a@np.array([.2126,.7152,.0722]);meta=json.loads(p.with_suffix('.json').read_text());source=Path(meta['source']);assert source.suffix=='.glb' and meta['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
  values[p.stem]=dict(display_luma_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),white_clipped_fraction=float(np.mean(np.all(a>=.999,axis=-1))),camera=meta['camera'])
 Path('build/tonal-review.json').write_text(json.dumps(values,indent=2))
 pairs=list(Path('renders/look-matches').glob('*-pair.jpg'))
 if pairs:contact(pairs,'renders/look-matches/contact.jpg',800)
 compare=Path('renders/comparison');rows=[]
 for after in sorted(compare.glob('after-*.png')):
  before=after.with_name(after.name.replace('after-','before-',1))
  if not before.exists():continue
  a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
  sheet=Image.new('RGB',(a.width*2,a.height+40),(230,230,220));sheet.paste(a,(0,40));sheet.paste(b,(a.width,40));d=ImageDraw.Draw(sheet);d.text((12,10),'ACCEPTED CHECKPOINT / BEFORE',fill='black');d.text((a.width+12,10),'FORM + LOOK REVISION / AFTER',fill='black');sheet.save(compare/(after.stem.removeprefix('after-')+'-pair.jpg'),quality=93);rows.append(compare/(after.stem.removeprefix('after-')+'-pair.jpg'))
 if rows:contact(rows,compare/'contact.jpg',800)
 print('Review receipt',len(files),'GLB frames;',len(pairs),'photo pairs;',len(rows),'same-camera comparisons')
if __name__=='__main__':main()
