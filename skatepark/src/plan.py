"""Seeded layout grammar, independent of Blender. Construction grid 6 inches.

Bounded named archetypes reserve separate transition/street lines, spectator
space and a pedestrian entry. Seed variations mirror banks of obstacles and
vary tree orientation; decade changes construction, not just paint.
"""
import random, math
GRID=.1524
SEEDS=(101,202,303)

def plan(seed,type=None,size=None):
    rng=random.Random(seed);kind=type or ('prefab' if seed%3==0 else 'poured')
    if kind not in ('poured','prefab'):raise ValueError(kind)
    compact=(size=='compact') if size else seed%2==0
    W,D=((36.576,27.432) if compact else (45.72,33.528)) if kind=='poured' else (36.576,27.432)
    out=dict(seed=seed,type=kind,year=1999 if kind=='prefab' else 2004 if compact else 2011,
             town='MILL CREEK' if kind=='prefab' else 'CEDAR JUNCTION' if compact else 'ALDER GLEN',
             skating=[W,D],site=[W+24.384,D+30.48],grid_m=GRID,
             shade=kind=='poured' and not compact,bleachers=kind=='prefab',pool_coping=not compact,
             bowl=None,placements=[])
    def add(key,x,y,yaw=0):out['placements'].append(dict(piece=key,location=[x,y,0],yaw=yaw))
    if kind=='poured':
        out['bowl']=dict(location=[-10.668 if not compact else -7.62,0,0],pool=not compact)
        # End decks join banks/quarters, a long clear flat in the street lane.
        x=10.668 if not compact else 9.144
        add('Quarter_5ft' if not compact else 'Quarter_4ft',x,D/2-4.572,0)
        add('Quarter_4ft',x+(-4.8768 if not compact else -4.8768),D/2-4.572,0)
        add('Bank_Rail',x,-D/2+3.048,180)
        add('Stairs_4' if compact else 'Stairs_5',x+2.4384,0)
        add('ManualPad',x-5.4864,-4.8768)
        add('Ledge_18in',x-1.2192,-6.7056)
        add('FlatBar',x-3.048,5.4864)
        if not compact:
            add('Pyramid',-1.2192,-10.668,90)
            add('Spine_5ft',-3.048,10.668,90)
        else:add('Ledge_18in',-9.144,9.144,90)
    else:
        for x in (-7.3152,0,7.3152):add('Prefab_Quarter',x,10.668)
        for x in (-7.3152,0,7.3152):add('Prefab_Quarter',x,-10.668,180)
        # Two separate beginner mini-ramp lanes: paired opposed quarters,
        # eight meters of clear native pad between their tangent toes.
        for x in (-14.6304,14.6304):
            add('Prefab_Quarter',x,5.0)
            add('Prefab_Quarter',x,-5.0,180)
        add('Prefab_Funbox',-6.096,0,90)
        add('Prefab_Launch',2.4384,1.8288,90)
        add('Prefab_Launch',8.5344,1.8288,270)
        add('Prefab_GrindBox',2.4384,-2.7432)
        add('Prefab_GrindBox',8.5344,-4.2672,90)
        add('FlatBar',3.6576,4.8768,90)
        add('FlatBar',0,-5.4864,90)
    out['layout_mirror']=bool(seed%5 in (0,4) and seed not in SEEDS)
    if out['layout_mirror']:
        if out['bowl']:out['bowl']['location'][0]*=-1
        for item in out['placements']:item['location'][0]*=-1;item['yaw']=-item['yaw']
    out['parameters']=dict(type_override=type,size_override=size,archetype='street+bowl' if kind=='poured' else 'end ramps + two mini lanes',mirror=out['layout_mirror'])
    out['trees']=[[-W/2-4.572,-D/2+6.096,0],[-W/2-4.572,4.572,0],[-W/2-3.048,D/2+4.572,0],
                  [0,D/2+6.096,0],[W/2+4.572,D/2+3.048,0],[W/2+4.572,0,0]]
    out['benches']=[[-W/2-1.524,-D/2+2.4384,0],[W/2+1.524,-D/2+2.4384,0],[0,D/2+1.524,0]]
    out['entry']=[0,-D/2-2.4384,0]
    out['variation']=rng.random()
    return out
