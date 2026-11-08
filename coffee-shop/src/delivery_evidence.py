"""Native fixed-camera crops, with explicit provenance and no image enlargement."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact
font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)
ap=argparse.ArgumentParser();ap.add_argument('--renders',type=Path,default=Path('renders/final'));args=ap.parse_args()
out=Path('renders/delivery-fixes');out.mkdir(parents=True,exist_ok=True);rows=[]
for seed in (117,228,339):
    for name in ('retained','above','site','table','awning','counter','use','wear','door','rail','hero'):
        old=out/'before'/f'{seed}-{name}.png';new=args.renders/str(seed)/(name+'.png')
        if not new.exists():continue
        a=json.loads(old.with_suffix('.json').read_text());b=json.loads(new.with_suffix('.json').read_text())
        assert a['recipe']==b['recipe'],('Different cameras',seed,name,a['recipe'],b['recipe'])
        im1=Image.open(old).convert('RGB');im2=Image.open(new).convert('RGB');assert im1.size==im2.size
        # Keep the native panel width: details cannot be faked by upscaling.
        if name in ('table','awning','counter','use','wear','door'):
            width=min(1000,im1.width);left=(im1.width-width)//2
            rect=(left,24,left+width,im1.height-24)
        else:rect=(0,0,im1.width,im1.height)
        w=rect[2]-rect[0];h=rect[3]-rect[1];assert w>=800
        canvas=Image.new('RGB',(2*w,h+48),'#e5e5dc');d=ImageDraw.Draw(canvas)
        for i,(im,title) in enumerate(((im1,'Before / 37e6af3'),(im2,'After / exported baked PBR'))):
            canvas.paste(im.crop(rect),(i*w,48));d.text((i*w+12,10),f'{seed} / {name} / {title}',font=font,fill='#25372f')
        path=out/f'{seed}-{name}.jpg';canvas.save(path,quality=96)
        rows.append(dict(seed=seed,view=name,width_each=w,rect=rect,path=str(path),camera=b['recipe'],before_revision='37e6af3',before_bundle_sha256=a['bundle_sha256'],after_bundle_sha256=b['bundle_sha256'],before_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),after_sha256=b['image_sha256']))
    if seed in (228,339) and (args.renders/str(seed)/'retained.png').exists():
        old=out/'before'/f'{seed}-retained.png';new=args.renders/str(seed)/'hero.png';im1=Image.open(old).convert('RGB');im2=Image.open(new).convert('RGB');w,h=im1.size
        canvas=Image.new('RGB',(w*2,h+48),'#e5e5dc');d=ImageDraw.Draw(canvas)
        for i,(im,title) in enumerate(((im1,'Before / accepted wide composition'),(im2,'After / closer storefront composition'))):
            canvas.paste(im,(i*w,48));d.text((i*w+12,10),title,font=font,fill='#25372f')
        path=out/f'{seed}-framing.jpg';canvas.save(path,quality=96)
        rows.append(dict(seed=seed,view='framing',width_each=w,path=str(path),different_cameras=True,limits='Composition change only; same-camera geometry/light proofs are separate'))
Path('build/delivery-corrections.json').write_text(json.dumps(rows,indent=2)+'\n')
contact([Path(r['path']) for r in rows],out/'contact.jpg',width=2000,title='Coffee shops / fixed cameras / delivery corrections')
print('DELIVERY CORRECTIONS',len(rows),'native pairs')
