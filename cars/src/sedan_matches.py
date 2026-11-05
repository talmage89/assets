"""Five chassis anchors per class camera; body landmarks are held out.

Native photographs are 2100 x 1575. Picks below were inspected at 1200 x 900.
Near hubs +/-3 preview pixels, contact shadows +/-5; obscured far-front contact
in Accord +/-12. These are camera registrations, not all-body shape fits.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('sedan_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']
def anchors(world,pixels,weights):
    return [dict(world=p,pixel=[v*1.75 for v in xy],weight=w) for p,xy,w in zip(world,pixels,weights)]
MATCHES={
 'accord_front':dict(title='Alder S240 / Accord class front / clay with stripes',photo=str(ROOT/'refs/sedan-accord-front.jpg'),
    crop=(-100,-80,2200,1655),location=(7,-10,2),target=(0,0,.7),lens=58,background='transparent',
    landmarks=anchors([(.895,F,H),(.900,R,H),(.88,F,0),(.885,R,0),(-.795,F,0)],
       [(684,594),(1100,505),(678,710),(1095,593),(194,651)],[1,1,1,1,.25])),
 'camry_rear':dict(title='Alder S240 / Camry class rear / clay with stripes',photo=str(ROOT/'refs/sedan-camry-rear.jpg'),
    crop=(-100,-80,2200,1655),location=(-7,10,2),target=(0,0,.7),lens=58,background='transparent',
    landmarks=anchors([(-.895,F,H),(-.900,R,H),(-.88,F,0),(-.885,R,0),(.800,R,0)],
       [(1120,505),(708,588),(1116,601),(704,700),(223,678)],[1,1,1,1,1])),
 'camry_front':dict(title='Alder S240 / Camry class front / clay with stripes',photo=str(ROOT/'refs/sedan-camry-front.jpg'),
    crop=(-100,-80,2200,1655),location=(7,-10,2),target=(0,0,.7),lens=58,background='transparent',
    landmarks=anchors([(.895,F,H),(.900,R,H),(.88,F,0),(.885,R,0),(-.795,F,0)],
       [(697,596),(1108,500),(697,700),(1105,595),(194,678)],[1,1,1,1,.25])),
 'accord_rear':dict(title='Alder S240 / Accord class rear / clay with stripes',photo=str(ROOT/'refs/sedan-accord-rear.jpg'),
    crop=(-100,-80,2200,1655),location=(-7,10,2),target=(0,0,.7),lens=58,background='transparent',
    landmarks=anchors([(-.895,F,H),(-.900,R,H),(-.88,F,0),(-.885,R,0),(.800,R,0)],
       [(1121,508),(711,596),(1119,600),(707,704),(207,680)],[1,1,1,1,1])),
}
