"""Whole shrub and foundation-row specimens; unsurveyed living individuals."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={
 'hyd_match_house':dict(title='Mophead by house / Ilouque, NC State',photo=str(R/'refs/hydrangea-ilouque.jpg'),crop=(12,10,570,382),location=(0,-3.65,1.65),target=(0,0,.58),lens=55,background='transparent',camera_height_m=(1.65,.18),lens_bounds_mm=(35,85),landmarks=[
  dict(world=(0,0,0),pixel=(289,357),weight=2),
  dict(world=(0,0,1.2),pixel=(286,25),weight=2),
  dict(world=(-.70,0,.60),pixel=(41,200),weight=.22),
  dict(world=(.70,0,.60),pixel=(528,211),weight=.22),
 ]),
 'hyd_match_bed':dict(title='Summer foundation bed / Jim Janke, NC State',photo=str(R/'refs/hydrangea-summer.jpg'),crop=(5,0,650,677),location=(0,-3.8,1.6),target=(0,0,.57),lens=55,background='transparent',camera_height_m=(1.6,.18),lens_bounds_mm=(35,85),landmarks=[
  dict(world=(0,0,0),pixel=(316,630),weight=2),
  dict(world=(0,0,1.2),pixel=(325,20),weight=2),
  dict(world=(-.70,0,.60),pixel=(30,319),weight=.18),
  dict(world=(.70,0,.60),pixel=(625,366),weight=.18),
 ]),
}
# Tight lit/front leaf and bloom regions, in original photographic coordinates.
PATCHES={
 'hyd_match_house':dict(crop=MATCHES['hyd_match_house']['crop'],foliage=(105,60,495,325),flower=(105,60,495,325),shade=(275,255,370,321)),
 'hyd_match_bed':dict(crop=MATCHES['hyd_match_bed']['crop'],foliage=(90,80,563,560),flower=(90,80,563,560),shade=(232,328,294,390)),
}
