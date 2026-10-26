"""Original municipal hot stamp and molded lid relief; never reference pixels."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.35);a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/TTF/DejaVuSans.ttf'
if not Path(FONT).exists():FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'
# Installed open-license font; all layout and text are original.
for name in ['city','lid']:
 im=Image.new('RGBA',(1536,768),(255,255,255,0));d=ImageDraw.Draw(im)
 def text(y,s,size):
  f=ImageFont.truetype(FONT,size);d.text((768,y),s,font=f,anchor='mt',fill=(160,162,153,255) if name=='city' else (255,255,255,255))
 if name=='city':
  text(85,'CITY OF',72);text(192,'ALDER CREEK',144)
  d.line((245,390,1291,390),fill='white',width=5)
  text(435,'PUBLIC WORKS',67);text(575,'AC 096-047281',83)
 else:
  text(10,'♻',480);text(550,'RECYCLING ONLY',70)
 im.save(out/(name+'.png'))
