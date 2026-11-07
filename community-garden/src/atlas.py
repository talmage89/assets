"""Original outline-only checkpoint leaf tiles, never photographic pixels."""
from pathlib import Path
import math
import numpy as np
from PIL import Image

SPECIES=('tomato','pepper','squash','bean','corn','lettuce','kale','herb','sunflower','marigold','weed')
COLORS=((57,101,26),(45,90,22),(64,105,34),(50,99,31),(66,107,33),(95,135,46),
        (49,86,61),(62,109,35),(65,105,32),(53,90,26),(90,108,38))


def rect(species):
    i=SPECIES.index(species);x=i%4;y=i//4
    return (x/4+.003,y/4+.003,(x+1)/4-.003,(y+1)/4-.003)


def generate(folder,size=1024):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    bc=np.zeros((size,size,4),np.uint8);nm=np.full((size,size,3),(128,128,255),np.uint8)
    orm=np.full((size,size,3),(255,190,0),np.uint8)
    for i,sp in enumerate(SPECIES):
        u0,v0,u1,v1=rect(sp);xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size)
        h,w=yb-ya,xb-xa;x,y=np.meshgrid(np.linspace(-1,1,w),np.linspace(1,0,h))
        t=np.clip((y-.025)/.95,0,1);width=np.sin(math.pi*t)**.78
        if sp=='squash':width*=.78+.22*np.cos(t*math.pi*8);width*=1-.28*np.exp(-((t-.12)/.09)**2)
        elif sp=='kale':width*=.84+.16*np.sin(t*math.pi*22)
        elif sp=='tomato':width*=.88+.12*np.sin(t*math.pi*18)
        elif sp=='bean':width*=1-.48*t
        elif sp=='corn':width=np.sin(math.pi*t)**.38*(1-.30*t)
        elif sp=='lettuce':width=np.sin(math.pi*t)**.52*(.94+.06*np.sin(t*54))
        elif sp=='sunflower':width*=1-.28*t
        mask=(abs(x)<width*.94)&(y>.025)&(y<.975)
        vein=np.exp(-(x/.016)**2)*.08
        c=np.array(COLORS[i])[None,None,:]*(1+vein[:,:,None])
        tile=bc[ya:yb,xa:xb];tile[:,:,:3]=np.clip(c,0,255);tile[:,:,3]=mask*255
    # A reserved non-botanical tile shares this checkpoint allocation: 15mm
    # bird netting over .48m, approximately .8mm strands. No extra image set.
    n=size//4;yy,xx=np.mgrid[0:n,0:n];pitch=n/32
    wire=(np.minimum(xx%pitch,pitch-xx%pitch)<n*.0008/.48/2)|(np.minimum(yy%pitch,pitch-yy%pitch)<n*.0008/.48/2)
    bc[:n,:n,:3]=(36,41,31);bc[:n,:n,3]=wire*255
    for c,a in [('BaseColor',bc),('Normal',nm),('ORM',orm)]:Image.fromarray(a).save(folder/f'T_GardenPlants_{c}.png')


if __name__=='__main__':generate('textures/checkpoint')
