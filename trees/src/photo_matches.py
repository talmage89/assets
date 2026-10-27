"""Approximate anatomical fits between different living specimens.

Only the summer half of OSU's seasonal comparison is used. Height/DBH were not
surveyed in either photo. World anchors express the brief's target envelope;
biological variation and unknown depth are reflected in the reported residuals.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={
 'match_psu':dict(title='Summer crown / Penn State',photo=str(R/'refs/psu-form.jpg'),crop=(90,0,835,675),
  location=(0,-23,1.7),target=(0,0,6.0),lens=43,background='transparent',camera_height_m=(1.7,.12),lens_bounds_mm=(28,80),landmarks=[
   dict(world=(0,0,0),pixel=(468,659),weight=3),
   dict(world=(.05,0,12.50),pixel=(446,34),weight=4),
   dict(world=(-4.8,0,6.1),pixel=(135,399),weight=.035),
   dict(world=(4.8,0,6.5),pixel=(817,349),weight=.035),
   dict(world=(0,0,2.5),pixel=(471,534),weight=.35),
  ]),
 'match_osu':dict(title='Summer crown / Oregon State',photo=str(R/'refs/osu-form.jpg'),crop=(704,0,1425,898),
  location=(0,-24,1.7),target=(0,0,6),lens=42,background='transparent',camera_height_m=(1.7,.12),lens_bounds_mm=(28,80),landmarks=[
   dict(world=(0,0,0),pixel=(1089,841),weight=3),
   dict(world=(.05,0,12.50),pixel=(1090,22),weight=4),
   dict(world=(-4.8,0,6.3),pixel=(748,470),weight=.035),
   dict(world=(4.8,0,6.3),pixel=(1404,475),weight=.035),
   dict(world=(0,0,2.5),pixel=(1076,682),weight=.35),
  ])}
