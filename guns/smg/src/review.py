"""Current-export provenance, dimensioned orthos and all-view checkpoint sheets."""
import hashlib,json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),17)

def panel(path,size):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(107,111,115,255));bg.alpha_composite(im)
 return ImageOps.contain(bg.convert('RGB'),size,Image.Resampling.LANCZOS)
def sheet(path,items,columns=3,cell=(600,420)):
 w,h=cell;out=Image.new('RGB',(w*columns,h*math.ceil(len(items)/columns)),(237,239,235));d=ImageDraw.Draw(out)
 for i,(name,p) in enumerate(items):
  x=i%columns*w;y=i//columns*h;d.text((x+12,y+9),name,font=SMALL,fill=(25,40,34))
  im=panel(p,(w-8,h-44));out.paste(im,(x+(w-im.width)//2,y+38+(h-44-im.height)//2))
 out.save(path,quality=93,optimize=True);return out

def main():
 rows=[]
 for folder in ('beauty','photos','source-photos','loaded','empty','cartridge','case'):
  meta=json.loads((OUT/folder/'shots.json').read_text())
  for name,r in meta.items():
   p=Path(r['source']);assert r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),(folder,name,'stale')
   assert p.suffix==('.blend' if folder=='source-photos' else '.glb')
   rows.append(dict(group=folder,shot=name,source=p.name,sha256=r['sha256'],engine=r['engine']))
 timing=json.loads((OUT/'strips/timing.json').read_text())
 for clip,t in timing.items():
  for name,r in json.loads((OUT/'strips'/clip/'shots.json').read_text()).items():
   p=Path(r['source']);assert r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
   rows.append(dict(group='strips',shot=name,source=p.name,sha256=r['sha256'],engine=r['engine']))
  with Image.open(OUT/'strips'/(clip+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
  assert duration==t['duration_ms'],(clip,duration,t['duration_ms'])
 checks=json.loads((BASE/'build/check.json').read_text());assert checks['passed']
 geometry=checks['bounds_m']['size'];length=checks['barrel_length_m']
 orthos=[]
 for n,label in [('side',f'Overall {geometry[1]*1000:.2f} mm | barrel {length*1000:.2f} mm'),
                 ('top',f'Maximum width {geometry[0]*1000:.2f} mm'),('front',f'Total height {geometry[2]*1000:.2f} mm')]:
  im=panel(OUT/'beauty'/(n+'.png'),(1440,660));canvas=Image.new('RGB',(1440,im.height+100),(237,239,235));d=ImageDraw.Draw(canvas)
  d.text((20,12),n.title()+' orthographic / actual evaluated mesh',font=FONT,fill=(25,40,34))
  canvas.paste(im,((1440-im.width)//2,53));d.text((20,im.height+65),label,font=FONT,fill=(25,40,34))
  p=OUT/(n+'-dimensions.jpg');canvas.save(p,quality=94);orthos.append((n+' / measured envelope',p))
 sheet(OUT/'dimensions.jpg',orthos,1,(1440,600))
 beauty=[(n.replace('_',' '),OUT/'beauty'/(n+'.png')) for n in json.loads((OUT/'beauty/shots.json').read_text())]
 extras=[('Loaded magazine',OUT/'loaded/mag_standalone.png'),('Loaded / lips',OUT/'loaded/mag_lips.png'),
  ('Empty magazine',OUT/'empty/mag_standalone.png'),('Empty / follower',OUT/'empty/mag_lips.png'),
  ('9 mm cartridge',OUT/'cartridge/cartridge.png'),('Fired case / open mouth',OUT/'case/case_mouth.png'),('Fired case / head and rim',OUT/'case/case.png')]
 sheet(OUT/'contact-sheet.jpg',beauty+extras)
 sheet(OUT/'photo-pairs.jpg',[(n,OUT/'pairs'/(n+'-pair.jpg')) for n in ('right_photo','left_photo','locked_photo','stock_photo','trigger_photo')],1,(1800,950))
 # Every strip frame appears in the individual strips. This overview retains
 # uniformly selected poses and explicit real duration labels.
 cliprows=[]
 for clip,t in timing.items():
  fs=sorted((OUT/'strips'/clip).glob('*.png'));picks=sorted(set(round(i*(len(fs)-1)/4) for i in range(5)))
  cliprows.append((clip,t,[fs[i] for i in picks]))
 canvas=Image.new('RGB',(1800,285*len(cliprows)),(237,239,235));d=ImageDraw.Draw(canvas)
 for i,(clip,t,fs) in enumerate(cliprows):
  y=i*285;d.text((12,y+7),f"{clip} / {t['duration_ms']} ms / uniformly timed GLB samples",font=SMALL,fill=(25,40,34))
  for j,p in enumerate(fs):im=panel(p,(350,244));canvas.paste(im,(j*360,y+33))
 canvas.save(OUT/'clips.jpg',quality=92,optimize=True)
 # Dedicated inspection sheets include every rendered clip sample, not only
 # the five-pose overview, so the reviewer can inspect intermediate frames.
 frames=[(clip+' / '+p.stem,p) for clip in timing for p in sorted((OUT/'strips'/clip).glob('*.png'))]
 folder=OUT/'inspection';folder.mkdir(exist_ok=True)
 for i in range(0,len(frames),18):sheet(folder/f'clips-{i//18:02d}.jpg',frames[i:i+18],3,(600,510))
 allrecords=dict(passed=True,render_records=len(rows),records=rows,clip_timing=timing,
  stage='checkpoint constants; no PBR or UV acceptance',triangles=checks['triangles'])
 (BASE/'build/provenance.json').write_text(json.dumps(allrecords,indent=2))
 print('CHECKPOINT REVIEW',len(rows),'current-source renders;',len(frames),'clip frames;',OUT/'contact-sheet.jpg',flush=True)
if __name__=='__main__':main()
