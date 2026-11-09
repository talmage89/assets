"""Native-size before/after panels; geometry comparisons use identical cameras."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from package import bundle,camera_signature


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder=Path('renders/fixes');folder.mkdir(parents=True,exist_ok=True);rows=[]
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),21)
    pairs=[]
    for seed in (101,202):
        from views import views
        for name in views(seed):
            pairs.append((seed,name,folder/'before'/str(seed)/(name+'.png'),
                          Path('renders/checkpoint')/str(seed)/(name+'.png')))
    for name in ('outfall','ladder'):
        pairs.append((101,name,Path('renders/wall-before')/(name+'.png'),
                      Path('renders/wall-details')/(name+'.png')))
    for seed,name,before,after in pairs:
        old=json.loads(before.with_suffix('.json').read_text());now=json.loads(after.with_suffix('.json').read_text())
        assert old.get('accepted_revision')=='4f09582',('Wrong comparison revision',before)
        assert camera_signature(old['camera'])==camera_signature(now['camera']),('Comparison camera changed',seed,name)
        assert now['bundle_sha256']==bundle(now['source']),('Stale comparison',after)
        a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB')
        assert a.size==b.size and a.width>=800,(before,a.size,b.size)
        for path,pixels in ((before,a),(after,b)):
            y=np.asarray(pixels,dtype=float)@np.array([.2126,.7152,.0722])/255
            assert np.percentile(y,99)>.08,('Occluded or nearly black comparison',path)
        im=Image.new('RGB',(a.width*2,a.height+50),(30,34,30));im.paste(a,(0,50));im.paste(b,(a.width,50))
        draw=ImageDraw.Draw(im);draw.text((16,14),f'{seed} / {name} — before',font=font,fill=(238,237,226))
        draw.text((a.width+16,14),'after / identical camera',font=font,fill=(238,237,226))
        path=folder/f'{seed}-{name}.jpg';im.save(path,quality=94,optimize=True)
        rows.append(dict(path=str(path),before=str(before),after=str(after),camera=old['camera'],
                         before_sha256=sha(before),after_sha256=sha(after),pixels_per_side=a.width,
                         before_bundle=old['bundle_sha256'],after_bundle=now['bundle_sha256']))
    Path('build/fix-evidence.json').write_text(json.dumps(dict(passed=True,panels=rows),indent=2)+'\n')
    print('IDENTICAL_CAMERA_PANELS',len(rows))
    from review import sheet
    sheet([Path(row['path']) for row in rows],folder/'contact.jpg','Accepted 4f09582 / current export / identical cameras',2)


if __name__=='__main__':main()
