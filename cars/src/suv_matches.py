"""Inspected 1200 x 900 chassis picks. Native photos 2100 x 1575.

Hub uncertainty +/-3 preview px; contacts +/-5 (far contact +/-9). Five
chassis anchors fit each camera; no body outline participates in the solve.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('suv_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']
MATCHES={}
for name,pixels in {
 'crv_front':[(655,612),(1093,557),(641,738),(1080,660),(202,694)],
 'rav4_front':[(688,612),(1105,560),(677,729),(1090,658),(224,696)],
 'crv_rear':[(1112,556),(690,620),(1101,672),(674,750),(190,702)],
 'rav4_rear':[(1105,558),(695,616),(1090,661),(677,740),(207,702)],
}.items():
 rear=name.endswith('rear');sign=-1 if rear else 1
 world=[(sign*.894,F,H),(sign*.899,R,H),(sign*.880,F,0),(sign*.885,R,0),(-sign*.805,R if rear else F,0)]
 # Rear views' pixel picks list the front wheel first, matching world order.
 MATCHES[name]=dict(title='Alder X220 / '+name.replace('_',' ')+' / clay with stripes',photo=str(ROOT/('refs/suv-'+name.replace('_','-')+'.jpg')),
  crop=(-100,-60,2200,1635),location=(sign*7,10 if rear else -10,2.3),target=(0,0,.85),lens=58,background='transparent',
  landmarks=[dict(world=w,pixel=[1.75*v for v in px],weight=wt) for w,px,wt in zip(world,pixels,[1,1,1,1,.5])])
