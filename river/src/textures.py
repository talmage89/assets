"""Original temporary bank field, botanical coverage and ripple normal.

CPU analytic quick materials for the form gate; no reference pixel inputs.
Final high-source manufacture baking is deliberately deferred.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


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
    dy,dx=np.gradient(height,n and 2/n)
    normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2);normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    Image.fromarray(np.uint8((normal*.5+.5)*255)).save(folder/'T_RiverBank_Normal.png')
    orm=np.zeros((n,n,3),np.uint8);orm[:,:,0]=255;orm[:,:,1]=220
    Image.fromarray(orm).save(folder/'T_RiverBank_ORM.png')
    # Reed/grass silhouette sheet: sixteen independently generated clumps.
    im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
    for j in range(16):
        ox=j%4*128;oy=j//4*128
        for k in range(28):
            base=ox+rng.uniform(30,98);h=rng.uniform(28,116);bend=rng.uniform(-31,31)
            pts=[(base,oy+126),(base+bend*.40,oy+126-h*.55),(base+bend,oy+126-h)]
            col=(int(rng.uniform(49,90)),int(rng.uniform(61,100)),int(rng.uniform(24,43)),255)
            d.line(pts,fill=col,width=int(rng.integers(1,4)))
            if j>11 and k%5==0:d.line([pts[2],(pts[2][0]+1,pts[2][1]-14)],fill=(63,43,24,255),width=4)
    im.save(folder/'T_RiverPlants_BaseColor.png')
    n=512;y,x=np.mgrid[:n,:n]/n
    h=.0025*np.sin(2*np.pi*(x*11+y*4)+.8*np.sin(y*np.pi*6))
    h+=.0011*np.sin(2*np.pi*(x*29-y*9))+.0005*np.cos(2*np.pi*(x*53+y*31))
    dy,dx=np.gradient(h,2/n);normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2)
    normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    Image.fromarray(np.uint8((normal*.5+.5)*255)).save(folder/'T_RiverWater_Normal.png')


if __name__=='__main__': generate()
