"""Reference-only linear-light neutral adaptation; never used by asset shaders.

The flash-lit bipod screw and white studio backgrounds constrain the black
finish. Field fabric and snow are estimated neutrals, retained as auxiliary
comparisons rather than treating unknown camouflage as a color chart.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1]
# Native pixels, picked by inspection. Gain normalization preserves the neutral
# patch's linear Rec.709 luminance; this corrects chromaticity, not exposure.
NEUTRALS={
 'left.jpg':((809,184,816,191),'bare silver bipod fastener, flash highlight; small sample, estimated neutral'),
 'm24_profile.jpg':((760,70,774,83),'bare silver mounting ring; white backdrop is clipped, so use this independent gray'),
 'PEO_M24_SWS-01.jpg':((150,100,500,220),'white studio backdrop; clipped neutral permits identity only, residual cast unconstrained; auxiliary comparison'),
 'detail_030.jpg':((1530,184,1640,197),'bare silver feed/raceway highlight; estimated neutral'),
 'detail_029.jpg':((855,154,863,176),'bare silver cocking pin; estimated neutral'),
 'open.jpg':((20,20,65,55),'pale gray uniform panel in shade; estimated neutral, auxiliary only'),
 'daylight.jpg':((145,650,200,685),'snow beside boot; estimated neutral, auxiliary only'),
}
def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,12.92*a,1.055*np.maximum(a,0)**(1/2.4)-.055)
def build():
 out=BASE/'build/white-balanced';out.mkdir(parents=True,exist_ok=True);rows={}
 for name,(rect,note) in NEUTRALS.items():
  im=Image.open(BASE/'refs'/name).convert('RGB');a=np.asarray(im,dtype=np.float32)/255
  x0,y0,x1,y1=rect;sample=np.median(linear(a[y0:y1,x0:x1]).reshape(-1,3),axis=0)
  # Snow includes dark ground at the selection's edge: use bright pixels only.
  if name=='daylight.jpg':
   pixels=linear(a[y0:y1,x0:x1]).reshape(-1,3);lum=pixels@np.array((.2126,.7152,.0722));sample=np.median(pixels[lum>=np.percentile(lum,85)],axis=0)
  weights=np.array((.2126,.7152,.0722));neutral=float(sample@weights);gains=neutral/np.maximum(sample,1e-6)
  corrected=np.clip(srgb(linear(a)*gains),0,1)
  dest=out/(Path(name).stem+'.png');Image.fromarray(np.round(corrected*255).astype('uint8')).save(dest)
  marked=im.copy();ImageDraw.Draw(marked).rectangle(rect,outline=(255,40,40),width=4);marked.thumbnail((1500,1000));marked.save(out/(Path(name).stem+'-neutral.jpg'),quality=90)
  rows[name]=dict(output=str(dest),neutral_rectangle_native=rect,neutral_description=note,neutral_srgb_255=np.round(srgb(sample)*255,2).tolist(),linear_rgb_gains=gains.round(6).tolist(),method='linear RGB diagonal adaptation, neutral Rec.709 luminance preserved')
 (out/'corrections.json').write_text(json.dumps(rows,indent=2));return rows
if __name__=='__main__':print(json.dumps(build(),indent=2))
