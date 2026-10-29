"""Z-buffered whole-part masks from actual imported triangle surfaces.

Camera projection matches the kit renderer. These are review masks only:
reference photographs never enter this module or the asset's material path.
"""
import math
import numpy as np
from kit.photo_match import project

def projection(points,shot,width,height):
 camera=np.asarray(shot['location']);d=np.asarray(shot['target'])-camera;d=d/np.linalg.norm(d)
 az=math.atan2(d[1],d[0]);el=math.atan2(d[2],np.linalg.norm(d[:2]));roll=shot.get('roll',0)
 params=np.array([az,el,*camera,math.log(shot.get('lens',70)),roll])
 if 'ortho' not in shot:return project(params,points,width,height)[:2]
 right=np.cross(d,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,d)
 right,up=right*math.cos(roll)+up*math.sin(roll),up*math.cos(roll)-right*math.sin(roll)
 q=points-camera;scale=width/shot['ortho']
 return np.stack([width/2+(q@right)*scale,height/2-(q@up)*scale],axis=1),q@d

def raster(geometry,shot,width,height):
 xyz=geometry['xyz'];tuv=geometry['uv'];ids=geometry['ids'];names=geometry['names']
 xy,depth=projection(xyz.reshape(-1,3),shot,width,height);xy=xy.reshape(-1,3,2);depth=depth.reshape(-1,3)
 zbuffer=np.full((height,width),np.inf);index=np.zeros((height,width),np.int32);coords=np.zeros((height,width,2),np.float32)
 keep=set(shot.get('diagnostic_isolate',[]))
 for points,dist,ident,uv in zip(xy,depth,ids,tuv):
  if keep and str(names[ident-1]) not in keep:continue
  if min(dist)<=.001:continue
  lo=np.maximum(np.floor(points.min(axis=0)).astype(int),[0,0]);hi=np.minimum(np.ceil(points.max(axis=0)).astype(int),[width-1,height-1])
  if np.any(hi<lo):continue
  a,b,c=points;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-8:continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
  w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
  w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1
  inside=(w0>=0)&(w1>=0)&(w2>=0)
  if 'ortho' not in shot:
   reciprocal=w0/dist[0]+w1/dist[1]+w2/dist[2];z=1/np.maximum(reciprocal,1e-12)
   w0=w0/dist[0]*z;w1=w1/dist[1]*z;w2=w2/dist[2]*z
  else:z=w0*dist[0]+w1*dist[1]+w2*dist[2]
  sl=np.s_[lo[1]:hi[1]+1,lo[0]:hi[0]+1];active=inside&(z<zbuffer[sl])
  zbuffer[sl][active]=z[active];index[sl][active]=ident
  interpolated=w0[:,:,None]*uv[0]+w1[:,:,None]*uv[1]+w2[:,:,None]*uv[2]
  coords[sl][active]=interpolated[active]
 return index,coords

def bilinear(a,points):
 x=np.clip(points[:,0],0,a.shape[1]-1.000001);y=np.clip(points[:,1],0,a.shape[0]-1.000001)
 i=x.astype(int);j=y.astype(int);u=x-i;v=y-j
 if a.ndim==3:u=u[:,None];v=v[:,None]
 return (1-v)*((1-u)*a[j,i]+u*a[j,i+1])+v*((1-u)*a[j+1,i]+u*a[j+1,i+1])
