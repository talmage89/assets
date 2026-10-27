"""Final contacts, small portfolio JPGs, bundle provenance and tonal evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from delivery_io import bundle_hash
from plan import PROOF_SEEDS
FONT=find_font('Noto Sans','Regular')


def photo_sheets(folder):
    review_sheet([[folder/(n+'-pair.jpg')] for n in ('colonial_1991_oh','colonial_rog_ri','colonial_2003_nh')],
        folder/'pairs.jpg',width=2200,title='Exported baked houses / calibrated photographs / original crop cameras')


def main(a):
    folder=Path('renders/final');folder.mkdir(parents=True,exist_ok=True)
    seeds=list(dict.fromkeys(map(int,a.seeds.split(','))))
    contact([folder/(n+'.png') for n in ('front','side','rear','top')],folder/'turnaround.jpg',width=2200,title='Hearthfield / exported glTF / front, side, rear and top')
    contact([folder/(n+'.png') for n in ('eave','window','entry_closed','entry')],folder/'details.jpg',width=2400,title='Shared baked maps / eave, window, faded entry and shallow foyer')
    cell=600;h=375;top=82;sheet=Image.new('RGB',(cell*len(seeds),top+2*(h+50)),(225,229,224));d=ImageDraw.Draw(sheet)
    d.text((20,18),'Independent seeded houses / one shared family texture directory',font=ImageFont.truetype(FONT,28),fill=(23,35,27))
    for i,seed in enumerate(seeds):
        meta=json.loads(Path(f'export/Hearthfield-{seed}.json').read_text())
        for j,shot in enumerate(('hero','back')):
            im=Image.open(f'renders/final-seeds/{seed}/{shot}.png').convert('RGB');im=ImageOps.contain(im,(cell,h));sheet.paste(im,(i*cell,top+j*(h+50)))
            label=f"{seed} / {meta['spec']['main']['roof']} / {meta['triangles']:,} tris" if j==0 else f"{meta['spec']['rear_landing']} / {meta['spec']['shingle_color']}"
            d.text((i*cell+10,top+j*(h+50)+h+8),label,font=ImageFont.truetype(FONT,20),fill=(23,35,27))
    sheet.save(folder/'six-seeds.jpg',quality=94,optimize=True)
    photo_sheets(Path('renders/final-matches'))
    paths=[folder/(n+'.png') for n in ('hero','front','side','back','rear','top','eave','window','entry','entry_closed','scale','shingles')]
    paths+=[Path('renders/final-eevee/hero.png'),Path('renders/street/street.png'),folder/'six-seeds.jpg']
    contact(paths,folder/'contact.jpg',width=3000,title='Hearthfield / baked shared textures / exported asset finals')
    checked=[]
    for base in (folder,Path('renders/final-eevee'),Path('renders/final-matches'),*[Path(f'renders/final-seeds/{s}') for s in seeds]):
        rows=json.loads((base/'provenance.json').read_text())
        for name,row in rows.items():
            source=Path(row['source']);assert source.suffix=='.gltf' and bundle_hash(source)==row['sha256'],(base,name,'stale exported bundle')
            assert row['stage']=='baked game delivery; shared external images'
            assert (base/(name+'.png')).exists();checked.append(str(base/(name+'.png')))
    street=json.loads(Path('renders/street/provenance.json').read_text())
    assert street['house_bundle_sha256']==bundle_hash(Path(street['house'])) and abs(street['camera_height_m']-1.68)<1e-6
    for r in street['context']:assert hashlib.sha256(Path(r['source']).read_bytes()).hexdigest()==r['sha256']
    pixels=np.asarray(Image.open(folder/'hero.png').convert('RGB'),dtype=float)/255
    mask=np.asarray(Image.open(folder/'hero-mask.png'))>127;rgb=pixels[mask];lum=rgb@np.array([.2126,.7152,.0722])
    assert mask.sum()>10000
    tonal=dict(scope='Display luminance inside projected asset triangle union; no external occluders; not albedo',
        percentiles=dict(zip(('p1','p5','p50','p95','p99'),map(float,np.percentile(lum,[1,5,50,95,99])))),
        clipped_white_fraction=float(np.mean(np.all(rgb>=.995,axis=1))),mask_pixels=int(mask.sum()))
    assert tonal['clipped_white_fraction']<.001
    Path('build/final-view-check.json').write_text(json.dumps(dict(passed=True,views=len(checked)+1,paths=checked+['renders/street/street.png'],tonal=tonal),indent=2))
    # Exactly five final documentation JPGs, each <=1600 px and <=200 KB.
    docs=Path('docs');docs.mkdir(exist_ok=True)
    for name,path in dict(hero=folder/'hero.png',turnaround=folder/'turnaround.jpg',details=folder/'details.jpg',
                          family=folder/'six-seeds.jpg',street=Path('renders/street/street.png')).items():
        im=Image.open(path).convert('RGB');im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        dest=docs/(name+'.jpg')
        for quality in range(91,39,-4):
            im.save(dest,quality=quality,optimize=True)
            if dest.stat().st_size<=200000:break
        assert dest.stat().st_size<=200000
    print('FINAL_VIEWS',len(checked)+1,'current exported views; five docs JPGs; tonal',tonal)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=27);p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)))
    main(p.parse_args())
