"""Native-pixel before/after comparisons; no resampling or invented detail."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib

def run():
 old=Path('../build/signals-before/checkpoint');new=Path('renders/checkpoint');out=Path('renders/form-fixes');out.mkdir(parents=True,exist_ok=True)
 cases={'intersection_201':'201/above','intersection_202':'202/above','intersection_203':'203/above','intersection_204':'204/above','setting':'201/hero','mast_cables':'201/head_lit','span_hanger_cables':'204/span_hanger','lit_lens':'201/head_lit','visor_doors':'201/head_dark','cabinet_interior':'201/cabinet_open'}
 rows=[]
 for label,rel in cases.items():
  a=Image.open(old/(rel+'.png')).convert('RGB');b=Image.open(new/(rel+'.png')).convert('RGB')
  # Both panels retain >=800 original pixels across. They can differ in
  # framing because the plan/camera are themselves part of the form fix.
  width=min(1100,a.width,b.width);panels=[]
  for im in (a,b):
   left=(im.width-width)//2;panels.append(im.crop((left,0,left+width,im.height)))
  h=max(p.height for p in panels);canvas=Image.new('RGB',(width*2,h+42),'#e7e8e4');d=ImageDraw.Draw(canvas)
  for i,(im,text) in enumerate(zip(panels,('Before / accepted checkpoint source pixels','After / exported shared-map game parts'))):canvas.paste(im,(i*width,42));d.text((i*width+10,12),text,fill='#22322c')
  canvas.save(out/(label+'.jpg'),quality=96,optimize=True)
  rows.append(dict(fix=label,before=str(old/(rel+'.png')),after=str(new/(rel+'.png')),crop_width_px=width,resampled=False))
 previous=old.parent/'matches/trenton-pair.jpg';current=Path('renders/matches/mast_sidewalk-pair.jpg')
 if previous.exists() and current.exists():
  panels=[Image.open(p).convert('RGB') for p in (previous,current)]
  width=max(im.width for im in panels);height=sum(im.height for im in panels)+84
  canvas=Image.new('RGB',(width,height),'#e7e8e4');d=ImageDraw.Draw(canvas);y=0
  for im,label in zip(panels,('Before / rejected New Jersey photo pairing','After / whole Oregon three-face installation fit')):
   d.text((10,y+12),label,fill='#22322c');canvas.paste(im,(0,y+42));y+=im.height+42
  canvas.save(out/'photo_pair_fit.jpg',quality=96,optimize=True)
  rows.append(dict(fix='photo_pair_fit',before=str(previous),after=str(current),crop_width_px=min(im.width for im in panels),resampled=False))
 (out/'provenance.json').write_text(json.dumps(rows,indent=2));print('FORM FIXES',len(rows),'native-pixel comparisons')
if __name__=='__main__':run()
