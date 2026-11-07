"""Checkpoint evidence, dimension drawings and contacts. Never writes docs/."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font
from kit.contact import contact,review_sheet


def main():
    folder=Path('renders/checkpoint');font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),19);small=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),16);receipts=[]
    check=json.loads(Path('build/check.json').read_text());shops={s['seed']:s for s in check['shops']}
    for seed in (117,228,339):
        p=folder/str(seed)/'above.png';im=Image.open(p).convert('RGBA');meta=json.loads(p.with_suffix('.json').read_text());layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
        for i,r in enumerate(meta['routes']):
            poly=[(u*im.width,v*im.height) for u,v in r['screen']];d.polygon(poly,fill=(25,191,137,35),outline=(70,255,177,255),width=3)
            x0,x1,y0,y1=r['rect'];width=min(x1-x0,y1-y0);a,b=(poly[0],poly[3]) if x1-x0>y1-y0 else (poly[0],poly[1]);d.line((*a,*b),fill='#66ffb4',width=4)
            for x,y in (a,b):d.ellipse((x-4,y-4,x+4,y+4),fill='#ddffdc')
            x=sum(q[0] for q in poly)/4;y=sum(q[1] for q in poly)/4;text=f'{i+1}. {width:.3f} m clear'
            bb=d.textbbox((x,y),text,font=font);d.rectangle((bb[0]-5,bb[1]-4,bb[2]+5,bb[3]+4),fill=(14,40,30,230));d.text((x,y),text,font=font,fill='#e5ffde')
        for t in meta['tables']:
            if t['accessible']:
                x,y=t['screen'];x*=im.width;y*=im.height;d.ellipse((x-22,y-22,x+22,y+22),outline='#f5db70',width=3);d.text((x+25,y-8),'accessible table',font=small,fill='#ffe489')
        im=Image.alpha_composite(im,layer).convert('RGB');canvas=Image.new('RGB',(im.width,im.height+155),'#e6e6dc');canvas.paste(im,(0,0));d=ImageDraw.Draw(canvas)
        for i,r in enumerate(meta['routes']):d.text((16,im.height+12+i*29),f'{i+1}  {r["name"]} — tested unobstructed box; minimum {r["required"]:.3f} m',font=small,fill='#25352f')
        canvas.save(folder/str(seed)/'layout.jpg',quality=94)
        hero=np.asarray(Image.open(folder/str(seed)/'hero.png').convert('RGB'))/255;roi=hero[round(hero.shape[0]*.22):round(hero.shape[0]*.88),round(hero.shape[1]*.14):round(hero.shape[1]*.91)];luma=roi@np.array([.2126,.7152,.0722]);values=dict(percentiles=dict(zip(('p1','p50','p95','p99'),np.percentile(luma,[1,50,95,99]).tolist())),white_clipped_fraction=float(np.mean(np.max(roi,axis=2)>.995)),measurement='display-space architectural framing rectangle, including glazing/reflections; not albedo')
        receipts.append(dict(seed=seed,hero_values=values,geometry=shops[seed]))
    p=folder/'pieces.png';im=Image.open(p).convert('RGB');d=ImageDraw.Draw(im);meta=json.loads(p.with_suffix('.json').read_text())
    for row in meta.get('labels',[]):
        x,y=row['screen'];x*=im.width;y*=im.height
        bb=d.textbbox((x,y),row['name'],font=small);d.rectangle((bb[0]-3,bb[1]-2,bb[2]+3,bb[3]+2),fill='#e5e4d9');d.text((x,y),row['name'],font=small,fill='#26342d')
    im.save(folder/'piece-sheet.jpg',quality=94)
    all_images=[];captions={}
    for seed in (117,228,339):
        for shot in ('hero','above','layout','counter','table','chair','awning','scale','walkup'):
            p=folder/str(seed)/(shot+('.jpg' if shot=='layout' else '.png'))
            if p.exists():all_images.append(p);captions[str(p)]=str(seed)+' / '+shot
    all_images.append(folder/'piece-sheet.jpg')
    pairs=sorted(Path('renders/matches').glob('*-pair.jpg'));all_images.extend(pairs)
    contact(all_images,folder/'contact.jpg',width=1800,title='Coffee shop family — form & construction checkpoint',captions=captions)
    review_sheet([[folder/str(s)/'hero.png'] for s in (117,228,339)],folder/'heroes.jpg',width=1600,title='Three original businesses — exports in Cycles')
    review_sheet([[folder/str(s)/'layout.jpg'] for s in (117,228,339)],folder/'layouts.jpg',width=1600,title='Seating and tested pedestrian corridors')
    # Reject stale images by their recorded external bundle and actual pixels.
    from package import bundle
    for p in folder.rglob('*.png'):
        record=json.loads(p.with_suffix('.json').read_text());assert record['bundle_sha256']==bundle(record['source']),('stale export',str(p));assert record['image_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
    Path('build/presentation-check.json').write_text(json.dumps(dict(shops=receipts,images=len(list(folder.rglob('*.png'))),pairs=len(pairs),status='current exported bundles; quick materials; no final docs'),indent=2)+'\n');print('PRESENTATION PASS')


if __name__=='__main__':main()
