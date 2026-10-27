"""Inspected chassis anchors, original 2100x1575 stock frames.

Fit camera pose/lens to two outer wheel hub centers, two visible tread-contact
centroids, and an opposite-side contact. The opposite-side point constrains
camera height. Hub height is the model's lightly loaded height, not fitted.
Contacts are visible surface points (+/-0.92 near side); the hidden
wheel-center contact is not substituted for the photographed tread shoulder.
Body styling is judged in the pair and side overlay, never used to force a fit.
A symmetric 200 px horizontal / 100 px vertical comparison margin keeps the
original design fully visible. The crop extends beyond the source photo; those
comparison margins are transparent, never invented photographic content.
Pixel uncertainty ~3 px preview at hubs, ~5 px at soft contact shadows.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('pickup_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F=S['FRONT_AXLE'];R=S['REAR_AXLE'];H=S['HUB_HEIGHT']
def anchors(world,pixels):
    return [dict(world=p,pixel=tuple(v*1.4 for v in xy)) for p,xy in zip(world,pixels)]
MATCHES={
 'match_front':dict(title='Crew short bed / front clay',photo=str(ROOT/'refs/stock-front.jpg'),
    crop=(-200,-100,2300,1675),location=(6,-8,1.5),target=(0,0,1),lens=42,background='transparent',
    landmarks=anchors([(.964,F,H),(.964,R,H),(.920,F,0),(.920,R,0),(-.858,F,0)],
                      [(865,848),(1375,724),(841,1016),(1369,844),(230,966)])),
 'match_rear':dict(title='Crew short bed / rear clay',photo=str(ROOT/'refs/stock-rear.jpg'),
    crop=(-200,-100,2300,1675),location=(-6,8,1.5),target=(0,0,1),lens=42,background='transparent',
    landmarks=anchors([(-.964,F,H),(-.964,R,H),(-.920,F,0),(-.920,R,0),(.858,R,0)],
                      [(1404,706),(914,790),(1392,808),(890,955),(320,900)])),
}
