"""Original quick checkpoint graphics. No reference pixels are read."""
from pathlib import Path
import math,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from plan import NAMES
FONT=find_font('DejaVu Sans','Bold')
TILES=['red','yellow','green','red_arrow','yellow_arrow','green_arrow','hand','walk']
def generate(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 im=Image.new('RGBA',(1024,512),(0,0,0,0))
 colors=[(255,1,0),(255,120,0),(0,255,75),(255,1,0),(255,120,0),(0,255,75),(255,108,2),(245,255,247)]
 for j,kind in enumerate(TILES):
  mask=Image.new('L',(256,256));d=ImageDraw.Draw(mask)
  if 'arrow' in kind:
   d.polygon([(24,128),(110,48),(110,96),(222,96),(222,157),(110,157),(110,207)],fill=255)
  elif kind=='hand':
   d.rounded_rectangle((90,102,175,211),25,fill=255)
   for x,top in [(82,62),(107,31),(132,23),(157,43)]:d.rounded_rectangle((x,top,x+20,149),9,fill=255)
   d.polygon([(95,151),(52,109),(39,118),(78,193),(110,215)],fill=255)
  elif kind=='walk':
   d.ellipse((111,19,150,58),fill=255)
   d.line([(123,75),(101,136),(142,178),(165,232)],fill=255,width=24)
   d.line([(108,130),(84,186),(60,230)],fill=255,width=24)
   d.line([(116,83),(76,112),(47,146)],fill=255,width=16)
   d.line([(119,86),(163,117),(204,125)],fill=255,width=16)
  else:d.ellipse((8,8,248,248),fill=255)
  dots=Image.new('RGBA',(256,256));dd=ImageDraw.Draw(dots)
  for y in range(10,250,9):
   for x in range(10+(4 if (y//9)%2 else 0),250,9):
    if mask.getpixel((x,y))>0:
     dd.ellipse((x-3,y-3,x+3,y+3),fill=(*colors[j],255))
  if j<6:
   # A continuous dark optical cover reflects the sky between LED packages.
   # Only emission is dotted; opacity is the full nominal circular lens.
   opacity=Image.new('L',(256,256));ImageDraw.Draw(opacity).ellipse((0,0,255,255),fill=255);dots.putalpha(opacity)
  im.alpha_composite(dots,((j%4)*256,(j//4)*256))
 im.save(out/'lenses.png')
 # The glTF exporter cannot preserve the source-only MixRGB darkening.
 # Generate the actual dark-state texels, preserving alpha and LED dot layout.
 import numpy as np
 data=np.array(im);rgb=data[:,:,:3].astype(float)/255
 linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)*.002
 dark=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
 data[:,:,:3]=np.uint8(np.round(np.clip(dark,0,1)*255))
 Image.fromarray(data).save(out/'lenses-off.png')
 # Names are equal geometry; a row changes only UVs, like street-signs.
 sheet=Image.new('RGB',(1024,512),(14,55,35));d=ImageDraw.Draw(sheet)
 for row,pair in enumerate(NAMES):
  for col,text in enumerate(pair):
   x=col*512;y=row*128
   d.rounded_rectangle((x+6,y+6,x+506,y+122),radius=9,outline=(224,230,219),width=3)
   font=ImageFont.truetype(FONT,37)
   while d.textbbox((0,0),text,font=font)[2]>465:font=ImageFont.truetype(FONT,font.size-1)
   d.text((x+256,y+64),text,font=font,anchor='mm',fill=(225,231,221))
 sheet.save(out/'names.png')
 sign=Image.new('RGB',(384,576),(219,220,205));d=ImageDraw.Draw(sign)
 d.rectangle((5,5,378,570),outline=(15,17,16),width=8)
 for text,y,size in [('TO CROSS STREET',44,30),('PUSH BUTTON',91,34)]:
  d.text((192,y),text,font=ImageFont.truetype(FONT,size),anchor='mm',fill=(14,17,15))
 d.line((100,143,285,143),fill=(15,17,16),width=11);d.polygon([(100,143),(144,119),(144,167)],fill=(15,17,16))
 # Original geometric walking person and hand, independent of reference pixels.
 d.ellipse((47,190,67,210),fill=(15,17,16));d.line([(57,215),(47,250),(73,280)],fill=(15,17,16),width=12)
 d.line([(49,245),(28,278)],fill=(15,17,16),width=12);d.line([(56,220),(85,242)],fill=(15,17,16),width=9)
 d.line([(54,220),(26,241)],fill=(15,17,16),width=9)
 for x,y in ((29,329),(41,317),(53,315),(65,323)):d.rounded_rectangle((x,y,x+10,365),5,fill=(15,17,16))
 d.rounded_rectangle((30,348,76,390),12,fill=(15,17,16));d.line([(35,366),(17,348)],fill=(15,17,16),width=12)
 for text,y,size in [('START CROSSING',224,25),('WATCH FOR',256,22),('TURNING CARS',284,22),('DO NOT START',345,24),('IF STARTED',376,22),('FINISH CROSSING',405,22),('TIMER SHOWS',463,25),('TIME TO FINISH',500,25)]:
  d.text((228,y),text,font=ImageFont.truetype(FONT,size),anchor='mm',fill=(14,17,15))
 sign.save(out/'r10.png')
if __name__=='__main__':generate(Path('build/graphics'))
