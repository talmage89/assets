"""Blender-free civic program grammar and deliberately different parcels."""
import random
FT=.3048


def building(seed=101,program='hall',style=None,bays=None,bay_width=None,stories=None,order=None,roof=None,wings=True):
    if program not in ('hall','station','post_office','library'):raise ValueError(program)
    rng=random.Random(seed);station=program=='station'
    bays=bays or (3 if station else 7 if program=='hall' else 5)
    bay_width=bay_width or (18*FT if station else 13.7142857*FT)
    if station and not 2<=bays<=4:raise ValueError('Station accepts 2–4 apparatus bays')
    if not station and (not 3<=bays<=11 or bays%2==0):raise ValueError('Historic frontages use 3–11 bays with a central entry bay')
    if bay_width<(4.8 if station else 3.0):raise ValueError('Bay width leaves insufficient pier/entry clearance')
    stories=stories or (1 if station or program=='post_office' else 2)
    if stories not in (1,2,3):raise ValueError('1–3 stories')
    if station and stories>2:raise ValueError('Station crew wing supports one or two stories')
    style=style or ('municipal_modern' if station else 'colonial' if program=='library' else 'classical')
    if style not in ('municipal_modern','classical','colonial'):raise ValueError(style)
    if station and style!='municipal_modern':raise ValueError('Station style is municipal_modern')
    if not station and style=='municipal_modern':raise ValueError('Historic civic programs use classical or colonial')
    order=order or ('plain' if station else 'columns' if program=='hall' else 'pilasters')
    roof=roof or ('hip' if style=='colonial' else 'parapet')
    if order not in ('columns','pilasters','plain'):raise ValueError(order)
    if roof not in ('parapet','hip','cupola'):raise ValueError(roof)
    if station and (order!='plain' or roof=='cupola'):raise ValueError('Station accepts a plain entry and parapet or hip roof')
    bayblock=bays*bay_width+(.9144 if station else 0)
    office=36*FT if station and wings else 0
    width=bayblock+office;depth=(60 if station else 58)*FT
    return dict(seed=seed,program=program,style=style,bays=bays,bay_width=bay_width,
        stories=stories,order=order,roof=roof,wings=wings,width=width,depth=depth,
        floor=.1524 if station or program=='post_office' else .9144,
        story_pitch=3.9624,bayblock=bayblock,office=office,
        name={'hall':'BRIAR GLEN CITY HALL','station':'BRIAR GLEN FIRE - RESCUE','post_office':'NORTH VALE POST OFFICE','library':'CEDAR FORK PUBLIC LIBRARY'}[program],
        year=1974 if station else 1928 if program=='hall' else 1936,
        brick=1 if station else 0,trim=(.64,.64,.59) if not station else (.45,.050,.024),
        replaced_windows=sorted(rng.sample(range(bays),min(2,bays))) if not station else [])


def site(seed=101):
    hall=seed%2==1;p=building(seed,'hall' if hall else 'station')
    if hall:
        return dict(seed=seed,kind='downtown',building=p,parcel=(-40,40,-29,39),
            building_at=(-6,0,0),road_y=-35,road_width=12.8,
            lots=[dict(id='Police',rect=(-21,9,22,38),rows=1,stalls=9,fenced=True),dict(id='Public',rect=(21,38,-9,28),rows=1,stalls=10,fenced=False)],
            walks=[(-8.1,-3.9,-29,-14.3),(-8.1,11.8,-16,-14.3),(9.3,11.2,-14.3,.2),(10.4,20.4,-3,-1.2),(-16,-8.1,-18.5,-14.3),(-1,3,-18.5,-16),(-14.8,-11.8,20.60,22.05)],
            ramps=[dict(rect=(20.4,22.4,-3,-1.2),high=.145,low=-.003)],
            trees=[(-32,-19),(27,-22),(-32,8),(-30,34),(34,34),(14,34)],
            flags=[(-21,-19),(12,-20)],occupancy=.78)
    return dict(seed=seed,kind='arterial',building=p,parcel=(-43,43,-32,34),
        building_at=(-5,4,0),road_y=-41,road_width=15.0,
        lots=[dict(id='Staff',rect=(15,40,-3,26),rows=1,stalls=9,fenced=False)],
        walks=[(2.8,4.6,-32,-5),(4.6,17,-8,-6.2),(11,12.8,-6.2,-1.2),(10.5,15,-13.6,-8)],
        ramps=[dict(rect=(12.8,15,-3,-1.2),high=.145,low=-.003)],
        trees=[(-36,23),(-34,-20),(33,-26),(38,30),(-20,31)],flags=[(9,-20)],occupancy=.78)


def cases():
    large=building(707,'hall',bays=11,bay_width=4.8768,wings=False)
    large['name']='MAPLE RIDGE MUNICIPAL HALL'
    return [building(101,'hall'),building(202,'station'),
        building(303,'post_office',bays=5,order='pilasters',wings=False),
        building(404,'library',bays=5,stories=2,roof='cupola',wings=False),
        building(505,'station',bays=2,stories=2,wings=True),
        building(606,'hall',bays=5,stories=1,order='plain',roof='hip',wings=False),large]
