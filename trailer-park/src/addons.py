"""Site-made timber and aluminum additions, utilities and household dressing."""
import math,random
from geometry import Assembly,label
from homes import STEEL,ZINC

WOOD=(.22,.195,.14)


def deck(name='Deck',width=3.6576,depth=2.1336,height=.885,seed=1):
    a=Assembly(name);m=a.mesh('Timber',component='deck');r=random.Random(seed)
    # Footings, 4x4 posts, beams, 2x8 rim/joists and 5/4 deck boards.
    for x in (-width/2+.10,width/2-.10):
        for y in (-depth/2+.14,depth/2-.14):
            m.box((x,y,.05),(.33,.33,.1),'Concrete')
            m.box((x,y,(height-.15+.10)/2),(.0889,.0889,height-.15-.10),'Veneer',WOOD)
    for y in (-depth/2+.10,depth/2-.10):m.box((0,y,height-.17),(width,.0762,.1842),'Veneer',WOOD)
    for j in range(math.ceil(width/.4064)+1):
        x=-width/2+j*width/math.ceil(width/.4064);m.box((x,0,height-.118),(.0381,depth,.1842),'Veneer',WOOD)
    n=math.ceil(depth/.145)
    for j in range(n):
        y=-depth/2+(j+.5)*depth/n;c=tuple(v*r.uniform(.92,1.08) for v in WOOD)
        # Gentle cup is authored as a three-station top with a genuine gauge.
        z=height-.003*r.random()
        m.prism([(-width/2,y-depth/n/2+.003,z+.001),(width/2,y-depth/n/2+.003,z+.001),
                 (width/2,y+depth/n/2-.003,z),(-width/2,y+depth/n/2-.003,z)],(0,0,-1),.0254,'Veneer',c)
    stairs(a,width,depth,height,m)
    # Front opening aligns to stair flight; home side remains open at the door.
    gap=.98;left=-width/2;right=width/2
    for x in (left,left+.95,right):m.box((x,-depth/2,height+.43),(.0889,.0889,.99),'Veneer',WOOD)
    for x0,x1 in ((left+.99,right),):
        for z in (height+.12,height+.86):m.box(((x0+x1)/2,-depth/2,z),(x1-x0,.0381,.0889),'Veneer',WOOD)
        m.box(((x0+x1)/2,-depth/2,height+.935),(x1-x0+.09,.1397,.032),'Veneer',WOOD)
        n=math.ceil((x1-x0)/.125)
        for j in range(n):m.box((x0+(j+.5)*(x1-x0)/n,-depth/2,height+.46),(.0381,.0381,.64),'Veneer',WOOD)
    for x in (left,right):
        m.box((x,depth/2,height+.43),(.0889,.0889,.99),'Veneer',WOOD)
        for z in (height+.12,height+.86):m.box((x,0,z),(.0381,depth,.0889),'Veneer',WOOD)
        m.box((x,0,height+.935),(.1397,depth+.09,.032),'Veneer',WOOD)
        for j in range(math.ceil(depth/.125)):
            m.box((x,-depth/2+(j+.5)*depth/math.ceil(depth/.125),height+.46),(.0381,.0381,.64),'Veneer',WOOD)
    m.finish();a.socket('Door',(0,depth/2+.025,height),'door_connection');a.socket('Occupant',(0,0,height),'occupant')
    a.socket('Walk',(-width/2+.475,-depth/2-1.4,0),'walk');return a


def stairs(a,width,depth,height,m):
    n=6;rise=height/n;run=.2794;x=-width/2+.475;y0=-depth/2
    # Side stringers bear on a concrete toe pad; six equal risers.
    m.box((x,y0-(n-1)*run+.14,-.035),(1.13,.65,.07),'Concrete')
    for sx in (-.40,.40):
        m.beam((x+sx,y0-.03,height-.13),(x+sx,y0-n*run+.05,.10),.0381,.1842,'Veneer',WOOD,r=0)
    for j in range(n-1):
        y=y0-(j+.5)*run;z=height-(j+1)*rise
        m.box((x,y,z-.019),(.94,run+.018,.0381),'Veneer',WOOD)
        m.box((x,y+run/2-.015,z-rise/2-.038),(.94,.0254,rise-.038),'Veneer',WOOD)
    for sx in (-.49,.49):
        m.box((x+sx,y0-n*run+.1,.51),(.0889,.0889,1.02),'Veneer',WOOD)
        m.beam((x+sx,y0,height+.90),(x+sx,y0-n*run+.10,.92),.042,.068,'Veneer',WOOD,r=.002)


def carport(name='Carport',length=6.7056,width=3.3528,sag=0):
    a=Assembly(name);m=a.mesh('AluminumPans',component='carport');zback=2.68;zfront=2.42
    # Independent support posts; an add-on never loads a mobile home's wall.
    for x in (-length/2+.13,0,length/2-.13):
        for sy in (-1,1):
            y=sy*(width/2-.08);z=zfront if sy<0 else zback
            m.box((x,y,.035),(.35,.35,.07),'Concrete')
            # Hollow 76.2 mm square posts, 2 mm walls and anchored foot plate.
            m.box((x,y,.085),(.15,.15,.010),'Trim',ZINC)
            for s in (-1,1):
                m.box((x+s*.0371,y,z/2),(.002,.0762,z-.14),'Trim',(.49,.50,.46))
                m.box((x,y+s*.0371,z/2),(.0722,.002,z-.14),'Trim',(.49,.50,.46))
            m.beam((x,y,z-.48),(x+(.28 if x<=0 else -.28),y,z-.05),.025,.025,'Trim',ZINC,r=0)
    for sy in (-1,1):m.box((0,sy*width/2,(zfront if sy<0 else zback)-.065),(length,.045,.13),'Trim')
    for x in (-length/2,0,length/2):m.beam((x,-width/2,zfront-.025),(x,width/2,zback-.025),.05,.10,'Trim',r=0)
    n=math.ceil(length/.3048)
    for j in range(n):
        x0=-length/2+j*length/n;x1=-length/2+(j+1)*length/n
        # Folded pans form shallow integral ribs with hems; a sag is confined
        # to one midspan pan rather than drooping the whole rigid frame.
        profile=[(x0,0),(x0+.018,.027),(x0+.038,.027),(x0+.052,0),(x1-.015,0),(x1,.022)]
        vs=[]
        for y in (-width/2,0,width/2):
            z=zfront+(y+width/2)/width*(zback-zfront)
            drop=sag*math.sin((y+width/2)/width*math.pi) if abs((x0+x1)/2)<.55 else 0
            vs.extend([(x,y,z+dz-drop) for x,dz in profile])
        fs=[]
        for row in range(2):
            for k in range(len(profile)-1):fs.append((row*6+k,row*6+k+1,(row+1)*6+k+1,(row+1)*6+k))
        m.geom(vs,fs,'Trim',(.57,.56,.49))
    m.finish();a.socket('Car',(0,-.05,0),'car',yaw=90);return a


def utility(name='UtilityService'):
    a=Assembly(name);m=a.mesh('MeterAndRisers',component='utilities')
    m.box((0,0,.04),(.68,.52,.08),'Concrete');m.box((0,0,.70),(.16,.12,1.32),'Trim',(.20,.24,.20))
    m.box((0,-.015,1.12),(.36,.18,.52),'Trim',(.27,.30,.27),r=.007)
    m.box((0,-.114,.95),(.30,.020,.17),'Trim',(.20,.24,.21),r=.004)
    m.tube([(0,-.11,1.22),(0,-.17,1.22)],.105,'Trim',ZINC,20)
    m.tube([(0,-.172,1.22),(0,-.178,1.22)],.084,'Glass',(.52,.59,.55),20)
    m.box((0,-.181,1.22),(.10,.004,.035),'Trim',(.025,.030,.024))
    m.tube([(.10,.06,.08),(.10,.06,.72),(.10,.09,.81),(.10,.10,.98)],.020,'Trim',ZINC,8)
    # Supply/riser bends, shutoff valve and insulated low connection.
    m.tube([(.56,.05,0),(.56,.05,.40),(.53,.05,.48),(.36,.05,.48)],.016,'Trim',(.26,.28,.26),8)
    m.box((.56,.05,.31),(.11,.025,.018),'Trim',(.12,.24,.28))
    m.tube([(.85,.05,.02),(.85,.05,.23)],.051,'Trim',(.55,.55,.45),12)
    m.tube([(.85,.05,.23),(.85,.05,.252)],.063,'Trim',(.58,.57,.48),12)
    m.box((.85,.05,.263),(.028,.045,.020),'Trim')
    m.finish();a.socket('Electric',(.10,.1,.08),'service');a.socket('Water',(.36,.05,.48),'water');a.socket('Sewer',(.85,.05,.1),'sewer');return a


def propane(name='PropaneBottles'):
    a=Assembly(name);m=a.mesh('Bottles',component='propane')
    m.box((0,0,.035),(.85,.46,.07),'Concrete')
    for x in (-.22,.22):
        # 100 lb vertical cylinder envelope, foot ring and open protective collar.
        profile=[(.08,.13),(.11,.16),(.16,.178),(.94,.178),(1.02,.15),(1.07,.055)]
        for (z0,r0),(z1,r1) in zip(profile,profile[1:]):
            vs=[(x+r*math.cos(k*math.tau/20),r*math.sin(k*math.tau/20),z) for z,r in ((z0,r0),(z1,r1)) for k in range(20)]
            m.geom(vs,[(k,(k+1)%20,(k+1)%20+20,k+20) for k in range(20)],'Trim',(.58,.57,.49))
        m.tube([(x,0,1.07),(x,0,1.14)],.019,'Trim',(.34,.23,.07),8)
        for sy in (-1,1):m.box((x,sy*.11,1.12),(.18,.012,.12),'Trim')
    m.tube([(-.22,0,1.13),(-.13,.08,1.17),(0,.14,1.13),(.14,.13,1.09),(.22,0,1.13)],.008,'Trim',STEEL,6)
    m.finish();return a


def conditioner(name='AC',kind='condenser'):
    a=Assembly(name);m=a.mesh('Housing',component='ac')
    if kind=='window':
        m.box((0,0,0),(.58,.55,.38),'Trim',(.48,.48,.42),r=.006)
        for j in range(12):m.box((-.255+j*.046,-.280,0),(.016,.012,.31),'Trim',(.12,.15,.13))
        for x in (-.20,.20):m.beam((x,.15,-.16),(x,-.24,-.36),.024,.025,'Trim',ZINC,r=0)
    else:
        m.box((0,0,.05),(.98,.98,.10),'Concrete');m.box((0,0,.47),(.75,.75,.75),'Trim',(.32,.33,.29),r=.006)
        for sy in (-1,1):
            for j in range(17):m.box((0,sy*.380,.16+j*.037),(.69,.009,.012),'Trim',(.13,.15,.125))
        m.tube([(0,0,.850),(0,0,.864)],.29,'Trim',(.10,.12,.095),20)
        for k in range(12):
            ang=k*math.tau/12;m.beam((0,0,.872),(.28*math.cos(ang),.28*math.sin(ang),.872),.008,.008,'Trim',ZINC,r=0)
        m.tube([(.35,.2,.18),(.49,.24,.18),(.53,.35,.13),(.62,.46,.13)],.025,'Trim',(.030,.035,.028),8)
    m.finish();return a


def dish(name='SatelliteDish'):
    a=Assembly(name);m=a.mesh('StampedDish',component='dish')
    # Concave spun oval pan with a return lip; inclined on a real mounting arm.
    rings=5;sides=24;vs=[]
    for j in range(rings):
        rr=.035+j*.285/(rings-1)
        for k in range(sides):
            t=k*math.tau/sides;vs.append((rr*math.cos(t),-.08*(rr/.32)**2,rr*1.12*math.sin(t)+.46))
    fs=[(j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k) for j in range(rings-1) for k in range(sides)]
    m.geom(vs,fs,'Trim',(.40,.42,.39));m.tube([(0,.09,.06),(0,.09,.44)],.024,'Trim',ZINC,8)
    m.tube([(0,0,.18),(0,-.44,.30),(0,-.49,.46)],.015,'Trim',ZINC,8)
    m.box((0,-.49,.46),(.075,.095,.065),'Trim',(.12,.14,.13));m.finish();return a


def room(name='AddedRoom',width=3.2,depth=2.4):
    a=Assembly(name);m=a.mesh('IndependentRoom',component='added_room')
    for x in (-width/2+.2,width/2-.2):
        for y in (-depth/2+.2,depth/2-.2):m.box((x,y,.35),(.25,.25,.70),'Concrete')
    m.box((0,0,.80),(width,depth,.18),'Veneer',WOOD)
    # Infill window opening is split, not painted over a solid wall.
    for x in (-width/2,width/2):m.box((x,0,1.85),(.10,depth,2.1),'Siding',(.34,.36,.28))
    for xx in (-width*.355,width*.355):m.box((xx,-depth/2,1.85),(width*.29,.10,2.1),'Siding',(.34,.36,.28))
    m.box((0,-depth/2,1.12),(width*.42,.10,.64),'Siding',(.34,.36,.28));m.box((0,-depth/2,2.73),(width*.42,.10,.34),'Siding',(.34,.36,.28))
    m.box((0,-depth/2,2.05),(width*.42,.01,1.2),'Glass');m.box((0,-depth/2-.018,2.05),(.032,.04,1.20),'Trim')
    m.prism([(-width/2-.10,-depth/2-.15,2.95),(width/2+.1,-depth/2-.15,2.95),(width/2+.1,depth/2,3.20),(-width/2-.1,depth/2,3.20)],(0,0,-1),.10,'Trim',(.47,.47,.41))
    m.finish();return a


def dressing(name='Household',seed=1):
    a=Assembly(name);m=a.mesh('PotsToy',component='household');r=random.Random(seed)
    for x in (-.5,.45):
        m.tube([(x,0,.02),(x,0,.24)],.13,'Veneer',(.32,.15,.075),10)
        for j in range(6):
            t=j*math.tau/6;m.beam((x,0,.22),(x+.16*math.cos(t),.16*math.sin(t),.43+r.random()*.12),.015,.025,'Siding',(.055,.12,.025),r=0)
    if seed%2:
        # Small ride-on toy: colored seat, four actual wheels, steering loop.
        m.box((.1,-.65,.24),(.36,.56,.17),'Trim',(.41,.025,.015),r=.03)
        for x in (-.22,.42):
            for y in (-.81,-.48):m.tube([(x-.05,y,.13),(x+.05,y,.13)],.10,'Trim',(.018,.021,.016),10)
        m.tube([(.1,-.84,.31),(.1,-.84,.52)],.018,'Trim',(.30,.22,.03),8)
    m.finish();return a


def sign(name='EntranceSign',text='ALDER COURT'):
    a=Assembly(name);m=a.mesh('PostsAndBoard',component='sign')
    for x in (-1.20,1.20):m.box((x,0,.98),(.14,.14,1.96),'Veneer',WOOD)
    m.box((0,-.025,1.37),(2.9,.10,.88),'Trim',(.032,.105,.080),r=.015)
    for z in (.97,1.77):m.box((0,-.088,z),(2.82,.025,.034),'Trim',(.44,.37,.20))
    m.finish();label(a,text,(0,-.088,1.42),.23);label(a,'MANUFACTURED HOME COMMUNITY',(0,-.089,1.17),.092)
    return a
