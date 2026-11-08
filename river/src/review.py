"""Contact sheets of every actual checkpoint export view; no docs this round."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
import json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from package import bundle
from plan import Plan
from views import views


def sheet(files,out,title,columns=3):
    files=list(files);w=480;h=352
    im=Image.new('RGB',(columns*w,52+((len(files)+columns-1)//columns)*h),(32,37,34));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15);d.text((14,14),title,font=font,fill=(237,236,224))
    for i,p in enumerate(files):
        pic=Image.open(p).convert('RGB');pic.thumbnail((w-10,h-37),Image.Resampling.LANCZOS)
        x=(i%columns)*w;y=52+(i//columns)*h;im.paste(pic,(x+(w-pic.width)//2,y))
        d.text((x+8,y+h-26),str(p.parent.name)+' / '+p.stem,font=font,fill=(215,218,206))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--gate',action='store_true');a=ap.parse_args()
    files=sorted(a.folder.rglob('*.png'));sheet(files,a.folder/'contact.jpg','River / exported glTF / form and construction checkpoint')
    pairs=sorted(Path('renders/checkpoint-matches').glob('*-pair.jpg'))
    if pairs:sheet(pairs,Path('renders/checkpoint-matches/contact.jpg'),'Photo type comparisons / balanced assumed neutrals',1)
    if a.gate:
        receipt=[];cache={};plans={}
        calibration=json.loads(Path('build/photo-calibration.json').read_text())
        expected=[a.folder/str(seed)/(name+'.png') for seed in (101,202) for name in views(seed)]
        expected += [a.folder/'modules.png']+[Path('renders/checkpoint-matches')/(name+'.png') for name in calibration]
        assert all(p.is_file() for p in expected),('Missing required view',[str(p) for p in expected if not p.is_file()])
        for p in files+sorted(Path('renders/checkpoint-matches').glob('*.png')):
            meta=json.loads(p.with_suffix('.json').read_text());source=meta['source']
            if source not in cache:cache[source]=bundle(source)
            assert meta['bundle_sha256']==cache[source],('Stale export view',p)
            if p.parent.name in ('101','202'):
                seed=int(p.parent.name)
                if seed not in plans:
                    doc=json.loads(Path(source).read_text())
                    plans[seed]=Plan(**next(n['extras']['plan'] for n in doc['nodes'] if n['name']==f'Crossing_{seed}'))
                camera=views(seed,plans[seed])[p.stem]
                assert meta['camera']==json.loads(json.dumps(camera)),('Stale view camera',p)
            elif p.parent.name=='checkpoint-matches':
                assert meta['camera']==calibration[p.stem]['shot'],('Stale photo camera',p)
            pixels=np.asarray(Image.open(p).convert('RGB'),dtype=float)/255
            y=pixels@np.array([.2126,.7152,.0722]);q=np.percentile(y,[1,50,99])
            assert q[2]>.08,('Nearly black view',p,q.tolist())
            receipt.append(dict(path=str(p),display_y_p1_p50_p99=q.tolist(),source_bundle_sha256=cache[source]))
        Path('build/render-check.json').write_text(json.dumps(dict(passed=True,views=receipt),indent=2)+'\n')
    print('REVIEW_SHEET',len(files),a.folder/'contact.jpg')


if __name__=='__main__':main()
