"""Original late-summer turf: seeded blades, thatch, clover and exposed soil.

PIL draws authored botanical shapes, never photographic pixels. Tile-edge
strokes wrap in both axes. The same palette serves the upright edging cards.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from kit.image_io import write_png,srgb_to_linear,linear_to_srgb


def lawn(out, n, coverage, noise):
    rng=np.random.default_rng(392607)
    fine=noise(n,512,rng);root=noise(n,16,rng)
    soil=np.stack((.20+.06*fine,.174+.047*fine,.112+.035*fine),axis=-1)
    im=Image.fromarray(np.uint8(np.clip(soil,0,1)*255),'RGB')
    height=Image.fromarray(np.uint8(30+22*fine),'L')
    d=ImageDraw.Draw(im);hd=ImageDraw.Draw(height)
    px=n/coverage
    # A thin sward exposes irregular bits of soil/thatch, rather than a brown
    # color wash. Green clover persists in some of these dry areas.
    sparse=noise(512,8,rng)
    for j in range(23000):
        x,y=rng.uniform(0,n,2)
        density=float(sparse[int(y/n*512)%512,int(x/n*512)%512])
        count=round(12+10*density) if density>.20 else 7
        for k in range(count):
            angle=rng.uniform(0,math.tau)
            length=rng.uniform(.012,.038)*px
            start=(x+rng.normal(0,.011)*px,y+rng.normal(0,.011)*px)
            end=(start[0]+math.cos(angle)*length,start[1]+math.sin(angle)*length)
            bend=(start[0]+math.cos(angle+.35)*length*.6,start[1]+math.sin(angle+.35)*length*.6)
            dry=rng.random()<(.10 if density>.20 else .38)
            t=rng.random()
            col=(int(91+35*t),int(86+28*t),int(43+20*t)) if dry else (int(43+42*t),int(62+41*t),int(24+21*t))
            width=max(1,round(rng.uniform(.0011,.0026)*px))
            h=int(rng.uniform(90,225))
            for dx in (-n,0,n):
                for dy in (-n,0,n):
                    pts=[(a+dx,b+dy) for a,b in (start,bend,end)]
                    if max(p[0] for p in pts)<0 or min(p[0] for p in pts)>n or max(p[1] for p in pts)<0 or min(p[1] for p in pts)>n:continue
                    d.line(pts,fill=col,width=width,joint='curve')
                    hd.line(pts,fill=h,width=width,joint='curve')
                    d.line([pts[1],pts[2]],fill=tuple(min(255,c+9) for c in col),width=1)
    for j in range(1150):
        x,y=rng.uniform(0,n,2);size=rng.uniform(.004,.009)*px
        col=tuple(int(c) for c in (rng.uniform(43,66),rng.uniform(67,94),rng.uniform(30,48)))
        for k in range(3):
            theta=k*math.tau/3+rng.uniform(-.13,.13)
            cx=x+math.cos(theta)*size;cy=y+math.sin(theta)*size
            for dx in (-n,0,n):
                for dy in (-n,0,n):
                    if not -size<cx+dx<n+size or not -size<cy+dy<n+size:continue
                    box=(cx+dx-size*.7,cy+dy-size*.55,cx+dx+size*.7,cy+dy+size*.55)
                    d.ellipse(box,fill=col);hd.ellipse(box,fill=190)
                    d.line((cx+dx-size*.40,cy+dy,cx+dx+size*.25,cy+dy-size*.12),fill=(84,107,52),width=max(1,round(n/4096)))
    col=srgb_to_linear(np.asarray(im,dtype=np.float32)/255)
    # Antialias authored sub-millimeter stroke edges in linear light before
    # the Cycles texel-footprint bake. The wrapped half-texel filter keeps
    # dense leaf tips from changing materially under bake antialias sampling.
    weight=.19
    for axis in (0,1):col=(col+weight*(np.roll(col,1,axis=axis)+np.roll(col,-1,axis=axis)))/(1+2*weight)
    col=linear_to_srgb(col)
    h=np.asarray(height,dtype=np.float32)/255
    # Physical microrelief, 2.6 mm full encoded range. Edge cards provide the
    # actual 35–80 mm blade silhouette that a flat normal cannot carry.
    write_png(out/'T_Lawn_BaseColor.png',col)
    write_png(out/'T_Lawn_Height.png',(.15+.65*h)[:,:,None],16)
    write_png(out/'T_Lawn_ORM.png',np.stack((.77+.22*h,.94-.045*h,np.zeros_like(h)),axis=-1))


def edging(w,h):
    """Eight independently seeded .24 × .09 m tufts, on transparent cells."""
    rng=np.random.default_rng(92614);im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im)
    for cell in range(4):
        for row in range(2):
            x0=cell*w/4;y0=row*h/2;cw=w/4;ch=h/2
            for k in range(67):
                x=x0+rng.uniform(.06,.94)*cw
                base=y0+ch*.95;top=y0+ch*rng.uniform(.12,.60)
                dx=rng.uniform(-.14,.14)*cw
                width=max(1.1,rng.uniform(.001,.0024)/.24*cw)
                t=rng.random();dry=t<.2
                col=(int(98+t*31),int(88+t*24),int(42+t*15),255) if dry else (int(42+t*44),int(61+t*40),int(24+t*20),255)
                p1=(x+dx*.20,base-(base-top)*.42);p2=(x+dx*.70,top+(base-top)*.15)
                d.polygon([(x-width,base),(x+width,base),(p1[0]+width*.70,p1[1]),(p2[0]+width*.30,p2[1]),(x+dx,top),(p2[0]-width*.30,p2[1]),(p1[0]-width*.70,p1[1])],fill=col)
    a=np.asarray(im,dtype=np.float32)/255
    # Color bleed in transparent texels prevents dark mip borders.
    a[a[:,:,3]==0,:3]=(.27,.35,.15)
    return a


def iron(kind,w,h,field,fine):
    """Sand-cast iron, abrasion on raised lands and oxidation in recesses."""
    yy,xx=np.mgrid[:h,:w].astype(np.float32);u=(xx+.5)/w;v=(yy+.5)/h
    r=np.sqrt((u-.5)**2+(v-.5)**2)*2
    col=np.zeros((h,w,3),np.float32)
    height=(fine-.5)*.0004
    rough=np.full((h,w),.82,np.float32);metal=np.full((h,w),.64,np.float32)
    if kind=='manhole':
        # 26 mm square waffle lands. Original fictional foundry bars interrupt
        # the grid; no trademark or photograph is copied.
        pitch=.070/.6096
        a=np.abs((u-.5+pitch/2)%pitch-pitch/2)
        b=np.abs((v-.5+pitch/2)%pitch-pitch/2)
        cx=np.round((u-.5)/pitch)*.070;cy=np.round((v-.5)/pitch)*.070
        cast_land=(np.hypot(cx,cy)<=.269)&~((np.abs(cy)<.075)&(np.abs(cx)<.20))
        pads=np.clip((.010/.6096-np.maximum(a,b))*w/2,0,1)*cast_land
        # Water/dirt linger at the casting seat and around each raised land.
        # No broad random rust islands: they read as camouflage in the pair.
        blank=~cast_land
        skirt=np.exp(-((np.maximum(a,b)-.012/.6096)/(.003/.6096))**2)*(~blank)
        rust=skirt*.32*(.8+.2*fine)
        rust=np.maximum(rust,np.exp(-((r-.94)/.018)**2)*.56*(.25+.75*field))
        col[:]=(.151,.146,.135);col+=((fine-.5)*.033+(field-.5)*.010)[:,:,None]
        col=col*(1-rust[:,:,None])+np.array((.285,.142,.062))*rust[:,:,None]
        col+=pads[:,:,None]*np.array((.015,.022,.022))
        height+=pads*.00008;rough-=pads*.36;metal[:]=.38;metal+=pads*.12;metal-=rust*.28
        text=Image.new('L',(w,h));d=ImageDraw.Draw(text)
        font=ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSansCondensed-Bold.ttf',max(8,round(w*.069)))
        for label,y in [('ALDERVALE',.43),('SANITARY',.55)]:
            d.text((w*.5,h*(y+.04)),label,font=font,fill=240,anchor='mm',stroke_width=0)
        t=np.asarray(text,dtype=np.float32)/255
        mask=(t>0).astype(float);height=height*(1-mask)+t*.0014
        col=col*(1-mask[:,:,None])+(.105+.035*t)[:,:,None]*mask[:,:,None]
        rough=rough*(1-mask)+(.84-.28*t)*mask
        # Pick recesses and circumferential cast rim only change the normal;
        # the load-bearing frame/lid gap is modeled separately.
        for cx in (.16,.84):
            slot=((u-cx)/.023)**2+((v-.5)/.045)**2<1
            col[slot]=(.07,.064,.050);height[slot]-=.002;metal[slot]=.1
    else:
        # U < .5 receives upward casting faces, U > .5 the sheltered
        # vertical walls. Rust stays in those wet walls and narrow frame edges.
        top=u<.5
        q=np.where(top,u/.5,(u-.5)/.5)
        edge=np.exp(-np.minimum.reduce((q,1-q,v,1-v))*55)
        retention=np.clip((field-.50)*3,0,1)*(.35+.65*fine)
        rust=np.where(top,edge*.34*retention,(.06+.22*retention))
        base=np.array((.185,.177,.162));oxide=np.array((.29,.137,.056))
        col[:]=base;col+=((fine-.5)*.034+(field-.5)*.008)[:,:,None]
        col=col*(1-rust[:,:,None])+oxide*rust[:,:,None]
        # Contact planes receive a dark burnish, without orange top coatings.
        rough[:]=np.where(top,.70,.88);rough+=(fine-.5)*.045
        metal[:]=np.where(top,.43,.16);metal*=1-rust*.8
        height=(fine-.5)*.00030
        if kind=='foundry':
            text=Image.new('L',(w,h));d=ImageDraw.Draw(text)
            font=ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSansCondensed-Bold.ttf',max(8,round(w*.115)))
            d.text((w/2,h*.38),'ALDERVALE',font=font,anchor='mm',fill=255)
            small=ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSansCondensed-Bold.ttf',max(8,round(w*.050)))
            d.text((w/2,h*.66),'DUMP NO WASTE',font=small,anchor='mm',fill=255)
            d.text((w/2,h*.78),'DRAINS TO STREAM',font=small,anchor='mm',fill=255)
            t=np.asarray(text,dtype=np.float32)/255
            height+=t*.0012;col[:]=(.15,.143,.126);col+=t[:,:,None]*.012;rough-=t*.12
    return col,height,rough,metal
