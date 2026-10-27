"""Different living specimens: approximate anatomical cameras, not survey fits."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={
 'match_green_velvet':dict(title='Green Velvet / Jim Robbins, NC State',photo=str(R/'refs/boxwood-form.jpg'),crop=(245,80,890,650),location=(0,-2.7,1.45),target=(0,0,.45),lens=55,background='transparent',camera_height_m=(1.45,.18),lens_bounds_mm=(35,85),landmarks=[
  dict(world=(0,0,0),pixel=(553,606),weight=2),
  dict(world=(0,0,.9),pixel=(552,122),weight=2),
  dict(world=(-.50,0,.43),pixel=(292,378),weight=.22),
  dict(world=(.50,0,.43),pixel=(848,392),weight=.22),
  dict(world=(0,-.40,.40),pixel=(558,480),weight=.12),
 ]),
 'match_clipped':dict(title='Clipped Buxus / A. Niemiera, Virginia Tech',photo=str(R/'refs/boxwood-rounded.jpg'),crop=(150,10,720,423),location=(0,-2.7,1.3),target=(0,0,.44),lens=55,background='transparent',camera_height_m=(1.3,.18),lens_bounds_mm=(35,85),landmarks=[
  dict(world=(0,0,0),pixel=(444,413),weight=2),
  dict(world=(0,0,.9),pixel=(450,40),weight=2),
  dict(world=(-.50,0,.43),pixel=(193,265),weight=.20),
  dict(world=(.50,0,.43),pixel=(665,263),weight=.20),
  dict(world=(0,-.40,.40),pixel=(444,323),weight=.12),
 ]),
}
