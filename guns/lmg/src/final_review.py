"""Original comparison sheets and a GLB-hash-checked image manifest, no docs."""
import hashlib,json,sys,math
import numpy as np
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
 from final_shots import DEFAULT_SHOTS
 from photo_matches import MATCHES
 required={'beauty':set(DEFAULT_SHOTS.split(',')),'eevee':{'hero'},'photos':set(MATCHES),'raw-check':{'hero','handguard','barrel_handle','belt'}}
 for n in ('box_loaded','box_empty','cartridge','case','link'):required['detachables/'+n]={n}
 for n in ('ak','smg'):required['precedents/'+n]={n+'_hero'}
 for n in ('receiver','cover','handle','flash','regulator','ports','feet','box','butt'):required['wear/'+n]={'hero','hero_right'}
 for folder,names in required.items():
  metadata=out/folder/'shots.json';assert metadata.exists(),str(metadata)
  assert names<=set(json.loads(metadata.read_text())),(folder,'missing shot metadata')
  for name in names:assert (out/folder/(name+'.png')).exists(),(folder,name)
 from image_masks import projection
 for name in ('box_loaded','box_empty','cartridge','case','link'):
  metadata=json.loads((out/'detachables'/name/'shots.json').read_text())[name]
  geometry=np.load(BASE/'build/image-geometry'/(name+'.npz'))
  assert str(geometry['sha256'])==metadata['sha256']
  size=Image.open(out/'detachables'/name/(name+'.png')).size
  pixels,depth=projection(geometry['xyz'].reshape(-1,3),metadata,*size)
  low=pixels.min(0);high=pixels.max(0);margin=np.array(size)*.03
  assert np.all(depth>0) and np.all(low>=margin) and np.all(high<=np.array(size)-margin),(name,'standalone clipping',low,high)
 for folder in ('pairs','source-pairs'):
  for name in MATCHES:assert (out/folder/(name+'-pair.jpg')).exists(),(folder,name)
 raw=json.loads((out/'raw-check/raw-comparison.json').read_text())
 assert raw['source_sha256']==hashlib.sha256((BASE/'export/lmg.glb').read_bytes()).hexdigest()
 controls=json.loads((BASE/'build/control-verification.json').read_text())
 assert controls['passed'] and len(controls['controls'])==9
 wear=json.loads((out/'look-review/wear-values.json').read_text())
 assert len(wear)==9 and all(set(r)=={'hero','hero_right'} for r in wear.values())
 assert all(max(v['changed_area_px'] for v in row.values())>0 for row in wear.values())
 framing=json.loads((BASE/'build/photo-frame-proof.json').read_text())
 assert framing['source_sha256']==hashlib.sha256((BASE/'export/lmg.glb').read_bytes()).hexdigest()
 for name,row in framing['shots'].items():
  x0,y0,x1,y1=row['projected_bounds_after'];w,h=row['frame'];m=row['minimum_margin_fraction']
  assert x0>=w*m and y0>=h*m and x1<=w*(1-m) and y1<=h*(1-m),(name,'clipped whole-gun photo pair')

 for folder in [out/'beauty',out/'eevee',out/'photos',out/'raw-check',*[out/'detachables'/n for n in ('box_loaded','box_empty','cartridge','case','link')],*[out/'precedents'/n for n in ('ak','smg')],*[out/'wear'/n for n in ('receiver','cover','handle','flash','regulator','ports','feet','box','butt')]]:
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
 hero=out/'beauty/hero.png';ak=out/'precedents/ak/ak_hero.png';smg=out/'precedents/smg/smg_hero.png'
 peer=out/'hero-beside-ak-smg.jpg'
 sheet([('Harrow 56 / same lights and exposure',hero),('Rill 39 / same lights and exposure',ak),('Relay 9 / same lights and exposure',smg)],peer,columns=1,cell=(1600,900))
 entries.append(('Three guns / identical studio lights and exposure',peer))
 for i in range(0,len(entries),12):sheet(entries[i:i+12],out/f'review-page-{i//12+1:02d}.jpg')
 sheet(entries,out/'contact-sheet.jpg',columns=4,cell=(420,280))
 (BASE/'build/final-presentation.json').write_text(json.dumps(dict(images=manifest,count=len(manifest),sheet_entries=len(entries),review_pages=math.ceil(len(entries)/12),no_docs=True),indent=2))
 print('FINAL PRESENTATION',len(manifest),'GLB-verified renders',len(entries),'sheet entries')
if __name__=='__main__':main()
