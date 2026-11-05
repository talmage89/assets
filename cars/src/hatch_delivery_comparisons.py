"""Same-camera native crops of the remaining H120 delivery corrections."""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
REGIONS={
 'grille-badge':('grille',(.25,.27,.76,.72)),
 'face':('face',(0,0,1,1)),
 'wheel-cap-and-spokes':('wheel',(.12,.06,.88,.95)),
 'projector':('lamp_unlit',(0,.25,1,1)),
 'tail-lens-and-fuel-reveal':('rear_quarter',(0,.28,.82,.74)),
 'gate':('used_rear',(.58,.30,.97,.72)),
}


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--pairs',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    before=Path(a.before);after=Path(a.after);pairs=Path(a.pairs);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bm=json.loads((before/'shots.json').read_text());am=json.loads((after/'shots.json').read_text());pm=json.loads((pairs/'shots.json').read_text())
    records={};font=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
    for name,(view,rect) in REGIONS.items():
        directory=pairs if view=='used_rear' else after;meta=pm if view=='used_rear' else am
        for field in ['location','target','lens','roll','studio_yaw','exposure','paint']:
            if bm[view].get(field)!=meta[view].get(field):raise ValueError('Comparison changed '+field+' in '+view)
        panels=[];crops=[];original_sizes=[]
        canonical_size=Image.open(before/(view+'.png')).size
        for path in [before/(view+'.png'),directory/(view+'.png')]:
            im=Image.open(path).convert('RGB');original_sizes.append(im.size)
            if im.size!=canonical_size:im=im.resize(canonical_size,Image.Resampling.LANCZOS)
            crop=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(rect));crops.append(crop)
            im=im.crop(crop);im.thumbnail((1000,900),Image.Resampling.LANCZOS);panels.append(im)
        height=max(im.height for im in panels);canvas=Image.new('RGB',(2000,height+48),(228,231,234));draw=ImageDraw.Draw(canvas)
        for k,im in enumerate(panels):
            draw.text((1000*k+14,10),('Surface checkpoint / ' if k==0 else 'Delivery / ')+name,font=font,fill=(20,30,35))
            canvas.paste(im,(1000*k+(1000-im.width)//2,48))
        canvas.save(out/('compare-'+name+'.jpg'),quality=94,optimize=True)
        records[name]=dict(view=view,crops=crops,original_sizes=original_sizes,comparison_size=canonical_size,
            before_sha256=bm[view]['source_sha256'],after_sha256=meta[view]['source_sha256'],same_camera_paint_exposure=True,
            resampling='Delivery downsampled to the original render size before identical pixel crops when native sizes differ')
    (out/'comparisons.json').write_text(json.dumps(records,indent=2));print('H120_DELIVERY_CROPS',len(records))
if __name__=='__main__':main()
