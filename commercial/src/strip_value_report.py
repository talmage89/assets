"""Native hero crops and explicit old/new-frame asphalt comparison receipts."""
import json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.fonts import find_font
from strip_measure import CASES,patch
from strip_value_controls import digest


def values(im,box):
    a=np.asarray(im.convert('RGB'),dtype='float32')/255;h,w=a.shape[:2]
    x0,y0,x1,y1=[round(v*(w if i%2==0 else h)) for i,v in enumerate(box)]
    q=a[y0:y1,x0:x1];y=q@np.array([.2126,.7152,.0722])
    return dict(box_fraction=box,median_Yprime=float(np.median(y)),Yprime_p10_p90=np.percentile(y,[10,90]).tolist(),median_RGB=np.median(q,axis=(0,1)).tolist())


def run():
    out=Path('renders/strip/values');out.mkdir(parents=True,exist_ok=True)
    before=Path('build/strip-value/before');lot=Path('renders/strip/matches/period_lot.png');cal=json.loads(Path('build/strip/cameras.json').read_text())['period_lot']
    photo_path=Path(cal['photo']);photo=Image.open(photo_path).convert('RGB');render=Image.open(lot).convert('RGB')
    # Three visibly sunlit native-photo patches, rather than calling the
    # unusually bright right corner representative of the entire wearing course.
    rectangles=((120,555,280,600),(350,560,530,600),(660,555,900,600))
    photo_rows=[values(photo,tuple(v/(photo.width if i%2==0 else photo.height) for i,v in enumerate(r))) for r in rectangles]
    render_rows=[values(render,box) for box in ((.84,.72,.98,.77),(.84,.79,.98,.84),(.84,.85,.98,.90))]
    result=dict(scope=__doc__,photo_sha256=digest(photo_path),render_sha256=digest(lot),sunlit_photo_patches=photo_rows,sunlit_render_patches=render_rows,current_wear=json.loads(Path('renders/strip/measurements/wear-values.json').read_text())['rows'])
    for im,rows,name in ((photo,photo_rows,'photo-sunlit-patches.jpg'),(render,render_rows,'render-sunlit-patches.jpg')):
        mark=im.copy();d=ImageDraw.Draw(mark)
        for i,row in enumerate(rows):
            box=tuple(round(v*(mark.width if k%2==0 else mark.height)) for k,v in enumerate(row['box_fraction']));d.rectangle(box,outline='#E97725',width=2);d.text((box[0]+3,box[1]+2),str(i+1),fill='#FFDB87')
        mark.save(out/name,quality=94)
    if before.exists():
        accepted=json.loads((before/'renders/strip/measurements/wear-values.json').read_text());result['accepted_wear']=accepted['rows']
        # The historical metric is retained separately; never silently call
        # a moved camera/rectangle a direct before/after material experiment.
        baseline=Path('renders/strip/value-before-reframed/period_lot.png')
        if baseline.exists():
            im=Image.open(baseline).resize((1440,round(1440/cal['shot']['aspect'])),Image.Resampling.LANCZOS)
            result['same_camera_before_asphalt']=patch(im,CASES['period_asphalt']['render_box'],out/'reframed-before-mask.png')
            result['same_camera_before_sha256']=digest(baseline)
        paths=[before/'renders/strip/checkpoint/hero.png',Path('renders/strip/checkpoint/hero.png')];crops=[];hero=[]
        for path in paths:
            im=Image.open(path).convert('RGB');hero.append(values(im,(.16,.90,.70,.99)));crops.append(im.crop((0,round(im.height*.70),im.width,im.height)))
        assert all(im.width>=800 for im in crops)
        w=max(im.width for im in crops);plate=Image.new('RGB',(w,sum(im.height for im in crops)+100),'#E9E7DF');d=ImageDraw.Draw(plate);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),23);yy=0
        for label,im in zip(('Before / accepted f0f9981 / native pixels','After / exported strip glTF / native pixels'),crops):
            d.text((14,yy+9),label,font=font,fill='#26302A');plate.paste(im,(0,yy+48));yy+=im.height+50
        plate.save(out/'hero-lot-before-after.jpg',quality=96,optimize=True)
        result['hero_lot_before_after']=hero
    (out/'value-round.json').write_text(json.dumps(result,indent=2)+'\n')
    print('STRIP VALUE ROUND photo sunlit medians',[round(r['median_Yprime'],3) for r in photo_rows],'; strip',[round(r['median_Yprime'],3) for r in render_rows])

if __name__=='__main__':run()
