"""Original bounded station grammar, meters, independent of Blender and photos.

Local station frontage is -Y. Corner yaw rotates the complete lot and its two
street sockets. All permanent building/site anchors use the ground 6-inch grid.
The reusable BuildingSpec is intentionally independent of the fuel equipment.
"""
from dataclasses import dataclass, asdict
import copy, json, math, random
FT=.3048
GRID=FT/2
PROOF_SEEDS=(101,102,103,104)

BRANDS={
 'rillway':dict(name='RILLWAY',primary=(.115,.031,.081),accent=(.59,.255,.105),light=(.72,.68,.58),mark='three_piers'),
 'latchline':dict(name='LATCHLINE',primary=(.025,.038,.047),accent=(.27,.31,.57),light=(.68,.71,.70),mark='offset_brackets'),
}

@dataclass
class BuildingSpec:
 width:float=60*FT
 depth:float=50*FT
 front:float=18*FT
 center_x:float=0
 floor:float=.1524
 roof:float=3.9624
 parapet:float=4.8768
 entry_x:float=0
 wall:str='split_cmu'
 wall_color:tuple=(.34,.32,.28)
 cooler:bool=True


def rotate(point,yaw):
 c,s=math.cos(math.radians(yaw)),math.sin(math.radians(yaw))
 return (c*point[0]-s*point[1],s*point[0]+c*point[1],*point[2:])


def generate(seed=101,overrides=None):
 rng=random.Random(seed);k=(seed-101)%4
 # Deliberate topological variants; random dimensions stay within each safe envelope.
 specs=[dict(lot=(150,150),store=(60,50,18),count=3,canopy_y=-35,angle=0,yaw=0,brand='rillway',wall='split_cmu',sign='monument'),
        dict(lot=(140,150),store=(56,48,20),count=2,canopy_y=-36,angle=90,yaw=90,brand='latchline',wall='brick',sign='pylon'),
        dict(lot=(160,160),store=(64,48,22),count=4,canopy_y=-39,angle=0,yaw=-90,brand='latchline',wall='smooth_cmu',sign='monument'),
        dict(lot=(160,160),store=(66,50,25),count=3,canopy_y=-40,angle=30,yaw=180,brand='rillway',wall='eifs',sign='pylon')]
 d=copy.deepcopy(specs[k]);d['seed']=seed
 if seed not in PROOF_SEEDS:
  width,depth,front=d['store'];width=max(56,width+rng.choice((-2,0,2)));depth=rng.choice((46,48,50))
  front=min(front,d['lot'][1]/2-depth-4)
  d['store']=(width,depth,front);d['brand']=rng.choice(tuple(BRANDS))
  d['yaw']=rng.choice((-90,0,90,180));d['sign']=rng.choice(('monument','pylon'))
 if overrides:
  if set(overrides)-{'brand','wall','sign','yaw','cooler','store','count','angle','canopy_y','lot'}:raise ValueError('Unsupported station control')
  d.update(copy.deepcopy(overrides))
 b=BuildingSpec(width=d['store'][0]*FT,depth=d['store'][1]*FT,front=d['store'][2]*FT,
                center_x=(2 if k==2 else 0)*FT,wall=d['wall'],cooler=d.get('cooler',k%2==0),
                wall_color=[(.34,.32,.28),(.24,.10,.055),(.34,.35,.32),(.45,.39,.29)][k])
 count=d['count'];pitch=25*FT;angle=d['angle']
 # Wider four-island canopy, with 12 ft end overhangs. Shorter variants retain that construction.
 can=dict(count=count,pitch=pitch,center=(0,d['canopy_y']*FT),angle=angle,
          width=(count-1)*pitch+24*FT,depth=36*FT,clear=14.5*FT,fascia=3.25*FT,
          column=.3556,island=(4*FT,18*FT,.1524))
 islands=[]
 for i in range(count):
  local=((i-(count-1)/2)*pitch,0)
  x,y=rotate(local,angle);islands.append(dict(center=(x,y+can['center'][1]),angle=angle,index=i+1))
 W,D=(v*FT for v in d['lot']);walk=7*FT;parking_depth=18*FT
 # Entrances remain on the two local street edges; the front opening varies with canopy.
 front_drive=(((count-1)/2*pitch+12*FT) if angle==0 else W/2-24*FT,-D/2)
 side_drive=(-W/2,(-12 if angle==0 else -13)*FT)
 result=dict(seed=seed,stage='form checkpoint: quick materials; no bake',lot=(W,D),yaw=d['yaw'],brand=d['brand'],
    building=asdict(b),canopy=can,islands=islands,sign=d['sign'],
    sign_center=(-W/2+14*FT,-D/2+14*FT),driveways=[dict(edge='south',center=front_drive,width=24*FT),dict(edge='west',center=side_drive,width=24*FT)],
    walk=walk,parking_depth=parking_depth,parking_front=b.front-walk-parking_depth,
    stalls=5 if b.width>19 else 4)
 validate(result);return result


def validate(p):
 b=p['building'];c=p['canopy'];W,D=p['lot']
 assert p['brand'] in BRANDS,'Unknown brand'
 assert b['wall'] in ('split_cmu','smooth_cmu','brick','eifs'),'Unknown wall'
 assert p['sign'] in ('pylon','monument'),'Unknown sign'
 assert p['yaw'] in (-90,0,90,180),'Corner yaw must be a quarter turn'
 assert 120*FT<=W<=160*FT and 120*FT<=D<=160*FT,'Lot bounds'
 assert 2500*FT**2<=b['width']*b['depth']<=4000*FT**2,'Store area'
 assert b['front']+b['depth']<D/2-FT,'Rear setback'
 assert 2<=c['count']<=4,'Island count'
 assert c['pitch']-c['island'][0]>=6.0,'Fueling lane too narrow'
 assert 14*FT<=c['clear']<=16*FT,'Canopy clearance'
 assert 3*FT<=c['fascia']<=4*FT,'Fascia bounds'
 assert c['angle'] in (0,30,90),'Supported canopy orientation'
 assert b['roof']<b['parapet'] and b['roof']>3.4,'Roof/parapet'
 # Actual island corner envelopes: reject encroachment on stalls or property edges.
 for island in p['islands']:
  for x,y in [(-c['island'][0]/2,-c['island'][1]/2),(c['island'][0]/2,c['island'][1]/2)]:
   u,v=rotate((x,y),c['angle']);u+=island['center'][0];v+=island['center'][1]
   assert abs(u)<W/2-2 and -D/2+2<v<p['parking_front']-2.4,'Island circulation envelope'
 for drive in p['driveways']:
  u=drive['center'][0] if drive['edge']=='south' else drive['center'][1]
  limit=W/2 if drive['edge']=='south' else D/2
  assert abs(u)+drive['width']/2+1.524<limit,'Driveway wing outside lot'
 return p


def load(seed,path=None):return generate(seed,json.loads(open(path).read()) if path else None)

if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--seed',type=int,default=101);a.add_argument('--out');a=a.parse_args()
 p=generate(a.seed);s=json.dumps(p,indent=2);print(s) if not a.out else open(a.out,'w').write(s+'\n')
