"""Original comparison sheets and a GLB-hash-checked image manifest, no docs."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),15)

def rgb(path):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im);return bg.convert('RGB')
def sheet(entries,path,columns=3,cell=(600,390)):
 w,h=cell;out=Image.new('RGB',(columns*w,((len(entries)+columns-1)//columns)*h),(32,35,38));d=ImageDraw.Draw(out)
 for i,(name,p) in enumerate(entries):
  im=ImageOps.contain(rgb(p),(w-12,h-42),Image.Resampling.LANCZOS);x=(i%columns)*w;y=(i//columns)*h
  out.paste(im,(x+(w-im.width)//2,y+35+(h-42-im.height)//2));d.text((x+12,y+7),name,font=SMALL,fill='white')
 out.save(path,quality=94)

def main():
 out=BASE/'renders/final';entries=[];manifest={}
 for folder in [out/'beauty',out/'eevee',out/'photos',*[out/'detachables'/n for n in ('box_loaded','box_empty','cartridge','case','link')],*[out/'precedents'/n for n in ('ak','smg')],*[out/'wear'/n for n in ('receiver','cover','handle','flash','regulator','ports','feet','box','butt')]]:
  p=folder/'shots.json'
  if not p.exists():continue
  for name,row in json.loads(p.read_text()).items():
   source=Path(row['source']);assert source.suffix=='.glb'
   assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],str(p)
   image=folder/(name+'.png');assert image.exists()
   entries.append((str(image.relative_to(out)),image));manifest[str(image.relative_to(out))]=dict(source=str(source.relative_to(BASE)) if source.is_relative_to(BASE) else '../'+str(source.relative_to(BASE.parent)),sha256=row['sha256'])
 for p in sorted((out/'pairs').glob('*-pair.jpg')):entries.append(('GLB photo pair / '+p.stem,p))
 for p in sorted((out/'source-pairs').glob('*-pair.jpg')):entries.append(('Dense source pair / '+p.stem,p))
 if (out/'look-review/finish-values.json').exists():
  for p in sorted((out/'look-review').glob('*.jpg')):entries.append((p.stem,p))
 for i in range(0,len(entries),12):sheet(entries[i:i+12],out/f'review-page-{i//12+1:02d}.jpg')
 sheet(entries,out/'contact-sheet.jpg',columns=4,cell=(420,280))
 hero=out/'beauty/hero.png';ak=out/'precedents/ak/ak_hero.png';smg=out/'precedents/smg/smg_hero.png'
 if all(p.exists() for p in (hero,ak,smg)):
  sheet([('Harrow 56 / same lights and exposure',hero),('Rill 39 / same lights and exposure',ak),('Relay 9 / same lights and exposure',smg)],out/'hero-beside-ak-smg.jpg',columns=1,cell=(1600,900))
 (BASE/'build/final-presentation.json').write_text(json.dumps(dict(images=manifest,count=len(manifest),no_docs=True),indent=2))
 print('FINAL PRESENTATION',len(manifest),'GLB-verified renders',len(entries),'sheet entries')
if __name__=='__main__':main()
