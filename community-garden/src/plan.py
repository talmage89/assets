"""Seeded, buildable garden plans. No Blender dependency. Dimensions in metres."""
import random

FT=.3048
SEEDS=(117,229,341)
STATES=('tidy','lush','weedy','fallow','new')
CROPS=('tomato','pepper','squash','bean','corn','lettuce','kale','herb')


def plan(seed,archetype=None):
    rng=random.Random(seed)
    kind=archetype or ('city' if seed%3==0 else 'park' if seed%3==1 else 'accessible')
    if kind not in ('city','park','accessible'):raise ValueError(kind)
    W,D={'city':(18.288,21.336),'park':(27.432,24.384),'accessible':(24.384,21.336)}[kind]
    p=dict(seed=seed,archetype=kind,size=[W,D],year={'city':1998,'park':2004,'accessible':2012}[kind],
           name={'city':'BELLWETHER GROWERS','park':'MEADOW COMMONS','accessible':'ALDER NEIGHBORS'}[kind],
           plots=[],paths=[],entry=[0,-D/2],main_width=1.8288 if kind=='accessible' else 1.524,
           service=[W/2-3.048,D/2-3.048],secondary_width=1.2192 if kind=='accessible' else .9144)
    def plot(x,y,w,d,edge,crop=None,state=None):
        i=len(p['plots']);state=state or STATES[(i+seed)%len(STATES)]
        p['plots'].append(dict(id=i+1,center=[x,y],width=w,depth=d,edge=edge,
                              crop=crop or CROPS[(i+seed//3)%len(CROPS)],state=state,
                              stage=.28 if state=='new' else .82 if state=='tidy' else 1.0,
                              seed=rng.randrange(100000),board_height=.28575 if i%2 else .23495))
    if kind=='city':
        # Narrow city parcel, central north/south accessible spine; 4 x 8 beds.
        for row,y in enumerate((-6.096,-2.7432,.6096,3.9624)):
            for x in (-5.334,-2.7432,2.7432,5.334):plot(x,y,1.2192,2.4384,'block' if row==2 and x>0 else 'lumber')
        p['paths']=[dict(center=[0,-1.524],size=[p['main_width'],D-3.048],surface='Gravel')]
        p['service']=[5.334,7.62];p['compost']=[-5.8,8.8];p['water']=[1.32,6.3];p['bench']=[-3.6,7.0]
    elif kind=='park':
        # Larger tenant plots (10 x 20 ft) contain rows separated by walk strips.
        for y in (-5.334,2.286):
            for x in (-8.5344,-3.6576,3.6576,8.5344):plot(x,y,3.048,6.096,'board' if x<0 else 'none')
        # Two smaller donated raised beds turn across the shared front apron.
        plot(-6.1,-10.15,2.4384,1.2192,'lumber','herb','tidy')
        plot(6.1,-10.15,2.4384,1.2192,'block','lettuce','new')
        p['paths']=[dict(center=[0,-1.524],size=[1.524,D-3.048],surface='Gravel'),
                    dict(center=[0,-1.524],size=[W-3.048,1.524],surface='Lawn')]
        p['service']=[9.5,9.2];p['compost']=[3.5,10.3];p['water']=[-1.3,8.6];p['bench']=[-8.5,9.0]
    else:
        # East/west cross aisle and front accessible court; main route reaches services.
        for y in (-2.7432,1.2192,5.1816):
            for x in (-8.5344,-4.2672,4.2672,8.5344):plot(x,y,2.4384,1.2192,'lumber' if x<0 else 'block')
        plot(-4.2672,-7.01,2.4384,.9144,'accessible','herb','tidy')
        plot(4.2672,-7.01,2.4384,.9144,'accessible','lettuce','lush')
        p['paths']=[dict(center=[0,0],size=[1.8288,D],surface='Gravel'),
                    dict(center=[0,-5.1816],size=[W-3.048,1.8288],surface='Gravel'),
                    dict(center=[0,6.60],size=[W-3.048,1.524],surface='Gravel'),
                    dict(center=[-1.8,7.9],size=[2.4,1.524],surface='Gravel'),
                    dict(center=[0,-8.5344],size=[W-3.048,1.8288],surface='Gravel')]
        p['service']=[9.2,8.9];p['compost']=[-8.3,8.9];p['water']=[-1.4,8.0];p['bench']=[3.8,8.0]
    p['gate_width']=1.8288 if kind=='accessible' else 1.524
    p['parameters']=dict(archetype=kind,seed=seed,season='midsummer',plant_seed=seed*7919,
                         plot_state_rule='five interleaved care states with seeded crop morphology')
    return p
