"""White balance comparison photographs on declared neutral background patches.

Only ignored comparison derivatives are written. No photograph is imported by
the modeling, material, baking or export stages.
"""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageOps
BASE=Path(__file__).resolve().parents[1]
PATCHES={'side-atf':(20,20,180,100),'right':(380,20,480,80),
 'left':(30,20,150,70),'open':(80,20,500,140),
 'quarter':(20,20,350,120),'cylinder':(1300,30,1550,220),
 'target':(1900,950,1960,1000),'used-rubber':(100,45,300,110),
 'softpoint':(5,4,42,20),'ammo':(180,90,205,120),
 'rear-top':(20,20,120,60),'lug-front':(20,20,120,60)}
def main():
 out=BASE/'build/references';out.mkdir(parents=True,exist_ok=True);rows={}
 for name,patch in PATCHES.items():
  path=BASE/'refs'/(name+'.jpg');im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');x=np.array(im,dtype=float)
  a,b,c,d=patch;p=x[b:d,a:c].reshape(-1,3);neutral=np.median(p,axis=0)
  clipped=bool(np.any(neutral>=250))
  linear=np.where(x/255<=.04045,x/255/12.92,((x/255+.055)/1.055)**2.4)
  neutral_linear=np.median(linear[b:d,a:c].reshape(-1,3),axis=0)
  luminance=float(neutral_linear@np.array([.2126,.7152,.0722]))
  gain=luminance/neutral_linear
  balanced=np.clip(linear*gain,0,1)
  corrected=(np.clip(np.where(balanced<=.0031308,balanced*12.92,1.055*balanced**(1/2.4)-.055),0,1)*255).round().astype('uint8');Image.fromarray(corrected).save(out/(name+'.png'))
  rows[name]=dict(neutral_patch=patch,neutral_description='neutral gray tabletop; form only at this resolution' if name in ('rear-top','lug-front') else 'white photographic backdrop' if name=='side-atf' else 'light gray paper backdrop' if name in ('left','right') else 'gray foam background' if name=='open' else 'unprinted gray paper in the top-left corner' if name=='softpoint' else 'graph-paper white cell; clipped, form only' if name=='ammo' else 'matte gray paper above the revolver' if name=='used-rubber' else 'assumed neutral uncoated hammer cheek; mixed blue lighting, form only' if name=='target' else 'bright neutral table/backdrop; directional blue lighting remains a limitation',
   original_rgb_median=neutral.tolist(),gain=gain.tolist(),corrected_rgb_median=np.median(corrected[b:d,a:c].reshape(-1,3),axis=0).tolist(),
   neutral_patch_clipped=clipped,usable_for_material_color=not clipped and name!='target',
   note='clipped white cannot establish chromatic balance; form comparison only' if clipped else 'linear-light neutral balance preserving neutral luminance; view values, not recovered albedo')
 (out/'whitebalance.json').write_text(json.dumps(rows,indent=2))
 print('WHITE BALANCE',out/'whitebalance.json')
if __name__=='__main__':main()
