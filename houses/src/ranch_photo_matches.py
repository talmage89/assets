"""Ranch type comparisons, not reconstructed private homes or texture sources.

Anchors were picked on local reference canvases; original-image coordinates
are retained. The broad comparison intentionally retains differences between
our modular-brick plan and the photograph's stone L-plan.
"""
from pathlib import Path
import os
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import generate,openings
p=generate(int(os.environ.get('RANCH_SEED','12')),overrides=json.loads(Path(os.environ['HOUSE_PLAN']).read_text()) if os.environ.get('HOUSE_PLAN') else None,house_type='ranch');m,g=p['blocks']
o=next(o for o in openings(p) if o.get('style')=='picture');x=m.x0+o['u'];z=o['z'];w=o['w'];h=o['h']
lo=min(m.x0,g.x0);hi=max(m.x1,g.x1)
def px(x,y,scale):return (x*scale,y*scale)
MATCHES=dict(
 ranch_summer=dict(title='Leaf-on ranch / long hip, low eave and broad chimney',
  photo='refs/ranch-summer-ok.jpg',crop=(80,330,1550,835),location=(13,-29,1.7),target=(0,m.y0,1.8),lens=40,
  camera_height_m=(1.7,1.0),lens_bounds_mm=(25,100),background='transparent',exposure=-.35,
  landmarks=[dict(world=(lo,m.y0,0),pixel=px(160,580,4/3)),dict(world=(hi,m.y0,0),pixel=px(1105,570,4/3)),
   dict(world=(lo,m.y0,m.eave-.14),pixel=px(160,440,4/3)),dict(world=(hi,m.y0,m.eave-.14),pixel=px(1105,416,4/3))]),
 ranch_brick_picture=dict(title='Brick ranch / picture unit, sill and eave shade',
  photo='refs/ranch-summer-mn.jpg',crop=(950,730,1620,1150),location=(x+3,m.y0-8,1.7),target=(x,m.y0,z+h/2),lens=48,
  camera_height_m=(1.7,1.2),lens_bounds_mm=(25,100),background='transparent',exposure=-.35,
  landmarks=[dict(world=(x-w/2,m.y0,z),pixel=px(380,380,3390/1200)),dict(world=(x+w/2,m.y0,z),pixel=px(548,378,3390/1200)),
   dict(world=(x-w/2,m.y0,z+h),pixel=px(380,302,3390/1200)),dict(world=(x+w/2,m.y0,z+h),pixel=px(548,300,3390/1200))]),
)

# The source is catalogued as a 1960 house. The main facade is partly screened
# by planting; the corners have greater picking uncertainty than the roof.
MATCHES['ranch_sun_1960']=dict(title='1960 brick ranch / sun, roof and eave shade',
 photo='refs/ranch-sun-1960.jpg',crop=(810,340,2190,920),
 location=(m.cx+6,m.y0-25,1.7),target=(m.cx,m.y0,1.8),lens=44,
 camera_height_m=(1.7,1.0),lens_bounds_mm=(28,110),background='transparent',exposure=.93,
 landmarks=[dict(world=(m.x0,m.y0,0),pixel=(500*2232/1200,430*1246/670)),
  dict(world=(m.x1,m.y0,0),pixel=(1130*2232/1200,430*1246/670)),
  dict(world=(m.x0,m.y0-m.overhang,m.eave-m.pitch*m.overhang-.055),pixel=(500*2232/1200,282*1246/670)),
  dict(world=(m.x1,m.y0-m.overhang,m.eave-m.pitch*m.overhang-.055),pixel=(1130*2232/1200,282*1246/670))])

# Sunny three-quarter comparison from a documented 1956–64 district. Exact
# house year is unverified; planting obscures the ground picks by ~15–25 px.
# The original photograph, rather than a resampled grid, supplies the anchors.
def ncpx(x,y):return (434+x*2641/1600,1938+y*2641/1600)
edge=m.eave-m.pitch*m.overhang
MATCHES['ranch_sun_oblique']=dict(title='Period brick ranch / sunny three-quarter, roof and deep eaves',
 photo='refs/ranch-sun-oblique.jpg',crop=(434,1938,3075,3041),
 location=(18,-27,1.7),target=(0,0,1.6),lens=45,
 camera_height_m=(1.7,1.2),lens_bounds_mm=(25,110),background='transparent',exposure=1.95,
 landmarks=[dict(world=(lo,m.y0,0),pixel=ncpx(150,438)),
  dict(world=(hi,m.y0,0),pixel=ncpx(930,470)),
  dict(world=(lo-m.overhang,m.y0-m.overhang,edge),pixel=ncpx(145,265)),
  dict(world=(hi+m.overhang,m.y0-m.overhang,edge),pixel=ncpx(920,235)),
  dict(world=(hi+m.overhang,m.y1+m.overhang,edge),pixel=ncpx(1200,285),weight=.6)])
