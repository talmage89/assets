"""Manually observed photographic landmarks, never traced or projected textures."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def L(world,pixel,weight=1):return dict(world=[v*.001 for v in world],pixel=pixel,weight=weight)
MATCHES={
 'right_photo':dict(title='Right exterior / fixed-stock belt-fed class',photo=str(BASE/'build/white-balanced/right.jpg'),crop=(0,0,2126,913),
  location=(3,.15,.4),target=(0,.17,.07),lens=105,lens_bounds_mm=(70,160),
  landmarks=[L((0,710,105),(2075,150)),L((0,536,176),(1630,151)),L((0,536,105),(1620,235)),
   L((0,-21,176),(595,265)),L((24,-50,92),(545,398)),L((24,236,105),(1080,300)),
   L((0,-330,47),(95,543),.5),L((0,47,22),(833,530),.5)]),
 'left_photo':dict(title='Left exterior / original furniture against class',photo=str(BASE/'build/white-balanced/left.jpg'),crop=(0,0,2126,1460),
  location=(-1.3,.9,.45),target=(0,.15,.05),lens=105,lens_bounds_mm=(50,160),
  landmarks=[L((0,710,105),(315,189)),L((0,536,176),(724,137)),L((0,536,105),(730,355)),
   L((0,-21,176),(1605,467)),L((-24,236,105),(1205,494)),L((-24,-50,92),(1656,760)),
   L((0,-330,47),(1950,950),.35)]),
 'open_photo':dict(title='Open cover / exterior tray comparison',photo=str(BASE/'build/white-balanced/open.jpg'),crop=(1600,1620,3900,2740),
  location=(.9,.12,.95),target=(0,.17,.10),lens=65,lens_bounds_mm=(25,140),
  landmarks=[L((24,-50,120),(1760,2320)),L((24,236,120),(2470,2260)),
   L((0,236,127),(2440,2220)),L((0,536,105),(3280,2215)),L((0,710,105),(3815,2200)),
   L((24,-50,53),(1780,2450)),L((24,236,53),(2460,2380))]),
 'trigger_photo':dict(title='Trigger / concave front toward muzzle',photo=str(BASE/'build/white-balanced/right.jpg'),crop=(770,432,915,561),
  location=(.5,.05,.04),target=(0,.045,.031),lens=105,lens_bounds_mm=(50,160),
  landmarks=[L((0,47,48),(821,471)),L((0,43.1,34),(823,511)),L((0,49,22),(841,535)),
   L((6,35,10),(826,549),.4),L((6,78,46),(897,455),.4)])}

MATCHES['belt_photo']=dict(title='Box and hanging belt / early exterior class',photo=str(BASE/'build/white-balanced/box.jpg'),crop=(0,0,2507,1064),location=(-1.5,.8,.9),target=(0,.18,.03),lens=70,lens_bounds_mm=(45,160),landmarks=[L((0,710,105),(60,80)),L((0,536,176),(490,90)),L((0,536,105),(500,260)),L((-24,236,105),(1110,435)),L((0,-21,176),(1590,398)),L((0,-330,47),(2300,755),.35)])
