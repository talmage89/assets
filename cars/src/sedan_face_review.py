"""Native final-camera front repair pairs and the accepted H120 face reference."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from sedan_detail_review import rgb,sheet

REGIONS={
    'lamp-left':('face',(0,200,800,750)),
    'lamp-right':('face',(800,200,1600,750)),
    'grille':('face',(300,260,1300,860)),
    'fascia':('front',(0,450,1600,1050)),
    'rim':('wheel',(150,150,1150,1200)),
    'rear-badge':('rear',(350,550,1150,850)),
    'hero-face':('front_three_quarter',(160,490,960,820)),
}


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--hatch-details',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    old=Path(a.before);new=Path(a.after);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    om=json.loads((old/'shots.json').read_text());nm=json.loads((new/'shots.json').read_text());report={}
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
    for name,(view,box) in REGIONS.items():
        for key in ['location','target','lens','ortho','aspect','studio_yaw','paint','exposure','width','height','render_recipe_sha256']:
            if om[view].get(key)!=nm[view].get(key):raise ValueError('Different final camera/recipe: '+view+' '+key)
        if any(m[view]['stage']!='final exported GLB' for m in [om,nm]):raise ValueError('Only exported GLB proof is accepted')
        before=rgb(old/(view+'.png')).crop(box);after=rgb(new/(view+'.png')).crop(box)
        w,h=before.size
        if w<800 or after.size!=before.size:raise ValueError('Proof must retain at least 800 native pixels per side')
        changed=int(np.any(np.abs(np.asarray(before,dtype='int16')-np.asarray(after,dtype='int16'))>=3,axis=2).sum())
        if not changed:raise ValueError('No visible fix: '+name)
        canvas=Image.new('RGB',(2*w,h+48),(230,232,230));canvas.paste(before,(0,48));canvas.paste(after,(w,48));draw=ImageDraw.Draw(canvas)
        draw.text((12,10),'BEFORE / '+view,font=font,fill=(24,31,34));draw.text((w+12,10),'AFTER / '+str(w)+' native pixels',font=font,fill=(24,31,34))
        path=out/(name+'.jpg');canvas.save(path,quality=96,optimize=True)
        report[name]=dict(view=view,crop_pixels=box,each_side_pixels=[w,h],changed_pixels_3_byte_levels=changed,before_glb_sha256=om[view]['source_sha256'],after_glb_sha256=nm[view]['source_sha256'],proof_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    # The H120's committed details use its 'face' camera: same position,
    # target, 65 mm lens, aspect and studio yaw as the S240 face camera.
    # Its original gallery image occupies this 800 px tile below a caption.
    hatch=Image.open(a.hatch_details).convert('RGB').crop((0,46,800,562))
    sedan=rgb(new/'face.png').resize((800,516),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(1600,564),(230,232,230));canvas.paste(hatch,(0,48));canvas.paste(sedan,(800,48));draw=ImageDraw.Draw(canvas)
    draw.text((12,10),'H120 / accepted face on main',font=font,fill=(24,31,34));draw.text((812,10),'S240 / same face camera and framing',font=font,fill=(24,31,34));canvas.save(out/'hatch-sedan-face.jpg',quality=96,optimize=True)
    sheet([out/(n+'.jpg') for n in REGIONS]+[out/'hatch-sedan-face.jpg'],out/'contact.jpg',1,1800)
    (out/'comparisons.json').write_text(json.dumps(report,indent=2));print('S240_FACE_REVIEW',len(report),'native pairs; H120 comparison')
if __name__=='__main__':main()
