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

# Region-specific cameras retain the same reference pixels; source geometry is
# never read from these annotations. Broad field variants are form-only.
MATCHES['receiver_photo']=dict(MATCHES['right_photo'],title='Right receiver / pressed sheet and rivet landmarks',crop=(460,210,1120,510))
# Use receiver-local anchors so the crop is not calibrated by the stock.
MATCHES['receiver_photo']['landmarks']=[
 L((24,-50,92),(545,398)),L((24,236,105),(1080,300)),
 L((24,-44,61),(576,491)),L((24,89,111),(698,301)),
 L((28,185,91),(991,315)),L((28,110,91),(854,335))]

def opened(x,y,z):
 import math
 angle=math.radians(-96);dy=y-236;dz=z-127
 return (x,236+dy*math.cos(angle)-dz*math.sin(angle),127+dy*math.sin(angle)+dz*math.cos(angle))
MATCHES['cover_detail_photo']=dict(title='Open cover / pressed walls and underside arm',photo=str(BASE/'build/white-balanced/cover_close.jpg'),crop=(600,0,2100,2770),
 location=(.32,-.36,.34),target=(0,.20,.25),lens=65,lens_bounds_mm=(30,180),
 landmarks=[L(opened(-28,-50,137),(1630,130)),L(opened(28,-50,137),(1860,235)),
 L(opened(-28,224,132),(1020,2440)),L(opened(28,224,132),(1240,2510)),
 L(opened(7,104,137),(1480,1420)),L(opened(7,205,132),(1280,2180))])
MATCHES['tray_detail_photo']=dict(title='Feed tray / formed plate and cartridge guides',photo=str(BASE/'build/white-balanced/cover_close.jpg'),crop=(580,2160,2020,3384),
 location=(.26,-.22,.34),target=(0,.16,.118),lens=70,lens_bounds_mm=(25,180),
 landmarks=[L((-43,134,118),(1100,3120)),L((23,134,118),(1650,2860)),
 L((-43,205,118),(810,2600)),L((23,205,118),(1360,2460)),
 L((0,236,127),(1100,2510))])
MATCHES['sight_detail_photo']=dict(title='Rear sight / thin pierced ears and small aperture',photo=str(BASE/'refs/sight.jpg'),crop=(0,0,2807,2461),
 location=(.035,-.09,.30),target=(0,-.021,.164),lens=90,lens_bounds_mm=(40,180),
 landmarks=[L((-15,-35,150),(735,2230)),L((15,-35,150),(2360,2240)),
 L((-15,-9,181),(825,150)),L((15,-9,181),(2060,170)),
 L((0,-22.5,176),(1580,1030)),L((-24,-30,159),(430,1540))])
MATCHES['box_detail_photo']=dict(title='Molded box / rim, ribs, catch and receiver clip',photo=str(BASE/'refs/box_molded.png'),crop=(150,100,830,940),
 location=(-.38,-.13,.13),target=(0,.164,-.029),lens=90,lens_bounds_mm=(30,180),
 landmarks=[L((-60,207,38),(230,220)),L((-60,121,38),(415,236)),
 L((60,121,38),(750,166)),L((48,123,-118),(706,805)),
 L((-48,205,-118),(280,748)),L((-48,123,-118),(490,877))])

# Issued finishes. These camera observations are comparison-only.
MATCHES['used_photo']=dict(title='Used receiver / gray-balanced backdrop',photo=str(BASE/'build/white-balanced/used_receiver.jpg'),crop=(0,0,1800,1174),location=(-1.0,.1,.29),target=(0,.10,.090),lens=100,lens_bounds_mm=(50,180),landmarks=[L((-24,-50,120),(1480,450)),L((-24,236,120),(490,440)),L((-24,-50,54),(1430,690)),L((-24,236,54),(510,694)),L((0,47,22),(1000,858)),L((0,-21,176),(1350,300))])
MATCHES['used_field_photo']=dict(title='Issued field finish / gravel neutral',photo=str(BASE/'build/white-balanced/stock.jpg'),crop=(0,0,2567,1314),location=(1.4,.35,.68),target=(0,.18,.06),lens=85,lens_bounds_mm=(45,180),landmarks=[L((0,710,105),(2510,256)),L((0,536,105),(1950,320)),L((0,536,176),(1920,200)),L((24,236,105),(1290,420)),L((24,-50,92),(550,560)),L((0,-21,176),(640,363))])
MATCHES['ammo_photo']=dict(title='Carried brass / copper / green tip / black steel links',photo=str(BASE/'build/white-balanced/belt.jpg'),crop=(0,0,3504,2336),location=(-.16,.28,.19),target=(-.05,.16,.11),lens=80,lens_bounds_mm=(30,180),landmarks=[L((-45,145,124),(1370,1900)),L((-45,202,124),(1110,440)),L((-70,145,110),(2200,1900)),L((-70,202,110),(1900,400))])

MATCHES['used_right_photo']=dict(title='Used whole gun / unclipped gray backdrop',photo=str(BASE/'build/white-balanced/used_right.jpg'),crop=(0,0,1800,779),location=(-1.8,.4,.65),target=(0,.18,.06),lens=100,lens_bounds_mm=(60,180),landmarks=[L((0,710,105),(62,148)),L((0,536,176),(414,188)),L((0,536,105),(398,236)),L((-24,236,105),(874,392)),L((-24,-50,92),(1415,452)),L((0,-21,176),(1240,338)),L((0,-330,47),(1738,590),.3)])
