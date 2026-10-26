"""Original analytic woven-wire tile and rounded residential selvage.

No reference pixels are read. Wire diameter and clear mesh size are physical
parameters, and PBR channels derive from round wire cross-section/over-under
height. The one tile is reused by small clipped card cells, never uniquely
baked over an entire 10 ft mesh section.
"""
import argparse,json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image
from dimensions import *

def field(x,z):
    a=(x+z)/math.sqrt(2);b=(x-z)/math.sqrt(2)
    # Slight interweave offset is periodic across both tile boundaries.
    a=a+.00065*np.sin(2*math.pi*b/NORMAL_PITCH)
    b=b+.00065*np.sin(2*math.pi*a/NORMAL_PITCH)
    da=(a+NORMAL_PITCH/2)%NORMAL_PITCH-NORMAL_PITCH/2
    db=(b+NORMAL_PITCH/2)%NORMAL_PITCH-NORMAL_PITCH/2
    ha=np.sqrt(np.maximum(0,(WIRE/2)**2-da**2))+.00045*np.cos(2*math.pi*b/NORMAL_PITCH)
    hb=np.sqrt(np.maximum(0,(WIRE/2)**2-db**2))-.00045*np.cos(2*math.pi*a/NORMAL_PITCH)
    ha=np.where(abs(da)<WIRE/2,ha,-.01);hb=np.where(abs(db)<WIRE/2,hb,-.01)
    mask=np.minimum(abs(da),abs(db))<WIRE/2
    return mask,np.maximum(0,np.maximum(ha,hb))

def edge(x,z):
    d=(x+TILE/8)%(TILE/4)-TILE/8
    curve=.003+np.sqrt(d*d+.003**2)-.003
    # Bottom knuckle is rounded, with two returned legs meeting the field.
    distance=(z-curve)/np.sqrt(1+(d/np.sqrt(d*d+.003**2))**2)
    mask=abs(distance)<WIRE/2
    return mask,np.sqrt(np.maximum(0,(WIRE/2)**2-distance**2))

def tile(w,h,physical_h,fn):
    ss=4;xx=(np.arange(w*ss)+.5)/(w*ss)*TILE
    zz=(np.arange(h*ss)+.5)/(h*ss)*physical_h
    x,z=np.meshgrid(xx,zz);mask,height=fn(x,z)
    # Numeric derivatives of a cylindrical height field supply tangent normals.
    gz,gx=np.gradient(height,physical_h/(h*ss),TILE/(w*ss))
    # Plane's tangent basis is +X / +Z / -Y, OpenGL +Y in the image's V axis.
    vectors=np.stack([-gx,-gz,np.ones_like(gx)],axis=2);vectors/=np.linalg.norm(vectors,axis=2,keepdims=True)
    vectors*=mask[:,:,None]
    normal=vectors.reshape(h,ss,w,ss,3).sum(axis=(1,3));length=np.linalg.norm(normal,axis=2,keepdims=True);normal/=np.maximum(length,1e-8);normal[length[:,:,0]<1e-8]=(0,0,1)
    alpha=mask.reshape(h,ss,w,ss).mean(axis=(1,3))
    # Zinc values vary subtly at the original procedural scale, not painted shadows.
    speck=.5+.5*np.sin(x*1137+np.sin(z*845)*2.1)*np.sin(z*1337+x*91)
    col=np.stack([.37+speck*.08,.40+speck*.08,.41+speck*.08],axis=2)
    col=col.reshape(h,ss,w,ss,3).mean(axis=(1,3))
    # Convert linear zinc reflectance to sRGB; alpha is linear coverage.
    col=np.where(col<=.0031308,12.92*col,1.055*col**(1/2.4)-.055)
    orm=np.stack([np.ones_like(alpha),np.full_like(alpha,.57),np.full_like(alpha,.88)],axis=2)
    return (np.dstack([col,alpha]),normal*.5+.5,orm)

def apply(folder,asset='ChainLink'):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);size=1024
    arrays=[]
    for channel in ('BaseColor','Normal','ORM'):
        p=folder/f'T_{asset}_{channel}.png'
        if p.exists():im=Image.open(p).convert('RGBA' if channel=='BaseColor' else 'RGB');arr=np.asarray(im,dtype=float).copy()/255
        else:arr=np.full((size,size,4 if channel=='BaseColor' else 3),0.0)
        if channel=='BaseColor':
            if arr.shape[2]==3:arr=np.dstack([arr,np.ones((size,size))])
            arr[:,:,3]=1
        elif channel=='Normal' and not p.exists():arr[:]=(.5,.5,1)
        elif channel=='ORM' and not p.exists():arr[:]=(1,.6,.88)
        arrays.append(arr)
    field_tiles=tile(256,256,TILE,field);edge_tiles=tile(256,32,EDGE,edge)
    for target,ft,et in zip(arrays,field_tiles,edge_tiles):
        # Arrays use top-down PNG rows, UVs bottom-up. Duplicate edge padding.
        target[size-272:size-16,16:272]=np.flipud(ft)
        target[size-320:size-288,16:272]=np.flipud(et)
        for x0,y0,w,h,pixels in [(16,16,256,256,ft),(16,288,256,32,et)]:
            y0=size-y0-h;block=np.flipud(pixels)
            target[y0-4:y0,x0:x0+w]=block[:1];target[y0+h:y0+h+4,x0:x0+w]=block[-1:]
            target[y0-4:y0+h+4,x0-4:x0]=target[y0-4:y0+h+4,x0:x0+1]
            target[y0-4:y0+h+4,x0+w:x0+w+4]=target[y0-4:y0+h+4,x0+w-1:x0+w]
    for channel,arr in zip(('BaseColor','Normal','ORM'),arrays):Image.fromarray(np.round(np.clip(arr,0,1)*255).astype('uint8')).save(folder/f'T_{asset}_{channel}.png')
    report=dict(generator='analytic original woven wire',size=size,field_pixels=256**2,selvage_pixels=256*32,field_region=FIELD_RECT,edge_region=EDGE_RECT,physical_tile_m=TILE,wire_diameter_m=WIRE,clear_mesh_m=CLEAR_MESH,coverage_fraction=float(field_tiles[0][:,:,3].mean()),density_px_m=256/TILE)
    (folder/'tile-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();apply(a.out)
