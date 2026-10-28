"""Original meter-scaled pin-oak rhytidome, never sampled from photographs.

R/G/B encode physical height / ridge-face pigment / cavity visibility. Elongated
cells change neighbors over 10–40 cm. Distance to their bisectors is measured
in meters, so fissures have a floor and shoulders rather than hairline ink.
The shader fades this mature field on upper wood and slender limbs.
"""
from pathlib import Path
import numpy as np
from PIL import Image
from kit.image_io import write_png


def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1)
    return t*t*(3-2*t)


def generate(out,species):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    w,h=2048,4096
    circ=species.BARK['field_circumference'];height=species.BARK['field_height']
    rng=np.random.default_rng(species.SEED+725)
    def noise(nx,ny):
        a=np.pad(rng.random((ny,nx),dtype=np.float32),((2,2),(2,2)),mode='wrap')
        a=Image.fromarray(a).resize((round(w*(nx+4)/nx),round(h*(ny+4)/ny)),Image.Resampling.BICUBIC)
        x,y=round(2*w/nx),round(2*h/ny)
        return np.asarray(a.crop((x,y,x+w,y+h)))-.5
    nx=round(circ/np.mean(species.BARK['ridge_width_m']))
    nz=round(height/np.mean(species.BARK['plate_length_m']))
    sx,sz=nx/circ,nz/height
    X=(np.arange(w,dtype=np.float32)[None,:]+.5)/w*nx
    Z=(1-(np.arange(h,dtype=np.float32)[:,None]+.5)/h)*nz
    # Broad unequal plates, interrupted by long tapering splits. Edge erosion
    # stays subordinate to the main channels and broad ridge faces.
    X=X+noise(18,27)*.58+.13*np.sin(Z*(np.pi*4/nz)+X*(np.pi*6/nx))
    X=X+noise(110,260)*.14+noise(340,900)*.045
    Z=Z+noise(20,24)*.24+noise(120,400)*.035
    ix=np.floor(X).astype(int);iz=np.floor(Z).astype(int)
    jitter=rng.uniform(.06,.94,(nz,nx,2)).astype(np.float32)
    pigment_seed=rng.random((nz,nx))
    shades=(.70+.50*pigment_seed**2.5+.35*smooth(.65,.95,pigment_seed)).astype(np.float32)
    d1=np.full((h,w),100,np.float32);d2=d1.copy()
    x1=np.zeros_like(d1);z1=x1.copy();x2=x1.copy();z2=x1.copy();face=np.ones_like(d1)
    for dz in (-1,0,1):
        for dx in (-1,0,1):
            cx=ix+dx;cz=iz+dz;j=jitter[cz%nz,cx%nx]
            px=cx+j[:,:,0];pz=cz+j[:,:,1]
            d=((X-px)**2+(Z-pz)**2).astype(np.float32)
            first=d<d1;second=(d<d2)&~first
            d2=np.where(first,d1,np.where(second,d,d2))
            x2=np.where(first,x1,np.where(second,px,x2));z2=np.where(first,z1,np.where(second,pz,z2))
            d1=np.where(first,d,d1);x1=np.where(first,px,x1);z1=np.where(first,pz,z1)
            face=np.where(first,shades[cz%nz,cx%nx],face)
    # Anisotropic metric gradient converts squared-distance difference into
    # actual perpendicular meters. This is the critical distinction from the
    # previous normalized F2-F1 line mask, whose width varied with cell angle.
    gx=(x2-x1)*sx;gz=(z2-z1)*sz
    edge=(d2-d1)/np.maximum(2*np.hypot(gx,gz),1e-6)
    longitudinal=np.abs(gx)/np.maximum(np.hypot(gx,gz),1e-6)
    breadth=.80+.55*(noise(36,64)+.5)
    # 5–12 mm channels with a narrow floor and gently eroded shoulders.
    # Transverse plate ends remain shallower than long axial fissures.
    floor=.0009*breadth;lip=.0045*breadth
    channel_top=smooth(floor,lip,edge)
    top=smooth(floor,.0060*breadth,edge)
    depth=.35+.65*longitudinal
    grain=noise(350,1200)*.55+noise(130,520)*.45
    fleck=smooth(.18,.36,noise(180,640))*top
    # Scaly fibers and shallow exfoliation interrupt the flat faces. This
    # relief is subordinate to the plate: not a second closed crack network.
    fibers=smooth(.08,.25,noise(240,380))*smooth(-.12,.06,noise(65,110))
    exfoliation=noise(420,1500)
    relief=.0038-(1-top)*species.BARK['relief_m']*depth+grain*.0014+fleck*.00030-fibers*top*.0006+exfoliation*top*.0008
    # Warm brown substrate is exposed only inside the channel. Ridge pigment
    # varies per plate and in fine fibers; light/shadow comes from relief/AO.
    cork=np.maximum(.73,face+.110+grain*.15+exfoliation*.25)+fleck*.13
    cork=np.maximum(.73,.80+1.05*(cork-.80))
    pigment=cork*(1-fibers*.10)*(1-(1-channel_top)**1.6*(.08+.37*longitudinal))
    ao=(1-(1-channel_top)*(.16+.30*longitudinal))*(1-fibers*top*.08)
    field=np.stack([np.clip((relief-species.BARK['field_floor_m'])/species.BARK['field_range_m'],0,1),np.clip(pigment/1.4,0,1),ao],axis=2)
    path=out/'BarkField.png';write_png(path,field,bits=16)
    return path
