"""Round-four maps, calibrated gloss pairs, and unchanged-camera comparisons."""
import argparse,hashlib,io,json,math,subprocess,tarfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from hatch_review import ROOT,ASSET,font,rgb,save

VIEWS=['front_three_quarter','rear_three_quarter','side','front','rear']
PAIRS=[m+'_'+v for m in ['corolla','hyundai'] for v in ['front','rear','side']]


def baseline(blender,width,samples,model_only=False):
    """Recover our own accepted source; no other worktree is read or changed."""
    dest=ASSET/'build/hatch-round3-baseline';model=dest/'game.blend'
    old=ASSET/'renders/hatch-round3';diagnostics=ASSET/'renders/hatch-round3-diagnostics'
    dest.mkdir(parents=True,exist_ok=True)
    prefix=[blender,'-t','1','-b','--factory-startup','--python-exit-code','1','--python']
    if not model.exists():
        source=dest/'source';source.mkdir(exist_ok=True)
        archive=subprocess.check_output(['git','archive','da466e3','cars/src','kit'],cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(source,filter='data')
        subprocess.run(prefix+[str(source/'cars/src/hatch_build.py'),'--','--quality','game','--out',str(model)],cwd=ROOT,check=True)
    if model_only:return old,diagnostics
    cameras=ASSET/'build/hatch/cameras.json'
    def render(script,out,mode,names):
        metadata=out/('round4-shots.json' if script=='hatch_round4_render.py' else 'shots.json')
        shots=json.loads(metadata.read_text()) if metadata.exists() else {}
        digest=hashlib.sha256(model.read_bytes()).hexdigest()
        if all((out/(n+'.png')).exists() and shots.get(n,{}).get('source_sha256')==digest and shots[n]['width']>=width for n in names):return
        command=[blender,'-b','--factory-startup','--python-exit-code','1','--python',str(ASSET/'src'/script),'--',
            '--source',str(model),'--out',str(out),'--mode',mode,'--width',str(width),'--samples',str(samples),'--cameras',str(cameras)]
        if mode!='curvature':command.insert(0,str(ROOT/'kit/with_gpu.sh'))
        subprocess.run(command,cwd=ROOT,check=True)
    matte=VIEWS+['top','side_raking']
    stripes=['stripes_'+n for n in ['horizontal','vertical','rear_horizontal','rear_vertical','side_horizontal','side_vertical','hood_driver','rear_unpainted']]
    for mode,names in [('clay',matte),('stripes',stripes),('pairs',PAIRS),('comparisons',[n+'_clay' for n in PAIRS])]:
        render('hatch_render.py',old,mode,names)
    for mode,names in [('curvature',VIEWS),('map-stripes',VIEWS),('gloss',[n for n in VIEWS if n!='front']+PAIRS)]:
        render('hatch_round4_render.py',diagnostics,mode,[mode.replace('-','_')+'_'+n for n in names])
    return old,diagnostics


def panel(images,labels,path,width=1600):
    h=max(round(im.height*width/im.width) for im in images)
    canvas=Image.new('RGB',(width*len(images),h+75),(229,231,232));d=ImageDraw.Draw(canvas)
    for i,(im,label) in enumerate(zip(images,labels)):
        im=ImageOps.contain(im,(width,h),Image.Resampling.LANCZOS)
        canvas.paste(im,(i*width+(width-im.width)//2,75+(h-im.height)//2))
        d.text((i*width+22,20),label,font=font(25),fill=(30,45,55))
    save(canvas,path)


def prepare(out,cameras):
    """Same resolution/color treatment for both rounds; never reshape a car."""
    shots={}
    for file in ['shots.json','round4-shots.json']:
        if (out/file).exists():shots.update(json.loads((out/file).read_text()))
    tone={}
    for name in shots:
        path=out/(name+'.png');save(rgb(path),out/(name+'.jpg'))
        if name.startswith('gloss'):
            a=np.array(Image.open(path).convert('RGBA'));c=a[...,:3][a[...,3]>250];y=c@np.array([.2126,.7152,.0722])
            tone[name]=dict(display_luma_p1_p50_p99=np.percentile(y,[1,50,99]).tolist(),clipped_channel_fraction=float(np.mean(c.max(axis=1)==255)),deep_shadow_fraction=float(np.mean(y<25)))
    if tone:(out/'gloss-tonal-range.json').write_text(json.dumps(tone,indent=2))
    from kit.photo_match import compose
    for prefix,suffix,title in [('', '', 'stripes'),('', '_clay','matte clay'),('gloss_','','gloss clay')]:
        data={prefix+n+suffix:dict(r,title='Alder H120 / '+n.replace('_',' ')+' / '+title) for n,r in json.loads(cameras.read_text()).items() if prefix+n+suffix in shots}
        if not data:continue
        calibration=out/(title.replace(' ','-')+'-cameras.json');calibration.write_text(json.dumps(data,indent=2));compose(calibration,out,out)
    return shots


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--cameras',required=True)
    p.add_argument('--blender',default='blender');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=40)
    p.add_argument('--baseline-only',action='store_true');p.add_argument('--baseline-model-only',action='store_true');a=p.parse_args()
    old,diagnostics=baseline(a.blender,a.width,a.samples,a.baseline_model_only)
    if a.baseline_only or a.baseline_model_only:return
    out=Path(a.renders).resolve();cameras=Path(a.cameras).resolve()
    before=prepare(old,cameras);before.update(prepare(diagnostics,cameras));after=prepare(out,cameras)
    if len({r['source_sha256'] for r in after.values()})!=1:raise ValueError('Mixed round-four source revisions')
    paths=[];records={}
    for name,shot in after.items():
        if name not in before:continue
        if any(before[name].get(k)!=shot.get(k) for k in ['location','target','lens','ortho','aspect','roll']):raise ValueError('Changed camera: '+name)
        is_pair=any(n in name for n in PAIRS);suffix='-pair.jpg' if is_pair else '.jpg'
        folder=diagnostics if name.startswith(('curvature_','map_stripes_','gloss_')) else old
        path=out/('round3-round4-'+name+'.jpg')
        panel([rgb(folder/(name+suffix)),rgb(out/(name+suffix))],['ROUND 3 / '+name,'ROUND 4 / '+name],path)
        paths.append(path);records[name]=dict(camera_unchanged=True,before_sha256=before[name]['source_sha256'],after_sha256=shot['source_sha256'])
    for name in VIEWS:
        path=out/('curvature-stripes-'+name+'.jpg')
        panel([rgb(out/('curvature_'+name+'.png')),rgb(out/('map_stripes_'+name+'.png'))],
            ['SIGNED MEAN CURVATURE / '+name,'SAME CAMERA / horizontal reflections'],path)
        im=Image.open(path);canvas=Image.new('RGB',(im.width,im.height+75),(229,231,232));canvas.paste(im,(0,0));d=ImageDraw.Draw(canvas)
        d.text((25,im.height+16),'Blue: concave / green: flat / red: convex. asinh scale, +/-40 m^-1. Gray: cut boundaries or unmeasured inserts. No smoothing.',font=font(24),fill=(30,45,55));save(canvas,path);paths.append(path)
    paths += [out/('gloss_'+n+'-pair.jpg') for n in PAIRS]
    paths += [out/('gloss_'+n+'.jpg') for n in ['side','front_three_quarter','rear_three_quarter','rear']]
    tw,th=800,440;canvas=Image.new('RGB',(3*tw,th*math.ceil(len(paths)/3)),(229,231,232));d=ImageDraw.Draw(canvas)
    for i,path in enumerate(paths):
        im=ImageOps.contain(Image.open(path),(tw-16,th-45));x=i%3*tw;y=i//3*th
        canvas.paste(im,(x+(tw-im.width)//2,y+42));d.text((x+12,y+7),path.stem,font=font(16),fill=(30,45,55))
    save(canvas,out/'round4-contact.jpg');(out/'round3-round4.json').write_text(json.dumps(records,indent=2))
    print('ROUND 4 REVIEW',len(records),'unchanged cameras;',len(paths),'contact views')


if __name__=='__main__':main()
