"""Original X220 display, fictional emblems and 225/65R17 relief; open fonts."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from kit.fonts import find_font
from markings import centered


def build(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 font=find_font('Noto Sans','Bold')
 for name,size,label,fg,bg in [('badge',(512,128),'ALDER',(193,201,204),(9,12,14)),('model',(512,128),'X220  AWD',(180,186,190),(13,16,18)),('plate',(1024,512),'ALDER',(41,47,49),(197,201,197)),('display',(512,256),'P  |  21°',(123,170,179),(5,9,12))]:
  im=Image.new('RGB',size,bg);d=ImageDraw.Draw(im)
  centered(d,(0,0,*size),label,round(size[1]*.52),fg,font)
  if name=='display':
   for x in [50,462]:d.arc((x-45,120,x+45,210),30,310,fill=(116,145,153),width=3)
  im.save(out/(name+'.png'))
 im=Image.new('L',(1024,1024),0);d=ImageDraw.Draw(im)
 for text,r,start,end,size in [('ALDER TOURING',362,-63,63,42),('225/65 R17',362,142,218,31)]:
  f=ImageFont.truetype(font,size)
  for k,char in enumerate(text):
   a=start+(end-start)*k/(len(text)-1);tile=Image.new('L',(size*2,size*2));td=ImageDraw.Draw(tile)
   td.text((size,size),char,font=f,anchor='mm',fill=215);tile=tile.rotate(-a,Image.Resampling.BICUBIC,expand=True)
   x=512+r*math.sin(math.radians(a));y=512-r*math.cos(math.radians(a));im.paste(tile,(round(x-tile.width/2),round(y-tile.height/2)),tile)
 for r in [290,298,422,428]:d.ellipse((512-r,512-r,512+r,512+r),outline=140,width=2)
 im.save(out/'tire_relief.png')

if __name__=='__main__':build(sys.argv[1])
