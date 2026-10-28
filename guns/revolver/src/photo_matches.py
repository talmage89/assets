"""Hand-measured landmarks for the kit photo-match solver, never geometry."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from guns.common.photo_matches import L
BASE=Path(__file__).resolve().parents[1]
def match(photo,title,crop,location,target,lens,landmarks):
 return dict(photo=str(BASE/'build/references'/(photo+'.png')),title=title,crop=crop,
  location=location,target=target,lens=lens,landmarks=landmarks,background='transparent',exposure=-.25,
  camera_height_m=(.060,.025),lens_bounds_mm=(65,140))
MATCHES={
 'right_photo':match('side-atf','Four-inch service class / right; clipped backdrop, form only',
  (150,40,1000,555),(.65,.055,.025),(0,.058,.015),80,[
   L((0,184,61),(931,136)),L((0,178,83),(912,77)),L((0,28,83),(467,92)),
   L((9,38,48.2),(497,175)),L((9,82.2,48.2),(630,175)),
   L((8.8,62,25.2),(570,251)),L((0,39,-7),(539,362)),
   L((0,-53.5,-63),(221,506),.4),L((0,-6,-63),(367,509),.4)]),
 'left_photo':match('left','Long-barrel class / left; frame fit, original 4-inch barrel and rubber grip differ',
  (5,35,495,315),(-.65,.03,.18),(0,.05,.025),75,[
   L((0,28,83),(283,90)),L((-9,38,48.2),(263,131)),
   L((-9,82.2,48.2),(217,145)),L((-9,82,75),(216,121)),
   L((-9,16,53),(298,133)),L((0,10,48),(307,149)),
   L((0,39,-7),(281,195),.5),
   # The photograph has a six-inch barrel. These two virtual class anchors
   # establish its optical direction; our four-inch barrel remains shorter.
   L((0,234.8,61),(35,184)),L((0,228.8,83),(37,160))]),
 'open_photo':match('open','Open cylinder / seven-shot reference; six-shot original',
  (70,50,3640,2860),(-.45,-.06,.24),(0,.06,.02),70,[
   L((0,184,61),(336,548)),L((0,178,83),(480,323)),
   L((0,28,83),(2399,208)),L((-8.8,82,77),(1673,383)),
   L((-12.0,23,53),(2530,763)),L((0,39,-9.3),(2029,1636)),
   L((-34.38,35.65,32.7),(2100,944))]),
}
# iPhone 11 EXIF: 26 mm equivalent. Keep that measured optical baseline rather
# than letting a seven-shot / different-grip object invent a telephoto lens.
MATCHES['open_photo']['lens']=26
MATCHES['open_photo']['camera_height_m']=(.025,.04)
MATCHES['open_photo']['lens_bounds_mm']=(25.999,26.001)
