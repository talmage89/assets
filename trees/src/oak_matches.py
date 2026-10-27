"""Different specimens: approximate composition fits, not surveyed dimensions.

OSU summer: some apex tips leave the photo. Stony Brook: neighboring crown
occludes the left edge. Downweight those biological anchors; keep residuals.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={
 'oak_match_osu':dict(title='Pin oak / Oregon State summer habit',photo=str(R/'refs/oak-osu-summer.jpg'),crop=(0,0,584,900),
  location=(0,-32,1.7),target=(0,0,8.2),lens=45,background='transparent',camera_height_m=(1.7,.15),lens_bounds_mm=(28,80),landmarks=[
   dict(world=(0,0,0),pixel=(290,870),weight=5),
   dict(world=(0,0,16.7),pixel=(303,9),weight=2),
   dict(world=(-4.9,0,5.5),pixel=(29,578),weight=.04),
   dict(world=(4.9,0,5.5),pixel=(544,573),weight=.04),
   dict(world=(0,0,2.6),pixel=(287,730),weight=.15)]),
 'oak_match_stony':dict(title='Pin oak / Stony Brook summer street planting',photo=str(R/'refs/oak-stony-summer.png'),crop=(0,0,2142,2856),
  location=(0,-26,1.7),target=(0,0,8.2),lens=39,background='transparent',camera_height_m=(1.7,.15),lens_bounds_mm=(24,80),landmarks=[
   dict(world=(0,0,0),pixel=(1070,2728),weight=5),
   dict(world=(0,0,16.7),pixel=(879,214),weight=4),
   dict(world=(-4.9,0,7.7),pixel=(365,1515),weight=.015),
   dict(world=(4.9,0,7.7),pixel=(2095,1505),weight=.04),
   dict(world=(0,0,2.6),pixel=(1054,2340),weight=.15)])}

# Display-light matching only, documented in the evidence. Same authored albedo
# in both cameras. The old OSU slide is never an absolute reflectance target.
MATCHES['oak_match_osu']['lighting']=dict(sun_energy=11,sky_strength=.25,exposure=1.05)
MATCHES['oak_match_stony']['lighting']=dict(sun_energy=7.6,sky_strength=.22,exposure=.5)
