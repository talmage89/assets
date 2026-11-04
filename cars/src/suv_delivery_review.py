"""Final GLB provenance, photo values, bake loss, contact sheets and bounded docs."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageFilter
from suv_detail_review import sheet,rgb,pairs
from kit.photo_match import compose

ASSET=Path(__file__).resolve().parents[1]


def photo_pages(out,label):
    result=pairs(out,label);cal=json.loads((ASSET/'build/suv-detail/used-cameras.json').read_text())
    for name,row in cal.items():
        row['photo']=str((out/result[name]['balanced_reference']).resolve());row['title']='X220 / '+label+' / accepted matched daylight / '+name
    path=out/'balanced-comparisons.json';path.write_text(json.dumps(cal,indent=2));compose(path,out,out)
    return result


def bounded_jpg(source,destination):
    im=ImageOps.contain(rgb(source),(1600,20000),Image.Resampling.LANCZOS)
    for quality in range(93,39,-3):
        im.save(destination,quality=quality,optimize=True,progressive=True)
        if destination.stat().st_size<=200000:return
    raise ValueError('Docs JPG cannot meet its budget: '+str(destination))


def main():
    p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args()
    out=ASSET/'renders/suv-final';eevee=ASSET/'renders/suv-eevee';photo=ASSET/'renders/suv-final-pairs';control=ASSET/'renders/suv-source-pairs';studio_control=ASSET/'renders/suv-source-studio'
    glb=ASSET/'export/AlderX220.glb';digest=hashlib.sha256(glb.read_bytes()).hexdigest()
    meta=json.loads((out/'shots.json').read_text())
    for directory in [out,eevee,photo]:
        data=json.loads((directory/'shots.json').read_text())
        if any(v['source_sha256']!=digest or v['stage']!='final exported GLB' for v in data.values()):raise ValueError('Stale final GLB image '+str(directory))
    final=photo_pages(photo,'Exported GLB / baked textures');source=photo_pages(control,'Source procedural materials')
    loss={}
    for name,row in final.items():
        loss[name]={}
        for patch,values in row['patches'].items():
            previous=source[name]['patches'][patch]
            loss[name][patch]=dict(source_luma=previous['render_luma'],export_luma=values['render_luma'],balanced_photo_luma=values['photo_luma'],bake_luma_delta=values['render_luma']-previous['render_luma'],bake_rgb_delta=(np.array(values['render_rgb'])-previous['render_rgb']).tolist())
        sheet([('Source / same sun and sky',control/(name+'.png')),('Export / baked three-map set',photo/(name+'.png')),('Balanced reference',photo/row['balanced_reference'])],photo/(name+'-source-export.jpg'),columns=3,width=2400,cell_height=650)
    studio_loss={}
    for name in ['hero','face','lamp','wheel']:
        aa=np.asarray(rgb(studio_control/(name+'.png')),np.float32);bb=np.asarray(rgb(out/(name+'.png')),np.float32)
        mask=np.asarray(Image.open(out/(name+'-mask.png')).convert('RGBA'));valid=(mask[:,:,3]>240)&(mask[:,:,:3].mean(axis=2)>240)
        valid=np.asarray(Image.fromarray(valid.astype(np.uint8)*255).filter(ImageFilter.MinFilter(5)))>0
        diff=bb[valid]-aa[valid];studio_loss[name]=dict(paint_pixels=int(valid.sum()),mean_absolute_rgb_delta=float(np.abs(diff).mean()),rgb_rmse=float(np.sqrt((diff**2).mean())))
        sheet([('Procedural source / gallery',studio_control/(name+'.png')),('Baked GLB / same camera and lights',out/(name+'.png'))],out/(name+'-source-export.jpg'),columns=2,width=2400,cell_height=850)
    (out/'bake-loss.json').write_text(json.dumps(dict(scope='Display RGB deltas in identical cameras/lights/exposure; source/export differences include atlas filtering and uniform surface approximations',photo_patches=loss,studio_paint=studio_loss),indent=2))
    tones={}
    for name in meta:
        values=np.asarray(rgb(out/(name+'.png')));mask=np.asarray(Image.open(out/(name+'-mask.png')).convert('RGBA'))
        geometry=mask[:,:,3]>240;paint=geometry&(mask[:,:,:3].mean(axis=2)>240);tones[name]={}
        for label,selected in [('geometry',geometry),('paint',paint)]:
            pixels=values[selected];luma=pixels@[.2126,.7152,.0722]
            tones[name][label]=dict(pixels=len(pixels),luma_p1_p50_p95_p99=np.percentile(luma,[1,50,95,99]).tolist(),clipped_pixels=int(np.count_nonzero(pixels.max(axis=1)>=255)),clipped_channel_fraction=float((pixels>=255).mean()))
    (out/'tonal-ranges.json').write_text(json.dumps(tones,indent=2))
    colors=[c+'_'+v for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for v in ['hero','rear']]
    sheet([(n.replace('_',' '),out/(n+'.png')) for n in colors],out/'five-colors.jpg',cell_height=480)
    sheet([(n,out/(n+'.png')) for n in ['face','wheel','cargo','lamps_lit']],out/'details.jpg',cell_height=600)
    sheet([(n,out/(n+'.png')) for n in ['front','side','back','top']]+[('1.8 m scale',out/'scale.png'),('Eevee / baked GLB',eevee/'hero.png')],out/'views.jpg',columns=2,cell_height=510)
    contact=[(n,out/(n+'.png')) for n in meta]
    contact+=[('Eevee',eevee/'hero.png')]+[(n+' / matched light',photo/(n+'-pair.jpg')) for n in final]
    sheet(contact,out/'contact.jpg',columns=3,width=1800,cell_height=400)
    motion=ASSET/'renders/suv-motion'
    if (motion/'shots.json').exists():
        mm=json.loads((motion/'shots.json').read_text())
        if any(v['source_sha256']!=digest for v in mm.values()):raise ValueError('Stale motion frames')
        sheet([(n,motion/(n+'.png')) for n in mm],motion/'contact.jpg',columns=3,width=1800,cell_height=400)
    if a.docs:
        docs=ASSET/'docs';docs.mkdir(exist_ok=True)
        for name,source_image in [('hero','hero.png'),('rear','rear.png'),('details','details.jpg'),('views','views.jpg'),('five-colors','five-colors.jpg')]:bounded_jpg(out/source_image,docs/('suv-'+name+'.jpg'))
        if (motion/'shots.json').exists():
            accepted=False
            for width in [800,720,640,560,480]:
                frames=[ImageOps.contain(rgb(motion/(n+'.png')),(width,width),Image.Resampling.LANCZOS) for n in mm]
                swatches=Image.new('RGB',(160*len(frames),100))
                for i,im in enumerate(frames):swatches.paste(im.resize((160,100)),(160*i,0))
                for colors in [256,128,96]:
                    palette=swatches.quantize(colors=colors,method=Image.Quantize.MEDIANCUT)
                    reduced=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
                    reduced[0].save(docs/'suv-liftgate.gif',save_all=True,append_images=reduced[1:],duration=110,loop=0,optimize=True,disposal=1)
                    if (docs/'suv-liftgate.gif').stat().st_size<=450000:accepted=True;break
                if accepted:break
            if not accepted:raise ValueError('Liftgate GIF exceeds budget')
    print('X220_FINAL_REVIEW',digest,'frames',len(meta),'bake loss',loss)


if __name__=='__main__':main()
