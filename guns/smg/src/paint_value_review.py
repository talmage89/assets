"""Visible-surface medians, independent of hand-picked shaded flat strips."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageFilter,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from finish_review import camera
from kit.photo_match import project
from kit.fonts import find_font
LUMA=np.array((.2126,.7152,.0722))

def masks(meta,width,height):
    data=np.load(BASE/'build/value-surfaces.npz');tri=data['triangles'];uv=data['uvs'];parts=data['parts'];names=data['names'].tolist()
    xy,depth,_=project(camera(meta),tri.reshape(-1,3),width,height);xy=xy.reshape(-1,3,2);depth=depth.reshape(-1,3)
    zbuffer=np.full((height,width),np.inf);owner=np.full((height,width),-1,np.int32)
    position=np.zeros((height,width,3));texcoord=np.zeros((height,width,2))
    for i,(points,z) in enumerate(zip(xy,depth)):
        if z.min()<=0:continue
        lo=np.maximum(0,np.floor(points.min(0)).astype(int));hi=np.minimum((width,height),np.ceil(points.max(0)).astype(int))
        if np.any(hi<=lo):continue
        (ax,ay),(bx,by),(cx,cy)=points;den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-9:continue
        yy,xx=np.mgrid[lo[1]:hi[1],lo[0]:hi[0]];xx=xx+.5;yy=yy+.5
        a=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den;b=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den;c=1-a-b
        weights=np.stack((a/z[0],b/z[1],c/z[2]),axis=-1);d=1/np.maximum(weights.sum(-1),1e-12)
        sl=np.s_[lo[1]:hi[1],lo[0]:hi[0]];keep=(a>=0)&(b>=0)&(c>=0)&(d<zbuffer[sl])
        if not keep.any():continue
        weights*=d[:,:,None];zbuffer[sl][keep]=d[keep];owner[sl][keep]=parts[i]
        position[sl][keep]=(weights@tri[i])[keep];texcoord[sl][keep]=(weights@uv[i])[keep]
    bc=np.asarray(Image.open(BASE/'textures/T_Relay9_BaseColor.png').convert('RGBA'))
    tx=np.clip((texcoord[:,:,0]*bc.shape[1]).astype(int),0,bc.shape[1]-1);ty=np.clip(((1-texcoord[:,:,1])*bc.shape[0]).astype(int),0,bc.shape[0]-1)
    # Paint-only reflection factor in opaque alpha; exposed substrate retains .56.
    intact=bc[ty,tx,3]>190
    regions=dict(paint_upper_flank=(owner==names.index('Receiver_Shell'))&(position[:,:,2]>.112)&intact,
                 stock=owner==names.index('Stock_Mold'),
                 grip=np.isin(owner,[i for i,name in enumerate(names) if name=='Lower_Mold' or name.startswith('Grip_TexturePanel')])&(position[:,:,2]<.025)&(position[:,:,1]<.040))
    return {name:np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>0 for name,mask in regions.items()}

def build(beauty=None,out=None):
    beauty=Path(beauty) if beauty else BASE/'renders/final/beauty';out=Path(out) if out else BASE/'renders/final'
    meta=json.loads((beauty/'shots.json').read_text())['hero'];im=Image.open(beauty/'hero.png').convert('RGB');rgb=np.asarray(im);lum=rgb@LUMA
    regions=masks(meta,im.width,im.height);result=dict(method='Perspective-correct triangle z-buffer of finalized surfaces; same accepted delivery triangles. Upper receiver above Z112 mm excludes exposed chips by actual BC texels; entire stock mold; grip lower mold plus texture panels below Z25 mm and behind Y40 mm. Each mask eroded one pixel. Display luma 0–255.',regions={})
    background=Image.new('RGBA',im.size,(108,111,114,255));background.alpha_composite(Image.open(beauty/'hero.png').convert('RGBA'))
    overlay=np.array(background.convert('RGB'))
    for (name,mask),color in zip(regions.items(),((220,120,30),(50,180,220),(90,210,80))):
        assert mask.any(),name
        result['regions'][name]=dict(pixels=int(mask.sum()),median_luma_255=float(np.median(lum[mask])),p10_p90=np.percentile(lum[mask],(10,90)).tolist())
        overlay[mask]=np.rint(rgb[mask]*.65+np.array(color)*.35).astype('uint8')
    marked=Image.fromarray(overlay);draw=ImageDraw.Draw(marked);font=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
    draw.text((16,16),'Visible-region medians / orange: intact upper paint / cyan: stock / green: grip including texture panels',font=font,fill='white')
    draw.text((16,42),' / '.join(f"{name}: {row['median_luma_255']:.2f}" for name,row in result['regions'].items()),font=font,fill='white')
    out.mkdir(parents=True,exist_ok=True);marked.save(out/'paint-value-regions.jpg',quality=95)
    (out/'paint-value-values.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--beauty');p.add_argument('--out');a=p.parse_args();print(json.dumps(build(a.beauty,a.out),indent=2))
