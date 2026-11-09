"""Bounded final gallery, gated by exported captures and the reviewed recipe."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import presentation_check


def recipe():
    files=[*Path('src').glob('*.py'),Path('src/tangent_rounding.json')]
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)
            if p.name not in ('delivery.py','repeat.py','texture_repeat.py','last_evidence.py')}


def encode(paths,out,cols=1,width=1600):
    cell=width//cols;height=round(cell*2/3)+26;rows=(len(paths)+cols-1)//cols
    canvas=Image.new('RGB',(width,height*rows),(227,228,222));draw=ImageDraw.Draw(canvas)
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGB');im.thumbnail((cell,height-26),Image.Resampling.LANCZOS)
        x=i%cols*cell;y=i//cols*height
        canvas.paste(im,(x+(cell-im.width)//2,y+26));draw.text((x+10,y+8),p.parent.name+' / '+p.stem,fill=(22,28,23))
    if len(paths)==1:canvas=Image.open(paths[0]).convert('RGB');canvas.thumbnail((width,1600),Image.Resampling.LANCZOS)
    out.parent.mkdir(parents=True,exist_ok=True)
    for quality in range(92,39,-3):
        canvas.save(out,quality=quality,optimize=True,progressive=True,subsampling=0)
        if out.stat().st_size<=200000:break
    assert canvas.width<=1600 and out.stat().st_size<=200000,out
    return dict(file=str(out),bytes=out.stat().st_size,size=canvas.size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),inputs=[str(p) for p in paths])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--record-review',action='store_true');a=ap.parse_args()
    stamp=Path('src/final_review.json')
    if a.record_review:
        stamp.write_text(json.dumps(dict(recipe=recipe(),review='Final review J; all exported frames opened at native size before gallery encoding'),indent=2)+'\n');return
    assert stamp.exists() and json.loads(stamp.read_text())['recipe']==recipe(),'Current recipe needs full-size visual review'
    presentation_check.main(require_before=Path('renders/before-look').exists())
    f=Path('renders/final');rows=[]
    for seed in (101,202):rows.append(encode([f/str(seed)/'hero.png'],Path(f'docs/hero-{seed}.jpg')))
    rows.append(encode([f/str(s)/'above.png' for s in (101,202)],Path('docs/places.jpg'),2))
    rows.append(encode([f/str(s)/(n+'.png') for s,n in ((101,'doors'),(101,'window'),(101,'window_dusk'),(202,'doors'),(202,'window'),(202,'window_dusk'))],Path('docs/glass-entry.jpg'),3))
    rows.append(encode([f/'range.png',Path('renders/modules/contact.jpg'),f/'101/tower.png',f/'202/wing.png',f/'101/sign.png',Path('renders/eevee/202/hero.png')],Path('docs/kit.jpg'),3))
    Path('build/delivery.json').write_text(json.dumps(dict(passed=True,gallery=rows,frames=json.loads(Path('build/presentation-check.json').read_text())['images']),indent=2))
    print('PASS five final gallery JPGs:',[(r['file'],r['bytes']) for r in rows])


if __name__=='__main__':main()
