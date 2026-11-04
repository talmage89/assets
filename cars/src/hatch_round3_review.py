"""Same-camera round-two/three comparisons; display resize, no silhouette fit."""
import argparse,io,json,math,subprocess,tarfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from hatch_review import ROOT,ASSET,font,rgb,save


def ensure_baseline(out,blender):
    """Recover missing comparisons from our own accepted source history."""
    names=['front','rear','front_three_quarter','rear_three_quarter','side_raking',
           'stripes_horizontal','stripes_vertical','stripes_rear_horizontal','stripes_rear_vertical',
           'stripes_side_horizontal','stripes_side_vertical']
    pairs=[make+'_'+view for make in ['corolla','hyundai'] for view in ['front','rear','side']]
    needed=[n+'.jpg' for n in names]+[n+s+'-pair.jpg' for n in pairs for s in ['','_clay']]
    if (out/'shots.json').exists() and all((out/n).exists() for n in needed):return
    dest=ASSET/'build/hatch-round2-baseline';source=dest/'source';source.mkdir(parents=True,exist_ok=True)
    archive=subprocess.check_output(['git','archive','082ca31','cars/src','kit'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(source,filter='data')
    prefix=[blender,'-t','1','-b','--factory-startup','--python-exit-code','1','--python']
    model=dest/'game.blend'
    for script,args in [('hatch_build.py',['--quality','game','--out',str(model)]),
                        ('hatch_check.py',['--source',str(model),'--out',str(dest/'form-check.json')])]:
        subprocess.run(prefix+[str(source/'cars/src'/script),'--']+args,cwd=ROOT,check=True)
    out.mkdir(parents=True,exist_ok=True)
    cameras=ASSET/'build/hatch/cameras.json'
    for mode in ['clay','stripes','pairs','comparisons']:
        subprocess.run([str(ROOT/'kit/with_gpu.sh'),blender,'-b','--factory-startup','--python-exit-code','1',
                        '--python',str(source/'cars/src/hatch_render.py'),'--','--source',str(model),
                        '--out',str(out),'--mode',mode,'--width','1600','--samples','40','--cameras',str(cameras)],cwd=ROOT,check=True)
    shots=json.loads((out/'shots.json').read_text())
    for name in shots:save(rgb(out/(name+'.png')),out/(name+'.jpg'))
    from kit.photo_match import compose
    compose(cameras,out,out)
    data=json.loads(cameras.read_text());clay={n+'_clay':dict(r,title=r['title'].replace('clay with stripes','neutral clay')) for n,r in data.items()}
    calibration=out/'clay-cameras.json';calibration.write_text(json.dumps(clay,indent=2));compose(calibration,out,out)
    (out/'baseline.json').write_text(json.dumps(dict(source_commit='082ca31',scope='Accepted round-two source rebuilt from local history; unchanged calibrated cameras'),indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--baseline',required=True);p.add_argument('--blender',default='blender')
    a=p.parse_args();out=Path(a.renders).resolve();old=Path(a.baseline).resolve();ensure_baseline(old,a.blender)
    before=json.loads((old/'shots.json').read_text());after=json.loads((out/'shots.json').read_text())
    names=['front','rear','front_three_quarter','rear_three_quarter','side_raking',
           'stripes_horizontal','stripes_vertical','stripes_rear_horizontal','stripes_rear_vertical',
           'stripes_side_horizontal','stripes_side_vertical']
    names += [n for n in before if n in after and ('corolla' in n or 'hyundai' in n)]
    records={};paths=[]
    for name in names:
        keys=['location','target','lens','ortho','aspect','roll']
        if any(before[name].get(k)!=after[name].get(k) for k in keys):
            raise ValueError('Changed camera: '+name)
        suffix='-pair.jpg' if 'corolla' in name or 'hyundai' in name else '.jpg'
        left,right=[rgb(folder/(name+suffix)) for folder in [old,out]]
        w=1600;h=max(round(im.height*w/im.width) for im in [left,right])
        canvas=Image.new('RGB',(w*2,h+70),(229,231,232));d=ImageDraw.Draw(canvas)
        for i,im in enumerate([left,right]):
            im=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS)
            canvas.paste(im,(i*w+(w-im.width)//2,70))
            d.text((i*w+25,18),('ROUND 2' if i==0 else 'ROUND 3')+' / '+name,font=font(27),fill=(30,45,55))
        path=out/('round2-round3-'+name+'.jpg');save(canvas,path);paths.append(path)
        records[name]=dict(camera_unchanged=True,before_sha256=before[name]['source_sha256'],after_sha256=after[name]['source_sha256'])
    tw,th=1200,460;canvas=Image.new('RGB',(tw*2,th*math.ceil(len(paths)/2)),(229,231,232));d=ImageDraw.Draw(canvas)
    for i,path in enumerate(paths):
        im=ImageOps.contain(Image.open(path),(tw-20,th-40));x=i%2*tw;y=i//2*th
        canvas.paste(im,(x+(tw-im.width)//2,y+35));d.text((x+12,y+5),path.stem,font=font(18),fill=(30,45,55))
    save(canvas,out/'round2-round3-contact.jpg');(out/'round2-round3.json').write_text(json.dumps(records,indent=2))
    print('Same-camera comparisons:',len(paths))


if __name__=='__main__':main()
