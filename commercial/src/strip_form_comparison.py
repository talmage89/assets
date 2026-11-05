"""Rebuildable same-recipe before/after evidence for the three form fixes.

The before source is the accepted historical form commit, read through git;
no checkout/worktree is changed. Everything generated stays under build/.
"""
import argparse,json,os,subprocess,hashlib
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font
REPO=Path(__file__).resolve().parents[2];BASE='b3a77d8'


def run(blender='blender',width=1200,samples=24):
    before=Path('build/strip-before');after=Path('build/strip-form-fixed')
    if not all((before/f'strip-{s}.glb').exists() for s in range(201,205)):
        snapshot=Path('build/strip-look/baseline-repo/commercial/src');snapshot.mkdir(parents=True,exist_ok=True)
        files=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','commercial/src'],text=True).splitlines()
        for name in files:
            if name.endswith('.py'):(snapshot/Path(name).name).write_bytes(subprocess.check_output(['git','show',BASE+':'+name]))
        env={**os.environ,'PYTHONPATH':str(REPO)}
        with Path('build/strip-look/before-build.log').open('w') as log:subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python',str(snapshot/'strip_build.py'),'--','--out',str(before)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    form_sources=[Path('src')/('strip_'+name+'.py') for name in ('build','building','site','plan','graphics')]
    after_models=[after/f'strip-{s}.glb' for s in range(201,205)]
    if not all(p.exists() for p in after_models) or max(p.stat().st_mtime for p in form_sources)>min(p.stat().st_mtime for p in after_models):
        with Path('build/strip-look/form-fixed-build.log').open('w') as log:subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/strip_build.py','--','--out',str(after)],stdout=log,stderr=subprocess.STDOUT,check=True)
    root=Path('renders/strip/form-fixes');root.mkdir(parents=True,exist_ok=True);records=[]
    for label,folder in (('before',before),('after',after)):
        for seed in range(201,205):
            out=root/label/str(seed);shots='above,endcap,rear' if seed==201 else 'above'
            cmd=[str(REPO/'kit/with_gpu.sh'),blender,'-b','--factory-startup','--python-exit-code','1','--python','src/strip_render.py','--','--source-root',str(folder),'--out',str(out),'--seed',str(seed),'--shots',shots,'--width',str(width),'--samples',str(samples)]
            with (root/f'{label}-{seed}.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
            records.append(dict(label=label,seed=seed,source=str(folder/f'strip-{seed}.glb'),sha256=hashlib.sha256((folder/f'strip-{seed}.glb').read_bytes()).hexdigest()))
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),18)
    cases=[(f'site-{seed}',seed,'above',None) for seed in range(201,205)]+[('endcap',201,'endcap',(.12,.24,.88,.86)),('rear-landings',201,'rear',(.32,.32,.96,.92))]
    for name,seed,shot,crop in cases:
        images=[Image.open(root/label/str(seed)/(shot+'.png')).convert('RGB') for label in ('before','after')]
        if crop:
            images=[im.crop(tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(crop))) for im in images]
        w=max(im.width for im in images);h=max(im.height for im in images);sheet=Image.new('RGB',(w,h*2+60),'#e6e8e4');d=ImageDraw.Draw(sheet)
        for i,(label,im) in enumerate(zip(('Before accepted form','After form fixes'),images)):
            y=i*(h+30);d.text((8,y+4),label,font=font,fill='#29372f');sheet.paste(im,(0,y+30))
        sheet.save(root/(name+'-before-after.jpg'),quality=95,optimize=True)
    (root/'comparison.json').write_text(json.dumps(dict(baseline_commit=BASE,rows=records,width=width,samples=samples,scope='Same renderer and procedural light, original quick finishes on both sides; each lot uses the same conservative footprint framing. Detail crops retain native pixels.'),indent=2)+'\n')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--blender',default='blender');a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a=a.parse_args();run(a.blender,a.width,a.samples)
