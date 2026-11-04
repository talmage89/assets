"""Used-crossover chassis camera fits, independent of body outlines.

Picks were re-inspected on 1400-pixel-wide previews.
The interrupted rear picks and wrong near-side sign are discarded. Four near-side wheel anchors
plus a disclosed 1.5 +/- .20 m camera-height prior constrain each pose. Estimated
focal lengths are not EXIF and the original X220 does not copy either silhouette.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('suv_spec.py')));ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']
MATCHES={}
for name,file,size,sgn,picks,paint in [
 ('used_front','suv-used-crv-front.jpg',(5265,3154),1,[(602,642),(1246,575),(591,770),(1233,687)],'Graphite'),
 ('used_rear','suv-used-rav4-rear.jpg',(4809,2934),1,[(108,555),(657,645),(113,672),(655,787)],'Aluminum')]:
 world=[(sgn*.895,F,H),(sgn*.900,R,H),(sgn*.885,F,0),(sgn*.890,R,0)]
 MATCHES[name]=dict(title='Alder X220 / used crossover / '+paint,photo=str(ROOT/('refs/'+file)),crop=(0,0,*size),location=(sgn*7,9 if name=='used_rear' else -9,1.5),target=(0,0,.85),lens=80,lens_bounds_mm=(55,115),camera_height_m=(1.5,.20),background='transparent',paint=paint,exposure=.6,
  landmarks=[dict(world=w,pixel=[v*size[0]/1400 for v in px],weight=1) for w,px in zip(world,picks)])

# Visible far rear tire/contact centroid breaks the planar near-side ambiguity.
# Approximately +/-8 preview pixels: partial occlusion and a soft contact shadow.
MATCHES['used_rear']['landmarks'].append(dict(world=(-.89,R,0),pixel=[1176*4809/1400,741*4809/1400],weight=.35))
