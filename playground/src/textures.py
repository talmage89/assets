"""Original manufacture fields: coated metal, rotomolding and surfacing.

All artwork is analytic or seeded Pillow drawing. References never enter this
module. 4096 sources go through locked Cycles flat baking and kit filtering.
"""
import argparse,json,sys,math,random
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from kit.image_io import write_png
METAL={'Coat':(0,.75,.25,1),'Worn':(.25,.75,.5,1),'Cast':(.5,.75,.75,1),'Zinc':(.75,.75,1,1),'Deck':(0,.5,.5,.75),'ChalkCoat':(.5,.5,.75,.75),'Rubber':(.75,.5,1,.75),'WornDeck':(0,.25,.5,.5),'Chain':(.5,.25,.75,.5),'Fastener':(.75,.25,1,.5),'Label':(0,0,.5,.25),'Wood':(.5,0,.75,.25),'Black':(.75,0,1,.25)}
PLASTIC={k:(i%4/4,(1-i//4)/2,(i%4+1)/4,(2-i//4)/2) for i,k in enumerate(('Clean','Chalk','Slide','Seam','Seat','Rock','Initials','OldSlide'))}
SURFACE={'Fiber':(0,.5,.5,1),'OldFiber':(.5,.5,1,1),'EPDM':(0,0,.5,.5),'WornEPDM':(.5,0,1,.5)}
COVERAGE={'PlayMetal':.8,'PlayPlastic':1.6,'PlaySurface':4.}
HEIGHT={'PlayMetal':.012,'PlayPlastic':.0008,'PlaySurface':.015}

def worn_rect(year,rail=False):
    """Colored coating plus neutral exposed steel in the existing Worn cell."""
    row=(1996,2005,2013).index(year);column=int(rail)
    return (.25+column*.125,.75+(2-row)/12,.25+(column+1)*.125,.75+(3-row)/12)

def noise(w,h,n,seed):
    a=np.random.default_rng(seed).random((n,n),dtype=np.float32)
    return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC),dtype=np.float32)

def build_set(name,rects,n,out):
    base=Image.new('RGBA',(n,n),(210,210,210,255));orm=Image.new('RGB',(n,n),(255,180,0));hei=Image.new('I;16',(n,n),32768)
    for index,(key,rect) in enumerate(rects.items()):
        x0,y0,x1,y1=round(rect[0]*n),round((1-rect[3])*n),round(rect[2]*n),round((1-rect[1])*n);w=x1-x0;h=y1-y0
        yy,xx=np.mgrid[:h,:w].astype(np.float32);u=(xx+.5)/w;v=(yy+.5)/h
        rng=np.random.default_rng(index+724);fine=rng.random((h,w),dtype=np.float32);mid=noise(w,h,64,41+index)
        color=np.ones((h,w,3),np.float32)*.87;rough=np.ones((h,w),np.float32)*.39;metal=np.zeros((h,w),np.float32);alpha=np.ones((h,w),np.float32);height=.5+.025*(fine-.5)
        if name=='PlayMetal':
            if key in ('Coat','Worn','Cast','Weld'):
                rough=.34+.10*mid;orange=noise(w,h,280,index+14);height=.5+.018*(orange-.5)
                if key=='Cast':height+=.018*(mid-.5);rough+=.06
                if key=='Worn':
                    from finishes import PALETTES
                    col=np.minimum(1,(u*2).astype(int));row=np.minimum(2,(v*3).astype(int));uu=u*2-col;vv=v*3-row
                    paints=[]
                    for year,age in ((1996,1.),(2005,.55),(2013,.13)):
                        fade=age*.10
                        paints.append([.73*(np.array(PALETTES[year][k][:3])*(1-fade)+np.array((.34,.32,.28))*fade) for k in ('steel','rail')])
                    linear=np.array(paints)[row,col];color=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
                    edge=np.minimum.reduce([uu,vv,1-uu,1-vv]);chip=np.clip((mid-.50)*8,0,1)*np.clip((.23-edge)*14,0,1)*np.take(np.array((1.,.55,.13)),row)
                    color=color*(1-chip[:,:,None])+np.array((.61,.63,.62))*chip[:,:,None];rough+=.12*chip;metal=.92*chip;height-=.12*chip
                if key=='Weld':height+=.24*np.exp(-((v-.5)/.06)**2)*(.8+.2*np.sin(u*170))
            elif key=='Zinc':
                color[:]=(.63,.66,.67);color*=.93+.12*mid[:,:,None];metal[:]=.95;rough=.29+.10*mid;height=.5+.004*(fine-.5)
            elif key in ('Deck','WornDeck'):
                qx=u*16%1-.5;qy=v*8%1-.5;hole=np.hypot(qx,qy)<.15
                color[:]=.72;color[hole]=.04;rough=.65+.08*mid;height=.5-.42*hole+.015*(fine-.5);alpha[hole]=0
                if key=='WornDeck':
                    lane=np.exp(-((u-.5-.025*np.sin(v*7))/.24)**6)
                    nosing=.20+.80*np.exp(-((v-.82)/.19)**4)
                    wear=lane*nosing*(.74+.26*mid)
                    color[:]=.11;color=color*(1-wear[:,:,None])+np.array((.62,.64,.63))*wear[:,:,None];color[hole]=.025;rough-=.28*wear;metal=.92*wear;height-=.025*wear
            elif key=='ChalkCoat':
                color[:]=.87;color*=.97+.03*mid[:,:,None];rough=.62+.10*mid;height=.5+.018*(mid-.5)
            elif key in ('Rubber','Black'):
                color[:]=.65 if key=='Rubber' else .10;rough=.70+.12*mid;height=.5+.04*(fine-.5)
            elif key=='Fastener':
                x=u-.5;y=v-.5;hexagon=np.maximum.reduce([abs(x),abs(x*.5+y*.866),abs(x*.5-y*.866)])<.19;pin=np.hypot(x,y)<.032
                color[:]=(.70,.72,.71);color[hexagon]=(.15,.16,.16);color[pin]=(.74,.75,.74);rough=.32+.04*mid;metal[:]=.95;height=.5-.25*hexagon+.23*pin
            elif key=='Wood':
                line=np.sin(v*600+mid*4)+.5*np.sin(v*1700+mid*9);g=.42+.055*line
                color=np.stack((g*1.18,g,g*.76),axis=-1);rough[:]=.89;height=.5+.055*line
            elif key=='Chain':
                # Two alternating 6 mm wire links / actual 45 mm pitch.
                active=1-16/256
                x=(u-.5)*(.036/active);physical_y=(v-8/256)*(.72/active);y=(physical_y%.09)-.045;rx=.0105;ry=.025;r=.003
                phi=np.hypot(x/rx,y/ry)-1;gradient=np.sqrt((x/rx**2)**2+(y/ry**2)**2)
                distance=phi/np.maximum(gradient,1e-8);front=np.abs(distance)<r
                ey=((physical_y+.045)%.09)-.045;edge=(np.abs(x)<r)&(np.abs(ey)<.028)
                front_h=np.sqrt(np.maximum(0,r*r-distance*distance))*front
                edge_h=np.sqrt(np.maximum(0,r*r-x*x))*edge
                color[:]=(.14,.15,.14);rough[:]=.61;alpha=(front|edge).astype(np.float32);height=.5+np.maximum(front_h,edge_h)/.012
            elif key=='Label':color[:]=(.77,.75,.65);rough[:]=.66;height[:]=.5
        elif name=='PlayPlastic':
            rough=.34+.07*mid;height=.5+.012*(fine-.5)
            if key=='Chalk':color*=.93+.07*mid[:,:,None];rough=.66+.08*mid
            if key in ('Slide','OldSlide','Seat','Initials'):
                # Long bed-direction scratches, restricted away from the sidewall.
                lane=np.exp(-((u-.5)/.31)**4);streak=np.clip((np.sin(u*1600+mid*.9)-.87)*7,0,1)*lane
                streak*=np.clip(np.sin(v*9+u*40)+.5,0,1)
                color*=1-.13*streak[:,:,None];rough=.47-.16*lane+.17*streak;height-=.09*streak
                scars=np.zeros((h,w),np.float32);scar_rng=random.Random(index+908)
                for j in range(19 if key=='OldSlide' else 11):
                    x=scar_rng.uniform(.22,.78);width=scar_rng.uniform(.0018,.0045);begin=scar_rng.uniform(.06,.65);end=min(.97,begin+scar_rng.uniform(.15,.60));phase=scar_rng.random()*math.tau
                    trace=np.exp(-((u-x-.001* np.sin(v*29+phase))/width)**2)*np.clip((v-begin)*50,0,1)*np.clip((end-v)*50,0,1)
                    scars=np.maximum(scars,trace)
                color=np.minimum(.99,color*(1+.22*scars[:,:,None]));rough+=.29*scars;height-=.15*scars
                if key=='OldSlide':rough+=.20; color*=.96+.04*mid[:,:,None]
                if key in ('Slide','OldSlide'):height+=.16*(np.exp(-((u-.065)/.004)**2)+np.exp(-((u-.935)/.004)**2))
                if key=='Seat':rough+=.12
            if key=='Seam':
                seam=np.exp(-((u-.5)/.006)**2);height+=.23*seam;color*=1-.11*seam[:,:,None];rough+=.07*seam
            if key=='Rock':rough=.68+.10*mid;height=.5+.09*(mid-.5)
        else:
            if key in ('Fiber','OldFiber'):
                old=key=='OldFiber';rgb=Image.new('RGB',(w,h),(125,105,68));hm=Image.new('L',(w,h),45);draw=ImageDraw.Draw(rgb);dh=ImageDraw.Draw(hm);randomizer=random.Random(847+index)
                # A 2m tile: individual split fibers 12-45mm long, 2-7mm wide.
                for i in range(round(52000*(n/4096)**2)):
                    x=randomizer.uniform(-.02,1.02)*w;y=randomizer.uniform(-.02,1.02)*h;t=randomizer.random()*math.tau
                    L=randomizer.uniform(.012,.045)*w/2;W=randomizer.uniform(.002,.007)*w/2
                    a=(math.cos(t)*L/2,math.sin(t)*L/2);b=(-math.sin(t)*W/2,math.cos(t)*W/2)
                    poly=[(x-a[0],y-a[1]),(x+a[0]-.3*b[0],y+a[1]-.3*b[1]),(x+a[0]+b[0],y+a[1]+b[1]),(x-a[0]+b[0],y-a[1]+b[1])]
                    g=randomizer.uniform(.52,.82) if old else randomizer.uniform(.54,.84);c=(int(g*255),int(g*255*(.82 if old else .78)),int(g*255*(.50 if old else .48)))
                    draw.polygon(poly,fill=c);dh.polygon(poly,fill=randomizer.randint(105,225))
                    if i%3==0:draw.line((poly[0],poly[1]),fill=tuple(min(255,int(c1*1.13)) for c1 in c),width=1)
                color=np.asarray(rgb,dtype=np.float32)/255;raw=np.asarray(hm,dtype=np.float32)/255
                height=.15+.70*raw;rough=.90+.05*mid
            else:
                color[:]=.83;g=np.clip((fine-.3)*1.6,0,1);color*=.65+.35*g[:,:,None]
                black=fine<.20;color[black]=(.10,.105,.10);rough=.86+.06*mid;height=.5+.040*(fine-.5)
                if key=='WornEPDM':rough-=.14;color*=.88;height=.5+.025*(fine-.5)
        if name=='PlayMetal' and key not in ('Chain','Fastener'):height=.5+(height-.5)*.1
        arr=np.uint8(np.clip(np.dstack((color,alpha)),0,1)*255+.5);patch=Image.fromarray(arr)
        if key=='Label':
            d=ImageDraw.Draw(patch);font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),max(14,w//23))
            for i,text in enumerate(('MEADOWWORKS','PUBLIC PLAY SYSTEMS','AGES 5–12  /  ADULT SUPERVISION','MODEL P48 • INSPECT MONTHLY')):d.text((w*.05,h*(.12+i*.21)),text,font=font,fill=(27,39,35,255))
            d.rectangle((5,5,w-6,h-6),outline=(45,51,44,255),width=3)
        if key=='Initials':
            hh=Image.fromarray(np.uint8(np.clip(height,0,1)*255));d=ImageDraw.Draw(hh);d.text((w*.53,h*.70),'J + M',font=ImageFont.truetype(find_font('DejaVu Sans','Book'),max(18,w//13)),fill=74,stroke_width=0);height=np.asarray(hh,dtype=np.float32)/255
        base.paste(patch,(x0,y0));ao=np.clip(.70+.30*(height*2).clip(0,1),0,1) if name=='PlaySurface' else np.ones((h,w))
        if name=='PlayMetal' and key=='Fastener':ao=np.where(hexagon & ~pin,.4,1)
        orm.paste(Image.fromarray(np.uint8(np.clip(np.dstack((ao,rough,metal)),0,1)*255+.5)),(x0,y0));hei.paste(Image.fromarray(np.uint16(np.clip(height,0,1)*65535)),(x0,y0))
    out.mkdir(parents=True,exist_ok=True)
    if name=='PlaySurface':base=base.filter(ImageFilter.GaussianBlur(.65))
    base.save(out/f'T_{name}_BaseColor.png');orm.save(out/f'T_{name}_ORM.png');hei.save(out/f'T_{name}_Height.png')

def main():
    p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=4096);p.add_argument('--out',type=Path,default=Path('build/procedural'));a=p.parse_args()
    for name,rects in (('PlayMetal',METAL),('PlayPlastic',PLASTIC),('PlaySurface',SURFACE)):build_set(name,rects,a.size,a.out)
    (a.out/'layout.json').write_text(json.dumps(dict(Metal=METAL,Plastic=PLASTIC,Surface=SURFACE,coverage_m=COVERAGE,height_distance_m=HEIGHT),indent=2))
if __name__=='__main__':main()
