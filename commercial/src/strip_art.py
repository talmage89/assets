"""Original 2K retail graphics, interior fronts and causal deposits.

One guarded sheet, no photographic input; every occupant owns window art.
Coordinates stay in source pixels until strip_graphics normalizes them.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from kit.fonts import find_font
from kit.image_io import srgb_to_linear,linear_to_srgb,write_png
from strip_plan import TENANTS


def populate(image,records,out):
    image.paste((0,0,0,0),(0,0,2048,2048));records.clear();dr=ImageDraw.Draw(image)
    cursor=[6,6,0];em=np.zeros((2048,2048,3),dtype=np.float32)
    def rect(w,h):
        x,y,row=cursor
        if x+w+6>2048:x=6;y+=row+12;row=0
        assert y+h+6<2048,('Strip sheet full',y,h)
        cursor[:]=[x+w+12,y,max(row,h)]
        return (x,y,x+w,y+h)
    def text(s,r,color='#ECE4CF',size=48,family='DejaVu Sans'):
        ff=ImageFont.truetype(str(find_font(family,'Bold')),size)
        while True:
            b=dr.textbbox((0,0),s,font=ff)
            if b[2]-b[0]<r[2]-r[0]-8 and b[3]-b[1]<r[3]-r[1]-4:break
            ff=ImageFont.truetype(ff.path,ff.size-1)
        dr.text(((r[0]+r[2]-b[0]-b[2])/2,(r[1]+r[3]-b[1]-b[3])/2),s,font=ff,fill=color)
    def light(r,power):
        x,y,a,b=r;rgb=np.asarray(image)[y:b,x:a].astype(np.float32)/255
        em[y:b,x:a]=srgb_to_linear(rgb[:,:,:3])*rgb[:,:,3:4]*power/300
    for kind in ('sign','faded'):
        for key,t in TENANTS.items():
            r=rect(490,78);x,y,a,b=r;records.setdefault(key,{'style':t['style']})[kind]=r
            # The backplate is opaque: letters cannot cast a detached second
            # alphabet through their carrier. Lit letters remain radiance-only.
            field=t['field'] if t['style']!='channel' else '#232322'
            dr.rectangle(r,fill=field)
            if t['style']=='panel':dr.rectangle((x+3,y+3,a-3,b-3),outline=t['ink'],width=2)
            text(t['name'],(x+8,y+2,a-8,y+47),t['ink'],48,'DejaVu Serif' if t['font']=='serif' else 'DejaVu Sans')
            text(t['subtitle'],(x+8,y+51,a-8,b-3),t['ink'],24)
            if kind=='faded':
                piece=np.asarray(image.crop(r)).copy();piece[:,:,:3]=np.uint8(piece[:,:,:3]*.86+22);image.paste(Image.fromarray(piece),(x,y))
            if key!='vacant':
                light(r,.75 if t['style']=='channel' else .45)
                if t['style']=='channel':
                    # Dark carrier is not a luminous sign face.
                    region=em[y:b,x:a];region[np.max(region,axis=2)<.00025]=0
    for key,t in TENANTS.items():
        r=rect(240,134);x,y,a,b=r;dr.rectangle(r,fill=t['field']);words=t['name'].split();records[key]['tower']=r
        if len(words)>1:
            text(' '.join(words[:-1]),(x+4,y,a-4,y+47),t['ink'],44,'DejaVu Serif');text(words[-1],(x+4,y+43,a-4,y+91),t['ink'],44,'DejaVu Serif')
        else:text(t['name'],(x+4,y+7,a-4,y+90),t['ink'],46)
        text(t['subtitle'],(x+3,y+96,a-3,b-4),t['ink'],18)
        if key!='vacant':light(r,.45)
    words={
        'nails':('MANICURE  /  PEDICURE','WALK-INS WELCOME','GEL + NAIL ART'),
        'cleaner':('ALTERATIONS','SAME DAY SERVICE','SHIRTS  •  DRY CLEANING'),
        'pizza':('SLICES  •  WHOLE PIES','LUNCH COMBO  8.50','FRESH FROM THE OVEN'),
        'laundry':('WASH  •  DRY  •  FOLD','LARGE LOAD MACHINES','OPEN DAILY  7 AM - 10 PM'),
        'phone':('CRACKED SCREEN?','REPAIRS WHILE YOU WAIT','CASES + CHARGERS'),
        'mattress':('SLEEP BETTER','FLOOR MODEL SALE','MATTRESS + FRAME'),
        'tax':('TAX + BOOKKEEPING','APPOINTMENTS AVAILABLE','PERSONAL + SMALL BUSINESS'),
        'hair':('CUT  •  COLOR  •  STYLE','WALK-INS WELCOME','YOUR NEXT GOOD HAIR DAY'),
        'vacant':('FOR LEASE','RETAIL SPACE AVAILABLE','INQUIRE AT CENTER OFFICE')}
    for kind in ('vinyl','poster'):
        for key,t in TENANTS.items():
            r=rect(240,100 if kind=='vinyl' else 260);x,y,a,b=r;records[key][kind]=r
            if kind=='poster':
                dr.rectangle(r,fill=('#E9DDC2' if key in ('pizza','tax','vacant','mattress') else t['field']))
                dr.rectangle((x+4,y+4,a-4,b-4),outline=t['ink'] if key not in ('pizza','tax','vacant','mattress') else '#684833',width=2)
            ink='#EEE9DA' if kind=='vinyl' else '#513C2C' if key in ('pizza','tax','vacant','mattress') else '#F1E9D7'
            if kind=='vinyl':
                for i,s in enumerate(words[key]):text(s,(x+6,y+i*(b-y)/3,a-6,y+(i+1)*(b-y)/3),ink,29 if i==0 else 23)
            else:
                text(words[key][0],(x+6,y+8,a-6,y+43),ink,27)
                text(words[key][1],(x+6,b-73,a-6,b-36),ink,26)
                text(words[key][2],(x+6,b-35,a-6,b-6),ink,21)
                cx=(x+a)//2;cy=y+112
                if key=='pizza':
                    dr.ellipse((cx-62,cy-62,cx+62,cy+62),fill='#AA6433',outline='#6C3D23',width=4)
                    dr.ellipse((cx-52,cy-52,cx+52,cy+52),fill='#D0A54D')
                    for xx,yy in ((-23,-18),(29,-15),(-5,31),(27,25),(-30,23),(4,-38)):dr.ellipse((cx+xx-8,cy+yy-8,cx+xx+8,cy+yy+8),fill='#8C3D28')
                    for dx,dy in ((1,0),(0,1),(.7,.7),(-.7,.7)):dr.line((cx-dx*56,cy-dy*56,cx+dx*56,cy+dy*56),fill='#EAD79C',width=2)
                elif key=='phone':
                    dr.rounded_rectangle((cx-35,cy-65,cx+35,cy+65),radius=9,outline=ink,width=5)
                    dr.line((cx-28,cy+20,cx+15,cy-30,cx-5,cy-5,cx+25,cy+30),fill='#CAAE68',width=3)
                elif key=='laundry':
                    dr.rectangle((cx-55,cy-60,cx+55,cy+60),outline=ink,width=4);dr.ellipse((cx-42,cy-35,cx+42,cy+49),outline=ink,width=6)
                    dr.rectangle((cx-43,cy-50,cx-12,cy-42),fill=ink)
                elif key in ('nails','hair'):
                    dr.ellipse((cx-48,cy-48,cx-8,cy-8),outline=ink,width=4);dr.ellipse((cx+8,cy-48,cx+48,cy-8),outline=ink,width=4)
                    dr.line((cx-26,cy-10,cx+38,cy+58),fill=ink,width=5);dr.line((cx+26,cy-10,cx-38,cy+58),fill=ink,width=5)
                elif key=='cleaner':
                    dr.line((cx-65,cy+28,cx,cy-18,cx+65,cy+28,cx-65,cy+28),fill=ink,width=4);dr.arc((cx-6,cy-47,cx+17,cy-18),160,450,fill=ink,width=4)
                elif key=='mattress':
                    for j in range(3):dr.rounded_rectangle((cx-68,cy-35+j*25,cx+68,cy-13+j*25),radius=7,outline=ink,width=3)
                else:
                    for j in range(4):dr.line((cx-50,cy-40+j*25,cx+50,cy-40+j*25),fill=ink,width=3)

    for key,t in TENANTS.items():
        r=rect(116,90);x,y,a,b=r;records[key]['window']=r
        text('HOURS' if key!='vacant' else 'FOR LEASE',(x,y,a,y+28),'#F1EBDD',24)
        text('AT OFFICE' if key=='vacant' else 'MON - SAT',(x,y+29,a,y+56),'#E3DECD',17)
        text('INQUIRE' if key=='vacant' else '9 AM - 7 PM',(x,y+59,a,b),'#E3DECD',16)
    specials={
        'Open':('OPEN',), 'PizzaMenu':('NOTCH OVEN','CHEESE  12   /   GARDEN  15','PEPPER + SAUSAGE  16','SLICES  3.50   /   COMBO  8.50'),
        'Drinks':('COLD DRINKS','•  •  •  •  •','•  •  •  •  •','•  •  •  •  •'),
        'Products':('CARE + COLOR','▮  ▮  ▮  ▮  ▮','▮  ▮  ▮  ▮  ▮'),
        'WashControl':('COPPERFOLD','60°   40°   30°','START  ●'),
        'Paper':('',), 'Waste':('CENTER SERVICE','KEEP LIDS CLOSED'),
    }
    for key,lines in specials.items():
        r=rect(240,118);x,y,a,b=r;records[key]={'sign':r}
        if key=='Paper':
            rng=np.random.default_rng(217);yy,xx=np.mgrid[:118,:240];v=1-.025*np.sin(xx*.12+yy*.03)-rng.random((118,240))*.025
            rgb=np.stack((.71*v,.63*v,.48*v,np.ones_like(v)),2);image.paste(Image.fromarray(np.uint8(np.clip(rgb,0,1)*255)),(x,y))
        else:
            if key!='Open':dr.rectangle(r,fill='#243331' if key!='Waste' else '#D7D0B6')
            for i,s in enumerate(lines):text(s,(x+5,y+i*118/len(lines),a-5,y+(i+1)*118/len(lines)), '#FF653D' if key=='Open' else '#ECE5C9' if key!='Waste' else '#303B32',72 if key=='Open' else 24)
            if key=='Open':
                dr.rounded_rectangle((x+5,y+10,a-5,b-10),radius=24,outline='#4E9AA8',width=3);light(r,5)
            if key in ('Drinks','PizzaMenu','Products'):light(r,.18)
    # Causal chart pixels retain the family's authored deposit shapes.
    catalogue=json.loads(Path('textures/ship/graphics.json').read_text());shared=Image.open('textures/ship/T_CommercialGraphics_BaseColor.png').convert('RGBA')
    for key in ('Oil0','Oil1','Oil2','Oil3','Tire','Gum','Salt','Grime','Scuff','Rust'):
        r=rect(180,104);x,y,a,b=r;u,v,c,d=catalogue['Wear:'+key]['rect'];piece=shared.crop((round(u*1024),round((1-d)*1024),round(c*1024),round((1-v)*1024))).resize((180,104),Image.Resampling.LANCZOS)
        pixels=np.asarray(piece).copy()
        if key=='Tire':pixels[:,:,3]=np.uint8(pixels[:,:,3]*.45)
        if key=='Grime':
            yy,xx=np.mgrid[:104,:180];alpha=np.zeros((104,180),float)
            for i in range(7):alpha+=.55*np.exp(-((xx/180-(.18+i*.105+.018*np.sin(yy/19+i)))/(.012+.016*(1-yy/104)))**2)*(1-yy/104)**.65
            pixels[:,:,:3]=[80,74,60];pixels[:,:,3]=np.uint8(np.clip(alpha,0,.62)*255)
        if key=='Rust':
            yy,xx=np.mgrid[:104,:180];rng=np.random.default_rng(631);broad=np.asarray(Image.fromarray(rng.random((9,32)).astype('float32')).resize((180,104),Image.Resampling.BICUBIC))
            wet=.10+.20*(.5+.5*np.sin(xx*.17+broad*4))**3
            alpha=np.clip((yy/104-(1-wet))/.05,0,1)*np.clip((broad-.32)*3.4,0,1)*.80
            pixels[:,:,:3]=[100,55,25];pixels[:,:,3]=np.uint8(alpha*255)
        image.paste(Image.fromarray(pixels),(x,y));records['Wear:'+key]={'sign':r}
    for key,base,opacity in (('WalkGrime','Oil2',.35),('WalkTrack','Tire',.30)):
        r=rect(180,104);piece=image.crop(records['Wear:'+base]['sign']);a=np.asarray(piece).copy();a[:,:,3]=np.uint8(a[:,:,3]*opacity);image.paste(Image.fromarray(a),r[:2]);records['Wear:'+key]={'sign':r}
    for i,address in enumerate(str(110+2*i) for i in range(12)):
        r=rect(64,27);dr.rectangle(r,fill='#252D2A');text(address,r,'#EAE5D2',23);records[address]={'sign':r}
    for name in ('ALDER RILL SHOPS','CROSSBEND COURT','LOWBANK COMMONS','WILLOW SPAN SHOPS'):
        r=rect(240,78);x,y,a,b=r;dr.rectangle(r,fill='#3E493C');text(name,(x,y,a,y+48),size=29,family='DejaVu Serif');text('NEIGHBORHOOD SHOPS',(x,y+50,a,b),size=16);records[name]={'sign':r};light(r,.45)
    for key in ('RESERVED','VAN ACCESSIBLE'):
        r=rect(156,24);dr.rectangle(r,fill='#ECE8D9');text(key,r,'#34483B',18);records[key]={'sign':r}
    for key,power in (('InteriorLamp',32),('WalkLamp',28),('WallLamp',20),('LotLamp',140),('Blank',0)):
        r=rect(24,24);dr.rectangle(r,fill='#E9E3D5');records[key]={'sign':r};light(r,power)
    r=rect(330,48);text('FEN ROW VIDEO',r,(130,123,103,100),36);records['Ghost']={'sign':r}
    em=em.reshape(1024,2,1024,2,3).mean(axis=(1,3));write_png(out/'T_StripSigns_Emission.png',linear_to_srgb(em),bits=16)
    print('STRIP ART used height',cursor[1]+cursor[2],flush=True)
