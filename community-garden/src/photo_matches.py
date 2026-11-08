"""Measured review landmarks. Unsurveyed gardens: along-edge phases are inferred.

Pixel coordinates refer to prepared 1024px wide copies, avoiding false subpixel
precision from oversized originals. The source photographs remain untouched.
"""
from pathlib import Path
import math
P=Path('build/photo-references')
MATCHES={
    'wise_bed':dict(title='Mature raised bed / July 2010',photo=str(P/'wise.jpg'),crop=(0,0,1024,768),
        location=(-2.3,-4.2,1.65),target=(0,0,.55),lens=38,lens_bounds_mm=(28,65),camera_height_m=(1.65,.30),
        landmarks=[
            dict(world=[-.6096,-1.2192,.28575],pixel=[153,561],weight=1),
            dict(world=[.6096,-1.2192,.28575],pixel=[420,607],weight=1),
            dict(world=[.6096,1.2192,.28575],pixel=[690,466],weight=1),
            dict(world=[-.6096,1.2192,.28575],pixel=[493,410],weight=.25)],
        exposure=-.35),
    'oliver_construction':dict(title='Bed construction / August installation',photo=str(P/'oliver.jpg'),crop=(0,0,1024,768),
        location=(.30,-2.5,1.75),target=(0,0,.22),lens=40,lens_bounds_mm=(28,65),camera_height_m=(1.75,.25),
        landmarks=[
            dict(world=[-.55,1.20,.23495],pixel=[486,248],weight=.6),
            dict(world=[.55,1.20,.23495],pixel=[754,232],weight=.6),
            dict(world=[.57,.8,.23495],pixel=[807,314],weight=.35),
            dict(world=[.57,-1.2,.23495],pixel=[923,750],weight=.35),
            dict(world=[.6096,-.8,.23495],pixel=[932,646],weight=.3),
            dict(world=[.6096,-.8,.16],pixel=[944,659],weight=.3)],
        exposure=-.35),
    'martin_place':dict(title='Neighborhood entrance / July 2009',photo=str(P/'martin.jpg'),crop=(0,0,1024,768),
        location=(3.2,-20,1.65),target=(3.4,-10,1.3),lens=40,lens_bounds_mm=(30,60),camera_height_m=(1.65,.15),
        landmarks=[
            dict(world=[3.4-.525,-12.192+.218,1.45+.33],pixel=[486,369]),
            dict(world=[3.4+.525,-12.192+.218,1.45+.33],pixel=[639,370]),
            dict(world=[3.4+.525,-12.192+.218,1.45-.33],pixel=[632,467]),
            dict(world=[3.4-.525,-12.192+.218,1.45-.33],pixel=[486,467]),
            dict(world=[3.4-.441,-12.192+.25,.05],pixel=[500,659],weight=.5),
            dict(world=[3.4+.441,-12.192+.25,1.90],pixel=[619,346],weight=.5)],
        exposure=-.35)
}

# Third in-season photograph. Board ends leave frame and are inferred: low
# weights keep this a habit/value comparison rather than a surveyed bed fit.
MATCHES['cityhall_mature']=dict(title='Overlapping summer crops / July 2010',photo=str(P/'cityhall.jpg'),crop=(0,0,1024,1365),
    location=(-.12,-3.8,1.65),target=(0,0,.65),lens=38,lens_bounds_mm=(28,65),camera_height_m=(1.65,.25),
    landmarks=[dict(world=[-1.2192,-.6096,.28575],pixel=[0,1040],weight=.3),
               dict(world=[1.2192,-.6096,.28575],pixel=[1024,1025],weight=.3),
               dict(world=[-1.2192,.6096,.28575],pixel=[0,690],weight=.3),
               dict(world=[1.2192,.6096,.28575],pixel=[1024,680],weight=.3)],exposure=-.35)
# The installation photograph remains in the archived form review only.
MATCHES.pop('oliver_construction')

# Out-of-frame board ends do not constrain pose reliably. The visible hoop's
# ellipse supplies an inferred comparison scale, not a survey of the real cage.
MATCHES['cityhall_mature'].update(location=(.76,-4.5,1.65),target=(.76,0,.75),
    landmarks=[dict(world=[.76-.296,0,1.40375],pixel=[400,483]),
               dict(world=[.76+.296,0,1.40375],pixel=[585,468]),
               dict(world=[.76,-.296,1.40375],pixel=[494,492]),
               dict(world=[.76,.296,1.40375],pixel=[497,465])])

# Express the original local bed/cage observations in the actual delivered
# site's frame. The camera fits against those world landmarks inside a garden;
# surrounding plots, circulation and neighborhood remain in the export.
for name,offset in [('wise_bed',(-1.3716,.6096,0))]:
    definition=MATCHES[name]
    for key in ('location','target'):
        definition[key]=[a+b for a,b in zip(definition[key],offset)]
    for landmark in definition['landmarks']:
        landmark['world']=[a+b for a,b in zip(landmark['world'],offset)]

# Preserve the measured sign projection in the actual angled frontage. Both
# initial camera and observed world points undergo the same rigid transform.
from plan import plan
entry=plan(229,'park');angle=math.radians(entry['sign_yaw_degrees'])
def place_definition(definition,old,new,angle):
    def placed(point):
        x,y,z=[a-b for a,b in zip(point,old)]
        return [new[0]+x*math.cos(angle)-y*math.sin(angle),new[1]+x*math.sin(angle)+y*math.cos(angle),new[2]+z]
    for key in ('location','target'):definition[key]=placed(definition[key])
    for landmark in definition['landmarks']:landmark['world']=placed(landmark['world'])
place_definition(MATCHES['martin_place'],(3.4,-entry['size'][1]/2+.24,0),(entry['sign_x'],-entry['size'][1]/2+entry['sign_inset'],0),angle)
# The circular hoop has no fixed azimuth. Choose its observed diameter phases
# from the city lot's clear central path, with adjacent corn/herbs in view.
# No bed, plant or cage is moved to stage the photographic comparison.
place_definition(MATCHES['cityhall_mature'],(.76,0,1.40375),(-1.3716,-.1504,1.40375),math.radians(45))
