"""Native/4x upper-land comparisons, backed by 2-D hero measurements."""
from pathlib import Path
import argparse,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from finish_review import camera
from kit.photo_match import project
from kit.fonts import find_font
from wear_2d_review import LENGTH

def build(beauty_dir=None):
    out=BASE/'renders/final/pairs'
    values=json.loads((out/'wear-2d-values.json').read_text())
    beauty=Path(beauty_dir) if beauty_dir else BASE/'renders/final/beauty'
    hero=Image.open(beauty/'hero.png').convert('RGBA')
    bg=Image.new('RGBA',hero.size,(108,111,114,255));bg.alpha_composite(hero)
    meta=json.loads((beauty/'shots.json').read_text())['hero']
    baseline=project(camera(meta),np.array([(-.0164,-.040,.096),(-.0164,.190,.096)]),hero.width,hero.height)[0]
    scale=np.linalg.norm(baseline[1]-baseline[0])/1090
    reference=Image.open(BASE/'build/white-balanced/navy2.png').convert('RGB')
    pairs=[];crops=[]
    for i,label in enumerate(('Forward / well rubbing','Middle / paint islands','Aft / edge bites')):
        ya=.140-i*LENGTH/3000;yb=.140-(i+1)*LENGTH/3000
        points=np.array([(x,y,z) for x in (-.017,-.012) for y in (ya,yb) for z in (.1105,.1245)])
        xy=project(camera(meta),points,hero.width,hero.height)[0]
        lo=np.floor(xy.min(0)).astype(int)-2;hi=np.ceil(xy.max(0)).astype(int)+2
        box=tuple(map(int,(*lo,*hi)));crop=bg.convert('RGB').crop(box)
        x0=round(1900+i*738/3);x1=round(1900+(i+1)*738/3)
        photo_box=(x0,268,x1,354);photo=reference.crop(photo_box)
        common=photo.resize((round(photo.width*scale),round(photo.height*scale)),Image.Resampling.LANCZOS)
        pairs.append((label,crop,common,photo));crops.append(dict(label=label,hero_crop_native=list(box),photo_crop_native=list(photo_box)))
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
    for native,name in ((False,'chips-4x-pair'),(True,'chips-native-4x-pair')):
        panels=[(label,left.resize((left.width*4,left.height*4),Image.Resampling.NEAREST),
                 (ref if native else common).resize(((ref if native else common).width*4,(ref if native else common).height*4),Image.Resampling.NEAREST))
                for label,left,common,ref in pairs]
        cw=max(700,max(max(a.width,b.width) for _,a,b in panels)+30)
        rh=max(max(a.height,b.height) for _,a,b in panels)+55
        canvas=Image.new('RGB',(cw*2,rh*3+200),(228,229,225));d=ImageDraw.Draw(canvas)
        d.text((16,12),'EXPORTED HERO / native pixels x4',font=font,fill=(20,30,25))
        d.text((cw+16,12),'PHOTO / '+('native pixels x4 (higher pixel density)' if native else 'common receiver scale, then x4'),font=font,fill=(20,30,25))
        for i,(label,left,right) in enumerate(panels):
            y=45+i*rh
            for col,panel in enumerate((left,right)):
                d.text((col*cw+16,y),label,font=font,fill=(20,30,25))
                canvas.paste(panel,(col*cw+(cw-panel.width)//2,y+26))
        for col,key in enumerate(('shipping','photo')):
            row=values[key];wr=row['worn_regions'];pr=row['paint_islands'];y=45+3*rh
            lines=[f"2-D worn share: {row['worn_share']:.1%}; forward/middle/aft "+' / '.join(f'{x:.0%}' for x in row['thirds_forward_middle_aft']),
                   f"Largest worn component: {wr['largest'][0]['area_mm2']:.1f} mm2 / {wr['largest_share_of_phase']:.0%} of wear",
                   f"Paint regions: {pr['count']}; enclosed islands: {pr['complete_count']}",
                   'See wear-2d-pair.jpg and wear-2d-values.json for masks, profiles and 2-D sizes.',
                   'No contrast adjustment. 4x is exact nearest-neighbor pixel replication.']
            for j,line in enumerate(lines):d.text((col*cw+16,y+j*25),line,font=font,fill=(20,30,25))
        canvas.save(out/(name+'.png'));canvas.save(out/(name+'.jpg'),quality=97)
    result=dict(crops=crops,reference_to_hero_scale=float(scale),enlargement=4,
                acceptance='2-D area/connectivity in wear-2d-values.json; longitudinal chip runs are superseded.',
                hero_native_size=list(hero.size),contrast_changed=False)
    (out/'chip-distribution.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--beauty');a=p.parse_args();print(json.dumps(build(a.beauty),indent=2))
