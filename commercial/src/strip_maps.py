"""Strip-only ink/radiance sheet extending the family's original shared swatches.

No photographic input. Reuses the gas delivery's exact manufactured/deposit
art; tenant art and the removed-letter ghost are original installed-font ink.
The 2K color + 1K emission allocation replaces gas graphics for a strip.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont,ImageFilter
from kit.image_io import srgb_to_linear,linear_to_srgb,write_png
from kit.fonts import find_font
from strip_plan import TENANTS


def extend(image,records,out):
    size=image.width;dr=ImageDraw.Draw(image)
    # South panel UV alternatives record accumulated UV exposure. North faces
    # and internally lit faces retain stronger pigment.
    for i,key in enumerate(TENANTS):
        a,b,c,d=records[key]['sign'];piece=image.crop((a,b,c,d));arr=np.asarray(piece).astype(float)/255
        lin=srgb_to_linear(arr[:,:,:3]);gray=lin@np.array([.2126,.7152,.0722]);lin=lin*.80+gray[:,:,None]*.20;lin=lin*.84+.035
        faded=np.concatenate((linear_to_srgb(lin),arr[:,:,3:4]),2)
        y=b+90;image.paste(Image.fromarray(np.uint8(np.clip(faded,0,1)*255+.5)),(a,y));records[key]['faded']=(a,y,c,y+d-b)
    def centered(text,rect,face,ink,maximum):
        ff=ImageFont.truetype(str(find_font(face,'Bold')),maximum)
        while dr.textbbox((0,0),text,font=ff)[2]>rect[2]-rect[0]-10:ff=ImageFont.truetype(ff.path,ff.size-1)
        bb=dr.textbbox((0,0),text,font=ff);dr.text(((rect[0]+rect[2]-bb[0]-bb[2])/2,(rect[1]+rect[3]-bb[1]-bb[3])/2),text,font=ff,fill=ink)
    # Spend the existing ink pixels on signs that are actually seen close.
    # Addresses need a few digits, not half a thousand pixels per label.
    for i,(key,t) in enumerate(TENANTS.items()):
        old=records[key]['window'];dr.rectangle(old,fill=(255,255,255,0));x,y=old[:2];r=(x,y,x+240,y+180)
        dr.rectangle(r,fill='#E6DFCC' if key=='vacant' else '#1D282B')
        for text,yy,fs in ((('FOR LEASE' if key=='vacant' else 'OPEN'),0,38),(('INQUIRE AT OFFICE' if key=='vacant' else 'MON - SAT  9 - 7'),65,18),(('RETAIL SPACE' if key=='vacant' else t['subtitle']),119,19)):
            centered(text,(x+6,y+yy,x+234,y+yy+53),'DejaVu Sans','#753C32' if key=='vacant' else '#E2D5B8',fs)
        records[key]['window']=r
    for i,(key,t) in enumerate(TENANTS.items()):
        index=22+i;x=(index%4)*512+12;y=(index//4)*204+12;r=(x,y,x+488,y+150)
        dr.rectangle(r,fill=t['field']);face='DejaVu Serif' if t['font']=='serif' else 'DejaVu Sans';words=t['name'].split()
        if len(words)>1:
            centered(' '.join(words[:-1]),(x+8,y+3,x+480,y+56),face,t['ink'],52)
            centered(words[-1],(x+8,y+53,x+480,y+108),face,t['ink'],52)
        else:centered(t['name'],(x+8,y+12,x+480,y+108),face,t['ink'],66)
        centered(t['subtitle'],(x+8,y+113,x+480,y+146),'DejaVu Sans',t['ink'],23);records[key]['tower']=r
    for i,address in enumerate(str(110+2*j) for j in range(12)):
        x=12+i*150;r=(x,1990,x+140,2038);dr.rectangle(r,fill='#22282A');centered(address,r,'DejaVu Sans','#EEEBDC',34);records[address]['sign']=r
    catalogue=json.loads(Path('textures/ship/graphics.json').read_text());shared=Image.open('textures/ship/T_CommercialGraphics_BaseColor.png').convert('RGBA');extra={}
    def place(key,index,piece):
        i=index-22
        if i<9:
            slot=9+i;x=(slot%4)*512+272;y=(slot//4)*204+16;w=224;h=172
        else:x,y,w,h=1536,1845,480,110
        image.paste(piece.resize((w,h),Image.Resampling.LANCZOS),(x,y));extra[key]=(x+5,y+4,x+w-5,y+h-4)
    for i,key in enumerate(('Oil0','Oil1','Oil2','Oil3','Tire','Gum','Salt','Grime','Scuff','Rust')):
        a,b,c,d=catalogue['Wear:'+key]['rect'];crop=shared.crop((round(a*1024),round((1-d)*1024),round(c*1024),round((1-b)*1024)))
        if key=='Rust':
            rng=np.random.default_rng(618);h,w=176,960;y,x=np.mgrid[:h,:w];u=x/w;v=y/h
            coarse=np.asarray(Image.fromarray(rng.random((7,39)).astype('float32')).resize((w,h),Image.Resampling.BICUBIC))
            wet=.16+.48*(.5+.5*np.sin(u*39+coarse*3))**2
            alpha=np.clip((v-(1-wet))/.055,0,1)*np.clip((coarse-.29)*3.3,0,1)*.80
            grain=rng.random((h,w));rgb=np.stack((.115+.07*grain,.040+.02*grain,.014+.009*grain),2)
            a=np.concatenate((linear_to_srgb(rgb),alpha[:,:,None]),2);crop=Image.fromarray(np.uint8(np.clip(a,0,1)*255+.5))
        if key=='Grime':
            h,w=176,960;y,x=np.mgrid[:h,:w];u=x/w;v=1-y/h;alpha=np.zeros((h,w))
            smooth=lambda a:np.clip(a,0,1)**2*(3-2*np.clip(a,0,1))
            for j in range(4):
                center=.31+j*.105+.014*np.sin(v*(7+j)+j);radius=.018+.008*v
                alpha+=.14*np.exp(-((u-center)/radius)**2)*smooth((v-.13*j)/.24)*smooth((1-v)/.04)
            alpha+=.12*np.exp(-((u-.49)/.21)**2)*smooth(v/.40)*smooth((1-v)/.05)
            rgb=np.broadcast_to(linear_to_srgb(np.array((.075,.068,.055))),(h,w,3));a=np.dstack((rgb,np.clip(alpha,0,.46)))
            crop=Image.fromarray(np.uint8(a*255+.5))
        if key=='Tire':
            a=np.asarray(crop).copy();a[:,:,3]=(a[:,:,3].astype(float)*.55).astype('uint8');crop=Image.fromarray(a)
        place('Wear:'+key,22+i,crop)
    # Lamp swatches are opaque white diffusers. All light classes still share
    # the same material; radiance varies in the 1K map, selected by UV1.
    for i,key in enumerate(('InteriorLamp','WalkLamp','WallLamp','LotLamp','Blank')):
        x=16+i*90;y=1740;r=(x,y,x+65,y+55);dr.rectangle(r,fill='#E6E4DC');extra[key]=r
    r=(1552,1735,2028,1815);dr.rectangle(r,fill=(255,255,255,0))
    ff=ImageFont.truetype(str(find_font('DejaVu Sans','Bold')),44)
    dr.text((r[0]+8,r[1]+12),'FEN ROW VIDEO',font=ff,fill=(154,158,146,102),stroke_width=0);extra['Ghost']=r
    # Dark retained deposits and corrosion carry zero radiance, including all
    # of the spare chart guards.
    a=np.asarray(image).astype('float32')/255;rgb=srgb_to_linear(a[:,:,:3]);em=np.zeros_like(rgb)
    for key,data in records.items():
        if key not in TENANTS and 'SHOPS' not in key and 'COURT' not in key and 'COMMONS' not in key:continue
        for kind in ('sign','tower','faded'):
            if kind not in data:continue
            x0,y0,x1,y1=map(round,data[kind]);style=data.get('style','box');strength=.85 if style=='channel' else .30 if style=='panel' else .55
            em[y0:y1,x0:x1]=rgb[y0:y1,x0:x1]*a[y0:y1,x0:x1,3:4]*strength/300
    for key,power in (('InteriorLamp',16),('WalkLamp',28),('WallLamp',15),('LotLamp',48)):
        x0,y0,x1,y1=extra[key];em[y0:y1,x0:x1]=rgb[y0:y1,x0:x1]*power/300
    # Linear averaging preserves the authored radiance; 16-bit keeps low sign
    # outputs distinct from the fixture outputs with one common glTF scalar.
    em=em.reshape(1024,2,1024,2,3).mean(axis=(1,3));write_png(out/'T_StripSigns_Emission.png',linear_to_srgb(em),bits=16)
    for key,r in extra.items():
        x0,y0,x1,y1=r;records[key]={'sign':(x0,y0,x1,y1)}
    return records
