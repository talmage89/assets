"""Analytic original mesh and crossed coil impostors; no reference pixels.

Three reserved regions are written after downsampling, preserving physical
thread scale without spending a unique atlas over 35 square meters of net.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from PIL import Image
from dimensions import *

def linear_srgb(c):return np.where(c<=.0031308,12.92*c,1.055*np.maximum(c,0)**(1/2.4)-.055)
def woven(w,h,mat=False,wear=.65):
 ss=4;x=(np.arange(w*ss)+.5)/(w*ss)*TILE;y=(np.arange(h*ss)+.5)/(h*ss)*TILE
 x,y=np.meshgrid(x,y);pitch=.004 if mat else .008;wire=.0032 if mat else .00125
 # Periodic over-under weave, with a lightly weathered fiber surface.
 dx=(x+pitch/2)%pitch-pitch/2;dy=(y+pitch/2)%pitch-pitch/2
 mask=(abs(dx)<wire/2)|(abs(dy)<wire/2)
 hx=np.sqrt(np.maximum(0,(wire/2)**2-dx**2));hy=np.sqrt(np.maximum(0,(wire/2)**2-dy**2))
 height=np.maximum(hx,hy);gy,gx=np.gradient(height,TILE/(h*ss),TILE/(w*ss))
 normal=np.stack([-gx,-gy,np.ones_like(x)],axis=2);normal/=np.linalg.norm(normal,axis=2,keepdims=True);normal*=mask[:,:,None]
 normal=normal.reshape(h,ss,w,ss,3).sum(axis=(1,3));normal/=np.maximum(np.linalg.norm(normal,axis=2,keepdims=True),1e-8)
 normal[np.linalg.norm(normal,axis=2)<.1]=(0,0,1)
 alpha=mask.reshape(h,ss,w,ss).mean(axis=(1,3))
 fuzz=.5+.5*np.sin(x*4597+y*137)*np.cos(y*3151-x*31)
 factor=wear/.65
 value=(.0025+factor*.0015+fuzz*(.001+factor*.001)) if mat else (.008+factor*.012+fuzz*(.002+factor*.007))
 col=np.stack([value*.91,value,value*.96],axis=2).reshape(h,ss,w,ss,3).mean(axis=(1,3))
 return np.dstack([linear_srgb(col),alpha]),normal*.5+.5,np.dstack([np.ones_like(alpha),np.full_like(alpha,.89),np.zeros_like(alpha)])

def spring(w,h,wear=.65):
 ss=4;xs=(np.arange(w*ss)+.5)/(w*ss)*SPRING_LENGTH;ys=((np.arange(h*ss)+.5)/(h*ss)-.5)*SPRING_WIDTH
 x,y=np.meshgrid(xs,ys);distance=np.full_like(x,1.)
 # A coil seen from the side: a projected helix, plus the two hooked ends
 # and a triangular mat ring. The crossed card supplies the other azimuth.
 t=np.linspace(0,math.tau*28,420);cx=.031+t/(math.tau*28)*.124;cy=.008*np.cos(t)
 paths=[list(zip(cx,cy)),[(.031,.008),(.019,.008),(.012,.002),(.019,-.005),(.026,-.003)],[(.155,.008),(.182,.008),(.190,.001),(.183,-.006),(.175,-.004)],[(.012,.002),(.001,-.010),(.001,.011),(.012,.002)]]
 for path in paths:
  for (xa,ya),(xb,yb) in zip(path,path[1:]):
   vx,vy=xb-xa,yb-ya;t=np.clip(((x-xa)*vx+(y-ya)*vy)/(vx*vx+vy*vy),0,1)
   d=np.sqrt((x-xa-t*vx)**2+(y-ya-t*vy)**2);distance=np.minimum(distance,d)
 wire=.0016;mask=distance<wire;alpha=mask.reshape(h,ss,w,ss).mean(axis=(1,3))
 rust=(x<.032)|(x>.157);fleck=.5+.5*np.sin(x*1719+y*1291)*np.sin(y*1211-x*331)
 oxide=rust & (fleck>(.90-.61*wear/.65)) & (wear>0)
 color=np.where(oxide[:,:,None],np.array([.18,.064,.019]),np.array([.37,.40,.40]))
 # Shading describes round steel wire in the original analytic color/normal.
 height=np.sqrt(np.maximum(0,wire*wire-distance*distance))
 col=linear_srgb(color).reshape(h,ss,w,ss,3).mean(axis=(1,3))
 gy,gx=np.gradient(height,SPRING_WIDTH/(h*ss),SPRING_LENGTH/(w*ss))
 normal=np.stack([-gx,-gy,np.ones_like(x)],axis=2);normal/=np.linalg.norm(normal,axis=2,keepdims=True);normal*=mask[:,:,None]
 normal=normal.reshape(h,ss,w,ss,3).sum(axis=(1,3));normal/=np.maximum(np.linalg.norm(normal,axis=2,keepdims=True),1e-8);normal[np.linalg.norm(normal,axis=2)<.1]=(0,0,1);normal=normal*.5+.5
 rough=np.where(oxide,.84,.49).reshape(h,ss,w,ss).mean(axis=(1,3));metal=np.where(oxide,.03,.88).reshape(h,ss,w,ss).mean(axis=(1,3))
 orm=np.dstack([np.ones_like(alpha),rough,metal])
 return np.dstack([col,alpha]),normal,orm

def apply(folder,asset='Trampoline',wear=.65):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);size=1024;arrays=[]
 for channel in ('BaseColor','Normal','ORM'):
  p=folder/f'T_{asset}_{channel}.png'
  if p.exists():arr=np.asarray(Image.open(p).convert('RGBA' if channel=='BaseColor' else 'RGB'),dtype=float).copy()/255
  else:arr=np.zeros((size,size,4 if channel=='BaseColor' else 3));arr[:]=(.06,.08,.1,1) if channel=='BaseColor' else ((.5,.5,1) if channel=='Normal' else (1,.75,0))
  if channel=='BaseColor':arr[:,:,3]=1
  arrays.append(arr)
 tiles=[(16,16,256,256,woven(256,256,wear=wear)),(288,16,256,256,woven(256,256,True,wear)),(560,16,256,64,spring(256,64,wear))]
 for x0,y0,w,h,pixels in tiles:
  y0=size-y0-h
  for a,tile in zip(arrays,pixels):
   block=np.flipud(tile);a[y0:y0+h,x0:x0+w]=block
   a[y0-4:y0,x0:x0+w]=block[:1];a[y0+h:y0+h+4,x0:x0+w]=block[-1:]
   a[y0-4:y0+h+4,x0-4:x0]=a[y0-4:y0+h+4,x0:x0+1];a[y0-4:y0+h+4,x0+w:x0+w+4]=a[y0-4:y0+h+4,x0+w-1:x0+w]
 for channel,arr in zip(('BaseColor','Normal','ORM'),arrays):Image.fromarray(np.round(np.clip(arr,0,1)*255).astype('uint8')).save(folder/f'T_{asset}_{channel}.png')
 report=dict(size=1024,wear=wear,net_tile_m=TILE,net_pitch_m=.008,net_thread_m=.00125,mat_pitch_m=.004,mat_thread_m=.0032,net_coverage=float(tiles[0][4][0][:,:,3].mean()),mat_coverage=float(tiles[1][4][0][:,:,3].mean()),spring_m=(SPRING_LENGTH,SPRING_WIDTH),geometry_policy='authored tiled alpha; intentional reuse only in declared rectangles')
 (folder/'tile-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.65);a=p.parse_args();apply(a.out,wear=a.wear)
