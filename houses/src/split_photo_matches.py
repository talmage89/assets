"""Measured facade landmarks for type comparisons, not surveyed replicas."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import generate
p=generate(56,house_type='split');m,w=p['blocks'][:2]
q=generate(55,house_type='split');n=q['blocks'][0]
MATCHES=dict(
    split_side=dict(title='Side split / leaf-on western photograph / original plan differs',photo='refs/split-side-fit.jpg',crop=(0,0,1100,555),
        location=(m.cx+7,m.y0-24,1.7),target=(w.x0,m.y0,2.4),lens=44,camera_height_m=(1.7,1.2),lens_bounds_mm=(25,110),background='transparent',exposure=-.2,
        landmarks=[dict(world=(m.x0,m.y0,m.floor),pixel=(25,392),weight=.4),dict(world=(m.x0,m.y0,m.eave-.15),pixel=(15,278),weight=.4),
          dict(world=(w.x0,w.y0,p['levels']['upper']-.254),pixel=(538,315)),dict(world=(w.x1,w.y0,p['levels']['upper']-.254),pixel=(1010,317)),
          dict(world=(w.x0,w.y0,w.eave-.15),pixel=(501,174)),dict(world=(w.x1,w.y0,w.eave-.15),pixel=(1014,148)),
          dict(world=(w.cx,w.y0,w.height(w.cx,w.y0)),pixel=(732,58)),dict(world=(p['door_x'],m.y0,p['levels']['living']),pixel=(435,396),weight=.7)]),
    split_foyer=dict(title='Between-floor split entry / leaf-on western photograph / original plan differs',photo='refs/split-foyer-fit.jpg',crop=(90,40,1110,455),
        location=(n.cx-6,n.y0-25,1.7),target=(n.cx,n.y0,2.1),lens=45,camera_height_m=(1.7,1.3),lens_bounds_mm=(25,110),background='transparent',exposure=-.2,
        landmarks=[dict(world=(n.x0,n.y0,n.plate),pixel=(125,203)),dict(world=(n.x1,n.y0,n.plate),pixel=(1090,112)),
          dict(world=(n.x0,n.y0,q['levels']['upper']-.254),pixel=(129,341)),dict(world=(n.x1,n.y0,q['levels']['upper']-.254),pixel=(1050,286),weight=.4),
          dict(world=(q['door_x'],n.y0,q['levels']['living']),pixel=(602,385)),dict(world=(q['door_x'],n.y0,q['levels']['living']+2.032),pixel=(612,263))]))
