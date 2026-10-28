"""Original stamps and mold legend from installed open-license Noto Sans."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
face=find_font('Noto Sans','Regular')
for name,rows in [('receiver',['PROPANE DEFENSE','RELAY 9     9×19']),('serial',['PD-R9-063218']),('lower',['PD  /  RELAY'])]:
 im=Image.new('L',(2048,360));d=ImageDraw.Draw(im)
 for i,text in enumerate(rows):d.text((1024,45+i*155),text,font=ImageFont.truetype(face,105),anchor='mt',fill=255)
 im.save(out/(name+'.png'))
im=Image.new('L',(1024,1024));font=ImageFont.truetype(face,80)
for text,start,end in [('PD RELAY',205,335),('9 × 19',155,25)]:
 widths=[font.getlength(c) for c in text];total=sum(widths);advance=0
 for char,width in zip(text,widths):
  angle=start+(end-start)*(advance+width/2)/total;advance+=width
  glyph=Image.new('L',(150,150));ImageDraw.Draw(glyph).text((75,75),char,font=font,anchor='mm',fill=255)
  glyph=glyph.rotate(90-angle,resample=Image.Resampling.BICUBIC,expand=True)
  t=math.radians(angle);x=512+350*math.cos(t);y=512-350*math.sin(t)
  im.paste(glyph,(round(x-glyph.width/2),round(y-glyph.height/2)),glyph)
im.save(out/'headstamp.png')
