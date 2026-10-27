"""Original periodic mineral fields and cause-specific decal graphics.

No reference images are opened here. Continuous periodic fields model binder,
aggregate and cement manufacture; all service-age dirt lives in placed decals.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png, srgb_to_linear, linear_to_srgb
from dimensions import ASPHALT_TILE,CONCRETE_TILE,LAWN_TILE
from organic import lawn,edging,iron

RECTS = dict(paint=(0,.75,.5,1),seal=(.5,.75,1,1),patch=(.25,.25,.5,.5),ravel=(0,.5,.5,.75),
    oil=(.5,.5,.75,.75),stain=(.75,.5,1,.75),sediment=(.5,.25,1,.5),scuff=(.125,0,.25,.125),
    iron=(0,0,.125,.25),foundry=(.125,.125,.25,.25),grass=(.25,0,.5,.25),manhole=(0,.25,.25,.5),
    crack=(.5,0,.625,.25),joint=(.625,0,.75,.25),warning=(.75,0,1,.25))


def noise(n, cells, rng):
    """Wrapped bicubic value field, sampled at texel centers."""
    a=rng.random((cells,cells),dtype=np.float32)
    pad=np.pad(a,2,mode='wrap'); s=n//cells
    return np.asarray(Image.fromarray(pad).resize((n+4*s,n+4*s),Image.Resampling.BICUBIC),dtype=np.float32)[2*s:2*s+n,2*s:2*s+n].copy()


def stone(n,cells,seed):
    """Periodic jittered Voronoi mineral faces, streamed to limit RAM."""
    rng=np.random.default_rng(seed); jitter=rng.uniform(.15,.85,(cells,cells,2)); value=rng.random((cells,cells))
    luminance=np.zeros((n,n),np.float32); relief=np.zeros_like(luminance); pitch=n/cells
    for start in range(0,n,64):
        yy,xx=np.mgrid[start:min(n,start+64),:n]; gx=xx/pitch; gy=yy/pitch
        ix=np.floor(gx).astype(int); iy=np.floor(gy).astype(int)
        best=np.full(gx.shape,10.); second=best.copy(); shade=best.copy()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                jx=(ix+dx)%cells; jy=(iy+dy)%cells
                dd=(gx-(ix+dx+jitter[jy,jx,0]))**2+(gy-(iy+dy+jitter[jy,jx,1]))**2
                take=dd<best; second=np.minimum(second,np.where(take,best,dd)); best=np.minimum(best,dd)
                shade=np.where(take,value[jy,jx],shade)
        boundary=np.clip((second-best)*8,0,1)
        luminance[start:start+len(yy)]=shade*.72+boundary*.28
        relief[start:start+len(yy)]=boundary*(.65+.35*shade)
    return luminance,relief


def sources(out,n,wear):
    out.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(240616)
    grain,relief=stone(n,640,2017)
    fines,fine_relief=stone(n,1536,6119)
    fine=noise(n,2048,rng); broad=noise(n,4,rng); mid=noise(n,32,rng)
    # Exposed 8–14 mm mixed stone in oxidized binder, with 3–5 mm fines.
    # Two physical scales survive the 2K bake/filter instead of becoming paint.
    exposed=np.clip((relief-.12)*4,0,1)
    g=.385+exposed*.22*(grain-.5)+.045*(fines-.5)+.07*(broad-.5)+.03*(mid-.5)
    color=np.stack((g*.995,g*1.004,g*1.003),axis=-1)
    rough=np.clip(.91-.17*relief+.045*(fine-.5),.7,.97)
    h=.18+.36*relief+.085*fine_relief+.035*(fine-.5)
    for channel,a in [('BaseColor',color),('ORM',np.stack((.94+.06*relief,rough,np.zeros_like(g)),axis=-1)),('Height',h[:,:,None])]:
        write_png(out/f'T_Asphalt_{channel}.png',a,bits=16 if channel=='Height' else 8)
    del grain,relief,color,rough,h,g
    fine,cement_relief=stone(n,1024,97031);mid=noise(n,32,rng);broad=noise(n,4,rng)
    yy,xx=np.mgrid[:n,:n].astype(np.float32)
    # Unequally loaded bristles leave irregular transverse grooves. A pure
    # sine at this density aliases into a woven pattern after the 2K filter.
    bristles=np.pad(rng.random(512,dtype=np.float32),2,mode='wrap')
    step=n//512
    stroke=np.asarray(Image.fromarray(bristles[None,:]).resize((n+4*step,1),Image.Resampling.BICUBIC))[0,2*step:2*step+n]
    warp=np.rint(1.5*np.sin(np.arange(n)*2*np.pi/n*4)).astype(int)
    broom=stroke[(np.arange(n)[:,None]+warp[None,:])%n]
    pores=np.clip((.16-fine)*5,0,1)
    # Light, neutral cement paste obscures the sand. Tile variation is quiet;
    # edge deposits and separate pours carry service variation in the assembly.
    g=.535+.006*(broad-.5)+.008*(mid-.5)+.045*(fine-.5)-.030*pores
    color=np.stack((g*1.020,g*1.005,g*.960),axis=-1)
    rough=np.clip(.9+.04*(mid-.5)+.025*pores,.83,.96)
    h=.3+.035*(broom-.5)+.025*(cement_relief-.5)-.05*pores
    for channel,a in [('BaseColor',color),('ORM',np.stack((1-.025*pores,rough,np.zeros_like(g)),axis=-1)),('Height',h[:,:,None])]:
        write_png(out/f'T_Concrete_{channel}.png',a,bits=16 if channel=='Height' else 8)
    del color,rough,h,g,fine,cement_relief,mid,broad,pores,broom,yy,xx
    lawn(out,n,LAWN_TILE,noise)


def atlas(out,n,wear):
    out.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(6349)
    rgba=np.zeros((n,n,4),np.float32); normal=np.zeros((n,n,3),np.float32);normal[:]=(.5,.5,1)
    orm=np.zeros_like(normal);orm[:]=(1,.8,0)
    for kind,(u0,v0,u1,v1) in RECTS.items():
        x0,x1=round(u0*n),round(u1*n); y0,y1=round((1-v1)*n),round((1-v0)*n)
        w,h=x1-x0,y1-y0; yy,xx=np.mgrid[:h,:w].astype(np.float32);u=(xx+.5)/w;v=(yy+.5)/h
        field=np.asarray(Image.fromarray(rng.random((32,32),dtype=np.float32)).resize((w,h),Image.Resampling.BICUBIC))
        fine=rng.random((h,w),dtype=np.float32); a=np.zeros((h,w),np.float32)
        col=np.zeros((h,w,3),np.float32);rough=np.full((h,w),.8,np.float32);height=np.zeros((h,w),np.float32)
        metallic=np.zeros((h,w),np.float32)
        if kind=='paint':
            # Four solid paint fragments. Only tire-crossed fragments lose
            # islands of binder, revealing the road through true alpha holes.
            variant=np.minimum((u*4).astype(int),3);s=u*4%1
            tire=np.exp(-((s-.5)/.34)**4)
            failure=(field+.18*(fine-.5)<.33).astype(np.float32)
            amount=np.take(np.array((0.,1.,.75,.25)),variant)
            a=1-failure*tire*amount*wear
            col[:]=(.84,.847,.834);col+=((fine-.5)*.012)[:,:,None]
            rough[:]=.86;height=(fine-.5)*.00010
        elif kind=='seal':
            center=.5+.08*np.sin(u*10)+.04*np.sin(u*43)+.018*np.sin(u*117)
            dist=np.abs(v-center); band=.16+.025*field
            a=np.clip((band-dist)*h/2,0,1)*np.clip(np.minimum(u,1-u)*60,0,1)
            col[:]=(.235,.238,.230);col+=field[:,:,None]*.018;rough[:]=.48;height=a*.0008
        elif kind=='patch':
            border=np.minimum.reduce([u,1-u,v,1-v]);a=np.clip((border-.022-.018*field)*250,0,1)
            gravel=fine*.055+field*.018; col[:]=(.255,.258,.25);col+=gravel[:,:,None]
            rough[:]=.85;height=a*.0006
            edge=np.exp(-((border-.047)/.012)**2);col*=1-.20*edge[:,:,None]
        elif kind=='ravel':
            grit=np.asarray(Image.fromarray(rng.random((512,16),dtype=np.float32)).resize((w,h),Image.Resampling.BICUBIC))
            a=u**2*np.clip((grit-.4)*2,0,.7)*wear
            col[:]=(.25,.253,.244);col+=grit[:,:,None]*.14;rough[:]=.96;height=-a*.0007
        elif kind=='oil':
            for cx,cy,rx,ry in ((.24,.47,.10,.29),(.52,.55,.12,.13),(.77,.38,.04,.07),(.4,.32,.06,.04)):
                a=np.maximum(a,np.clip((1-((u-cx)/rx)**2-((v-cy)/ry)**2+field*.55)*.42,0,.65))
            col[:]=(.13,.115,.09);rough[:]=.48;a*=wear
        elif kind=='stain':
            # Soil leachate / capillary damp near planting-strip concrete edges.
            edge=np.exp(-u*5)
            a=edge*np.clip((field-.25)*.95,0,.48)*(.4+.6*fine)*wear
            a*=np.sin(np.pi*v)**2
            col[:]=(.31,.315,.28);rough[:]=.95
        elif kind=='sediment':
            # u follows flow; image v=0 is the curb-side lip of the card.
            # A narrow damp toe with washouts, then individual deposited grit.
            # Sample grit in meters before stretching into the atlas cell:
            # its 3.048 x .236 m footprint needs round grains, not thin streaks.
            sand=np.asarray(Image.fromarray(rng.random((max(8,round(w*.236/3.048)),w),dtype=np.float32)).resize((w,h),Image.Resampling.BICUBIC))
            center=.14+.025*np.sin(u*19)+.018*np.sin(u*61)
            low=.52+.22*np.sin(u*17+.8)+.16*np.sin(u*43)+.10*np.sin(u*97+1.1)
            band=np.exp(-((v-center)/.19)**2)
            damp=np.exp(-v*8)*np.clip(low+.35*field,0,1)
            grit=np.clip((sand-.55)*5,0,1)*np.clip((field-.24)*2,0,1)
            a=np.clip(damp*1.12+band*grit*.95,0,.97)*wear
            a*=np.clip(np.minimum(u,1-u)*60,0,1)
            col[:]=(.17,.166,.146);col+=((sand-.5)*.14)[:,:,None]
            rough[:]=.96;height=band*grit*.0004
            # A few original needles/leaves settle in the same low strip.
            debris=Image.new('L',(w,h));draw=ImageDraw.Draw(debris)
            for j in range(57):
                x=float(rng.uniform(.03,.97)*w);y=float(rng.uniform(.04,.24)*h)
                dx=float(rng.uniform(.004,.018)*w);dy=float(rng.uniform(-.035,.035)*h)
                draw.line((x,y,x+dx,y+dy),fill=210,width=max(1,round(n/2048)))
            for j in range(10):
                x=float(rng.uniform(.08,.92)*w);y=float(rng.uniform(.05,.21)*h)
                draw.polygon([(x-4,y),(x,y-8),(x+5,y+1),(x+1,y+9)],fill=190)
            debris=np.asarray(debris,dtype=np.float32)/255
            a=np.maximum(a,debris*wear);col=col*(1-debris[:,:,None])+np.array((.16,.12,.075))*debris[:,:,None]
            # Opaque mineral grains interrupt the damp stain. Draw them in
            # physical dimensions so the atlas stretch cannot turn them into
            # streaks: 1.5–4 mm grit along a 3.048 m flow-line fragment.
            grains=Image.new('L',(w,h));gd=ImageDraw.Draw(grains)
            gravel=Image.new('RGB',(w,h));cd=ImageDraw.Draw(gravel)
            for j in range(1700):
                x=float(rng.uniform(.005,.995)*w);y=float(np.clip(rng.normal(.13,.09),.015,.42)*h)
                radius=float(rng.uniform(.00075,.002));rx=max(.65,radius*w/3.048);ry=radius*h/.236
                box=(x-rx,y-ry,x+rx,y+ry)
                gd.ellipse(box,fill=245)
                gray=float(rng.uniform(.13,.33));cd.ellipse(box,fill=(round(gray*255),round(gray*.97*255),round(gray*.83*255)))
            mask=np.asarray(grains,dtype=np.float32)/255
            a=np.maximum(a,mask*wear);col=np.where((mask>0)[:,:,None],np.asarray(gravel,dtype=np.float32)/255,col)
            height+=mask*.0005
        elif kind=='scuff':
            for c in (.23,.29,.38,.55,.61):
                a=np.maximum(a,np.exp(-((v-c-.05*np.sin(u*7))/.025)**2)*np.exp(-((u-.52)/.33)**6))
            a*=.30*wear*(.15+.85*fine);col[:]=(.17,.175,.17);rough[:]=.73
        elif kind in ('iron','manhole','foundry'):
            col,height,rough,metallic=iron(kind,w,h,field,fine);a[:]=1
            if kind=='foundry':a=np.clip((height-.0004)/.0004,0,1)
        elif kind=='grass':
            blades=edging(w,h);col=blades[:,:,:3];a=blades[:,:,3];rough[:]=.91
        elif kind=='crack':
            center=.5+.12*np.sin(v*9)+.03*np.sin(v*59)+.013*np.sin(v*177)
            a=np.clip((.006+.008*field-np.abs(u-center))*w,0,1)*np.clip(np.minimum(v,1-v)*40,0,1)
            col[:]=(.16,.155,.135);rough[:]=.94;height=-a*.002
        elif kind=='joint':
            col[:]=(.205,.20,.18);rough[:]=.94;a[:]=1
        elif kind=='warning':
            # 30 x 12 truncated domes across a 1.524 x .6096 m plate.
            dx=(u*30%1-.5)*.0508;dy=(v*12%1-.5)*.0508;r=np.sqrt(dx*dx+dy*dy)
            height=np.clip((.01397-r)/(.01397-.008382),0,1)*.00508
            # FED-STD-595C 33538, Appendix IV XYZ(C), adapted to sRGB D65.
            col[:]=(.9851,.6758,0);col*=((.97+.03*field)[:,:,None]);rough[:]=.86;a[:]=1
            top=np.clip(height/.00508,0,1)
            foot=np.exp(-((u-.5)/.26)**4)
            col*=1+.025*top[:,:,None]-.16*(foot*(.3+.7*field))[:,:,None]
            col-=.08*(foot*top*field)[:,:,None]
            rough-=.12*foot*top
        if kind=='ravel':
            px=.18/w;py=6.096/h
        elif kind=='paint':
            px=.4572/(w/4);py=1.8288/h
        elif kind=='sediment':
            px=3.048/w;py=.236/h
        elif kind=='warning':
            px=1.524/w;py=.6096/h
        elif kind=='manhole':px=.6096/w;py=.6096/h
        elif kind in ('iron','foundry'):px=.3/w;py=.3/h
        else:px=3.048/w;py=1.524/h
        gy,gx=np.gradient(height,py,px);norm=np.stack((-gx,gy,np.ones_like(gx)),axis=-1);norm/=np.linalg.norm(norm,axis=-1,keepdims=True)
        rgba[y0:y1,x0:x1,:3]=col;rgba[y0:y1,x0:x1,3]=a
        normal[y0:y1,x0:x1]=norm*.5+.5;orm[y0:y1,x0:x1,1]=rough;orm[y0:y1,x0:x1,2]=metallic
    write_png(out/'T_GroundTrim_BaseColor.png',rgba)
    write_png(out/'T_GroundTrim_Normal.png',normal,16)
    write_png(out/'T_GroundTrim_ORM.png',orm)


def ship_atlas(source,out,size):
    from kit.image_io import read_png
    out.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','Normal','ORM'):
        a=read_png(source/f'T_GroundTrim_{channel}.png');n=a.shape[0];factor=n//size;c=a.shape[2]
        if channel=='BaseColor': a[:,:,:3]=srgb_to_linear(a[:,:,:3])
        elif channel=='Normal':a=a*2-1
        elif channel=='ORM':a[:,:,1]**=2
        a=a.reshape(size,factor,size,factor,c).mean(axis=(1,3))
        if channel=='BaseColor':a[:,:,:3]=linear_to_srgb(a[:,:,:3])
        elif channel=='Normal':a=a/np.maximum(np.linalg.norm(a,axis=-1,keepdims=True),1e-8)*.5+.5
        elif channel=='ORM':a[:,:,1]=np.sqrt(a[:,:,1])
        write_png(out/f'T_GroundTrim_{channel}.png',a)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['source','atlas','ship']);p.add_argument('--out',type=Path,required=True);p.add_argument('--source',type=Path);p.add_argument('--size',type=int,default=4096);p.add_argument('--wear',type=float,default=1.)
    a=p.parse_args()
    if a.mode=='source':sources(a.out,a.size,a.wear)
    elif a.mode=='atlas':atlas(a.out,a.size,a.wear)
    else:ship_atlas(a.source,a.out,a.size)
