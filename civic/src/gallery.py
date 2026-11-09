"""Five bounded gallery JPGs, after the final native-size review is recorded."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw


def recipe():
    excluded={'gallery.py','texture_repeat.py','repeat.py','compare.py','resources.py','review.py'}
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('src').glob('*.py')) if p.name not in excluded}


def encode(paths,target,cols=1):
    cell=1600//cols;h=round(cell*.68)+28
    canvas=Image.new('RGB',(1600,h*((len(paths)+cols-1)//cols)),(226,228,221));draw=ImageDraw.Draw(canvas)
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGB');im.thumbnail((cell,h-28),Image.Resampling.LANCZOS)
        x=i%cols*cell;y=i//cols*h
        canvas.paste(im,(x+(cell-im.width)//2,y+28));draw.text((x+10,y+8),p.parent.name+' / '+p.stem,fill=(24,30,25))
    if len(paths)==1:
        canvas=Image.open(paths[0]).convert('RGB');canvas.thumbnail((1600,1600),Image.Resampling.LANCZOS)
    target.parent.mkdir(exist_ok=True)
    for quality in range(93,30,-3):
        canvas.save(target,quality=quality,optimize=True,progressive=True,subsampling=0)
        if target.stat().st_size<=200000:break
    assert canvas.width<=1600 and target.stat().st_size<=200000,target
    return dict(file=str(target),bytes=target.stat().st_size,size=canvas.size,inputs=[str(p) for p in paths],sha256=hashlib.sha256(target.read_bytes()).hexdigest())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--record-review',action='store_true');args=ap.parse_args()
    stamp=Path('src/final_review.json')
    if args.record_review:
        stamp.write_text(json.dumps(dict(recipe=recipe(),review='Passes 15 and 16; every final and pair opened at native size; partial corrections listed in README Known flaws'),indent=2)+'\n');return
    assert json.loads(stamp.read_text())['recipe']==recipe(),'Review current full-size exports before gallery encoding'
    from review import main as review
    review();f=Path('renders/final');rows=[]
    for seed in (101,202):rows.append(encode([f/str(seed)/'hero.png'],Path(f'docs/hero-{seed}.jpg')))
    rows.append(encode([f/str(s)/'above.png' for s in (101,202)],Path('docs/places.jpg'),2))
    rows.append(encode([f/str(s)/(n+'.png') for s,n in ((101,'entry'),(101,'cornice'),(101,'flag'),(101,'police'),(202,'bays'),(202,'scupper'))],Path('docs/details.jpg'),3))
    rows.append(encode([f/'range.png',f/'modules.png',f/'scale.png',f/'202/interior.png',f/'202/tower.png',Path('renders/eevee/202/hero.png')],Path('docs/kit.jpg'),3))
    Path('build/gallery.json').write_text(json.dumps(dict(passed=True,images=rows),indent=2)+'\n')
    print('CIVIC GALLERY PASS',[(r['file'],r['bytes']) for r in rows])


if __name__=='__main__':main()
