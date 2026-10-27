"""Original plate, badges, tire relief and repeating grille relief; open fonts."""
import argparse,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
FONT='/usr/share/fonts/noto/NotoSans-Bold.ttf'


def centered(d,box,text,size,fill,font=FONT):
    f=ImageFont.truetype(font,size);bb=d.textbbox((0,0),text,font=f)
    d.text(((box[0]+box[2]-bb[2])/2,(box[1]+box[3]-bb[3])/2-bb[1]/2),text,font=f,fill=fill)


def build(out):
    out.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1024,512),(212,219,214));d=ImageDraw.Draw(im)
    d.rounded_rectangle((22,18,1002,494),radius=28,outline=(42,62,66),width=12)
    centered(d,(0,25,1024,130),'FOUNDRY COUNTY',62,(41,64,73))
    centered(d,(0,130,1024,370),'08N 417',175,(22,38,42))
    centered(d,(0,375,1024,485),'ALDER  /  FIELD SERIES',43,(45,63,66))
    im.save(out/'plate.png')
    im=Image.new('RGB',(1024,256),(10,13,15));d=ImageDraw.Draw(im)
    centered(d,(15,5,1009,251),'ALDER',185,(190,198,201));im.save(out/'badge.png')
    im=Image.new('RGB',(512,192),(12,14,17));d=ImageDraw.Draw(im)
    centered(d,(0,0,512,192),'C150  4x4',80,(175,181,184));im.save(out/'model.png')
    im=Image.new('RGB',(512,256),(7,12,15));d=ImageDraw.Draw(im)
    for x in [135,377]:
        d.ellipse((x-83,45,x+83,211),outline=(113,137,144),width=3)
        for a in range(-130,131,26):
            t=math.radians(a-90);d.line((x+65*math.cos(t),128+65*math.sin(t),x+76*math.cos(t),128+76*math.sin(t)),fill=(167,182,178),width=2)
        d.line((x,128,x-44,160),fill=(173,75,34),width=3)
    centered(d,(0,0,512,43),'ALDER  /  PARK',24,(175,193,193));im.save(out/'display.png')
    im=Image.new('L',(1024,1024),0)
    def arc(text,radius,start,end,size):
        f=ImageFont.truetype(FONT,size)
        for char,angle in zip(text,[start+(end-start)*i/(len(text)-1) for i in range(len(text))]):
            tile=Image.new('L',(size*2,size*2));td=ImageDraw.Draw(tile);bb=td.textbbox((0,0),char,font=f)
            td.text(((size*2-bb[2])/2,(size*2-bb[3])/2-bb[1]/2),char,font=f,fill=220)
            tile=tile.rotate(-angle,Image.Resampling.BICUBIC,expand=True)
            a=math.radians(angle);x=512+radius*math.sin(a);y=512-radius*math.cos(a)
            im.paste(tile,(round(x-tile.width/2),round(y-tile.height/2)),tile)
    arc('ALDER TRAIL A/T',352,-62,62,40);arc('275/65 R18',352,142,218,30)
    d=ImageDraw.Draw(im)
    for r in [292,300,418,424]:d.ellipse((512-r,512-r,512+r,512+r),outline=150,width=2)
    im.save(out/'tire_relief.png')
    im=Image.new('RGB',(512,512),(13,16,18));d=ImageDraw.Draw(im)
    for y in range(-30,550,42):
        for x in range(-30,550,60):
            xx=x+(30 if (y//42)%2 else 0);d.polygon([(xx,y),(xx+24,y-12),(xx+48,y),(xx+24,y+12)],fill=(45,49,50))
    im.save(out/'grille.png')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.65);a=p.parse_args();build(Path(a.out))
