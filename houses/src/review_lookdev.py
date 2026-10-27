"""Ignored source-checkpoint contacts, all-view provenance and tonal evidence."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from plan import PROOF_SEEDS
FONT=find_font('Noto Sans','Regular')


def main():
    folder=Path('renders/lookdev');matches=Path('renders/lookdev-matches')
    names=['hero','back','eave','window','entry','entry_closed','shingles','side','scale','roof']
    contact([folder/(n+'.png') for n in names],folder/'contact.jpg',width=2400,
        title='Hearthfield / source look development / Cycles / before bake')
    w=3600;cell=w//6;h=round(cell/1.6);top=84
    sheet=Image.new('RGB',(w,top+2*(h+50)),(232,235,230));d=ImageDraw.Draw(sheet)
    d.text((20,15),'Six independent sources / same fifteen family images / front and rear',font=ImageFont.truetype(FONT,29),fill=(22,36,29))
    for i,seed in enumerate(PROOF_SEEDS):
        meta=json.loads(Path(f'build/lookdev-seeds/house-{seed}.json').read_text())
        for j,shot in enumerate(('hero','back')):
            im=Image.open(f'renders/lookdev-seeds/{seed}/{shot}.png').convert('RGB');im=ImageOps.contain(im,(cell,h))
            sheet.paste(im,(i*cell,top+j*(h+50)))
            label=f"{seed} / {meta['spec']['main']['roof']} / {meta['spec']['rear_landing']} / {meta['triangles']:,} tris" if j==0 else f"rear / fireplace: {meta['spec']['fireplace']}"
            d.text((i*cell+10,top+j*(h+50)+h+8),label,font=ImageFont.truetype(FONT,19),fill=(22,36,29))
    sheet.save(folder/'six-seeds.jpg',quality=94,optimize=True)
    review_sheet([[folder/'hero.png'],[folder/'back.png'],[folder/'window.png',folder/'eave.png'],
        [folder/'entry.png',folder/'entry_closed.png'],[folder/'shingles.png'],
        *[[matches/(n+'-pair.jpg')] for n in ('colonial_1991_oh','colonial_rog_ri','colonial_2003_nh')]],
        folder/'review-sheet.jpg',width=2400,title='Source materials / causal age / calibrated house photographs')
    image=np.asarray(Image.open(folder/'hero.png').convert('RGB'),dtype=float)/255
    mask=np.asarray(Image.open(folder/'hero-mask.png'))>127;pixels=image[mask];l=pixels@np.array([.2126,.7152,.0722])
    tonal=dict(scope='Display RGB in projected asset triangle-union silhouette; no external occluders. This is not an albedo measurement.',
        percentiles=dict(zip(('p1','p5','p50','p95','p99'),map(float,np.percentile(l,[1,5,50,95,99])))),
        clipped_white_fraction=float(np.mean(np.all(pixels>=.995,axis=-1))),
        near_black_fraction=float(np.mean(l<.015)),mask_pixels=int(mask.sum()))
    Path('build/lookdev-tonal.json').write_text(json.dumps(tonal,indent=2))
    checked=[]
    for base in (folder,matches,*[Path(f'renders/lookdev-seeds/{s}') for s in PROOF_SEEDS]):
        for name,row in json.loads((base/'provenance.json').read_text()).items():
            digest=hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()
            assert digest==row['sha256'],(base,name,'stale source render')
            assert 'source look-development' in row['stage'] and row['engine']=='CYCLES'
            checked.append(str(base/(name+'.png')))
    Path('build/lookdev-view-check.json').write_text(json.dumps(dict(passed=True,source_views=len(checked),paths=checked),indent=2))
    print('SOURCE_CHECKPOINT',len(checked),'current Cycles views; contact, six-seeds and three pairs; tonal',tonal)


if __name__=='__main__':main()
