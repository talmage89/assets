"""Ignored form sheets and source/image provenance gate; never writes docs/."""
import hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font
from plan import generate,PROOF_SEEDS,rotate
from check_plan import path,rect
from context import recipe
FONT=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)


def sheet(entries,out,columns=2,cell=(800,520)):
 rows=math.ceil(len(entries)/columns);canvas=Image.new('RGB',(columns*cell[0],rows*cell[1]),'#e8e9e6');d=ImageDraw.Draw(canvas)
 for i,(label,path) in enumerate(entries):
  im=Image.open(path).convert('RGB');im.thumbnail((cell[0]-16,cell[1]-48),Image.Resampling.LANCZOS)
  x=(i%columns)*cell[0];y=(i//columns)*cell[1]
  canvas.paste(im,(x+(cell[0]-im.width)//2,y+40));d.text((x+12,y+8),label,font=FONT,fill='#26352f')
 Path(out).parent.mkdir(parents=True,exist_ok=True);canvas.save(out,quality=90,optimize=True)
 return str(out)


def circulation(out):
 ims=[]
 for seed in PROOF_SEEDS:
  p=generate(seed);W,D=p['lot'];scale=13
  im=Image.new('RGB',(800,840),'#e9eae7');d=ImageDraw.Draw(im)
  def xy(p):
   x,y=rotate(p,generate(seed)['yaw']);return (400+x*scale,430-y*scale)
  def poly(points,fill,outline=None):d.polygon([xy(v) for v in points],fill=fill,outline=outline)
  poly([(-W/2,-D/2),(W/2,-D/2),(W/2,D/2),(-W/2,D/2)],'#777c79','#333b35')
  b=p['building'];poly(rect((b['center_x'],b['front']+b['depth']/2),b['width'],b['depth'],0),'#d2c9b4')
  poly(rect((b['center_x'],(p['parking_front']+b['front']-p['walk'])/2),b['width'],p['parking_depth'],0),'#b7bdc0')
  for island in p['islands']:poly(rect(island['center'],p['canopy']['island'][0],p['canopy']['island'][1],p['canopy']['angle']),'#ebebe4')
  route=path(p);d.line([xy((x,y)) for x,y,yaw in route],fill='#fee788',width=4)
  for x,y,yaw in route[::45]:poly(rect((x,y),2.14,5.7,yaw),None,'#d84328')
  for drive in p['driveways']:
   x,y=xy(drive['center']);d.ellipse((x-7,y-7,x+7,y+7),fill='#eefaf8',outline='black')
  d.text((20,15),f'{seed} / {p["brand"].upper()} / corner yaw {p["yaw"]}',font=FONT,fill='#20332b')
  d.text((20,780),'5.70 x 2.14 m pickup; 4.8 m center radius',font=FONT,fill='#20332b')
  # World north is up in this orthographic diagram.
  d.text((735,75),'N ↑',font=FONT,fill='#20332b')
  file=Path('build')/f'circulation-{seed}.jpg';im.save(file,quality=90);ims.append((str(seed),file))
 sheet(ims,out,2,(800,860))


def main():
 root=Path('renders/checkpoint');names=['hero','above','dispenser','canopy','entry','sign','rear','scale','motion']
 entries=[(n,root/(n+'.png')) for n in names if (root/(n+'.png')).exists()]
 family=[]
 for seed in PROOF_SEEDS:
  for name in ('above','street'):
   file=root/'seeds'/str(seed)/(name+'.png')
   if file.exists():family.append((f'{seed} / {name}',file))
 if family:sheet(family,root/'family.jpg',2,(900,640))
 if entries:sheet(entries,root/'details.jpg',2,(850,600))
 all_entries=entries+family
 for name in ('period_canopy','period_dispenser'):
  f=Path('renders/matches')/(name+'-pair.jpg')
  if f.exists():all_entries.append((name,f))
 if all_entries:sheet(all_entries,root/'contact.jpg',3,(700,480))
 circulation(root/'circulation.jpg')
 # Prove every checkpoint view still names its current source and actual PNG.
 reports=[]
 files=list(root.rglob('provenance.json'))
 if Path('renders/matches/provenance.json').exists():files.append(Path('renders/matches/provenance.json'))
 current_recipe=recipe()
 for file in files:
  for name,r in json.loads(file.read_text()).items():
   assert r['recipe_sha256']==current_recipe,'Stale render recipe'
   assert hashlib.sha256(Path(r['source']).read_bytes()).hexdigest()==r['sha256'],'Stale source '+str(file)
   assert hashlib.sha256((file.parent/(name+'.png')).read_bytes()).hexdigest()==r['image_sha256'],'Stale image'
   reports.append(str(file.parent/(name+'.png')))
 Path('build/view-check.json').write_text(json.dumps(dict(passed=True,checked_views=reports,stage='form only, no final bake or docs'),indent=2))
 print('REVIEW',len(reports),'current source/image views, sheets in',root)

if __name__=='__main__':main()
