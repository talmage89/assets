"""Native fixed-camera before/after proof. Never creates docs or edits photos."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact

font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),24)
out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True);rows=[]
for seed in (117,228,339):
    for shot in ('hero','above','table','counter','awning','walkup'):
        old=Path(f'build/before-lookdev/renders/checkpoint/{seed}/{shot}.png');new=Path(f'renders/lookdev/{seed}/{shot}.png')
        if not old.exists() or not new.exists():continue
        a=json.loads(old.with_suffix('.json').read_text());b=json.loads(new.with_suffix('.json').read_text())
        assert a['recipe']==b['recipe'],('Camera changed',seed,shot)
        im1=Image.open(old).convert('RGB');im2=Image.open(new).convert('RGB');w=min(im1.width,im2.width);assert w>=800
        h=round(im1.height*w/im1.width);canvas=Image.new('RGB',(2*w,h+56),'#e5e5dc');d=ImageDraw.Draw(canvas)
        for i,(im,title) in enumerate(((im1,'Before / 0b013bb'),(im2,'After / exported PBR site'))):
            canvas.paste(im.resize((w,h),Image.Resampling.LANCZOS),(i*w,56));d.text((i*w+14,12),f'{seed} / {shot} / {title}',font=font,fill='#25372f')
        path=out/f'{seed}-{shot}.jpg';canvas.save(path,quality=94);rows.append(dict(seed=seed,shot=shot,width_each=w,path=str(path),camera=a['recipe']))
Path('build/before-after.json').write_text(json.dumps(rows,indent=2)+'\n')
contact([Path(r['path']) for r in rows],out/'contact.jpg',width=2000,title='Fixed cameras / form and site corrections')
print('BEFORE AFTER',len(rows),'pairs, each >=800px wide')
