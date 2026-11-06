"""Baked-export checkpoint evidence, value checks and local contact sheets."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from kit.contact import contact,review_sheet
from plan import PROFILES
from deliver import bundle


def docs(renders):
    from io import BytesIO
    from PIL import ImageOps
    folder=Path('docs');folder.mkdir(exist_ok=True);scratch=Path('build/docs');scratch.mkdir(parents=True,exist_ok=True)
    detail=[renders/'101'/f'{n}.png' for n in ('transformer','crossarm','communication','service','base','tags')]
    review_sheet([detail[i:i+2] for i in range(0,len(detail),2)],scratch/'details.jpg',width=1600,title='Rill / equipment, wood and service age')
    gallery=[Path('renders/gallery')/(n+'-front.png') for n in ('tangent-top','deadend-guy','transformer-top','bank','riser','light-bracket','crossarm','splice-case')]
    gallery += [Path('renders/gallery/scale-front.png'),Path('renders/final-eevee/101/hero.png')]
    contact(gallery,scratch/'parts.jpg',width=1600,title='Delivered parts / sections, 1.8 m scale and Eevee')
    sources={'utility-hero.jpg':renders/'101/hero.png','utility-details.jpg':scratch/'details.jpg','utility-streets.jpg':renders/'four-streets.jpg','utility-parts.jpg':scratch/'parts.jpg','utility-dusk.jpg':renders/'101/dusk.png'}
    rows=[]
    for name,source in sources.items():
        im=Image.open(source).convert('RGB');im=ImageOps.contain(im,(1600,6000))
        while True:
            for quality in range(90,34,-3):
                stream=BytesIO();im.save(stream,format='JPEG',quality=quality,optimize=True)
                if len(stream.getvalue())<=200_000:break
            else:
                im=im.resize((round(im.width*.9),round(im.height*.9)),Image.Resampling.LANCZOS);continue
            break
        path=folder/name;path.write_bytes(stream.getvalue());assert path.stat().st_size<=200_000 and im.width<=1600
        rows.append(dict(path=str(path),source=str(source),pixels=list(im.size),bytes=path.stat().st_size,quality=quality))
    Path('build/docs.json').write_text(json.dumps(rows,indent=2));print('FINAL DOCS',rows)


def balance():
    from photo_matches import balance_photos
    balance_photos()
    rows=json.loads(Path('build/reference-balance/balance.json').read_text())
    Path('build/reference-balance.json').write_text(json.dumps(dict(photos=rows,scope='Inspection copies only; pairs retain photographed colors. Hardware neutral rejected; hue not used as a color target.'),indent=2))


def main(a):
    files=sorted(a.renders.glob('*/*.png'));assert len(files)==22,(len(files),files)
    recipe=hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('render.py','ribbon.py','setting.py'))).hexdigest()
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
        joins=json.loads(Path('build/nc-corner-joins.json').read_text())['joins']
        assert len(joins)==8 and max(r['measured_maximum_endpoint_gap_m'] for r in joins)<.001
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
    wear=list(Path('renders/wear').glob('*/*.png'))
    for p in wear:
        r=json.loads((p.parent/'provenance.json').read_text())[p.stem]
        assert r['sha256']==bundle(r['source']) and r['recipe_sha256']==recipe
    extras+=wear
    gallery=sorted(Path('renders/gallery').glob('*.png'))
    if gallery:
        from gallery_views import ITEMS
        gallery_recipe=hashlib.sha256((Path(__file__).parent/'gallery.py').read_bytes()+(Path(__file__).parent/'gallery_views.py').read_bytes()).hexdigest()
        for name,(stem,root,low,high) in ITEMS.items():
            reports=json.loads(Path('renders/gallery',name+'.json').read_text())
            for r in reports.values():assert r['sha256']==bundle(r['source']) and r['recipe_sha256']==gallery_recipe
        review_sheet([[Path('renders/gallery')/(n+'-'+v+'.png') for v in ('front','side','back','top')] for n in ITEMS if n!='scale'],a.renders/'gallery.jpg',width=3200,title='Exported triangles / gallery front, side, back, top / named height sections')
        extras+=gallery
        contact(files+[Path('renders/gallery/scale-front.png'),extras[0]],a.renders/'contact.jpg',title='Utility / 22 Cycles streets and details, scale and Eevee',captions=captions)
    all_views=files+extras+sorted(Path('renders/wires').glob('*-tube.png'))+sorted(Path('renders/wires').glob('*-ribbon.png'))+sorted(Path('renders/wires').glob('*-sky.png'))
    all_views += [Path('renders/matches')/(name+'.png') for name in ('nc_street','md_top','comm_space')]
    manifest=[dict(path=str(p),pixels=list(Image.open(p).size),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in all_views]
    review_sheet([all_views[i:i+6] for i in range(0,len(all_views),6)],a.renders/'all-views.jpg',width=2400,title=f'Utility / all {len(all_views)} export, gallery, range and matched render views')
    Path('build/image-manifest.json').write_text(json.dumps(dict(native_images=manifest,tonal=tonal),indent=2))
    from color_review import main as colors
    from costs import main as costs
    colors();costs()
    if a.docs:docs(a.renders)
    print('REVIEW',len(files),'current Cycles images;',json.dumps(tonal))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/checkpoint'));p.add_argument('--docs',action='store_true');main(p.parse_args())
