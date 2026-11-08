"""Native-size before/after panels; geometry comparisons use identical cameras."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from package import bundle


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder=Path('renders/fixes');folder.mkdir(parents=True,exist_ok=True);rows=[]
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),21)
    for seed in (101,202):
        for name in ('hero','above','under','bearings','pier','abutment','riffle','bar','driver','scale'):
            before=Path('build/round2-before/renders/checkpoint')/str(seed)/(name+'.png')
            current=Path('renders/checkpoint')/str(seed)/(name+'.png')
            old=json.loads(before.with_suffix('.json').read_text());now=json.loads(current.with_suffix('.json').read_text())
            after=current
            if old['camera']!=now['camera']:
                before=folder/'before'/str(seed)/(name+'.png');old=json.loads(before.with_suffix('.json').read_text())
            assert old['camera']==now['camera'],('Comparison camera changed',seed,name)
            assert now['bundle_sha256']==bundle(now['source']),('Stale comparison',after)
            a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB')
            assert a.size==b.size and a.width>=800,(before,a.size,b.size)
            im=Image.new('RGB',(a.width*2,a.height+50),(30,34,30));im.paste(a,(0,50));im.paste(b,(a.width,50))
            draw=ImageDraw.Draw(im);draw.text((16,14),f'{seed} / {name} — before',font=font,fill=(238,237,226))
            draw.text((a.width+16,14),'after / identical camera',font=font,fill=(238,237,226))
            path=folder/f'{seed}-{name}.jpg';im.save(path,quality=94,optimize=True)
            rows.append(dict(path=str(path),before=str(before),after=str(after),camera=old['camera'],
                             before_sha256=sha(before),after_sha256=sha(after),pixels_per_side=a.width,
                             before_bundle=old['bundle_sha256'],after_bundle=now['bundle_sha256']))
    Path('build/fix-evidence.json').write_text(json.dumps(dict(passed=True,panels=rows),indent=2)+'\n')
    print('IDENTICAL_CAMERA_PANELS',len(rows))


if __name__=='__main__':main()
