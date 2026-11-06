"""Original checkpoint sign sheet; interchangeable business names use UVs only."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from kit.fonts import find_font
from plan import TENANTS


def generate(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGBA',(2048,2048),(255,255,255,0));d=ImageDraw.Draw(im);layout={}
    serif=str(find_font('DejaVu Serif','Bold'));sans=str(find_font('DejaVu Sans','Book'))
    fields=['#243D36','#693D29','#293B42','#41362B','#D3CBB6','#4B4934','#424B47','#573F34']
    def fit(text,rect,path,size=65,color='#E7DCBA'):
        x,y,x1,y1=rect;f=ImageFont.truetype(path,size)
        while d.textbbox((0,0),text,font=f)[2]>x1-x-16:f=ImageFont.truetype(path,f.size-1)
        bb=d.textbbox((0,0),text,font=f);d.text(((x+x1-bb[2]-bb[0])/2,(y+y1-bb[3]-bb[1])/2),text,font=f,fill=color)
    for i,(key,(name,sub)) in enumerate(TENANTS.items()):
        x=(i%2)*1024+12;y=(i//2)*270+12;r=(x,y,x+1000,y+230)
        d.rectangle(r,fill=fields[i]);d.rectangle((x+7,y+7,x+993,y+223),outline='#A99167',width=3)
        fit(name,(x+18,y+20,x+982,y+142),serif);fit(sub,(x+20,y+153,x+980,y+210),sans,36,color='#DDD3B9' if key!='vacant' else '#453D30')
        layout[key]=tuple((v/2048 if j%2==0 else 1-v/2048) for j,v in enumerate((x,y+230,x+1000,y)))
    for i,text in enumerate(('MERIDIAN BLOCK 1894','RILL MERCANTILE','MILLSTONE GOODS','ROOMS & OFFICES','1898','1906','OPEN • 9 TO 6','STAIR TO OFFICES')):
        x=(i%2)*1024+12;y=1100+(i//2)*170;r=(x,y,x+1000,y+150)
        d.rectangle(r,fill='#8D8064' if i<4 else '#C6B998');fit(text,r,serif,60,color='#DED1AD' if i<4 else '#4E493D')
        layout['label'+str(i)]=(x/2048,1-(y+150)/2048,(x+1000)/2048,1-y/2048)
    # The ghost lettering is original faded paint with open, irregular losses.
    import random
    rng=random.Random(714)
    x,y=12,1810;d.rectangle((x,y,2020,2015),fill='#8B684A');fit('MILLSTONE  •  SEED & FEED',(x,y,2020,2015),serif,110,color='#C1B18B')
    for i in range(1700):
        xx=rng.randrange(12,2020);yy=rng.randrange(y,2015);d.rectangle((xx,yy,xx+rng.randrange(1,18),yy+rng.randrange(1,5)),fill='#8B684A')
    layout['ghost']=(12/2048,1-2015/2048,2020/2048,1-y/2048)
    out=folder/'T_DowntownFormSigns_BaseColor.png';im.save(out)
    (folder/'layout.json').write_text(json.dumps(layout,indent=2)+'\n');return out,layout
