"""Original fictional markings; installed Noto Sans, no reference pixels."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
DPMM=48
out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
for name,w,h,rows in [
 ('barrel',64,8,[(32,3,'PROPANE DEFENSE',2.6),(32,6.2,'.357 MAGNUM',1.5)]),
 ('frame',26,11,[(13,3.1,'MERIDIAN SIX',2.2),(13,7.3,'PD-M6-028641',1.45)])]:
 im=Image.new('L',(round(w*DPMM),round(h*DPMM)),0);d=ImageDraw.Draw(im)
 for x,y,s,size in rows:d.text((x*DPMM,y*DPMM),s,font=ImageFont.truetype(find_font('Noto Sans','Regular'),round(size*DPMM)),anchor='mm',fill=255)
 im.filter(ImageFilter.GaussianBlur(.4)).save(out/(name+'.png'))
im=Image.new('L',(576,576),0)
for text,start,radius in [('PD 357',205,4.1),('26',35,4.1)]:
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),52)
 for j,char in enumerate(text):
  angle=start+j*14;tile=Image.new('L',(90,90),0)
  ImageDraw.Draw(tile).text((45,45),char,font=font,anchor='mm',fill=255)
  tile=tile.rotate(90-angle,resample=Image.Resampling.BICUBIC)
  x=288+radius*DPMM*math.cos(math.radians(angle));y=288+radius*DPMM*math.sin(math.radians(angle))
  im.paste(tile,(round(x-45),round(y-45)),tile)
im.filter(ImageFilter.GaussianBlur(.35)).save(out/'headstamp.png')
