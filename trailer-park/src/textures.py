"""Original manufacture fields, GPU baked at 4096, filtered to one 2048 set.

No photographic inputs. Meter-based flutes, folded seams, zinc grain and
concrete pores; large service history belongs to each placed mesh's colors.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png,linear_to_srgb,srgb_to_linear

NAME='Manufactured'
COVERAGE=4.8768
RECTS=dict(Ribbed=(0,.5,.5,1),Skirt=(.5,.5,1,.75),Roof=(.5,.75,1,1),
           Zinc=(0,0,.25,.5),Steel=(.25,0,.5,.5),Pier=(.5,0,.75,.5),Plain=(.875,.25,1,.5),
           Rust=(.75,0,.875,.25),Damp=(.875,0,1,.125),Splash=(.875,.125,1,.25),Fatigue=(.75,.25,.875,.5))


def field(w,h,cells,seed):
    rng=np.random.default_rng(seed);a=rng.random((cells,cells),dtype=np.float32)
    return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC),np.float32)


def source(out,n=4096):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    bc=np.ones((n,n,3),np.float32);orm=bc.copy();height=np.full((n,n),.5,np.float32);alpha=np.ones((n,n),np.float32)
    for index,(kind,(u0,v0,u1,v1)) in enumerate(RECTS.items()):
        x0,x1=round(u0*n),round(u1*n);y0,y1=round((1-v1)*n),round((1-v0)*n)
        w,h=x1-x0,y1-y0;yy,xx=np.mgrid[:h,:w].astype(np.float32)
        x=(xx+.5)/n*COVERAGE;y=(h-yy-.5)/n*COVERAGE
        fine=np.random.default_rng(930+index).random((h,w),dtype=np.float32)
        broad=field(w,h,22,100+index);mid=field(w,h,128,200+index)
        c=np.ones((h,w,3),np.float32)*.92;r=np.full((h,w),.76,np.float32);m=np.zeros((h,w),np.float32);ao=np.ones((h,w),np.float32)
        relief=.5+.001*(fine-.5)
        if kind=='Ribbed':
            phase=x%.2032
            rib=np.exp(-((phase-.013)/.011)**8)
            fine_rib=.18*np.exp(-((phase-.102)/.006)**6)
            relief=.50+.30*rib+.06*fine_rib+.0015*(mid-.5)
            c*=1-.15*rib[:,:,None]-.04*fine_rib[:,:,None];ao-=.08*rib;r=.75+.05*(fine-.5)
            # Rivets only on folded sheet laps, with tiny gravity rust tails.
            dz=y%.6096;head=np.exp(-((phase-.013)/.006)**6-((dz-.035)/.006)**6)
            tail=np.exp(-((phase-.013)/.009)**2)*np.exp(-((dz-.035)%.6096)/.04)*.16
            c=c*(1-tail[:,:,None])+np.array((.28,.105,.032))*tail[:,:,None];relief+=.04*head
        elif kind=='Skirt':
            phase=x%.1016;rib=np.exp(-((phase-.018)/.010)**6)
            relief=.5+.24*rib+.001*(fine-.5);c*=1-.12*rib[:,:,None];ao-=.12*rib;r[:]=.81
            # Openly declared manufacture relief; splash is not repeated here.
        elif kind=='Roof':
            seam=np.exp(-((x%.6096-.018)/.010)**6)
            raised=np.exp(-((y%.3048-.008)/.006)**6)*.22
            relief=.5+.36*seam+.06*raised+.0007*(fine-.5)
            c*=.83+.05*(mid-.5)[:,:,None];c*=1-.13*seam[:,:,None];ao-=.12*seam;r=.56+.08*mid;m[:]=.36
        elif kind=='Zinc':
            # Galvanizing is microns of crystal variation, not hammered metal.
            c*=.75+.16*mid[:,:,None];r=.37+.16*mid;m[:]=.88;relief=.5+.0007*(fine-.5)
        elif kind=='Steel':
            c*=.73+.14*mid[:,:,None];r=.64+.12*mid;m[:]=.62;relief=.5+.002*(mid-.5)
        elif kind=='Pier':
            pores=np.clip((fine-.91)*9,0,.7)*np.clip((mid-.3)*3,0,1)
            c*=.81+.16*(mid-.5)[:,:,None]-.18*pores[:,:,None];r=.88+.08*mid
            relief=.5+.022*(mid-.5)-.06*pores;ao-=.13*pores
        elif kind in ('Rust','Damp','Splash','Fatigue'):
            from weather_fields import field as weather
            c,packed,relief,opacity=weather(kind,w,h,8401+index)
            ao,r,m=packed[:,:,0],packed[:,:,1],packed[:,:,2];alpha[y0:y1,x0:x1]=opacity
        else:
            c*=.97+.025*(mid-.5)[:,:,None];r=.68+.04*mid
        bc[y0:y1,x0:x1]=np.clip(c,0,1);height[y0:y1,x0:x1]=np.clip(relief,0,1)
        orm[y0:y1,x0:x1]=np.stack([ao,r,m],axis=-1)
    write_png(out/f'T_{NAME}_BaseColor.png',linear_to_srgb(bc))
    write_png(out/f'T_{NAME}_Coverage.png',alpha[:,:,None])
    write_png(out/f'T_{NAME}_ORM.png',orm)
    write_png(out/f'T_{NAME}_Height.png',height[:,:,None],bits=16)
    (out/'layout.json').write_text(json.dumps(dict(coverage_m=COVERAGE,rects=RECTS,height_distance_m=.012,source_size=n),indent=2))


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('textures/source'));a.add_argument('--size',type=int,default=4096);a=a.parse_args();source(a.out,a.size)
