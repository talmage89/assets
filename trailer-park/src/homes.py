"""Original permanent-chassis exterior shells, built from measured sections."""
import math,random
from geometry import Assembly,place,label
import era_details

STEEL=(.045,.049,.043)
ZINC=(.43,.45,.43)


def hinge(fixed,moving,xf,u,d,z):
    """Fixed pin/offset ears and a hollow moving sleeve with axial clearance."""
    x,y,zz=xf((u,d,z));sides=8;vs=[]
    for height,r in ((zz-.022,.005),(zz-.022,.007),(zz+.022,.007),(zz+.022,.005)):
        vs.extend([(x+r*math.cos(k*math.tau/sides),y+r*math.sin(k*math.tau/sides),height) for k in range(sides)])
    moving.geom(vs,[(j*sides+k,j*sides+(k+1)%sides,((j+1)%4)*sides+(k+1)%sides,((j+1)%4)*sides+k) for j in range(4) for k in range(sides)],'Trim',ZINC)
    fixed.tube([(x,y,zz-.040),(x,y,zz+.040)],.004,'Trim',ZINC,8)
    for dz in (-.031,.031):
        # Ears connect into the actual wall return, beyond the sleeve ends.
        fixed.beam(xf((u-.027,-.100 if d<0 else .025,z+dz)),xf((u-.006,d,z+dz)),.008,.010,'Trim',ZINC,r=0)


def chassis(a,p):
    L,W=p['length'],p['width'];m=a.mesh('Chassis',component='chassis');rails=[]
    # 19.05 mm deck over actual 2x6 floor joists, bearing on 254 mm I rails.
    joist_top=p['floor']-.01905;rail_top=joist_top-.1397;rail_bottom=rail_top-.254
    for section in range(2 if p['double'] else 1):
        cy=(section-.5)*W/2 if p['double'] else 0
        for y in (cy-.94,cy+.94):
            rails.append(y)
            # 254 mm rolled I section: two flanges and a real web.
            for z in (rail_bottom+.006,rail_top-.006):m.box((0,y,z),(L-.30,.115,.012),'Trim',STEEL)
            m.box((0,y,(rail_bottom+rail_top)/2),(L-.30,.006,.230),'Trim',STEEL)
        for j in range(math.ceil((L-.6)/2.4)+1):
            x=-L/2+.3+j*(L-.6)/math.ceil((L-.6)/2.4)
            m.box((x,cy,rail_top-.055),(.055,W/(2 if p['double'] else 1)-.16,.09),'Trim',STEEL)
    # Piers bear on visible concrete pads; nominal 8x8x16 CMU with vertical
    # open cells, closed by the cap. Rails run X; blocks' long direction Y.
    n=math.ceil((L-1.0)/2.4384)
    for y in rails:
        for j in range(n+1):
            x=-L/2+.5+j*(L-1)/n
            # Six-inch pad, 102.4 mm buried: its top is 50 mm above grade.
            m.box((x,y,-.0262),(.61,.61,.1524),'Concrete',(.25,.24,.21))
            for z in (.147,.341):
                # Two side webs, three transverse webs; no solid fake cubes.
                for dx in (-.082,.082):m.box((x+dx,y,z),(.031,.390,.194),'Concrete')
                for dy in (-.178,0,.178):m.box((x,y+dy,z),(.133,.034,.194),'Concrete')
            # Nominal 2 in hardwood cap (38.1 mm actual) and opposed wedges.
            m.box((x,y,.45705),(.2032,.4064,.0381),'Veneer',(.27,.21,.12))
            low=.4761;high=rail_bottom;mid0=low+.001;mid1=high-.001
            for poly in ([(-.07,low),(.07,low),(.07,mid1),(-.07,mid0)],
                         [(-.07,mid0),(.07,mid1),(.07,high),(-.07,high)]):
                m.prism([(x+xx,y-.125,z) for xx,z in poly],(0,1,0),.25,'Veneer',(.27,.21,.12))
    # Floor joists and the black underbelly sit above the main chassis.
    count=math.ceil((L-.15)/.4064)
    for j in range(count+1):
        x=-L/2+.075+j*(L-.15)/count
        m.box((x,0,(joist_top+rail_top)/2),(.0381,W-.02,.1397),'Veneer',(.24,.19,.12))
    m.box((0,0,rail_top-.001),(L,W,.002),'Trim',(.055,.052,.044))
    m.box((0,0,p['floor']-.01905/2),(L,W,.01905),'Veneer',(.24,.19,.12))
    # 1-1/4 in straps terminate at exposed tensioning heads just above grade.
    for sx in (-1,1):
        for x in (-L/2+1,L/2-1):
            rail_y=sx*((W/4 if p['double'] else 0)+.94)
            y=rail_y+sx*.009;q=(x,sx*(W/2-.20),.09)
            m.box((x,rail_y+sx*.006,rail_top-.04),(.062,.012,.042),'Trim',ZINC)
            m.beam((x,y,rail_top-.04),q,.03175,.0009,'Trim',ZINC,r=0)
            m.tube([(q[0],q[1],.02),(q[0],q[1],.14)],.014,'Trim',STEEL,8)
            m.box((q[0],q[1],.115),(.09,.055,.028),'Trim',ZINC)
    if p['double']:
        # Marriage-line supports at end walls and the large central opening.
        for x in (-L/2+.30,-2.2,2.2,L/2-.30):
            m.box((x,0,-.0262),(.61,.61,.1524),'Concrete')
            for z in (.147,.341,.535):m.box((x,0,z),(.39,.20,.194),'Concrete')
            m.box((x,0,.6828),(.4064,.2032,.1016),'Concrete')
            m.box((x,0,(.7336+rail_top)/2),(.25,.14,rail_top-.7336),'Veneer',(.25,.20,.13))
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
    if double:
        return [dict(u=s*W*.21,w=1.30,z=F+.83,h=1.16,kind='window') for s in (-1,1)]
    return [dict(u=0,w=W*.66,z=F+.77,h=1.31,kind='window')]


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
    # Fine ribs/lap relief belongs to the physical-scale baked tile. Keeping
    # thousands of hidden cube sides here spent triangles without silhouette.
    for h in holes:
        u,w,z,ht=h['u'],h['w'],h['z'],h['h']
        # Real jamb depth, sill, head drip and 25 mm corner/J trim.
        for uu in (u-w/2-.022,u+w/2+.022):tr.box((uu,.014,z+ht/2),(.044,.038,ht+.088),'Trim',xf=xf)
        for zz in (z-.022,z+ht+.022):tr.box((u,.018,zz),(w+.088,.046,.044),'Trim',xf=xf)
        tr.box((u,.045,z+ht+.045),(w+.125,.10,.014),'Trim',xf=xf)
        if h['kind']=='door':
            name=face.title()+'Door';pivot=a.pivot(name,xf((u-w/2+.002,-.126,z+.006)),(0,100) if face=='front' else (-100,0))
            leaf=a.mesh(name+'Leaf',part=pivot.name,component='door')
            leaf.box((u,-.104,z+ht/2),(w-.024,.040,ht-.012),'Trim',p['accent'],r=.002,xf=xf)
            # Door upper lite and lower pressed field remain attached to hinge.
            leaf.box((u,-.081,z+ht*.73),(w*.55,.005,ht*.22),'Glass',xf=xf)
            leaf.box((u,-.078,z+ht*.30),(w*.72,.008,ht*.32),'Trim',r=.002,xf=xf)
            leaf.box((u+w*.34,-.042,z+.96),(.030,.060,.045),'Trim',ZINC,r=.002,xf=xf)
            for hz in (z+.18,z+ht/2,z+ht-.18):
                hinge(tr,leaf,xf,u-w/2+.002,-.126,hz)
                leaf.box((u-w/2+.018,-.1095,hz),(.022,.027,.044),'Trim',ZINC,xf=xf)
            leaf.finish()
            if face=='front':
                sp=a.pivot('StormDoor',xf((u-w/2+.012,.103,z+.006)),(-105,0))
                sm=a.mesh('StormDoorFrame',part=sp.name,component='storm_door')
                for uu in (u-w/2+.028,u+w/2-.028):sm.box((uu,.083,z+ht/2),(.032,.024,ht-.016),'Trim',ZINC,xf=xf)
                for zz in (z+.023,z+ht-.023,z+.80):sm.box((u,.083,zz),(w-.040,.024,.034),'Trim',ZINC,xf=xf)
                sm.box((u,.083,z+ht*.7),(w-.075,.004,ht*.46),'Glass',xf=xf)
                sm.box((u,.083,z+.39),(w-.075,.008,.73),'Trim',(.38,.40,.37),xf=xf)
                for hz in (z+.18,z+ht/2,z+ht-.18):
                    hinge(tr,sm,xf,u-w/2+.012,.103,hz)
                    sm.box((u-w/2+.024,.093,hz),(.024,.010,.045),'Trim',ZINC,xf=xf)
                sm.finish()
                a.socket('OccupantThreshold',xf((u,.26,F)),'occupant');a.socket('DoorApproach',xf((u,.75,0)),'walk')
        else:
            era_details.window(a,p,face,h,xf)
            # Recessed dark room, glass, two offset aluminum sashes and storm.
            tr.box((u,-.27,z+ht/2),(w-.025,.018,ht-.025),'Trim',(.025,.026,.022),xf=xf)
            tr.box((u,.046,z+ht/2),(w-.03,.005,ht-.03),'Glass',xf=xf)
            for uu in (u-w/2+.020,u+w/2-.020):tr.box((uu,.006,z+ht/2),(.025,.024,ht),'Trim',ZINC,xf=xf)
            for zz in (z+.020,z+ht/2,z+ht-.020):tr.box((u,.008,zz),(w,.024,.026),'Trim',ZINC,xf=xf)
            for uu in (u-w/2+.047,u+w/2-.047):tr.box((uu,.026,z+ht/2),(.014,.012,ht-.04),'Trim',(.50,.52,.49),xf=xf)
            # Varied blind slats in an actual cavity, not a white window card.
            blind_step=.032+.005*((p['seed']+round(u*100)+sum(map(ord,face)))%5)
            for j in range(6+p['seed']%7):
                zz=z+ht-.045-j*blind_step
                tr.box((u,-.05,zz),(w-.075,.024,.016),'Trim',(.48,.46,.39),xf=xf)
    m.finish();tr.finish()


def roof(a,p):
    L,W,E=p['length'],p['width'],p['eave'];m=a.mesh('Roof',component='roof');trim=a.mesh('EaveRake',component='roof_trim')
    over=.254 if p['double'] else .20 if p['era']=='1984' else .12
    half=W/2+over;lx=L/2+over
    def height(y):return E+.10+(.13*(1-(y/half)**2) if p['era']=='1972' else (half-abs(y))*p['pitch'])
    stations=[-half+i*2*half/12 for i in range(13)] if p['era']=='1972' else [-half,0,half]
    coating={'kept':(.72,.73,.67),'faded':(.40,.41,.37),'patched':(.32,.33,.29)}[p['upkeep']]
    for y0,y1 in zip(stations,stations[1:]):
        m.prism([(-lx,y0,height(y0)),(lx,y0,height(y0)),(lx,y1,height(y1)),(-lx,y1,height(y1))],(0,0,-1),.055,'Shingles' if p['roof']=='shingle' else 'Trim',None if p['roof']=='shingle' else coating)
    if p['roof']=='rolled':
        for j in range(math.ceil(L/.9144)):
            x=-L/2+j*L/math.ceil(L/.9144)
            m.tube([(x,y,height(y)+.005) for y in stations],.009,'Trim',(.24,.25,.22),6)
    else:
        m.box((0,0,height(0)+.018),(L+.22,.15,.045),'Shingles')
    for sy in (-1,1):
        fascia=.24 if p['era']=='1984' else .12
        trim.box((0,sy*half,height(half)+.012-fascia/2),(L+2*over,.032,fascia),'Trim',p['accent'] if p['era']=='1984' else None)
        trim.box((0,sy*(half+.023),height(half)-.012),(L+.25,.055,.027),'Trim',ZINC)
    for sx in (-1,1):
        for y0,y1 in zip(stations,stations[1:]):trim.beam((sx*lx,y0,height(y0)-.04),(sx*lx,y1,height(y1)-.04),.027,.14 if p['era']=='1984' else .09,'Trim',p['accent'] if p['era']=='1984' else None,r=0)
        if p['era']=='1972':
            ys=[-W/2+i*W/12 for i in range(13)]
            poly=[(sx*(L/2+.002),-W/2,E),(sx*(L/2+.002),W/2,E)]
            poly.extend((sx*(L/2+.002),y,height(y)-.03) for y in reversed(ys))
            trim.prism(poly,(-sx,0,0),.06,'Siding')
        else:
            # Close to the actual roof underside at the wall stations. A
            # triangle ending at E left a daylight slit above each rake.
            trim.prism([(sx*(L/2+.002),-W/2,E),(sx*(L/2+.002),W/2,E),
                        (sx*(L/2+.002),W/2,height(W/2)-.025),
                        (sx*(L/2+.002),0,height(0)-.025),
                        (sx*(L/2+.002),-W/2,height(-W/2)-.025)],(-sx,0,0),.06,'Siding')
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
            # Interlocking panels overlap at their seams; open butt gaps
            # leaked sky through the chassis in the end-on turnaround.
            u=-length/2+(j+.5)*length/count;w=length/count+.001
            # One intentional missing panel exposes real support construction.
            if p['missing_skirt'] and face==0 and j==count//2+3:continue
            if p['missing_skirt'] and face in (2,3) and j==1:continue
            vent=j%7==2 and along;z=.045+height/2
            xf=lambda v,along=along,sign=sign:(v[0],sign*(W/2+.005+v[1]),v[2]) if along else (sign*(L/2+.005+v[1]),v[0],v[2])
            if p['era']=='1972' and p['seed']%4==0 and face==0 and j==count//3:
                base=xf;xf=lambda v,base=base:base((v[0],v[1]+.055*max(0,1-v[2]/.9),v[2]))
            if face==1 and j in (count//2-1,count//2):
                m.box((u,0,.160),(w,.012,.230),'Trim',(.34,.33,.28),xf=xf)
                continue
            if vent:
                m.box((u,0,.31),(w,.012,.53),'Trim',(.34,.33,.28),xf=xf)
                m.box((u,0,.80),(w,.012,.18),'Trim',(.34,.33,.28),xf=xf)
                m.box((u,-.012,.624),(w-.04,.009,.17),'Trim',(.030,.036,.027),xf=xf)
                for zz in (.57,.61,.65,.69):m.box((u,.008,zz),(w-.03,.022,.013),'Trim',xf=xf)
            elif p['era']=='1972' and p['seed']%2==0 and face==0 and j==count//4:
                # A brittle lower panel splits upward from a kicked/splashed
                # bottom edge. The opening exposes the real dark underfloor.
                poly=[(u-w/2,.045),(u-.04,.045),(u+.01,.31),(u+.02,.045),
                      (u+w/2,.045),(u+w/2,.885),(u-w/2,.885)]
                m.prism([xf((uu,0,zz)) for uu,zz in poly],(0,-sign,0) if along else (-sign,0,0),.012,'Trim',(.43,.43,.37))
            else:m.box((u,0,z),(w,.012,height),'Trim',(.34,.33,.28) if p['era']=='1972' else (.43,.43,.37),xf=xf)
            # Fluted panel relief is in the shared normal sheet.
        for zz in (.042,.878):m.box((0,.012,zz),(length+.04,.035,.035),'Trim',xf=xf)
    # Lift-out access covers a real 0.61 m high opening, wider than 18 in.
    # Its separate ownership allows a game to remove it for utility access.
    m.finish()
    count=math.ceil(L/.4064);cx=-L/2+(count//2)*L/count;cw=2*L/count
    access=Assembly(a.root.name+'__SkirtAccess');access.root.parent=sk.root;access.root['export_part']='lift_out_access'
    leaf=access.mesh('LiftOutPanel',component='skirt_access')
    leaf.box((cx,W/2+.028,.580),(cw+.024,.016,.610),'Trim',(.39,.39,.33))
    for xx in (cx-cw/2,cx+cw/2):leaf.box((xx,W/2+.045,.580),(.026,.020,.65),'Trim')
    leaf.box((cx,W/2+.055,.66),(.09,.035,.022),'Trim',ZINC);leaf.finish()
    return sk


def build(p,name='Home',support_only=False):
    a=Assembly(name,dict(Siding=p['color'],Trim=p['trim']));a.root['home_spec']=__import__('json').dumps(p,sort_keys=True)
    chassis(a,p)
    if not support_only:
        for f in ('front','back','left','right'):wall(a,p,f)
        roof(a,p);skirt=skirting(a,p);era_details.exterior(a,p);era_details.steps(a,p)
        from home_age import runoff
        runoff(a,p)
        from patina import home as weather_skin
        weather_skin(a,p,skirt.root)
        m=a.mesh('Corners',component='corners')
        for x in (-p['length']/2,p['length']/2):
            for y in (-p['width']/2,p['width']/2):m.box((x,y,(p['floor']+p['eave'])/2),(.05,.05,p['eave']-p['floor']),'Trim')
        m.finish()
        a.socket('FootprintMin',(-p['length']/2,-p['width']/2,0),'footprint');a.socket('FootprintMax',(p['length']/2,p['width']/2,0),'footprint')
        a.socket('Deck',(-p['length']*.035,-p['width']/2-.02,p['floor']-.025),'deck')
        if 'variant_id' not in p:label(a,str(p.get('lot_number',p['seed']%100)),(-p['length']*.035+ .69,-p['width']/2-.037,2.30),.11,p['accent'])
    return a
