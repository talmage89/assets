"""Original cafe stock, construction first. Units meters, individual origins at grade."""
import math
import random
from geometry import Batch,root,socket


def bent_stock(points,tangent=.045):
    """Die-bent stock with rounded tangent transitions, straight between bends."""
    points=[Vector(p) for p in points];out=[points[0]]
    for a,p,c in zip(points,points[1:],points[2:]):
        d=min(tangent,(p-a).length*.30,(c-p).length*.30);u=p-(p-a).normalized()*d;v=p+(c-p).normalized()*d
        out.extend((1-t)**2*u+2*(1-t)*t*p+t*t*v for t in (0,.25,.5,.75,1))
    out.append(points[-1]);return out


def chair(name='BistroChair',parent=None):
    r=root(name,parent=parent,piece='BistroChair');b=Batch(name+'__SteelConstruction',r)
    # 22 mm bent round stock; swept rear legs rise to the back rim.
    for s in (-1,1):
        b.tube(bent_stock([(s*.238,-.268,.012),(s*.218,-.213,.34),(s*.216,-.196,.48),(s*.245,-.12,.645),(s*.248,.10,.66),(s*.208,.221,.59)]),.011,sides=10)
        b.tube([(s*.255,.292,.012),(s*.210,.215,.40),(s*.206,.218,.58),(s*.219,.270,.77)],.011,sides=8)
        for y in (-.268,.292):b.cylinder((s*(.238 if y<0 else .255),y,.008),.014,.016,'rubber',8)
    # Curved welded pan edging and crowned woven/expanded steel ribbons.
    edge=[(x,y,.445+.018*(1-(x/.224)**2)) for x,y in __import__('kit.model',fromlist=['rounded_rectangle']).rounded_rectangle(.448,.448,.065,4)]
    b.tube(edge+[edge[0]],.009,sides=6)
    # A continuous crowned sheet with fine cutout coverage meets its rolled
    # frame. This avoids the previous oversized, unsupported wire lattice.
    from geometry import LAYOUT
    def patch(rows):
        n=len(rows[0]);m=len(rows);a,bb,c,d=LAYOUT['mesh']
        for j in range(m-1):
            for k in range(n-1):
                uv=[(a+(c-a)*u/(n-1),bb+(d-bb)*v/(m-1)) for u,v in ((k,j),(k+1,j),(k+1,j+1),(k,j+1))]
                b.geom([rows[v][u] for u,v in ((k,j),(k+1,j),(k+1,j+1),(k,j+1))],[(0,1,2,3)],'mesh',uv,smooth=True)
    rows=[]
    for j in range(9):
        y=-.211+j*.422/8;half=.216-.018*(abs(y)/.211)**7
        rows.append([(x:=(-half+k*2*half/8),y,.446+.017*(1-(x/.225)**2)-.018*(y/.23)**2) for k in range(9)])
    patch(rows)
    rim=[(.23*math.cos(a),.255+.040*math.sin(a),.655+.17*math.sin(a)) for a in [j*math.pi/16 for j in range(17)]]
    b.tube(rim,.011,sides=8)
    b.tube([(-.21,.235,.49),(0,.270,.48),(.21,.235,.49)],.009,sides=6)
    rows=[]
    for j in range(9):
        t=j/8
        row=[]
        for k in range(9):
            x=-.209+k*.418/8;f=abs(x)/.21;top=math.sqrt(max(0,1-(x/.23)**2));bottomy=.270-.035*f;bottomz=.480+.010*f
            row.append((x,bottomy*(1-t)+(.255+.040*top)*t,bottomz*(1-t)+(.655+.170*top)*t))
        rows.append(row)
    patch(rows)
    for k in (0,8):b.tube([row[k] for row in rows],.006,sides=6)
    for y in (-.19,.20):b.tube([(-.21,y,.41),(.21,y,.41)],.008,sides=6)
    b.finish();socket(name+'__Seat',(0,0,.4572),r,'seated_person',facing='-Y',clearance_radius_m=.30)
    return r


def table(name='BistroTable',accessible=False,parent=None,umbrella=False):
    r=root(name,parent=parent,piece='AccessibleTable' if accessible else 'UmbrellaTable' if umbrella else 'BistroTable');b=Batch(name+'__Construction',r)
    if accessible:
        # Four corner legs, no apron on the approach edge; .782m clear width.
        b.rounded((0,0,.747),(.9144,.9144,.030),.014,'oak')
        for x in (-.416,.416):
            for y in (-.416,.416):
                b.box((x,y,.364),(.032,.032,.728));b.box((x,y,.010),(.045,.045,.020),'rubber')
        b.box((0,.40,.710),(.80,.025,.026));b.box((0,-.40,.710),(.80,.025,.026))
        # X-facing approach has .700m unobstructed height and .76m width.
        socket(name+'__Wheelchair',(-.584,0,0),r,'accessible_forward_approach',clear_floor_m=[.762,1.2192],knee_width_m=.762,knee_height_m=.6858)
    else:
        # Cast perimeter and open diagonal lattice. No wasted hidden disk.
        b.lathe([(.720,.335),(.720,.3556),(.737,.3556),(.742,.348),(.742,.335),(.720,.335)],n=48)
        for s in (-1,1):
            for i in range(-7,8):
                c=i*.045;# y=s*x+c, clipped to circle
                disc=2*.331**2-c*c
                if disc<=0:continue
                lo=(-s*c-math.sqrt(disc))/2;hi=(-s*c+math.sqrt(disc))/2
                intervals=[(lo,hi)]
                if umbrella and abs(c)/math.sqrt(2)<.034:
                    rootdisc=math.sqrt(max(0,2*.034**2-c*c));aa=(-s*c-rootdisc)/2;bb=(-s*c+rootdisc)/2;intervals=[(lo,aa),(bb,hi)]
                for aa,bb in intervals:b.beam((aa,s*aa+c,.731),(bb,s*bb+c,.731),.008,.006)
        if umbrella:
            for sx in (-1,1):
                for sy in (-1,1):
                    b.tube([(sx*.28,sy*.28,.013),(sx*.23,sy*.23,.65),(sx*.21,sy*.21,.717)],.013,sides=8)
                    b.cylinder((sx*.28,sy*.28,.012),.019,.024,'rubber',8)
                b.beam((-.23,sx*.23,.70),(.23,sx*.23,.70),.023,.018)
            b.lathe([(.69,.026),(.69,.045),(.735,.045),(.735,.026),(.69,.026)],n=20)
        else:
            b.lathe([(.056,.08),(.085,.053),(.69,.037),(.712,.09),(.72,.105)],n=16)
            for j in range(3):
                a=j*math.tau/3;pts=[(.04*math.cos(a),.04*math.sin(a),.11),(.17*math.cos(a),.17*math.sin(a),.035),(.30*math.cos(a),.30*math.sin(a),.018)]
                b.tube(pts,.017,sides=8);b.cylinder((.30*math.cos(a),.30*math.sin(a),.012),.025,.024,'rubber',8)
            for j in range(3):
                a=j*math.tau/3;b.beam((0,0,.66),(.22*math.cos(a),.22*math.sin(a),.717),.022,.018)
    b.finish();socket(name+'__Top',(0,0,.762 if accessible else .742),r,'table_setting');return r


def cup(b,x,y,z):
    b.lathe([(z,.027),(z+.004,.029),(z+.108,.043),(z+.112,.043),(z+.112,.040),(z+.104,.039),(z+.009,.025)],'white',16,center=(x,y))
    b.lathe([(z+.032,.031),(z+.078,.037)],'wood',16,center=(x,y))
    b.lathe([(z+.111,.046),(z+.117,.046),(z+.121,.038),(z+.124,.038)],'black',16,center=(x,y))


def setting(name='TableSetting',kind='cup',seed=1,parent=None):
    r=root(name,parent=parent,piece='TableSetting');b=Batch(name+'__Objects',r);rng=random.Random(seed)
    cup(b,-.20,-.11,0)
    if kind=='laptop':
        b.rounded((.035,-.075,.010),(.30,.21,.018),.007,'steel',2)
        b.box((.035,-.085,.021),(.258,.12,.002),'black')
        for j in range(4):
            for k in range(9):b.box((-.075+k*.026,-.134+j*.025,.023),(.018,.017,.002),'cream')
        b.beam((-.115,.020,.02),(-.115,.075,.20),.012,.012,'steel');b.beam((.185,.020,.02),(.185,.075,.20),.012,.012,'steel')
        b.geom([(-.11,.019,.020),(.18,.019,.020),(.18,.075,.20),(-.11,.075,.20)],[(0,1,2,3)],'black')
    elif kind=='paper':
        b.print([(-.18,-.18,.003),(.12,-.18,.003),(.12,.045,.007),(-.18,.045,.007)],'news')
        b.box((-.03,-.07,.001),(.301,.223,.002),'cream')
    else:
        b.cylinder((.10,-.10,.008),.074,.008,'white',24)
        b.rounded((.10,-.10,.026),(.095,.059,.035),.015,'pastry',3)
    b.finish();return r


def counter(name='Counter',length=3.65,parent=None):
    r=root(name,parent=parent,piece='Counter');b=Batch(name+'__Joinery',r)
    b.box((0,0,.045),(length-.06,.58,.09),'black');b.box((0,0,.51),(length,.64,.98),'wood');b.box((0,-.34,.08),(length,.035,.12),'black')
    b.rounded((0,0,1.025),(length+.08,.78,.055),.014,'cream')
    for j in range(max(3,round(length/.7))):
        x=-length/2+(j+.5)*length/max(3,round(length/.7));b.box((x,-.325,.54),(length/max(3,round(length/.7))-.035,.025,.78),'oak')
    b.box((0,.29,.57),(length,.035,.82),'black');b.finish();return r


def espresso(name='EspressoMachine',parent=None):
    r=root(name,parent=parent,piece='EspressoMachine');b=Batch(name+'__FoldedSteelAndGroups',r)
    # Legacy Linea-class envelope .711 x .559 x .533; original two-group design.
    for x in (-.26,.26):
        for y in (-.19,.19):b.cylinder((x,y,.027),.019,.054,'rubber',10)
    b.rounded((0,.06,.25),(.7112,.43,.395),.018,'steel',3)
    b.box((0,-.159,.235),(.65,.018,.205),'black');b.box((0,-.246,.065),(.68,.133,.022),'steel')
    b.box((0,.06,.468),(.72,.45,.025),'steel')
    for x in (-.34,.34):b.tube([(x,-.13,.485),(x,-.13,.533),(x,.25,.533)],.006,'steel',6)
    for x in (-.155,.155):
        b.rounded((x,-.182,.339),(.18,.045,.055),.009,'black',2)
        for dx in (-.045,0,.045):b.cylinder((x+dx,-.208,.342),.008,.008,'cream',8)
        b.tube([(x,-.17,.265),(x,-.255,.262)],.044,'steel',16)
        b.tube([(x,-.255,.247),(x+.015,-.34,.22)],.014,'black',8)
        b.tube([(x,-.235,.221),(x,-.235,.178)],.007,'steel',6)
    for s in (-1,1):
        b.tube([(s*.29,-.18,.30),(s*.34,-.24,.28),(s*.34,-.30,.15),(s*.31,-.33,.12)],.005,'steel',6)
        b.tube([(s*.29,-.18,.36),(s*.29,-.22,.36)],.022,'black',10)
    for x in (-.24,0,.24):
        for y in (0,.14):
            b.lathe([(.486,.023),(.520,.030),(.525,.026),(.49,.020)],'white',10,center=(x,y))
    for j in range(13):b.box((-.30+j*.05,-.25,.078),(.004,.105,.004),'black')
    b.finish();return r


def grinder(name='Grinder',parent=None):
    r=root(name,parent=parent,piece='Grinder');b=Batch(name+'__CastingAndHopper',r)
    b.rounded((0,0,.025),(.235,.30,.05),.02,'black',3)
    b.lathe([(.05,.070),(.08,.085),(.25,.075),(.28,.063),(.32,.08)],'steel',16)
    b.lathe([(.32,.055),(.36,.055),(.45,.104),(.56,.10),(.58,.095)],'glass',16)
    b.lathe([(.355,.052),(.445,.096),(.51,.094)],'coffee',16)
    b.cylinder((0,0,.589),.106,.018,'black',16)
    b.lathe([(.15,.055),(.29,.055)],'steel',14,center=(0,-.09));b.box((0,-.16,.11),(.10,.07,.012),'steel')
    b.tube([(0,-.075,.26),(0,-.17,.24)],.018,'black',8);b.finish();return r


def brewer(name='Brewer',parent=None):
    r=root(name,parent=parent,piece='Brewer');b=Batch(name+'__SheetAndDecanter',r)
    b.rounded((0,0,.018),(.2134,.4775,.036),.009,'steel',2)
    b.box((0,.13,.23),(.20,.18,.43),'steel');b.rounded((0,-.08,.40),(.2134,.28,.078),.01,'steel',2)
    b.lathe([(.035,.065),(.046,.075),(.12,.077),(.18,.055),(.20,.035)],'glass',16,center=(0,-.135))
    b.lathe([(.039,.063),(.11,.074)],'coffee',16,center=(0,-.135))
    b.tube([(.034,-.135,.186),(.103,-.135,.171),(.10,-.135,.08),(.065,-.135,.065)],.008,'black',8)
    b.lathe([(.30,.046),(.34,.065),(.365,.066)],'black',16,center=(0,-.135));b.finish();return r


def pastry(name='PastryCase',parent=None):
    r=root(name,parent=parent,piece='PastryCase');b=Batch(name+'__Case',r)
    b.rounded((0,0,.39),(1.10,.68,.78),.018,'wood',3)
    # Actual curved front glass on narrow aluminum end frames, open display volume.
    for s in (-1,1):
        pts=[(s*.544,-.36+.24*(1-math.cos(t*math.pi/2)),.81+.57*math.sin(t*math.pi/2)) for t in [j/8 for j in range(9)]]
        b.tube(pts,.012,'steel',6);b.box((s*.548,.31,1.1),(.022,.025,.60),'steel')
        poly=[(s*.54,-.34,.80),(s*.54,.31,.80),(s*.54,.31,1.37)]+pts[::-1];b.geom(poly,[tuple(range(len(poly)))],'glass')
    for j in range(8):
        t0=j/8;t1=(j+1)/8
        b.geom([(-.53,-.36+.24*(1-math.cos(t0*math.pi/2)),.81+.57*math.sin(t0*math.pi/2)),(.53,-.36+.24*(1-math.cos(t0*math.pi/2)),.81+.57*math.sin(t0*math.pi/2)),(.53,-.36+.24*(1-math.cos(t1*math.pi/2)),.81+.57*math.sin(t1*math.pi/2)),(-.53,-.36+.24*(1-math.cos(t1*math.pi/2)),.81+.57*math.sin(t1*math.pi/2))],[(0,1,2,3)],'glass',smooth=True)
    b.box((0,.10,1.39),(1.12,.46,.035),'steel')
    for z in (.80,1.02,1.24):
        b.box((0,.02,z),(1.03,.46,.012),'steel')
        for j in range(5):b.rounded((-.40+j*.20,.0,z+.027),(.13,.10,.045),.018,'pastry',2)
    b.finish();return r


def armchair(name='SoftChair',parent=None):
    r=root(name,parent=parent,piece='SoftChair');b=Batch(name+'__Upholstery',r)
    for x in (-.30,.30):
        for y in (-.29,.29):b.box((x,y,.055),(.045,.045,.11),'wood')
    b.rounded((0,0,.25),(.76,.77,.30),.055,'wine',4);b.rounded((0,-.02,.445),(.54,.57,.14),.055,'wine',4)
    for x in (-.33,.33):b.rounded((x,.0,.50),(.15,.76,.43),.065,'wine',4)
    b.rounded((0,.30,.64),(.64,.19,.58),.075,'wine',4);b.finish();return r


def aframe(name='AFrame',parent=None):
    r=root(name,parent=parent,piece='AFrame');b=Batch(name+'__HingedBoards',r)
    for s in (-1,1):
        for x in (-.29,.29):b.beam((x,s*.30,.018),(x,s*.025,1.03),.045,.035,'oak')
        for z in (.14,.92):b.beam((-.31,s*(.30-.275*z/1.03),z),(.31,s*(.30-.275*z/1.03),z),.045,.035,'oak')
        verts=[(-.26,s*.255,.18),(.26,s*.255,.18),(.26,s*.046,.91),(-.26,s*.046,.91)]
        b.print(verts if s<0 else list(reversed(verts)),'chalk')
    for x in (-.29,.29):b.tube([(x,-.025,.99),(x,.025,.99)],.013,'steel',8)
    for x in (-.29,.29):b.tube([(x,-.16,.51),(x,0,.45),(x,.16,.51)],.004,'steel',6)
    b.finish();return r


def planter(name='Planter',seed=1,parent=None):
    r=root(name,parent=parent,piece='Planter');b=Batch(name+'__PotAndPlant',r);rng=random.Random(seed)
    b.lathe([(.015,.22),(.04,.23),(.49,.29),(.53,.29),(.53,.265),(.475,.261)],'rust',20)
    b.cylinder((0,0,.47),.26,.01,'soil',20)
    for j in range(18):
        a=rng.random()*math.tau;rad=rng.uniform(.04,.14);h=rng.uniform(.17,.42)
        p=(rad*math.cos(a),rad*math.sin(a),.50+h)
        b.tube([(0,0,.48),p],.003,'leaf',5)
        for s in (-1,1):
            v=Vector(p);u=Vector((math.cos(a+s*.7),math.sin(a+s*.7),-.2))*.10
            b.geom([v,v+u+Vector((-.02,.02,0)),v+u*1.7,v+u+Vector((.02,-.02,0))],[(0,1,2,3)],'leaf')
    b.finish();return r


from mathutils import Vector
