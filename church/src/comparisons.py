"""Native-size before/after pairs, with camera equality proved by receipts."""
import json
from pathlib import Path
from PIL import Image,ImageDraw


def main(after='renders/checkpoint'):
    root=Path('renders/before-after');root.mkdir(exist_ok=True)
    rows=[]
    for seed in (101,202):
        for shot in ('hero','above','window','window_dusk'):
            before=Path(f'renders/before-look/checkpoint/{seed}/{shot}.png');now=Path(after)/str(seed)/(shot+'.png')
            a=json.loads(before.with_suffix('.json').read_text());b=json.loads(now.with_suffix('.json').read_text())
            for key in ('location','target','lens'):assert a[key]==b[key],(seed,shot,key)
            images=[Image.open(p).convert('RGB') for p in (before,now)]
            assert all(im.width>=800 for im in images)
            w=max(im.width for im in images);h=max(im.height for im in images)
            pair=Image.new('RGB',(w*2,h+36),(228,229,223));draw=ImageDraw.Draw(pair)
            for i,im in enumerate(images):pair.paste(im,(w*i,36));draw.text((w*i+12,10),'Before' if i==0 else 'After',fill=(15,23,18))
            name=f'{seed}-{shot}.jpg';pair.save(root/name,quality=95,optimize=True)
            rows.append(dict(file=name,before=str(before),after=str(now),camera_equal=True,panel_widths=[im.width for im in images]))
    (root/'receipts.json').write_text(json.dumps(rows,indent=2));print('PASS',len(rows),'same-camera native-size pairs')


if __name__=='__main__':main()
