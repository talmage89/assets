from pathlib import Path
from PIL import Image
import numpy as np,json
base=Path(__file__).resolve().parents[1];out=base/'build/white-balanced';out.mkdir(exist_ok=True)
# These are estimated neutrals, not gray-card measurements.
patches={'right':(1900,750,2070,850),'left':(40,30,230,100),'box':(20,20,220,90),'open':None,'cover_close':(40,40,300,280),'used_receiver':(80,40,280,210),'used_oblique':(2900,2200,3250,2450),'stock':(2170,110,2290,190),'belt':(60,110,240,200),'used_whole':(800,20,1100,90),'used_right':(800,20,1100,90),'used_stock':(80,80,400,300),'used_box2':(10,880,100,980),'used_box':(30,1130,180,1300)}
rows={}
for n,patch in patches.items():
 p=base/'refs'/f'{n}.jpg'
 if not p.exists():continue
 im=Image.open(p).convert('RGB');a=np.array(im,dtype=float)/255
 x=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
 if patch:
  q=np.array(im.crop(patch),float)/255;q=np.where(q<=.04045,q/12.92,((q+.055)/1.055)**2.4)
  mean=q.mean(axis=(0,1));g=mean.mean()/np.maximum(mean,1e-6);clipped=bool((q>.99).mean()>.2)
 else:g=np.ones(3);clipped=False
 y=np.clip(x*g,0,1);rgb=np.where(y<=.0031308,y*12.92,1.055*y**(1/2.4)-.055)
 Image.fromarray(np.uint8(np.clip(rgb,0,1)*255+.5)).save(out/f'{n}.jpg',quality=97)
 rows[n]=dict(neutral_patch=patch,gains=g.tolist(),clipped_neutral=clipped,limit=('No trustworthy neutral; form-only, no color measurement' if patch is None else 'Estimated gray studio backdrop' if n in ('used_receiver','used_whole','used_right') else 'Estimated concrete neutral' if n=='used_stock' else 'Estimated pale gravel neutral' if n=='stock' else 'Gray range background in upper left' if n=='belt' else 'Estimated backdrop; clipped patches cannot constrain residual cast'))
(out/'corrections.json').write_text(json.dumps(rows,indent=2))
print(rows)
