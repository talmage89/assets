"""Site-made timber and aluminum additions, utilities and household dressing."""
import math,random,json
from geometry import Assembly,label
from homes import STEEL,ZINC

WOOD=(.22,.195,.14)


def deck(name='Deck',width=3.6576,depth=2.1336,height=.885,seed=1,flight='front',context=None):
    a=Assembly(name)
    if context:a.root['weather_spec']=json.dumps(context,sort_keys=True)
    m=a.mesh('Timber',component='deck',look_seed=seed);r=random.Random(seed)
    # Footings, 4x4 posts, beams, 2x8 rim/joists and 5/4 deck boards.
    joist_top=height-.0254;joist_bottom=joist_top-.1842
    beam_top=joist_bottom;beam_bottom=beam_top-.1842
    for x in (-width/2+.10,width/2-.10):
        for y in (-depth/2+.14,depth/2-.14):
            m.box((x,y,.05),(.33,.33,.1),'Concrete')
            m.box((x,y,(beam_bottom+.10)/2),(.0889,.0889,beam_bottom-.10),'Veneer',WOOD)
    for sy in (-1,1):
        m.box((0,sy*(depth/2-.14),(beam_top+beam_bottom)/2),(width,.0762,.1842),'Veneer',WOOD)
        m.box((0,sy*(depth/2-.01905),(joist_top+joist_bottom)/2),(width,.0381,.1842),'Veneer',WOOD)
    count=math.ceil((width-.0381)/.4064)
    for j in range(count+1):
        x=-width/2+.01905+j*(width-.0381)/count
        m.box((x,0,(joist_top+joist_bottom)/2),(.0381,depth-.0762,.1842),'Veneer',WOOD)
    n=math.ceil(depth/.145)
    for j in range(n):
        y=-depth/2+(j+.5)*depth/n;c=tuple(v*r.uniform(.92,1.08) for v in WOOD)
        # Gentle cup is authored as a three-station top with a genuine gauge.
        z=height-.003*r.random()
        top=[(xx,yy,zz) for xx in (-width/2,width/2) for yy,zz in
             ((y-depth/n/2+.003,z+.001),(y,z-.0015),(y+depth/n/2-.003,z))]
        faces=[(0,3,4,1),(1,4,5,2),(7,10,9,6),(8,11,10,7)]
        for aa,bb in ((0,3),(3,4),(4,5),(5,2),(2,1),(1,0)):faces.append((bb,aa,aa+6,bb+6))
        m.geom(top+[(xx,yy,zz-.0254) for xx,yy,zz in top],faces,'Veneer',c)
    if flight=='front':stairs(a,width,depth,height,m)
    elif flight=='right':
        sm=a.mesh('SideFlight',component='deck',look_seed=seed)
        stairs(a,width,depth,height,sm)
        anchor=-width/2+.475;y0=-depth/2
        sm.v=[(width/2-(y-y0),x-anchor,z) for x,y,z in sm.v];sm.finish()
    else:raise ValueError('flight front/right')
    # Front opening aligns to stair flight; home side remains open at the door.
    gap=.98;left=-width/2;right=width/2
    rail_post_top=height+.925
    for x in ((left,left+.95,right) if flight=='front' else (left,right)):m.box((x,-depth/2,(rail_post_top+joist_bottom)/2),(.0889,.0889,rail_post_top-joist_bottom),'Veneer',WOOD)
    for x0,x1 in (((left+.99,right),) if flight=='front' else ((left,right),)):
        for z in (height+.12,height+.86):m.box(((x0+x1)/2,-depth/2,z),(x1-x0,.0381,.0889),'Veneer',WOOD)
        m.box(((x0+x1)/2,-depth/2,height+.935),(x1-x0+.09,.1397,.032),'Veneer',WOOD)
        n=math.ceil((x1-x0)/.125)
        for j in range(n):m.box((x0+(j+.5)*(x1-x0)/n,-depth/2,height+.46),(.0381,.0381,.64),'Veneer',WOOD)
    for x in (left,right):
        m.box((x,depth/2,(rail_post_top+joist_bottom)/2),(.0889,.0889,rail_post_top-joist_bottom),'Veneer',WOOD)
        if flight=='right' and x==right:continue
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


def carport(name='Carport',length=6.7056,width=3.3528,sag=0,context=None):
    a=Assembly(name);a.root['weather_spec']=json.dumps(context or dict(seed=303,era='1972',upkeep='patched'),sort_keys=True)
    m=a.mesh('AluminumPans',component='carport');zback=2.68;zfront=2.42
    posts=a.mesh('PaintedSteelPosts',component='carport_posts')
    # Independent support posts; an add-on never loads a mobile home's wall.
    for x in (-length/2+.13,0,length/2-.13):
        for sy in (-1,1):
            y=sy*(width/2-.08);z=zfront if sy<0 else zback
            m.box((x,y,.035),(.35,.35,.07),'Concrete')
            # Hollow 76.2 mm square posts, 2 mm walls and anchored foot plate.
            posts.box((x,y,.085),(.15,.15,.010),'Trim',(.49,.50,.46))
            for s in (-1,1):
                posts.box((x+s*.0371,y,z/2),(.002,.0762,z-.14),'Trim',(.49,.50,.46))
                posts.box((x,y+s*.0371,z/2),(.0722,.002,z-.14),'Trim',(.49,.50,.46))
            m.beam((x,y,z-.48),(x+(.28 if x<=0 else -.28),y,z-.05),.025,.025,'Trim',ZINC,r=0)
    for sy in (-1,1):m.box((0,sy*width/2,(zfront if sy<0 else zback)-.065),(length,.045,.13),'Trim')
    for x in (-length/2,0,length/2):m.beam((x,-width/2,zfront-.05065),(x,width/2,zback-.05065),.05,.10,'Trim',r=0)
    n=math.ceil(length/.3048)
    for j in range(n):
        x0=-length/2+j*length/n;x1=-length/2+(j+1)*length/n
        # Folded pans form shallow integral ribs with hems; a sag is confined
        # to one midspan pan rather than drooping the whole rigid frame.
        profile=[(x0,0),(x0+.018,.027),(x0+.038,.027),(x0+.052,0),(x1-.015,0),(x1,.022)]
        vs=[]
        for y in (-width/2,0,width/2):
            z=zfront+(y+width/2)/width*(zback-zfront)
            drop=sag*math.sin((y+width/2)/width*math.pi) if abs((x0+x1)/2-length*.25)<.50 else 0
            vs.extend([(x,y,z+dz-drop) for x,dz in profile])
        fs=[]
        for row in range(2):
            for k in range(len(profile)-1):fs.append((row*6+k,row*6+k+1,(row+1)*6+k+1,(row+1)*6+k))
        # Actual 0.8 mm rolled skin, including the returned profile's cut ends.
        count=len(vs);back=[(x,y,z-.0008) for x,y,z in vs];closed=fs+[tuple(i+count for i in reversed(f)) for f in fs]
        occurrences={}
        for f in fs:
            for u,v in zip(f,f[1:]+f[:1]):
                key=tuple(sorted((u,v)));occurrences.setdefault(key,[]).append((u,v))
        for edge,uses in occurrences.items():
            if len(uses)==1:
                u,v=uses[0];closed.append((v,u,u+count,v+count))
        m.geom(vs+back,closed,'Trim',(.57,.56,.49))
    posts.finish();m.finish();a.socket('Car',(0,-.05,0),'car',yaw=90);return a


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
        profile=[(.08,.13),(.11,.17),(.16,.189),(1.01,.189),(1.09,.14),(1.12,.055)]
        for (z0,r0),(z1,r1) in zip(profile,profile[1:]):
            vs=[(x+r*math.cos(k*math.tau/20),r*math.sin(k*math.tau/20),z) for z,r in ((z0,r0),(z1,r1)) for k in range(20)]
            m.geom(vs,[(k,(k+1)%20,(k+1)%20+20,k+20) for k in range(20)],'Trim',(.58,.57,.49))
        for z,r in (profile[0],profile[-1]):m.geom([(x+r*math.cos(k*math.tau/20),r*math.sin(k*math.tau/20),z) for k in range(20)],[tuple(reversed(range(20))) if z==profile[0][0] else tuple(range(20))],'Trim',(.58,.57,.49))
        m.tube([(x,0,.07),(x,0,.12)],.1778,'Trim',(.43,.44,.39),20)
        m.tube([(x,0,1.12),(x,0,1.21)],.019,'Trim',(.34,.23,.07),8)
        for sy in (-1,1):m.box((x,sy*.11,1.211),(.18,.012,.13),'Trim')
    m.tube([(-.22,0,1.20),(-.13,.08,1.24),(0,.14,1.20),(.14,.13,1.16),(.22,0,1.20)],.008,'Trim',STEEL,6)
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


def room(name='AddedRoom',width=3.2,depth=2.4,seed=1):
    a=Assembly(name);m=a.mesh('IndependentRoom',component='added_room',look_seed=seed)
    color=((.31,.36,.34),(.50,.40,.22),(.45,.46,.39))[seed%3]
    for x in (-width/2+.2,width/2-.2):
        for y in (-depth/2+.2,depth/2-.2):
            m.box((x,y,.35),(.25,.25,.70),'Concrete')
            m.box((x,y,.705),(.26,.26,.01),'Veneer',WOOD)
    m.box((0,0,.80),(width,depth,.18),'Veneer',WOOD)
    # Infill window opening is split, not painted over a solid wall.
    for sign in (-1,1):
        x=sign*width/2
        m.prism([(x,-depth/2,.80),(x,depth/2,.80),(x,depth/2,3.20),(x,-depth/2,2.95)],(-sign,0,0),.10,'Siding',color)
    for xx in (-width*.355,width*.355):m.box((xx,-depth/2,1.85),(width*.29,.10,2.1),'Siding',color)
    m.box((0,-depth/2,1.12),(width*.42,.10,.64),'Siding',color);m.box((0,-depth/2,2.73),(width*.42,.10,.34),'Siding',color)
    m.box((0,-depth/2,2.925),(width,.10,.05),'Siding',color)
    # Two hung aluminum sashes: recessed backing, perimeter returns, meeting
    # rails and a projecting sill. The room is independently supported, with
    # removable skirt panels hiding its piers as on an occupied addition.
    ww=width*.42
    m.box((0,-depth/2+.18,2.05),(ww,.018,1.20),'Trim',(.025,.026,.022))
    m.box((0,-depth/2-.006,2.05),(ww,.005,1.20),'Glass')
    for x in (-ww/2,0,ww/2):m.box((x,-depth/2-.027,2.05),(.036,.048,1.24),'Trim',ZINC)
    for z in (1.45,2.05,2.65):m.box((0,-depth/2-.033,z),(ww+.07,.052,.032),'Trim',ZINC)
    m.box((0,-depth/2-.05,1.424),(ww+.13,.12,.025),'Trim')
    for j in range(9):m.box((0,-depth/2+.025,2.60-j*.04),(ww-.07,.020,.013),'Trim',(.43,.42,.35))
    for x in (-width/2,width/2):m.box((x,-depth/2-.016,1.86),(.05,.035,2.13),'Trim')
    for j in range(math.ceil(width/.2032)):
        x=-width/2+(j+.5)*width/math.ceil(width/.2032)
        m.box((x,-depth/2,.43),(width/math.ceil(width/.2032)-.008,.022,.70),'Trim',(.43,.44,.37))
    for sx in (-1,1):
        m.box((sx*width/2,0,.43),(.022,depth,.70),'Trim',(.43,.44,.37))
    m.box((0,-depth/2-.018,.81),(width+.05,.045,.05),'Trim')
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
