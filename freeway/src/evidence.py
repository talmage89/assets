"""Native-size identical-camera before/after views, no committed gallery files."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
PAIRS=[('town-diamond','101','above'),('traffic-diamond','101','hero'),('girders','101','pier_girders'),('terminal','101','terminal'),('cut-slopes','101','sign_structure'),('town-backyards','202','above'),('sun-curved','202','hero'),('sound-wall','202','sound_wall')]
font=ImageFont.truetype(find_font('DejaVu Sans','Book'),24);out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True);rows={}
for label,seed,view in PAIRS:
 before=Path(f'renders/before-lookdev/checkpoint/{seed}/{view}.png');after=Path(f'renders/lookdev/{seed}/{view}.png')
 if not before.exists():continue
 a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');old=json.loads(before.with_suffix('.json').read_text());new=json.loads(after.with_suffix('.json').read_text())
 assert old['camera']['location']==new['camera']['location'] and old['camera']['target']==new['camera']['target'],(label,'camera changed')
 w=max(a.width,b.width);h=max(a.height,b.height);canvas=Image.new('RGB',(w*2,h+48),(24,28,27));d=ImageDraw.Draw(canvas)
 # Native pixels are never enlarged; center the smaller view in its panel.
 canvas.paste(a,((w-a.width)//2,48));canvas.paste(b,(w+(w-b.width)//2,48));d.text((16,10),label+' / BEFORE',font=font,fill=(230,235,225));d.text((w+16,10),'AFTER / exported glTF',font=font,fill=(230,235,225));canvas.save(out/(label+'.jpg'),quality=94)
 rows[label]=dict(before=str(before),after=str(after),before_width=a.width,after_width=b.width,camera_location=new['camera']['location'],camera_target=new['camera']['target'],before_and_after_lighting_may_differ=True)
# Labelled module sheets retain their full native widths.
a=Image.open('renders/before-lookdev/checkpoint/modules.png').convert('RGB');b=Image.open('renders/lookdev/modules.png').convert('RGB');w=max(a.width,b.width);canvas=Image.new('RGB',(w,a.height+b.height+100),(24,28,27));canvas.paste(a,(0,50));canvas.paste(b,(0,a.height+100));d=ImageDraw.Draw(canvas);d.text((16,10),'BEFORE / module sheet',font=font,fill=(230,235,225));d.text((16,a.height+60),'AFTER / 1000px individual views',font=font,fill=(230,235,225));canvas.save(out/'modules.jpg',quality=93)
(out/'cameras.json').write_text(json.dumps(rows,indent=2));print('FIX EVIDENCE',len(rows),'identical-camera pairs and module sheets')
