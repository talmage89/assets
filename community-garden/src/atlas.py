"""Analytic species leaves: venation, real greens, old lower blades and bites.

Generated at 4K, filtered to the accepted 1K/4 MiB allocation. Photos are
comparison inputs only. Each species has healthy and senescent half tiles.
"""
from pathlib import Path
import math,sys
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png
SPECIES=('tomato','pepper','squash','bean','corn','lettuce','kale','herb','sunflower','marigold','weed')
COLORS=((64,110,43),(55,101,40),(47,88,54),(56,108,43),(67,112,43),(100,132,68),
        (68,105,89),(57,111,45),(53,90,32),(43,81,28),(85,105,41))

def rect(species,old=False):
    i=SPECIES.index(species);x=i%4;y=i//4
    return (x/4+.003+(.125 if old else 0),y/4+.003,x/4+(.247 if old else .122),(y+1)/4-.003)

def flower_rect(name):
    x={'Flower':1,'Yellow':2,'Spent':3}.get(name,1)
    return (x/4+.003,.753,(x+1)/4-.003,.997)

def generate(folder,size=4096):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    bc=np.zeros((size,size,4),np.uint8);nm=np.full((size,size,3),(128,128,255),np.uint8);orm=np.full((size,size,3),(255,173,0),np.uint8)
    for i,sp in enumerate(SPECIES):
      for old in (False,True):
        u0,v0,u1,v1=rect(sp,old);xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size)
        h,w=yb-ya,xb-xa;x,y=np.meshgrid(np.linspace(-1,1,w),np.linspace(1,0,h));t=np.clip((y-.025)/.95,0,1)
        width=np.sin(math.pi*t)**.78
        if sp=='kale':width*=.84+.16*np.sin(t*math.pi*22)
        elif sp=='tomato':width*=.86+.14*np.sin(t*math.pi*18)
        elif sp=='bean':width*=1-.38*t
        elif sp=='corn':width=np.sin(math.pi*t)**.42*(1-.22*t)
        elif sp=='lettuce':width=np.sin(math.pi*t)**.52*(.94+.06*np.sin(t*54))
        elif sp=='sunflower':width*=1-.28*t
        mask=(abs(x)<width*.94)&(y>.025)&(y<.975)
        vein=np.exp(-(x/.018)**2)
        # Pinnate secondaries meet the midrib. Five radiating squash veins.
        secondary=np.exp(-(np.sin((y-abs(x)*.18)*math.pi*9)/.08)**2)*(1-abs(x))
        if sp=='squash':
            dy=(y-.52)*2;angle=np.arctan2(dy,x)
            # Zucchini has pointed palmate lobes, rather than a rounded
            # pumpkin-like scallop. Fine teeth remain in alpha, not geometry.
            delta=(angle-math.pi/2+math.pi/5)%(2*math.pi/5)-math.pi/5
            radius=(.50+.46*(1-abs(delta)/(math.pi/5))**1.4)*(.965+.035*np.sin(angle*39))
            mask=(np.hypot(x,dy)<radius)&(y>.025)&(y<.975);mask|=(abs(x)<.019)&(y>.025)&(y<.34)
            vein=np.zeros_like(x)
            for a in np.linspace(-math.pi*.3,math.pi*1.3,5):
                dx=x;dz=y-.17;along=dx*math.cos(a)+dz*math.sin(a);dist=abs(-dx*math.sin(a)+dz*math.cos(a))
                vein=np.maximum(vein,np.exp(-(dist/.014)**2)*(along>0))
            secondary=vein*.5
        if sp=='marigold':
            mask=(abs(x)<.020)&(y>.025)&(y<.95)
            for j in range(5):
                cy=.18+j*.145;leaf=((abs(x)-.37)/.49)**2+((y-cy-.08*abs(x))/.055)**2<1
                mask|=leaf & (abs(x)>.025)
            mask|=((x/.15)**2+((y-.90)/.085)**2<1)
        mask|=(abs(x)<.018)&(y<.17)
        if sp not in ('corn','marigold'):
            # A few margin bites, not a noise wash or perforated healthy canopy.
            for bx,by,r in ((-.66,.48,.055),(.57,.65,.038)):
                if old:mask&=((x-bx)**2+(y-by)**2>r*r)
        fine=np.sin(x*137+y*41)*np.sin(y*211-x*33)
        tone=.86+.19*y+.045*np.sin(x*11+y*8)+.018*fine
        c=np.array(COLORS[i])[None,None,:]*tone[:,:,None]+(vein*.65+secondary*.18)[:,:,None]*np.array([14,19,7])
        if sp=='squash':
            silver=np.zeros_like(x);patch_rng=np.random.default_rng(731)
            for a in (math.pi/2,.40,.86,math.pi-.40,math.pi-.86):
                ca,sa=math.cos(a),math.sin(a)
                for k in range(7):
                    at=.16+k*.092+patch_rng.uniform(-.02,.02);off=patch_rng.uniform(-.055,.055)
                    cx=at*ca-off*sa;cy=.17+at*sa+off*ca;dx=x-cx;dy=y-cy
                    cross=-dx*sa+dy*ca;forward=dx*ca+dy*sa
                    patch=np.exp(-(cross/patch_rng.uniform(.023,.052))**2-(forward/patch_rng.uniform(.025,.059))**2)*patch_rng.uniform(.26,.68)
                    silver=np.maximum(silver,patch)
            c+=silver[:,:,None]*np.array([93,104,89])
        if old:
            # Senescence follows older basal tissue, green persists along ribs.
            edge=np.clip(abs(x)/np.maximum(width,.1),0,1);age=.35+.35*edge
            c=c*(1-age[:,:,None])+np.array([126,112,42])*age[:,:,None]
        bc[ya:yb,xa:xb,:3]=np.clip(c,0,255);bc[ya:yb,xa:xb,3]=mask*255
        height=vein*.001+secondary*.00020+fine*.000008
        gy,gx=np.gradient(height,.25/h,.12/w);normal=np.stack((-gx,gy,np.ones_like(gx)),axis=-1);normal/=np.linalg.norm(normal,axis=-1)[:,:,None]
        nm[ya:yb,xa:xb]=np.uint8(np.clip((normal*.5+.5)*255,0,255));orm[ya:yb,xa:xb,1]=np.uint8(161+old*24+fine*4)
    # Supported tomato branchlets, nine overlapping leaflets per alpha card.
    # Shared shrub/tree idiom: texture gives fine leaflet geometry at low cost.
    xa,xb=round(.753*size),round(.997*size);ya,yb=round(.253*size),round(.497*size)
    h,w=yb-ya,xb-xa;xx,yy=np.meshgrid(np.linspace(0,1,w),np.linspace(1,0,h));mask=(abs(xx-.5)<.004);color=np.zeros((h,w,3));color[:]=[64,103,35]
    normal=np.full((h,w,3),(128,128,255),np.uint8)
    sites=[(.5,.76,0,.235,.10)]+[(.5,.16+j*.155,side*1.16,.30-j*.025,.105-j*.009) for j in range(4) for side in (-1,1)]
    for k,(bx,by,a,length,width) in enumerate(sites):
        dx,dy=xx-bx,yy-by;along=dx*math.sin(a)+dy*math.cos(a);cross=dx*math.cos(a)-dy*math.sin(a);t=along/length
        outline=np.maximum(0,np.sin(math.pi*np.clip(t,0,1)))**.7*(.88+.12*np.sin(t*math.pi*15+cross*8))
        blade=(t>0)&(t<1)&(abs(cross)<width*outline*.5);mask|=blade
        rib=np.exp(-(cross/.003)**2);secondary=np.exp(-(np.sin((t-abs(cross)*2)*math.pi*7)/.12)**2)
        shade=.88+.10*t+.05*math.sin(k*3.4);c=np.array(COLORS[0])[None,None,:]*shade[:,:,None]+(rib*.60+secondary*.08)[:,:,None]*np.array([13,17,7])
        color[blade]=c[blade]
        nx=-(cross/max(width,.01))*.2;ny=(t-.5)*.12;nn=np.stack((nx,ny,np.ones_like(nx)),axis=-1);nn/=np.linalg.norm(nn,axis=-1)[:,:,None];normal[blade]=np.uint8((nn[blade]*.5+.5)*255)
    bc[ya:yb,xa:xb,:3]=np.uint8(np.clip(color,0,255));bc[ya:yb,xa:xb,3]=mask*255;nm[ya:yb,xa:xb]=normal
    # Composite marigold heads for field specimens: ruffled ray florets and
    # a compact disc, with cutout coverage. All texels are analytic.
    for name,color in [('Flower',(198,115,24)),('Yellow',(220,173,42)),('Spent',(105,78,40))]:
        u0,v0,u1,v1=flower_rect(name);xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size)
        yy,xx=np.meshgrid(np.linspace(-1,1,yb-ya),np.linspace(-1,1,xb-xa),indexing='ij');rr=np.hypot(xx,yy);phi=np.arctan2(yy,xx)
        radius=.78+.09*np.cos(phi*13)+.035*np.sin(phi*27);mask=rr<radius
        corr=.72+.20*np.sin(rr*29+np.sin(phi*13)*1.5)+.08*np.cos(phi*13)
        c=np.array(color)[None,None,:]*corr[:,:,None];bc[ya:yb,xa:xb,:3]=np.uint8(np.clip(c,0,255));bc[ya:yb,xa:xb,3]=mask*255
        orm[ya:yb,xa:xb,1]=202
    n=size//4;yy,xx=np.mgrid[0:n,0:n];pitch=n/32
    # Conservative source-pixel coverage keeps the fine net visible after
    # 4K-to-1K filtering and the shared cutout threshold.
    wire=(np.minimum(xx%pitch,pitch-xx%pitch)<max(n*.0008/.48/2,2.0))|(np.minimum(yy%pitch,pitch-yy%pitch)<max(n*.0008/.48/2,2.0))
    bc[:n,:n,:3]=(36,41,31);bc[:n,:n,3]=wire*255
    for c,a in [('BaseColor',bc),('Normal',nm),('ORM',orm)]:write_png(folder/f'T_GardenPlants_{c}.png',a.astype(np.float32)/255)

if __name__=='__main__':generate('textures/4k-plants')
