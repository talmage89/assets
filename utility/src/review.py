"""Baked-export checkpoint evidence, value checks and local contact sheets."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from kit.contact import contact,review_sheet
from plan import PROFILES
from deliver import bundle


def balance():
    from photo_matches import balance_photos
    balance_photos()
    rows=json.loads(Path('build/reference-balance/balance.json').read_text())
    Path('build/reference-balance.json').write_text(json.dumps(dict(photos=rows,scope='Inspection copies only; pairs retain photographed colors. Hardware neutral rejected; hue not used as a color target.'),indent=2))


def main(a):
    files=sorted(a.renders.glob('*/*.png'));assert len(files)==22,(len(files),files)
    recipe=hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('render.py','ribbon.py'))).hexdigest()
    for p in files:
        receipts=json.loads((p.parent/'provenance.json').read_text());r=receipts[p.stem]
        assert r['sha256']==bundle(r['source']),p
        assert r['recipe_sha256']==recipe,p
    captions={str(p):f'Seed {p.parent.name} / {p.stem.replace("_"," ")}' for p in files}
    contact(files,a.renders/'contact.jpg',title='Utility / baked shared atlas / 22 Cycles views',captions=captions)
    towns={str(a.renders/str(s)/v):f'{s} / {PROFILES[s]["town"]} / {Path(v).stem}' for s in (101,102,103,104) for v in ('street.png','above.png')}
    contact(list(towns),a.renders/'four-streets.jpg',title='Four utility towns / street and above',captions=towns)
    details=[a.renders/'101'/f'{n}.png' for n in ('transformer','crossarm','deadend','anchor','communication','service','base','tags')]+[a.renders/'103/bank.png',a.renders/'103/riser.png']
    contact(details,a.renders/'construction.jpg',title='Construction and service age / exported baked utilities',captions=captions)
    review_sheet([[a.renders/'101/distance.png',a.renders/'101/distance_filtered.png']],a.renders/'wire-distance.jpg',title='True-diameter tubes / camera-facing .85px coverage-compensated ribbons')
    pairs=[Path('renders/matches')/(n+'-pair.jpg') for n in ('nc_street','md_top','comm_space')]
    if all(p.exists() for p in pairs):
        receipts=json.loads(Path('renders/matches/provenance.json').read_text())
        for name in ('nc_street','md_top','comm_space'):
            r=receipts[name];assert r['sha256']==bundle(r['source']);assert r['recipe_sha256']==recipe
        review_sheet([[p] for p in pairs],a.renders/'matched-pairs.jpg',title='Matched-light local fits / estimated cameras / exported asset at left')
    im=np.asarray(Image.open(a.renders/'101/hero.png').convert('RGB'),float)/255
    # The lower image crop includes buildings, paving, poles and lawns; it is
    # not misrepresented as a segmented utility-only albedo measurement.
    foreground=im[round(im.shape[0]*.44):];Y=foreground@np.array([.2126,.7152,.0722])
    tonal=dict(scope='Lower 56% of displayed hero, including context; encoded Rec.709 Y prime, not albedo',
               percentiles=dict(zip(('p1','p10','p50','p95','p99'),map(float,np.quantile(Y,[.01,.1,.5,.95,.99])))),
               white_clip_fraction=float(np.mean(np.min(foreground,axis=2)>.99)))
    Path('build/hero-tones.json').write_text(json.dumps(tonal,indent=2));balance()
    extras=[Path('renders/final-eevee/101/hero.png')]
    manifest=[dict(path=str(p),pixels=list(Image.open(p).size),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files+extras if p.exists()]
    Path('build/image-manifest.json').write_text(json.dumps(dict(native_images=manifest,tonal=tonal),indent=2))
    print('REVIEW',len(files),'current Cycles images;',json.dumps(tonal))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/checkpoint'));main(p.parse_args())
