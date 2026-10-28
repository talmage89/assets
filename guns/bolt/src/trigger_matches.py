"""Local blade silhouette landmarks; reference pixels are review only.

The guard/chassis differ deliberately and are not fit landmarks. The two
photographs provide side and oblique views; neither photograph is mirrored.
Short-baseline camera fits are estimates, not dimensional measurements.
"""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
MATCHES={
 'trigger_photo_right':dict(title='Right side / concave front, forward toe',
  photo=str(BASE/'refs/trigger_right.jpg'),crop=(65,209,155,293),
  location=(.55,.030,.008),target=(0,.030,.005),lens=100,lens_bounds_mm=(100,100),exposure=-.15,
  landmarks=[L((0,34.56,14),(103,233)),L((0,29.96,4),(94,253)),L((0,32.95,-3),(101,273)),
             L((0,30.62,14),(96,233)),L((0,26.69,4),(90,253)),L((0,28.42,-3),(96,273))]),
 'trigger_photo_quarter':dict(title='Oblique right / flat radiused blade',
  photo=str(BASE/'refs/trigger_m24.jpg'),crop=(1490,820,1680,970),
  location=(.20,.11,.055),target=(0,.030,.005),lens=100,lens_bounds_mm=(60,150),exposure=-.15,
  landmarks=[L((3.175,34.56,14),(1590,874)),L((3.175,29.96,4),(1578,900)),L((3.175,32.95,-3),(1590,925)),
             L((3.175,30.62,14),(1570,877)),L((3.175,26.69,4),(1567,900)),L((3.175,28.42,-3),(1579,932)),
             L((-3.175,32.95,-3),(1595,922),.5)]),
}
