"""Original ranch source fields, independent of every accepted colonial image.

Four 512 brick tiles, a 1024 two-finish roof atlas, and a 1024 ORM-only
trim variant add 9 1/3 MiB with mips: 47 1/3 MiB including the original family.
No photographic pixel enters a generated field. Sources may be built at 4K.
"""
from pathlib import Path
import numpy as np
from textures import noise
from kit.image_io import write_png,linear_to_srgb

BRICK_COLORS=dict(red=(.235,.113,.068),red_brown=(.165,.078,.050),buff=(.39,.28,.17),tan=(.29,.205,.135))


def save_maps(folder,name,color,h,ao,rough,metal,coverage):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 dx=(np.roll(h,-1,axis=1)-np.roll(h,1,axis=1))/(2*coverage[0]/h.shape[1])
 dy=(np.roll(h,-1,axis=0)-np.roll(h,1,axis=0))/(2*coverage[1]/h.shape[0])
 nm=np.stack([-dx,dy,np.ones_like(h)],axis=-1);nm/=np.linalg.norm(nm,axis=-1,keepdims=True)
 for channel,data in dict(BaseColor=linear_to_srgb(color),Normal=nm*.5+.5,ORM=np.stack([ao,rough,metal],axis=-1)).items():write_png(folder/f'T_{name}_{channel}.png',data,bits=8)
 # Retain the authored relief for the delivery bake without changing any
 # accepted checkpoint RGB image or random sequence.
 lo=float(h.min());distance=max(.00001,float(h.max())-lo)
 write_png(folder/f'T_{name}_Height.png',((h-lo)/distance)[:,:,None],bits=16)
 import json
 (folder/f'{name}-height.json').write_text(json.dumps(dict(height_distance_m=distance,coverage_m=coverage)))


def brick(folder,kind,n=512):
 rng=np.random.default_rng(8301);coverage=1.2192;y,x=np.mgrid[0:n,0:n].astype('float32');x=x/n*coverage;y=(n-1-y)/n*coverage
 cw=.2032;ch=.2032/3;row=np.floor(y/ch).astype(int);shift=(row%2)*cw/2
 xx=np.mod(x+shift,cw);col=np.floor((x+shift)/cw).astype(int)%6;yy=np.mod(y,ch)
 edge=np.minimum.reduce([xx,cw-xx,yy,ch-yy]);mask=np.clip((edge-.0045)/.0028,0,1)
 fine=rng.random((n,n)).astype('float32');mid=noise(n,64,rng)
 # Fired units have independent body color and iron-flashed ends, never a
 # single noise wash over a wall. Mortar stays pale and a full 9 mm recessed.
 table=rng.uniform(.58,1.38,(18,6));unit=table[row%18,col]
 flashed=rng.random((18,6))[row%18,col]>.66
 ends=np.exp(-xx/.037)+.7*np.exp(-(cw-xx)/.018)
 flash=1-.32*flashed*np.minimum(1,ends)
 body=np.array(BRICK_COLORS[kind])/.72*(unit*flash*(.93+.14*mid))[:,:,None]
 mortar=np.array([.33,.305,.257])/.72*(.96+.08*mid)[:,:,None]
 color=body*mask[:,:,None]+mortar*(1-mask[:,:,None])
 h=.009*mask+.00055*(mid-.5)*mask+.00015*(fine-.5)
 save_maps(folder,'RanchBrick',color,h,.72+.28*mask,.86+.10*fine,np.zeros_like(h),(coverage,coverage))


def roof(folder,n=1024):
 # Upper half architectural, lower half three-tab. Both have the same
 # 5 5/8 in exposure. Lower source density is 210 px/m at 1024 delivery.
 rng=np.random.default_rng(9824);y,x=np.mgrid[0:n,0:n].astype('float32');x=x/n*4.8768
 strip=(y>=n/2).astype(int);local=np.mod(n-1-y,n/2)/(n/2)*2.4384
 exposure=2.4384/17;row=np.floor(local/exposure).astype(int);v=np.mod(local,exposure)/exposure
 fine=rng.random((n,n)).astype('float32');mid=noise(n,64,rng)
 color=np.zeros((n,n,3),dtype='float32');h=np.zeros((n,n),dtype='float32');ao=np.ones_like(h)
 for style in (0,1):
  for j in range(17):
   mask=(strip==style)&(row==j)
   if style==0:
    # Laminated dimensional tabs, varied lengths and stagger per course.
    boundaries=np.cumsum(rng.uniform(.11,.35,28));boundaries=boundaries/boundaries[-1]*4.8768
    col=np.searchsorted(boundaries,np.mod(x+j*.271,4.8768));table=rng.uniform(.93,1.09,29)
    value=table[col];lam=((col+j*3)%5<2)&(v<.48)
    height=.0025*v+.0012*lam
   else:
    col=np.floor(np.mod(x+(j%2)*.1524,4.8768)/.3048).astype(int);table=rng.uniform(.92,1.08,17)
    value=table[col];slot=np.mod(x+(j%2)*.1524,.3048)<.007
    height=.0024*v-.0015*slot*(v<.75)
   base=.17*value*(.83+.34*fine)*(1-.22*np.exp(-v/.04))
   if style==1:base*=np.where(slot&(v<.75),.28,1.)
   color[mask]=np.stack([base,base*.965,base*.90],axis=-1)[mask]
   h[mask]=height[mask]+.0003*(fine[mask]-.5);ao[mask]=1-.18*np.exp(-v[mask]/.04)
 save_maps(folder,'RanchRoof',color,h,ao,.84+.14*fine,np.zeros_like(h),(4.8768,4.8768))


def trim_orm(folder,source):
 """A 1024 linear ORM variant only; color/normal and all glass maps are shared."""
 from PIL import Image
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 a=np.asarray(Image.open(source).convert('RGB').resize((1024,1024),Image.Resampling.BOX)).astype('float32')/255
 y,x=np.mgrid[0:1024,0:1024];strip=np.floor((1023-y)/1024*8).astype(int)
 rng=np.random.default_rng(1714);mid=noise(1024,32,rng)
 painted=(strip==0)|(strip==2)|(strip==3)
 a[:,:,1][painted]=np.maximum(a[:,:,1][painted],.61+.07*mid[painted])
 metal=(strip==5)&(x>1024*.75);oxide=.58+.35*mid[metal]
 a[:,:,1][metal]=.48+.34*oxide;a[:,:,2][metal]*=1-.65*oxide
 write_png(folder/'T_RanchTrim_ORM.png',a,bits=8)
