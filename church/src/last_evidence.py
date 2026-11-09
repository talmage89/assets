"""Native crops of the five final-round fixes, with optical receipts."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
from review import sheet


def main():
    root=Path('renders/last-fixes');root.mkdir(parents=True,exist_ok=True)
    baseline=Path('renders/before-delivery')
    if not baseline.exists():
        print('Historical handoff frames absent; current finals remain independently audited');return
    rows=[]
    for seed,shot,label,box in (
        (101,'age','01-masonry-101',(0,80,1000,900)),
        (202,'age','01-masonry-202',(300,80,1300,900)),
        (101,'north_roof','02-roof-101',(100,0,1300,900)),
        (202,'north_roof','02-roof-202',(0,0,1200,900)),
        (202,'hero','03-aframe-light',None),
        (101,'above','04-lawn-101',(0,100,1200,920)),
        (202,'above','04-lawn-202',(100,100,1300,920)),
        (101,'doors','05-entry-101',(200,80,1200,920)),
        (202,'doors','05-entry-202',(200,80,1200,920)),
        (101,'hero','hero-101',None),(202,'hero','hero-202',None)):
        old=baseline/str(seed)/(shot+'.png');new=Path('renders/final')/str(seed)/(shot+'.png')
        a=json.loads(old.with_suffix('.json').read_text());b=json.loads(new.with_suffix('.json').read_text())
        for key in ('location','target','lens','resolution'):assert a[key]==b[key],(label,key)
        images=[Image.open(p).convert('RGB') for p in (old,new)]
        if box:images=[im.crop(box) for im in images]
        assert min(im.width for im in images)>=800
        w,h=images[0].size;pair=Image.new('RGB',(w*2,h+32),(225,227,221));draw=ImageDraw.Draw(pair)
        for j,im in enumerate(images):
            pair.paste(im,(j*w,32));draw.text((j*w+12,10),'c655bb4 handoff' if j==0 else 'Final export',fill=(20,25,21))
        out=root/(label+'.jpg');pair.save(out,quality=95,optimize=True)
        rows.append(dict(file=str(out),before=str(old),after=str(new),crop=box,panel_width=w,camera_equal=True,
                         light_equal=a.get('sun_direction')==b.get('sun_direction') and a.get('sky_strength')==b.get('sky_strength'),
                         sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
    (root/'receipts.json').write_text(json.dumps(rows,indent=2))
    sheet([p for p in sorted(root.glob('*.jpg')) if p.name!='contact.jpg'],root/'contact.jpg')
    print('PASS',len(rows),'native same-camera final-round comparisons')


if __name__=='__main__':main()
