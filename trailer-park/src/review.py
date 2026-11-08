"""Ignored, labeled review contacts; no final docs at this form gate."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def sheet(paths,out,width=600):
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),17);h=round(width*.65)+36
    im=Image.new('RGB',(width*2,h*((len(paths)+1)//2)),(226,227,220));draw=ImageDraw.Draw(im)
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGB');tile=ImageOps.contain(src,(width-12,h-44));x=(i%2)*width+(width-tile.width)//2;y=(i//2)*h
        im.paste(tile,(x,y+32));draw.text(((i%2)*width+9,y+7),str(p.parent.name)+' / '+p.stem,font=font,fill=(25,33,28))
    im.save(out,quality=92,optimize=True);return out


def main():
    a=argparse.ArgumentParser();a.add_argument('--renders',type=Path,required=True);a=a.parse_args();root=a.renders
    receipts=json.loads((root/'provenance.json').read_text())
    for row in receipts:
        source=Path(row['source'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],('Stale export render',row['stem'],row['shot'])
        for im in row['images']:
            assert hashlib.sha256((source.parent/im['uri']).read_bytes()).hexdigest()==im['sha256'],('Changed image input',im['uri'])
        relative=Path(row['stem'])/(row['shot']+'.png')
        assert (root/relative).is_file() or (root/'matches'/relative).is_file(),('Missing rendered frame',relative)
    paths=[p for p in sorted(root.glob('*/*.png')) if p.parent.name!='matches'];assert paths,'No exported review frames'
    sheet(paths,root/'contact.jpg')
    pairs=sorted((root/'matches').glob('*-pair.jpg'))
    if pairs:sheet(pairs,root/'matched-contact.jpg',1000)
    for stem in ('SingleWide-120','DoubleWide-228'):
        frames=[root/stem/(n+'.png') for n in ('front','side','back','top')]
        if all(p.exists() for p in frames):sheet(frames,root/stem/'turnaround.jpg')
    stats={}
    import numpy as np
    for p in paths:
        rgb=np.array(Image.open(p).convert('RGB'));v=rgb.max(2)/255
        stats[str(p.relative_to(root))]=dict(size=Image.open(p).size,dark_fraction=float((v<.10).mean()),near_clip_fraction=float((v>.985).mean()),p5=float(np.percentile(v,5)),p95=float(np.percentile(v,95)))
    (root/'tonal-report.json').write_text(json.dumps(stats,indent=2))
    (root/'source-verification.json').write_text(json.dumps(dict(passed=True,render_receipts=len(receipts),scope='Current glTF and referenced external image SHA-256 identities'),indent=2))
    print('CONTACT',root/'contact.jpg',len(paths),'frames',len(pairs),'photo pairs; source identities verified')

if __name__=='__main__':main()
