"""Original botanical branchlet atlas: analytic lobes, teeth, venation and cups.

No photograph is read. Eight seeded arrangements share the same species controls;
the upper half of the family atlas is reserved for unique baked bark islands.
"""
from pathlib import Path
import json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from species import MAPLE,get


def outline(rng, five=False, species=MAPLE):
    # Broad, shallow sinuses distinguish rubrum from deeply cut silver maple.
    side=list(species.LEAF_PROFILE_5 if five else species.LEAF_PROFILE_3)
    major=side+[(-x,y) for x,y in side[-2:0:-1]]
    if species.PLACEHOLDER:return major
    teeth=[]
    for a,b in zip(major,major[1:]+major[:1]):
        a=np.array(a);b=np.array(b);delta=b-a;length=np.linalg.norm(delta)
        count=max(1,round(length/.065));normal=np.array([-delta[1],delta[0]])/length
        for j in range(count):
            p=a+delta*j/count;teeth.append(tuple(p))
            if p[1]>.10:
                p=a+delta*(j+.48)/count+normal*rng.uniform(.008,.021)
                teeth.append(tuple(p))
    return teeth


def generate(folder, size=4096, species=MAPLE):
    if species.ARCHITECTURE=="excurrent":
        from oak_leaves import generate as oak_generate
        return oak_generate(folder,size,species)
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    color=np.empty((size,size,4),np.uint8);color[:]=(*species.LEAF_COLOR,0)
    normal=np.empty((size,size,3),np.uint8);normal[:]=(128,128,255)
    orm=np.empty((size,size,3),np.uint8);orm[:]=(255,170,0)
    variants=[]
    for k,rect in enumerate(species.LEAF_RECTS):
        rng=random.Random(100+k);u0,v0,u1,v1=rect
        xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size)
        w,h=xb-xa,yb-ya
        tile=Image.new('RGBA',(w,h),(*species.LEAF_COLOR,0));draw=ImageDraw.Draw(tile)
        nm=np.full((h,w,3),(128,128,255),np.uint8);rm=np.full((h,w,3),(255,170,0),np.uint8)
        def pt(x,y):return (round(x*w),round((1-y)*h))
        axes=[((.48,.045),(.15+rng.uniform(-.04,.04),.76)),
              ((.48,.045),(.83+rng.uniform(-.03,.03),.76)),
              ((.48,.045),(.49+rng.uniform(-.07,.07),.96))]
        count=0;lengths=[];damaged=0;old_count=0
        for origin,tip in axes:
            mid=((origin[0]+tip[0])*.5+rng.uniform(-.025,.025),(origin[1]+tip[1])*.5)
            draw.line([pt(*origin),pt(*mid),pt(*tip)],fill=(*species.TWIG_COLOR,255),width=max(2,round(w*.0030)),joint='curve')
            angle_axis=math.atan2(tip[0]-origin[0],tip[1]-origin[1])
            nodes=species.LEAF_NODES[k%2]
            for node in range(nodes):
                t=.20+node*(.65/(nodes-1))+rng.uniform(-.025,.025)
                ax=origin[0]+(tip[0]-origin[0])*t;ay=origin[1]+(tip[1]-origin[1])*t
                for side in ((-1 if node%2 else 1,) if species.LEAF_ALTERNATE else (-1,1)):
                    angle=angle_axis+side*rng.uniform(.65,1.40)
                    length=rng.uniform(*species.LEAF_LENGTH);scale=length/species.CARD_SIZE
                    petiole=rng.uniform(.023,.042)/species.CARD_SIZE
                    base=(ax+math.sin(angle)*petiole,ay+math.cos(angle)*petiole)
                    draw.line([pt(ax,ay),pt(*base)],fill=(*species.PETIOLE_COLOR,255),width=max(1,round(w*.0025)))
                    shape=outline(rng,five=rng.random()<.24,species=species)
                    width_scale=rng.uniform(.72,1.06)
                    ca,sa=math.cos(angle),math.sin(angle)
                    def transform(x,y):return pt(base[0]+scale*(x*width_scale*ca+y*sa),base[1]+scale*(-x*width_scale*sa+y*ca))
                    points=[transform(x,y) for x,y in shape]
                    maskim=Image.new('L',(w,h));md=ImageDraw.Draw(maskim);md.polygon(points,fill=255)
                    # Sparse bites are at an exposed margin; no uniform damage wash.
                    if rng.random()<.045:
                        bx,by=transform(-.40,.45);r=max(1,round(scale*w*.055));md.ellipse((bx-r,by-r,bx+r,by+r),fill=0);damaged+=1
                    mask=np.asarray(maskim)>0
                    ys,xs=np.nonzero(mask)
                    if not len(xs):continue
                    dx=(xs/w-base[0])/scale;dy=(1-ys/h-base[1])/scale
                    x=(dx*ca-dy*sa)/width_scale;y=dx*sa+dy*ca
                    # Palmately branching veins: distance to five true vein axes.
                    dist=np.full(len(xs),10.);vein_dx=np.zeros(len(xs));vein_dy=np.zeros(len(xs))
                    for vx,vy in [(0,.96),(-.50,.63),(.50,.63),(-.40,.27),(.40,.27)]:
                        tt=np.clip((x*vx+y*vy)/(vx*vx+vy*vy),0,1)
                        ddx=x-tt*vx;ddy=y-tt*vy;candidate=np.hypot(ddx,ddy);near=candidate<dist
                        vein_dx[near]=ddx[near];vein_dy[near]=ddy[near];dist=np.minimum(dist,candidate)
                    rib=np.exp(-(dist/.010)**2)
                    fine=.5+.5*np.sin(x*177+y*31)*np.sin(y*219-x*29)
                    light=rng.uniform(.84,1.12);older=rng.random()<.035;old_count+=older
                    basecol=np.array(species.LEAF_COLOR,dtype=float)*(light*(1+.025*(fine-.5)))[:,None]
                    c=np.broadcast_to(basecol,(len(xs),3)).copy()
                    c+=rib[:,None]*np.array([7,9,3]);c+=((y-.5)*2)[:,None]*np.array([2,3,0])
                    if older:c=c*.90+np.array([12,14,7])
                    rgba=np.zeros((h,w,4),np.uint8);rgba[ys,xs,:3]=np.clip(c,0,255);rgba[ys,xs,3]=255
                    layer=Image.fromarray(rgba);tile.alpha_composite(layer)
                    # Curved blade and raised ribs, expressed in the card tangent frame.
                    rib_gradient=-2*.00007/length/.010**2*rib
                    tilt_x=rng.uniform(-.20,.20);tilt_y=rng.uniform(-.16,.16)
                    slope_x=.23*x+rib_gradient*vein_dx+tilt_x
                    slope_y=.10*(y-.35)+rib_gradient*vein_dy+tilt_y
                    nx=-(slope_x*ca+slope_y*sa);ny=-(-slope_x*sa+slope_y*ca)
                    normals=np.c_[nx,ny,np.ones(len(xs))];normals/=np.linalg.norm(normals,axis=1)[:,None]
                    nm[ys,xs]=np.round((normals*.5+.5)*255).astype(np.uint8)
                    rm[ys,xs]=np.c_[np.full(len(xs),255),np.clip(163+fine*10+older*13,0,255),np.zeros(len(xs))].astype(np.uint8)
                    count+=1;lengths.append(length)
        c=np.asarray(tile).copy();alpha=c[:,:,3].copy()
        # Six source pixels of color dilation prevent dark alpha fringes in mips.
        occupied=alpha>0
        for _ in range(6):
            fresh=occupied.copy()
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                shifted=np.roll(occupied,(dy,dx),(0,1));take=shifted & ~fresh
                c[take,:3]=np.roll(c,(dy,dx),(0,1))[take,:3]
                nm[take]=np.roll(nm,(dy,dx),(0,1))[take]
                fresh|=take
            occupied=fresh
        c[:,:,3]=alpha;color[ya:yb,xa:xb]=c;normal[ya:yb,xa:xb]=nm;orm[ya:yb,xa:xb]=rm
        variants.append(dict(index=k,leaves=count,blade_min_m=min(lengths),blade_max_m=max(lengths),insect_bites=damaged,older_leaves=old_count))
    if species.PLACEHOLDER:
        normal[:]=(128,128,255);orm[:]=(255,180,0)
    for channel,array in [('BaseColor',color),('Normal',normal),('ORM',orm)]:Image.fromarray(array).save(folder/f'T_{species.ASSET}_{channel}.png')
    (folder/'branchlet-atlas.json').write_text(json.dumps(variants,indent=2))
    return folder/f'T_{species.ASSET}_BaseColor.png'


def apply(folder,source,species=MAPLE):
    """Composite analytic leaf tiles into the 4K bark bake before kit filtering."""
    folder=Path(folder);source=Path(source)
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
    from kit.image_io import read_png,write_png
    for channel in ('BaseColor','Normal','ORM'):
        target=folder/f'T_{species.ASSET}_{channel}.png';array=read_png(target)
        if channel=='BaseColor':array=np.dstack([array[:,:,:3],np.ones(array.shape[:2],np.float32)])
        leaf=np.asarray(Image.open(source/target.name).convert('RGBA' if channel=='BaseColor' else 'RGB'),dtype=np.float32)/255
        array[array.shape[0]//2:]=leaf[leaf.shape[0]//2:]
        write_png(target,array,bits=16 if channel=='Normal' else 8)



if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--species',choices=('maple','oak'),default='maple');p.add_argument('--out',type=Path,required=True);p.add_argument('--size',type=int,default=4096);p.add_argument('--composite',type=Path)
    a=p.parse_args();species=get(a.species);apply(a.out,a.composite,species=species) if a.composite else generate(a.out,a.size,species=species)
