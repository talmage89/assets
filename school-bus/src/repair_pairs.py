"""Native-resolution same-camera repair evidence; never writes docs/."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=ROOT/'school-bus'

def main():
    before=BASE/'renders/round2-before/checkpoint';after=BASE/'renders/checkpoint'
    out=BASE/'renders/round2-repairs';out.mkdir(parents=True,exist_ok=True)
    old=json.loads((before/'provenance.json').read_text());new=json.loads((after/'provenance.json').read_text())
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),22);rows={}
    views=[('front','front_detail','front_detail'),('glass','side','side'),
           ('lining','interior','interior'),('seats','aisle','aisle'),
           ('stepwell','entrance','entrance'),('hero_read','hero','original_hero'),
           ('school_loop','hero','hero')]
    for label,bn,an in views:
        prior=before if label!='school_loop' else BASE/'renders/round2-before/new-hero-camera'
        history=old if label!='school_loop' else json.loads((prior/'provenance.json').read_text())
        bp=prior/(bn+'.png');ap=after/(an+'.png')
        left=Image.open(bp).convert('RGB');right=Image.open(ap).convert('RGB')
        if min(left.width,right.width)<800:raise ValueError('Insufficient native pair width')
        # Shot dictionaries also contain light states and exposure. The framing
        # must match exactly; both lighting receipts remain explicit below.
        framing=['location','target','lens','aspect','ortho','roll']
        if any(history[bn]['camera'].get(k)!=new[an]['camera'].get(k) for k in framing):
            raise ValueError('Changed camera in '+label)
        canvas=Image.new('RGB',(left.width+right.width,max(left.height,right.height)+48),(231,231,224))
        canvas.paste(left,(0,48));canvas.paste(right,(left.width,48))
        draw=ImageDraw.Draw(canvas);draw.text((15,12),'Before / exported checkpoint',font=font,fill=(20,25,22))
        draw.text((left.width+15,12),'After / exported round 2',font=font,fill=(20,25,22))
        canvas.save(out/(label+'.png'));canvas.save(out/(label+'.jpg'),quality=94,optimize=True)
        rows[label]=dict(before=str(bp.relative_to(BASE)),after=str(ap.relative_to(BASE)),
            native_widths=[left.width,right.width],camera=new[an]['camera'],
            source_hashes=[history[bn]['sha256'],new[an]['sha256']],
            image_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in [bp,ap]],
            before_lighting=history[bn]['lighting'],after_lighting=new[an]['lighting'])
    (out/'comparisons.json').write_text(json.dumps(rows,indent=2))
    print('BUS_REPAIR_PAIRS',len(rows),'native same-camera pairs')
if __name__=='__main__':main()
