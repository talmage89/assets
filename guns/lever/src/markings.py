"""Original fictional rollmarks, rasterized from installed open-license fonts."""
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
for name,rows in [('receiver',['PROPANE DEFENSE','BRACKEN L20']),('barrel',['CAL. 30-30  /  PD L20']),('serial',['PD-L20-082147'])]:
 im=Image.new('L',(1024,256),0);draw=ImageDraw.Draw(im)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),64 if len(rows)>1 else 76)
 for i,text in enumerate(rows):
  box=draw.textbbox((0,0),text,font=font);draw.text(((1024-box[2])/2,22+i*108),text,font=font,fill=255)
 im.save(out/(name+'.png'))
