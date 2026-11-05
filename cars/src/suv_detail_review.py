"""Checkpoint sheets, white-balanced comparison samples and source tone proof."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.photo_match import compose
ASSET=Path(__file__).resolve().parents[1]
FONT=find_font('Noto Sans','Regular')


def rgb(path):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGBA')
    bg=Image.new('RGBA',im.size,(232,234,234,255));bg.alpha_composite(im)
    return bg.convert('RGB')


def sheet(items,path,columns=2,width=1600,cell_height=540):
    cw=width//columns;page=Image.new('RGB',(width,cell_height*((len(items)+columns-1)//columns)),(232,234,234));d=ImageDraw.Draw(page);font=ImageFont.truetype(FONT,19)
    for i,(label,file) in enumerate(items):
        im=ImageOps.contain(rgb(file),(cw-24,cell_height-56),Image.Resampling.LANCZOS);x=i%columns*cw;y=i//columns*cell_height
        page.paste(im,(x+(cw-im.width)//2,y+42+(cell_height-50-im.height)//2));d.text((x+12,y+10),label,font=font,fill=(25,37,41))
    page.save(path,quality=91,optimize=True)


def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,a*12.92,1.055*a**(1/2.4)-.055)


def pairs(out,asset_label='Original X220 / source'):
    settings={
      'used_front':dict(file='suv-used-crv-front.jpg',neutral=(25,797,90,818),neutral_description='Neutral asphalt in the lower-left foreground; aged pavement, not a calibrated gray card',patches=dict(door_mid=(827,438,912,477),door_low=(823,537,911,558),cladding=(808,599,887,613),glass=(900,236,936,273))),
      'used_rear':dict(file='suv-used-rav4-rear.jpg',neutral=(6,124,15,137),neutral_description='Unprinted white area of the parking sign at the left edge',patches=dict(door_mid=(431,410,478,447),rear_quarter=(820,435,864,470),cladding=(1035,595,1110,619),glass=(594,191,630,231)))}
    report={}
    for name,rec in settings.items():
        native=rgb(ASSET/'refs'/rec['file']);photo=native.resize((1400,round(1400*native.height/native.width)),Image.Resampling.LANCZOS)
        render=rgb(out/(name+'.png'));render=render.resize(photo.size,Image.Resampling.LANCZOS)
        array=np.asarray(photo)/255;box=rec['neutral'];neutral=np.median(linear(array[box[1]:box[3],box[0]:box[2]]).reshape(-1,3),axis=0);gains=neutral.mean()/neutral
        photo=Image.fromarray(np.uint8(np.clip(srgb(linear(array)*gains),0,1)*255+.5));balanced=name+'-reference-balanced.jpg'
        tables=[np.uint8(np.clip(srgb(linear(np.arange(256)/255)*gain),0,1)*255+.5).tolist() for gain in gains]
        Image.merge('RGB',tuple(band.point(table) for band,table in zip(native.split(),tables))).save(out/balanced,quality=95,optimize=True)
        item=dict(neutral_box_1400=box,neutral_description=rec['neutral_description'],linear_white_balance_gains=gains.tolist(),balanced_reference=balanced,patches={})
        for label,rect in rec['patches'].items():
            pp=np.median(np.asarray(photo.crop(rect)).reshape(-1,3),axis=0);rr=np.median(np.asarray(render.crop(rect)).reshape(-1,3),axis=0)
            item['patches'][label]=dict(photo_box_1400=rect,render_box_1400=rect,photo_rgb=pp.tolist(),render_rgb=rr.tolist(),photo_luma=float(pp@[.2126,.7152,.0722]),render_luma=float(rr@[.2126,.7152,.0722]))
        item['scope']='Display RGB after photographic neutral balance; chassis-camera correspondence, not measured albedo or identical reflection environments'
        report[name]=item
        crops={'lamp':(220,350,530,520),'wheel':(470,480,730,790)} if name=='used_front' else {'lamp':(790,290,1080,400),'cladding':(925,510,1365,680)}
        for label,rect in crops.items():
            views=[render.crop(rect),photo.crop(rect)];height=round(800*views[0].height/views[0].width)
            page=Image.new('RGB',(1600,height+42),(232,234,234));d=ImageDraw.Draw(page)
            for j,(view,title) in enumerate(zip(views,[asset_label,'Used reference / neutral balanced'])):
                page.paste(view.resize((800,height),Image.Resampling.LANCZOS),(j*800,42));d.text((j*800+10,10),title,font=ImageFont.truetype(FONT,18),fill=(25,37,41))
            page.save(out/(name+'-'+label+'-pair.jpg'),quality=93,optimize=True)
        annotated=[]
        for im,color in [(render,'cyan'),(photo,'red')]:
            copy=im.copy();d=ImageDraw.Draw(copy)
            for label,rect in rec['patches'].items():d.rectangle(rect,outline=color,width=2);d.text((rect[0],rect[1]-17),label,fill=color,font=ImageFont.truetype(FONT,14))
            annotated.append(copy)
        ImageDraw.Draw(annotated[1]).rectangle(box,outline='white',width=2)
        page=Image.new('RGB',(2800,photo.height),(232,234,234));page.paste(annotated[0],(0,0));page.paste(annotated[1],(1400,0));page.save(out/(name+'-measurement-picks.jpg'),quality=93,optimize=True)
    (out/'pair-measurements.json').write_text(json.dumps(report,indent=2));return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--form',required=True);p.add_argument('--cameras',required=True);p.add_argument('--report',required=True);a=p.parse_args()
    out,form=Path(a.renders),Path(a.form);data=json.loads(Path(a.report).read_text());meta=json.loads((out/'shots.json').read_text());names=list(meta)
    stale=[name for name,r in meta.items() if r['source_sha256']!=data['source_sha256']]
    if stale:raise ValueError('Stale source renders: '+str(stale))
    recipes=[ASSET/'src/suv_lookdev.py',ASSET/'src/suv_lighting.py',ASSET/'src/suv_finishes.py',ASSET/'src/lighting.py',ROOT/'kit/studio.py']
    recipe_hash=hashlib.sha256(b''.join(p.read_bytes() for p in recipes)).hexdigest()
    if any(r['render_recipe_sha256']!=recipe_hash for r in meta.values()):raise ValueError('Stale render recipe; rerender affected views')
    sweeps=json.loads((out/'sweeps.json').read_text())
    if any(r['source_sha256']!=data['source_sha256'] for r in sweeps.values()):raise ValueError('Stale motion trajectory images')
    colors=[f'{color}_{view}' for color in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for view in ['front_three_quarter','rear_three_quarter']]
    sheet([(name.replace('_',' '),out/(name+'.png')) for name in colors],out/'five-colors.jpg',cell_height=480)
    details=['face','lamp_unlit','lamp_lit','wheel','cladding','interior_glass','interior_dash','cargo_open','underbody','underbody_layout','opened','gate_open','steering']
    sheet([(name.replace('_',' '),out/(name+'.png')) for name in details],out/'details.jpg')
    sheet([(name.replace('_',' '),out/(name+'.png')) for name in ['opened','gate_open','sweeps_front','sweeps_rear','steering']],out/'motion.jpg')
    sheet([(name.replace('_',' '),form/'gloss'/(name+'.png')) for name in ['front_three_quarter','rear_three_quarter','side']],out/'gloss-clay.jpg')
    for view in ['front_three_quarter','rear_three_quarter','side','front','rear']:
        sheet([('Actual triangles / signed mean curvature',form/('mean_curvature_'+view+'.png')),('Matching camera / reflection bands',form/('curvature_stripes_'+view+'.png'))],out/('curvature-'+view+'.jpg'),cell_height=620)
    form_views=sorted(form.glob('*.png'))
    sheet([(file.stem.replace('_',' '),file) for file in form_views],out/'form-contact.jpg',columns=3,cell_height=360)
    gloss_calibration=json.loads((ASSET/'build/suv/cameras.json').read_text())
    for name,rec in gloss_calibration.items():rec['title']='Alder X220 / '+name+' / GLOSS CLAY'
    gc=form/'gloss-pairs/calibration.json';gc.write_text(json.dumps(gloss_calibration,indent=2))
    compose(gc,form/'gloss-pairs',form/'gloss-pairs')
    # The original form calibration's historical title mentions stripes; label
    # the gloss sheets explicitly instead of making a shader claim from it.
    sheet([(name+' / gloss clay beside reference',form/'gloss-pairs'/(name+'-pair.jpg')) for name in ['crv_front','rav4_front','crv_rear','rav4_rear']],out/'gloss-pairs.jpg',columns=1,cell_height=690)
    measurements=pairs(out);tones={}
    balanced=json.loads(Path(a.cameras).read_text())
    for name,rec in balanced.items():
        rec['photo']=str((out/measurements[name]['balanced_reference']).resolve());rec['title']+=' / reference neutral-balanced'
    calibration=out/'balanced-comparisons.json';calibration.write_text(json.dumps(balanced,indent=2));compose(calibration,out,out)
    for name in names:
        im=np.asarray(Image.open(out/(name+'.png')).convert('RGB'));mask=np.asarray(Image.open(out/meta[name]['tonal_mask']).convert('RGBA'))
        geometry=mask[:,:,3]>240;paint=geometry & (mask[:,:,:3].mean(axis=2)>240)
        row={}
        for label,selection in [('geometry',geometry),('paint',paint)]:
            pixels=im[selection];luma=pixels@[.2126,.7152,.0722]
            row[label]=dict(pixels=len(pixels),luma_p1_p50_p95_p99=np.percentile(luma,[1,50,95,99]).tolist() if len(pixels) else None,clipped_channel_fraction=float((pixels>=255).mean()) if len(pixels) else None)
        tones[name]=row
    (out/'tonal-ranges.json').write_text(json.dumps(tones,indent=2))
    sheet([(name+' / paint and geometry mask',out/meta[name]['tonal_mask']) for name in names],out/'masks-contact.jpg',columns=3,cell_height=330)
    contact=[(name.replace('_',' '),out/(name+'.png')) for name in names]
    contact += [('Motion / '+name,out/(name+'.png')) for name in ['sweeps_front','sweeps_rear']]
    contact += [('Photo pair / '+name,out/(name+'-pair.jpg')) for name in ['used_front','used_rear']]
    contact += [('Gloss / '+name,form/'gloss'/(name+'.png')) for name in ['front_three_quarter','rear_three_quarter','side']]
    contact += [('Curvature and bands / '+view,out/('curvature-'+view+'.jpg')) for view in ['front_three_quarter','rear_three_quarter','side','front','rear']]
    sheet(contact,out/'contact.jpg',columns=3,cell_height=360)
    (out/'checkpoint.json').write_text(json.dumps(dict(stage='Source detail/look checkpoint; no SUV bake/GLB',source_sha256=data['source_sha256'],triangles=data['triangles'],renders=len(names),actual_vertex_bounds_m=data['actual_vertex_bounds_m'],pair_measurements=measurements,tonal_ranges=tones),indent=2))
    print('SUV_REVIEW',out/'contact.jpg',len(names),'source renders')

if __name__=='__main__':main()
