"""Review contact sheets, dimension sheet and normal-speed strip overview.

All files stay ignored until final acceptance. No committed checkpoint images.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
from kit.contact import contact,review_sheet
OUT=BASE/'renders/checkpoint';font=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
def panel(path,size,bg=(221,223,219)):
 src=Image.open(path).convert('RGBA');src.thumbnail(size,Image.Resampling.LANCZOS)
 im=Image.new('RGBA',size,(*bg,255));im.alpha_composite(src,((size[0]-src.width)//2,(size[1]-src.height)//2));return im.convert('RGB')
def main():
 digest=hashlib.sha256((BASE/'build/shotgun.glb').read_bytes()).hexdigest()
 for folder in ('final','orthos','matches','stock-masks'):
  data=json.loads((OUT/folder/'shots.json').read_text())
  assert all(s['sha256']==digest for s in data.values()),folder
 files=[OUT/'final'/(n+'.png') for n in ('right','left','raking_right','raking_left','receiver','guard','open','underside','aimed','muzzle','stock','forend')]
 files += [OUT/'shell/shell.png',OUT/'shell/shell_crimp.png',OUT/'hull/hull.png',OUT/'hull/hull_primer.png']
 contact(files,OUT/'contact-sheet.jpg',width=2000,title='PD Hearth 12 / unbaked form and motion checkpoint')
 data=json.loads((BASE/'build/check.json').read_text());s=data['bounds_m']['size']
 sheet=Image.new('RGB',(1700,1360),(235,236,231));d=ImageDraw.Draw(sheet)
 d.text((20,16),f"Measured {s[1]*1000:.2f} L × {s[2]*1000:.2f} H × {s[0]*1000:.2f} W mm",font=font,fill=(25,35,30))
 d.text((20,52),f"Barrel {data['barrel_length_m']*1000:.2f} mm | pull {data['length_of_pull_m']*1000:.2f} mm",font=font,fill=(25,35,30))
 for i,n in enumerate(('side','top','front')):
  y=100+i*410;d.text((20,y),n,font=font,fill=(25,35,30));sheet.paste(panel(OUT/'orthos'/(n+'.png'),(1640,365)),(30,y+35))
 sheet.save(OUT/'dimensions.jpg',quality=92,optimize=True)
 review_sheet([[OUT/'pairs'/(n+'_photo-pair.jpg')] for n in ('right','left','open')],OUT/'photo-pairs.jpg',width=2200,title='Independent right / left / open photograph pairs')
 clips=['Fire','FireLast','Reload','ReloadEmpty','Inspect']
 review_sheet([[OUT/'strips'/(n+'.jpg')] for n in clips],OUT/'clips.jpg',width=2000,title='Uniform 15-Hz samples / playback WebPs retain real duration')
 timing=json.loads((OUT/'strips/timing.json').read_text());durations={}
 for name,t in timing.items():
  im=Image.open(OUT/'strips'/(name+'.webp'));total=0
  for i in range(getattr(im,'n_frames',1)):
   im.seek(i);im.load();total+=im.info.get('duration',0)
  # Still-image WebP carries no animation duration; timing manifest carries it.
  if getattr(im,'n_frames',1)>1:assert total==t['duration_ms'],(name,total,t)
  durations[name]=dict(expected_ms=t['duration_ms'],decoded_animation_ms=total,frames=getattr(im,'n_frames',1))
 (BASE/'build/playback.json').write_text(json.dumps(durations,indent=2))
 values={}
 for name in ('right','left','receiver','stock','forend','open','underside'):
  pixels=np.asarray(Image.open(OUT/'final'/(name+'.png')).convert('RGBA'))
  rgb=pixels[:,:,:3][pixels[:,:,3]>128].astype(float)
  luma=rgb@np.array([.2126,.7152,.0722])
  values[name]=dict(display_luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),
   deep_shadow_fraction=float(np.mean(luma<24)),clipped_pixel_fraction=float(np.mean(np.all(rgb>=254,axis=1))))
 (BASE/'build/value-review.json').write_text(json.dumps(dict(scope='display pixel values under inspection lighting; not measured albedo',shots=values),indent=2))
 print('REVIEW',OUT/'contact-sheet.jpg',OUT/'dimensions.jpg',OUT/'sections.jpg',OUT/'clips.jpg')
if __name__=='__main__':main()
