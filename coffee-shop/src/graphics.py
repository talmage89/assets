"""One original quick PBR sheet: solids, fictional signs and room graphics.

This is a form-stage allocation, not the promised 4096 manufactured bake.
No reference image is read. All lettering uses installed open DejaVu fonts.
"""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font
from plan import IDENTITIES

COLORS={'black':('#202322',.64,.0),'steel':('#959c9b',.30,1),'white':('#d4ccaf',.65,0),
 'wood':('#63452d',.57,0),'oak':('#97724d',.65,0),'cream':('#c6bda5',.87,0),
 'forest':('#24483c',.60,0),'wine':('#632c37',.63,0),'teal':('#38666a',.69,0),
 'ochre':('#8d652a',.65,0),'ink':('#2c3b4a',.62,0),'rust':('#884332',.68,0),
 'cork':('#987347',.95,0),'coffee':('#25140d',.30,0),'pastry':('#ac6e2d',.85,0),
 'rubber':('#171a19',.9,0),'soil':('#3b3023',.98,0),'leaf':('#365535',.86,0),
 'copper':('#9a6744',.38,.8),'wall':('#a59a7d',.85,0),'floor':('#756659',.83,0)}


def generate(folder=Path('build/atlas')):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);N=2048
    bc=Image.new('RGBA',(N,N),'#e5dfce');orm=Image.new('RGB',(N,N),(255,190,0));normal=Image.new('RGB',(N,N),(128,128,255))
    d=ImageDraw.Draw(bc);od=ImageDraw.Draw(orm);layout={}
    for i,(name,(color,r,m)) in enumerate(COLORS.items()):
        x=i*80;y=1950;d.rectangle((x,y,x+78,2047),fill=color);od.rectangle((x,y,x+78,2047),fill=(255,round(r*255),round(m*255)))
        layout[name]=[(x+30)/N,1-2000/N,(x+48)/N,1-1980/N]
    serif=str(find_font('DejaVu Serif','Bold'));sans=str(find_font('DejaVu Sans','Book'))
    def text(s,rect,size=48,color='#e2d9bf',font=sans):
        x,y,xx,yy=rect;f=ImageFont.truetype(font,size)
        while d.textbbox((0,0),s,font=f)[2]>xx-x-24:f=ImageFont.truetype(font,max(6,f.size-1))
        bb=d.textbbox((0,0),s,font=f);d.text(((x+xx-bb[2]-bb[0])/2,(y+yy-bb[3]-bb[1])/2),s,font=f,fill=color)
    def cell(key,rect,bg):
        d.rectangle(rect,fill=bg);x,y,xx,yy=rect;layout[key]=[x/N,1-yy/N,xx/N,1-y/N];return rect
    for i,(name,sub,pal) in enumerate(v for values in IDENTITIES.values() for v in values):
        x=(i%2)*1024+8;y=(i//2)*210+8;rect=cell(name,(x,y,x+1000,y+190),COLORS[pal][0]);d.rectangle((x+9,y+9,x+991,y+181),outline='#a38f62',width=3)
        text(name,(x+25,y+10,x+975,y+126),78,font=serif);text(sub,(x+25,y+128,x+975,y+181),31)
    for i,title in enumerate(('COFFEE','ESPRESSO','FROM THE OVEN')):
        x=10+i*680;y=652;cell('menu'+str(i),(x,y,x+660,y+440),'#242b26')
        text(title,(x+18,y+8,x+642,y+78),46)
        rows=[('House drip','1.65'),('Americano','2.00'),('Cappuccino','2.75'),('Cafe latte','3.00'),('Mocha','3.25'),('Tea / cocoa','2.25')] if i<2 else [('Butter croissant','1.85'),('Morning bun','2.00'),('Blueberry scone','1.75'),('Bagel + cheese','2.25'),('Coffee cake','2.50'),('Ask for today’s soup','')]
        for j,(s,price) in enumerate(rows):
            f=ImageFont.truetype(sans,27);d.text((x+24,y+96+j*50),s,font=f,fill='#b8c0a6');d.text((x+554,y+96+j*50),price,font=f,fill='#ded7b9')
    cell('hours',(12,1120,490,1420),'#d4ccaf');text('COME ON IN',(20,1132,480,1192),44,color='#2a3d34',font=serif)
    for j,s in enumerate(('MON – FRI   6:30 – 7','SAT – SUN   7 – 6','PLEASE USE OTHER DOOR','LOCALLY ROASTED')):text(s,(20,1200+j*49,480,1245+j*49),25,color='#2a3d34')
    cell('chalk',(515,1120,1015,1700),'#263d35');text('GOOD MORNING',(528,1135,1000,1250),43)
    for j,s in enumerate(('Fresh coffee','Warm scones','Take a seat','Soup at noon')):text(s,(530,1250+j*88,1000,1330+j*88),41)
    cell('news',(1035,1120,1660,1550),'#d2c7a5');text('THE DAILY POST',(1050,1125,1645,1220),54,color='#292b25',font=serif);text('RIVER WALK REOPENS',(1050,1230,1645,1287),35,color='#30342c')
    for xx in (1055,1260,1465):
        for yy in range(1300,1530,11):d.line((xx,yy,xx+168,yy),fill='#817d69',width=2)
    cell('community',(1035,1570,1660,1920),'#8c7049')
    for j,s in enumerate(('OPEN MIC','GARDEN CLUB','LESSONS','LOST CAT','BOOK SWAP','JAZZ NIGHT')):
        x=1052+(j%3)*199;y=1586+(j//3)*164;d.rectangle((x,y,x+177,y+140),fill=('#bfc0a1','#d2ba85','#a4b9a7')[j%3]);text(s,(x+3,y+10,x+174,y+56),21,color='#333c31')
        for k in range(4):d.line((x+18,y+71+k*13,x+152,y+71+k*13),fill='#737764',width=2)
    cell('art',(1685,1120,2030,1580),'#b1976e')
    for j in range(6):d.ellipse((1700+j*22,1160+j*38,1930+j*13,1370+j*24),outline=('#334a42','#713f29','#c6b78d')[j%3],width=14)
    cell('screen',(1685,1600,2030,1870),'#233b3e');text('TODAY',(1695,1620,2020,1700),38)
    # Original expanded-steel aperture tile, 15 mm diamond pitch at chair
    # scale. Fine holes belong to coverage, not thousands of wire cylinders.
    import numpy as np
    arr=np.asarray(bc).copy();yy,xx=np.mgrid[:500,:480]
    dx=np.abs((xx+8)%16-8);dy=np.abs((yy+8)%16-8)
    web=(dx+dy>6.6).astype(float)
    arr[1435:1935,12:492,:3]=(32,35,34);arr[1435:1935,12:492,3]=(web*255).astype('uint8')
    bc=Image.fromarray(arr);d=ImageDraw.Draw(bc);layout['mesh']=[12/N,1-1935/N,492/N,1-1435/N]
    cell('vinyl',(1685,1880,2030,1940),(0,0,0,0));text('FRESH COFFEE',(1685,1880,2030,1940),38,color='#e5d7b4')
    for k,im in (('BaseColor',bc),('Normal',normal),('ORM',orm)):im.save(folder/f'T_CoffeeShop_{k}.png')
    (folder/'layout.json').write_text(json.dumps(layout,indent=2)+'\n');return layout


if __name__=='__main__':generate()
