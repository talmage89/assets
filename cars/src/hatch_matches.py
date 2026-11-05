"""Five inspected chassis anchors per photo. Body points are NOT camera fit inputs.

Native photographs 2100x1575; picks inspected at 1200x900. Hub picking +/-3 px,
soft tire contact +/-5 px; far tire contact has greater uncertainty. The
photographed 16/17-inch tire diameters differ slightly from the H120's 18-inch.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('hatch_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']
def anchors(world,pixels,weights):return [dict(world=p,pixel=[v*1.75 for v in xy],weight=w) for p,xy,w in zip(world,pixels,weights)]
MATCHES={}
for make,front,picks in [
 ('corolla',True,[(685,603),(1117,507),(677,730),(1110,594),(196,665)]),
 ('corolla',False,[(1125,527),(720,627),(1118,625),(710,754),(176,691)]),
 ('hyundai',True,[(695,605),(1124,531),(686,731),(1116,620),(194,687)]),
 ('hyundai',False,[(1132,533),(722,609),(1125,624),(711,736),(166,698)])]:
 sign=1 if front else -1
 worlds=[(sign*.876,F,H),(sign*.881,R,H),(sign*.86,F,0),(sign*.865,R,0),(-sign*(.775 if front else .780),F if front else R,0)]
 MATCHES[make+('_front' if front else '_rear')]=dict(title='Alder H120 / '+make+' / clay with stripes',
  photo=str(ROOT/('refs/hatch-'+make+('-front.jpg' if front else '-rear.jpg'))),crop=(-90,-70,2190,1645),
  location=(sign*7,-sign*10,2),target=(0,0,.7),lens=58,background='transparent',
  landmarks=anchors(worlds,picks,[1,1,1,1,.5]))

# Near-profile cameras have no visible far wheel contact. The two near hubs
# and tire contacts constrain their pose, with a stated 65 mm lens prior.
# Silhouette points are withheld, as in the three-quarter fits. Contact picks
# refer to the tread center, not the outer sidewall's curved shadow.
for make,picks in [
 ('corolla',[(246,566),(974,566),(246,648),(974,648)]),
 ('hyundai',[(241,566),(976,565),(241,649),(976,648)])]:
 MATCHES[make+'_side']=dict(title='Alder H120 / '+make+' / perspective profile',
  photo=str(ROOT/('refs/hatch-'+make+'-side.jpg')),crop=(0,0,2100,1575),
  location=(7.5,0,1.4),target=(0,0,.75),lens=65,lens_bounds_mm=(45,100),
  background='transparent',landmarks=anchors(
   [(.876,F,H),(.881,R,H),(.775,F,0),(.780,R,0)],picks,[1,1,1,1]))
