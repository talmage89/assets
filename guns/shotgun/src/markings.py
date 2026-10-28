"""Original fictional engraving sheets; installed open-license fonts only."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
fontpath=find_font('Noto Sans','Regular')
for name,rows in [('receiver-left',['PROPANE DEFENSE','HEARTH 12']),
                  ('receiver-right',['12 GA   2 3/4 & 3','PD-H12-061843'])]:
 im=Image.new('L',(1800,300));d=ImageDraw.Draw(im)
 for y,text,size in [(30,rows[0],85),(160,rows[1],64)]:
  font=ImageFont.truetype(fontpath,size);d.text((900,y),text,font=font,anchor='mt',fill=255,stroke_width=0)
 im.save(out/(name+'.png'))
# Text follows a circle, drawn character by character with actual font advances.
im=Image.new('L',(1000,1000));font=ImageFont.truetype(fontpath,80)
for text,start,end in [('PD  HEARTH',205,335),('12   12',155,25)]:
 widths=[font.getlength(c) for c in text];total=sum(widths);advance=0
 for char,width in zip(text,widths):
  angle=start+(end-start)*(advance+width/2)/total;advance+=width
  glyph=Image.new('L',(140,150));ImageDraw.Draw(glyph).text((70,75),char,font=font,anchor='mm',fill=255)
  glyph=glyph.rotate(90-angle,resample=Image.Resampling.BICUBIC,expand=True)
  t=math.radians(angle);x=500+365*math.cos(t);y=500-365*math.sin(t)
  im.paste(glyph,(round(x-glyph.width/2),round(y-glyph.height/2)),glyph)
im.save(out/'headstamp.png')
print('HEARTH ORIGINAL MARKINGS',fontpath)
