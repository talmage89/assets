"""Original flat interlacing rhytidome, in physical bole coordinates.

An anisotropic cellular field changes neighbors every 10–40 cm. Its continuous
boundaries split/rejoin between 2–5 cm broad ridge faces. A narrow rounded
shoulder carries millimeter relief, rather than dark disconnected markings.
No reference pixels are read here.
"""
from pathlib import Path
import numpy as np
from PIL import Image
from kit.image_io import write_png


def generate(out,species):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    w,h=2048,4096;circ=species.BARK['field_circumference'];height=species.BARK['field_height']
    rng=np.random.default_rng(species.SEED+725)
    def noise(nx,ny):
        # Padding before bicubic filtering keeps the repeated bole field
        # continuous at its angular seam, including its fine erosion.
        a=np.pad(rng.random((ny,nx),dtype=np.float32),((2,2),(2,2)),mode='wrap')
        a=Image.fromarray(a).resize((round(w*(nx+4)/nx),round(h*(ny+4)/ny)),Image.Resampling.BICUBIC)
        x,y=round(2*w/nx),round(2*h/ny)
        return np.asarray(a.crop((x,y,x+w,y+h)))-.5
    nx,nz=round(circ/.032),round(height/.25)
    X=(np.arange(w,dtype=np.float32)[None,:]+.5)/w*nx
    Z=(1-(np.arange(h,dtype=np.float32)[:,None]+.5)/h)*nz
    X=X+noise(24,32)*.42+.16*np.sin(Z*(np.pi*4/nz)+X*(np.pi*6/nx))
    # Physical edge erosion at several scales removes the straight Voronoi
    # segments; small fibers are an order below the broad flat ridge width.
    X=X+noise(130,300)*.20+noise(380,1000)*.065
    Z=Z+noise(22,26)*.20+noise(140,500)*.085
    ix=np.floor(X).astype(int);iz=np.floor(Z).astype(int)
    jitter=rng.uniform(.12,.88,(nz,nx,2)).astype(np.float32)
    shades=rng.uniform(.91,1.02,(nz,nx)).astype(np.float32)
    d1=np.full((h,w),100,np.float32);d2=d1.copy();face=np.ones_like(d1)
    for dz in (-1,0,1):
        for dx in (-1,0,1):
            cx=ix+dx;cz=iz+dz
            j=jitter[cz%nz,cx%nx]
            d=(X-cx-j[:,:,0])**2+(Z-cz-j[:,:,1])**2
            take=d<d1;d2=np.where(take,d1,np.minimum(d2,d));d1=np.minimum(d1,d)
            face=np.where(take,shades[cz%nz,cx%nx],face)
    # Narrow continuous fissures; the old high-frequency interruption produced
    # tick marks. Broad shoulders flatten into a gently scaly ridge top.
    boundary=np.sqrt(d2)-np.sqrt(d1)
    dz,dx=np.gradient(boundary);dx*=w/nx;dz*=h/nz
    longitudinal=np.abs(dx)/np.maximum(np.hypot(dx,dz),1e-6)
    crack=np.exp(-(boundary/.045)**2)
    shoulder=1-np.exp(-(boundary/.13)**1.5)
    grain=noise(380,1400)*.35+noise(140,550)*.65
    flake=np.clip((noise(170,600)-.16)*4,0,1)*shoulder
    relief=-.0006+.0034*shoulder+grain*.0025+flake*.0007
    variation=(face+grain*.75)*(1-crack*.72*(.30+.70*longitudinal))+flake*.065
    ao=1-crack*(.20+.44*longitudinal)
    field=np.stack([np.clip((relief+.001)/.005,0,1),np.clip(variation/1.4,0,1),ao],axis=2)
    path=out/'BarkField.png';write_png(path,field,bits=16);return path
