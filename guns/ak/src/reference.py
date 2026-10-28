"""Reference-only neutral adaptation and anonymous comparison crops."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1]
PATCHES={'museum.jpg':((20,20,350,65),'gray museum backdrop, upper-left unshadowed margin'),
 'early.jpg':((700,65,940,125),'unprinted white cloth away from creases'),
 'muzzle.jpg':((5,5,80,40),'pale neutral backdrop estimate; mixed daylight uncertain'),
 'weld.jpg':((1750,1000,1830,1090),'pale garment estimate; uncertain colored fabric, auxiliary silhouette only'),
 'ammunition.jpg':((100,100,600,500),'light paper grid cells; brightest half excludes orange printed grid')}
PATCHES['trigger-sharp.jpg']=((950,1450,1150,1550),'unclipped white display paper; brightest half excludes lettering')
def main():
 out=BASE/'build/white-balanced';out.mkdir(parents=True,exist_ok=True);report={}
 for name,(rect,description) in PATCHES.items():
  p=BASE/'refs'/name
  if not p.exists():continue
  im=Image.open(p).convert('RGB');a=np.asarray(im).astype(float)/255
  linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  x0,y0,x1,y1=rect;patch=linear[y0:y1,x0:x1].reshape(-1,3)
  if name in ('ammunition.jpg','trigger-sharp.jpg'):
   lum=patch@np.array([.2126,.7152,.0722]);patch=patch[lum>=np.median(lum)]
  neutral=np.median(patch,axis=0)
  luma=float(neutral@np.array([.2126,.7152,.0722]));gain=luma/np.maximum(neutral,1e-6)
  b=np.clip(linear*gain,0,1);b=np.where(b<=.0031308,b*12.92,1.055*b**(1/2.4)-.055)
  balanced=Image.fromarray(np.rint(b*255).astype('uint8'));balanced.save(out/name,quality=98)
  overlay=im.copy();ImageDraw.Draw(overlay).rectangle(rect,outline=(255,60,20),width=3);overlay.thumbnail((1400,1000));overlay.save(out/(Path(name).stem+'-neutral.jpg'))
  report[name]=dict(neutral=description,rectangle=list(rect),linear_gains=gain.tolist(),
   limits='estimated neutral, edited exposure and reflection angles remain uncontrolled')
 (out/'corrections.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
