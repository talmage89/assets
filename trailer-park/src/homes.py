"""Original permanent-chassis exterior shells, built from measured sections."""
import math,random
from geometry import Assembly,place,label

STEEL=(.045,.049,.043)
ZINC=(.43,.45,.43)


def chassis(a,p):
    L,W=p['length'],p['width'];m=a.mesh('Chassis',component='chassis');rails=[]
    for section in range(2 if p['double'] else 1):
        cy=(section-.5)*W/2 if p['double'] else 0
        for y in (cy-.94,cy+.94):
            rails.append(y)
            # 254 mm rolled I section: two flanges and a real web.
            for z in (.600,.842):m.box((0,y,z),(L-.30,.115,.012),'Trim',STEEL)
            m.box((0,y,.721),(L-.30,.006,.230),'Trim',STEEL)
        for j in range(math.ceil((L-.6)/2.4)+1):
            x=-L/2+.3+j*(L-.6)/math.ceil((L-.6)/2.4)
            m.box((x,cy,.78),(.055,W/(2 if p['double'] else 1)-.16,.09),'Trim',STEEL)
    # Piers bear on visible concrete pads; nominal 8x8x16 CMU with vertical
    # open cells, closed by the cap. Rails run X; blocks' long direction Y.
    n=math.ceil((L-1.0)/2.4384)
    for y in rails:
        for j in range(n+1):
            x=-L/2+.5+j*(L-1)/n
            m.box((x,y,.05),(.61,.61,.10),'Concrete',(.25,.24,.21))
            for z in (.197,.391):
                # Two side webs, three transverse webs; no solid fake cubes.
                for dx in (-.082,.082):m.box((x+dx,y,z),(.031,.390,.194),'Concrete')
                for dy in (-.178,0,.178):m.box((x,y+dy,z),(.133,.034,.194),'Concrete')
            m.box((x,y,.528),(.2032,.4064,.08),'Concrete',(.30,.29,.26))
            m.box((x,y,.581),(.14,.25,.026),'Veneer',(.27,.21,.12))
    # Floor joists and the black underbelly sit above the main chassis.
    m.box((0,0,.872),(L,W,.044),'Trim',(.055,.052,.044))
    m.box((0,0,.904),(L,W,.020),'Veneer',(.24,.19,.12))
    # 1-1/4 in straps terminate at exposed tensioning heads just above grade.
    for sx in (-1,1):
        for x in (-L/2+1,L/2-1):
            y=sx*(W/2-.16);q=(x,sx*(W/2+.20),.09)
            m.beam((x,y,.77),q,.03175,.0009,'Trim',ZINC,r=0)
            m.tube([(q[0],q[1],.02),(q[0],q[1],.14)],.014,'Trim',STEEL,8)
            m.box((q[0],q[1],.115),(.09,.055,.028),'Trim',ZINC)
    if p['double']:
        # Marriage-line supports at end walls and the large central opening.
        for x in (-L/2+.30,-2.2,2.2,L/2-.30):
            m.box((x,0,.05),(.61,.61,.1),'Concrete')
            for z in (.20,.40):m.box((x,0,z),(.39,.20,.20),'Concrete')
            m.box((x,0,.55),(.4064,.2032,.10),'Concrete')
            m.box((x,0,.73),(.13,.20,.26),'Veneer',(.25,.20,.13))
    return m.finish()


def openings(p,face):
    L,W=p['length'],p['width'];F=p['floor'];double=p['double']
    if face in ('front','back'):
        positions=[-L*.38,-L*.19,L*.13,L*.35]
        out=[dict(u=x,w=1.22 if double else .92,z=F+.94,h=.96,kind='window') for x in positions]
        if face=='back':
            out[1].update(w=.61,h=.46,z=F+1.30)
            out.append(dict(u=L*.26,w=.76,z=F,h=1.93,kind='door'))
        else:out.append(dict(u=-L*.035,w=.813 if not double else .9144,z=F,h=1.98 if not double else 2.032,kind='door'))
        return out
    return [dict(u=(-W*.20 if double else 0),w=1.52 if double else 1.22,z=F+.92,h=1.04,kind='window')]


def wall(a,p,face):
    L,W=p['length'],p['width'];F,E=p['floor'],p['eave'];holes=openings(p,face)
    along=face in ('front','back');length=L if along else W;sign=-1 if face in ('front','left') else 1
    def xf(v):
        u,d,z=v
        return (u,sign*(W/2+d),z) if along else (sign*(L/2+d),u,z)
    m=a.mesh('Wall_'+face,component='wall');tr=a.mesh('Opening_'+face,component='openings')
    us=sorted({-length/2,length/2,*[v for h in holes for v in (h['u']-h['w']/2,h['u']+h['w']/2)]})
    zs=sorted({F,E,*[v for h in holes for v in (h['z'],h['z']+h['h'])]})
    for u0,u1 in zip(us,us[1:]):
        for z0,z1 in zip(zs,zs[1:]):
            if any(h['u']-h['w']/2<(u0+u1)/2<h['u']+h['w']/2 and h['z']<(z0+z1)/2<h['z']+h['h'] for h in holes):continue
            m.box(((u0+u1)/2,-.052,(z0+z1)/2),(u1-u0,.104,z1-z0),'Siding',xf=xf)
    def allowed(u,z):return not any(abs(u-h['u'])<h['w']/2+.006 and h['z']-.006<z<h['z']+h['h']+.006 for h in holes)
    # Sheet ribs/courses have physical relief at this form gate. Fine grooves
    # and fasteners will move to the shared normal sheet during look-dev.
    if p['siding']=='ribbed':
        for i in range(math.ceil(length/.2032)):
            u=-length/2+(i+.5)*length/math.ceil(length/.2032)
            for z0,z1 in zip(zs,zs[1:]):
                if allowed(u,(z0+z1)/2):m.box((u,.006,(z0+z1)/2),(.019,.012,z1-z0),'Siding',xf=xf)
    else:
        count=math.ceil((E-F)/.2032)
        for j in range(count):
            z=F+j*(E-F)/count+.012
            for u0,u1 in zip(us,us[1:]):
                if allowed((u0+u1)/2,z):m.box(((u0+u1)/2,.006,z),(u1-u0,.014,.022),'Siding',xf=xf)
    for h in holes:
        u,w,z,ht=h['u'],h['w'],h['z'],h['h']
        # Real jamb depth, sill, head drip and 25 mm corner/J trim.
        for uu in (u-w/2-.022,u+w/2+.022):tr.box((uu,.014,z+ht/2),(.044,.038,ht+.088),'Trim',xf=xf)
        for zz in (z-.022,z+ht+.022):tr.box((u,.018,zz),(w+.088,.046,.044),'Trim',xf=xf)
        tr.box((u,.045,z+ht+.045),(w+.125,.10,.014),'Trim',xf=xf)
        if h['kind']=='door':
            name=face.title()+'Door';hinge=xf((u-w/2+.012,-.037,z+.006));pivot=a.pivot(name,hinge,(0,100) if face=='front' else (-100,0))
            leaf=a.mesh(name+'Leaf',part=pivot.name,component='door')
            leaf.box((u,-.020,z+ht/2),(w-.024,.040,ht-.012),'Trim',p['accent'],r=.002,xf=xf)
            # Door upper lite and lower pressed field remain attached to hinge.
            leaf.box((u,.003,z+ht*.73),(w*.55,.005,ht*.22),'Glass',xf=xf)
            leaf.box((u,.006,z+ht*.30),(w*.72,.008,ht*.32),'Trim',r=.002,xf=xf)
            leaf.box((u+w*.34,.042,z+.96),(.030,.060,.045),'Trim',ZINC,r=.002,xf=xf)
            leaf.finish()
            if face=='front':
                sp=a.pivot('StormDoor',xf((u-w/2+.012,.073,z+.006)),(-105,0))
                sm=a.mesh('StormDoorFrame',part=sp.name,component='storm_door')
                for uu in (u-w/2+.028,u+w/2-.028):sm.box((uu,.083,z+ht/2),(.032,.024,ht-.016),'Trim',ZINC,xf=xf)
                for zz in (z+.023,z+ht-.023,z+.80):sm.box((u,.083,zz),(w-.040,.024,.034),'Trim',ZINC,xf=xf)
                sm.box((u,.083,z+ht*.7),(w-.075,.004,ht*.46),'Glass',xf=xf)
                sm.box((u,.083,z+.39),(w-.075,.008,.73),'Trim',(.38,.40,.37),xf=xf);sm.finish()
                a.socket('OccupantThreshold',xf((u,.26,F)),'occupant');a.socket('DoorApproach',xf((u,.75,0)),'walk')
        else:
            # Recessed dark room, glass, two offset aluminum sashes and storm.
            tr.box((u,-.27,z+ht/2),(w-.025,.018,ht-.025),'Trim',(.025,.026,.022),xf=xf)
            tr.box((u,-.008,z+ht/2),(w-.03,.005,ht-.03),'Glass',xf=xf)
            for uu in (u-w/2+.020,u+w/2-.020):tr.box((uu,.006,z+ht/2),(.025,.024,ht),'Trim',ZINC,xf=xf)
            for zz in (z+.020,z+ht/2,z+ht-.020):tr.box((u,.008,zz),(w,.024,.026),'Trim',ZINC,xf=xf)
            for uu in (u-w/2+.047,u+w/2-.047):tr.box((uu,.026,z+ht/2),(.014,.012,ht-.04),'Trim',(.50,.52,.49),xf=xf)
            # Varied blind slats in an actual cavity, not a white window card.
            for j in range(6+p['seed']%7):
                zz=z+ht-.045-j*.045
                tr.box((u,-.05,zz),(w-.075,.024,.016),'Trim',(.48,.46,.39),xf=xf)
    m.finish();tr.finish()


def roof(a,p):
    L,W,E=p['length'],p['width'],p['eave'];m=a.mesh('Roof',component='roof');trim=a.mesh('EaveRake',component='roof_trim')
    half=W/2+.12;lx=L/2+.10
    def height(y):return E+.10+(.13*(1-(y/half)**2) if p['era']=='1972' else (half-abs(y))*p['pitch'])
    stations=[-half+i*2*half/12 for i in range(13)] if p['era']=='1972' else [-half,0,half]
    for y0,y1 in zip(stations,stations[1:]):
        m.prism([(-lx,y0,height(y0)),(lx,y0,height(y0)),(lx,y1,height(y1)),(-lx,y1,height(y1))],(0,0,-1),.055,'Shingles' if p['roof']=='shingle' else 'Trim',None if p['roof']=='shingle' else (.38,.39,.35))
    if p['roof']=='rolled':
        for j in range(math.ceil(L/.9144)):
            x=-L/2+j*L/math.ceil(L/.9144)
            m.tube([(x,y,height(y)+.005) for y in stations],.009,'Trim',(.24,.25,.22),6)
    else:
        m.box((0,0,height(0)+.018),(L+.22,.15,.045),'Shingles')
    for sy in (-1,1):
        trim.box((0,sy*half,height(half)-.048),(L+.22,.032,.120),'Trim')
        trim.box((0,sy*(half+.023),height(half)-.012),(L+.25,.055,.027),'Trim',ZINC)
    for sx in (-1,1):
        for y0,y1 in zip(stations,stations[1:]):trim.beam((sx*lx,y0,height(y0)-.04),(sx*lx,y1,height(y1)-.04),.027,.09,'Trim',r=0)
        if p['era']!='1972':
            trim.prism([(sx*(L/2+.002),-W/2,E),(sx*(L/2+.002),W/2,E),(sx*(L/2+.002),0,height(0)-.03)],(-sx,0,0),.06,'Siding')
    # Vented plumbing boots and furnace flue, at measured roof surface.
    for x,y,r,h in ((L*.27,.43,.045,.30),(-L*.28,.38,.075,.42)):
        z=height(y);trim.box((x,y,z+.007),(.27,.27,.020),'Trim',(.10,.11,.095))
        trim.tube([(x,y,z),(x,y,z+h)],r,'Trim',ZINC,12)
        trim.tube([(x,y,z+h),(x,y,z+h+.025)],r*1.45,'Trim',ZINC,12)
    if p['double']:
        # End joint under the common ridge makes the two transported sections
        # legible without inventing a second roof ridge.
        for sx in (-1,1):trim.box((sx*(L/2+.016),0,(p['floor']+height(0))/2),(.028,.045,height(0)-p['floor']),'Trim')
    m.finish();trim.finish()


def skirting(a,p):
    L,W=p['length'],p['width'];sk=Assembly(a.root.name+'__Skirting');sk.root.parent=a.root;sk.root['export_part']='removable_skirt_diagnostic'
    m=sk.mesh('Panels',component='skirting');height=.84
    for face in range(4):
        along=face<2;sign=-1 if face%2==0 else 1;length=L if along else W
        count=math.ceil(length/.4064)
        for j in range(count):
            u=-length/2+(j+.5)*length/count;w=length/count-.003
            # One intentional missing panel exposes real support construction.
            if p['missing_skirt'] and face==0 and j==count//2+3:continue
            vent=j%7==2 and along;z=.045+height/2
            xf=lambda v,along=along,sign=sign:(v[0],sign*(W/2+.005+v[1]),v[2]) if along else (sign*(L/2+.005+v[1]),v[0],v[2])
            if vent:
                m.box((u,0,.31),(w,.012,.53),'Trim',(.34,.33,.28),xf=xf)
                m.box((u,0,.80),(w,.012,.18),'Trim',(.34,.33,.28),xf=xf)
                m.box((u,-.012,.624),(w-.04,.009,.17),'Trim',(.030,.036,.027),xf=xf)
                for zz in (.57,.61,.65,.69):m.box((u,.008,zz),(w-.03,.022,.013),'Trim',xf=xf)
            else:m.box((u,0,z),(w,.012,height),'Trim',(.34,.33,.28) if p['era']=='1972' else (.43,.43,.37),xf=xf)
            for du in (-w*.36,0,w*.36):m.box((u+du,.010,z),(.012,.014,height),'Trim',(.39,.38,.32),xf=xf)
        for zz in (.042,.878):m.box((0,.012,zz),(length+.04,.035,.035),'Trim',xf=xf)
    # 18x24 inch access opening is cut into back skirt by removing two panels.
    # The overlapping lift-out frame is a removable diagnostic piece, not hinged.
    m.finish()
    return sk


def build(p,name='Home',support_only=False):
    a=Assembly(name,dict(Siding=p['color'],Trim=p['trim']));a.root['home_spec']=__import__('json').dumps(p,sort_keys=True)
    chassis(a,p)
    if not support_only:
        for f in ('front','back','left','right'):wall(a,p,f)
        roof(a,p);skirting(a,p)
        m=a.mesh('Corners',component='corners')
        for x in (-p['length']/2,p['length']/2):
            for y in (-p['width']/2,p['width']/2):m.box((x,y,(p['floor']+p['eave'])/2),(.05,.05,p['eave']-p['floor']),'Trim')
        m.finish()
        a.socket('FootprintMin',(-p['length']/2,-p['width']/2,0),'footprint');a.socket('FootprintMax',(p['length']/2,p['width']/2,0),'footprint')
        a.socket('Deck',(-p['length']*.035,-p['width']/2-.02,p['floor']-.025),'deck')
        label(a,str(p.get('lot_number',p['seed']%100)),(-p['length']*.035+ .69,-p['width']/2-.037,2.30),.11,p['accent'])
    return a
