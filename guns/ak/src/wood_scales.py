"""Comparison-only physical-scale wood analysis. Never used by lookdev/bake.

Both views are sampled on a 0.5 mm Y/Z grid. Broad = normalized Gaussian
convolution, FWHM 10 mm (sigma 4.247 mm); fine = original value minus broad.
Spreads use (p90-p10)/the original median HSV value for all three signals.
This measures photographed/rendered appearance, including broad lighting.
"""
from pathlib import Path
import argparse,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,projection,bilinear
from look_review import REGIONS,polygon_mask,masked
from furniture_review import FLAT_WORLD,FLAT_PHOTO
from wear_sites import homography
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),19)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
PITCH=.5
PARTS=('stock','lower_handguard','upper_handguard','stock_flat_side')

def convolve(a,k):
    r=len(k)//2
    for axis in (0,1):
        padding=[(0,0)]*2;padding[axis]=(r,r)
        a=np.apply_along_axis(lambda row:np.convolve(row,k,mode='valid'),axis,np.pad(a,padding))
    return a

def signals(rgb,mask):
    value=rgb.max(axis=2)
    sigma=10/(2*np.sqrt(2*np.log(2)))/PITCH
    xx=np.arange(-int(np.ceil(sigma*3)),int(np.ceil(sigma*3))+1)
    k=np.exp(-.5*(xx/sigma)**2);k/=k.sum()
    broad=convolve(value*mask,k)/np.maximum(convolve(mask.astype(float),k),1e-9)
    fine=value-broad
    median=float(np.median(value[mask]));row={'pixels':int(mask.sum()),'median_value':median}
    for key,signal in [('total',value),('broad',broad),('fine',fine)]:
        q=np.percentile(signal[mask],[10,50,90]);row[key]=dict(p10_p50_p90=q.tolist(),spread=float((q[2]-q[0])/median))
    return row,broad,fine

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',default='renders/final/photos');p.add_argument('--out',default='renders/final/look-review')
    p.add_argument('--shot',default='used_photo');p.add_argument('--parts',default=','.join(PARTS));a=p.parse_args()
    folder=BASE/a.renders;out=BASE/a.out;out.mkdir(parents=True,exist_ok=True)
    meta=json.loads((folder/'shots.json').read_text())[a.shot]
    image=np.asarray(Image.open(folder/(a.shot+'.png')).convert('RGB')).astype(float);h,w=image.shape[:2]
    geo=np.load(BASE/'build/value-geometry.npz');ids,_=raster(geo,meta,w,h)
    photo=np.asarray(Image.open(BASE/'build/white-balanced/early.jpg').convert('RGB')).astype(float)
    H=homography([[-.035,.086],[-.035,.050],[.220,.086],[.220,.050]],[[612,246],[612,352],[1270,228],[1270,323]])
    rows={};tiles=[]
    for name in a.parts.split(','):
        role='stock' if name=='stock_flat_side' else name
        _,polys,_,prefix=REGIONS[role]
        selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefix)]
        if name=='stock_flat_side':polys=[FLAT_PHOTO];world=np.array(FLAT_WORLD)[:,1:]
        else:world=geo['xyz'][np.isin(geo['ids'],selected)].reshape(-1,3)[:,1:]
        pp=np.array([p for poly in polys for p in poly]);qq=np.c_[pp,np.ones(len(pp))]@np.linalg.inv(H).T
        world=np.r_[world,qq[:,:2]/qq[:,2:]]
        y0,z0=world.min(axis=0)-.002;y1,z1=world.max(axis=0)+.002
        yy,zz=np.meshgrid(np.arange(y0,y1,PITCH*.001),np.arange(z0,z1,PITCH*.001))
        points=np.stack([np.full_like(yy,.0175),yy,zz],axis=2).reshape(-1,3)
        xy,_=projection(points,meta,w,h)
        ii=np.clip(xy[:,0].astype(int),0,w-1);jj=np.clip(xy[:,1].astype(int),0,h-1)
        valid=np.isin(ids[jj,ii],selected).reshape(yy.shape)
        if name=='stock_flat_side':
            corners,_=projection(np.array(FLAT_WORLD),meta,w,h)
            valid &= bilinear(polygon_mask((w,h),[corners.tolist()]).astype(float),xy).reshape(yy.shape)>.99
            polys=[FLAT_PHOTO]
        q=np.stack([yy.ravel(),zz.ravel(),np.ones(yy.size)],axis=1)@H.T;q=q[:,:2]/q[:,2:]
        pm=polygon_mask((photo.shape[1],photo.shape[0]),polys)
        pv=bilinear(pm.astype(float),q).reshape(yy.shape)>.99
        observed=bilinear(image,xy).reshape(*yy.shape,3);ref=bilinear(photo,q).reshape(*yy.shape,3)
        row={};tile=Image.new('RGB',(1800,640),'#ebede9');d=ImageDraw.Draw(tile)
        d.text((20,8),name+' / physical-scale value structure: FWHM 10 mm Gaussian; 0.5 mm grid',font=FONT,fill='black')
        for index,(rgb,m,key) in enumerate([(observed,valid,'render'),(ref,pv,'photo')]):
            result,broad,fine=signals(rgb,m);row[key]=result;x=20+index*900
            for j,(arr,title) in enumerate([(rgb,'Original'),(np.repeat(broad[:,:,None],3,axis=2),'Broad'),(np.repeat((128+fine*3)[:,:,None],3,axis=2),'Fine residual x3 +128')]):
                arr=np.flipud(np.clip(arr,0,255));mm=np.flipud(m)
                pic=masked(arr,mm,(855,132));tile.paste(pic,(x,65+j*160));d.text((x,44+j*160),key+' / '+title,font=SMALL,fill='black')
            d.text((x,552),'Total / broad / fine: '+ ' / '.join(f"{result[k]['spread']:.3f}" for k in ('total','broad','fine')),font=FONT,fill='black')
        row['bounds_yz_m']=[y0,y1,z0,z1];rows[name]=row;tiles.append(tile)
        print(name,{k:{s:round(row[k][s]['spread'],4) for s in ('total','broad','fine')} for k in ('render','photo')},flush=True)
    report=dict(method=__doc__,pitch_mm=PITCH,blur_fwhm_mm=10,blur_sigma_mm=10/(2*np.sqrt(2*np.log(2))),rows=rows,
                render_sha256=meta['sha256'],photo_neutral=json.loads((BASE/'build/white-balanced/corrections.json').read_text())['early.jpg'],
                limits='Side-plane rectification at X17.5 mm; photo scale uses independently observed receiver corners and 255 mm span. Part depth, mixed light, original contours and diffuse/specular shading differ. Normalized masked convolution excludes backdrop; no exposure fitting or morphology filtering.')
    (out/'wood-two-scale-values.json').write_text(json.dumps(report,indent=2))
    canvas=Image.new('RGB',(1800,640*len(tiles)),'#ebede9')
    for i,t in enumerate(tiles):canvas.paste(t,(0,i*640))
    canvas.save(out/'wood-two-scale.jpg',quality=95)
if __name__=='__main__':main()
