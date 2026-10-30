"""Native photographic 2D wear evidence, with complete visible-part denominators.

Same exported GLBs, camera, physical lights and exposure at 4000 pixels. This
resolves diamond tips which merged in the archived 1600-pixel diagnostic.
Never substitutes the source shader's wear mask for an actual image change.
"""
import argparse,hashlib,json,subprocess,sys,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from wear_reference import SITES
from wear_review import evidence,bbox,components,projected_axis,graph
from look_matches import PHOTOS
from look_review import native_mask,panel,LUMA
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)

def render(source,out,width,samples,reuse=None):
    h=hashlib.sha256()
    for p in [BASE/'src/final_render.py',BASE/'src/final_shots.py',BASE.parent/'common/render.py']:h.update(p.read_bytes())
    signature=h.hexdigest();digest=hashlib.sha256(Path(source).read_bytes()).hexdigest()
    # Reuse byte-identical primary evidence when it already has this native
    # resolution and exact renderer/source signatures. Never rescale an image.
    if reuse is not None and (reuse/'shots.json').exists() and (reuse/'hero.png').exists():
        shared=json.loads((reuse/'shots.json').read_text()).get('hero',{})
        if (shared.get('sha256')==digest and shared.get('samples_used')==samples and
            shared.get('renderer_signature')==signature and Image.open(reuse/'hero.png').width==width):
            out.mkdir(parents=True,exist_ok=True);shutil.copy2(reuse/'hero.png',out/'hero.png')
            (out/'shots.json').write_text(json.dumps(dict(hero=shared),indent=2))
    meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    old=meta.get('hero',{})
    if not (old.get('sha256')==digest and old.get('samples_used')==samples and old.get('renderer_signature')==signature and
            (out/'hero.png').exists() and Image.open(out/'hero.png').width==width):
        out.mkdir(parents=True,exist_ok=True)
        log=BASE/'build'/('wear-native-'+out.name+'.log')
        with log.open('w') as f:
            subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),
                '--','--source',str(source),'--out',str(out),'--width',str(width),'--samples',str(samples),'--shots','hero'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
        meta=json.loads((out/'shots.json').read_text());meta['hero']['renderer_signature']=signature
        (out/'shots.json').write_text(json.dumps(meta,indent=2))
    return meta['hero']

def normalized(mask,part,angle=0):
    result=evidence(mask,part,angle=angle)
    x0,y0,x1,y1=bbox(part);scale=800/max(x1-x0,y1-y0)
    size=(max(1,round((x1-x0)*scale)),max(1,round((y1-y0)*scale)))
    p=np.asarray(Image.fromarray(np.uint8(part[y0:y1,x0:x1])*255).resize(size,Image.Resampling.NEAREST))>0
    m=np.asarray(Image.fromarray(np.uint8(mask[y0:y1,x0:x1])*255).resize(size,Image.Resampling.NEAREST))>0
    result.update(connectivity_raster_size=size,worn_regions=components(m,p),remaining_finish=components(p&~m,p))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=4000);p.add_argument('--samples',type=int,default=48);a=p.parse_args()
    out=BASE/'renders/final/wear-native';out.mkdir(parents=True,exist_ok=True)
    variants=json.loads((BASE/'build/wear/variants.json').read_text());main_path=BASE/'export/sxs.glb'
    meta=render(main_path,out/'on',a.width,a.samples,reuse=BASE/'renders/final/beauty');assert meta['sha256']==variants['main_sha256']
    coarse=json.loads((BASE/'renders/final/beauty/shots.json').read_text())['hero']
    for key in ['location','target','lens','aspect','exposure','engine']:assert meta[key]==coarse[key]
    mask_meta=out/'masks/shots.json'
    current=json.loads(mask_meta.read_text()) if mask_meta.exists() else {}
    if current.get('hero',{}).get('sha256')!=meta['sha256'] or not (out/'masks/hero.png').exists() or Image.open(out/'masks/hero.png').width!=a.width:
        with (BASE/'build/wear-native-masks.log').open('w') as f:
            subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/part_masks.py'),
                '--','--source',str(main_path),'--photos',str(out/'on'),'--out',str(out/'masks'),'--shots','hero'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
    labels=np.asarray(Image.open(out/'masks/hero.png'));ids={n:int(i) for i,n in json.loads((BASE/'build/look-part-ids.json').read_text()).items()}
    on=Image.open(out/'on/hero.png').convert('RGBA');after=np.asarray(on,dtype=float);records={}
    for name,row in SITES.items():
        off_meta=render(variants['sites'][name]['glb'],out/'off'/name,a.width,a.samples,reuse=BASE/'renders/final/wear/off'/name)
        for key in ['location','target','lens','aspect','exposure','engine']:assert off_meta[key]==meta[key]
        off=Image.open(out/'off'/name/'hero.png').convert('RGBA');before=np.asarray(off,dtype=float)
        part=np.isin(labels[:,:,0],[ids[n] for n in row['parts']])&(labels[:,:,3]>250)
        delta=np.max(abs(after[:,:,:3]-before[:,:,:3]),axis=2);worn=(delta>=6)&part
        ours=normalized(worn,part,projected_axis(meta,a.width));ours['threshold_sensitivity']={str(t):float(((delta>=t)&part).sum()/part.sum()) for t in (3,4,6,8,12)}
        native=Image.open(BASE/'build/look-photos'/(row['photo']+'-native.png')).convert('RGB')
        preview=Image.open(BASE/'build/look-photos'/(row['photo']+'.png'))
        def annotation(polys):
            im=Image.new('L',preview.size);draw=ImageDraw.Draw(im)
            for polygon in polys:draw.polygon(polygon,fill=255)
            return np.asarray(native_mask(im,row['photo'],native.size))>0
        pm=annotation(row['part_polygons']);wm=annotation(row['polygons'])&pm
        if row.get('threshold'):wm&=(np.asarray(native,dtype=float)@LUMA)>=row['threshold']
        photo=normalized(wm,pm)
        angle=PHOTOS[row['photo']]['angle']
        if angle:
            native=native.rotate(angle,expand=True,resample=Image.Resampling.BICUBIC)
            pm=np.asarray(Image.fromarray(np.uint8(pm)*255).rotate(angle,expand=True,resample=Image.Resampling.NEAREST))>0
            wm=np.asarray(Image.fromarray(np.uint8(wm)*255).rotate(angle,expand=True,resample=Image.Resampling.NEAREST))>0
            geometry=normalized(wm,pm)
            for key in ['along_length','across_height','connectivity_raster_size','worn_regions','remaining_finish']:photo[key]=geometry[key]
        difference=Image.fromarray(np.uint8(np.clip(abs(after[:,:,:3]-before[:,:,:3])*4,0,255)))
        rb=bbox(part,3);pb=bbox(pm,3)
        sheet=Image.new('RGB',(1800,1200),(230,231,227));d=ImageDraw.Draw(sheet)
        d.text((15,10),name+' / native 2D: same exported hero at '+str(a.width)+' pixels; photo remains native',font=FONT,fill='black')
        for i,(im,box) in enumerate([(on,rb),(off,rb),(native,pb)]):sheet.paste(panel(im,box,(580,300)),(10+600*i,45))
        for i,(im,box) in enumerate([(difference,rb),(Image.fromarray(np.uint8(worn)*255),rb),(Image.fromarray(np.uint8(wm)*255),pb)]):
            sheet.paste(panel(im,box,(580,280)),(10+600*i,355))
        graph(d,(15,660,860,150),ours['along_length'],photo['along_length'],'Worn share along the part')
        graph(d,(920,660,860,150),ours['across_height'],photo['across_height'],'Worn share across its height')
        d.text((15,830),f'Native visible fractions: ours {ours["fraction"]*100:.2f}% / photo {photo["fraction"]*100:.2f}%. Complete visible parts; full-frame on/off proof is separate.',font=FONT,fill='black')
        d.text((15,870),'800-pixel longest part dimension, aspect preserved. Both worn regions and surviving finish use 8-connectivity.',font=SMALL,fill='black')
        d.text((15,900),'Worn region counts ours / photo: '+str(ours['worn_regions']['count'])+' / '+str(photo['worn_regions']['count'])+
            '; surviving finish: '+str(ours['remaining_finish']['count'])+' / '+str(photo['remaining_finish']['count']),font=SMALL,fill='black')
        d.text((15,930),'Largest worn shares ours / photo: '+str([round(v['fraction_of_part']*100,2) for v in ours['worn_regions']['largest'][:4]])+' / '+
            str([round(v['fraction_of_part']*100,2) for v in photo['worn_regions']['largest'][:4]]),font=SMALL,fill='black')
        import textwrap
        for i,line in enumerate(textwrap.wrap(row['uncertainty'],width=170)):d.text((15,970+24*i),line,font=SMALL,fill='black')
        d.text((15,1080),'Physical part forms and perspective differ. No 1D or region-count acceptance replaces inspection of these 2D fields.',font=SMALL,fill='black')
        sheet.save(out/(name+'-native-2d-pair.jpg'),quality=94,optimize=True)
        Image.fromarray(np.uint8(worn)*255).save(out/(name+'-render-mask.png'));Image.fromarray(np.uint8(wm)*255).save(out/(name+'-photo-mask.png'))
        records[name]=dict(ours=ours,photo=photo,model_sha256=meta['sha256'],site_off_sha256=off_meta['sha256'],threshold=6)
        print('NATIVE WEAR',name,round(ours['fraction']*100,2),round(photo['fraction']*100,2),ours['worn_regions']['count'],photo['worn_regions']['count'],flush=True)
    (out/'measurements.json').write_text(json.dumps(dict(method='Same-camera actual exported-image differences at 4000 pixels; complete visible parts without erosion; native balanced photographs, 800-pixel 2D connectivity raster; no source wear masks',sites=records),indent=2))
if __name__=='__main__':main()
