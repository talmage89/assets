"""Local contact sheets only. Checkpoint images are never committed docs."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from plans import garden
base=Path('renders/checkpoint');out=Path('renders/review');out.mkdir(parents=True,exist_ok=True)
paths=sorted(base.glob('*/*.png'));assert len(paths)>=52,('Missing checkpoint views',len(paths))
# Every displayed frame must belong to the current procedural/exported source.
# The source photo pairs are deliberately separate from the delivered glTF.
audit={}
for p in paths:
    record=json.loads((p.parent/'provenance.json').read_text())[p.stem]
    src=Path(record['source'])
    assert record['engine']=='CYCLES'
    assert record['source_sha256']==hashlib.sha256(src.read_bytes()).hexdigest(),p
    assert p.stat().st_mtime>=src.stat().st_mtime,p
    if p.stem in ('hero','ground'):
        assert record['camera']['eye_height_m']==1.68,p
        assert 35<=record['camera']['lens']<=50,p
    audit[str(p)]=record
for folder in ('matches','source-matches'):
    records=json.loads((Path('renders')/folder/'provenance.json').read_text())
    for key in ('used-garden','period-mansard','garage-row'):
        r=records[key];src=Path(r['source']);p=Path('renders')/folder/(key+'.png')
        assert r['engine']=='CYCLES' and r['source_sha256']==hashlib.sha256(src.read_bytes()).hexdigest(),p
        assert p.stat().st_mtime>=src.stat().st_mtime,p
        audit[str(p)]=r
(out/'evidence-audit.json').write_text(json.dumps(audit,indent=2))
contact(paths,out/'contact-sheet.jpg',width=1600,title='Apartments / exported glTF / FORM CHECKPOINT',captions={str(p):p.parent.name+' / '+p.stem for p in paths})
for stem in sorted(set(p.parent.name for p in paths)):
    selected=[p for p in paths if p.parent.name==stem]
    contact(selected,out/(stem+'-inspection.jpg'),width=1600,title=stem+' / current exported form',captions={str(p):p.stem for p in selected})
for kind in ('Complex','Row'):
    selected=[p for p in paths if p.parent.name.startswith(kind) and p.stem in ('above','ground','rear')]
    contact(selected,out/(kind.lower()+'-family.jpg'),width=1600,title=kind+' variants / above, eye height and rear',captions={str(p):p.parent.name+' / '+p.stem for p in selected})
details=[p for p in paths if p.stem in ('stairs','balcony','meters','entry','patios')]
contact(details,out/'construction-details.jpg',width=1600,title='Stairs, balconies, entries, services and patios',captions={str(p):p.parent.name+' / '+p.stem for p in details})
review_sheet([[base/'Complex-301/hero.png'],[base/'Row-403/hero.png']],out/'heroes.jpg',width=1600,title='Parking court and garage row / 40 mm / 1.68 m eyes')
pairs=sorted(Path('renders/matches').glob('*-pair.jpg'));assert len(pairs)==3
review_sheet([[p] for p in pairs],out/'photo-pairs.jpg',width=1600,title='Exported form comparisons / independently fitted photographic views')
# Exported image tonal facts; whole-frame statistics include ground and sky.
report={}
for p in (base/'Complex-301/hero.png',base/'Row-403/hero.png'):
    rgb=np.array(Image.open(p).convert('RGB'))/255;y=rgb@np.array([.2126,.7152,.0722])
    report[str(p)]=dict(percentiles=dict(zip(('p1','p10','median','p90','p99'),np.quantile(y,[.01,.1,.5,.9,.99]).tolist())),white_clipping_fraction=float(np.mean(np.min(rgb,axis=2)>.99)),any_channel_clipping_fraction=float(np.mean(np.max(rgb,axis=2)>.99)),scope='Whole-frame encoded display RGB luma, not a silhouette mask, linear photometry or measured albedo')
(out/'tonal-range.json').write_text(json.dumps(report,indent=2))
# Original schematic unit reservations, never traced from a reference drawing.
canvas=Image.new('RGB',(1500,1000),(241,239,231));draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20);head=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),25)
for col,seed in enumerate((301,304)):
    p=garden(seed);w,d=p['unit_width'],p['unit_depth'];scale=65;x0=50+col*750;y0=120
    draw.text((x0,30),'Central-core 2 bedroom' if seed==301 else 'Breezeway 1 bedroom',font=head,fill='#222d24')
    draw.text((x0,70),f'{w:.3f} × {d:.3f} m gross / front exterior at top',font=font,fill='#222d24')
    for i,r in enumerate(p['unit_rooms']):
        a,b,c,e=r['rect'];box=(x0+a*scale,y0+c*scale,x0+b*scale,y0+e*scale)
        draw.rectangle(box,fill=('#d2d6c4','#c8d2d4','#dfd0b7','#ddd6b9')[i%4],outline='#31382d',width=3)
        draw.text((box[0]+5,box[1]+8),r['name'],font=font,fill='#222d24')
    draw.text((x0,y0+d*scale+20),'Schematic reservations / shallow window rooms in mesh',font=font,fill='#222d24')
canvas.save(out/'unit-plans.jpg',quality=90,optimize=True)
print('REVIEW',len(paths),'views, three pairs; contacts in',out)
