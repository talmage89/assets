"""Observed exterior landmarks. No image is sampled or traced into geometry."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
RIGHT=[((17.5,-35,86),(578,162),1),((17.5,-35,50),(579,244),1),
 ((17.5,220,86),(1137,150),1),((17.5,220,50),(1137,230),1),
 ((0,595,85),(1996,184),.5),((0,-285,35),(64,289),.5),
 ((0,365,85),(1470,176),.6)]
LEFT=[((-17.5,-35,86),(1466,798),1),((-17.5,-35,50),(1468,888),1),
 ((-17.5,220,86),(908,793),1),((-17.5,220,50),(910,881),1),
 ((0,595,85),(52,854),.5),((0,-285,35),(1980,936),.5),
 ((0,365,85),(571,846),.6)]
MATCHES={}
for name,landmarks,crop,loc in [('right_photo',RIGHT,(0,0,2050,650),(2.8,.16,.25)),
 ('left_photo',LEFT,(0,650,2050,1300),(-2.8,.16,.25)),
 ('receiver_photo',RIGHT[:4],(555,85,1155,333),(2.5,.10,.15))]:
 MATCHES[name]=dict(title=name.replace('_',' ')+' / original exterior contours',
  photo=str(BASE/'build/white-balanced/museum.jpg'),crop=crop,location=loc,
  target=(0,.10,.075),lens=100,lens_bounds_mm=(45,180),exposure=-.3,
  landmarks=[L(w,p,weight) for w,p,weight in landmarks])
# A separate blade crop uses the same receiver-camera orientation. Its short
# native baseline limits contour metrology; the image still judges concavity.
MATCHES['trigger_photo']=dict(MATCHES['right_photo'],title='Trigger blade direction and thickness',
 crop=(720,245,850,335),lens=700,lens_bounds_mm=(50,1600),landmarks=[L(w,p,v) for w,p,v in RIGHT[:4]])
MATCHES['trigger_sharp']=dict(title='Concave muzzle-facing blade / sharp wet left photograph',
 photo=str(BASE/'build/white-balanced/trigger-sharp.jpg'),crop=(3070,1070,3215,1225),
 location=(-.55,.20,.22),target=(0,.048,.032),lens=300,lens_bounds_mm=(100,1400),exposure=-.3,
 landmarks=[L(w,p) for w,p in [((-3,53,50),(3114,1082)),((-3,46,34),(3143,1145)),
  ((-3,65,20),(3091,1203)),((-3,43,50),(3185,1090)),((-3,40,34),(3177,1145)),
  ((-3,64,16.5),(3102,1215))]])
