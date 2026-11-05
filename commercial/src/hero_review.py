"""Fixed-mask visible deposit measurements and native-pixel hero comparisons.

Photographs are inspection inputs only. Nothing here enters an asset map.
The masks select sunlit paving, omitting structures, cast shadows and covers.
Coverage is projected pixel area, not a claim of surveyed square meters or
chemical identification. Fine aggregate, residual seams and camera responses
limit this appearance proxy; the annotated masks expose what was counted.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from review import FONT

CASES={
 'used_forecourt':dict(photo='pa-canopy',crop=(0,1120,1660,1599),
  render_polygon=[(0,.13),(.03,.13),(.22,.65),(.95,.51),(1,.50),(1,.75),(.05,.99),(0,.99)],
  photo_polygon=[(0,.07),(.20,.07),(.42,.21),(.64,.24),(.71,.46),(.95,.46),(1,.51),(1,1),(0,1)],
  photo_covers=[(100,60,220,82),(125,84,265,104),(290,145,415,168),(186,207,382,238)]),
 'used_asphalt':dict(photo='va-store',crop=(405,1893,3848,2592),
  render_polygon=[(.15,.62),(.85,.62),(.85,.74),(.15,.74)],
  photo_polygon=[(.42,.44),(.84,.44),(.84,.68),(.42,.68)],photo_covers=[]),
}


def measure(im,case,photo,out):
 w,h=im.size;mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
 poly=case['photo_polygon' if photo else 'render_polygon']
 d.polygon([(round(x*w),round(y*h)) for x,y in poly],fill=255)
 if photo:
  for box in case['photo_covers']:d.rectangle(tuple(round(v*w/1600) for v in box),fill=0)
 rgb=np.asarray(im,dtype=float)/255;y=rgb@np.array([.2126,.7152,.0722]);m=np.asarray(mask)>0
 baseline=float(np.percentile(y[m],85));ratios=y[m]/baseline;rows={}
 for drop in (.04,.08):
  selected=ratios<1-drop
  rows[str(drop)]=dict(coverage_fraction=float(selected.mean()),median_contrast=float(1-np.median(ratios[selected])) if selected.any() else 0)
 stain=m&(y<baseline*.96);a=rgb.copy();a[~m]*=.24;a[stain]=a[stain]*.45+np.array([.82,.21,.08])*.55
 Image.fromarray(np.uint8(np.clip(a,0,1)*255+.5)).save(out)
 return dict(pixels=int(m.sum()),clean_Yprime_p85=baseline,thresholds=rows,polygon=poly,
  scope='Share of selected sunlit paving pixels below 96%/92% of its clean p85 Yprime; median relative contrast within selected deposits')


def run(before=None,folder=Path('renders/look-matches'),final=Path('renders/final')):
 out=Path('renders/hero-review');out.mkdir(parents=True,exist_ok=True);rows={}
 for name,case in CASES.items():
  path=folder/(name+'.png');im=Image.open(path).convert('RGB')
  photo=Image.open(Path('build')/(case['photo']+'-neutral.png')).convert('RGB').crop(case['crop']).resize(im.size,Image.Resampling.LANCZOS)
  row=dict(after=measure(im,case,False,out/(name+'-after-mask.png')),photo=measure(photo,case,True,out/(name+'-photo-mask.png')),after_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  if before:
   p=before/'look-matches'/(name+'.png');old=Image.open(p).convert('RGB');assert old.size==im.size
   row['before']=measure(old,case,False,out/(name+'-before-mask.png'));row['before_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
   assert row['before_sha256']==json.loads((before/'look-matches/provenance.json').read_text())[name]['image_sha256']
  assert row['after_sha256']==json.loads((folder/'provenance.json').read_text())[name]['image_sha256']
  rows[name]=row
 result=dict(rows=rows,neutral_balance=json.loads(Path('build/reference-balance.json').read_text()),
  limits='2D matched-view appearance estimate; different original station plans, seams, aggregate, estimated light and unknown camera response. Not physical surface area or segmentation ground truth.')
 (out/'wear-measurements.json').write_text(json.dumps(result,indent=2))
 if before:
  a=Image.open(before/'final/hero.png').convert('RGB');b=Image.open(final/'hero.png').convert('RGB');assert a.size==b.size==(1600,604)
  # Stack without scaling: one image pixel remains one comparison pixel.
  for name,box in dict(light=(65,230,805,405),forecourt=(735,325,1535,445),fascia=(600,170,1330,258),setting=(0,95,1600,410),driveway=(1060,375,1590,470)).items():
   crops=[im.crop(box) for im in (a,b)];w,h=crops[0].size;canvas=Image.new('RGB',(w,h*2+64),'#e8e9e6');d=ImageDraw.Draw(canvas)
   for i,(label,im) in enumerate(zip(('Before ce33d6e / native pixels','After / native pixels'),crops)):
    y=i*(h+32);d.text((8,y+5),label,font=FONT,fill='#26352f');canvas.paste(im,(0,y+32))
   canvas.save(out/('hero-'+name+'-before-after.jpg'),quality=96,optimize=True)
  canvas=Image.new('RGB',(1600,604*2+64),'#e8e9e6');d=ImageDraw.Draw(canvas)
  for i,im in enumerate((a,b)):
   y=i*636;d.text((8,y+5),'Before ce33d6e' if i==0 else 'After',font=FONT,fill='#26352f');canvas.paste(im,(0,y+32))
  canvas.save(out/'hero-before-after.jpg',quality=96,optimize=True)
 print(json.dumps({k:{label:v[label]['thresholds'] for label in ('before','after','photo') if label in v} for k,v in rows.items()},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path);p.add_argument('--folder',type=Path,default=Path('renders/look-matches'));p.add_argument('--final',type=Path,default=Path('renders/final'));a=p.parse_args();run(a.before,a.folder,a.final)
