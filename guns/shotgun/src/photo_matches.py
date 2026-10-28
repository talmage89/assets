"""Independent observed landmarks; source images are comparison-only."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
def l(w,p,v=1):return L((w[0],w[1]+55,w[2]-16),p,v)
MATCHES={
 'wood_photo':dict(title='Sharp used walnut / grain and finish structure',
  photo=str(BASE/'refs/stock-sharp.jpg'),crop=(140,75,1820,950),
  location=(1.3,-.10,.17),target=(0,-.10,-.025),lens=70,lens_bounds_mm=(35,140),exposure=-.15,
  landmarks=[l(w,p,v) for w,p,v in [
   ((0,-298,20),(255,345),1),((0,-284.6,-102),(184,918),1),
   ((0,-18,66),(1762,96),1),((17.1,-18,18),(1785,282),1)]]),
 'used_photo':dict(title='Used blued steel and walnut / daylight / different sighted barrel',photo=str(BASE/'refs/daylight-used.jpg'),
  crop=(5,80,4790,810),location=(2.3,.20,.20),target=(0,.18,.01),lens=70,lens_bounds_mm=(35,140),exposure=-.15,
  landmarks=[l(w,(p[0]*4793/2048,p[1]*4793/2048),v) for w,p,v in [
   ((0,-18,66),(678,72),1),((0,55,80),(820,56),1),
   ((0,195,78),(1072,81),1),((17.6,195,22),(1063,193),1),
   ((17.7,8,18),(727,173),1),((0,-322,20),(24,100),.5),
   ((0,-308,-102),(25,334),.5),((0,645,80.6),(1992,191),.4)]]),
 'right_photo':dict(title='Right receiver and carved stock / reference has shorter barrel',photo=str(BASE/'refs/wood-side.jpg'),
  crop=(10,25,1270,335),location=(2,.18,.17),target=(0,.16,.01),lens=70,lens_bounds_mm=(35,140),exposure=-.6,
  # Receiver/barrel and butt envelope set scale and perspective. Comb and wrist
  # outlines are independent review measurements, not camera-fit inputs.
  landmarks=[l(w,p,v) for w,p,v in [
   ((0,195,78),(760,55),1),((15.1,195,22),(761,134),1),
   ((0,-18,66),(489,74),1),((15.5,-18,18),(495,132),1),
   ((0,55,80),(585,50),1),((0,250,65),(829,76),.6),
   ((0,-322,20),(25,144),1),((0,-308,-102),(42,310),1)]]),
 'left_photo':dict(title='Left receiver, wrist and comb / field configuration reference',photo=str(BASE/'refs/hunter.jpg'),
  crop=(1950,650,3150,1120),location=(-2.5,.18,1.0),target=(0,.08,.01),lens=70,lens_bounds_mm=(35,140),exposure=-.6,
  landmarks=[l(w,tuple(q*2 for q in p),v) for w,p,v in [
   ((0,195,80),(1027,396),1),((0,-10,80),(1218,379),1),
   ((-17.75,195,19),(1030,454),1),((-17.75,-16,19),(1224,438),1),
   ((0,-305,20),(1517,415),.25),((0,-305,-102),(1537,528),.25),
   ((-17.75,8,29),(1199,438),.4),((-17.75,69,29),(1145,443),.4)]]),
 'open_photo':dict(title='Open action / receiver comparison / tactical reference furniture',photo=str(BASE/'refs/left.jpg'),
  crop=(250,30,463,105),location=(1.8,.20,.30),target=(0,.17,.05),lens=70,lens_bounds_mm=(35,140),exposure=-.6,
  landmarks=[l(w,p,v) for w,p,v in [
   ((0,-10,80),(300,40),.4),((0,195,80),(453,40),1),
   ((17.75,-16,19),(263,98),.3),((17.75,195,19),(454,103),1),
   ((17.75,94,76),(368,45),1),((17.75,177,76),(442,45),1),
   ((17.75,94,51),(365,63),1),((17.75,177,51),(441,65),1)]]),
}
