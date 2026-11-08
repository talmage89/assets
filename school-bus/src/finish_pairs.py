"""Round-three evidence, each side at native resolution with held cameras."""
import hashlib,json,os,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parent
sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font

def main():
    before=BASE/'renders/round3-before';after=BASE/'renders/final'
    out=BASE/'renders/round3-repairs';out.mkdir(parents=True,exist_ok=True)
    new=json.loads((after/'provenance.json').read_text())
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),24);rows={}
    for label,view in [('surface','hood_surface'),('lamps','lamp_detail'),('header','front_detail'),
                       ('paint','front_detail'),('vinyl','aisle'),('cabin','aisle_daylight'),
                       ('queue','hero'),('fleet','fleet')]:
        prior=before/'details' if label in ['surface','lamps'] else before
        if label in ['queue','fleet']:
            # This is the actual stale gallery from before the marking repair,
            # not a newly rendered historical export with repaired lettering.
            prior=ROOT/'build/bus-round3/before/renders/checkpoint'
        old=json.loads((prior/'provenance.json').read_text())
        ps=[prior/(view+'.png'),after/(view+'.png')]
        ims=[Image.open(p).convert('RGB') for p in ps]
        if min(im.width for im in ims)<800:raise ValueError('Native evidence too small')
        for k in ['location','target','lens','aspect','ortho','roll']:
            if old[view]['camera'].get(k)!=new[view]['camera'].get(k):raise ValueError('Changed camera: '+view)
        canvas=Image.new('RGB',(sum(im.width for im in ims),max(im.height for im in ims)+48),(231,231,224))
        d=ImageDraw.Draw(canvas);x=0
        for im,title in zip(ims,['Before / round 2 export','After / current baked export']):
            canvas.paste(im,(x,48));d.text((x+15,10),title,font=font,fill=(25,25,23));x+=im.width
        canvas.save(out/(label+'.jpg'),quality=95,optimize=True)
        rows[label]=dict(images=[os.path.relpath(p,BASE) for p in ps],native_widths=[im.width for im in ims],
                         sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in ps],
                         camera=new[view]['camera'],sources=[old[view]['sha256'],new[view]['sha256']])
    (out/'comparisons.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':main()
