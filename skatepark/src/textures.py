"""Original cause-specific trim and phenolic fields; no reference pixels.

4096 source fields are baked with kit.flat_bake, then filtered with the kit.
Opaque trim, masked marks and rules use the same image triple.
"""
import sys,argparse,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png
from kit.fonts import find_font
RECTS=dict(Steel=(0,.75,.25,1),Wall=(.25,.75,.5,1),Coping=(.5,.75,1,1),Tile=(0,.5,.25,.75),Composite=(.25,.5,.5,.75),
           Paint=(.5,.5,.75,.75),Zinc=(.75,.5,1,.625),ToePlate=(.75,.625,1,.75),Burnish=(0,.25,.25,.5),Scrape=(.25,.25,.5,.5),
           Tag=(.5,.25,.75,.5),Dirt=(.75,.25,.875,.5),Crack=(.875,.25,1,.5),Rules=(0,0,1,.25))

def field(w,h,cells,seed):
    a=np.random.default_rng(seed).random((cells,cells),dtype=np.float32)
    return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC),dtype=np.float32)

def source(out,n):
    out.mkdir(parents=True,exist_ok=True)
    base=Image.new('RGBA',(n,n));orm=Image.new('RGB',(n,n));height=Image.new('I;16',(n,n),32768)
    for index,(name,rect) in enumerate(RECTS.items()):
        if name=='Grout':continue
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
            color=color*(1-crown[:,:,None])+np.array((.74,.77,.76))*crown[:,:,None]
            scratch=np.clip((np.sin(u*1400+mid*8)-.80)*6,0,1)*crown
            color-=scratch[:,:,None]*.10;metal=np.clip(.08+.87*crown-rust*.06,0,1);rough=.55-.32*crown+.3*rust;relief=.5-.04*scratch+.025*mid
        elif name=='Coping':
            worn=np.exp(-((v-.91)/.125)**4)*(.70+.30*mid)
            stains=np.exp(-v*6)*np.clip((broad-.3)*1.4,0,.6)
            edge=np.minimum.reduce([u,1-u,v,1-v])
            chips=np.clip((mid-.65)*7,0,1)*np.exp(-edge*32)
            aggregate=np.clip((fine-.68)*5,0,1)*np.clip((mid-.28)*2,0,1)
            color[:]=(.68,.665,.62);color*=1-.27*stains[:,:,None]-.34*chips[:,:,None]-.22*aggregate[:,:,None]
            color=color*(1-.85*worn[:,:,None])+np.array((.13,.125,.115))*.85*worn[:,:,None]
            rough=.81-.22*worn+.08*chips;relief=.5-.38*chips-.045*aggregate+.014*mid
        elif name=='Wall':
            column=field(w,1,92,661)[0][None,:]
            tracks=np.clip((column-.38)*3,0,1)
            runoff=tracks*np.exp(-v*(2.0+7*mid))*np.sin(np.pi*u)**.25
            foot=np.exp(-(1-v)*19)*(.3+.7*broad)
            grain=field(w,h,512,1650+index)
            g=.70+.09*(grain-.5)+.020*(column-.5)
            color=np.stack((g,g*.986,g*.955),axis=-1)*np.ones((h,1,1))
            color*=1-.35*runoff[:,:,None]-.12*foot[:,:,None]
            # Short paired urethane contacts below the pumping lines. These
            # occupy the lower part of the chart: shallow retaining walls
            # sample only its top, while bowl transitions use its full height.
            wheel=np.zeros((h,w),np.float32)
            for cx,start,end,bend in ((.18,.32,.46,.030),(.59,.52,.72,-.045),(.79,.70,.90,.025)):
                t=(v-start)/(end-start);tt=np.clip(t,0,1)
                center=cx+bend*np.sin(tt*np.pi)
                pair=np.maximum(np.exp(-((u-center-.035)/.0045)**4),np.exp(-((u-center+.035)/.0045)**4))
                envelope=np.maximum(np.sin(np.pi*tt),0)**.45*((t>0)&(t<1))
                wheel=np.maximum(wheel,pair*envelope*np.clip((field(w,h,110,421+int(cx*100))-.30)*2,0,1))
            color*=1-.52*wheel[:,:,None]
            color[:,:,2]*=1-.18*runoff;rough=.82-.06*runoff-.08*wheel;relief=np.full((h,w),.5)
        elif name=='Composite':
            lane=np.maximum(np.exp(-((u-.28-.025*np.sin(v*8))/.12)**4),np.exp(-((u-.70-.04*np.sin(v*9))/.10)**4))
            edge=np.exp(-np.minimum(u,1-u)*38)
            g=.31+.13*lane+.035*(broad-.5)-.065*edge
            wheel=np.zeros((h,w),np.float32)
            for cx,start,end,phase in ((.25,.06,.31,.2),(.32,.42,.67,1.1),(.68,.20,.44,2.3),(.74,.64,.91,3.5)):
                t=np.clip((v-start)/(end-start),0,1)
                center=cx+.022*np.sin(v*9+phase)
                contact=np.exp(-((u-center)/(.0025+.0015*mid))**2)*np.maximum(np.sin(np.pi*t),0)**.6
                contact*=.30+.70*field(w,h,150,1440+int(cx*100))
                wheel=np.maximum(wheel,contact)
            g*=1-.65*wheel
            color=np.stack((g*1.12,g*.91,g*.71),axis=-1);rough=.83-.22*lane;relief=.5+.015*(fine-.5)-.018*edge
        elif name=='Tile':
            gx=u*8%1;gy=v*8%1;grout=(np.minimum.reduce([gx,1-gx,gy,1-gy])<.032).astype(float)
            cell=(np.floor(u*8)*17+np.floor(v*8)*13)%19
            missing=((cell==8)&(mid>.3)).astype(float)
            salts=np.clip((v-.5)*1.2,0,.35)*broad
            grime=np.exp(-v*5)*(.4+.6*mid)
            color[:]=(.11,.29,.35);color*=.9+.2*mid[:,:,None]
            color=color*(1-grout[:,:,None])+np.array((.38,.37,.31))*grout[:,:,None]
            color=color*(1-missing[:,:,None])+np.array((.34,.31,.25))*missing[:,:,None]
            color+=salts[:,:,None]*.22;color*=1-.65*grime[:,:,None];rough=.31+.4*grout+.5*missing;relief=.5-.12*grout-.26*missing
        elif name=='Grout':color[:]=(.43,.42,.37);color*=.85+.18*broad[:,:,None];rough[:]=.91
        elif name=='Paint':
            edge=np.minimum.reduce([u,1-u,v,1-v]);exposed=np.clip((mid-.42)*5,0,1)*np.exp(-edge*48)
            corners=np.maximum(np.exp(-((u-.04)/.075)**4-((v-.06)/.095)**4),np.exp(-((u-.95)/.070)**4-((v-.91)/.110)**4))
            exposed=np.maximum(exposed,corners*(.45+.45*mid))
            color[:]=(.09,.18,.155);color=color*(1-exposed[:,:,None])+np.array((.37,.28,.17))*exposed[:,:,None];rough=.72+.12*exposed;metal=.15+.45*exposed
        elif name in ('Zinc','ToePlate'):
            # Millimeter-scale zinc grain, not stretched centimeter ripples.
            # Its physical relief is microns; the adjacent coping chips are
            # tenths of millimeters and deliberately retain their own height.
            grain=field(w,h,512,1720+index)
            color[:]=(.72,.75,.76);color*=.92+.12*grain[:,:,None];metal[:]=.86;rough=.37+.11*(broad-.5);relief=.5+.0015*(fine-.5)
            if name=='ToePlate':
                scuff=np.clip((np.sin(u*330+mid*4)-.83)*5,0,1)*np.exp(-((v-.4)/.36)**4)
                rust=np.clip((mid-.35)*3,0,1)*np.exp(-np.minimum.reduce([u,1-u,v,1-v])*36)
                color=color*(1-rust[:,:,None])+np.array((.27,.15,.07))*rust[:,:,None]
                color+=scuff[:,:,None]*.20;metal=.94-.9*rust;rough+=.47*rust-scuff*.19;relief=.5-.004*scuff+.002*(fine-.5)
        elif name=='Burnish':
            # Smoother, slightly darker riding route, interrupted at grain scale.
            broad_route=np.sin(np.pi*u)**1.8*np.sin(np.pi*v)**.55
            coverage=np.clip((mid-.25)*1.8,0,1)*broad_route*.12
            pair=np.maximum(np.exp(-((u-.34-.035*np.sin(v*19))/(.035+.010*mid))**4),np.exp(-((u-.67-.035*np.sin(v*19))/(.037+.012*mid))**4))
            ends=np.maximum(np.exp(-((v-.11)/.14)**4),np.exp(-((v-.88)/.15)**4))
            contact=pair*np.clip((field(w,h,44,187)-.43)*4,0,1)*ends
            tail=np.exp(-((v-.78)/.017)**4)*np.exp(-((u-.52)/.30)**4)
            black=np.clip(contact*.78+tail*.40,0,.88)
            a=np.maximum(coverage,black)
            color[:]=(.59,.585,.565)
            color=color*(1-black[:,:,None])+np.array((.10,.105,.10))*black[:,:,None]
            rough=.40+.22*black;relief[:]=.5
        elif name=='Scrape':
            # Centimeter board contacts at the lip, no continuous painted band.
            line=np.clip((np.sin(u*390+mid*7)-.55)*3,0,1)
            a=line*np.sin(np.pi*v)**1.6*np.clip((broad-.35)*3,0,1)*.82
            color[:]=(.105,.11,.105);rough[:]=.45;relief=.5-line*.006
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
    # Fictional aerosol monogram: variable pressure, overspray, runs, buff ghost.
    from random import Random
    rng=Random(410);q=n//4;mask=Image.new('L',(q,q));d=ImageDraw.Draw(mask)
    paths=[[(.12,.68),(.24,.25),(.31,.20),(.21,.47),(.43,.40)],[(.32,.70),(.46,.25),(.59,.28),(.47,.45),(.38,.47),(.62,.68)],[(.58,.65),(.66,.27),(.70,.59),(.83,.25)],[(.14,.74),(.78,.67),(.89,.57)]]
    for path in paths:
        for (x,y),(xx,yy) in zip(path,path[1:]):
            steps=80
            for j in range(steps):
                t=j/(steps-1);cx=(x+(xx-x)*t+.008*math.sin(t*math.pi)*math.sin(y*40))*q;cy=(y+(yy-y)*t+.014*math.sin(t*math.pi)*math.sin(x*30))*q
                radius=q*(.007+.004*math.sin(j*.08+cx*.02))
                d.ellipse((cx-radius,cy-radius*3.85,cx+radius,cy+radius*3.85),fill=210)
    for x,y,length in [(.24,.48,.23),(.62,.68,.15),(.70,.59,.24)]:
        d.line((x*q,y*q,(x+.005)*q,(y+length)*q),fill=150,width=max(1,q//180))
        d.ellipse(((x+.005)*q-2,(y+length)*q-2,(x+.005)*q+2,(y+length)*q+2),fill=175)
    overspray=mask.filter(ImageFilter.GaussianBlur(q*.008));aa=np.maximum(np.asarray(mask),np.asarray(overspray)*.6).astype('uint8')
    aa=np.rint(aa*(.80+.20*field(q,q,160,330))).astype('uint8')
    rgba=Image.new('RGBA',(q,q),(31,57,51,0));rgba.putalpha(Image.fromarray(aa))
    # A faint gray buff occupies one margin beside the current paint.
    ghost=Image.new('RGBA',(q,q));gd=ImageDraw.Draw(ghost)
    gd.rounded_rectangle((q*.015,q*.22,q*.19,q*.88),radius=q*.025,fill=(153,151,139,90))
    rgba=Image.alpha_composite(ghost,rgba)
    base.paste(rgba,(n//2,n//2))
    base.save(out/'T_SkateTrim_BaseColor.png');orm.save(out/'T_SkateTrim_ORM.png');height.save(out/'T_SkateTrim_Height.png')
    # One full 1024 shared concrete surface set: the same 4 MiB allocation.
    surface(out,n)
    (out/'layout.json').write_text(json.dumps(RECTS,indent=2))
    (out/'.stamp').touch()

# Mortar samples an existing quiet coping patch, without an extra atlas region.
RECTS['Grout']=(.96,.96,.985,.985)

def surface(out,n):
    # Full-size concrete tile. Troweled rides suppress its physical bristle
    # normal; broom walks retain it. Flat-bake coverage is 3.048m, delivered
    # repeat 1.524m (see bake_tiles.py and finishes.py).
    v,u=np.mgrid[:n,:n].astype(np.float32);u/=n;v/=n
    broad=field(n,n,18,220);mid=field(n,n,90,1220);grain=field(n,n,700,217)
    fine=np.random.default_rng(310).random((n,n),dtype=np.float32)
    g=.67+.030*(broad-.5)+.035*(mid-.5)+.020*(grain-.5)
    arcs=np.sin(170*np.sqrt((u+.2)**2+(v-.14)**2)+mid*1.4)
    trowel=np.clip((arcs-.76)*3,0,1)*(.3+.7*mid)
    pores=np.clip((grain-.77)*5,0,1)*np.clip((fine-.80)*6,0,1)
    color=np.stack([g,g*.989,g*.955],axis=-1)*(1-.025*trowel[:,:,None]-.15*pores[:,:,None])
    bristle=np.sin(u*2800+field(n,n,90,302)*.7)
    rough=.86-.17*trowel+.06*(mid-.5)
    relief=.5+.09*bristle+.012*(grain-.5)-.14*pores
    for ch,arr in [('BaseColor',color),('ORM',np.stack((np.ones_like(rough),rough,np.zeros_like(rough)),axis=-1)),('Height',relief[:,:,None])]:
        write_png(out/f'T_Prefab_{ch}.png',arr,bits=16 if ch=='Height' else 8)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('build/procedural'));ap.add_argument('--size',type=int,default=4096);a=ap.parse_args();source(a.out,a.size)
