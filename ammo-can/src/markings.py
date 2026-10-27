"""Original fictional lot stencil, drawn with an installed open-license font."""
import argparse,random
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.35);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
im=Image.new('RGBA',(1200,440));d=ImageDraw.Draw(im);font=find_font('DejaVu Sans', 'Condensed Bold')
for text,y,size in [('100 CTG .50 CAL',8,102),('LINKED / FIELD',122,88),('LOT ACX-26H-041',224,84),('TYPE A-51',330,76)]:
 f=ImageFont.truetype(font,size);w=d.textlength(text,font=f);x=(1200-w)/2;d.text((x,y),text,font=f,fill=(197,181,85,255))
 for c in text:
  cw=d.textlength(c,font=f);cx=x+cw*.53;d.rectangle((cx-2,y,cx+2,y+size+10),fill=(0,0,0,0));x+=cw
rng=random.Random(51)
for _ in range(int(3000*a.wear)):
 x=rng.randrange(im.width);y=rng.randrange(im.height);d.rectangle((x,y,x+rng.randrange(1,7),y+rng.randrange(1,3)),fill=(0,0,0,0))
im.save(out/'lot.png')
