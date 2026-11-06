"""Validate final external-glTF provenance, then make local contact/docs images.

Docs are opt-in after the caller has opened every full-size final. Reference
photos and book comparisons never enter committed documentation images.
"""
import argparse,hashlib,json,sys
import numpy as np
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jpg(image,path):
    image=image.convert('RGB');image.thumbnail((1600,16000),Image.Resampling.LANCZOS);path.parent.mkdir(parents=True,exist_ok=True)
    for q in range(94,35,-2):
        image.save(path,quality=q,optimize=True)
        if path.stat().st_size<=200000:break
    assert image.width<=1600 and path.stat().st_size<=200000

def grid(paths,cols=2,width=1600):
    w=width//cols;h=round(w*.75);im=Image.new('RGB',(width,h*((len(paths)+cols-1)//cols)),(220,222,216))
    for j,p in enumerate(paths):
        src=Image.open(p).convert('RGB');src=ImageOps.contain(src,(w-8,h-8),Image.Resampling.LANCZOS);im.paste(src,((j%cols)*w+(w-src.width)//2,(j//cols)*h+(h-src.height)//2))
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',type=Path,default=Path('renders/final'));ap.add_argument('--docs',action='store_true');a=ap.parse_args()
    names=['hero','lineup','signs-regulatory','signs-warning','sign-face','sign-back','post-base','pole-band','shelter-frame','bench','meter','boxes','collection','receptacles','rack','route-plate','front','side','back','top']
    paths=[a.folder/(n+'.png') for n in names]+[Path('renders/eevee/hero.png')]+[Path('renders/match')/(n+'.png') for n in ('used-shelter','used-meter','used-news','used-sign')]
    for p in paths:
        meta=json.loads(p.with_suffix('.json').read_text());assert meta['image_sha256']==sha(p),p
        assert meta['engine']==('BLENDER_EEVEE' if 'eevee' in str(p) else 'CYCLES'),p
        assert meta['recipe_sha256']==sha(Path(__file__).with_name('render.py')),p
        if meta.get('renderer_adapter_sha256'):assert meta['renderer_adapter_sha256']==sha(Path(__file__).with_name('eevee.py')),p
        for b in meta['inputs']:
            for file,h in b['files'].items():assert sha(ROOT/file)==h,(p,file)
        if meta.get('photo_calibration_sha256'):assert meta['photo_calibration_sha256']==sha('build/photo-calibration.json'),p
    rows=[[a.folder/'hero.png'],[a.folder/'lineup.png'],[a.folder/'signs-regulatory.png'],[a.folder/'signs-warning.png']]
    rows += [[a.folder/(n+'.png') for n in pair] for pair in [('sign-face','sign-back'),('post-base','pole-band'),('shelter-frame','bench'),('meter','boxes'),('collection','receptacles'),('rack','front'),('side','back'),('top',)]]
    rows += [[Path('renders/eevee/hero.png')]]+[[Path('renders/match')/(n+'-pair.jpg')] for n in ('used-shelter','used-meter','used-news','used-sign')]
    review_sheet(rows,a.folder/'contact.jpg',width=1800,title='Rill street furniture and 2009 sign set / exported PBR glTF')
    receipt=dict(passed=True,views=[str(p) for p in paths],scope='Image bytes, current render recipe and actual external-glTF bundle hashes; appearance is separately recorded in REVIEW.md')
    if a.docs:
        jpg(Image.open(a.folder/'hero.png'),Path('docs/furniture-hero.jpg'))
        jpg(Image.open(a.folder/'lineup.png'),Path('docs/furniture-lineup.jpg'))
        jpg(grid([a.folder/(n+'.png') for n in ('shelter-frame','bench','rack','receptacles')]),Path('docs/furniture-construction.jpg'))
        jpg(grid([a.folder/(n+'.png') for n in ('meter','boxes','collection')]),Path('docs/furniture-mechanisms.jpg'))
        # The three accepted STOP/blade JPGs stay byte-identical. Two additions
        # keep the whole street-signs family within its five-JPG ceiling.
        jpg(grid([a.folder/(n+'.png') for n in ('hero','sign-face','sign-back','post-base')]),ROOT/'street-signs/docs/set-street.jpg')
        jpg(grid([a.folder/'signs-regulatory.png',a.folder/'signs-warning.png'],cols=1),ROOT/'street-signs/docs/set-lineup.jpg')
        receipt['docs']={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=sha(p)) for d in (Path('docs').resolve(),ROOT/'street-signs/docs') for p in sorted(d.glob('*.jpg'))}
    Path('build/view-check.json').write_text(json.dumps(receipt,indent=2));print('FINAL VIEWS VALIDATED',len(paths),'docs',a.docs)
    hero=np.asarray(Image.open(a.folder/'hero.png').convert('RGB')).astype(float)/255;lum=hero@np.array([.2126,.7152,.0722]);tonal=dict(hero_srgb_luminance_percentiles={str(p):float(np.percentile(lum,p)) for p in (1,5,50,95,99)},hero_share_max_channel_at_least_254=float((hero.max(axis=2)>=254/255).mean()),hero_share_luminance_below_005=float((lum<.05).mean()),scope='Display-referred final PNG luminance, not linear albedo. Full-size visual audit is separate.')
    Path('build/hero-range.json').write_text(json.dumps(tonal,indent=2))
if __name__=='__main__':main()
