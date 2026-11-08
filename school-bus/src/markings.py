"""Only original fictional markings; never reads any reference photograph."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font
from spec import SEEDS
FONT=find_font('Noto Sans','Bold')

def label(text,path,size=(1600,240),color=(5,6,5),background=(249,174,13)):
    im=Image.new('RGB',size,background);d=ImageDraw.Draw(im);f=ImageFont.truetype(FONT,round(size[1]*.80))
    bb=d.textbbox((0,0),text,font=f);tw=bb[2]-bb[0];th=bb[3]-bb[1]
    tile=Image.new('RGB',(tw+10,th+10),background);ImageDraw.Draw(tile).text((5-bb[0],5-bb[1]),text,font=f,fill=color)
    fit=min((size[0]-12)/tile.width,(size[1]-12)/tile.height);tile=tile.resize((round(tile.width*fit),round(tile.height*fit)),Image.Resampling.LANCZOS)
    im.paste(tile,((size[0]-tile.width)//2,(size[1]-tile.height)//2));im.save(path)

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    label('SCHOOL BUS',out/'school.png',(1800,260))
    label('EMERGENCY DOOR',out/'emergency.png',(1200,150))
    label('MORROW  /  C75',out/'maker.png',(900,120),background=(18,19,18),color=(170,174,159))
    label('STOP',out/'stop.png',(768,384),color=(230,232,220),background=(170,12,8))
    for seed,s in SEEDS.items():
        label(s['district'],out/f'district-{seed}.png',(2000,200))
        label(s['fleet'],out/f'fleet-{seed}.png',(500,300))
        label('FS '+s['fleet']+' 82',out/f'plate-{seed}.png',(600,300),background=(182,192,174),color=(20,30,24))

if __name__=='__main__':build(Path(sys.argv[1]))
