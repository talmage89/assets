"""Five bounded gallery JPGs after the final full-size delivery review."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def encode(im,path):
    im=im.convert('RGB')
    if im.width>1600 or im.height>2400:im=ImageOps.contain(im,(1600,2400))
    for quality in (92,88,84,80,76,72,68,64,60):
        im.save(path,quality=quality,optimize=True,progressive=True)
        if path.stat().st_size<=200000:break
    assert im.width<=1600 and path.stat().st_size<=200000,path
    return dict(path=str(path),size=im.size,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def panel(folder,items,cols=2):
    width=1600//cols;height=round(width*.62)+32;font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),18)
    im=Image.new('RGB',(1600,height*((len(items)+cols-1)//cols)),(226,227,220));d=ImageDraw.Draw(im)
    for i,(name,label) in enumerate(items):
        tile=ImageOps.contain(Image.open(folder/name).convert('RGB'),(width-10,height-37));x=i%cols*width+(width-tile.width)//2;y=i//cols*height
        im.paste(tile,(x,y+32));d.text((i%cols*width+9,y+7),label,font=font,fill=(25,31,26))
    return im


def main(folder):
    from presentation_check import check
    text=Path('REVIEW.md').read_text()
    for n in (1,2,3):assert f'## Completion pass {n}' in text,('Missing current-round full-size critique',n)
    status=text.rsplit('\nDelivery gate: ',1)[-1].splitlines()[0]
    assert status in ('ACCEPTED','DELIVERED WITH KNOWN FLAWS'), 'Final delivery review is missing'
    if status=='DELIVERED WITH KNOWN FLAWS':
        assert '## Known flaws' in Path('README.md').read_text(), 'Disclose remaining flaws before gallery delivery'
    check(folder);out=Path('docs');out.mkdir(exist_ok=True);rows=[]
    for seed in (101,202):rows.append(encode(Image.open(folder/f'Park-{seed}/hero.png'),out/f'hero-{seed}.jpg'))
    rows.append(encode(panel(folder,[('Park-101/above.png','Alder Court / 36 homes'),('Park-202/above.png','Meadow Bend / 33 homes')]),out/'parks.jpg'))
    items=[(f'{stem}/{view}.png',label+' / '+view) for stem,label in [('SingleWide-120','1972 single-wide'),('DoubleWide-228','1996 double-wide')] for view in ('front','side','back','top')]
    items += [('Modules/detail.png','Modules and add-ons'),('HomeForms/detail.png','Six home dimensions'),('SingleWide-120/scale.png','1.8 m human and car'),('Park-202/eevee.png','Meadow Bend / Eevee')]
    rows.append(encode(panel(folder,items,3),out/'homes-modules.jpg'))
    items=[('Park-101/row.png','Older siding, skirting and occupied lot'),('SupportFrame/piers.png','Piers, shims and tie-downs'),('Deck/detail.png','Deck and stair construction'),('Carport/detail.png','Folded aluminum carport'),('UtilityService/detail.png','Meter, breaker and service risers'),('EntranceSign/detail.png','Fictional entrance sign')]
    rows.append(encode(panel(folder,items),out/'details.jpg'))
    assert len(list(out.glob('*.jpg')))==5
    Path('build/docs.json').write_text(json.dumps(dict(passed=True,images=rows,source_receipt='build/final-provenance.json'),indent=2));print('DOCS PASS',[(r['path'],r['bytes']) for r in rows])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/final'));a=p.parse_args();main(a.renders)
