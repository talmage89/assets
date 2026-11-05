"""Fixed, annotated display-value and wear-variation patches in fitted pairs.

Photos are measurement-only, balanced before measurement. The 4/8% thresholds
measure projected visible variation relative to a clean p85, not physical oil
area; aggregate, repairs, unknown exposure and residual shadows limit it.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
CASES={
 'period_asphalt':dict(pair='period_lot',render_box=(.50,.88,.98,.98),photo_box=(.72,.86,.98,.98),material='Asphalt',surface='Sunlit asphalt, omitting the photographs tree shadows, cars and curb'),
 'shaded_walk':dict(pair='period_walk',render_box=(.54,.715,.62,.73),photo_box=(.43421,.648,.46053,.65867),material='CommercialConcrete',surface='Shaded covered concrete walk, away from column bases; ray-verified before accepting'),
}


def patch(image,box,path):
    a=np.asarray(image.convert('RGB'),dtype=float)/255;h,w=a.shape[:2];x0,y0,x1,y1=[round(v*(w if i%2==0 else h)) for i,v in enumerate(box)];mask=np.zeros((h,w),bool);mask[y0:y1,x0:x1]=True
    y=a@np.array([.2126,.7152,.0722]);vals=y[mask];clean=float(np.percentile(vals,85));rows={}
    for t in (.04,.08):
        hit=vals<clean*(1-t);rows[str(t)]=dict(coverage_fraction=float(hit.mean()),median_contrast=float(1-np.median(vals[hit])/clean) if hit.any() else 0)
    selected=mask&(y<clean*.96);out=a.copy();out[~mask]*=.22;out[selected]=out[selected]*.5+np.array([.82,.19,.07])*.5
    Image.fromarray(np.uint8(np.clip(out,0,1)*255+.5)).save(path)
    return dict(median_Yprime=float(np.median(vals)),clean_Yprime_p85=clean,pixels=len(vals),thresholds=rows,box_fraction=box)


def run(folder=Path('renders/strip/matches')):
    cal=json.loads(Path('build/strip/cameras.json').read_text());out=Path('renders/strip/measurements');out.mkdir(parents=True,exist_ok=True);rows={}
    for name,case in CASES.items():
        row=cal[case['pair']];im=Image.open(folder/(case['pair']+'.png')).convert('RGB');im=im.resize((1440,round(1440/row['shot']['aspect'])),Image.Resampling.LANCZOS);photo=Image.open(row['photo']).convert('RGB').crop(row['crop']).resize(im.size,Image.Resampling.LANCZOS)
        rows[name]=dict(**case,render=patch(im,case['render_box'],out/(name+'-render-mask.png')),photo=patch(photo,case['photo_box'],out/(name+'-photo-mask.png')),render_sha256=hashlib.sha256((folder/(case['pair']+'.png')).read_bytes()).hexdigest())
    (out/'wear-values.json').write_text(json.dumps(dict(rows=rows,neutral_balance=json.loads(Path('build/strip/references/balance.json').read_text()),scope=__doc__),indent=2)+'\n')
    print(json.dumps(rows,indent=2))

if __name__=='__main__':run()
