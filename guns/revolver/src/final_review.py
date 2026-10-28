"""Current-GLB provenance, decoded playback, tonal check and review-only docs."""
import argparse,json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
import final_shots
from presentation import digest as presentation_digest
OUT=BASE/'renders/final'
p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args()
digest=hashlib.sha256((BASE/'export/revolver.glb').read_bytes()).hexdigest();records=0
for folder in ('beauty','eevee','photos','hammer'):
 for name,row in json.loads((OUT/folder/'shots.json').read_text()).items():
  assert row['sha256']==digest,(folder,name,'stale GLB')
  assert row['presentation_sha256']==presentation_digest(),(folder,name,'stale render recipe');records+=1
  assert Image.open(OUT/folder/(name+'.png')).size[0]>0
for folder,name in [('cartridge','cartridge'),('case','case'),('loader','speedloader_loaded')]:
 expected=hashlib.sha256((BASE/'export'/(name+'.glb')).read_bytes()).hexdigest()
 assert all(r['sha256']==expected for r in json.loads((OUT/'ammo'/folder/'shots.json').read_text()).values())
timing=json.loads((OUT/'strips/timing.json').read_text())
for clip,row in timing.items():
 data=json.loads((OUT/'strips'/clip/'shots.json').read_text())
 assert all(r['sha256']==digest and r['engine']=='BLENDER_EEVEE' and r['presentation_sha256']==presentation_digest() for r in data.values());records+=len(data)
 with Image.open(OUT/'strips'/(clip+'.webp')) as im:
  duration=0
  for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
 assert duration==row['duration_ms'],clip
raw=Image.open(OUT/'beauty/hero.png').convert('RGBA');bg=Image.new('RGBA',raw.size,(105,108,111,255));bg.alpha_composite(raw)
bg.convert('RGB').save(OUT/'hero-gray.jpg',quality=95,optimize=True)
turn=[OUT/'beauty'/(n+'.png') for n in ('front','side','back','top')]
details=[OUT/'beauty'/(n+'.png') for n in ('hammer_cocked','sights','grip','muzzle','frame_bottom','grip_seam')]
actions=[OUT/'beauty'/(n+'.png') for n in ('wear_front','star','reload','aimed')]
contact(turn,OUT/'turnaround.jpg',width=1600,title='Meridian Six / exported PBR GLB / front, side, back, top')
contact(details,OUT/'details.jpg',width=1800,title='Curvature, checkering, rubber, machining and fitted construction')
contact(actions,OUT/'action.jpg',width=1600,title='Open cylinder, extraction, loader and exact Socket_Eye')
beauty=[OUT/'beauty'/(n+'.png') for n in final_shots.DEFAULT_SHOTS.split(',')]
if OUT/'beauty/wear_front.png' not in beauty:beauty.insert(2,OUT/'beauty/wear_front.png')
extras=[OUT/'ammo'/folder/(n+'.png') for folder,n in [('cartridge','cartridge'),('cartridge','cartridge_head'),('case','case'),('case','case_head'),('loader','speedloader')]]
contact([*beauty,OUT/'eevee/hero.png',*extras],OUT/'contact-sheet.jpg',width=2400,title='Meridian Six / current exported 2048 PBR GLBs / Cycles, scale, Eevee and detachments')
review_sheet([[OUT/'pairs'/(n+'_photo-pair.jpg')] for n in ('right','left','open','used')],OUT/'photo-pairs.jpg',title='Exported baked GLB / photographic comparisons / neutral balance where recoverable')
review_sheet([[OUT/'hammer-pairs'/(n+'_photo-pair.jpg')] for n in ('hammer_rest','hammer_cocked')],OUT/'hammer-pairs.jpg',title='Rest and cocked / one sculpted crescent / fixed visual camera estimates')
contact([OUT/'strips'/(n+'.jpg') for n in timing],OUT/'clips.jpg',width=2400,title='All 22 clips / actual-time Eevee playback beside each strip')
x=np.asarray(raw);rgb=x[:,:,:3][x[:,:,3]>128];luma=rgb@np.array([.2126,.7152,.0722])
values=dict(object_pixels=len(rgb),luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),all_channels_clipped_fraction=float(np.all(rgb==255,axis=1).mean()),deep_shadow_fraction=float((luma<15).mean()))
assert values['all_channels_clipped_fraction']<.005,values
result=dict(passed=True,current_glb_sha256=digest,current_glb_png_records=records,decoded_clips=len(timing),hero_values=values)
(OUT/'audit.json').write_text(json.dumps(result,indent=2))
if a.docs:
 docs=BASE/'docs';docs.mkdir(exist_ok=True)
 for name,path in [('hero',OUT/'hero-gray.jpg'),('turnaround',OUT/'turnaround.jpg'),('details',OUT/'details.jpg'),('action',OUT/'action.jpg'),('eevee',OUT/'eevee/hero.png')]:
  im=Image.open(path).convert('RGBA');im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
  base=Image.new('RGBA',im.size,(105,108,111,255));base.alpha_composite(im);im=base.convert('RGB')
  dst=docs/(name+'.jpg')
  for quality in range(93,39,-4):
   im.save(dst,quality=quality,optimize=True)
   if dst.stat().st_size<=200000:break
  assert im.width<=1600 and dst.stat().st_size<=200000
 print('DOCS GENERATED FOR LEAD REVIEW; leave uncommitted')
print('FINAL REVIEW',records,'current GLB images;',len(timing),'decoded clips;',values)
