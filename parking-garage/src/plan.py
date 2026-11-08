"""Original bounded garage grammar. All coordinates are Blender meters.

No Blender dependency: a game may use this manifest without modeling software.
The precast variant has a sloped 60ft parking bay and a flat 60ft bay; the PT
variant replaces the sloped parking bay with a narrow external speed ramp.
"""
import math
import random

FT = .3048
TEE = 12*FT
SPAN = 60*FT
STALL = 8.5*FT
DEPTH = 18*FT
AISLE = 24*FT
FLOOR = 11*FT
SEEDS = (101, 202)


def ramp_fraction(x, p):
    a, b = p['ramp_limits']
    if x <= a: return 0.
    if x >= b: return 1.
    if p['system'] == 'precast': return (x-a)/(b-a)
    t = p['transition']
    run = b-a
    # Half-gradient transitions: continuous elevation, deliberate grade breaks.
    distance = x-a
    effective = distance*.5 if distance < t else distance-t*.5 if distance < run-t else run-t-(run-distance)*.5
    return effective/(run-t)


def deck_z(p, level, x, y, ramp=False):
    # One percent crossfall toward paired edge drains. Accessible ground bays
    # receive the same 1% plane, safely below the 1:48 maximum.
    center = p['ramp_y'] if ramp else p['flat_y']
    width = p['ramp_width'] if ramp else SPAN
    return level*FLOOR + (FLOOR*ramp_fraction(x, p) if ramp else 0) + .01*(width/2-abs(y-center))*end_fade(p,x)


def end_fade(p,x):
    """Grade the crowns into the flat tower thresholds at the terminal edge."""
    return max(0,min(1,(x+p['length']/2)/p['end_length'],(p['length']/2-x)/p['end_length']))


def garage(seed=101, system=None, levels=None, tee_count=None, occupancy=None):
    rng = random.Random(seed)
    system = system or ('precast' if seed % 2 else 'pt')
    if system not in ('precast', 'pt'): raise ValueError(system)
    municipal = system == 'precast'
    count = tee_count if tee_count is not None else ((22 if municipal else 16) if seed in SEEDS else rng.choice((20,21,22,24) if municipal else (16,17,18)))
    levels = levels if levels is not None else ((4 if municipal else 3) if seed in SEEDS else rng.choice((4,5) if municipal else (3,4)))
    if not 3 <= levels <= 5 or not 12 <= count <= 24: raise ValueError('3–5 levels, 12–24 tee stations')
    length = count*TEE
    end = 3*TEE
    rw = SPAN if municipal else AISLE
    width = SPAN+rw
    fy = -width/2+SPAN/2
    ry = width/2-rw/2
    p = dict(seed=seed, system=system, name='ALDER QUAY / MUNICIPAL PARKING' if municipal else 'BELLWETHER / COMMONS PARKING',
             year=1988 if municipal else 1996, levels=levels, tee_count=count,
             length=length, width=width, floor_to_floor=FLOOR, flat_y=fy,
             ramp_y=ry, ramp_width=rw, ramp_limits=[-length/2+end, length/2-end],
             end_length=end, transition=0 if municipal else 10*FT,
             occupancy=occupancy if occupancy is not None else (.67 if municipal else .74),
             structural_grid=3*TEE, stalls=[], paths=[], pedestrian_paths=[],
             towers=[[-length/2-2.5,-width/2+4.35,0], [length/2+2.5,-width/2+4.35,0]],
             joint_y=(SPAN-rw)/2)
    if not 0<=p['occupancy']<=1:raise ValueError('Occupancy must be a fraction in [0,1]')
    p['ramp_slope'] = FLOOR/(p['ramp_limits'][1]-p['ramp_limits'][0]-p['transition'])
    a,b=p['ramp_limits']
    stations=[-length/2+i*3*TEE for i in range(count//3+1)]
    p['structural_stations']=sorted({-length/2,a,b,length/2,*[x for x in stations if a<x<b]})
    if municipal and p['ramp_slope'] > 1/15+1e-9: raise ValueError('Parking slope exceeds 1:15')
    if not municipal and p['ramp_slope'] > .125: raise ValueError('Speed ramp exceeds 12.5%')
    # Avoid end turning bays and column envelopes; stall lines are independent
    # of tee joints. Accessible block is reserved on the ground south row.
    n = int((length-2*end-6*FT)//STALL)
    x0 = -n*STALL/2
    raw_capacity=2*n*((2*levels-1) if municipal else levels)
    required=next(number for limit,number in ((25,1),(50,2),(75,3),(100,4),(150,5),(200,6),(300,7),(400,8),(500,9)) if raw_capacity<=limit)
    pairs=math.ceil(required/2);van_pairs=math.ceil(2*pairs/6)
    reserved_width=sum((11 if j<van_pairs else 8)*FT+5*FT+8*FT for j in range(pairs))
    reserved_normal=math.ceil(reserved_width/STALL)
    p['accessible_interval']=[x0,x0+reserved_width]
    p['ground_lane_shift']=.5148
    index = 0
    for level in range(levels):
        for ramp in (False, True):
            if ramp and (not municipal or level == levels-1): continue
            cy = ry if ramp else fy
            for row in (-1, 1):
                for i in range(n):
                    x = x0+(i+.5)*STALL
                    if level == 0 and not ramp and row == -1 and i < reserved_normal: continue
                    y = cy+row*(AISLE/2+DEPTH/2)
                    index += 1
                    compact = not ramp and row==1 and ((level==levels-1 and i in (n-3,n-2,n-1)) or (level==0 and x0-2<x<x0+reserved_width+2))
                    dep=16*FT if compact else DEPTH
                    if compact:y+=row*(DEPTH-dep)/2
                    p['stalls'].append(dict(id=f'L{level+1}-{index:03d}', x=x, y=y, z=deck_z(p,level,x,y,ramp),
                         level=level, ramp=ramp, yaw=180 if row==-1 else 0, width=STALL, depth=dep,
                         slope_x=p['ramp_slope'] if ramp else 0, crossfall=-.01*row,
                         occupied=rng.random()<p['occupancy'], car=rng.choice((0,3)) if compact else rng.randrange(6), compact=compact, accessible=False))
    # Count-dependent paired spaces: eight at the municipal garage, four at
    # the smaller garage. Two / one vans respectively (one in every six).
    x = x0
    for pair in range(pairs):
        is_van=pair<van_pairs
        w = 11*FT if is_van else 8*FT
        aisle = 5*FT
        for side in (0,1):
            xx = x+w/2 if side==0 else x+w+aisle+8*FT/2
            ww = w if side==0 else 8*FT
            yy = fy-AISLE/2-DEPTH/2+.42
            p['stalls'].append(dict(id=f'ACCESS-{pair*2+side+1}',x=xx,y=yy,z=deck_z(p,0,xx,yy),level=0,ramp=False,
                yaw=180,width=ww,depth=DEPTH,slope_x=0,crossfall=.01,occupied=False,car=1,compact=False,accessible=True,
                van=is_van and side==0,access_aisle=[x+w,x+w+aisle]))
        x+=w+aisle+8*FT
    # Two-way drive centerlines: one up circuit per floor, duplicated with
    # reversed points for descent. End turns use 9.144m centerline diameter.
    a,b=p['ramp_limits'];radius=22*FT
    for level in range(levels-1):
        pts=[]
        # Main ramp center follows actual modeled elevations.
        for j in range(33):
            xx=a+(b-a)*j/32
            pts.append([xx,ry,deck_z(p,level,xx,ry,True)])
        # End bays are crossfall-warped connection slabs between ramp and flat.
        arc=[]
        # Two true quarter circles with a tangent straight between. At the
        # smaller garage their radii share a short tangent at the center.
        r=min(radius,(ry-fy)/2)
        for j in range(1,9):
            th=j*math.pi/16;arc.append((b+r*math.sin(th),ry-r*(1-math.cos(th))))
        if ry-fy>2*r+1e-6:arc.append((b+r,fy+r))
        for j in range(1,9):
            th=j*math.pi/16;arc.append((b+r*math.cos(th),fy+r-r*math.sin(th)))
        for xx,yy in arc:pts.append([xx,yy,deck_z(p,level+1,xx,yy,yy>p['joint_y'])-FLOOR*ramp_fraction(xx,p)*(yy>p['joint_y'])])
        for j in range(1,33):
            xx=b-(b-a)*j/32;pts.append([xx,fy,deck_z(p,level+1,xx,fy)])
        if level<levels-2:
            for xx,yy in arc: # mirror across both plan center axes
                xx=-xx;yy=fy+ry-yy
                pts.append([xx,yy,deck_z(p,level+1,xx,yy,yy>p['joint_y'])-FLOOR*ramp_fraction(xx,p)*(yy>p['joint_y'])])
        p['paths'].append(dict(name=f'Drive_Up_{level+1}_{level+2}',points=pts,width=AISLE,two_way=True))
        p['paths'].append(dict(name=f'Drive_Down_{level+2}_{level+1}',points=list(reversed(pts)),width=AISLE,two_way=True))
    # Street to ground aisle, then the actual first ramp. The exit is a
    # different lane, not an oppositely directed copy through the same gate.
    ex=length/2-end/2;turn=15*FT;entry_x=ex-1.65;exit_x=ex+1.65
    def ground_point(xx,yy):
        if abs(yy-fy)<1e-6:yy+=ground_lane_offset(p,xx)
        if municipal and yy<-width/2-(6.1-1.8288):
            return [xx,yy,-.14605*((-width/2-(6.1-1.8288))-yy)/1.8288]
        return [xx,yy,max(0,deck_z(p,0,xx,yy,yy>p['joint_y'])-FLOOR*ramp_fraction(xx,p)*(yy>p['joint_y']))]
    entry=[ground_point(entry_x,-width/2-6.05),ground_point(entry_x,-width/2-5.3),ground_point(entry_x,-width/2-(6.1-1.8288)),ground_point(entry_x,fy-turn)]
    for j in range(1,9):
        th=j*math.pi/16;entry.append(ground_point(entry_x-turn*(1-math.cos(th)),fy-turn+turn*math.sin(th)))
    entry_start=entry[-1][0]
    entry.extend(ground_point(entry_start+(a-entry_start)*j/32,fy) for j in range(1,33))
    west=[(-xx,fy+ry-yy) for xx,yy in arc]
    entry.extend(ground_point(xx,yy) for xx,yy in west)
    exit_route=[ground_point(xx,yy) for xx,yy in reversed([(a,fy),*west])]
    exit_route.extend(ground_point(a+(exit_x-turn-a)*j/32,fy) for j in range(1,33))
    for j in range(1,9):
        th=j*math.pi/16;exit_route.append(ground_point(exit_x-turn+turn*math.sin(th),fy-turn*(1-math.cos(th))))
    exit_route.extend([ground_point(exit_x,-width/2-(6.1-1.8288)),ground_point(exit_x,-width/2-5.3),ground_point(exit_x,-width/2-6.05)])
    p['paths'].extend([dict(name='Drive_Entry_to_L1',points=entry,width=2.925,two_way=False),dict(name='Drive_L1_to_Exit',points=exit_route,width=2.925,two_way=False)])
    # Access aisles connect behind the stalls to the lift approach, rather
    # than attempting to pass through the front vehicle barrier.
    ty=p['towers'][0][1]
    for pair in range(pairs):
        s=next(s for s in p['stalls'] if s['id']==f'ACCESS-{2*pair+1}')
        xx=sum(s['access_aisle'])/2;yy=fy-1.4
        coords=[(xx,s['y']),(xx,yy),(a-.9,yy),(-length/2+1.2,yy),(-length/2+1.2,ty-1.3),(-length/2+.215,ty-1.3)]
        p['pedestrian_paths'].append(dict(name=f'AccessAisle_{pair+1}_to_Lift',width=1.524,points=[[x,y,deck_z(p,0,x,y)] for x,y in coords]))
    p['pedestrian_paths'].append(dict(name='WestStair_to_PublicWalk',width=.9144,points=[
        [-length/2+.215,ty+1.45,0],[-length/2-.67,ty+1.45,0],
        [-length/2-.67,ty+4.65,0],[-length/2-5.35,ty+4.65,0]]))
    for level in range(levels):
        pts=[]
        for xx,yy in ((b,fy+2.2),(0,fy+2.2),(a,fy+2.2),(-length/2+.35,fy+2.2),(-length/2+.215,p['towers'][0][1]+1.45)):
            pts.append([xx,yy,deck_z(p,level,xx,yy)])
        p['pedestrian_paths'].append(dict(name=f'Walk_L{level+1}_to_WestStair',width=1.524,points=pts))
    counters={}
    for stall in p['stalls']:
        level=stall['level'];counters[level]=counters.get(level,0)+1
        stall['paint_number']=f'{counters[level]:03d}'
    return p


def ground_lane_offset(p,x):
    a,b=p['accessible_interval']
    return p['ground_lane_shift']*max(0,min(1,(x-a+2)/2,(b+2-x)/2))
