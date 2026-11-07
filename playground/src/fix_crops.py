"""Native-pixel crops with camera and exported-resource receipts; ignored output."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,default=ROOT/'build/playground-before/renders/lookdev');p.add_argument('--after',type=Path,default=Path('renders/fixes'));p.add_argument('--out',type=Path,default=Path('renders/fix-crops'));p.add_argument('--only',default='all');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
specs={
 '1-fiber-and-hollow':('swing-hollow',(0,0,1200,857)),
 '2-raking-sun-1996':('101/hero',(160,110,1160,790)),
 '2-raking-sun-2005':('202/hero',(180,120,1180,790)),
 '2-raking-sun-2013':('303/hero',(100,160,1200,790)),
 '3-school-age':('101/hero',(180,130,1050,680)),
 '3-middle-years':('202/hero',(200,160,1100,690)),
 '3-newer-contact':('303/hero',(280,240,1180,700)),
 '4-open-step-decks':('transfer',(0,0,1200,857)),
 '5-poured-rubber':('rubber-wear',(0,0,1200,857)),
 '5-patch-and-seam':('rubber-seams',(0,0,1200,857)),
 '1-fiber-carryout':('fiber-carryout',(0,0,1200,857)),
 '1-slide-exit':('slide-exit',(0,0,1200,857)),
 '3-clamp-chips':('clamp-deck',(0,0,1200,857))}
if (a.after/'matches/used-swings-2009.png').exists():specs['6-swings-on-fiber']=('matches/used-swings-2009',(0,0,1200,669))
font=ImageFont.truetype(find_font('Noto Sans'),23);report={};paths=[]
for name,(shot,rect) in specs.items():
 if a.only!='all' and name not in a.only.split(','):continue
 before=a.before/(shot+'.png')
 if name.startswith('6-') or shot in ('rubber-seams','fiber-carryout'):before=Path('renders/fixes-before')/(shot+'.png')
 after=a.after/(shot+'.png');j0=json.loads(before.with_suffix('.json').read_text());j1=json.loads(after.with_suffix('.json').read_text())
 diff=float(np.max(abs(np.array(j0['camera_matrix_world'])-j1['camera_matrix_world'])));assert diff<1e-6,(name,diff)
 assert abs(j0['lens_mm']-j1['lens_mm'])<1e-6
 im0=Image.open(before).convert('RGB');im1=Image.open(after).convert('RGB');assert im0.size==im1.size
 x,y,r,b=rect;b=min(b,im0.height);rect=(x,y,r,b);im0=im0.crop(rect);im1=im1.crop(rect);w,h=im0.size;assert w>=800
 # Retain each full-size crop separately, as well as the comparison sheet.
 im0.save(a.out/(name+'-before.png'));im1.save(a.out/(name+'-after.png'))
 out=Image.new('RGB',(w*2,h+48),(237,238,234));out.paste(im0,(0,48));out.paste(im1,(w,48));d=ImageDraw.Draw(out)
 d.text((14,10),'Before / '+name,font=font,fill=(24,36,31));d.text((w+14,10),'After / same camera / native pixels',font=font,fill=(24,36,31));path=a.out/(name+'.jpg');out.save(path,quality=96,optimize=True);paths.append(path)
 report[name]=dict(shot=shot,crop_pixels=rect,panel_width=w,camera_matrix_max_delta=diff,lens_mm=j1['lens_mm'],before= str(before),after=str(after),after_bundle=j1['resource_bundle_sha256'])
(a.out/'receipts.json').write_text(json.dumps(report,indent=2));contact(paths,a.out/'contact.jpg',width=2200,title='Six requested corrections / native crops available alongside');print('FIX CROPS',len(paths))
