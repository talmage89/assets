"""Measured display contrast against neutral-balanced sunlit photographs.

Y prime/R ratios describe these JPEG/rendered views; no candela or inverse
albedo claim. The colored indication and an adjacent patch of sky are both
measured, and annotations expose the chosen samples.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

def circle(im,rect):
 a=np.array(im.convert('RGB'),dtype=float)/255;x0,y0,x1,y1=map(int,rect);cut=a[y0:y1,x0:x1];h,w=cut.shape[:2];y,x=np.mgrid[:h,:w];mask=((x-w/2)/(w*.47))**2+((y-h/2)/(h*.47))**2<1
 return cut[mask]
def metric(lens,sky):
 y=lens@np.array([.2126,.7152,.0722]);s=np.median(sky.reshape(-1,3),axis=0)
 return dict(lens_mean_rgb=lens.mean(axis=0).tolist(),lens_R_p95=float(np.percentile(lens[:,0],95)),sky_median_rgb=s.tolist(),R95_over_skyR=float(np.percentile(lens[:,0],95)/s[0]),lens_mean_Yprime_over_skyYprime=float(y.mean()/(s@np.array([.2126,.7152,.0722]))))
def run():
 out=Path('renders/measurements');out.mkdir(parents=True,exist_ok=True);photos={}
 for name,rect,skybox in [('span-2009',(1218,748,1535,1067),(1800,650,2050,900)),('gadsden-2025',(1398,1104,1433,1137),(1700,100,1950,300))]:
  im=Image.open('refs/'+name+'-balanced.jpg').convert('RGB');a=np.array(im)/255;x0,y0,x1,y1=skybox;photos[name]=metric(circle(im,rect),a[y0:y1,x0:x1]);ann=im.copy();d=ImageDraw.Draw(ann);d.ellipse(rect,outline='magenta',width=3);d.rectangle(skybox,outline='cyan',width=3);ann.save(out/(name+'-samples.jpg'),quality=95)
 ranges=json.loads(Path('build/lens-distances.json').read_text());comparisons={}
 for row in ranges:
  distance=row['distance'];im=Image.open(f'renders/checkpoint/optics/{distance}m.png').convert('RGB');a=np.array(im)/255;h,w=a.shape[:2];sky=a[round(.10*h):round(.20*h),round(.65*w):round(.75*w)];items=[]
  for head in row['heads']:items.append(dict(**head,measure=metric(circle(im,head['rect_pixels']),sky)))
  comparisons[str(distance)]=items
 surfaces={}
 # One flat painted strip below the red lens. This camera-space sample is
 # exposed in the record; original housing/visor shapes and JPEG clipping
 # limit the conclusion, so it is not an albedo or pass/fail measurement.
 paint_roi=(1450,1070,1490,1090)
 for key,file in [('photo_yellow',Path('refs/span-2009-balanced.jpg')),*[(f'head_{seed}',Path(f'renders/matches/head_{seed}.png')) for seed in (201,203)]]:
  if not file.exists():continue
  a=np.asarray(Image.open(file).convert('RGB'),dtype=float)/255;x0,y0,x1,y1=paint_roi
  if key!='photo_yellow':
   meta=json.loads(file.with_suffix('.json').read_text());crop=meta.get('render_crop')
   if crop:
    factor=meta['render_scale'];x0,y0,x1,y1=[round((v-crop[k%2])*factor) for k,v in enumerate((x0,y0,x1,y1))]
  cut=a[y0:y1,x0:x1].reshape(-1,3)
  surfaces[key]=dict(file=str(file),roi=paint_roi,median_display_rgb=np.median(cut,axis=0).tolist(),clipped_red_fraction=float((cut[:,0]>=.99).mean()),scope='Flat paint patch in nominally matched framing; not a physical albedo measurement. Different visor shadows remain visible in the pair.')
 result=dict(photos=photos,render=comparisons,surfaces=surfaces,neutral_balance=json.loads(Path('build/reference-balance.json').read_text()),scope='Display-domain contrast under documented sun/sky, median adjacent sky. Different exposure/camera response and optical products prevent physical luminance inference.')
 Path('build/lens-measurements.json').write_text(json.dumps(result,indent=2));print('OPTICS',json.dumps({n:{'R95/skyR':r['R95_over_skyR'],'Y/skyY':r['lens_mean_Yprime_over_skyYprime']} for n,r in photos.items()}))
if __name__=='__main__':run()
