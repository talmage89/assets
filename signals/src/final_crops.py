"""Requested fix evidence at native resolution, never upsampled."""
from pathlib import Path
import json
from PIL import Image,ImageDraw

def run():
 before=Path('../build/signals-finals-before/renders/checkpoint');after=Path('renders/checkpoint');out=Path('renders/final-fixes');out.mkdir(parents=True,exist_ok=True)
 cases=[('hero','201/hero','202/hero'),('asphalt','201/driver','201/driver'),('yellow','201/head_lit','201/head_lit'),('dark_lenses','201/head_dark','201/head_dark'),('dusk','201/dusk','202/dusk'),('cabinet_exterior','201/cabinet','201/cabinet'),('cabinet_interior','201/cabinet_open','201/cabinet_open'),('trees','201/driver','201/driver')]
 rows=[]
 for name,old,new in cases:
  source=before/(old+'.png');current=after/(new+'.png')
  if not source.exists():continue
  frames=[Image.open(p).convert('RGB') for p in (source,current)];width=min(im.width for im in frames);assert width>=800
  crops=[im.crop(((im.width-width)//2,0,(im.width+width)//2,im.height)) for im in frames]
  height=max(im.height for im in crops);canvas=Image.new('RGB',(width*2,height+40),'#dfe1dd');d=ImageDraw.Draw(canvas)
  for i,(im,label) in enumerate(zip(crops,('Before / accepted checkpoint / native pixels','After / exported finals / native pixels'))):canvas.paste(im,(i*width,40));d.text((i*width+12,12),label,fill='#1a2927')
  path=out/(name+'.jpg');canvas.save(path,quality=96,optimize=True)
  rows.append(dict(fix=name,before=str(source),after=str(current),crop_width=width,resampled=False,file=str(path),note='Hero/dusk compare two authored installations and revised cameras; material detail crops retain the original camera. This is visible outcome evidence, not a controlled light-only experiment.'))
 (out/'provenance.json').write_text(json.dumps(rows,indent=2));print('FINAL CROPS',len(rows),'native panels')
if __name__=='__main__':run()
