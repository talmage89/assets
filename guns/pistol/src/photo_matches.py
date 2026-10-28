"""Independently selected right/open photo landmarks. No image-derived mesh."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
MATCHES={
 'right_photo':dict(title='Right side / battery',photo=str(BASE/'refs/round2-right.jpg'),
  crop=(60,55,760,535),location=(.7,.045,.10),target=(0,.045,.01),lens=75,lens_bounds_mm=(35,140),exposure=-.6,
  landmarks=[L(w,p,v) for w,p,v in [
   ((12.75,-38,64.5),(165,112),1),((12.75,-38,40),(164,171),1),
   ((12.75,136,64.5),(686,111),1),((12.75,136,40),(690,170),1),
   ((8.9,-28,72),(184,98),.5),((1.6,124,72),(659,104),.5),
   ((14,-45,-51),(126,442),.25),((14,1,-51),(300,475),.25)]]),
 'open_photo':dict(title='Right side / locked open',photo=str(BASE/'refs/round2-open.jpg'),
  crop=(40,55,755,520),location=(.7,.035,.09),target=(0,.035,.01),lens=75,lens_bounds_mm=(35,140),exposure=-.6,
  landmarks=[L(w,p,v) for w,p,v in [
   ((12.75,-72,64.5),(100,111),1),((12.75,-72,40),(99,166),1),
   ((12.75,102,64.5),(595,111),1),((12.75,102,40),(598,165),1),
   ((7,134,54),(695,128),.6),((7,134,46),(695,162),.6),
   ((12,132,31),(710,180),.35),((12,-38,35),(201,186),.35),
   ((14,-45,-51),(169,434),.15),((14,1,-51),(341,455),.15)]]),
}
# The calibrated camera is independent of action selection. The asset renderer
# applies IdleOpen explicitly to the open_photo entry after loading the fit.

# Level the existing left photograph for the comparison canvas only. The kit's
# fitted roll is limited to 20 degrees; this source lies about 30 degrees on the
# page. This reversible image rotation supplies no mesh or material information.
# Pixel picks remain manual observations of named corners, not traced outlines.
from PIL import Image
import math
source=Image.open(BASE/'refs/daylight-side.jpg').convert('RGB')
angle=-30.0
leveled=source.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True,fillcolor=(238,239,236))
photo=BASE/'build/left-leveled.jpg';photo.parent.mkdir(parents=True,exist_ok=True)
leveled.save(photo,quality=98)
def left_pixel(x,y):
 t=math.radians(angle);x-=source.width/2;y-=source.height/2
 return (math.cos(t)*x+math.sin(t)*y+leveled.width/2,
         -math.sin(t)*x+math.cos(t)*y+leveled.height/2)
MATCHES['left_photo']=dict(title='Left side / leveled comparison photograph',
 photo=str(photo),crop=(135,360,1410,1250),
 location=(-.7,.10,.16),target=(0,.045,.01),lens=80,lens_bounds_mm=(35,160),exposure=-.6,
 landmarks=[L(w,left_pixel(*p),weight) for w,p,weight in [
  ((-12.75,136,66.5),(57,535),1),((-12.75,136,39.5),(84,607),1),
  ((-12.75,-38,66.5),(858,64),1),((-12.75,-38,39.5),(918,154),1),
  ((-8.9,-28,72),(814,36),.4),((-1.6,124,72),(100,500),.4),
  ((-14,-45,-51),(1211,546),.15),((-14,1,-51),(1000,671),.15)]])
