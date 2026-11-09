"""Native-size last-round comparisons to the preserved 56cce73 handoff."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from package import sha,bundle,camera_signature
from review import sheet
from kit.fonts import find_font


def main():
    base=Path('../build/river-last-round/before');out=Path('renders/last-fixes');out.mkdir(parents=True,exist_ok=True)
    views=[(str(seed),name) for seed in (101,202) for name in
           ('hero','above','under','abutment','pier','bearings','bar','riffle','driver')]
    views += [('101','floodwall'),('wall-details','outfall'),('wall-details','ladder')]
    rows=[];font=ImageFont.truetype(find_font('DejaVu Sans','Book'),21)
    for seed,name in views:
        before=base/'renders/final'/seed/(name+'.png')
        after=Path('renders/wall-details' if seed=='wall-details' else f'renders/checkpoint/{seed}')/(name+'.png')
        old=json.loads(before.with_suffix('.json').read_text());new=json.loads(after.with_suffix('.json').read_text())
        assert camera_signature(old['camera'])==camera_signature(new['camera']),(seed,name,'Camera changed')
        for key in ('exposure','sun_energy','engine','width','samples'):
            assert old.get(key)==new.get(key),(seed,name,'Accepted presentation changed',key)
        assert max(abs(a-b) for a,b in zip(old['sun_direction'],new['sun_direction']))<1e-6
        assert new['bundle_sha256']==bundle(new['source']),('Stale last-round frame',after)
        a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB')
        assert a.size==b.size and a.width>=800
        im=Image.new('RGB',(a.width*2,a.height+50),(30,34,30));im.paste(a,(0,50));im.paste(b,(a.width,50))
        draw=ImageDraw.Draw(im);draw.text((16,14),f'{seed} {name} / 56cce73',font=font,fill=(238,237,226))
        draw.text((a.width+16,14),'Last round / identical camera and lighting',font=font,fill=(238,237,226))
        path=out/f'{seed}-{name}.jpg';im.save(path,quality=94,optimize=True)
        rows.append(dict(path=str(path),before_sha256=sha(before),after_sha256=sha(after),pixels_per_side=a.width,
                         camera=new['camera'],before_bundle=old['bundle_sha256'],after_bundle=new['bundle_sha256']))
    sheet([Path(r['path']) for r in rows],out/'contact.jpg','Last round / original 56cce73 and final exported surface',2)
    Path('build/last-evidence.json').write_text(json.dumps(dict(passed=True,baseline='56cce73',panels=rows),indent=2)+'\n')
    print('LAST_ROUND_IDENTICAL_CAMERAS',len(rows))


if __name__=='__main__':main()
