"""Rejected correction ledger and contacts; never produces final docs."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from external import bundle
from fix_batch import NAMES

def contact(paths,dest,tile=600):
 paths=list(paths);cell=round(tile*.72)+30;out=Image.new('RGB',(tile*3,cell*((len(paths)+2)//3)),(224,224,215));d=ImageDraw.Draw(out)
 for i,path in enumerate(paths):
  im=Image.open(path).convert('RGB');im.thumbnail((tile,cell-30));x=i%3*tile;y=i//3*cell;out.paste(im,(x,y+30));d.text((x+7,y+7),path.stem,fill=(20,30,24))
 out.save(dest,quality=90)

def main():
 folder=Path('renders/fixes');files=[folder/('after-'+name+'.png') for name in NAMES];values={}
 for path in files:
  meta=json.loads(path.with_suffix('.json').read_text());assert meta['sha256']==bundle(meta['source']) and meta['engine']=='CYCLES',(path,'stale external export')
  image=Image.open(path).convert('RGB');assert image.width>=800
  pixels=np.asarray(image,float)/255;y=pixels@np.array([.2126,.7152,.0722]);values[path.stem]=dict(source=meta['source'],sha256=meta['sha256'],width=image.width,luma_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),white_clipped_fraction=float(np.mean(np.all(pixels>=.999,axis=-1))))
 pairs=sorted(folder.glob('*-pair.jpg'))
 for path in pairs:assert Image.open(path).width>=1600
 contact(pairs,folder/'contact.jpg',800)
 photos=[Path('renders/look-matches')/(key+'-pair.jpg') for key in ('period_classic_green','period_castle')]
 for key,path in zip(('period_classic_green','period_castle'),photos):
  meta=json.loads(path.with_name(key+'.json').read_text());assert meta['sha256']==bundle(meta['source']) and Image.open(path).width>=1600
 contact(photos,Path('renders/look-matches/contact.jpg'),800)
 Path('build/tonal-review.json').write_text(json.dumps(values,indent=2))
 report=dict(accepted=False,reason='Rock, waterfall and adventure terrain still fail native-size photographic critique; carpet nap and classic reference framing remain weak.',export_frames=len(files),native_panel_width=1440,comparison_pairs=len(pairs),current_photo_pairs=2,lighthouse_photo_rejected_for_occlusion=True,finals_generated=False,docs_generated=False,values=values)
 Path('build/render-check.json').write_text(json.dumps(report,indent=2));print('CORRECTION REVIEW: REJECTED;',len(files),'external-export frames;',len(pairs),'before/after pairs; 2 photo pairs; no finals/docs')
if __name__=='__main__':main()
