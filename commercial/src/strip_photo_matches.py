"""Sparse storefront fits to three used strip-center photographs.

Bay dimensions are our original authored comparators, not surveyed widths of
these buildings. Held-out roof, sign, parking and construction differences stay
visible. Wikimedia picks derive from a 1400px inspection; brochure picks use
its native 1164px JPEG. The older California center is auxiliary context.
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
m3=p['modules'][1];xl3=xl+m3['origin'][0]-m['origin'][0];xr3=xr+m3['origin'][0]-m['origin'][0];fy=m3['origin'][1]-.04
sterling=[point(world,pixel,label) for world,pixel,label in (
    ((xl3,fy,2.75),(1083,272),'clear right-pavilion window upper left'),
    ((xr3,fy,2.75),(1114,273),'clear right-pavilion window upper right'),
    ((xr3,fy,.27),(1114,322),'clear right-pavilion window lower right'),
    ((xl3,fy,.27),(1083,321),'clear right-pavilion window lower left'))]
MATCHES={
    'commerce':dict(title='Used Texas row / storefront height, bay subdivision and sign fascia',photo='build/strip/references/commerce-neutral.png',crop=(500,1150,5200,3250),
                    location=(m['origin'][0]+12,front-18,1.65),target=(m['origin'][0]+3,front,2.3),lens=36,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),landmarks=commerce,background='transparent',exposure=-.15),
    'sunnyvale':dict(title='Used California row / mansard, glazing and masonry piers',photo='build/strip/references/sunnyvale-neutral.png',crop=(100,1350,3350,2350),
                     location=(m2['origin'][0]+7,front2-25,1.65),target=(m2['origin'][0]+4,front2,2.5),lens=38,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),landmarks=sunnyvale,background='transparent',exposure=-.15),
    'sterling':dict(title='Documented 1989 Virginia center / glazing, shelter and entry punctuation',photo='build/strip/references/sterling-neutral.png',crop=(600,170,1164,350),
                    location=(m3['origin'][0]+25,fy-55,1.65),target=(m3['origin'][0],fy,2.3),lens=40,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),landmarks=sterling,background='transparent',exposure=-.15),
}
PAIR_SEEDS=dict(commerce=201,sunnyvale=202,sterling=201)
LIGHTING=dict(commerce=dict(sun_direction=(.65,.25,-1),sun_energy=3.0,sky_strength=.06,sky_saturation=.60),
              sunnyvale=dict(sun_direction=(.30,.15,-1),sun_energy=3.2,sky_strength=.035,sky_saturation=.85),
              sterling=dict(sun_direction=(-.50,.40,-1),sun_energy=3.2,sky_strength=.04,sky_saturation=.75))

# Look checkpoint: four dated-period views plus rear/older-paving auxiliaries.
# Window picks are sparse, unsurveyed fit anchors; material ROIs are held out.
p202=generate(202);mm=p202['modules'][0];ww=mm['width'];dx2=-ww*.23
lo2=dx2+.9144/2+.07;hi2=ww/2-.31;sp2=(hi2-lo2)/max(1,round((hi2-lo2)/1.50));cc=lo2+sp2/2
lx=mm['origin'][0]+cc-(sp2-.035)/2;rx=lx+sp2-.035;ff=mm['origin'][1]-.04

def pane(lt,rt,rb,lb):
    return [point(q,pixel,label) for q,pixel,label in (
        ((lx,ff,2.75),lt,'held glazing upper left'),((rx,ff,2.75),rt,'held glazing upper right'),
        ((rx,ff,.27),rb,'held glazing lower right'),((lx,ff,.27),lb,'held glazing lower left'))]

MATCHES['period_walk']=dict(title='1985/86 center at 21–22 years / covered walk, glazing and accumulated service',photo='build/strip/references/westlakes-neutral.png',crop=(140,220,900,595),
    location=(mm['origin'][0]+14,ff-14,1.65),target=(mm['origin'][0],ff,2),lens=40,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),
    landmarks=pane((378,346),(430,352),(430,466),(378,477)),background='transparent',exposure=.1)
MATCHES['period_lot']=dict(title='1985/86 center at 21–22 years / sidewalk edge and repaired asphalt',photo='build/strip/references/westlakes_lot-neutral.png',crop=(110,270,911,608),
    location=(mm['origin'][0]-14,ff-17,1.65),target=(mm['origin'][0]+3,ff,2),lens=40,lens_bounds_mm=(24,100),camera_height_m=(1.65,.35),
    landmarks=pane((251,321),(289,326),(289,459),(251,466)),background='transparent',exposure=.1)
# Rear door stands in a rotated real aperture, independently of the storefront fit.
rp=generate(201);rm=rp['modules'][1];cx=rm['origin'][0]-rm['width']*.20;ry=rp['building']['rear']+.05
rear_anchors=[point(q,pixel,label) for q,pixel,label in (
    ((cx+.492,ry,2.268),(278,193),'rear steel upper left'),((cx-.492,ry,2.268),(306,192),'rear steel upper right'),
    ((cx-.492,ry,.158),(307,272),'rear steel lower right'),((cx+.492,ry,.158),(279,273),'rear steel lower left'))]
MATCHES['used_rear']=dict(title='Used strip-center rear / date unverified; service and base-damp auxiliary',photo='build/strip/references/rear-neutral.png',crop=(35,90,590,365),
    location=(cx,ry+22,1.7),target=(cx,ry,2),lens=45,lens_bounds_mm=(24,100),camera_height_m=(1.7,.4),landmarks=rear_anchors,background='transparent',exposure=.1)
PAIR_SEEDS.update(period_walk=202,period_lot=202,used_rear=201)
LIGHTING.update(period_walk=dict(sun_direction=(-.75,-.35,-.65),exposure=.15,sun_energy=6,sky_strength=.035,sky_saturation=1),
    period_lot=dict(sun_direction=(.72,-.75,-.62),exposure=1.25,sun_energy=6,sky_strength=.035,sky_saturation=1),
    used_rear=dict(sun_direction=(.25,-.45,-1),sun_energy=0,sky_strength=.35,sky_saturation=.10,sun_angle=20))

# Outdoor comparison skies remain procedural and visible, as on the station.
for match in MATCHES.values():match.pop('background',None)
