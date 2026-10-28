"""Checkpoint sheets, dimensioned orthos and image provenance. No docs writes."""
import sys,json,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),24)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
def dimensions(report):
 panels=[];width,height=report['dimensions_mm'][1:]
 for name,label in [('side',f'Overall length {width:.2f} mm / height {height:.2f} mm'),
  ('top',f'Overall width {report["dimensions_mm"][0]:.2f} mm / length {width:.2f} mm'),
  ('front',f'Width {report["dimensions_mm"][0]:.2f} mm / height {height:.2f} mm')]:
  raw=Image.open(OUT/'beauty'/(name+'.png')).convert('RGBA')
  bg=Image.new('RGBA',raw.size,(232,234,230,255));bg.alpha_composite(raw)
  im=Image.new('RGB',(raw.width,raw.height+100),(232,234,230));im.paste(bg.convert('RGB'),(0,55));d=ImageDraw.Draw(im)
  d.text((20,14),name.upper()+' / imported GLB',font=FONT,fill=(28,40,34))
  d.text((20,im.height-35),label,font=SMALL,fill=(28,40,34));panels.append(im)
 total=Image.new('RGB',(1600,sum(round(p.height*1600/p.width) for p in panels)),(232,234,230));y=0
 for p in panels:
  p=p.resize((1600,round(p.height*1600/p.width)),Image.Resampling.LANCZOS);total.paste(p,(0,y));y+=p.height
 total.save(OUT/'dimensions.jpg',quality=92,optimize=True)
def main():
 OUT.mkdir(parents=True,exist_ok=True);report=json.loads((BASE/'build/serialization.json').read_text())
 glb=BASE/'build/revolver.glb';digest=hashlib.sha256(glb.read_bytes()).hexdigest()
 assert report['sha256']==digest
 records=0
 for folder in ['beauty','photos','trigger']:
  data=json.loads((OUT/folder/'shots.json').read_text())
  for name,row in data.items():
   assert row['sha256']==digest,(folder,name,'stale render');records+=1
 dense_digest=hashlib.sha256((BASE/'build/sculpt.blend').read_bytes()).hexdigest()
 for row in json.loads((OUT/'source-photos/shots.json').read_text()).values():assert row['sha256']==dense_digest
 for item,name in [('cartridge','cartridge'),('case','case'),('speedloader','speedloader_loaded')]:
  data=json.loads((OUT/'ammo'/(item+'-shots.json')).read_text())
  expected=hashlib.sha256((BASE/'build'/(name+'.glb')).read_bytes()).hexdigest()
  assert all(row['sha256']==expected for row in data.values()),item
 for folder in (OUT/'strips').iterdir():
  if not folder.is_dir():continue
  for row in json.loads((folder/'shots.json').read_text()).values():
   assert row['sha256']==digest;records+=1
 sections=json.loads((OUT/'sections/sections.json').read_text());assert sections['source_sha256']==digest and sections['high_sha256']==dense_digest
 timing=json.loads((OUT/'strips/timing.json').read_text())
 for clip,row in timing.items():
  with Image.open(OUT/'strips'/(clip+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
  assert duration==row['duration_ms'],clip
 dimensions(report)
 beauty=[OUT/'beauty'/(name+'.png') for name in ['hero','side','left','top','front','rake_right','rake_left','open','star','reload','rear','grip','trigger_side','trigger_quarter','sights','aimed']]
 contact(beauty,OUT/'contact-sheet.jpg',width=2000,title='Meridian Six / FORM CHECKPOINT / imported unbaked GLB')
 review_sheet([[OUT/'pairs'/(n+'_photo-pair.jpg')] for n in ['right','left','open']],OUT/'photo-pairs.jpg',title='Photographic form comparisons / neutral balance where recoverable')
 review_sheet([[OUT/'source-pairs'/(n+'_photo-pair.jpg')] for n in ['right','left','open']],OUT/'source-photo-pairs.jpg',title='Dense source / same photographic comparisons')
 contact([OUT/'ammo'/(n+'.png') for n in ['cartridge','cartridge_head','case','case_head','speedloader']],OUT/'ammunition.jpg',width=1600,title='Original .357 exterior ammunition and loaded speedloader')
 contact([OUT/'strips'/(clip+'.jpg') for clip in timing],OUT/'clips.jpg',width=2400,title='All clips / uniform 15 Hz samples / true-duration WebP loops beside each strip')
 # Exact optical frame, with a labeled magnification for blade/notch review.
 aim=Image.open(OUT/'beauty/aimed.png').convert('RGB');w,h=aim.size
 side=round(w*.16);cx=w//2;cy=round(h*.55)
 crop=aim.crop((cx-side//2,cy-side//2,cx+side//2,cy+side//2)).resize((600,600),Image.Resampling.NEAREST)
 detail=Image.new('RGB',(aim.width+620,max(aim.height,650)+60),(232,234,230));detail.paste(aim,(0,45));detail.paste(crop,(aim.width+10,45));dd=ImageDraw.Draw(detail)
 dd.text((14,10),'Exact Socket_Eye / gray backdrop',font=FONT,fill=(28,40,34))
 dd.text((aim.width+10,10),'Native pixels enlarged / no camera shift',font=SMALL,fill=(28,40,34));detail.save(OUT/'aimed-detail.jpg',quality=94,optimize=True)
 # Tonal range of object pixels, separate from transparent studio margins.
 raw=np.array(Image.open(OUT/'beauty/hero.png').convert('RGBA'));mask=raw[:,:,3]>128
 rgb=raw[:,:,:3][mask];luma=rgb@np.array([.2126,.7152,.0722])
 values=dict(object_pixels=int(mask.sum()),luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),
  all_channels_clipped_fraction=float(np.all(rgb==255,axis=1).mean()),deep_shadow_fraction=float((luma<15).mean()),
  note='unbaked constants; tonal inspection, no finish/albedo acceptance')
 (OUT/'audit.json').write_text(json.dumps(dict(passed=True,source_sha256=digest,current_glb_png_records=records,clips=len(timing),hero_values=values),indent=2))
 print('REVIEW',records,'current GLB renders;',len(timing),'true-duration clips;',OUT/'contact-sheet.jpg')
if __name__=='__main__':main()
