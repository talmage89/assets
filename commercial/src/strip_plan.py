"""Bounded neighborhood-center grammar. Pure Python, meters, frontage -Y.

Dimensions are authored choices against the authorities in STRIP_REFERENCE.md.
The L has a real elbow/storage volume, rather than interpenetrating shop boxes.
Public driveway stations and all major plan lines use the ground six-inch grid.
"""
import copy
import math
import random

FT = .3048
GRID = FT / 2
PROOF_SEEDS = (201, 202, 203, 204)
TENANTS = {
    'nails': dict(name='VELLUM NAILS', subtitle='NAIL STUDIO', style='channel',
                  ink='#E7C5B8', field='#393746', font='serif'),
    'cleaner': dict(name='HEMWICK', subtitle='DRY CLEANERS', style='box',
                    ink='#F3EEDF', field='#285B58', font='sans'),
    'pizza': dict(name='NOTCH OVEN', subtitle='PIZZA + TAKEOUT', style='channel',
                  ink='#EAC393', field='#60392E', font='serif'),
    'laundry': dict(name='COPPERFOLD', subtitle='SELF SERVICE LAUNDRY', style='box',
                    ink='#F0EEDD', field='#3B5062', font='sans'),
    'phone': dict(name='PINTRACE', subtitle='PHONE REPAIR', style='panel',
                  ink='#E6EBE6', field='#33484C', font='sans'),
    'mattress': dict(name='DROWSEFIELD', subtitle='MATTRESS & BED', style='box',
                     ink='#F3EBDC', field='#5F4B63', font='serif'),
    'tax': dict(name='TALLIED OAK', subtitle='TAX & BOOKKEEPING', style='panel',
                ink='#293E3D', field='#D7D5C6', font='serif'),
    'hair': dict(name='SNIPWELL', subtitle='HAIR STUDIO', style='channel',
                 ink='#E6D9BC', field='#3A3732', font='sans'),
    'vacant': dict(name='FOR LEASE', subtitle='RETAIL SPACE AVAILABLE', style='banner',
                   ink='#F4EEE1', field='#693A32', font='sans'),
}


def transform(point, origin, yaw):
    a = math.radians(yaw)
    x, y, *z = point
    return (origin[0]+math.cos(a)*x-math.sin(a)*y,
            origin[1]+math.sin(a)*x+math.cos(a)*y, *z)


def required_accessible(n):
    return next(v for limit, v in ((25,1),(50,2),(75,3),(100,4),(150,5),(200,6)) if n <= limit)


def generate(seed=201, overrides=None):
    rng = random.Random(seed)
    variants = (
        dict(lot_ft=(336,244), bays=10, bay_ft=24, depth_ft=70, style='flat',
             wall='split_cmu', color=(.31,.285,.245), towers='ends', shape='row', rear_ft=32, shift_ft=0, rows=4, drive_ft=(18,18), endcaps=('wrap','sign')),
        dict(lot_ft=(390,210), bays=10, bay_ft=22, depth_ft=64, style='mansard',
             wall='brick', color=(.26,.105,.057), towers='center', shape='row', rear_ft=28, shift_ft=24, rows=3, drive_ft=(22,18), endcaps=('sign','wrap')),
        dict(lot_ft=(348,260), bays=11, bay_ft=22, depth_ft=76, style='arcade',
             wall='eifs', color=(.43,.38,.29), towers='ends', shape='row', rear_ft=30, shift_ft=-8, rows=4, drive_ft=(18,24), endcaps=('wrap','wrap')),
        dict(lot_ft=(396,244), bays=7, bay_ft=24, depth_ft=64, style='flat',
             wall='smooth_cmu', color=(.32,.34,.31), towers='elbow', shape='L', rear_ft=32, shift_ft=0, rows=4, drive_ft=(18,18), endcaps=('sign','wrap')),
    )
    d = copy.deepcopy(variants[(seed-201)%4])
    if seed not in PROOF_SEEDS:
        d['color'] = tuple(c*rng.uniform(.95,1.05) for c in d['color'])
        d['depth_ft'] += rng.choice((-2,0,2))
        d['lot_ft'] = (d['lot_ft'][0], min(260,d['lot_ft'][1]+d['depth_ft']-variants[(seed-201)%4]['depth_ft']))
    if overrides:
        if set(overrides)-set(d): raise ValueError('Unknown strip-center controls')
        d.update(copy.deepcopy(overrides))
    W,D = (v*FT for v in d['lot_ft'])
    bw,dep = d['bay_ft']*FT,d['depth_ft']*FT
    rear = D/2-d['rear_ft']*FT
    front = rear-dep
    walk = 10*FT
    rowwidth = bw*d['bays']
    totalwidth = rowwidth+(dep if d['shape']=='L' else 0)
    left = -totalwidth/2+d['shift_ft']*FT
    modules=[]
    for i in range(d['bays']):
        modules.append(dict(id=f'Bay_{i+1:02d}', origin=(left+(i+.5)*bw,front), yaw=0,
                            width=bw,depth=dep,wing=False,partition=True))
    elbow=None
    if d['shape']=='L':
        inner=left+rowwidth
        elbow=dict(id='Elbow',bounds=(inner,inner+dep,front,rear),
                   role='Rear storage/service volume of the combined return tenant')
        for i in range(2):
            modules.append(dict(id=f'Bay_{len(modules)+1:02d}',origin=(inner,front-(i+.5)*bw),yaw=-90,
                                width=bw,depth=dep,wing=True,partition=i==1,corner_walk_clip=i==0))
    # Nine original occupants including vacancy. One end tenant can lease two
    # structural bays; each structural bay retains its own doors and roof share.
    order=['nails','cleaner','pizza','phone','vacant','tax','hair','mattress','laundry']
    if seed!=201:
        fixed=order[:];rng.shuffle(fixed);order=fixed
    tenants=[]
    for i,m in enumerate(modules):
        key=order[min(i,len(order)-1)]
        if i>=9:key=order[-1]
        m.update(tenant=key,address=f'{110+i*2}',lease_group=key)
        tenants.append(key)
    # Full-width two-way side drives connect the street to the rear loop.
    drive_x=[-W/2+d['drive_ft'][0]*FT,W/2-d['drive_ft'][1]*FT]
    drives=[dict(edge='south',center=(x,-D/2),width=24*FT) for x in drive_x]
    lane_centers=(front-walk-18*FT-12*FT,
                  front-walk-18*FT-24*FT-36*FT-4*FT-12*FT)
    # Facing north/south pairs around both 24-foot aisles. The 4-foot median
    # between the center rows is planted at its ends, not striped as parking.
    ys=[(front-walk-18*FT,front-walk,1),
        (front-walk-42*FT-18*FT,front-walk-42*FT,-1),
        (front-walk-82*FT,front-walk-64*FT,1),
        (front-walk-124*FT,front-walk-106*FT,-1)]
    rows=[];islands=[];stalls=[]
    x0,x1=drive_x[0]+15*FT,drive_x[1]-15*FT
    for j,(y0,y1,facing) in enumerate(ys[:d['rows']]):
        right=x1
        if elbow and j<2:right=min(right,elbow['bounds'][0]-walk-32*FT)
        # 9-foot islands bookend each row. The full front row is step-free:
        # a parking-level protected route behind stops meets each ramp opening.
        a=x0+9*FT;b=right-9*FT
        count=math.floor((b-a)/(9*FT))
        b=a+count*9*FT
        rows.append(dict(index=j,x0=a,x1=b,y0=y0,y1=y1,facing=facing,count=count))
        for s,(lo,hi) in enumerate(((x0,a),(b,b+9*FT))):
            islands.append(dict(bounds=(lo,hi,y0,y1),row=j,end=s))
        middle=count//2 + (1 if (seed-201)%4==1 and j==1 else -2 if (seed-201)%4==2 and j%2 else 0)
        islands.append(dict(bounds=(a+middle*9*FT,a+(middle+1)*9*FT,y0,y1),row=j,end='intermediate'))
        for k in range(count):
            if k==middle:continue
            stalls.append(dict(row=j,index=k,x0=a+k*9*FT,x1=a+(k+1)*9*FT,
                               y0=y0,y1=y1,facing=facing,accessible=False))
    # Dispersed wider bays + an exclusive 5-foot aisle replace blocks of three
    # standard spaces. Reserve four from the outset; exact count checked below.
    frontrow=rows[0];candidates=[2,frontrow['count']//2+2,frontrow['count']-4]
    access=[];reserved=[]
    columns=[(left+i*bw,.28) for i in range(d['bays']+1)]
    tower_x=([left+1.8,left+totalwidth-1.8] if d['towers']=='ends' else [left+totalwidth/2] if d['towers']=='center' else [elbow['bounds'][0]-5.0])
    columns += [(x+s*1.6,.34) for x in tower_x for s in (-1,1)]
    # Find whole 27-foot conversions near each desired group. Access aisles
    # must actually reach the covered walk and clear its piers/column plinths.
    for group_id,preferred in enumerate(candidates):
        choices=[]
        for k in range(frontrow['count']-2):
            aa=frontrow['x0']+k*9*FT;ax0=aa+11*FT;ax1=aa+16*FT
            if ax0<left+.36 or ax1>left+rowwidth-.36:continue
            if any(ax0<x+radius+.05 and ax1>x-radius-.05 for x,radius in columns):continue
            if any(k<t+3 and k+3>t for t in reserved):continue
            if any(isl['row']==0 and isl['end']=='intermediate' and aa<isl['bounds'][1] and aa+27*FT>isl['bounds'][0] for isl in islands):continue
            choices.append(k)
        assert choices,'No unobstructed dispersed accessible group'
        k=min(choices,key=lambda k:(abs(k-preferred),k));reserved.append(k)
        a=frontrow['x0']+k*9*FT
        removed=[s for s in stalls if s['row']==0 and a-.01<s['x0']<a+27*FT-.01]
        if any(s.get('accessible') for s in removed):continue
        stalls=[s for s in stalls if s not in removed]
        # Two 11-foot van-sized stalls share a five-foot aisle (27ft total).
        for side_num,(lo,hi) in enumerate(((a,a+11*FT),(a+16*FT,a+27*FT))):
            stalls.append(dict(row=0,index=frontrow['count']+group_id*2+side_num,x0=lo,x1=hi,y0=frontrow['y0'],y1=frontrow['y1'],facing=1,accessible=True))
        access.append(dict(x0=a+11*FT,x1=a+16*FT,y0=frontrow['y0'],y1=frontrow['y1'],ramp_run=6*FT))
    cross=None
    if elbow:
        cross=dict(center_x=elbow['bounds'][0]-walk-18*FT,width=24*FT,turn_flare=6*FT,
                   y0=lane_centers[1],y1=lane_centers[0])
        # The short leg must not turn the front aisle into a dead end. A cross
        # aisle continues through the next parking row to the street-side
        # aisle, with an extra six-foot flare on the eastern turn.
        lo=cross['center_x']-cross['width']/2;hi=cross['center_x']+cross['width']/2+cross['turn_flare']
        stalls=[s for s in stalls if not (s['row']==2 and s['x0']<hi and s['x1']>lo)]
    if d['shape']=='L':
        drives[1]=dict(edge='east',center=(W/2,lane_centers[1]),width=24*FT)
    area=(rowwidth*dep+(dep*dep+2*bw*dep if elbow else 0))
    p=dict(seed=seed,stage='strip form checkpoint: diagnostic materials, no look-dev acceptance',
           lot=(W,D),building=dict(width=totalwidth,depth=dep,front=front,rear=rear,
             floor=.1524,roof=4.2672,parapet=5.1816,wall=d['wall'],wall_color=d['color'],area_m2=area,left=left),
           shape=d['shape'],style=d['style'],towers=d['towers'],modules=modules,elbow=elbow,
           walk=walk,driveways=drives,side_drive_centers=drive_x,
           rear_drive=(rear+2*FT,rear+26*FT),rows=rows,stalls=stalls,islands=islands,
           access=access,aisle_centers=lane_centers,cross_aisle=cross,stall_count=len(stalls),
           center_name=('ALDER RILL SHOPS','CROSSBEND COURT','LOWBANK COMMONS','WILLOW SPAN SHOPS')[(seed-201)%4],
           sign_center=((-W/2+38*FT,-D/2+6*FT), (W/2-43*FT,-D/2+7*FT), (-W/2+40*FT,-D/2+10*FT), (W/2-7*FT,-D/2+8*FT))[(seed-201)%4],
           endcaps=d['endcaps'], site_archetype=('centered deep lot','wide shallow offset row','west-biased row and staggered islands','two-street corner L')[(seed-201)%4],
           parking_ratio=len(stalls)/(area/FT**2)*1000)
    validate(p)
    return p


def validate(p):
    W,D=p['lot'];b=p['building']
    assert 250*FT<=W<=400*FT and 180*FT<=D<=260*FT, 'Lot bounds'
    assert 10000<=b['area_m2']/FT**2<=30000, 'Building area'
    assert p['style'] in ('flat','arcade','mansard'), 'Front style'
    assert p['shape'] in ('row','L'), 'Shape'
    assert b['wall'] in ('brick','split_cmu','smooth_cmu','eifs'), 'Wall finish'
    assert p['rows'][-1]['y0']>-D/2+3*FT, 'No front landscape setback'
    assert b['left']>-W/2+30*FT and b['left']+b['width']<W/2-30*FT, 'Side circulation squeezed'
    assert p['parking_ratio']>=3.0, 'Insufficient parking for reference shopping-center baseline'
    assert sum(s['accessible'] for s in p['stalls'])>=required_accessible(p['stall_count']), 'Accessible count'
    assert 'vacant' in [m['tenant'] for m in p['modules']], 'No vacant bay'
    for m in p['modules']:
        assert 20*FT<=m['width']<=30*FT and 60*FT<=m['depth']<=80*FT,'Bay dimensions'
    for j,row in enumerate(p['rows']):
        assert row['count']>=10, 'Row too short'
        assert abs(row['y1']-row['y0']-18*FT)<1e-6
    return p
