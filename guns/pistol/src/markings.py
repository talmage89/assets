"""Original fictional engravings, rasterized from installed open-license fonts.

These monochrome height masks contain no photograph pixels. Dimensions are
millimeters; the look-dev shader projects them only onto their authored face.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font

DPMM=32
LAYOUTS={
 'slide-left':(74,17,[(9,5.1,'C9',6.0),(44,4.8,'PROPANE DEFENSE',3.1),
                      (9,12.1,'9 x 19',2.5),(45,12.1,'PD-C9-047216',2.7)]),
 'slide-right':(22,17,[(11,5.4,'C9',6.0),(11,12.4,'9 x 19',2.8)]),
 'frame-left':(44,8,[(22,2.7,'PROPANE DEFENSE',2.7),(22,6,'PD 047216',1.9)]),
 'frame-right':(37,7,[(18.5,3.5,'PROPANE DEFENSE',2.7)]),
 'magazine':(23,10,[(11.5,3.1,'9 x 19',2.9),(11.5,7.0,'15 RD',2.2)]),
}

def main():
 out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True)
 for name,(w,h,rows) in LAYOUTS.items():
  im=Image.new('L',(round(w*DPMM),round(h*DPMM)),0);draw=ImageDraw.Draw(im)
  for x,y,text,size in rows:
   font=ImageFont.truetype(find_font('Noto Sans','Bold' if text=='C9' else 'Regular'),round(size*DPMM))
   draw.text((x*DPMM,y*DPMM),text,font=font,anchor='mm',fill=255)
  # A tool-radius edge rather than an ideal pixel-sharp printed decal.
  im.filter(ImageFilter.GaussianBlur(.38)).save(out/(name+'.png'))
  print('MARKING',name,im.size)

if __name__=='__main__':main()
