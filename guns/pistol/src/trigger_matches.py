"""Guard-landmark trigger comparisons; reference contours never drive meshes."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
MATCHES={
 'trigger_right_photo':dict(title='Trigger / right side / muzzle right',
  photo=str(BASE/'refs/trigger-right.JPG'),crop=(0,0,1920,1440),trigger_crop=(780,420,1330,800),camera_height_m=(.005,.005),
  location=(.4,.047,.016),target=(0,.047,.012),lens=70,lens_bounds_mm=(35,140),exposure=-.15,
  matched_view=dict(target=(0,.048,.01275),direction=(1,.04,-.03),anchor_pixel=(962,579),span_pixels=206,span_m=.0205),
  landmarks=[L(w,p) for w,p in [
   ((7,31,-2.2),(902,681)),((7,55,-2.2),(1193,679)),
   ((7,58,10),(1233,562)),((7,54.5,24),(1203,479)),
   ((7,32.5,24),(951,491)),((7,57,-9),(1212,748))]]),
 'trigger_quarter_photo':dict(title='Trigger / three-quarter / muzzle left',
  photo=str(BASE/'refs/daylight-quarter.JPG'),crop=(0,0,4608,3456),trigger_crop=(1650,1100,2600,1950),
  location=(-.45,.22,-.14),target=(0,.047,.014),lens=70,lens_bounds_mm=(35,140),exposure=-.15,
  matched_view=dict(target=(0,.048,.01275),direction=(-1,.25,-.22),anchor_pixel=(2350,1445),span_pixels=300,span_m=.0205),
  landmarks=[L(w,p,v) for w,p,v in [
   ((-12.75,136,66.5),(1020,790),1),((-12.75,136,39.5),(907,982),1),
   ((-12.75,-38,66.5),(3738,807),1),((-12.75,-38,39.5),(3788,1016),1),
   ((-7,44,-9),(2040,1798),.25)]])}
