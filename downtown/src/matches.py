"""Kit camera fit, stated neutral white balance and photo-specific sun fields."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate
from kit.image_io import srgb_to_linear,linear_to_srgb
from photo_matches import MATCHES
folder=Path('build/balanced');folder.mkdir(parents=True,exist_ok=True);out={}
for name,m in MATCHES.items():
 m=dict(m);balance=None
 if 'neutral' in m:
  im=Image.open(m['photo']).convert('RGB');a=np.asarray(im).astype(float)/255;x0,y0,x1,y1=m['neutral'];linear=srgb_to_linear(a);neutral=np.median(linear[y0:y1,x0:x1].reshape(-1,3),axis=0);gains=float(neutral@np.array((.2126,.7152,.0722)))/neutral
  data=np.uint8(np.clip(linear_to_srgb(linear*gains),0,1)*255+.5);dest=folder/(name+'.jpg');Image.fromarray(data).save(dest,quality=97);m['photo']=str(dest)
  balance=dict(original=MATCHES[name]['photo'],neutral_pixels=m['neutral'],neutral_linear_rgb=neutral.tolist(),gains=gains.tolist(),assumption='Unpainted sunlit apron for Auburn; pale painted hood fascia for Louisiana. Neutral assumptions, not measured gray cards.')
 d=calibrate(m);d['region']=m['region'];d['white_balance']=balance
 for key in ('sun_direction','sun_elevation','sun_energy','context','exposure','sky_strength','overcast'):
  if key in m:d['shot'][key]=m[key]
 out[name]=d
Path('build/cameras.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out.items():print('CAMERA',n,'lens',round(d['shot']['lens'],2),'RMS px',round(d['residual_rms_pixels'],2))
