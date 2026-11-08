"""Original temporary bank field, botanical coverage and ripple normal.

CPU analytic quick materials for the form gate; no reference pixel inputs.
Final high-source manufacture baking is deliberately deferred.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def generate(folder=Path('textures/checkpoint')):
    folder.mkdir(parents=True,exist_ok=True);n=1024
    y,x=np.mgrid[:n,:n]/n;rng=np.random.default_rng(716)
    grain=rng.random((n,n))-.5
    field=.5*np.sin(x*39+y*25)+.3*np.cos(y*71-x*17)
    rgb=np.zeros((n,n,4));rgb[:,:,:3]=(.29,.255,.185);rgb[:,:,3]=1
    rgb[:,:,:3]+=((field*.020+grain*.035)[:,:,None])
    height=grain*.0004
    # Elliptic, irregular pebbles over silt. Deterministic periodic placement.
    for i in range(1100):
        cx,cy=rng.random(2);r=rng.uniform(.004,.022);asp=rng.uniform(.55,1.4)
        dx=(x-cx+.5)%1-.5;dy=(y-cy+.5)%1-.5
        q=(dx/r)**2+(dy/(r*asp))**2;mask=q<1
        shade=rng.uniform(.22,.48);tint=np.array((shade*1.04,shade,shade*.88))
        v=np.sqrt(np.maximum(0,1-q));h=r*.25*v
        rgb[mask,:3]=tint+v[mask,None]*.025+grain[mask,None]*.018
        height=np.maximum(height,h)
    Image.fromarray(np.uint8(np.clip(rgb,0,1)*255)).save(folder/'T_RiverBank_BaseColor.png')
    dy,dx=np.gradient(height,2/n)
    normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2);normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    Image.fromarray(np.uint8((normal*.5+.5)*255)).save(folder/'T_RiverBank_Normal.png')
    orm=np.zeros((n,n,3),np.uint8);orm[:,:,0]=255;orm[:,:,1]=220
    Image.fromarray(orm).save(folder/'T_RiverBank_ORM.png')
    # Eight bank colonies occupy the lower half. The upper half carries the
    # plaques and four alpha maintenance masks; no extra image allocation.
    im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
    for j in range(4):
        ox=j%2*128;oy=128+j//2*64
        for k in range(120):
            px=rng.uniform(3,124);py=31+math.sin(px*.083+j)*rng.uniform(2,13)+rng.normal(0,6)
            r=rng.uniform(.5,2.5);alpha=int(rng.uniform(70,230))
            d.ellipse((ox+px-r,oy+py-r*.55,ox+px+r,oy+py+r*.55),fill=(202,205,181,alpha))
    for j in range(8):
        ox=j%4*128;oy=256+j//4*128
        for k in range(23):
            base=ox+rng.uniform(25,103);h=rng.uniform(34,110);bend=rng.uniform(-38,38)
            pts=[(base,oy+126),(base+bend*.30,oy+126-h*.52),(base+bend*.72,oy+126-h*.86),(base+bend,oy+126-h)]
            value=rng.uniform(.75,1.12)
            col=tuple(int(v*value) for v in ((110,142,62) if k%6 else (154,144,81)))+(255,)
            d.line(pts,fill=col,width=int(rng.integers(2,4)))
            if j>=6 and k%4==0:
                tip=pts[-1];d.line([tip,(tip[0]+1,tip[1]-14)],fill=(104,76,43,255),width=4)
            elif k%6==0:
                tip=pts[-1]
                for n in range(5):
                    yy=tip[1]+n*2;d.line([(tip[0]-5+n,yy+3),(tip[0],yy),(tip[0]+5-n,yy+3)],fill=(158,150,91,255),width=1)
    # Streak masks: gravity fingers are softened, interrupted and broad at
    # their source. Patches follow irregular chipped outlines, never spikes.
    for j in range(4):
        py,px=np.mgrid[:128,:128]/127;mask=np.zeros((128,128))
        if j<2:
            for k in range(18):
                cx=rng.uniform(.08,.92);width=rng.uniform(.010,.065);length=rng.uniform(.15,1.0)
                mask=np.maximum(mask,np.exp(-((px-cx-.012*np.sin(py*19+k))/width)**2)*np.clip((length-py)*7,0,1)*np.clip((1-py)*3,0,1))
            mask*=.55+.45*rng.random((128,128))
        else:
            q=((px-.5)/.45)**2+((py-.5)/.39)**2
            boundary=.90+.13*np.sin(px*24+py*17)+.07*np.sin(py*39-px*33)
            mask=np.clip((boundary-q)*8,0,1)*(.65+.35*rng.random((128,128)))
        col=(90,91,80) if j==0 else (211,207,183) if j==1 else (156,154,138) if j==2 else (178,173,155)
        rgba=np.zeros((128,128,4),np.uint8);rgba[:,:,:3]=col;rgba[:,:,3]=np.uint8(mask*(120 if j==1 else 165))
        im.paste(Image.fromarray(rgba),(256+j%2*128,j//2*128))
    # Two tiny plaque legends reuse this same image, outside all plant charts.
    font=find_font('DejaVu Sans','Book')
    for y,year in ((0,1974),(60,1968)):
        d.rectangle((0,y,255,y+55),fill=(47,49,44,255))
        d.text((128,y+3),'CEDAR RUN',font=ImageFont.truetype(font,22),anchor='mt',fill=(186,184,159,255))
        d.text((128,y+32),str(year)+'  COUNTY WORKS',font=ImageFont.truetype(font,12),anchor='mt',fill=(171,168,149,255))
    im.save(folder/'T_RiverPlants_BaseColor.png')
    n=512;y,x=np.mgrid[:n,:n]/n
    # Several wind/current wave trains, with different phases and scales.
    # Integer modes tile exactly without a dominant regular comb.
    rng=np.random.default_rng(381);h=np.zeros((n,n))
    for i in range(18):
        kx=int(rng.integers(3,54));ky=int(rng.integers(-24,25))
        amplitude=.0007/(1+math.hypot(kx,ky)/18)
        h+=amplitude*np.sin(2*np.pi*(kx*x+ky*y)+rng.uniform(0,6.28)+.6*np.sin(2*np.pi*(x*2+y*3)+i))
    dy,dx=np.gradient(h,2/n);normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2)
    normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    Image.fromarray(np.uint8((normal*.5+.5)*255)).save(folder/'T_RiverWater_Normal.png')


if __name__=='__main__': generate()
