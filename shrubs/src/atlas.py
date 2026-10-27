"""Original boxwood shoot tiles, cup/rib normals and stem grain. No photo inputs.

Analytic 4096 RGBA/normal/ORM source fields; kit filters to the proposed 2048
family allocation before look-dev, so these views expose actual tile resolution.
Eight opposed, decussate shoots include new growth and shaded old leaves.
"""
import argparse,math,random,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from kit.image_io import write_png
from settings import CARD_SIZE,LEAF_LENGTH,LEAF_COLOR,LEAF_RECTS


def generate(folder,size=4096):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    color=np.full((size,size,4),(*LEAF_COLOR,0),np.uint8)
    normal=np.full((size,size,3),(128,128,255),np.uint8)
    orm=np.full((size,size,3),(255,112,0),np.uint8)
    records=[]
    for k,(u0,v0,u1,v1) in enumerate(LEAF_RECTS):
        rng=random.Random(890+k)
        xa,xb=round(u0*size),round(u1*size);ya,yb=round((1-v1)*size),round((1-v0)*size)
        w,h=xb-xa,yb-ya;tile=Image.new('RGBA',(w,h),(*LEAF_COLOR,0));draw=ImageDraw.Draw(tile)
        nm=normal[ya:yb,xa:xb].copy();rm=orm[ya:yb,xa:xb].copy()
        def pixel(x,y):return (round(x*w),round((1-y)*h))
        new=k==6;aged=k==7;lengths=[]
        # Each plane holds six short 6–10-leaf sprigs, not one flat spray.
        axes=[((.23,.06),(.15,.42),rng.randrange(3,6)),
              ((.48,.12),(.45,.51),rng.randrange(3,6)),
              ((.75,.14),(.87,.52),rng.randrange(3,6)),
              ((.21,.51),(.15,.89),rng.randrange(3,6)),
              ((.49,.52),(.54,.94),rng.randrange(3,6)),
              ((.74,.52),(.84,.91),rng.randrange(3,6))]
        if new:axes=[((.48,.10),(.50,.91),5)]
        for base,tip,count in axes:
            draw.line([pixel(*base),pixel(*tip)],fill=(88,78,40,255) if not new else (81,101,42,255),width=max(2,round(w*.006)))
            axis=math.atan2(tip[0]-base[0],tip[1]-base[1])
            for node in range(count):
                t=.18+node*.74/(count-1)+rng.uniform(-.045,.045)
                ax=base[0]+(tip[0]-base[0])*t;ay=base[1]+(tip[1]-base[1])*t
                for side in (-1,1):
                    angle=axis+side*rng.uniform(.72,1.40)
                    length=rng.uniform(*LEAF_LENGTH);scale=length/CARD_SIZE*rng.uniform(.66,1.0)
                    # Alternating pairs turn partly out of the shoot plane.
                    width=rng.uniform(.43,1.02)*( .70 if node%2 else 1)
                    ca,sa=math.cos(angle),math.sin(angle)
                    bx=ax+math.sin(angle)*.010;by=ay+math.cos(angle)*.010
                    def tr(x,y):return pixel(bx+scale*(x*width*ca+y*sa),by+scale*(-x*width*sa+y*ca))
                    outline=[]
                    for i in range(49):
                        a=i/48*math.tau;y=(1-math.cos(a))/2
                        x=.30*math.sin(a)*(.81+.25*y)
                        # A blunt/occasionally shallow-notched tip, entire margin.
                        y-=.018*math.exp(-(x/.06)**2)*max(0,(y-.8)/.2)
                        outline.append(tr(x,y))
                    maskim=Image.new('L',(w,h));ImageDraw.Draw(maskim).polygon(outline,fill=255)
                    mask=np.asarray(maskim)>0;ys,xs=np.nonzero(mask)
                    if not len(xs):continue
                    dx=(xs/w-bx)/scale;dy=(1-ys/h-by)/scale
                    x=(dx*ca-dy*sa)/width;y=dx*sa+dy*ca
                    rib=np.exp(-(x/.016)**2);veins=np.exp(-((np.mod(y-np.abs(x)*.64,.18)-.09)/.014)**2)
                    # Color changes between blades, never baked directional light.
                    col=np.array(LEAF_COLOR,float)*rng.uniform(.82,1.15)
                    if new:col=col*.98+np.array([10,15,1])
                    if aged:col=np.array([64,56,26]) if rng.random()<.38 else col*.76+np.array([11,4,0])
                    fine=np.sin(x*210+y*27)*np.sin(y*221-x*19)
                    rgb=col[None,:]+rib[:,None]*np.array([3,5,1])+fine[:,None]*.7
                    rgba=np.zeros((h,w,4),np.uint8);rgba[ys,xs,:3]=np.clip(rgb,0,255);rgba[ys,xs,3]=255
                    tile.alpha_composite(Image.fromarray(rgba))
                    tilt_x=rng.uniform(-.9,.9);tilt_y=rng.uniform(-.65,.65)
                    sx=.95*x-.12*np.sign(x)*rib+tilt_x
                    sy=.37*(y-.45)+.025*veins+tilt_y
                    nx=-(sx*ca+sy*sa);ny=-(-sx*sa+sy*ca)
                    ns=np.c_[nx,ny,np.ones(len(xs))];ns/=np.linalg.norm(ns,axis=1)[:,None]
                    nm[ys,xs]=np.round((ns*.5+.5)*255).astype(np.uint8)
                    rm[ys,xs]=np.c_[np.full(len(xs),255),np.full(len(xs),rng.randrange(58,88) if not aged else 153),np.zeros(len(xs))]
                    lengths.append(length)
        c=np.asarray(tile).copy();alpha=c[:,:,3].copy();occupied=alpha>0
        for _ in range(8):
            fresh=occupied.copy()
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                take=np.roll(occupied,(dy,dx),(0,1)) & ~fresh
                c[take,:3]=np.roll(c,(dy,dx),(0,1))[take,:3];nm[take]=np.roll(nm,(dy,dx),(0,1))[take];rm[take]=np.roll(rm,(dy,dx),(0,1))[take];fresh|=take
            occupied=fresh
        c[:,:,3]=alpha;color[ya:yb,xa:xb]=c;normal[ya:yb,xa:xb]=nm;orm[ya:yb,xa:xb]=rm
        records.append(dict(tile=k,sprig_leaf_counts=[2*n for _,_,n in axes],leaves=len(lengths),blade_min_m=min(lengths),blade_max_m=max(lengths),new_growth=new,shaded_old=aged))
    # Original longitudinal fine bark field in an opaque strip; soil uses its
    # darkest corner. No source image other than these equations is accepted.
    y,x=np.mgrid[:size//2,:size//4];u=x/size*4;v=y/size*2
    grain=np.sin(u*132+np.sin(v*23)*1.3)+.4*np.sin(u*321+v*18)
    crack=np.maximum(0,np.cos(u*81+np.sin(v*7)*.7))**22
    c=np.zeros((*u.shape,4),np.uint8);c[:,:,:3]=np.clip(np.array([71,58,43])+grain[:,:,None]*3-crack[:,:,None]*13,0,255);c[:,:,3]=255
    color[:size//2,:size//4]=c;orm[:size//2,:size//4]=(245,215,0)
    normal[:size//2,:size//4,0]=np.clip(128+np.cos(u*132+np.sin(v*23)*1.3)*22,0,255)
    # Small root-entry soil patch: granular organic soil with sparse angular
    # mulch fragments. Physical field is generated independently of references.
    rng=np.random.default_rng(998)
    sh=round(size*.06);sw=size//4;yy,xx=np.mgrid[:sh,:sw]
    grain=rng.random((sh,sw));coarse=np.sin(xx*.13+np.sin(yy*.07))*np.cos(yy*.17-xx*.035)
    soil=np.clip(np.array([35,26,18])+grain[:,:,None]*8+coarse[:,:,None]*3,0,255).astype(np.uint8)
    color[size//2-sh:size//2,:sw,:3]=soil;color[size//2-sh:size//2,:sw,3]=255
    orm[size//2-sh:size//2,:sw]=(220,243,0)
    normal[size//2-sh:size//2,:sw,0]=np.clip(128+(grain-.5)*10,0,255)
    normal[size//2-sh:size//2,:sw,1]=np.clip(128+(rng.random((sh,sw))-.5)*10,0,255)
    from hydrangea_atlas import paint,branchlet_tile
    hydrangea=paint(color,normal,orm,size)
    hydrangea[1]=branchlet_tile(color,normal,orm,size)
    for channel,array in [('BaseColor',color),('Normal',normal),('ORM',orm)]:write_png(folder/f'T_Shrubs_{channel}.png',array.astype(np.float32)/255,bits=16 if channel=='Normal' else 8)
    (folder/'atlas.json').write_text(json.dumps(dict(source_size=size,boxwood=records,hydrangea=hydrangea),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--size',type=int,default=4096);a=p.parse_args();generate(a.out,a.size)
