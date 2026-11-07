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
 'wood':('#63452d',.57,0),'oak':('#795438',.65,0),'cream':('#c6bda5',.87,0),
 'forest':('#24483c',.60,0),'wine':('#632c37',.63,0),'teal':('#38666a',.69,0),
 'ochre':('#8d652a',.65,0),'ink':('#2c3b4a',.62,0),'rust':('#884332',.68,0),
 'cork':('#987347',.95,0),'coffee':('#25140d',.30,0),'pastry':('#aa8050',.85,0),
 'rubber':('#171a19',.9,0),'soil':('#3b3023',.98,0),'leaf':('#365535',.86,0),
 'copper':('#9a6744',.38,.8),'wall':('#a59a7d',.85,0),'floor':('#756659',.83,0)}


def quick(folder=Path('build/atlas')):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);N=2048
    bc=Image.new('RGBA',(N,N),'#e5dfce');orm=Image.new('RGB',(N,N),(255,190,0));normal=Image.new('RGB',(N,N),(128,128,255))
    d=ImageDraw.Draw(bc);od=ImageDraw.Draw(orm);layout={}
    for i,(name,(color,r,m)) in enumerate(COLORS.items()):
        x=i*80;y=1950;d.rectangle((x,y,x+78,2047),fill=color);od.rectangle((x,y,x+78,2047),fill=(255,round(r*255),round(m*255)))
        layout[name]=[(x+30)/N,1-2000/N,(x+48)/N,1-1980/N]
    serif=str(find_font('DejaVu Serif','Bold'));sans=str(find_font('DejaVu Sans','Book'));boldsans=str(find_font('DejaVu Sans','Bold'))
    def text(s,rect,size=48,color='#e2d9bf',font=sans):
        x,y,xx,yy=rect;f=ImageFont.truetype(font,size)
        while d.textbbox((0,0),s,font=f)[2]>xx-x-24:f=ImageFont.truetype(font,max(6,f.size-1))
        bb=d.textbbox((0,0),s,font=f);d.text(((x+xx-bb[2]-bb[0])/2,(y+yy-bb[3]-bb[1])/2),s,font=f,fill=color)
    def cell(key,rect,bg):
        d.rectangle(rect,fill=bg);x,y,xx,yy=rect;layout[key]=[x/N,1-yy/N,xx/N,1-y/N];return rect
    for i,(name,sub,pal) in enumerate(v for values in IDENTITIES.values() for v in values):
        x=(i%2)*1024+8;y=(i//2)*210+8;rect=cell(name,(x,y,x+1000,y+190),COLORS[pal][0]);d.rectangle((x+9,y+9,x+991,y+181),outline='#a38f62',width=3)
        face=boldsans if pal in ('teal','rust') else sans if pal in ('wine','ochre') else serif
        title=name.title() if pal in ('wine','ochre') else name
        text(title,(x+25,y+10,x+975,y+126),78,font=face);text(sub,(x+25,y+128,x+975,y+181),31)
    for i,title in enumerate(('COFFEE','ESPRESSO','FROM THE OVEN')):
        x=10+i*680;y=652;cell('menu'+str(i),(x,y,x+660,y+440),'#242b26')
        text(title,(x+18,y+8,x+642,y+78),46)
        rows=([('House drip','1.65'),('Cold brew','2.25'),('Cafe au lait','2.50'),('Hot chocolate','2.50'),('Tea','1.75'),('Local cider','2.25')] if i==0 else [('Espresso','1.85'),('Americano','2.00'),('Cappuccino','2.75'),('Cafe latte','3.00'),('Mocha','3.25'),('Macchiato','2.25')] if i==1 else [('Butter croissant','1.85'),('Morning bun','2.00'),('Blueberry scone','1.75'),('Bagel + cheese','2.25'),('Coffee cake','2.50'),('Ask for today’s soup','')])
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


def generate(folder=Path('build/atlas')):
    """Guarded shared charts; manufactured channels are baked separately.

    Reuse our own scripted lettering compositor, then repack its charts to
    reserve meaningful area for wood, brushed steel, cloth and causal marks.
    """
    import numpy as np
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    old=quick(folder/'lettering');src=Image.open(folder/'lettering/T_CoffeeShop_BaseColor.png')
    n=2048;bc=Image.new('RGBA',(n,n),'#30332f');orm=Image.new('RGB',(n,n),(255,200,0));height=np.full((n,n),.5,np.float32);layout={};rects={}
    def chart(key,rect):
        x,y,xx,yy=rect;a,b,c,d=old[key];crop=src.crop((round(a*n),round((1-d)*n),round(c*n),round((1-b)*n)))
        bc.paste(crop.resize((xx-x,yy-y),Image.Resampling.LANCZOS),(x,y));rects[key]=rect;layout[key]=[x/n,1-yy/n,xx/n,1-y/n]
    names=[v[0] for values in IDENTITIES.values() for v in values]
    for i,key in enumerate(names):chart(key,(8+i%2*1024,8+i//2*138,1016+i%2*1024,138+i//2*138))
    for i in range(3):chart('menu'+str(i),(8+i*408,430,408+i*408,710))
    for key,rect in dict(hours=(8,730,400,990),chalk=(420,730,800,1210),news=(820,730,1300,1050),community=(820,1070,1300,1410),art=(1320,730,1580,1150),screen=(1320,1170,1580,1410),mesh=(1600,730,2032,1230),vinyl=(8,1010,400,1080)).items():chart(key,rect)
    # Wiped chalk ghosts stay on this written substrate, without adding
    # geometry to the accepted 220-triangle A-frame.
    sd=ImageDraw.Draw(bc)
    for j in range(18):
        yy=955+j*6;sd.line((445+(j%4)*6,yy,760-(j%5)*11,yy-3),fill=(91,110,95,255),width=2)
    # Every cell has an eight-pixel gutter; coverage spans its useful interior.
    rng=np.random.default_rng(73591)
    for i,(key,(color,rough,metal)) in enumerate(COLORS.items()):
        x=8+i%7*292;y=1448+i//7*200;w=272;h=180
        if key=='oak':x=1240;y=430;w=792;h=280
        yy,xx=np.mgrid[:h,:w];u=xx/w;v=yy/h;fine=rng.random((h,w));grain=np.sin(u*160+2*np.sin(v*7)+np.sin(u*37+v*3))
        factor=1+.025*(fine-.5);relief=.5+.008*(fine-.5);rr=np.full((h,w),rough)
        if key in ('wood','oak'):
            factor*=.88+.13*(grain*.5+.5)+.06*np.sin(u*43+v*4);relief+=.04*grain;rr+=.06*grain
            if key=='oak':
                hand=np.exp(-(1-v)/.025)*(.5+.5*np.sin(u*17)**2)
                factor*=1-.24*hand;rr-=.12*hand
        elif key=='steel':
            grain=np.sin(v*510+fine*3);factor*=.92+.08*grain;relief+=.004*grain;rr+=.06*grain
        elif key in ('forest','wine','teal','ochre','ink'):
            weave=np.sin(xx*2.2)*np.sin(yy*2.2);factor*=.93+.025*weave;relief+=.012*weave;rr[:]=.85
        elif key=='pastry':
            factor*=.76+.32*np.sin(u*8+v*6)**2;relief+=.07*(fine-.5)
        elif key=='black':rr+=.025*(fine-.5)
        rgb=np.array(Image.new('RGB',(1,1),color))[0,0];patch=np.uint8(np.clip(rgb*factor[:,:,None],0,255))
        bc.paste(Image.fromarray(patch),(x,y));orm.paste(Image.fromarray(np.uint8(np.stack((np.ones((h,w)),np.clip(rr,0,1),np.full((h,w),metal)),2)*255)),(x,y));height[y:y+h,x:x+w]=relief
        layout[key]=[(x+8)/n,1-(y+h-8)/n,(x+w-8)/n,1-(y+8)/n];rects[key]=(x,y,x+w,y+h)
    # Causal coverage charts: rims, runoff, chips and swept chalk. Their
    # placements, sizes and seeds are chosen by the actual assembled object.
    draw=ImageDraw.Draw(bc)
    for i,key in enumerate(('ring','spill','scuff','drip','crack','chalk_smear')):
        x=8+i*256;y=1240 if i<3 else 1340;x=(i%3)*256+8
        draw.rectangle((x,y,x+240,y+85),fill=(0,0,0,0));layout[key]=[x/n,1-(y+85)/n,(x+240)/n,1-y/n]
        yy,xx=np.mgrid[:85,:240];u=xx/239;v=yy/84;noise=rng.random((85,240))
        if key=='ring':mask=np.exp(-((np.sqrt(((u-.5)/.43)**2+((v-.5)/.39)**2)-1)/.045)**2)*(.40+.60*noise);color=(77,48,27)
        elif key=='spill':mask=np.exp(-(((u-.45)/(.30+.06*np.sin(v*24)))**2+((v-.5)/.38)**2)**2)*(.20+.45*noise);color=(66,49,33)
        elif key=='scuff':mask=(np.sin(v*110+u*8)>.86)*np.sin(np.pi*u)**2*(noise>.45);color=(144,143,126)
        elif key=='drip':mask=np.exp(-((u-.50-.025*np.sin(v*18))/.15)**2)*(.2+.8*v)*(.15+.55*noise);color=(51,46,34)
        elif key=='crack':mask=np.exp(-((v-.48-.17*np.sin(u*10)-.06*np.sin(u*33))/.018)**2)*(.50+.50*noise);color=(66,62,53)
        else:mask=(np.sin(v*45+u*10)>.5)*np.sin(np.pi*u)*(.1+.3*noise);color=(176,175,152)
        tile=np.empty((85,240,4),np.uint8);tile[:,:,:3]=color;tile[:,:,3]=np.uint8(np.clip(mask,0,1)*255);bc.paste(Image.fromarray(tile),(x,y))
    for i,key in enumerate(('forest','wine','teal')):
        x=1600+i*144;y=1250;w=136;h=168
        source=np.asarray(bc.crop(rects[key])).astype(np.float32)
        patch=Image.fromarray(np.uint8(source)).resize((w,h),Image.Resampling.BICUBIC)
        arr=np.asarray(patch).copy();rgb=arr[:,:,:3].astype(float)
        # Oxidized exposed yarn retains the pigment's hue as it lightens.
        arr[:,:,:3]=np.uint8(rgb*.72+np.array((173,165,139))*.28)
        bc.paste(Image.fromarray(arr),(x,y));ImageDraw.Draw(orm).rectangle((x,y,x+w,y+h),fill=(255,232,0));layout[key+'_faded']=[(x+8)/n,1-(y+h-8)/n,(x+w-8)/n,1-(y+8)/n]
    # The large oak chart freed its original cell. Use it for foot-zone
    # abrasion: steel revealed only in the lowest 30–40 mm of a chair leg.
    x,y,w,h=1176,1448,272,180;yy,xx=np.mgrid[:h,:w];u=xx/(w-1);v=1-yy/(h-1)
    chip=(v<(.055+.045*np.sin(u*19)**2))&(np.sin(u*43+v*17)>.20)&(rng.random((h,w))>.22)
    arr=np.empty((h,w,4),np.uint8);arr[:]=(32,35,34,255);arr[chip,:3]=(112,111,100)
    bc.paste(Image.fromarray(arr),(x,y));o=np.empty((h,w,3),np.uint8);o[:]=(255,163,0);o[chip]=(240,124,225);orm.paste(Image.fromarray(o),(x,y));height[y:y+h,x:x+w]-=chip*.005
    layout['leg_wear']=[(x+8)/n,1-(y+h-8)/n,(x+w-8)/n,1-(y+8)/n]
    for key,im in [('BaseColor',bc),('ORM',orm)]:im.save(folder/f'T_CoffeeShop_{key}.png')
    Image.fromarray(np.uint16(np.clip(height,0,1)*65535)).save(folder/'T_CoffeeShop_Height.png')
    (folder/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    return layout


if __name__=='__main__':generate()
