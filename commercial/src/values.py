"""Fixed material appearance ROIs in the used-photo pairs.

These are encoded display RGB/Y-prime statistics, not inferred albedos. The
photographs are neutral-balanced beforehand; rendered pixels are unedited.
Different station plans/finishes and sparse fits remain explicit limitations.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.fonts import find_font
from PIL import ImageFont
FONT=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20)
CASES={
 'soffit':dict(pair='period_canopy',photo='pa-canopy',photo_box=(1410,360,1535,440),render_box=(.45,.045,.58,.14),surface='White painted soffit in canopy shade; photo has aged warmer cladding'),
 'concrete':dict(pair='used_forecourt',photo='pa-canopy',photo_box=(500,1350,650,1450),render_box=(.08,.55,.25,.82),surface='Forecourt concrete, away from the cover and large stains; different shadow coverage remains'),
 'dark_cabinet':dict(pair='period_dispenser',photo='ca-dispenser',photo_box=(450,1000,480,1120),render_box=(.025,.04,.040,.20),surface='Ray-verified charcoal cabinet beside the hose; the former wide patch mixed black rubber and the cabinet finish; different makes and finishes'),
 'eifs':dict(pair='used_store',photo='tx-store',photo_box=(710,680,840,730),render_box=(.72,.16,.78,.19),surface='Sunlit upper EIFS above the 4.12m belt, ray-verified material; the former ROI mixed belt concrete and its cast shadow'),
 'asphalt':dict(pair='used_asphalt',photo='va-store',photo_box=(2400,2170,2600,2240),render_box=(.40,.60,.65,.69),surface='Sunlit weathered forecourt asphalt between shadow bands, away from foliage, the patch and large stains; different mixture and repair history'),
}


def stats(a):
 a=np.asarray(a,dtype=float).reshape(-1,3)/255;y=a@np.array((.2126,.7152,.0722));rgb=np.median(a,axis=0)
 return dict(p10=float(np.percentile(y,10)),median=float(np.median(y)),p90=float(np.percentile(y,90)),median_rgb=rgb.tolist(),ratios=(rgb/max(rgb[1],1e-6)).tolist(),pixels=len(a),clip_fraction=float((a.min(axis=1)>.985).mean()))


def measure(folder):
 folder=Path(folder);rows={};balance=json.loads(Path('build/reference-balance.json').read_text())
 for name,case in CASES.items():
  path=folder/(case['pair']+'.png');im=Image.open(path).convert('RGB');w,h=im.size;box=tuple(round(q*(w if i%2==0 else h)) for i,q in enumerate(case['render_box']))
  render=im.crop(box);ref=Image.open(Path('build')/(case['photo']+'-neutral.png')).convert('RGB').crop(case['photo_box']);a=stats(render);b=stats(ref)
  row=dict(case);row.update(photo_id=case['photo'],render_box_pixels=box,render=a,photo=b,relative_Y_errors={k:a[k]/b[k]-1 for k in ('p10','median','p90')},hue_ratio_errors=[a['ratios'][i]/b['ratios'][i]-1 for i in (0,2)],neutral=balance[case['photo']],image_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  rows[name]=row;canvas=Image.new('RGB',(1200,620),(232,233,230));d=ImageDraw.Draw(canvas)
  for i,(label,patch) in enumerate((('Export / Cycles / unedited pixels',render),('Used photograph / stated neutral',ref))):
   p=ImageOps.contain(patch,(570,480),Image.Resampling.LANCZOS);canvas.paste(p,(i*600+(600-p.width)//2,52+(480-p.height)//2));d.text((i*600+12,12),label,font=FONT,fill=(30,35,32))
  d.text((12,548),f"{name}  Y' median {a['median']:.3f} / {b['median']:.3f}; R:G:B {a['ratios'][0]:.3f}:1:{a['ratios'][2]:.3f} / {b['ratios'][0]:.3f}:1:{b['ratios'][2]:.3f}",font=FONT,fill=(30,35,32))
  canvas.save(folder/(name+'-values.jpg'),quality=94)
 result=dict(rows=rows,scope='Fixed semantically selected ROIs in actual exported Cycles pairs; encoded Rec.709 Y prime and channel ratios, not inverse reflectance or identical construction')
 (folder/'values.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:dict(model=v['render']['median'],photo=v['photo']['median'],relative=v['relative_Y_errors']['median'],model_ratios=v['render']['ratios'],photo_ratios=v['photo']['ratios']) for k,v in rows.items()},indent=2))


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--folder',type=Path,default=Path('renders/look-matches'));measure(a.parse_args().folder)
