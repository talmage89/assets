"""Original S240 and 235/45R18 sidewall graphics; installed open Noto font."""
import math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=find_font('Noto Sans','Bold')

def build(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    image=Image.new('RGB',(512,128),(12,14,16));d=ImageDraw.Draw(image);f=ImageFont.truetype(FONT,76)
    text='S240';bb=d.textbbox((0,0),text,font=f);d.text(((512-bb[2])/2,(128-bb[3]-bb[1])/2),text,font=f,fill=(185,193,195));image.save(out/'model.png')
    image=Image.new('L',(1024,1024),0)
    for text,r,start,end,size in [('ALDER TOURING',352,-62,62,40),('235/45 R18',352,142,218,30)]:
        f=ImageFont.truetype(FONT,size)
        for i,char in enumerate(text):
            angle=start+(end-start)*i/(len(text)-1);tile=Image.new('L',(size*2,size*2));d=ImageDraw.Draw(tile);bb=d.textbbox((0,0),char,font=f)
            d.text(((size*2-bb[2])/2,(size*2-bb[3]-bb[1])/2),char,font=f,fill=220)
            tile=tile.rotate(-angle,Image.Resampling.BICUBIC,expand=True);a=math.radians(angle)
            image.paste(tile,(round(512+r*math.sin(a)-tile.width/2),round(512-r*math.cos(a)-tile.height/2)),tile)
    d=ImageDraw.Draw(image)
    for r in [292,300,418,424]:d.ellipse((512-r,512-r,512+r,512+r),outline=150,width=2)
    image.save(out/'tire_relief.png')
if __name__=='__main__':build(sys.argv[1])
