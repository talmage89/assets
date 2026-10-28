"""Manual class landmarks. Photos never enter model or materials."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from guns.common.photo_matches import L
def anchors(rows,scale=1):return [L(w,(p[0]*scale,p[1]*scale),v) for w,p,v in rows]
MATCHES={
 'right_photo':dict(title='Right / precision rifle class, 20-inch reference',
  photo=str(BASE/'refs/left.jpg'),crop=(10,25,1135,320),
  location=(1.8,.2,.32),target=(0,.2,.055),lens=70,lens_bounds_mm=(35,140),exposure=-.6,
  landmarks=anchors([
   ((0,-310,68),(47,151),1),((0,-310,-30),(30,289),1),
   ((0,444,48),(886,132),1),((0,437,26),(880,171),1),
   ((0,-125,113),(324,87),.35),((0,232,113),(724,87),.35),
   ((0,45,65),(435,136),.4),((0,224,65),(612,136),.4)])),
}

# Round 2: clean true side photographs and sharp local action photography.
# A mechanism baseline calibrates the close-ups; original stock differences stay visible.
MATCHES.update({
 'profile_right':dict(title='Clean right / USAF M24 class',
  photo=str(BASE/'refs/m24_profile.jpg'),crop=(0,0,2100,445),
  location=(2.8,.55,.30),target=(0,.25,.06),lens=80,lens_bounds_mm=(45,140),exposure=-1.1,
  landmarks=anchors([
   ((0,819.6,65),(1170,83),1),((17.5,45,65),(401,105),1),
   ((17.5,224,65),(568,96),1),((0,-310,75),(35,107),.5),
   ((0,-310,-46),(38,215),.5),((17.5,45,82),(400,89),1),
   ((17.5,45,48),(401,129),1),((0,819.6,76.8),(1168,73),1)],2100/1200)),
 'left_photo':dict(title='Clean left / PEO Soldier M24 class',
  photo=str(BASE/'refs/PEO_M24_SWS-01.jpg'),crop=(0,180,2936,1000),
  location=(-3.3,-.15,.30),target=(0,.25,.06),lens=105,lens_bounds_mm=(105,105),exposure=-1.1,
  landmarks=anchors([
   ((0,819.6,65),(72,204),1),((-17.5,45,65),(809,220),1),
   ((-17.5,224,65),(635,209),1),((0,-310,75),(1132,229),.5),
   ((0,-310,-46),(1124,336),.5),((-17.5,45,82.5),(808,202),1),
   ((-17.5,45,47.5),(810,234),1),((0,819.6,76.8),(72,195),1)],2936/1200)),
 'open_photo':dict(title='Sharp open action / collar, port and raceway',
  photo=str(BASE/'refs/detail_030.jpg'),crop=(0,0,2400,827),
  location=(.8,.15,.28),target=(0,.10,.06),lens=100,lens_bounds_mm=(65,140),exposure=-1.0,
  landmarks=anchors([
   ((10.8,-69,65),(150,88),1),((17.5,45,65),(585,85),1),
   ((17.5,100,52),(742,151),1),((17.5,172,52),(990,149),1),
   ((8,100,80),(741,34),1),((8,172,80),(988,32),1),
   ((0,224,82.5),(1160,20),.6),((0,224,47.5),(1160,139),.6)],2)),
 'wrist_photo':dict(title='Large wrist / inlet and grip transition',
  photo=str(BASE/'refs/detail_029.jpg'),crop=(0,0,1600,778),
  location=(.6,-.10,.22),target=(0,.005,.055),lens=100,lens_bounds_mm=(65,140),exposure=-1.1,
  landmarks=anchors([
   ((17.5,45,82),(600,27),1),((17.5,45,48),(600,149),1),
   ((10.8,35,65),(572,90),1),((6,-1,65),(444,97),1),
   ((8,100,80),(750,34),1),((17.5,100,52),(750,153),1)],2329/1200)),
})

# Used field finish comparison, retained alongside the sharper form photo.
# The coating differs from our original web paint; this view judges the wear
# mechanism and material separation, not a copied camouflage pattern.
MATCHES['used_open']=dict(title='Used field rifle / open bolt, contact wear and coating',
 photo=str(BASE/'refs/open.jpg'),crop=(330,170,2990,1430),
 location=(.7,-.25,.34),target=(0,.06,.09),lens=70,lens_bounds_mm=(35,150),exposure=-.15,
 landmarks=anchors([
  ((19,-125,113),(184,274),.7),((19,-18,113),(444,249),1),
  ((19,123,113),(738,220),1),((0,62,151.5),(582,102),.5),
  ((17,187,65),(754,352),1),((17,100,65),(540,390),1),
  ((17,200,79),(782,311),.7),((17,100,49),(573,417),.7)],3008/1200))
