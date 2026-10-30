"""Visible 2D wear proof from site-off baked exports and native photographs.

No shader mask decides acceptance. Actual same-camera exported-image changes
define the rendered mask. Report threshold sensitivity, full-frame visibility,
both 2D profiles and connected worn AND remaining-finish regions. Photographic
annotations stay review-only. Geometry/UV/clip equality is independently proved
by wear_variants.py before rendering.
"""
import argparse,hashlib,json,math,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from wear_reference import SITES
from look_matches import PHOTOS
from look_review import native_mask,panel,LUMA
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)

def poly_mask(polys,size):
    im=Image.new('L',size);d=ImageDraw.Draw(im)
    for p in polys:d.polygon(p,fill=255)
    return np.asarray(im)>0

def bbox(mask,pad=0):
    yy,xx=np.nonzero(mask)
    assert len(xx),'Empty physical part'
    return (max(0,int(xx.min())-pad),max(0,int(yy.min())-pad),
            min(mask.shape[1],int(xx.max())+1+pad),min(mask.shape[0],int(yy.max())+1+pad))

def components(mask,part):
    """8-connected pixel area and bounding size; include remaining islands."""
    h,w=mask.shape;seen=np.zeros(mask.shape,bool);records=[]
    for sy,sx in zip(*np.nonzero(mask)):
        if seen[sy,sx]:continue
        seen[sy,sx]=True;stack=[(sy,sx)];n=0;x0=x1=int(sx);y0=y1=int(sy);boundary=False
        while stack:
            y,x=stack.pop();n+=1;x0=min(x0,x);x1=max(x1,x);y0=min(y0,y);y1=max(y1,y)
            for dy,dx in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
                qy,qx=y+dy,x+dx
                if not (0<=qy<h and 0<=qx<w) or not part[qy,qx]:boundary=True;continue
                if mask[qy,qx] and not seen[qy,qx]:seen[qy,qx]=True;stack.append((qy,qx))
        records.append(dict(pixels=n,fraction_of_part=n/max(1,int(part.sum())),
                            width_px=int(x1-x0+1),height_px=int(y1-y0+1),touches_part_boundary=bool(boundary)))
    records.sort(key=lambda r:r['pixels'],reverse=True)
    return dict(count=len(records),largest=records[:20],
                interior_islands=sum(not r['touches_part_boundary'] for r in records))

def profile(mask,part,axis,bins=24,angle=0):
    yy,xx=np.nonzero(part);c,s=math.cos(angle),math.sin(angle)
    coordinate=(c*xx+s*yy) if axis==1 else (-s*xx+c*yy)
    lo,hi=coordinate.min(),coordinate.max()+1e-8
    ids=np.minimum(bins-1,((coordinate-lo)/(hi-lo)*bins).astype(int))
    total=np.bincount(ids,minlength=bins);worn=np.bincount(ids,weights=mask[yy,xx],minlength=bins)
    return [float(worn[i]/total[i]) if total[i] else None for i in range(bins)]

def projected_axis(shot,width):
    # Project two rigid points along +Y, independent of either wear mask.
    location=np.array(shot['location']);forward=np.array(shot['target'])-location;forward/=np.linalg.norm(forward)
    right=np.cross(forward,(0,0,1));right/=np.linalg.norm(right);up=np.cross(right,forward)
    points=np.array(((0,-.15,.044),(0,.65,.044)))-location
    q=np.column_stack((points@right,-points@up))/(points@forward)[:,None]
    return float(math.atan2(*(q[1]-q[0])[::-1]))

def evidence(mask,part,angle=0):
    # Preserve fractions in native pixels. Connectivity is measured at the
    # report's declared common 800-px part-width raster, with no 1D inference.
    x0,y0,x1,y1=bbox(part);scale=min(1,800/max(x1-x0,y1-y0))
    size=(max(1,round((x1-x0)*scale)),max(1,round((y1-y0)*scale)))
    p=np.asarray(Image.fromarray(np.uint8(part[y0:y1,x0:x1])*255).resize(size,Image.Resampling.NEAREST))>0
    m=np.asarray(Image.fromarray(np.uint8(mask[y0:y1,x0:x1])*255).resize(size,Image.Resampling.NEAREST))>0
    return dict(fraction=float(mask.sum()/part.sum()),worn_pixels=int(mask.sum()),part_pixels=int(part.sum()),
                along_length=profile(mask,part,1,angle=angle),across_height=profile(mask,part,0,angle=angle),
                connectivity_raster_size=size,worn_regions=components(m,p),remaining_finish=components(p&~m,p))

def graph(draw,box,ours,photo,title):
    x,y,w,h=box;draw.text((x,y),title+' (ours orange / photo blue)',font=SMALL,fill='black');y+=25;h-=25
    draw.rectangle((x,y,x+w,y+h),outline=(140,140,140))
    for vals,color in ((ours,(190,87,26)),(photo,(30,105,170))):
        points=[(x+(i+.5)*w/len(vals),y+h*(1-v)) for i,v in enumerate(vals) if v is not None]
        if len(points)>1:draw.line(points,fill=color,width=3)

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48)
    p.add_argument('--folder',type=Path,default=BASE/'renders/final');p.add_argument('--no-render',action='store_true');a=p.parse_args()
    out=a.folder/'wear';out.mkdir(parents=True,exist_ok=True)
    variants=json.loads((BASE/'build/wear/variants.json').read_text())
    main_meta=json.loads((a.folder/'beauty/shots.json').read_text())['hero']
    assert main_meta['sha256']==variants['main_sha256']
    used=Image.open(a.folder/'beauty/hero.png').convert('RGBA');w,h=used.size
    assert w==a.width
    labels=np.asarray(Image.open(a.folder/'hero-masks/hero.png'))
    ids={n:int(i) for i,n in json.loads((BASE/'build/look-part-ids.json').read_text()).items()}
    results={}
    for name,row in SITES.items():
        variant=variants['sites'][name];folder=out/'off'/name
        if not a.no_render:
            current=json.loads((folder/'shots.json').read_text()) if (folder/'shots.json').exists() else {}
            valid=current.get('hero',{}).get('sha256')==variant['sha256'] and (folder/'hero.png').exists() and Image.open(folder/'hero.png').width==a.width
            if not valid:
                with (BASE/'build'/('wear-'+name+'.log')).open('w') as log:
                    subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1',
                        '--python',str(BASE/'src/final_render.py'),'--','--source',variant['glb'],'--out',str(folder),
                        '--width',str(a.width),'--samples',str(a.samples),'--shots','hero'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        off_meta=json.loads((folder/'shots.json').read_text())['hero'];assert off_meta['sha256']==variant['sha256']
        for key in ('location','target','lens','exposure','aspect','engine'):assert off_meta[key]==main_meta[key],(name,key)
        off=Image.open(folder/'hero.png').convert('RGBA');assert off.size==used.size
        before=np.asarray(off,dtype=float);after=np.asarray(used,dtype=float)
        part=np.isin(labels[:,:,0],[ids[n] for n in row['parts']])&(labels[:,:,3]>250)
        part=np.asarray(Image.fromarray(np.uint8(part)*255).filter(ImageFilter.MinFilter(3)))>0
        delta=np.max(abs(after[:,:,:3]-before[:,:,:3]),axis=2)
        mask=(delta>=6)&part
        ours=evidence(mask,part,angle=projected_axis(main_meta,w))
        ours['profile_axis_radians']=projected_axis(main_meta,w)
        ref=Image.open(BASE/'build/look-photos'/(row['photo']+'.png')).convert('RGB')
        native=Image.open(BASE/'build/look-photos'/(row['photo']+'-native.png')).convert('RGB')
        pm=poly_mask(row['part_polygons'],ref.size);wm=poly_mask(row['polygons'],ref.size)&pm
        pnative=np.asarray(native_mask(Image.fromarray(np.uint8(pm)*255),row['photo'],native.size))>0
        wnative=np.asarray(native_mask(Image.fromarray(np.uint8(wm)*255),row['photo'],native.size))>0
        threshold=row.get('threshold')
        if threshold:wnative&=(np.asarray(native,dtype=float)@LUMA)>=threshold
        photo=evidence(wnative,pnative)
        display_mask=Image.fromarray(np.uint8(wnative)*255)
        if PHOTOS[row['photo']]['angle']:
            display_mask.thumbnail((1707,10000),Image.Resampling.NEAREST)
            display_mask=display_mask.rotate(PHOTOS[row['photo']]['angle'],expand=True,resample=Image.Resampling.NEAREST)
        display_mask=display_mask.resize(ref.size,Image.Resampling.NEAREST)
        wdisplay=(np.asarray(display_mask)>0)&pm
        geometry=evidence(wdisplay,pm)
        for key in ('along_length','across_height','connectivity_raster_size','worn_regions','remaining_finish'):photo[key]=geometry[key]
        photo['profile_axes']='Normalized rigid photo rotation: length horizontal, height vertical; fraction remains native.'
        uncertainty={}
        for t in (3,4,6,8,12):uncertainty[str(t)]=float(((delta>=t)&part).sum()/part.sum())
        eroded=np.asarray(Image.fromarray(np.uint8(wnative)*255).filter(ImageFilter.MinFilter(3)))>0
        dilated=np.asarray(Image.fromarray(np.uint8(wnative)*255).filter(ImageFilter.MaxFilter(3)))>0
        photo_band=[float(eroded.sum()/pnative.sum()),float((dilated&pnative).sum()/pnative.sum())]
        r=dict(ours=ours,photo=photo,description=row['description'],photo_uncertainty=row['uncertainty'],
               rendered_threshold_max_rgb_levels=6,rendered_threshold_sensitivity=uncertainty,
               photo_one_native_pixel_boundary_band=photo_band,
               fraction_difference_percentage_points=(ours['fraction']-photo['fraction'])*100,
               model_sha256=main_meta['sha256'],site_off_sha256=variant['sha256'],
               whole_frame_mean_visible_change=float(delta[part].mean()),maximum_change=float(delta[part].max()),
               passed=abs(ours['fraction']-photo['fraction'])<=max(.005,photo['fraction']*.20))
        results[name]=r
        background=Image.new('RGBA',used.size,(160,160,158,255));on=Image.alpha_composite(background,used).convert('RGB');clean=Image.alpha_composite(background,off).convert('RGB')
        Image.fromarray(np.uint8(mask)*255).save(out/(name+'-render-mask.png'))
        Image.fromarray(np.uint8(wnative)*255).save(out/(name+'-photo-mask.png'))
        Image.fromarray(np.uint8(pnative)*255).save(out/(name+'-photo-part.png'))
        difference=Image.fromarray(np.uint8(np.clip(abs(after[:,:,:3]-before[:,:,:3])*4,0,255)))
        sheet=Image.new('RGB',(1800,1360),(230,231,227));d=ImageDraw.Draw(sheet)
        d.text((15,10),name+' / exported GLB: wear ON, site OFF, difference x4',font=FONT,fill='black')
        for i,im in enumerate((on,clean,difference)):
            sheet.paste(panel(im,(0,0,w,h),(580,225)),(10+i*600,45))
        rb=bbox(part,4)
        on.save(out/(name+'-on.png'));clean.save(out/(name+'-off.png'));difference.save(out/(name+'-difference-x4.png'))
        for label,im in (('on',on),('off',clean),('difference-x4',difference)):
            crop=im.crop(rb);crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(out/(name+'-'+label+'-crop-4x.png'))
        for i,im in enumerate((on,clean,difference)):
            sheet.paste(panel(im,rb,(580,240)),(10+i*600,280))
        reference_box=bbox(pm,3)
        sheet.paste(panel(ref,reference_box,(580,240)),(10,530))
        sheet.paste(panel(Image.fromarray(np.uint8(mask)*255),rb,(580,240),(0,0,0)),(610,530))
        sheet.paste(panel(Image.fromarray(np.uint8(wdisplay)*255),reference_box,(580,240),(0,0,0)),(1210,530))
        d.text((15,780),f'Whole visible part worn: ours {ours["fraction"]*100:.2f}% / photo {photo["fraction"]*100:.2f}%; delta {r["fraction_difference_percentage_points"]:+.2f} percentage points.',font=FONT,fill='black')
        d.text((15,812),'Photo context (left); actual exported-image binary difference (center); independent photograph annotation (right).',font=SMALL,fill='black')
        graph(d,(15,845,860,150),ours['along_length'],photo['along_length'],'Worn share along the part')
        graph(d,(920,845,860,150),ours['across_height'],photo['across_height'],'Worn share across its height')
        d.text((15,1010),row['description'],font=SMALL,fill='black')
        d.text((15,1040),'2D regions, ours / photo: worn '+str(ours['worn_regions']['count'])+' / '+str(photo['worn_regions']['count'])+
               '; remaining finish '+str(ours['remaining_finish']['count'])+' / '+str(photo['remaining_finish']['count']),font=SMALL,fill='black')
        d.text((15,1070),'Largest worn region as share of whole part, ours / photo: '+
               str([round(v['fraction_of_part']*100,2) for v in ours['worn_regions']['largest'][:4]])+' / '+
               str([round(v['fraction_of_part']*100,2) for v in photo['worn_regions']['largest'][:4]]),font=SMALL,fill='black')
        import textwrap
        lines=textwrap.wrap('Uncertainty: '+row['uncertainty'],width=170)
        for i,line in enumerate(lines):d.text((15,1100+25*i),line,font=SMALL,fill='black')
        d.text((15,1190),'Threshold sensitivity (3,4,6,8,12 RGB levels): '+str([round(v*100,2) for v in uncertainty.values()])+'%.',font=SMALL,fill='black')
        d.text((15,1220),'Photo +/- one native boundary pixel: '+str([round(v*100,2) for v in photo_band])+'%. No shader-mask or line-profile acceptance.',font=SMALL,fill='black')
        d.text((15,1250),'Fraction target: '+('within 20% / 0.5 pp' if r['passed'] else 'MISS; see residual and visual assessment in REVIEW.md'),font=SMALL,fill='black')
        sheet.save(out/(name+'-on-off-pair.jpg'),quality=94,optimize=True)
        print(name,round(ours['fraction']*100,2),round(photo['fraction']*100,2),flush=True)
    (out/'measurements.json').write_text(json.dumps(dict(method='Actual same-camera image differences of kit-exported site-off GLBs; native balanced photos; independent full visible part denominators; all nine sites',sites=results),indent=2))
if __name__=='__main__':main()
