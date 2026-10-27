"""Original pin-oak atlas: alternate distal clusters, U sinuses and bristle tips.

Eight independently grown sprays with staggered short side shoots. Physical blade dimensions are
recorded before the documented per-card scaling. No reference image is read.
"""
from pathlib import Path
import math,random,json
import numpy as np
from PIL import Image,ImageDraw


def outline(rng):
    # One side of a 5/7-lobed blade, with narrow bristle apices and round deep
    # sinuses. Cubic segments form the U bottoms; no photo outline is traced.
    seven=rng.random()<.78
    tips=[(.30,.22),(.40,.53),(.27,.81)] if seven else [(.36,.30),(.32,.70)]
    points=[(0,0)];veins=[]
    for sign in (-1,1):
        half=[(0,0)]
        for j,(width,height) in enumerate(tips):
            width*=rng.uniform(.88,1.10);height+=rng.uniform(-.025,.025)
            half.extend([(sign*width*.62,height-.10),(sign*width,height),
                         (sign*(width+.018),height+.037), # bristle
                         (sign*width*.88,height+.020)])
            veins.append((sign*width,height))
            if j<len(tips)-1:
                end=height+.11
                A=np.array([sign*width*.88,height+.020]);B=np.array([sign*.028,end])
                C=np.array([sign*.020,end+.035]);D=np.array([sign*.065,end+.060])
                for t in np.linspace(.15,1,8):half.append(tuple((1-t)**3*A+3*(1-t)**2*t*B+3*(1-t)*t*t*C+t**3*D))
        half.extend([(sign*.055,.872),(sign*.030,.900),(sign*.065,.927),(0,1.015)])
        if sign==-1:left=half
        else:right=half
    return left+right[-2:0:-1],veins


def generate(folder,size,species):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    color=np.full((size,size,4),(*species.LEAF_COLOR,0),np.uint8)
    normal=np.full((size,size,3),(128,128,255),np.uint8)
    orm=np.full((size,size,3),(255,110,0),np.uint8);variants=[]
    for k,rect in enumerate(species.LEAF_RECTS):
        rng=random.Random(species.SEED+101+k*79);u0,v0,u1,v1=rect
        xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size);w,h=xb-xa,yb-ya
        tile=Image.new('RGBA',(w,h),(*species.LEAF_COLOR,0));draw=ImageDraw.Draw(tile)
        nm=np.full((h,w,3),(128,128,255),np.uint8);rm=np.full((h,w,3),(255,110,0),np.uint8)
        def pt(x,y):return round(x*w),round((1-y)*h)
        count=0;lengths=[];lobes=[];damaged=0
        # One curved continuation, with laterals starting at different nodes.
        # Different branch counts and attachments prevent the old repeated
        # bare pitchfork shape. Each blade still has its own original outline.
        base_origin=(rng.uniform(.40,.56),.045)
        main_tip=(rng.uniform(.40,.62),rng.uniform(.86,.94));main_bend=rng.uniform(-.07,.07)
        def main_shoot(t):return (base_origin[0]+(main_tip[0]-base_origin[0])*t+main_bend*math.sin(t*math.pi),base_origin[1]+(main_tip[1]-base_origin[1])*t)
        axes=[(base_origin,main_tip,main_bend)]
        lateral_count=2+k%2
        for q in range(lateral_count):
            start=.20+q*.19+rng.uniform(-.04,.04)
            sign=-1 if (q+k)%2 else 1
            origin=main_shoot(start)
            tip=(rng.uniform(.16,.28) if sign<0 else rng.uniform(.72,.84),rng.uniform(.66,.88))
            axes.append((origin,tip,rng.uniform(-.06,.06)))
        for q,(origin,tip,bend) in enumerate(axes):
            nodes=(17+(k+q)%2) if len(axes)==3 else (12+(k+q)%3)
            def shoot(t):return (origin[0]+(tip[0]-origin[0])*t+bend*math.sin(t*math.pi),origin[1]+(tip[1]-origin[1])*t)
            draw.line([pt(*shoot(t)) for t in np.linspace(0,1,20)],fill=(*species.TWIG_COLOR,255),width=max(1,round(w*(.003 if q==0 else .0018))),joint='curve')
            axis=math.atan2(tip[0]-origin[0],tip[1]-origin[1])
            for j in range(nodes):
                t=.13+.82*(j/(nodes-1))**.72+rng.uniform(-.018,.018);ax,ay=shoot(t)
                side=-1 if (j+q+k)%2 else 1
                angle=axis+side*rng.uniform(.62,1.65)
                length=rng.uniform(.081,.125);scale=length/species.CARD_SIZE
                petiole=rng.uniform(.013,.028)/species.CARD_SIZE
                base=(ax+math.sin(angle)*petiole,ay+math.cos(angle)*petiole)
                shape,veins=outline(rng);lobes.append(len(veins)+1);width_scale=rng.uniform(.76,.99)
                ca,sa=math.cos(angle),math.sin(angle)
                def transform(x,y):return pt(base[0]+scale*(x*width_scale*ca+y*sa),base[1]+scale*(-x*width_scale*sa+y*ca))
                # Keep the complete blade inside its tile. A clipped distal
                # lobe makes a hard card-edge line, especially in backlight.
                draft=[transform(x,y) for x,y in shape]
                margin=max(8,round(w*.012))
                xlo=min(x for x,y in draft);xhi=max(x for x,y in draft)
                ylo=min(y for x,y in draft);yhi=max(y for x,y in draft)
                shiftx=max(0,margin-xlo)-max(0,xhi-(w-1-margin))
                shifty=max(0,margin-ylo)-max(0,yhi-(h-1-margin))
                base=(base[0]+shiftx/w,base[1]-shifty/h)
                points=[transform(x,y) for x,y in shape]
                draw.line([pt(ax,ay),pt(*base)],fill=(*species.PETIOLE_COLOR,255),width=max(1,round(w*.0018)))
                maskim=Image.new('L',(w,h));md=ImageDraw.Draw(maskim);md.polygon([transform(x,y) for x,y in shape],fill=255)
                if rng.random()<.035:
                    bx,by=transform(-.29,.54);r=max(1,round(scale*w*.04));md.ellipse((bx-r,by-r,bx+r,by+r),fill=0);damaged+=1
                ys,xs=np.nonzero(np.asarray(maskim)>0)
                if not len(xs):continue
                dx=(xs/w-base[0])/scale;dy=(1-ys/h-base[1])/scale
                x=(dx*ca-dy*sa)/width_scale;y=dx*sa+dy*ca
                dist=np.abs(x);vx=x.copy();vy=np.zeros_like(x)
                # Pinnate veins begin along the midrib, then run to lobe tips.
                for endx,endy in veins:
                    starty=max(.06,endy*.58);ex,ey=endx,endy-starty
                    tt=np.clip((x*ex+(y-starty)*ey)/(ex*ex+ey*ey),0,1)
                    ddx=x-tt*ex;ddy=y-starty-tt*ey;dd=np.hypot(ddx,ddy);take=dd<dist
                    vx[take]=ddx[take];vy[take]=ddy[take];dist=np.minimum(dist,dd)
                rib=np.exp(-(dist/.016)**2);fine=np.sin(x*221+y*71)*np.sin(y*287-x*41)
                light=rng.uniform(.82,1.17);older=rng.random()<.045
                c=np.tile(np.array(species.LEAF_COLOR)*light,(len(xs),1))
                c+=rib[:,None]*np.array([14,18,8])+fine[:,None]*1.2
                c+=((y-.5)*2)[:,None]*[2,3,-1]
                if older:c=c*.93+[6,5,1]
                rgba=np.zeros((h,w,4),np.uint8);rgba[ys,xs,:3]=np.clip(c,0,255);rgba[ys,xs,3]=255;tile.alpha_composite(Image.fromarray(rgba))
                # Unequal blade twist and midrib cup; broad smooth cuticle sheen.
                ribgrad=-2*.00014/length/.016**2*rib
                slope_x=1.65*x+ribgrad*vx+rng.uniform(-.52,.52)+.32*np.sin(y*5+k)
                slope_y=.62*(y-.35)+ribgrad*vy+rng.uniform(-.26,.26)
                nx=-(slope_x*ca+slope_y*sa);ny=-(-slope_x*sa+slope_y*ca)
                ns=np.c_[nx,ny,np.ones(len(xs))];ns/=np.linalg.norm(ns,axis=1)[:,None]
                nm[ys,xs]=np.round((ns*.5+.5)*255).astype(np.uint8)
                rm[ys,xs]=np.c_[np.full(len(xs),255),np.clip(98+fine*4+rng.uniform(-12,18)+older*15,0,255),np.zeros(len(xs))].astype(np.uint8)
                count+=1;lengths.append(length*1.015)
        c=np.asarray(tile).copy();alpha=c[:,:,3].copy();occupied=alpha>0
        for _ in range(6):
            fresh=occupied.copy()
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                take=np.roll(occupied,(dy,dx),(0,1)) & ~fresh
                c[take,:3]=np.roll(c,(dy,dx),(0,1))[take,:3];nm[take]=np.roll(nm,(dy,dx),(0,1))[take];rm[take]=np.roll(rm,(dy,dx),(0,1))[take];fresh|=take
            occupied=fresh
        c[:,:,3]=alpha;color[ya:yb,xa:xb]=c;normal[ya:yb,xa:xb]=nm;orm[ya:yb,xa:xb]=rm
        assert not any(np.any(edge) for edge in [alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]]),'Clipped leaf tile'
        variants.append(dict(index=k,shoots=len(axes),leaves=count,blade_min_m=min(lengths),blade_max_m=max(lengths),lobes=sorted(set(lobes)),insect_bites=damaged,alpha_coverage=float((alpha>0).mean())))
    for channel,array in [('BaseColor',color),('Normal',normal),('ORM',orm)]:Image.fromarray(array).save(folder/f'T_{species.ASSET}_{channel}.png')
    (folder/'branchlet-atlas.json').write_text(json.dumps(variants,indent=2))
    return folder/f'T_{species.ASSET}_BaseColor.png'
