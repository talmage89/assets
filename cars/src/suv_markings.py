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
 for name,size,label,fg,bg in [('badge',(512,128),'ALDER',(193,201,204),(9,12,14)),('model',(512,128),'X220  AWD',(180,186,190),(13,16,18)),('plate',(1024,512),'ALDER',(41,47,49),(197,201,197))]:
  im=Image.new('RGB',size,bg);d=ImageDraw.Draw(im)
  centered(d,(0,0,*size),label,round(size[1]*.52),fg,font)
  im.save(out/(name+'.png'))
 regular=find_font('Noto Sans','Regular')
 im=Image.new('RGB',(512,256),(5,9,12));d=ImageDraw.Draw(im)
 d.text((18,10),'ALDER',font=ImageFont.truetype(font,17),fill=(153,177,182));d.text((400,10),'10:24',font=ImageFont.truetype(regular,16),fill=(142,160,166))
 d.rectangle((16,42,353,206),fill=(17,28,32))
 for y in [70,110,157,187]:d.line([(17,y),(125,y-12),(230,y+8),(351,y-4)],fill=(40,56,61),width=4)
 for x in [70,180,283]:d.line([(x-25,45),(x,115),(x-13,205)],fill=(40,56,61),width=4)
 d.line([(157,200),(153,157),(204,122),(208,79),(252,45)],fill=(75,154,170),width=5);d.polygon([(153,139),(144,160),(164,157)],fill=(194,215,216))
 d.text((378,66),'21°',font=ImageFont.truetype(regular,34),fill=(151,180,185));d.text((373,113),'AUTO',font=ImageFont.truetype(regular,13),fill=(107,132,138))
 for i,label in enumerate(['MAP','AUDIO','PHONE','SETUP']):d.text((28+i*126,225),label,font=ImageFont.truetype(regular,13),fill=(126,149,154))
 im.save(out/'display.png')
 im=Image.new('RGB',(512,160),(4,7,10));d=ImageDraw.Draw(im)
 for cx,label in [(83,'rpm ×1000'),(429,'km/h')]:
  for k in range(25):
   a=math.radians(140+260*k/24);r=62;inner=53 if k%3==0 else 57
   d.line([(cx+inner*math.cos(a),80+inner*math.sin(a)),(cx+r*math.cos(a),80+r*math.sin(a))],fill=(136,157,162) if k<22 else (165,52,41),width=2)
  a=math.radians(145);d.line([(cx,80),(cx+46*math.cos(a),80+46*math.sin(a))],fill=(170,191,195),width=2)
  centered(d,(cx-53,112,cx+53,140),label,12,(116,138,145),regular)
 centered(d,(206,18,306,94),'0',58,(174,196,201),regular);centered(d,(220,92,292,112),'km/h',13,(117,143,150),regular)
 d.text((173,24),'P',font=ImageFont.truetype(font,20),fill=(154,184,191));d.text((308,27),'21°',font=ImageFont.truetype(regular,16),fill=(116,145,153))
 d.line([(183,129),(329,129)],fill=(49,70,77),width=1);d.text((203,138),'ODO  62 480',font=ImageFont.truetype(regular,11),fill=(105,134,141))
 im.save(out/'cluster.png')
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
