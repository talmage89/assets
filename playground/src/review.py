"""Ignored checkpoint contact sheets and measured budget table; never docs/."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact
from kit.fonts import find_font

def main():
    out=Path('renders/checkpoint')
    if (out/'pieces.json').exists():
        im=Image.open(out/'pieces.png').convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans'),19)
        for row in json.loads((out/'pieces.json').read_text()).get('piece_labels',[]):
            x,y=row['pixel'];label=row['name'];w=d.textlength(label,font=font)
            d.rectangle((x-w/2-4,y-2,x+w/2+4,y+25),fill=(238,239,235));d.text((x-w/2,y),label,font=font,fill=(22,32,27))
        im.save(out/'pieces-labeled.jpg',quality=95)
    paths=sorted(out.glob('[123]*/hero.png'))+sorted(out.glob('[123]*/above.png'))+sorted(out.glob('*.png'));contact(paths,out/'contact.jpg',width=2000,title='Playground / form and construction checkpoint / exported glTF')
    pairs=sorted((out/'matches').glob('*-pair.jpg'))
    if pairs:contact(pairs,out/'matched-contact.jpg',width=2000,title='Period photographs / construction comparisons / camera fit residuals retained')
    # Numerical value audit is descriptive; no exposure tricks or look acceptance.
    values={}
    for p in out.glob('*/hero.png'):
        a=__import__('numpy').asarray(Image.open(p).convert('RGB'))/255;lum=.2126*a[:,:,0]+.7152*a[:,:,1]+.0722*a[:,:,2]
        values[p.parent.name]=dict(p1=float(__import__('numpy').percentile(lum,1)),p50=float(__import__('numpy').percentile(lum,50)),p99=float(__import__('numpy').percentile(lum,99)),clipped_pixels_fraction=float((a.max(axis=2)>.995).mean()),scope='whole-frame display luminance; quick materials, not albedo calibration')
    Path('build/hero-values.json').write_text(json.dumps(values,indent=2));print('CONTACT',out/'contact.jpg')

if __name__=='__main__':main()
