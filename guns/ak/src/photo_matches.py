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
 crop=(720,235,890,335),location=(1,.05,.10),target=(0,.045,.03),lens=400,lens_bounds_mm=(80,1400),
 landmarks=[L(w,p) for w,p in [((0,3,48),(739,255)),((0,73,48),(847,251)),
  ((0,15,16),(742,314)),((0,71,15),(839,312))]])
# Receiver envelope anchors set the scale for the trigger and front-sight crops.
# No trigger contour is allowed to resize its own camera to conceal a mismatch.
SHARP=[((-17.5,220,86),(2230,823)),((-17.5,220,50),(2246,1042)),
       ((-17.5,-35,86),(3608,886)),((-17.5,-35,50),(3605,1084)),
       ((0,100,113),(2870,733))]
for name,crop,title in [('trigger_sharp',(3000,1020,3290,1260),'Compact trigger / external receiver scale anchors')]:
 MATCHES[name]=dict(title=title,photo=str(BASE/'build/white-balanced/trigger-sharp.jpg'),crop=crop,
  location=(-2,.20,.55),target=(0,.15,.07),lens=500,lens_bounds_mm=(80,1400),exposure=-.3,
  landmarks=[L(w,p) for w,p in SHARP])
MATCHES['front_sight_photo']=dict(title='Forged front tower / open protective ears',
 photo=str(BASE/'build/white-balanced/trigger-sharp.jpg'),crop=(245,625,460,1015),
 location=(-.7,.55,.2),target=(0,.552,.105),lens=140,lens_bounds_mm=(50,600),exposure=-.3,
 landmarks=[L(w,p) for w,p in [((-10,562,85),(317,948)),((-10,543,85),(402,950)),
  ((-11,552,117),(365,766)),((-10,552,73.5),(362,1007))]])
for name,crop,title in [('trigger_guard',(705,235,905,350),'Compact trigger and flat stamped guard'),
 ('topcover_side',(560,60,1080,185),'Pressed transverse cover ribs / side'),
 ('selector_photo',(590,150,1120,290),'Stamped selector / hub, widening blade and folded tab')]:
 MATCHES[name]=dict(MATCHES['right_photo'],title=title,crop=crop)
MATCHES['trigger_guard']=dict(MATCHES['trigger_photo'],title='Compact trigger and flat stamped guard',crop=(705,235,905,350))
MATCHES['selector_photo']=dict(MATCHES['receiver_photo'],
 title='Stamped selector / hub, widening blade and folded tab',
 crop=(570,90,1140,290))
# The local saddle's nonplanar corners admit a false elevated-camera solution.
# Use the same independent long receiver baseline as the sharp trigger instead.
MATCHES['rear_sight_side']=dict(MATCHES['trigger_sharp'],
 title='Tangent leaf and forged block / sharp side / receiver-scale anchors',
 crop=(1980,600,2440,850))
MATCHES['rear_sight_photo']=dict(title='Tangent leaf, cylindrical releases and forged saddle / above-behind',
 photo=str(BASE/'build/white-balanced/rear-sight.jpg'),crop=(900,580,2390,1780),
 location=(-.30,-.05,.35),target=(0,.22,.115),lens=85,lens_bounds_mm=(35,240),exposure=-.3,
 landmarks=[L(w,p) for w,p in [((-6.7,248,123),(1303,887)),((6.7,248,123),(1426,786)),
  ((-6.7,190,124),(1870,1510)),((6.7,190,124),(2020,1370))]])
# Oblique cover crop from a museum display. Sparse exterior receiver corners
# determine its frame; reflected glass and the display wire are excluded from form.
MATCHES['topcover_top']=dict(title='Cover crown and pressed ribs / oblique above',
 photo=str(BASE/'build/white-balanced/exhibit-rotated.jpg'),crop=(181,1390,511,1660),
 location=(.7,-.2,.7),target=(0,.09,.09),lens=120,lens_bounds_mm=(40,350),exposure=-.3,
 landmarks=[L(w,(1401-p[1],p[0])) for w,p in [((17.5,220,86),(1597,902)),((17.5,220,50),(1669,911)),
  ((17.5,-35,86),(1462,1192)),((17.5,-35,50),(1532,1204)),
  ((0,190,113),(1532,942)),((0,-35,110),(1415,1162))]])
