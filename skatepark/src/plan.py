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
    def add(key,x,y,yaw=0,z=0):out['placements'].append(dict(piece=key,location=[x,y,z],yaw=yaw))
    if kind=='poured':
        out['bowl']=dict(location=[-10.668 if not compact else -8.2296,-1.2192,0],pool=not compact,
                         shape='kidney' if not compact else 'clover')
        h=(4 if compact else 5)*.1524
        edge=1.8288 if compact else 3.048
        sx=10.0584 if compact else 12.192
        out['plaza']=dict(bounds=[2.4384,W/2-1.524,edge,D/2-1.524],height=h,stair_x=sx)
        add('Stairs_4' if compact else 'Stairs_5',sx,edge-(4 if compact else 5)*.3048/2)
        add('PlazaBank_4' if compact else 'PlazaBank_5',4.8768,edge-h/math.tan(math.radians(20))/2)
        # Native-width adjacent pours become a continuous north transition run.
        out['transition_runs']=[dict(name='plaza_entry',indices=[1],shared_deck=False)]
        out['landscape_cuts']=[[-W/2,-1.524,-D/2,-9.144 if compact else -10.668]]
        for row,xs,y,z,key in [
            ('north_west',[-12.192,-7.3152] if compact else [-14.6304,-9.7536,-4.8768],D/2-4.572-(0 if compact else 2.4384),0,'Quarter_4ft'),
            ('north_east',[9.7536] if compact else [9.144,14.0208],D/2-4.572-(0 if compact else 2.4384),h,'Quarter_4ft'),
            ('south',[7.3152,12.192] if compact else [9.7536,14.6304],-D/2+3.048+(0 if compact else 1.524),0,'Bank_3ft')]:
            ids=[]
            for x in xs:
                ids.append(len(out['placements']));add(key,x,y,180 if row=='south' else 0,z)
            out['transition_runs'].append(dict(name=row,indices=ids))
        add('ManualPad',4.8768,-5.4864+(0 if compact else 1.524))
        add('Ledge_18in',10.668,-5.7912+(0 if compact else .9144))
        add('FlatBar',15.24 if compact else 18.288,-3.048)
        add('Ledge_18in',W/2-3.6576,edge+3.048,0,h)
        out['fence_height_m']=1.8288
        out['age']=.38 if not compact else .68
    else:
        for x in (-6.096,0,6.096):add('Prefab_Quarter',x,9.7536)
        for x in (-6.096,0,6.096):add('Prefab_Quarter',x,-9.7536,180)
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
        out['fence_height_m']=1.8288
        out['age']=1.0
    out['layout_mirror']=bool(seed%5 in (0,4) and seed not in SEEDS)
    if out['layout_mirror']:
        if out['bowl']:out['bowl']['location'][0]*=-1
        for item in out['placements']:item['location'][0]*=-1;item['yaw']=-item['yaw']
        if 'plaza' in out:
            x0,x1,y0,y1=out['plaza']['bounds'];out['plaza']['bounds']=[-x1,-x0,y0,y1];out['plaza']['stair_x']*=-1
            out['landscape_cuts']=[[-x1,-x0,y0,y1] for x0,x1,y0,y1 in out['landscape_cuts']]
    out['parameters']=dict(type_override=type,size_override=size,archetype='street+bowl' if kind=='poured' else 'end ramps + two mini lanes',mirror=out['layout_mirror'])
    out['trees']=[[-W/2-4.572,-D/2+6.096,0],[-W/2-4.572,4.572,0],[-W/2-3.048,D/2+4.572,0],
                  [0,D/2+6.096,0],[W/2+4.572,D/2+3.048,0],[W/2+4.572,0,0]]
    out['benches']=[[-W/2-1.524,-D/2+2.4384,0],[W/2+1.524,-D/2+2.4384,0],[0,D/2+1.524,0]]
    out['terrain_yaw']=180 if compact and kind=='poured' else 0
    out['site_yaw']=90 if compact and kind=='poured' else 0
    out['entry']=[W/2+2.4384,1.524,0] if out['site_yaw']==90 else [0,-D/2-2.4384,0]
    if out['site_yaw']==90:
        sw,sd=D,W
        out['site']=[sd+30.48,sw+24.384]
        local_trees=[[-sw/2-4.572,-sd/2+6.096,0],[-sw/2-4.572,4.572,0],[-sw/2-3.048,sd/2+4.572,0],[0,sd/2+6.096,0],[sw/2+4.572,sd/2+3.048,0],[sw/2+4.572,0,0]]
        local_benches=[[-sw/2-1.524,-sd/2+2.4384,0],[sw/2+1.524,-sd/2+2.4384,0],[0,sd/2+1.524,0]]
        out['trees']=[[-y,x,z] for x,y,z in local_trees]
        out['benches']=[[-y,x,z] for x,y,z in local_benches]
    out['coordinate_frames']='Skating placements/bowl/cuts use terrain_yaw; site fixtures and entry above are world positions.'

    out['variation']=rng.random()
    return out
