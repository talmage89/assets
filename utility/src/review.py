"""Checkpoint evidence, current-source image receipts and contact sheets."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from kit.contact import contact,review_sheet
from plan import PROFILES


def balance():
    # Assumed neutral cement in each photograph, not a gray-card calibration.
    rois={'residential-a':(184,430,215,450),'residential-b':(1800,1370,1900,1400)};report={}
    for name,roi in rois.items():
        im=Image.open('refs/'+name+'.jpg').convert('RGB');rgb=np.asarray(im).astype(float)/255
        linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
        x0,y0,x1,y1=roi;med=np.median(linear[y0:y1,x0:x1].reshape(-1,3),axis=0)
        target=float(np.mean(med));gains=target/med
        corrected=np.clip(linear*gains,0,1);encoded=np.where(corrected<=.0031308,corrected*12.92,1.055*corrected**(1/2.4)-.055)
        p=Path('build/reference-balance');p.mkdir(parents=True,exist_ok=True)
        Image.fromarray(np.uint8(encoded*255+.5)).save(p/(name+'.jpg'),quality=94)
        report[name]=dict(assumed_neutral='bare concrete sidewalk/driveway',roi_native=roi,linear_rgb_median=med.tolist(),linear_gains=gains.tolist(),
                         scope='White-balance inspection only. Photographs are not calibrated albedos; comparison pairs retain their original photographed colors.')
    Path('build/reference-balance.json').write_text(json.dumps(report,indent=2))


def main(a):
    files=sorted(a.renders.glob('*/*.png'));assert len(files)==20,(len(files),files)
    recipe=hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('render.py','ribbon.py'))).hexdigest()
    for p in files:
        receipts=json.loads((p.parent/'provenance.json').read_text());r=receipts[p.stem]
        assert r['sha256']==hashlib.sha256(Path(r['source']).read_bytes()).hexdigest(),p
        assert r['recipe_sha256']==recipe,p
    captions={str(p):f'Seed {p.parent.name} / {p.stem.replace("_"," ")}' for p in files}
    contact(files,a.renders/'contact.jpg',title='Utility / construction checkpoint / 20 Cycles views',captions=captions)
    towns={str(a.renders/str(s)/v):f'{s} / {PROFILES[s]["town"]} / {Path(v).stem}' for s in (101,102,103,104) for v in ('street.png','above.png')}
    contact(list(towns),a.renders/'four-streets.jpg',title='Four utility towns / street and above',captions=towns)
    details=[a.renders/'101'/f'{n}.png' for n in ('transformer','crossarm','deadend','anchor','communication','service','base')]+[a.renders/'103/bank.png',a.renders/'103/riser.png']
    contact(details,a.renders/'construction.jpg',title='Construction / exported quick-material utility GLBs',captions=captions)
    review_sheet([[a.renders/'101/distance.png',a.renders/'101/distance_filtered.png']],a.renders/'wire-distance.jpg',title='True-diameter tubes / camera-facing .85px coverage-compensated ribbons')
    pairs=[Path('renders/matches')/(n+'-pair.jpg') for n in ('nc_street','md_street')]
    if all(p.exists() for p in pairs):
        receipts=json.loads(Path('renders/matches/provenance.json').read_text())
        for name in ('nc_street','md_street'):
            r=receipts[name];assert r['sha256']==hashlib.sha256(Path(r['source']).read_bytes()).hexdigest();assert r['recipe_sha256']==recipe
        review_sheet([[p] for p in pairs],a.renders/'matched-pairs.jpg',title='Residential street type comparisons / estimated cameras / original asset at left')
    im=np.asarray(Image.open(a.renders/'101/hero.png').convert('RGB'),float)/255
    # The lower image crop includes buildings, paving, poles and lawns; it is
    # not misrepresented as a segmented utility-only albedo measurement.
    foreground=im[round(im.shape[0]*.44):];Y=foreground@np.array([.2126,.7152,.0722])
    tonal=dict(scope='Lower 56% of displayed hero, including context; encoded Rec.709 Y prime, not albedo',
               percentiles=dict(zip(('p1','p10','p50','p95','p99'),map(float,np.quantile(Y,[.01,.1,.5,.95,.99])))),
               white_clip_fraction=float(np.mean(np.min(foreground,axis=2)>.99)))
    Path('build/hero-tones.json').write_text(json.dumps(tonal,indent=2));balance()
    print('REVIEW',len(files),'current Cycles images;',json.dumps(tonal))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/checkpoint'));main(p.parse_args())
