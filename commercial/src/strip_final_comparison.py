"""Native-pixel before/after crops; the original accepted handoff is immutable.

Before images are captured once at takeover, never rebuilt with new code.
All crops are >=800 px wide; no crop is enlarged to claim full-size evidence.
"""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def run():
    before=Path('build/strip-final/before');final=Path('renders/strip/checkpoint');out=Path('renders/strip/fixes');out.mkdir(parents=True,exist_ok=True)
    cases=[('window-life','storefront',(.12,.28,.94,.96)),('sign-face','storefront',(.10,.02,.94,.45)),('night-light','dusk',(.02,.18,.97,.99)),('asphalt','stalls',(0,.25,1,1)),('walk','walk',(0,0,1,1)),('rear','rear',(0,.20,1,1)),('warm-palette','hero',(0,.15,1,.99))]
    cases += [(f'site-{s}',f'seeds/{s}/above',(0,0,1,1)) for s in range(201,205)]
    rows=[];font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),23)
    for name,shot,crop in cases:
        paths=[before/'checkpoint'/(shot+'.png'),final/(shot+'.png')];images=[]
        for path in paths:
            im=Image.open(path).convert('RGB');box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(crop));im=im.crop(box)
            assert im.width>=800,(path,im.size);images.append(im)
        w=max(im.width for im in images);h=sum(im.height for im in images)+100;sheet=Image.new('RGB',(w,h),'#E9E7DF');dr=ImageDraw.Draw(sheet);y=0
        for label,im in zip(('Before / handoff 23cbe31 / native pixels','After / external glTF / native pixels'),images):
            dr.text((14,y+9),label,font=font,fill='#26302A');sheet.paste(im,(0,y+48));y+=im.height+50
        target=out/(name+'-before-after.jpg');sheet.save(target,quality=94,optimize=True)
        rows.append(dict(name=name,output=str(target),sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],crop_fraction=crop,native_sizes=[im.size for im in images]))
    (out/'comparison.json').write_text(json.dumps(dict(baseline='23cbe31',rows=rows,scope=__doc__),indent=2)+'\n')
    print('STRIP FINAL COMPARISONS',len(rows),'native crops, each >=800px')

if __name__=='__main__':run()
