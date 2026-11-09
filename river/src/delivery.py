"""Collect current export views and encode the five bounded gallery images."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from package import bundle,presentation_recipe
from review import sheet
from kit.fonts import find_font


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def collage(files,columns=2):
    cell_w=1600//columns;cell_h=round(cell_w*2/3)+28
    result=Image.new('RGB',(cell_w*columns,cell_h*((len(files)+columns-1)//columns)),(32,36,33))
    draw=ImageDraw.Draw(result);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),17)
    for i,(path,label) in enumerate(files):
        im=Image.open(path).convert('RGB');im.thumbnail((cell_w,cell_h-28),Image.Resampling.LANCZOS)
        x=i%columns*cell_w;y=i//columns*cell_h;result.paste(im,(x+(cell_w-im.width)//2,y))
        draw.text((x+9,y+cell_h-23),label,font=font,fill=(230,232,220))
    return result


def encode(im,path):
    im=im.convert('RGB');im.thumbnail((1600,4000),Image.Resampling.LANCZOS)
    for quality in range(94,49,-2):
        im.save(path,quality=quality,optimize=True,progressive=True)
        if path.stat().st_size<=200000:break
    assert path.stat().st_size<=200000


def main():
    out=Path('renders/final');matches=Path('renders/final-matches');receipt=[];cache={}
    for folder,target in ((Path('renders/checkpoint'),out),(Path('renders/checkpoint-matches'),matches),
                          (Path('renders/wall-details'),out/'wall-details')):
        for p in sorted(folder.rglob('*.png')):
            meta=json.loads(p.with_suffix('.json').read_text());source=meta['source']
            assert meta.get('recipe_sha256')==presentation_recipe(),('Stale gallery light/shader',p)
            assert meta.get('image_sha256')==sha(p),('Changed gallery pixels',p)
            assert not meta.get('source_fields_sha256'),('Source fields in gallery',p)
            if folder.name=='wall-details':
                assert meta.get('wall_recipe_sha256')==sha(Path('src/wall_views.py')),('Stale wall inspection',p)
            if source not in cache:cache[source]=bundle(source)
            assert meta['bundle_sha256']==cache[source],('Stale gallery input',p)
            dest=target/p.relative_to(folder);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);shutil.copy2(p.with_suffix('.json'),dest.with_suffix('.json'))
            receipt.append(dict(path=str(dest),sha256=sha(dest),source_bundle_sha256=cache[source]))
    for p in sorted(Path('renders/checkpoint-matches').glob('*-pair.jpg')):
        matches.mkdir(parents=True,exist_ok=True);shutil.copy2(p,matches/p.name)
    sheet(sorted(out.rglob('*.png'))+sorted(matches.glob('*-pair.jpg')),out/'contact.jpg','River / final exported glTF / complete inspection set')
    sheet(sorted(matches.glob('*-pair.jpg')),matches/'contact.jpg','Concrete-balanced photographic type comparisons',1)
    docs=Path('docs');docs.mkdir(exist_ok=True)
    galleries={
        'hero-101':Image.open(out/'101/hero.png'),
        'hero-202':Image.open(out/'202/hero.png'),
        'places':collage([(out/f'{s}/above.png',title) for s,title in ((101,'Downtown / three spans'),(202,'County edge / two spans'))]),
        'construction':collage([(out/p,label) for p,label in (
            ('101/under.png','Girders and overhang'),('202/abutment.png','Wingwalls and graded quarry stone'),
            ('101/pier.png','Narrow joint runoff and waterline'),('101/bearings.png','Laminated pads, plates and anchors'),
            ('101/floodwall.png','Poured bays and riverwalk access'),('202/driver.png','Two-lane county crossing'),
            ('wall-details/outfall.png','Storm outfall and flood residue'),('wall-details/ladder.png','Ladder, paint-over and bulkhead lights'))],3),
        'water-modules':collage([(out/p,label) for p,label in (
            ('101/riffle.png','Standing waves and flow-aligned foam'),('202/bar.png','Shallow bed and point bar'),
            ('modules.png','Reusable bridge modules'),('101/scale.png','1.8m human and native car'),
            ('101/eevee.png','Downtown / Eevee'),('202/eevee.png','County edge / Eevee'))],3)}
    rows=[]
    for name,im in galleries.items():
        p=docs/(name+'.jpg');encode(im,p)
        rows.append(dict(path=str(p),bytes=p.stat().st_size,size=list(Image.open(p).size),sha256=sha(p)))
    Path('build/delivery.json').write_text(json.dumps(dict(export_bundles=cache,frames=receipt,docs=rows),indent=2)+'\n')
    print('RIVER_DELIVERY',len(receipt),'export frames',[(r['path'],r['bytes']) for r in rows])


if __name__=='__main__':main()
