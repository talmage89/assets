"""Type/framing comparisons; no photographed plan is reproduced.

Photo pixels refer to upright, 1200-wide, casing-neutralized review copies.
The first photo is April supplemental evidence; the second is leaf-on May.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import generate
p=generate(36,house_type='cape');m=p['blocks'][0]
q=generate(33,house_type='cape');n=q['blocks'][0]
MATCHES=dict(
 cape_dormers=dict(title='Two gabled dormers / supplemental spring photograph',photo='refs/cape-northeast-spring-fit.jpg',crop=(75,140,1030,800),
  location=(m.cx+12,m.y0-18,1.8),target=(m.cx,m.y0,3.1),lens=45,camera_height_m=(1.8,1.2),lens_bounds_mm=(25,100),background='transparent',exposure=-.15,
  landmarks=[dict(world=(m.x0,m.y0,m.floor),pixel=(112,726)),dict(world=(m.x1,m.y0,m.floor),pixel=(710,687)),
   dict(world=(m.x0,m.y0,m.eave-.15),pixel=(108,505)),dict(world=(m.x1,m.y0,m.eave-.15),pixel=(710,399)),
   dict(world=(m.x1,m.y1,m.floor),pixel=(1111,616),weight=.3),dict(world=(m.x1,m.y1,m.eave-.15),pixel=(1110,431),weight=.3)]),
 cape_plain=dict(title='Unpierced steep roof / leaf-on mid-Atlantic photograph',photo='refs/cape-midatl-leaf-fit.jpg',crop=(220,35,1160,590),
  location=(n.cx+12,n.y0-18,1.8),target=(n.cx,n.y0,3.0),lens=45,camera_height_m=(1.8,1.),lens_bounds_mm=(25,100),background='transparent',exposure=-.15,
  landmarks=[dict(world=(n.x0,n.y0,n.floor),pixel=(264,564)),dict(world=(n.x1,n.y0,n.floor),pixel=(1007,520)),
   dict(world=(n.x0,n.y0,n.eave-.15),pixel=(260,386)),dict(world=(n.x1,n.y0,n.eave-.15),pixel=(1007,350)),
   dict(world=(n.x1,n.cy,n.height(n.x1,n.cy)),pixel=(1090,62)),dict(world=(n.x1,n.y1,n.eave-.15),pixel=(1133,343),weight=.4)]),
)
