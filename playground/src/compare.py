"""Native fixed-camera before/after panels, kept out of documentation history."""
import json,sys,argparse,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,default=Path('renders/before'));p.add_argument('--after',type=Path,default=Path('renders/lookdev'));p.add_argument('--out',type=Path,default=Path('renders/comparisons'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
shots=[f'{s}/{name}' for s in (101,202,303) for name in ('hero','above')]+['stairs','transfer','clamp-deck','arch-swing','swing-seat','bucket-seat','swing-hanger','swing-hollow']
shots += ['matches/'+n for n in ('used-deck-2009','used-swings-2009','used-stair-2005') if (a.before/'matches'/(n+'.png')).exists()]
report={};paths=[]
for name in shots:
    old=a.before/(name+'.png');new=a.after/(name+'.png');im0=Image.open(old).convert('RGB');im1=Image.open(new).convert('RGB');j0=json.loads(old.with_suffix('.json').read_text());j1=json.loads(new.with_suffix('.json').read_text())
    assert im0.size==im1.size,(name,im0.size,im1.size)
    difference=float(np.max(np.abs(np.array(j0['camera_location'])-j1['camera_location'])));lens=abs(j0['lens_mm']-j1['lens_mm']);assert difference<1e-6 and lens<1e-6,(name,difference,lens)
    if 'camera_matrix_world' in j0 and 'camera_matrix_world' in j1:assert np.max(abs(np.array(j0['camera_matrix_world'])-np.array(j1['camera_matrix_world'])))<1e-6,name
    w,h=im0.size;assert w>=800
    out=Image.new('RGB',(w*2,h+60),(237,238,234));out.paste(im0,(0,60));out.paste(im1,(w,60));d=ImageDraw.Draw(out);font=ImageFont.truetype(find_font('Noto Sans'),24)
    d.text((18,14),'Before / '+name,font=font,fill=(24,36,31));d.text((w+18,14),'After / same authored camera',font=font,fill=(24,36,31))
    target=a.out/(name.replace('/','-')+'.jpg');out.save(target,quality=95,optimize=True);paths.append(target)
    report[name]=dict(camera_origin_max_difference_m=difference,lens_difference_mm=lens,panel_width=w,before_source=j0['source'],after_source=j1['source'],after_bundle=j1.get('resource_bundle_sha256'),scope='Recorded origins/lenses and identical authored shot definitions; quick before and baked after')
(a.out/'cameras.json').write_text(json.dumps(report,indent=2));contact(paths,a.out/'contact.jpg',width=2400,title='Playground / fixed-camera form and look corrections / native pairs alongside')
print('PAIRS',len(paths),a.out)

# Reference plans are comparison evidence only. No raster enters the asset,
# UV generator or baked maps. Original layouts borrow relationships, not lines.
plans=[
    (101,'eastview-1995.pdf',1,(.29,.23,.64,.80),'Eastview / sheet 2 / 10 July 1995',
     'Connected composite and swing containment; entrance ramp, walk, benches and shade.',
     'Original school variant: straight timber/EWF replaces the plan\'s curved curb/play sand.'),
    (202,'lively-2005.pdf',31,(.17,.27,.65,.64),'Lively / plan diagram / August 2005 in approved October 2005 plan',
     'Playground beside picnic space, parking and a circulating path under retained trees.',
     'Original compact park: no recreation-center building or pool is reproduced.'),
    (303,'simon-2013.pdf',1,(.40,.05,.94,.90),'Simon / L1.0 / 28 February 2013',
     'Curved soft-surface area, accessible approach, loop circulation, open lawn and shade.',
     'Original smaller neighborhood variant; the school building is outside this installation.'),
]
scratch=Path('build/plan-evidence');scratch.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(find_font('Noto Sans'),20)
for seed,filename,page,crop,title,relation,limitation in plans:
    prefix=scratch/str(seed)
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','2000','-png',str(Path('refs')/filename),str(prefix)],check=True)
    ref=Image.open(prefix.with_suffix('.png')).convert('RGB');w,h=ref.size
    ref=ref.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(crop)))
    right=Image.open(a.after/str(seed)/'above.png').convert('RGB')
    canvas=Image.new('RGB',(2400,1280),(241,241,236));canvas.paste(ImageOps.contain(ref,(1180,1080)),(10,60));canvas.paste(right,(1200,60));draw=ImageDraw.Draw(canvas)
    for xy,txt in [((16,15),title),((1216,15),f'Seed {seed} / exported layout with use zones'),((16,1160),relation),((16,1200),limitation),((16,1240),'Reference only: '+filename+'; full attribution and direct URL in refs/SOURCES.md')]:draw.text(xy,txt,font=font,fill=(22,35,29))
    canvas.save(a.out/f'layout-{seed}.jpg',quality=94,optimize=True)
