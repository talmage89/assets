"""Seeded, front-relative cafe plans in meters. No Blender dependency.

Sites use distinct topologies rather than shuffling a common seating plan.
The front-frame is at the building's front-center; the delivered shop origin
is its host footprint center. Occupancy includes a pulled-out chair allowance.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

FT = .3048
PROOFS = ((117, 'downtown'), (228, 'strip'), (339, 'pad'))
IDENTITIES = {
    'downtown': [('FOLIO', 'COFFEE & READING ROOM', 'forest'), ('BRACKET', 'NEIGHBORHOOD COFFEE', 'ink')],
    'strip': [('MORROW', 'COFFEE • BAKERY', 'wine'), ('DAYBREAK', 'COFFEE & COMPANY', 'ochre')],
    'pad': [('SWITCHYARD', 'COFFEE HOUSE', 'teal'), ('WREN STOP', 'COFFEE • WALK UP', 'rust')],
}


def generate(seed, kind, overrides=None):
    rng = random.Random(seed)
    name, subtitle, palette = IDENTITIES[kind][rng.randrange(2)]
    p = dict(seed=seed, kind=kind, name=name, subtitle=subtitle, palette=palette,
             stage='look-dev checkpoint; baked shared PBR and placed causal age',
             year={'downtown':2011,'strip':2004,'pad':1997}[kind],
             age={'downtown':'old shell, fresh fit-out','strip':'worn door and patio','pad':'faded and patched'}[kind],
             width={'downtown':30*FT,'strip':42*FT,'pad':36*FT}[kind],
             depth={'downtown':90*FT,'strip':64*FT,'pad':30*FT}[kind],
             grade=0 if kind=='downtown' else .1524,
             room_depth={'downtown':6.7,'strip':7.5,'pad':7.8}[kind],
             counter_y={'downtown':3.5,'strip':4.35,'pad':4.55}[kind],
             counter_x={'downtown':1.45,'strip':-2.6,'pad':1.8}[kind],
             counter_yaw={'downtown':0,'strip':90,'pad':0}[kind],
             counter_length={'downtown':3.65,'strip':4.25,'pad':3.9}[kind],
             tables=[], routes=[], rail=[], umbrellas=[])
    if kind == 'downtown':
        # 20 ft walk: 3 ft car-door buffer, curbside furniture, 6 ft public path.
        p.update(walk=20*FT, entry=(.297,1.11), seating_zone=[-4.36,4.36,-5.12,-2.20],
                 route_rule='Seattle 4-2011 downtown 6 ft pedestrian zone; 3 ft curb buffer',
                 barrier_height=.9144)
        xy=[(-2.65,-3.66),(0.,-3.66),(3.02,-3.66)]
        p['routes']=[dict(name='Public through walk',rect=[-4.57,4.57,-2.13,-.26],required=6*FT),
                     dict(name='Curb car-door buffer',rect=[-4.57,4.57,-6.096,-5.1816],required=3*FT),
                     dict(name='Cafe west entry',rect=[-4.36,-3.14,-4.38,-2.86],required=1.2192),
                     dict(name='Cafe public connection',rect=[-5.40,-4.46,-4.38,-2.13],required=.9144)]
        p['rail']=[(-4.36,-5.12,4.36,-5.12),(-4.36,-2.20,4.36,-2.20),(4.36,-5.12,4.36,-2.20)]
        p['umbrellas']=[dict(x=0,y=-3.66,state='open')]
    elif kind == 'strip':
        p.update(walk=6.1, entry=(-4.672,-.15), seating_zone=[-2.65,6.05,-5.7,-2.72],
                 route_rule='6 ft through walk; 4 ft patio entry; occupied envelopes',barrier_height=1.016)
        xy=[(-.82,-4.22),(1.72,-4.22),(4.68,-4.22)]
        p['routes']=[dict(name='Covered public walk',rect=[-6.40,6.40,-2.48,-.60],required=6*FT),
                     dict(name='Patio west entry',rect=[-2.60,-1.38,-4.85,-3.46],required=1.2192),
                     dict(name='Patio public connection',rect=[-3.70,-2.70,-4.85,-2.48],required=.9144)]
        p['rail']=[(-2.65,-5.7,6.05,-5.7),(-2.65,-2.72,6.05,-2.72),(6.05,-5.7,6.05,-2.72)]
        p['umbrellas']=[dict(x=1.72,y=-4.22,state='open'),dict(x=4.68,y=-4.22,state='closed')]
    else:
        p.update(walk=6.4,entry=(-1.35,-.15),seating_zone=[6.9,10.30,.0,8.35],
                 route_rule='private patio; 36 in accessible route, 60 in turning pad',barrier_height=.9144)
        xy=[(8.52,1.35),(8.52,4.28),(8.52,7.15),(-3.78,-3.00),(.65,-3.00)]
        p['routes']=[dict(name='Public through walk',rect=[-5.49,10.5,-6.40,-4.50],required=6*FT),
                     dict(name='Front door approach',rect=[-2.15,-.55,-4.5,-.18],required=1.524),
                     dict(name='Walk-up side route',rect=[6.00,6.92,.0,7.9],required=.9144),
                     dict(name='Side public connection',rect=[6.00,6.92,-4.50,.0],required=.9144)]
        p['rail']=[(10.30,.0,10.30,8.35),(6.90,8.35,10.30,8.35),(-5.15,-4.43,-2.30,-4.43),(-.35,-4.43,1.42,-4.43)]
        p['umbrellas']=[dict(x=8.52,y=4.28,state='open'),dict(x=-3.78,y=-3.00,state='open')]
    arrangement=random.Random(seed+844)
    count=2 if arrangement.random()<.25 else 3
    if kind=='pad':xy=xy[:count]+xy[3:]
    else:xy=xy[:count]
    if count==2 and kind in ('downtown','strip'):
        old=p['seating_zone'][1];new=1.25 if kind=='downtown' else 3.15;p['seating_zone'][1]=new
        p['rail']=[tuple(new if k in (0,2) and abs(v-old)<.001 else v for k,v in enumerate(segment)) for segment in p['rail']]
    # Some seeds have two outdoor pairs rather than three; the side-court
    # seed has two or three in its court plus its two front tables.
    p['umbrellas']=[u for u in p['umbrellas'] if any(abs(u['x']-x)<.05 and abs(u['y']-y)<.05 for x,y in xy)]
    p['counter_y']+=arrangement.choice((-.10,0,.10));p['counter_x']+=arrangement.choice((-.08,0,.08))
    setting_order=rng.sample(['cup','paper','laptop'],3)
    for i,(x,y) in enumerate(xy):
        # Accessible table on the first bay; approach is on its unoccupied west
        # side downtown/strip, south side in the pad's side court.
        p['tables'].append(dict(id=f'Table_{i+1:02}',x=x+rng.uniform(-.025,.025),
            y=y,accessible=i==0,occupied_radius=.79,setting=setting_order[i%3],
            rotation=0 if kind!='pad' or i>=3 else 90,placement_seed=rng.randrange(2**24)))
    p.update(overrides or {})
    p['plan_sha256']=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
    return p


def main():
    a=argparse.ArgumentParser();a.add_argument('--seed',type=int,default=117);a.add_argument('--kind',choices=IDENTITIES,default='downtown');a.add_argument('--out',type=Path,required=True)
    a=a.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(generate(a.seed,a.kind),indent=2)+'\n')


if __name__=='__main__':main()
