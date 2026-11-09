"""Pure-Python church grammar; meters, +Z up, -Y entrance."""
import math
import random

STYLES=('gothic','romanesque','aframe','chapel')


def church(seed=101,style=None,bays=None,width=None,pitch=None,tower=None,top=None,wings=None):
    rng=random.Random(seed)
    style=style or ('gothic' if seed==101 else 'aframe' if seed==202 else rng.choice(STYLES))
    if style not in STYLES:raise ValueError(style)
    modern=style=='aframe';frame=style=='chapel'
    bays=bays or (7 if modern else 6 if seed==101 else rng.randint(3,9))
    width=width or (17.6784 if modern else 7.3152 if frame else 13.1064)
    pitch=pitch or (57 if modern else 45 if frame else 48)
    if not 3<=bays<=18 or not 5<=width<=42 or not 25<=pitch<=65:raise ValueError('Unsupported church envelope')
    tower=tower or ('freestanding' if modern else 'none' if frame else 'corner')
    top=top or ('cross' if modern else 'spire')
    if tower not in ('corner','center','freestanding','none'):raise ValueError(tower)
    if top not in ('spire','belfry','cross'):raise ValueError(top)
    bay=4.2672;length=bay*bays;wall=.3048 if modern or frame else .4572
    eave=2.7432 if modern else 4.8768 if frame else 8.2296
    floor=.1524 if modern else .6096
    wings=list(wings if wings is not None else ['education','hall'] if modern else [] if frame else ['hall'])
    p=dict(seed=seed,style=style,bays=bays,width=width,length=length,bay=bay,wall=wall,
           pitch=pitch,eave=eave,ridge=eave+width/2*math.tan(math.radians(pitch)),
           floor=floor,tower=tower,top=top,wings=wings,
           date=1963 if modern else 1908 if seed==101 else 1916,
           name='CEDAR & BELL CHURCH' if modern else 'GRACE CORNER CHURCH',
           ramp=dict(rise=.6096,run=7.9248,clear=1.524,landing=1.8288),
           wear=.65,occupancy=.22 if modern else .88)
    p['tower_xy']=(-width/2-1.8,-length/2+1.8) if tower=='corner' else (0,-length/2-2.6) if tower=='center' else (-width/2-5,-length/2+2)
    p['parcel']=(-27,31,-26,49) if not modern else (-30,61,-46,42)
    p['stalls']=[];p['paths']=[]
    return p


def range_plans():
    return [church(301,'chapel',3,tower='none',wings=[]),
            church(302,'romanesque',4,width=10.668,pitch=38,top='belfry',wings=[]),
            church(101),church(202)]
