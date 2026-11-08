"""Five bounded final JPGs from current exported, baked presentation images.

Run after native review. Historical/rejected images and reference photographs
never enter docs. Sources and encoded bytes are recorded for the final audit.
"""
import hashlib,io,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from package import bundle

folder=Path('renders/final');dest=Path('docs');dest.mkdir(exist_ok=True);rows=[]
font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20)

def write(name,im,sources):
    im=im.convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
    for quality in range(94,29,-2):
        payload=io.BytesIO();im.save(payload,'JPEG',quality=quality,optimize=True,progressive=True)
        if len(payload.getvalue())<=200000:break
    else:raise AssertionError(('Docs JPEG too large',name))
    path=dest/name;path.write_bytes(payload.getvalue());rows.append(dict(path=str(path),size=list(im.size),bytes=path.stat().st_size,quality=quality,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sources=sources))

def sheet(name,items,columns=3):
    cell=1600//columns;h=round(cell*2/3)+40;im=Image.new('RGB',(1600,h*((len(items)+columns-1)//columns)),'#e7e4d8');d=ImageDraw.Draw(im)
    for i,(rel,title) in enumerate(items):
        p=folder/rel;src=Image.open(p).convert('RGB');src.thumbnail((cell-12,h-45),Image.Resampling.LANCZOS);x=i%columns*cell+(cell-src.width)//2;y=i//columns*h
        im.paste(src,(x,y));d.text((i%columns*cell+10,y+h-32),title,font=font,fill='#283a31')
    write(name,im,[str(folder/rel) for rel,_ in items])

for seed in (117,228,339):
    p=folder/str(seed)/'hero.png';meta=json.loads(p.with_suffix('.json').read_text());assert meta['bundle_sha256']==bundle(meta['source'])
    assert meta['image_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
    write(f'hero-{seed}.jpg',Image.open(p),[str(p)])
sheet('layouts.jpg',[(f'{s}/layout.jpg',f'{s} / measured clear routes') for s in (117,228,339)]+[('pieces.png','Furniture and fit-out / exported pieces')],columns=2)
sheet('details.jpg',[
    ('117/table.png','Folio / period laptop and table'),('228/rail.png','Morrow / chipped rail and used paving'),('339/walkup.png','Switchyard / walk-up window'),
    ('117/counter.png','Folio / counter through the glass'),('228/awning.png','Morrow / awning and sign'),('117/chair.png','Accepted 2,156-triangle chair'),
    ('228/door.png','Worn entrance and dog bowl'),('117/scale.png','1.8 m scale silhouette'),('339/eevee.png','Switchyard / Eevee')])
assert len(rows)==5
Path('build/docs.json').write_text(json.dumps(rows,indent=2)+'\n');print('DOCS',[(r['path'],r['bytes']) for r in rows])
