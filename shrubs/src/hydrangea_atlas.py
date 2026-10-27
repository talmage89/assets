"""Original serrate bigleaf blades and four-sepal florets; analytic pixels only."""
import math,random
import numpy as np
from PIL import Image,ImageDraw

LEAF_RECTS=[(.25,.5,.5,.75),(.5,.5,.75,.75)]
FLOWER_RECTS=[(.75,.5,1,.75),(.25,.75,.5,1),(.5,.75,.75,1),(.75,.75,1,1)]


def paint(color,normal,orm,size):
    records=[]
    for k,rect in enumerate(LEAF_RECTS+FLOWER_RECTS):
        rng=random.Random(1290+k);u0,v0,u1,v1=rect
        xa,xb=round(size*u0),round(size*u1);ya,yb=round(size*(1-v1)),round(size*(1-v0));w,h=xb-xa,yb-ya
        tile=Image.new('RGBA',(w,h),(64,96,39,0));draw=ImageDraw.Draw(tile)
        nm=np.full((h,w,3),(128,128,255),np.uint8);rm=np.full((h,w,3),(255,148,0),np.uint8)
        yy,xx=np.mgrid[:h,:w];x=(xx+.5)/w;y=1-(yy+.5)/h
        def pt(a,b):return (round(a*w),round((1-b)*h))
        if k<2:
            # Coarse asymmetric teeth, broad ovate blade, raised pinnate veins.
            shape=[]
            for side in (1,-1):
                ts=np.linspace(.075,.94,127) if side==1 else np.linspace(.94,.075,127)
                for t in ts:
                    f=(t-.075)/.865
                    width=.407*math.sin(math.pi*f)**.72*(1.07-.20*f)
                    tooth=.018*(1-abs(((f*19)%1)*2-1))*(math.sin(math.pi*f)**.4)
                    shape.append(pt(.5+side*(width+tooth),t))
            maskim=Image.new('L',(w,h));ImageDraw.Draw(maskim).polygon(shape,fill=255);mask=np.asarray(maskim)>0
            vein=np.exp(-((x-.5)/.008)**2)
            secondary=np.exp(-((np.mod(y-np.abs(x-.5)*.88,.135)-.05)/.007)**2)*(1-np.exp(-np.abs(x-.5)*30))
            base=np.array((44,73,35) if k==0 else (57,77,38),float)
            fine=np.sin(x*335+y*97)*np.sin(y*421-x*33)
            rgb=base+vein[:,:,None]*np.array([9,15,5])+secondary[:,:,None]*np.array([4,7,2])+fine[:,:,None]*.6
            rgba=np.zeros((h,w,4),np.uint8);rgba[mask,:3]=np.clip(rgb[mask],0,255);rgba[mask,3]=255;tile=Image.fromarray(rgba)
            sx=.40*(x-.5)-.09*np.sign(x-.5)*vein;sy=.05*np.cos((y-np.abs(x-.5)*.88)*46)*secondary
            ns=np.stack([-sx,-sy,np.ones_like(sx)],-1);ns/=np.linalg.norm(ns,axis=-1)[:,:,None];nm[mask]=((ns[mask]*.5+.5)*255).astype(np.uint8)
            rm[mask]=(255,142,0)
            petiole=(np.abs(x-.5)<.0065)&(y<.102)
            rgba=np.asarray(tile).copy();rgba[petiole]=(68,74,37,255);tile=Image.fromarray(rgba)
            nm[petiole]=(128,128,255);rm[petiole]=(255,174,0)
        else:
            palette=[(76,102,147),(91,104,144),(132,97,123),(100,115,155)]
            base=np.array(palette[k-2],float)
            # A small three-floret cluster provides head grain efficiently.
            # Each floret still has four unequal enlarged sterile sepals.
            for fi,(cx,cy) in enumerate(((.28,.30),(.69,.38),(.45,.76))):
                angle=rng.random()*math.tau;scale=rng.uniform(.57,.64)
                for petal in range(4):
                    a=angle+petal*math.pi/2+rng.uniform(-.12,.12);ca,sa=math.cos(a),math.sin(a)
                    dx=(x-cx)/scale;dy=(y-cy)/scale;along=dx*ca+dy*sa;across=-dx*sa+dy*ca
                    mask=((along-.205)/.258)**2+(across/.235)**2<1;mask &= along>-.015
                    vein=np.exp(-(across/.012)**2)*np.clip(along*2,0,1)
                    fine=np.sin(along*92+across*13)*.55
                    rgb=base*rng.uniform(.88,1.09)+vein[:,:,None]*np.array([6,7,7])+fine[:,:,None]
                    rgba=np.zeros((h,w,4),np.uint8);rgba[mask,:3]=np.clip(rgb[mask],0,255);rgba[mask,3]=255;tile.alpha_composite(Image.fromarray(rgba))
                    saxis=(along-.15)*1.6+rng.uniform(-.16,.16);cross=across*.9
                    nx=-(saxis*ca-cross*sa);ny=-(saxis*sa+cross*ca)
                    ns=np.stack([nx,ny,np.ones_like(nx)],-1);ns/=np.linalg.norm(ns,axis=-1)[:,:,None];nm[mask]=((ns[mask]*.5+.5)*255).astype(np.uint8);rm[mask]=(255,rng.randrange(158,182),0)
                draw=ImageDraw.Draw(tile);rr=.021;draw.ellipse((w*(cx-rr),h*(1-cy-rr),w*(cx+rr),h*(1-cy+rr)),fill=(134,146,103,255))
        rgba=np.asarray(tile).copy();alpha=rgba[:,:,3].copy();occupied=alpha>0
        for _ in range(6):
            fresh=occupied.copy()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                take=np.roll(occupied,(dy,dx),(0,1))&~fresh
                rgba[take,:3]=np.roll(rgba,(dy,dx),(0,1))[take,:3];nm[take]=np.roll(nm,(dy,dx),(0,1))[take];rm[take]=np.roll(rm,(dy,dx),(0,1))[take];fresh|=take
            occupied=fresh
        rgba[:,:,3]=alpha;color[ya:yb,xa:xb]=rgba;normal[ya:yb,xa:xb]=nm;orm[ya:yb,xa:xb]=rm
        records.append(dict(rect=rect,kind='serrate broad leaf' if k<2 else 'three clustered four-sepal sterile florets'))
    return records


def branchlet_tile(color,normal,orm,size):
    """Six original coarse blades on three opposite nodes for hidden core depth.

    Composite only our analytically generated leaf tile, never reference pixels.
    Palette/normal provenance remains the same shared three-map source.
    """
    from PIL import ImageOps
    source_rect=LEAF_RECTS[0];target_rect=LEAF_RECTS[1]
    def box(rect):
        a,b,c,d=rect;return (round(a*size),round((1-d)*size),round(c*size),round((1-b)*size))
    xa,ya,xb,yb=box(source_rect);leaf=Image.fromarray(color[ya:yb,xa:xb]);leafnm=Image.fromarray(normal[ya:yb,xa:xb]);w=xb-xa
    tile=Image.new('RGBA',(w,w),(44,73,35,0));normal_tile=Image.new('RGBA',(w,w),(128,128,255,0));draw=ImageDraw.Draw(tile)
    draw.line([(w*.50,w*.98),(w*.47,w*.14)],fill=(76,74,38,255),width=max(2,round(w*.005)))
    rng=random.Random(9988);records=[]
    for node,t in enumerate((.25,.48,.71)):
        for side in (-1,1):
            length=rng.uniform(.117,.145);scale=length/.36/.865;edge=round(w*scale)
            angle=side*rng.uniform(47,73)
            blade=leaf.resize((edge,edge),Image.Resampling.LANCZOS).rotate(angle,Image.Resampling.BICUBIC,expand=True)
            # Rotate the petiole's base offset about the source image center.
            a=math.radians(angle);bx=math.sin(a)*edge*.5;by=math.cos(a)*edge*.5
            x=w*(.5+(node-1)*.015)-blade.width*.5-bx;y=w*(1-t)-blade.height*.5-by
            tile.alpha_composite(blade,(round(x),round(y)))
            values=np.asarray(leafnm).astype(float)/255*2-1;nx=values[:,:,0].copy();ny=values[:,:,1].copy()
            values[:,:,0]=nx*math.cos(a)-ny*math.sin(a);values[:,:,1]=nx*math.sin(a)+ny*math.cos(a)
            normal_rgba=np.dstack([np.clip((values*.5+.5)*255,0,255).astype(np.uint8),np.asarray(leaf)[:,:,3]])
            normal_blade=Image.fromarray(normal_rgba).resize((edge,edge),Image.Resampling.LANCZOS).rotate(angle,Image.Resampling.BICUBIC,expand=True)
            normal_tile.alpha_composite(normal_blade,(round(x),round(y)));records.append(length)
    xa,ya,xb,yb=box(target_rect);rgba=np.asarray(tile).copy();alpha=rgba[:,:,3].copy();occupied=alpha>0
    nm=np.asarray(normal_tile)[:,:,:3].copy()
    for _ in range(5):
        fresh=occupied.copy()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            take=np.roll(occupied,(dy,dx),(0,1))&~fresh;rgba[take,:3]=np.roll(rgba,(dy,dx),(0,1))[take,:3];nm[take]=np.roll(nm,(dy,dx),(0,1))[take];fresh|=take
        occupied=fresh
    rgba[:,:,3]=alpha;color[ya:yb,xa:xb]=rgba;normal[ya:yb,xa:xb]=nm;orm[ya:yb,xa:xb]=(255,153,0)
    return dict(rect=target_rect,kind='six opposite core leaves',blade_lengths_m=records,card_size_m=.36)
