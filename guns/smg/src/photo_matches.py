"""Manually observed exterior landmarks; photographs never enter the model."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
# Clean side/quarter samples have retractable stocks. Crop to the class's
# common receiver/furniture; compare our fixed stock in its own fourth pair.
MATCHES={
 'right_photo':dict(title='Right receiver, sights and magazine / retractable reference stock excluded',
  photo=str(BASE/'refs/left.jpg'),crop=(395,20,1200,500),
  location=(1.3,.08,.24),target=(0,.15,.080),lens=75,lens_bounds_mm=(35,140),exposure=-.3,
  landmarks=[L(w,p,weight) for w,p,weight in [
   ((0,-40,131),(427,82),1),((17.8,-40,76),(425,173),1),
   ((0,190,131),(857,86),1),((17.8,190,76),(859,174),1),
   ((0,340.5,163.5),(1107,34),.7),
   ((0,400,95),(1187,147),.4),((14,151,42),(792,238),.4)]]),
 'left_photo':dict(title='Left quarter / charging tube and original slim molding',
  photo=str(BASE/'refs/right.jpg'),crop=(65,245,1285,1110),
  location=(-1.2,.55,.35),target=(0,.15,.060),lens=65,lens_bounds_mm=(35,140),exposure=-.3,
  landmarks=[L(w,p,weight) for w,p,weight in [
   ((0,-40,131),(1178,375),1),((-17.8,-40,76),(1204,533),1),
   ((0,190,131),(768,393),1),((-17.8,190,76),(790,585),1),
   ((0,340.5,163.5),(232,291),.8),((0,400,95),(88,527),.5),
]]),
 'locked_photo':dict(title='Manual handle lock, magazine removed / navy display reference',
  photo=str(BASE/'refs/navy2.jpg'),crop=(560,60,2850,1120),
  location=(-1.1,.45,.45),target=(0,.16,.085),lens=45,lens_bounds_mm=(18,140),exposure=-.3,
  landmarks=[L(w,(400+2*p[0],70+2*p[1]),weight) for w,p,weight in [
   ((0,-40,131),(1112,50),1),((-17.8,-40,76),(1115,157),1),
   ((0,190,131),(648,68),1),((-17.8,190,76),(654,155),1),
   ((0,340.5,163.5),(221,14),.8),((0,400,95),(111,165),.4),
]]),
 'stock_photo':dict(title='Fixed polymer stock / separate original contour comparison',
  photo=str(BASE/'refs/fixed.jpg'),crop=(1025,420,2000,1120),
  location=(-1.2,-.20,.20),target=(0,-.15,.060),lens=80,lens_bounds_mm=(18,140),exposure=-.3,
  landmarks=[L(w,p,weight) for w,p,weight in [
   ((0,-280,107),(1980,600),1),((0,-280,-7),(1962,926),1),
   ((-18,-40,131),(1246,499),1),((-18,-40,73),(1246,721),1),
   ((0,-136,111),(1524,606),.5),((0,-136,57),(1524,766),.5)]]),
 'trigger_photo':dict(title='Trigger concavity, radiused blade and toe / sharp display photograph',
  photo=str(BASE/'refs/trigger-ref.jpg'),crop=(2100,940,2300,1225),
  location=(-.60,.28,.30),target=(0,.061,.027),lens=350,lens_bounds_mm=(40,1200),exposure=-.3,
  landmarks=[L(w,p,weight) for w,p,weight in [
   ((-2.9,72,44),(2154,978),1),((-2.9,56.75,27.5),(2188,1070),1),
   ((-2.9,49.625,26.375),(2226,1070),1),((0,65.98,8.72),(2177,1159),1)]]),
}

# Original staged photograph; preserve the inherited form-comparison camera.
MATCHES["paint_studio_photo"]=dict(MATCHES["left_photo"],
 title="Original staged photo / independent nonpaint light anchors",photo=str(BASE/"refs/studio-original.jpg"))

# Independent paint camera: observed near-side view; historical form cameras stay intact.
MATCHES["paint_issued_photo"]=dict(MATCHES["locked_photo"],
 title="Issued paint / constrained observed side view",fixed_view=True,
 location=(-3.,.70,.50),target=(0,.10,.09),lens=300,lens_bounds_mm=(300,300))
MATCHES["paint_issued_photo"]["landmarks"]=[dict(r,world=[r['world'][0],.3625,r['world'][2]])
 if abs(r['world'][1]-.3405)<1e-6 else dict(r) for r in MATCHES["paint_issued_photo"]["landmarks"]]
