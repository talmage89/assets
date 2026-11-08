"""Native-size before/after panels for every requested correction."""
import argparse,json,sys,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from final_baseline import ensure,frame
parser=argparse.ArgumentParser();parser.add_argument('--after',default='renders/final');parser.add_argument('--matches');parser.add_argument('--out',default='renders/fix-crops');args=parser.parse_args()
pairs=ensure(args.after,matches=args.matches);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(find_font('DejaVu Sans','Book'),24);rows={}
regions={'town':(0,.05,.70,.95),'traffic':(.25,.18,.95,1),'grass':(0,.30,.70,1),'concrete':(0,0,.8,1)}
for label,old,new,seed,isolated in pairs:
 before=Path('renders/before-final')/(old+'.png');after=frame(args.after,new,args.matches)
 a,b=[Image.open(p).convert('RGB') for p in (before,after)]
 ar,br=[json.loads(p.with_suffix('.json').read_text()) for p in (before,after)]
 assert all(ar['camera'].get(k)==br['camera'].get(k) for k in ('location','target','lens','aspect')),(label,'projection differs')
 assert min(a.width,b.width)>=800,(label,'insufficient native width')
 region=regions.get(label,(0,0,1,1));boxes=[];panels=[]
 for im in (a,b):
  box=tuple(round(v*(im.width if k%2==0 else im.height)) for k,v in enumerate(region))
  boxes.append(box);panels.append(im.crop(box))
 a,b=panels;assert min(a.width,b.width)>=800,(label,'native crop too narrow')
 # Native source pixels within each ROI; never enlarge or resample a panel.
 w=max(a.width,b.width);h=max(a.height,b.height);im=Image.new('RGB',(2*w,h+50),(24,29,26));d=ImageDraw.Draw(im)
 im.paste(a,((w-a.width)//2,50));im.paste(b,(w+(w-b.width)//2,50));d.text((16,11),label+' / BEFORE',font=font,fill=(231,234,226));d.text((w+16,11),'AFTER / exported PBR',font=font,fill=(231,234,226))
 path=out/(label+'.jpg');im.save(path,quality=95)
 rows[label]=dict(before=str(before),after=str(after),panel_widths=[a.width,b.width],native_crop_boxes=boxes,normalized_crop_region=region,camera={k:br['camera'][k] for k in ('location','target','lens','aspect')},before_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),after_sha256=hashlib.sha256(after.read_bytes()).hexdigest(),scope='Identical projection, native pixels. Lighting may change for the requested sky/value correction; bearing surroundings intentionally change from isolated module to full scene.')
(out/'cameras.json').write_text(json.dumps(rows,indent=2));print('FINAL FIX CROPS',len(rows),'native identical-camera pairs')
