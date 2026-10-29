"""Reference-only neutral adaptation and anonymous comparison crops."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1]
PATCHES={'museum.jpg':((20,20,350,65),'gray museum backdrop, upper-left unshadowed margin'),
 'early.jpg':((760,475,895,550),'unprinted white cloth immediately beneath the receiver, same local light as the gun; upper cloth is strongly warm-lit'),
 'muzzle.jpg':((5,5,80,40),'no dependable neutral: sky is colored; identity correction, form only'),
 'weld.jpg':((1750,1000,1830,1090),'no dependable neutral: garment is colored; identity correction, cheek-weld geometry only'),
 'ammunition.jpg':((100,100,600,500),'light paper grid cells; brightest half excludes orange printed grid')}
PATCHES['trigger-sharp.jpg']=((950,1450,1150,1550),'unclipped white display paper; brightest half excludes lettering')
PATCHES['rear-sight.jpg']=((2600,180,2860,380),'gray concrete backdrop at upper right; estimated neutral under flash')
PATCHES['exhibit.jpg']=((1890,550,1990,650),'gray display backing; glass and flash limit absolute color use')
PATCHES.update({
 'front-side.jpg':((1450,500,1600,650),'tan cardboard: no reliable neutral, identity; form only'),
 'front-behind.jpg':((1300,500,1450,650),'tan cardboard: no reliable neutral, identity; form only'),
 'front-sharp.jpg':((1750,100,1950,250),'weathered gray wood, estimated neutral; sun/shade split limits color'),
 'rear-sharp.jpg':((200,80,420,180),'weathered gray wood, estimated neutral; sun/shade split limits color'),
 'rear-side.jpg':((200,3000,450,3200),'dark work surface has colored paint: identity; form only'),
 'gas-side.jpg':((3000,300,3400,550),'unprinted white photographic backdrop'),
 'gas-sharp.jpg':((2300,300,2500,500),'unprinted white photographic backdrop'),
 'grip-sharp.jpg':((100,300,240,450),'light gray concrete away from rusty fissures')})
PATCHES['cover-sharp.jpg']=((2400,400,2700,600),'unprinted white photographic backdrop')
PATCHES['retainer.jpg']=((20,20,80,80),'unprinted white photographic backdrop')
PATCHES['ammunition-copper.jpg']=((700,80,1500,300),'unprinted white paper above the cartridge, away from ruler and shadow')
PATCHES['ammunition-green.jpg']=((1190,130,1240,170),'unprinted white label corner; strong mixed flash/ambient light, secondary finish-variation comparison only')
FORM_ONLY={'muzzle.jpg','weld.jpg','front-side.jpg','front-behind.jpg','rear-side.jpg'}
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
  if name in FORM_ONLY:gain=np.ones(3)
  b=np.clip(linear*gain,0,1);b=np.where(b<=.0031308,b*12.92,1.055*b**(1/2.4)-.055)
  balanced=Image.fromarray(np.rint(b*255).astype('uint8'));balanced.save(out/name,quality=98)
  if name=='exhibit.jpg':balanced.transpose(Image.Transpose.ROTATE_270).save(out/'exhibit-rotated.jpg',quality=98)
  overlay=im.copy();ImageDraw.Draw(overlay).rectangle(rect,outline=(255,60,20),width=3);overlay.thumbnail((1400,1000));overlay.save(out/(Path(name).stem+'-neutral.jpg'))
  report[name]=dict(neutral=description,rectangle=list(rect),linear_gains=gain.tolist(),
   color_measurements_allowed=name not in FORM_ONLY,
   limits='estimated neutral, edited exposure and reflection angles remain uncontrolled')
 (out/'corrections.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
