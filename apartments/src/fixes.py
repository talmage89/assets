"""Native-pixel handoff/current plates; each side at least 800 px wide."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
rows={
 'brick-bands-and-stair-bay':('checkpoint/Complex-301/hero.png','renders/checkpoint/Complex-301/hero.png'),
 'continuous-mansard':('checkpoint/Complex-302/ground.png','renders/checkpoint/Complex-302/ground.png'),
 'row-depth-and-mansard':('checkpoint/Row-401/hero.png','renders/checkpoint/Row-401/hero.png'),
 'projecting-garage-bays':('checkpoint/Row-403/hero.png','renders/checkpoint/Row-403/hero.png'),
 'matched-recessed-type':('matches/used-garden.png','renders/matches/used-garden.png')}
out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True);receipt={}
for key,(old,new) in rows.items():
 a=Image.open(Path('build/handoff')/old).convert('RGB');b=Image.open(new).convert('RGB')
 width=min(a.width,b.width);assert width>=800
 # Preserve one native pixel per output pixel. Crops are centered; neither
 # handoff nor current witness is upsampled to manufacture missing detail.
 crops=[]
 for im in (a,b):
  left=(im.width-width)//2;crops.append(im.crop((left,0,left+width,im.height)))
 height=max(im.height for im in crops);canvas=Image.new('RGB',(width*2,height+32),(232,232,225));draw=ImageDraw.Draw(canvas)
 for x,title,im in ((0,'Handoff / original pixels',crops[0]),(width,'Current exported PBR / original pixels',crops[1])):draw.text((x+12,9),title,fill=(25,28,24));canvas.paste(im,(x,32))
 canvas.save(out/(key+'-before-after.jpg'),quality=94,optimize=True)
 receipt[key]=dict(before=str(Path('build/handoff')/old),after=new,crop_width_px=width,resampled=False)
(out/'crops.json').write_text(json.dumps(receipt,indent=2))
