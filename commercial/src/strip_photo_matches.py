"""Sparse storefront fits to two used strip-center photographs.

Bay dimensions are our original authored comparators, not surveyed widths of
these buildings. Held-out roof, sign, parking and construction differences stay
visible. Native-coordinate picks derive from a documented 1400px inspection.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from strip_plan import generate


def point(world,pixel,label):return dict(world=world,pixel=pixel,label=label)


p=generate(201);m=p['modules'][0];w=m['width'];dx=-w*.23;dw=.9144
lo=dx+dw/2+.07;hi=w/2-.31;span=(hi-lo)/3;center=lo+span/2;width=span-.035
xl=m['origin'][0]+center-width/2;xr=xl+width;front=m['origin'][1]-.04
factor=6000/1400
commerce=[point(world,tuple(v*factor for v in pixel),label) for world,pixel,label in (
    ((xl,front,2.75),(328,460),'empty bay window, upper left'),
    ((xr,front,2.75),(400,463),'empty bay window, upper right'),
    ((xr,front,.27),(400,607),'empty bay window, lower right'),
    ((xl,front,.27),(328,609),'empty bay window, lower left'))]
p2=generate(202);m2=p2['modules'][0];xl2=m2['origin'][0]-m2['width']/2;xr2=xl2+m2['width'];front2=m2['origin'][1]
factor2=4000/1400
sunnyvale=[point(world,tuple(v*factor2 for v in pixel),label) for world,pixel,label in (
    ((xl2,front2,2.75),(214,601),'masonry/frontage station, upper left'),
    ((xr2,front2,2.75),(516,606),'masonry/frontage station, upper right'),
    ((xr2,front2,.1524),(516,712),'frontage station, pavement right'),
    ((xl2,front2,.1524),(214,709),'frontage station, pavement left'))]
MATCHES={
    'commerce':dict(title='Used Texas row / storefront height, bay subdivision and sign fascia',photo='build/strip/references/commerce-neutral.png',crop=(500,1150,5200,3250),
                    location=(m['origin'][0]+12,front-18,1.65),target=(m['origin'][0]+3,front,2.3),lens=36,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),landmarks=commerce,background='transparent',exposure=-.15),
    'sunnyvale':dict(title='Used California row / mansard, glazing and masonry piers',photo='build/strip/references/sunnyvale-neutral.png',crop=(100,1350,3350,2350),
                     location=(m2['origin'][0]+7,front2-25,1.65),target=(m2['origin'][0]+4,front2,2.5),lens=38,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),landmarks=sunnyvale,background='transparent',exposure=-.15),
}
PAIR_SEEDS=dict(commerce=201,sunnyvale=202)
LIGHTING=dict(commerce=dict(sun_direction=(.65,.25,-1),sun_energy=3.0,sky_strength=.06,sky_saturation=.60),
              sunnyvale=dict(sun_direction=(.30,.15,-1),sun_energy=3.2,sky_strength=.035,sky_saturation=.85))
