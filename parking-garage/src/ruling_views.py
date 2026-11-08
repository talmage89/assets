"""Full native-size 4c63d8c/final comparisons; historical inputs are optional."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from kit.contact import review_sheet
from kit.fonts import find_font


def compose(folder=Path('renders/final')):
    history=Path('build/ruling-before')
    if not (history/'views.json').exists():return
    old=json.loads((history/'views.json').read_text());new=json.loads((folder/'views.json').read_text())
    out=Path('renders/ruling-fixes');out.mkdir(parents=True,exist_ok=True);rows=[];receipt=[]
    for seed,name in ((202,'hero'),(101,'aisle'),(202,'top_deck')):
        before=history/str(seed)/(name+'.png');after=folder/str(seed)/(name+'.png')
        if not after.exists():continue
        a=next(r for r in old if (r['seed'],r['name'])==(seed,name))
        b=next(r for r in new if (r['seed'],r['name'])==(seed,name))
        for key in ('camera','target','lens_mm','sensor_width_mm','width','height'):
            assert a[key]==b[key],(seed,name,key,'Comparison must keep the camera')
        left,right=Image.open(before).convert('RGB'),Image.open(after).convert('RGB')
        assert left.size==right.size and left.width>=800
        w,h=left.size;canvas=Image.new('RGB',(w*2,h+44),(25,28,28));d=ImageDraw.Draw(canvas)
        font=ImageFont.truetype(find_font('DejaVu Sans','Book'),20)
        for x,label in ((12,'Before / 4c63d8c'),(w+12,'After / delivered baked GLB')):d.text((x,12),label,font=font,fill=(230,227,215))
        canvas.paste(left,(0,44));canvas.paste(right,(w,44));path=out/f'{seed}-{name}.jpg';canvas.save(path,quality=95,optimize=True)
        rows.append([path]);receipt.append(dict(seed=seed,name=name,panel_width=w,unchanged_camera=True,before=a['sha256'],after=b['sha256']))
    if rows:review_sheet(rows,out/'contact.jpg',width=2400,title='Final two corrections / same full-size cameras')
    (out/'views.json').write_text(json.dumps(receipt,indent=2)+'\n')
