"""Rebuild the SUV surface gate's studio, fairness, pairs and comparison pages.

Run through ``make BODY=suv surfaces``. All Cycles subprocesses use the shared
kit lock. Earlier detail images and the optional frozen source are read-only.
This source checkpoint deliberately does not imply a bake or GLB delivery.
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[2]
ASSET=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ASSET/'src')]
from suv_detail_review import sheet, rgb, pairs, FONT
from kit.photo_match import compose

VIEWS=['front_three_quarter','rear_three_quarter','side','front','rear','face','lamp_unlit','rear_quarter']
COLORS=['Porcelain','Carbon','Graphite','Aluminum','Atlantic']


def run(a, script, args, gpu=False):
    cmd=([str(ROOT/'kit/with_gpu.sh')] if gpu else [])+[a.blender,'-t','6' if gpu else '1','-b','--factory-startup','--python-exit-code','1','--python',str(ASSET/'src'/script),'--',*map(str,args)]
    print('SURFACE_CHECKPOINT',script,*args,flush=True)
    subprocess.run(cmd,cwd=ASSET,check=True)


def crop_page(items, rect, path):
    # Same normalized camera crop, independent of preview/final image size.
    width=1800;cw=width//len(items);images=[]
    for title,p in items:
        im=rgb(p);box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(rect))
        images.append((title,im.crop(box)))
    ch=round(cw*images[0][1].height/images[0][1].width)
    page=Image.new('RGB',(width,ch+60),(232,234,234));d=ImageDraw.Draw(page)
    for j,(title,im) in enumerate(images):
        page.paste(im.resize((cw,ch),Image.Resampling.LANCZOS),(j*cw,60))
        d.text((j*cw+10,12),title,font=ImageFont.truetype(FONT,17),fill=(25,37,41))
    page.save(path,quality=95,optimize=True)


def review(out,before,control):
    meta=json.loads((out/'shots.json').read_text())
    source_hashes={r['source_sha256'] for r in meta.values()}
    if len(source_hashes)!=1:raise ValueError('Mixed source hashes in checkpoint studio/pairs')
    colors=[f'{c}_{v}' for c in COLORS for v in ['front_three_quarter','rear_three_quarter']]
    sheet([(n.replace('_',' '),out/(n+'.png')) for n in colors],out/'five-colors.jpg',cell_height=490)
    sheet([(n.replace('_',' '),out/(n+'.png')) for n in ['face','lamp_unlit','rear_quarter']],out/'close-ups.jpg',columns=1,width=1600,cell_height=1020)
    for v in VIEWS:
        sheet([('Actual triangles / signed mean H',out/('mean_curvature_'+v+'.png')),
               ('All exterior parts / horizontal reflection bands',out/('curvature_stripes_'+v+'.png')),
               ('All exterior parts / vertical reflection bands',out/('curvature_stripes_vertical_'+v+'.png'))],out/('fairness-'+v+'.jpg'),columns=1,width=1400,cell_height=850)
    definitions={
        'face':('face',(.055,.08,.94,.97)),
        'hood':('face',(.07,.04,.98,.39)),
        'lens':('lamp_unlit',(.20,.28,.99,.79)),
        'front-fender':('lamp_unlit',(.35,.69,.99,.99)),
        'rear-quarter':('rear_three_quarter',(.28,.32,.58,.76)),
        'rear-bumper':('rear_three_quarter',(.105,.59,.57,.84)),
        'rear-arch-tail':('front_three_quarter',(.74,.41,.86,.68)),
        'windshield':('front_three_quarter',(.25,.20,.65,.49)),
        'backlight':('rear_three_quarter',(.12,.30,.41,.48))}
    for label,(view,rect) in definitions.items():
        oldname='Graphite_'+view if view in ['front_three_quarter','rear_three_quarter'] else view
        items=[]
        if (before/(oldname+'.png')).exists():items.append(('Earlier detail / original lighting',before/(oldname+'.png')))
        if (control/(view+'.png')).exists():items.append(('Earlier mesh / same softbox stage',control/(view+'.png')))
        items.append(('Repaired / same softbox stage',out/(view+'.png')))
        crop_page(items,rect,out/('before-after-'+label+'.jpg'))
    if (control/'rear_quarter.png').exists():
        crop_page([('Earlier mesh / same camera and light',control/'rear_quarter.png'),('Repaired quarter / same camera and light',out/'rear_quarter.png')],(0,0,1,1),out/'quarter-same-light.jpg')
    measurements=pairs(out)
    calibration=json.loads((ASSET/'build/suv-detail/used-cameras.json').read_text())
    for name,r in calibration.items():
        r['photo']=str((out/measurements[name]['balanced_reference']).resolve())
        r['title']='X220 / estimated matched diffuse sun and sky / '+name
        measurements[name]['lighting']=meta[name]['lighting']
        measurements[name]['scope']='Display RGB after scene-neutral photographic white balance, under photo-estimated diffuse sun/sky; different surroundings and original body, not measured albedo'
    (out/'pair-measurements.json').write_text(json.dumps(measurements,indent=2))
    (out/'balanced-comparisons.json').write_text(json.dumps(calibration,indent=2))
    compose(out/'balanced-comparisons.json',out,out)
    tones={}
    for name in colors+['face','lamp_unlit','rear_quarter','used_front','used_rear']:
        im=np.asarray(Image.open(out/(name+'.png')).convert('RGB'))
        mask=np.asarray(Image.open(out/(name+'-mask.png')).convert('RGBA'))
        geometry=mask[:,:,3]>240;paint=geometry&(mask[:,:,:3].mean(axis=2)>240)
        tones[name]={}
        for label,sel in [('geometry',geometry),('paint',paint)]:
            pixels=im[sel];luma=pixels@[.2126,.7152,.0722]
            tones[name][label]=dict(pixels=len(pixels),luma_p1_p50_p95_p99=np.percentile(luma,[1,50,95,99]).tolist(),clipped_channel_fraction=float((pixels>=255).mean()))
    (out/'tonal-ranges.json').write_text(json.dumps(tones,indent=2))
    pages=[('Five colors / front and rear',out/'five-colors.jpg')]
    pages += [('Softbox / '+n,out/(n+'.png')) for n in ['face','lamp_unlit','rear_quarter']]
    pages += [('Before / after '+n,out/('before-after-'+n+'.jpg')) for n in definitions]
    pages += [('Photo-estimated daylight / '+n,out/(n+'-pair.jpg')) for n in ['used_front','used_rear']]
    pages += [('All exterior fairness / '+v,out/('fairness-'+v+'.jpg')) for v in VIEWS]
    sheet(pages,out/'contact.jpg',columns=3,width=1800,cell_height=460)
    (out/'checkpoint.json').write_text(json.dumps(dict(stage='Source surface checkpoint; no baked SUV GLB',source_sha256=next(iter(source_hashes)),pair_measurements=measurements,tonal_ranges=tones),indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/suv-detail/game.blend');p.add_argument('--out',default='renders/suv-surfaces');p.add_argument('--before',default='renders/suv-detail');p.add_argument('--control',default='renders/suv-surface-control');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);p.add_argument('--blender',default='blender');p.add_argument('--compose-only',action='store_true')
    a=p.parse_args();os.chdir(ASSET);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    if not a.compose_only:
        base=['--source',a.source,'--out',a.out,'--width',a.width,'--samples',a.samples]
        run(a,'suv_lookdev.py',base+['--shots','face,lamp_unlit,rear_quarter,front_three_quarter,rear_three_quarter','--masks'],True)
        run(a,'suv_lookdev.py',base+['--colors','--masks'],True)
        run(a,'suv_lookdev.py',base+['--camera-file','build/suv-detail/used-cameras.json','--masks'],True)
        diagnostic=Path('build/suv-surfaces/curvature')
        run(a,'suv_curvature_map.py',['--source',a.source,'--out',diagnostic])
        run(a,'suv_render.py',['--source',diagnostic/'mean-curvature.blend','--out',a.out,'--mode','curvature','--width',a.width,'--samples','16'],True)
        for direction in ['horizontal','vertical']:
            run(a,'suv_render.py',base+['--mode','diagnostic_stripes','--direction',direction],True)
    review(out,Path(a.before),Path(a.control))


if __name__=='__main__':main()
