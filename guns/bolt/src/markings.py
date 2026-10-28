"""Original fictional markings, rasterized from installed Noto Sans."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
face=find_font('Noto Sans','Regular')
for name,rows in [('receiver-left',['PROPANE DEFENSE','VESPER  B24']),('receiver-right',['308 WIN','PD-B24-028417']),('scope',['PD OPTICS','4–16 × 44  /  FIELD SERIES'])]:
 im=Image.new('L',(1800,300));d=ImageDraw.Draw(im)
 for y,text,size in [(28,rows[0],86),(170,rows[1],64)]:
  d.text((900,y),text,font=ImageFont.truetype(face,size),anchor='mt',fill=255)
 im.save(out/(name+'.png'))
im=Image.new('L',(2400,300));d=ImageDraw.Draw(im)
for i in range(12):
 x=100+i*200;d.text((x,90),str(i),font=ImageFont.truetype(face,100),anchor='mm',fill=255)
 for k in range(4):
  t=x-90+k*50;d.line((t,205,t,280 if k==0 else 245),fill=255,width=6)
im.save(out/'turret.png')
im=Image.new('L',(1000,1000));font=ImageFont.truetype(face,86)
for text,start,end in [('PD  VESPER',205,335),('308  W',155,25)]:
 widths=[font.getlength(c) for c in text];total=sum(widths);advance=0
 for char,width in zip(text,widths):
  angle=start+(end-start)*(advance+width/2)/total;advance+=width
  glyph=Image.new('L',(150,150));ImageDraw.Draw(glyph).text((75,75),char,font=font,anchor='mm',fill=255)
  glyph=glyph.rotate(90-angle,resample=Image.Resampling.BICUBIC,expand=True)
  t=math.radians(angle);x=500+365*math.cos(t);y=500-365*math.sin(t)
  im.paste(glyph,(round(x-glyph.width/2),round(y-glyph.height/2)),glyph)
im.save(out/'headstamp.png')
