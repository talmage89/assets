"""Seeded meter-scale ridges and lifted plates; original analytic bitmap field.

R/G/B store normalized physical height / face variation / cavity visibility.
These are intermediate procedural fields, baked into the shared delivery atlas.
"""
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
from kit.image_io import write_png
from settings import BARK,SEED


def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)


def generate(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    w,h=2048,4096;circ=BARK['field_circumference'];height=BARK['field_height']
    rng=np.random.default_rng(SEED+725)
    # Unequal ridge widths are normalized around one closed bole circumference.
    widths=rng.uniform(*BARK['ridge_width_m'],round(circ/np.mean(BARK['ridge_width_m'])));widths*=circ/widths.sum();bounds=np.r_[0,np.cumsum(widths)]
    x=(np.arange(w,dtype=np.float32)[None,:]+.5)/w*circ
    z=height*(1-(np.arange(h,dtype=np.float32)[:,None]+.5)/h)
    angle=x/circ*np.pi*2
    # Periodic around the trunk, with coarse waviness and small torn edges.
    warped=(x+.007*np.sin(z*3.7+np.sin(angle*3))+.003*np.sin(z*12.3+angle*5)
              +.00065*np.sin(z*143+angle*17)+.00035*np.sin(z*311-angle*37))%circ
    height_map=np.zeros((h,w),np.float32);face_map=np.zeros_like(height_map);ao=np.ones_like(height_map)
    def noise(nx,ny):
        a=rng.random((ny,nx),dtype=np.float32)
        return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC))-.5
    grain=noise(200,900)*.7+noise(65,320)*.6
    mottling=noise(70,220)
    boundary=[np.zeros_like(z)]
    for b in bounds[1:-1]:
        boundary.append(b+.004*np.sin(z*rng.uniform(4,9)+rng.uniform(0,6.28))
                        +.0015*np.sin(z*rng.uniform(15,29)+rng.uniform(0,6.28)))
    boundary.append(np.full_like(z,circ))
    for i in range(len(widths)):
        width=boundary[i+1]-boundary[i]
        side=(warped-boundary[i])/width
        mask=(side>=0)&(side<1)
        edge=np.minimum(side,1-side)*width
        face=smooth(.0005,.0032,edge)
        levels=[-.30]
        while levels[-1]<height+.3:levels.append(levels[-1]+rng.uniform(*BARK['plate_length_m']))
        levels=np.array(levels);idx=np.searchsorted(levels,z,side='right')-1
        cycle=(z-levels[idx])/(levels[idx+1]-levels[idx])
        # A ragged, oblique plate lip. It stops short on some faces, exposing
        # narrow cracks rather than a continuous course around the bole.
        tilt=rng.uniform(-.018,.018,len(levels))[idx]
        lipdist=(z-levels[idx])+tilt*(side-.5)+.003*np.sin(side*5+i)+.0012*np.sin(side*34+i)
        lip=(1-smooth(.001,.005,np.abs(lipdist)))*smooth(.12,.28,side)
        lip*=1-.6*smooth(.65,.90,side)
        variation=rng.uniform(.65,1.30,len(levels))[idx]
        relief=(face*(.0011+.0018*cycle**3)+grain*.0015*face+mottling*.0005-lip*.0013)*(BARK['relief_m']/.003)
        fissure=1-smooth(.0008,.0028,edge)
        color=variation*(.88+.12*cycle)+grain*.24+mottling*.18
        color=color*(1-fissure*.82)*(1-lip*.55)
        height_map[mask]=relief[mask];face_map[mask]=np.broadcast_to(color,(h,w))[mask]
        visibility=(1-fissure*.65)*(1-lip*.35)
        ao[mask]=visibility[mask]
    pixels=np.stack([np.clip((height_map+.001)/.005,0,1),np.clip(face_map/1.4,0,1),ao],axis=2)
    path=out/'BarkField.png';write_png(path,pixels,bits=16)
    return path
