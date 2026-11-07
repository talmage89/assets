"""Original cause-specific trim and phenolic fields; no reference pixels.

4096 source fields are baked with kit.flat_bake, then filtered with the kit.
Opaque trim, masked marks and rules use the same image triple.
"""
import sys,argparse,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png
from kit.fonts import find_font
RECTS=dict(Steel=(0,.75,.5,1),Coping=(.5,.75,1,1),Tile=(0,.5,.25,.75),Grout=(.25,.5,.5,.75),
           Paint=(.5,.5,.75,.75),Zinc=(.75,.5,1,.625),ToePlate=(.75,.625,1,.75),Burnish=(0,.25,.25,.5),Scrape=(.25,.25,.5,.5),
           Tag=(.5,.25,.75,.5),Dirt=(.75,.25,.875,.5),Crack=(.875,.25,1,.5),Rules=(0,0,1,.25))

def field(w,h,cells,seed):
    a=np.random.default_rng(seed).random((cells,cells),dtype=np.float32)
    return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC),dtype=np.float32)

def source(out,n):
    out.mkdir(parents=True,exist_ok=True)
    base=Image.new('RGBA',(n,n));orm=Image.new('RGB',(n,n));height=Image.new('I;16',(n,n),32768)
    for index,(name,rect) in enumerate(RECTS.items()):
        x0,y0,x1,y1=round(rect[0]*n),round((1-rect[3])*n),round(rect[2]*n),round((1-rect[1])*n)
        w,h=x1-x0,y1-y0;v,u=np.mgrid[:h,:w].astype(np.float32);u=(u+.5)/w;v=(v+.5)/h
        broad=field(w,h,12,120+index);mid=field(w,h,64,720+index);fine=np.random.default_rng(900+index).random((h,w),dtype=np.float32)
        color=np.full((h,w,3),.4,np.float32);a=np.ones((h,w),np.float32);rough=np.full((h,w),.8,np.float32);metal=np.zeros((h,w),np.float32);relief=.5+fine*.025
        if name=='Steel':
            # v across the pipe: bare polished contact crown, oxide on sides.
            # Three age lanes share the original rectangle and memory budget.
            severity=np.take(np.array((.35,.70,1.),np.float32),np.minimum((u*3).astype(int),2))
            crown=np.exp(-((v-.5)/(.12+.07*severity))**4)*(.70+.30*severity)
            rust=(1-crown)*np.clip((broad-.37)*2.2,0,.8)*severity
            color[:]=(.12,.15,.145);color=color*(1-rust[:,:,None])+np.array((.28,.13,.055))*rust[:,:,None]
            color=color*(1-crown[:,:,None])+np.array((.61,.64,.63))*crown[:,:,None]
            scratch=np.clip((np.sin(u*1400+mid*8)-.80)*6,0,1)*crown
            color-=scratch[:,:,None]*.10;metal=np.clip(.08+.87*crown-rust*.06,0,1);rough=.55-.32*crown+.3*rust;relief=.5-.04*scratch+.025*mid
        elif name=='Coping':
            worn=np.exp(-((v-.93)/.11)**4)*(.65+.35*broad)
            stains=np.exp(-v*6)*np.clip((broad-.3)*1.4,0,.6)
            edge=np.minimum.reduce([u,1-u,v,1-v])
            chips=np.clip((mid-.65)*7,0,1)*np.exp(-edge*32)
            color[:]=(.64,.625,.56);color*=1-.20*stains[:,:,None]-.24*chips[:,:,None]
            color=color*(1-.85*worn[:,:,None])+np.array((.30,.29,.27))*.85*worn[:,:,None]
            rough=.81-.22*worn+.08*chips;relief=.5-.45*chips+.012*mid
        elif name=='Tile':
            gx=u*8%1;gy=v*8%1;grout=(np.minimum.reduce([gx,1-gx,gy,1-gy])<.032).astype(float)
            cell=(np.floor(u*8)*17+np.floor(v*8)*13)%19
            missing=((cell==8)&(mid>.3)).astype(float)
            salts=np.clip((v-.5)*1.2,0,.35)*broad
            color[:]=(.11,.29,.35);color*=.9+.2*mid[:,:,None]
            color=color*(1-grout[:,:,None])+np.array((.38,.37,.31))*grout[:,:,None]
            color=color*(1-missing[:,:,None])+np.array((.34,.31,.25))*missing[:,:,None]
            color+=salts[:,:,None]*.35;rough=.31+.4*grout+.5*missing;relief=.5-.12*grout-.26*missing
        elif name=='Grout':color[:]=(.43,.42,.37);color*=.85+.18*broad[:,:,None];rough[:]=.91
        elif name=='Paint':
            exposed=np.clip((mid-.60)*4,0,1)*np.exp(-v*4)
            color[:]=(.09,.18,.155);color=color*(1-exposed[:,:,None])+np.array((.37,.28,.17))*exposed[:,:,None];rough=.72+.12*exposed;metal=.15+.45*exposed
        elif name in ('Zinc','ToePlate'):
            color[:]=(.52,.55,.55);color*=.8+.32*mid[:,:,None];metal[:]=.86;rough=.52+.14*(broad-.5)
            if name=='ToePlate':
                scuff=np.clip((np.sin(u*330+mid*4)-.83)*5,0,1)*np.exp(-((v-.4)/.36)**4)
                color+=scuff[:,:,None]*.16;rough-=scuff*.22;relief=.5-.025*scuff+.012*(fine-.5)
        elif name=='Burnish':
            edge=np.sin(np.pi*u)**1.1*np.sin(np.pi*v)**.5
            coverage=edge*np.clip(.18+.70*broad,0,.9)
            a=(fine<coverage).astype(np.float32)
            color[:]=(.50,.492,.47);rough[:]=.50;relief[:]=.5
        elif name=='Scrape':
            line=np.clip((np.sin(u*420+mid*13)-.7)*5,0,1)
            a=line*np.sin(np.pi*v)**2*np.sin(np.pi*u)**.25*.65
            color[:]=(.16,.155,.14);rough[:]=.73;relief=.5-line*.015
        elif name=='Tag':
            a[:]=0;color[:]=(.19,.25,.24);rough[:]=.83
        elif name=='Dirt':
            coverage=(.18+.65*broad)*np.sin(np.pi*u)**2*np.sin(np.pi*v)**2
            a=(fine<coverage).astype(np.float32)
            color[:]=(.42,.39,.32);color*=.9+.16*mid[:,:,None];rough[:]=.98;relief=.5+fine*.035
        elif name=='Crack':
            center=.50+.13*np.sin(v*15)+.07*np.sin(v*48)+.025*np.sin(v*110)
            line=np.exp(-((u-center)/.018)**4);a=line*np.sin(np.pi*v)**.3
            color[:]=(.23,.21,.17);rough[:]=.96;relief=.5-.3*line
        elif name=='Rules':a[:]=1;color[:]=(.17,.26,.23);rough[:]=.8
        color=np.clip(color+(fine[:,:,None]-.5)*.012,0,1)
        rgba=np.dstack((color,np.clip(a,0,1)))
        base.paste(Image.fromarray(np.rint(rgba*255).astype('uint8')),(x0,y0))
        orm.paste(Image.fromarray(np.rint(np.stack((np.ones_like(rough),np.clip(rough,0,1),metal),axis=-1)*255).astype('uint8')),(x0,y0))
        height.paste(Image.fromarray(np.rint(np.clip(relief,0,1)*65535).astype('uint16')),(x0,y0))
    draw=ImageDraw.Draw(base)
    for i,town in enumerate(('ALDER GLEN','CEDAR JUNCTION','MILL CREEK')):
        x=int(i*n/3);yy=int(n*.75);ww=int(n/3)
        for text,pos,size,bold in [(town,.12,.032,1),('PARKS & RECREATION',.28,.020,0),('SKATE PARK',.46,.033,1),('DAWN TO DUSK / HELMETS REQUIRED',.67,.013,0),('SHARE THE LINES / NO GLASS',.79,.015,0),('EST. '+str((2011,2004,1999)[i]),.91,.018,0)]:
            font=ImageFont.truetype(find_font('DejaVu Sans','Bold' if bold else 'Book'),int(n*size))
            draw.text((x+ww/2,yy+int(n*.25*pos)),text,font=font,fill=(216,215,202,255),anchor='mm')
    # Fictional tags, authored strokes, occasional drips under their own ends.
    rect=RECTS['Tag'];x0=int(rect[0]*n);y0=int((1-rect[3])*n);ww=int(.25*n)
    font=ImageFont.truetype(find_font('DejaVu Sans','Oblique'),int(ww*.24))
    draw.text((x0+ww*.08,y0+ww*.36),'FERN',font=font,fill=(43,70,67,205),stroke_width=max(1,n//1500))
    draw.line([(x0+ww*.1,y0+ww*.67),(x0+ww*.74,y0+ww*.58)],fill=(43,70,67,210),width=max(2,n//850))
    for u in (.22,.63):draw.line([(x0+ww*u,y0+ww*.64),(x0+ww*u,y0+ww*.80)],fill=(43,70,67,120),width=max(1,n//1800))
    base.save(out/'T_SkateTrim_BaseColor.png');orm.save(out/'T_SkateTrim_ORM.png');height.save(out/'T_SkateTrim_Height.png')
    # Phenolic wear follows riding lanes; panel edges and screw seats retain grime.
    v,u=np.mgrid[:n,:n].astype(np.float32);u/=n;v/=n
    broad=field(n,n,24,219);fine=field(n,n,512,1219)
    lane=np.maximum(np.exp(-((u-.28-.04*np.sin(v*8))/.105)**4),np.exp(-((u-.70-.03*np.sin(v*9))/.09)**4))
    edge=np.exp(-np.minimum(u,1-u)*38)
    g=.29+.11*lane+.035*(broad-.5)-.055*edge
    color=np.stack((g*1.12,g*.91,g*.71),axis=-1)
    rough=np.clip(.84-.18*lane+.05*(fine-.5),.5,.95)
    for ch,arr in [('BaseColor',color),('ORM',np.stack((np.ones_like(g),rough,np.zeros_like(g)),axis=-1)),('Height',(.5+.018*(fine-.5)-.025*edge)[:,:,None])]:
        write_png(out/f'T_Prefab_{ch}.png',arr,bits=16 if ch=='Height' else 8)
    (out/'layout.json').write_text(json.dumps(RECTS,indent=2))
    (out/'.stamp').touch()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('build/procedural'));ap.add_argument('--size',type=int,default=4096);a=ap.parse_args();source(a.out,a.size)
