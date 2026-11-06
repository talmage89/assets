"""Rebuild the accepted old checkpoint locally, then fixed-camera crops.

The historical source is our own Git code. The scratch tree never modifies
another worktree or neighboring delivery. No comparison image is committed.
"""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE='b983dbe'
SHOTS=('hero','base','tags','transformer','crossarm','communication','deadend','anchor','distance','matched_top')


def run(cmd,cwd,log):
    with log.open('w') as file:subprocess.run(cmd,cwd=cwd,stdout=file,stderr=subprocess.STDOUT,check=True)


def main(width,samples,prepare_only=False):
    repo=ASSET/'build/baseline-repo';stage=repo/'utility';(stage/'src').mkdir(parents=True,exist_ok=True)
    files=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'utility/src'],cwd=ROOT,text=True).splitlines()
    for name in files:
        p=repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT))
    for name in ('kit','houses','ground','trees','cars','street-light'):
        p=repo/name
        if not p.exists():p.symlink_to(ROOT/name,target_is_directory=True)
    (stage/'build').mkdir(exist_ok=True)
    # Historical --camera-file selected overcast for the MD form pair. These
    # are ordinary old checkpoint views with current fixed cameras, so retain
    # that checkpoint's own ordinary sun/sky instead of its MD special case.
    p=stage/'src/render.py';text=p.read_text().replace('overcast=bool(a.camera_file and seed==101)','overcast=False');p.write_text(text)
    blender=os.environ.get('BLENDER','blender');bp=[blender,'-b','-t','4','--factory-startup','--python-exit-code','1']
    old_recipe=stage/'build/source.recipe'
    if not old_recipe.exists() or old_recipe.read_text()!=BASE or not (stage/'build/utility.glb').exists():
        run(['python3','src/context.py'],stage,ASSET/'build/before-context.log')
        run([*bp,'--python','src/build.py','--','--out','build/utility.blend'],stage,ASSET/'build/before-model.log')
        old_recipe.write_text(BASE)
    if prepare_only:return
    receipts=json.loads(Path('renders/final/101/provenance.json').read_text());cameras={n:dict(seed=101,shot=receipts[n]['camera']) for n in SHOTS if n!='matched_top'}
    cameras['matched_top']=dict(seed=101,shot=json.loads(Path('renders/matches/provenance.json').read_text())['md_top']['camera'])
    camera_file=ASSET/'build/comparison-cameras.json';camera_file.write_text(json.dumps(cameras,indent=2))
    recipe=hashlib.sha256((BASE+str(width)+str(samples)).encode()+camera_file.read_bytes()+p.read_bytes()).hexdigest()
    stamp=stage/'build/comparison.recipe';out=ASSET/'renders/before'
    if not stamp.exists() or stamp.read_text()!=recipe or any(not (out/(n+'.png')).exists() for n in SHOTS):
        run([str(ROOT/'kit/with_gpu.sh'),*bp,'--python','src/render.py','--','--out',str(out),'--seeds','101','--camera-file',str(camera_file),'--width',str(width),'--samples',str(samples)],stage,ASSET/'build/before-render.log')
        stamp.write_text(recipe)
    folder=Path('renders/fixes');folder.mkdir(parents=True,exist_ok=True);rows=[]
    fixes=[('wire-value-count','hero',(.0,.0,1,.58)),('town-setting','hero',(0,.38,1,1)),
           ('wood-ground','base',(.18,.04,.90,.98)),('tags-scars','tags',(.12,.02,.94,.98)),('transformer-zinc-paint','transformer',(.12,.04,.94,.96)),
           ('fir-insulators','crossarm',(.03,.04,.97,.92)),('communication-routes','communication',(.02,.04,.98,.96)),
           ('guard-anchor-age','anchor',(0,0,1,1)),('deadend-cables','deadend',(0,0,1,1)),('wire-distance','distance',(0,0,1,.76)),('matched-light','matched_top',(.03,.02,.97,.98))]
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),21)
    for name,shot,fraction in fixes:
        a=Image.open(out/(shot+'.png')).convert('RGB');b=Image.open(Path('renders/matches/md_top.png') if shot=='matched_top' else Path('renders/final/101')/(shot+'.png')).convert('RGB');assert a.size==b.size
        box=tuple(round(v*a.size[i%2]) for i,v in enumerate(fraction));a=a.crop(box);b=b.crop(box);assert a.width>=800,(name,a.size)
        for label,im in (('before',a),('after',b)):im.save(folder/(name+'-'+label+'.png'))
        sheet=Image.new('RGB',(a.width+b.width+24,max(a.height,b.height)+96),(235,235,231));draw=ImageDraw.Draw(sheet)
        draw.text((12,8),name+' / native pixels / fixed camera',font=font,fill=(24,29,24));draw.text((12,43),'Before: accepted construction checkpoint',font=font,fill=(24,29,24));draw.text((a.width+24,43),'After: exported shared-atlas delivery',font=font,fill=(24,29,24))
        sheet.paste(a,(0,90));sheet.paste(b,(a.width+24,90));path=folder/(name+'-before-after.jpg');sheet.save(path,quality=95)
        rows.append(dict(fix=name,shot=shot,crop_native_px=box,each_panel_px=list(a.size),sheet=str(path)))
    (folder/'comparison.json').write_text(json.dumps(dict(historical_source=BASE,fixed_cameras=str(camera_file.relative_to(ASSET)),
      baseline_light='Historical ordinary checkpoint sun/sky; current cameras. The overcast MD-pair special case is disabled in the scratch source.',rows=rows),indent=2))
    print('NATIVE BEFORE/AFTER',len(rows),'pairs; each panel at least 800 pixels wide')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=64);p.add_argument('--prepare-only',action='store_true');a=p.parse_args();main(a.width,a.samples,a.prepare_only)
