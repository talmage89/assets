"""Operating doors, handrails and hung bell with actual pivot frames."""
import math,json
import geometry as G


def doors(name,parent,point=(0,0,0),yaw=0,modern=False):
    rt=G.root(name,point,parent,module_kind='DoorPair');rt.rotation_euler.z=math.radians(yaw)
    m=G.Mesh(name+'__Frame',rt,component='door_frame')
    for x in (-1.07,1.07):m.box((x,0,1.13),(.115,.24,2.26),'stone')
    for s in (-1,1):
        for z in (.295,1.105,1.905):
            m.box((s*1.07,-.115,z),(.115,.03,.16),'iron')
            for dz in (-.067,.067):m.box((s*1.0425,-.145,z+dz),(.09,.045,.020),'iron')
            m.tube([(s*1.005,-.155,z-.077),(s*1.005,-.155,z+.077)],.0075,'iron',12)
    m.box((0,0,2.26),(2.22,.24,.12),'stone');m.box((0,-.06,.025),(2.22,.36,.05),'stone');m.finish()
    for s in (-1,1):
        pivot=G.root('Door_Left' if s<0 else 'Door_Right',(s*1.005,-.155,.055),rt,
                     pivot_axis='Z',range_degrees=[-90,0] if s<0 else [0,90],moving=True)
        m=G.Mesh(pivot.name+'__Leaf',pivot,solid=True,door=True,component='door_leaf');cx=-s*.5065
        if modern:
            for xx in (cx-.457,cx+.457):m.box((xx,0,1.067),(.07,.062,2.1336),'iron')
            for z,h in ((.14,.28),(.98,.14),(2.085,.098)):m.box((cx,0,z),(.844,.062,h),'iron')
            for z,h in ((.595,.63),(1.555,.97)):m.box((cx,0,z),(.842,.006,h),'glass')
        else:m.box((cx,0,1.067),(.984,.062,2.1336),'timber')
        for z in (.39,1.22,1.88):
            m.box((cx,-.042,z),(.81,.038,.055),'iron' if modern else 'timber')
        if modern:
            m.box((cx,.049,1.0),(.80,.045,.05),'iron')
        else:
            for x in (-.25,.25):
                for z,h in ((.39,.46),(1.25,.97),(1.93,.18)):
                    m.box((cx+x,-.04,z),(.37,.024,h),'timber',(.68,.64,.57))
        # Exterior pull on standoffs; interior panic bar and closer body.
        xx=-s*.86
        m.tube([(xx,-.045,.91),(xx,-.12,.91),(xx,-.12,1.23),(xx,-.045,1.23)],.013,'bronze',8)
        m.box((cx,.065,1.01),(.76,.05,.055),'iron');m.box((-s*.22,.056,2.01),(.23,.08,.055),'iron')
        m.finish()
        m=G.Mesh(pivot.name+'__Sleeves',pivot,component='door_hinge')
        for z in (.24,1.05,1.85):m.lathe([(z-.055,.016),(z+.055,.016),(z+.055,.009),(z-.055,.009),(z-.055,.016)],'iron',12)
        m.finish()
    m=G.Mesh(name+'__Vestibule shadow',rt)
    m.box((0,.70,1.16),(2.06,.05,2.30),'black');m.box((0,.35,2.31),(2.06,.75,.05),'black');m.finish()
    return rt


def rail(name,parent,a,b,guard=False):
    rt=G.root(name,parent=parent,module_kind='RailRun');m=G.Mesh('Welded iron rail',rt)
    dist=math.dist(a,b);count=max(1,math.ceil(dist/1.5));height=.9144
    def at(t):return tuple(a[k]+t*(b[k]-a[k]) for k in range(3))
    for i in range(count+1):
        x,y,z=at(i/count);m.box((x,y,z+height/2),(.038,.038,height),'iron')
        m.box((x,y,z+.025),(.11,.11,.012),'iron')
    aa=at(0);bb=at(1);d=[(bb[k]-aa[k])/dist for k in range(3)]
    pts=[(aa[0]-.3048*d[0],aa[1]-.3048*d[1],aa[2]+height-.12),
         (aa[0]-.3048*d[0],aa[1]-.3048*d[1],aa[2]+height),
         (aa[0],aa[1],aa[2]+height),(bb[0],bb[1],bb[2]+height),
         (bb[0]+.3048*d[0],bb[1]+.3048*d[1],bb[2]+height),
         (bb[0]+.3048*d[0],bb[1]+.3048*d[1],bb[2]+height-.12)]
    m.tube(pts,.0212,'iron',8)
    if guard:
        n=math.ceil(dist/.125)
        for j in range(n+1):
            x,y,z=at(j/n);m.box((x,y,z+.48),(.015,.015,.80),'iron')
        m.beam((aa[0],aa[1],aa[2]+.10),(bb[0],bb[1],bb[2]+.10),.025,.025,'iron')
    m.finish();return rt


def bell(parent,point=(0,0,0)):
    rt=G.root('Bell',point,parent,pivot_axis='X',range_degrees=[-30,30],moving=True,module_kind='Bell')
    m=G.Mesh('Cast bell shell',rt)
    # Both shell faces, thickened sound bow and open mouth, not a solid cone.
    profile=[(-1.23,.57),(-1.19,.60),(-1.11,.54),(-1.03,.45),(-.84,.34),(-.55,.25),(-.38,.23),(-.28,.17),(-.28,.10),(-.38,.16),(-.55,.18),(-.84,.27),(-1.03,.38),(-1.11,.47),(-1.16,.51),(-1.23,.57)]
    m.lathe(profile,n=48);m.box((0,0,-.16),(.94,.20,.23),'timber');m.tube([(-1.15,0,0),(1.15,0,0)],.045,'iron',12)
    for x in (-.57,.57):m.box((x,0,-.05),(.12,.26,.22),'iron')
    m.tube([(0,0,-.41),(0,0,-1.12)],.024,'iron',10);m.lathe([(-1.18,.04),(-1.14,.09),(-1.07,.08),(-1.03,.03)],'iron',20)
    m.finish();m=G.Mesh('Bell wheel spokes and rim',rt)
    points=[(1.08,.62*math.sin(k*math.tau/48),.62*math.cos(k*math.tau/48)) for k in range(49)]
    m.tube(points,.023,'timber',8)
    for k in range(8):
        a=k*math.tau/8;m.beam((1.08,0,0),(1.08,.60*math.sin(a),.60*math.cos(a)),.035,.035,'timber')
    m.finish();return rt


def bearing(m,x,z,hung=False):
    rings=[]
    for u,r in ((-.09,.09),(.09,.09),(.09,.05),(-.09,.05),(-.09,.09)):
        rings.append([(x+u,r*math.cos(k*math.tau/16),z+r*math.sin(k*math.tau/16)) for k in range(16)])
    m.loft(rings,'iron',caps=False,smooth=True)
    if hung:
        for y in (-.10,.10):m.box((x,y,z+.47),(.16,.055,.94),'iron')
    else:m.box((x,0,z-.10),(.22,.26,.02),'iron')


def sign(parent,point,name,lines):
    rt=G.root('Changeable sign',point,parent,module_kind='Sign');m=G.Mesh('Sign case posts and tracks',rt)
    for x in (-1.26,1.26):m.box((x,0,1.01),(.13,.13,2.02),'iron')
    m.box((0,0,1.96),(3.20,.25,1.60),'iron');m.box((0,-.14,1.84),(3.04,.035,1.17),'stone',(1.3,1.28,1.16))
    for z in (1.43,1.68,1.93,2.18):m.box((0,-.17,z),(3.02,.027,.015),'iron')
    m.finish();layout=json.loads(__import__('pathlib').Path('build/letters.json').read_text())
    for row,text in enumerate(lines):
        for j,c in enumerate(text):
            if c==' ':continue
            x=(j-(len(text)-1)/2)*.137;z=2.06-row*.25
            letter=G.root(f'Letter_{row}_{j}_{c}',(x,-.185,z),rt,socket_kind='sign_letter',character=c,row=row,column=j)
            m=G.Mesh('Replaceable letter',letter,sheet=True);m.panel(0,0,0,.13,.225,'letters',layout[c]);m.finish()
    return rt
