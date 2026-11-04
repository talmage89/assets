"""Five-year class photographs. Wheel picks only; no body outline fit."""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('sedan_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']

def rows(world,pixels,scale,weights):
    return [dict(world=p,pixel=[v*scale for v in xy],weight=w) for p,xy,w in zip(world,pixels,weights)]
MATCHES={
 'used_front':dict(title='S240 / five-year class front (MY2020 photographed 2025)',photo=str(ROOT/'refs/sedan-used-front.jpg'),
    crop=(-180,-100,4700,2736),location=(-4.8,-5.5,2),target=(0,-.1,.75),lens=50,background='transparent',paint='Graphite',exposure=1.2,
    landmarks=rows([(-.895,F,H),(-.900,R,H),(-.875,F,0),(-.88,R,0)],
      [(490,512),(80,320),(501,638),(84,397)],4520/1200,[1,1,1,1]),
    lens_bounds_mm=(25,110),
    calibration_note='Hubs +/-3 px, near contacts +/-5 px, No far-wheel anchor: its contact is occluded. Class tire and trim differ; no body anchors.'),
 'used_rear':dict(title='S240 / five-year class rear (MY2020 photographed 2025)',photo=str(ROOT/'refs/sedan-used-rear.jpg'),
    crop=(-180,-100,5555,3277),location=(-5,7,2),target=(0,.1,.75),lens=55,background='transparent',paint='Graphite',exposure=1.0,
    landmarks=rows([(-.895,F,H),(-.900,R,H),(-.875,F,0),(-.88,R,0)],
      [(1138,321),(806,522),(1140,398),(805,657)],5375/1200,[1,1,1,1]),
    lens_bounds_mm=(25,110),
    calibration_note='Hubs +/-3 px, near contacts +/-5 px, No far-wheel anchor: its contact is occluded. Registration is not body or albedo agreement.'),
}
