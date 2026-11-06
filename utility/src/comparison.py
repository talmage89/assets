"""Native before/after evidence for the f824685 appearance handoff.

The immutable local receipt can be reused. If absent, our own historical Git
scripts rebuild their atlas, parts, setting and cameras in isolated scratch.
"""
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=HERE.parents[1]
BASE='f824685'


def run(cmd,cwd,log):
    with log.open('w') as f:subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)


def baseline(width,samples):
    cache=ROOT/'build/utility-look-before';required=[cache/'final/101'/f'{s}.png' for s in ('hero','base','tags','transformer','dusk')]+[cache/'matches'/f'{s}.png' for s in ('md_top','nc_street')]
    expected=hashlib.sha256(b''.join(subprocess.check_output(['git','show',BASE+':utility/src/'+n],cwd=ROOT) for n in ('render.py','ribbon.py'))).hexdigest()
    if all(p.exists() for p in required):
        for folder,names in (('final/101',('hero','base','tags','transformer','dusk')),('matches',('md_top','nc_street'))):
            receipts=json.loads((cache/folder/'provenance.json').read_text())
            assert all(receipts[n]['recipe_sha256']==expected for n in names),'Historical render recipe differs from f824685'
        return cache
    repo=ASSET/'build/baseline-repo';stage=repo/'utility'
    files=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'utility'],cwd=ROOT,text=True).splitlines()
    for name in files:
        p=repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT))
    for name in ('kit','houses','ground','trees','cars','street-light'):
        p=repo/name
        if not p.exists():p.symlink_to(ROOT/name,target_is_directory=True)
    for p in (ASSET/'refs').iterdir():
        target=stage/'refs'/p.name
        if p.is_file() and p.name!='SOURCES.md' and not target.exists():target.symlink_to(p)
    (stage/'build').mkdir(exist_ok=True)
    run(['make','export'],stage,ASSET/'build/before-build.log')
    bp=[os.environ.get('BLENDER','blender'),'-b','-t','4','--factory-startup','--python-exit-code','1']
    run([str(ROOT/'kit/with_gpu.sh'),*bp,'--python','src/render.py','--','--out','renders/final','--seeds','101','--shots','hero,base,tags,transformer,dusk','--width',str(width),'--samples',str(samples)],stage,ASSET/'build/before-render.log')
    run(['make','matches',f'WIDTH={width}',f'SAMPLES={samples}'],stage,ASSET/'build/before-matches.log')
    for folder in ('final','matches'):
        target=cache/folder;target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(stage/'renders'/folder,target,dirs_exist_ok=True)
    return cache


def main(width,samples,prepare_only=False):
    before=baseline(width,samples)
    if prepare_only:return
    import sys;sys.path.insert(0,str(ROOT));from kit.fonts import find_font
    fixes=[('wood-checks-scars','tags',(0.05,0,1,1)),('vine-removed','base',(0.12,0,1,1)),('soil-grass-wet-trimmer','base',(0.05,.20,1,1)),('tank-gray-runoff','transformer',(.1,.1,1,1)),('clear-day-sky','hero',(0,0,1,.60)),('near-hero-ground','hero',(0,0,1,1)),('dusk-gradient-pool','dusk',(0,0,1,1)),('street-plan-light','nc_street',(0,0,1,1)),('matched-wood-tank-sky','md_top',(0,0,1,1))]
    out=ASSET/'renders/fixes';out.mkdir(parents=True,exist_ok=True);rows=[];font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)
    for name,shot,fraction in fixes:
        relative=Path('matches')/(shot+'.png') if shot in ('nc_street','md_top') else Path('final/101')/(shot+'.png')
        sources=[before/relative,ASSET/'renders'/relative];ims=[];boxes=[]
        for p in sources:
            im=Image.open(p).convert('RGB');box=tuple(round(v*im.size[i%2]) for i,v in enumerate(fraction));im=im.crop(box);assert im.width>=800,(name,p,im.size)
            ims.append(im);boxes.append(box)
        for label,im in zip(('before','after'),ims):im.save(out/(name+'-'+label+'.png'))
        a,b=ims;sheet=Image.new('RGB',(a.width+b.width+24,max(a.height,b.height)+98),(235,235,231));draw=ImageDraw.Draw(sheet)
        draw.text((12,7),name+' / native pixels; no enlargement',font=font,fill=(24,29,24));draw.text((12,43),'Before: f824685 baked export',font=font,fill=(24,29,24));draw.text((a.width+24,43),'After: delivered baked export',font=font,fill=(24,29,24));sheet.paste(a,(0,94));sheet.paste(b,(a.width+24,94));path=out/(name+'-before-after.jpg');sheet.save(path,quality=95)
        rows.append(dict(fix=name,shot=shot,native_boxes=boxes,panel_pixels=[list(i.size) for i in ims],input_sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in sources],camera_policy='Hero/dusk deliberately reframed; close studies and photographic cameras retained',sheet=str(path.relative_to(ASSET))))
    (out/'comparison.json').write_text(json.dumps(dict(historical_source=BASE,rows=rows),indent=2));print('NATIVE FIX CROPS',len(rows),'pairs; all panels >=800 px wide')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=64);p.add_argument('--prepare-only',action='store_true');a=p.parse_args();main(a.width,a.samples,a.prepare_only)
