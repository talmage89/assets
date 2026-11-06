"""Bounded original rental-housing grammar. Pure Python, meters, -Y frontage.

Dimensions are design decisions checked against REFERENCE.md, never asserted
as measurements of a photograph. Separate stair cores keep wings legible.
"""
import copy
import math
import random
FT=.3048
COMPLEX_SEEDS=(301,302,303,304)
ROW_SEEDS=(401,402,403,404)
PALETTES=(
 dict(siding=(.25,.29,.22),brick=(.24,.105,.057),trim=(.52,.49,.39),door=(.09,.13,.105)),
 dict(siding=(.36,.29,.20),brick=(.28,.17,.105),trim=(.38,.32,.23),door=(.12,.065,.035)),
 dict(siding=(.40,.42,.37),brick=(.25,.115,.075),trim=(.67,.65,.58),door=(.12,.055,.035)),
 dict(siding=(.29,.33,.35),brick=(.32,.23,.15),trim=(.64,.63,.57),door=(.075,.10,.13)))


def garden(seed=301,**overrides):
    r=random.Random(seed);i=(seed-301)%4
    d=copy.deepcopy((
        dict(era=1967,floors=3,access='enclosed',skin='brick',roof='gable',shape='straight',sunken=False),
        dict(era=1978,floors=2,access='breezeway',skin='mixed',roof='mansard',shape='L',sunken=False),
        dict(era=1986,floors=3,access='open',skin='mixed',roof='gable',shape='offset',sunken=False),
        dict(era=1973,floors=2,access='breezeway',skin='siding',roof='mansard',shape='straight',sunken=False))[i])
    allowed=set(d)|{'unit_width_ft','unit_depth_ft','color','modules'}
    if set(overrides)-allowed:raise ValueError('Unknown garden controls')
    if seed not in COMPLEX_SEEDS and 'unit_width_ft' not in overrides:d['unit_width_ft']=r.choice((24,26,28))
    d.update(overrides)
    d.update(seed=seed,color=copy.deepcopy(overrides.get('color',PALETTES[i])),floor_height=9*FT,wall=.254)
    if i==3:d['color']['siding']=(.16,.29,.23)
    d['unit_width']=d.get('unit_width_ft',28 if d['access']!='breezeway' else 24)*FT
    d['unit_depth']=overrides.get('unit_depth_ft',25 if d['access']!='breezeway' else 32)*FT
    d['core_width']=16*FT
    d['wing_gap_m']=10*FT
    d['base']=.1524 if not d['sunken'] else -.9144
    d['width']=2*d['unit_width']+d['core_width'] if d['access']!='breezeway' else 4*d['unit_width']
    d['depth']=2*d['unit_depth'] if d['access']!='breezeway' else d['unit_depth']
    # Wings connect through a supported open link; roof envelopes never overlap.
    w,dep=d['width'],d['depth']
    modules=[dict(origin=(0,0,0),yaw=0)]
    if d['shape']=='L':modules.append(dict(origin=(w/2+dep/2+d['wing_gap_m'],w/2-dep/2,0),yaw=90))
    elif d['shape']=='offset':modules.append(dict(origin=(w+d['wing_gap_m'],dep*.30,0),yaw=0))
    d['modules']=copy.deepcopy(overrides.get('modules',modules))
    corners=[transform((x,y,0),q['origin'],q['yaw']) for q in d['modules'] for x in (-w/2,w/2) for y in (-dep/2,dep/2)]
    cx=(min(q[0] for q in corners)+max(q[0] for q in corners))/2;cy=(min(q[1] for q in corners)+max(q[1] for q in corners))/2
    d['module_recenter_m']=(cx,cy)
    for q in d['modules']:q['origin']=(q['origin'][0]-cx,q['origin'][1]-cy,q['origin'][2])
    d['footprint_polygons']=[[transform((x,y,0),q['origin'],q['yaw']) for x,y in ((-w/2,-dep/2),(w/2,-dep/2),(w/2,dep/2),(-w/2,dep/2))] for q in d['modules']]
    d['units_per_module']=4*d['floors'];d['units']=d['units_per_module']*len(d['modules'])
    if not 8<=d['units']<=24:raise ValueError('Garden building must have 8–24 units')
    d['stairs']=dict(risers=16,rise=d['floor_height']/16,going=11*FT/12,clear_width=44*FT/12,
                     guard=42*FT/12,handrail=36*FT/12,baluster=.0127,pitch=.1016,landing=48*FT/12)
    d['unit_rooms']=unit_rooms(d['unit_width'],d['unit_depth'],d['access']=='breezeway')
    d['name']='Rill Court';d['period']=2005
    validate_garden(d);return d


def row(seed=401,**overrides):
    r=random.Random(seed);i=(seed-401)%4
    d=copy.deepcopy((dict(era=1974,count=6,width_ft=20,depth_ft=32,roof='mansard',skin='siding',garage=False,parapet=True),
                     dict(era=1985,count=6,width_ft=20,depth_ft=34,roof='gable',skin='brick',garage=False,parapet=False),
                     dict(era=2002,count=6,width_ft=24,depth_ft=38,roof='cross_gable',skin='stone',garage=True,parapet=False),
                     dict(era=1979,count=4,width_ft=18,depth_ft=32,roof='mansard',skin='mixed',garage=False,parapet=True))[i])
    if set(overrides)-set(d):raise ValueError('Unknown row controls')
    if seed not in ROW_SEEDS:
        d['count']=r.choice((4,5,6,7,8));d['width_ft']=r.choice((22,24)) if d['garage'] else r.choice((18,20,22))
    d.update(overrides);d.update(seed=seed,color=copy.deepcopy(PALETTES[(i+1)%4]),floor_height=9*FT,base=.3048)
    d['width']=d['width_ft']*FT;d['depth']=d['depth_ft']*FT
    d['period']=2015 if d['era']>=2000 else 2005
    d['units']=[dict(index=j,x=(j-(d['count']-1)/2)*d['width'],y=(0,.6096,.3048,0)[j%4]-.3048,z=(j//2%2)*.1524,
                    door_replaced=r.random()<.23,window_replaced=r.random()<.32) for j in range(d['count'])]
    if not (4<=d['count']<=8 and 16<=d['width_ft']<=24):raise ValueError('Unsupported townhouse row dimensions')
    return d


def complex_plan(seed=301):
    i=(seed-301)%4;p=garden(seed);w,dep=p['width'],p['depth'];multi=len(p['modules'])>1
    lot=(136.,122.) if multi else (100.,86.)
    # Buildings flank a central landscaped court; wide drives join stall aisles.
    placements=([dict(id='A',origin=(-26,30,0),yaw=0),dict(id='B',origin=(26,-32,0),yaw=180)] if multi else [dict(id='A',origin=(-23,24,0),yaw=0),dict(id='B',origin=(23,24,0),yaw=0),dict(id='C',origin=(0,-27,0),yaw=180)])
    # Keep site geometry in its designed place after recentering each building.
    cx,cy=p['module_recenter_m']
    for b in placements:b['origin']=transform((cx,cy,0),b['origin'],b['yaw'])
    return dict(seed=seed,name=('RILL COURT','ALDER GLEN','MILLBROOK GREEN','FERN MEADOW')[i],building=p,
                lot=lot,buildings=placements,carports=i==1,amenity=('playground','pool','playground','none')[i],
                stalls=[dict(x=x,y=y,yaw=yaw) for y,yaw in ((-6.7932,0),(6.7932,180)) for x in [(-lot[0]/2+9)+j*9*FT for j in range(int((lot[0]-18)/(9*FT)))]] )


def transform(p,origin,yaw):
    a=math.radians(yaw);x,y,z=p
    return (origin[0]+x*math.cos(a)-y*math.sin(a),origin[1]+x*math.sin(a)+y*math.cos(a),origin[2]+z)


def unit_rooms(w,d,breezeway=False):
    # Schematic room reservations, not furnished interior meshes. Fractions
    # reserve real circulation rather than filling an envelope with bedrooms.
    if breezeway:
        return [dict(name=n,rect=[x0*w,x1*w,y0*d,y1*d]) for n,x0,x1,y0,y1 in (
            ('Entry / dining',0,.45,0,.27),('Kitchen',.45,1,0,.30),
            ('Storage / bath',.45,1,.30,.55),('Circulation',0,.45,.27,.55),
            ('Living',0,.58,.55,1),('Bedroom',.58,1,.55,1))]
    return [dict(name=n,rect=[x0*w,x1*w,y0*d,y1*d]) for n,x0,x1,y0,y1 in (
        ('Living',0,.58,0,.50),('Bedroom 1',.58,1,0,.50),
        ('Bedroom 2',0,.42,.50,1),('Passage',.42,1,.50,.60),
        ('Kitchen',.42,.72,.60,1),('Bath',.72,1,.72,1),
        ('Entry',.72,1,.60,.72))]


def validate_garden(d):
    s=d['stairs'];assert s['rise']<=7*.0254 and s['going']>=11*.0254-1e-8
    assert s['clear_width']>=44*.0254-1e-8 and s['guard']>=42*.0254-1e-8
    assert s['pitch']-s['baluster']<4*.0254
    assert 34*.0254<=s['handrail']<=38*.0254
    assert d['floor_height']-.254>=8*FT


if __name__=='__main__':
    import json
    for s in COMPLEX_SEEDS:print(json.dumps(garden(s)))
