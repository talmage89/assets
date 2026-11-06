"""Native-camera R9/R10 comparison crops; no resizing of either proof image."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from sedan_detail_review import rgb,sheet
REGIONS={
 'gaps-doors':('side',(440,270,1240,580)),
 'gaps-tail':('side',(800,300,1600,610)),
 'nose-profile':('side',(0,330,800,650)),
 'tail-profile':('side',(800,330,1600,650)),
 'lamp-and-surround':('face',(0,230,800,650)),
 'lamp-hero':('front_three_quarter',(200,360,1000,820)),
 'tires':('wheel',(0,150,900,1200)),
}


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    before=Path(a.before);after=Path(a.after);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bm=json.loads((before/'shots.json').read_text());am=json.loads((after/'shots.json').read_text());font=ImageFont.truetype(find_font('Noto Sans','Regular'),22);report={}
    for name,(view,box) in REGIONS.items():
        for key in ['location','target','lens','ortho','aspect','studio_yaw','paint','exposure','width','height','render_recipe_sha256']:
            if bm[view].get(key)!=am[view].get(key):raise ValueError('Different comparison recipe: '+view+' '+key)
        if any(meta[view]['stage']!='final exported GLB' for meta in [bm,am]):raise ValueError('Proof must use two exported GLBs')
        old=rgb(before/(view+'.png')).crop(box);new=rgb(after/(view+'.png')).crop(box)
        if old.width<800 or old.size!=new.size:raise ValueError('Native comparison crop size')
        difference=np.abs(np.asarray(old,dtype='int16')-np.asarray(new,dtype='int16'))
        changed=int(np.any(difference>=3,axis=2).sum())
        if not changed:raise ValueError('The fix does not change the image: '+name)
        w,h=old.size;canvas=Image.new('RGB',(2*w,h+48),(230,232,230));canvas.paste(old,(0,48));canvas.paste(new,(w,48));draw=ImageDraw.Draw(canvas)
        draw.text((12,10),'BEFORE - R9 / '+view,font=font,fill=(24,31,34));draw.text((w+12,10),'AFTER - R10 / native '+str(w)+' px crop',font=font,fill=(24,31,34))
        path=out/(name+'.jpg');canvas.save(path,quality=96,optimize=True)
        report[name]=dict(view=view,original_crop_pixels=box,each_side_size_pixels=[w,h],different_pixels_at_3_or_more_byte_levels=changed,before_glb_sha256=bm[view]['source_sha256'],after_glb_sha256=am[view]['source_sha256'],comparison_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    sheet([out/(name+'.jpg') for name in REGIONS],out/'contact.jpg',1,1800)
    (out/'comparisons.json').write_text(json.dumps(report,indent=2));print('NATIVE_TELL_COMPARISONS',len(report))
if __name__=='__main__':main()
