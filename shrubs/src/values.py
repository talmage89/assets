"""Spatially matched foliage measurements; include gray-green leaf highlights.

Display-image evidence only. A brightness population cannot identify actual
illumination, so lit/front patches and their brighter half are both reported.
These deliberately replace the previous strict saturated-green whole-crown mask.
"""
from pathlib import Path
import sys,json,colorsys,argparse
import numpy as np
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font

BOX_PATCHES={
 'match_green_velvet':dict(lit=(375,215,740,380),shade=(345,445,730,535)),
 'match_clipped':dict(lit=(280,120,555,250),shade=(265,290,570,365)),
}


def stats(im,kind='leaf'):
    a=np.asarray(im.convert('RGBA'),float)/255;r,g,b,alpha=np.moveaxis(a,-1,0)
    if kind=='leaf':mask=(g>r*1.015)&(g>b*1.025)&(alpha>.90)
    else:mask=(b>g*1.045)&(b>r*.95)&(alpha>.90)
    rgb=a[:,:,:3][mask]
    if len(rgb)<20:return dict(pixels=len(rgb),insufficient=True)
    y=rgb@np.array([.2126,.7152,.0722]);hsv=np.array([colorsys.rgb_to_hsv(*p) for p in rgb])
    bright=y>=np.median(y)
    return dict(pixels=len(y),median_display_Y=float(np.median(y)),p5_p50_p95=np.percentile(y,[5,50,95]).tolist(),brighter_half_median_Y=float(np.median(y[bright])),median_RGB=np.median(rgb,axis=0).tolist(),hue_deg=float(np.median(hsv[:,0])*360),saturation=float(np.median(hsv[:,1])),brighter_half_saturation=float(np.median(hsv[bright,1])),clipped_fraction=float(np.mean(np.any(rgb>=1,axis=1))))


def measure(renders,calibration,patches):
    renders=Path(renders);cal=json.loads(Path(calibration).read_text());out={};annot=[]
    for name,regions in patches.items():
        row=cal[name];photo=Image.open(row['photo']).convert('RGBA').crop(row['crop']);model=Image.open(renders/(name+'.png')).convert('RGBA').resize(photo.size,Image.Resampling.LANCZOS)
        # Original photo coordinates -> framed canvas coordinates. Framer adds
        # symmetric margins, preserving the original pinhole pixel projection.
        raw=regions['crop'];mx=(photo.width-(raw[2]-raw[0]))//2;my=(photo.height-(raw[3]-raw[1]))//2
        results={};pdraw=ImageDraw.Draw(photo);mdraw=ImageDraw.Draw(model)
        for label,rect in regions.items():
            if label=='crop':continue
            rr=tuple(round(v-raw[k%2]+(mx if k%2==0 else my)) for k,v in enumerate(rect))
            kind='flower' if label.startswith('flower') else 'leaf'
            results[label]=dict(photo_patch_original_pixels=rect,model=stats(model.crop(rr),kind),photo=stats(photo.crop(rr),kind))
            for d in (pdraw,mdraw):d.rectangle(rr,outline=(255,200,30),width=2);d.text((rr[0]+2,rr[1]+2),label,fill=(255,200,30))
        pair=Image.new('RGBA',(photo.width*2,photo.height),(238,239,236,255));pair.alpha_composite(model,(0,0));pair.alpha_composite(photo,(photo.width,0));pair.convert('RGB').save(renders/(name+'-value-patches.jpg'),quality=93)
        out[name]=results
    (renders/'measured-values.json').write_text(json.dumps(dict(scope='matched display-image patches, different lighting/specimens; brighter-half is a population proxy, not illumination or reflectance',results=out),indent=2))
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);p.add_argument('--calibration',type=Path,default=Path('build/framed-cameras.json'));a=p.parse_args()
    from photo_matches import MATCHES
    patches={k:dict(crop=MATCHES[k]['crop'],**v) for k,v in BOX_PATCHES.items()}
    measure(a.renders,a.calibration,patches)
