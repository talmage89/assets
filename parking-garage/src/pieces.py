"""Construction modules. Fine hardware and service age belong to later maps."""
import math
from mathutils import Vector
from geometry import Mesh, root
from plan import TEE, SPAN, FLOOR


def door_pull(b):
    for z in (.94,1.20):b.box((.88,.04,z),(.035,.07,.035),'Steel')
    b.beam((.88,.075,.94),(.88,.075,1.20),.025,.025)


def tee(r):
    b=Mesh(r.name+'__Mesh',r)
    w=TEE-.020;h=.6096;fl=.1016
    # One continuous double-tee section: taper each prestressed web, preserve
    # the flange underside between stems. 50mm topping is a separate pour.
    x=w/2;s=TEE/4
    section=[(-x,-.05),(x,-.05),(x,-.05-fl),(s+.095,-.05-fl),(s+.060,-h-.05),
             (s-.060,-h-.05),(s-.095,-.05-fl),(-s+.095,-.05-fl),
             (-s+.060,-h-.05),(-s-.060,-h-.05),(-s-.095,-.05-fl),(-x,-.05-fl)]
    def stations(sec,ys,mat):
        n=len(sec);vs=[(x,y,z) for y in ys for x,z in sec]
        fs=[tuple(reversed(range(n))),tuple(range((len(ys)-1)*n,len(ys)*n))]
        fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(ys)-1) for i in range(n)]
        b.geom(vs,fs,mat)
    stations(section,[-SPAN/2+.22,0,SPAN/2-.22],'Concrete')
    stations([(-x,0),(x,0),(x,-.05),(-x,-.05)],[-SPAN/2+.03,0,SPAN/2-.03],'Deck')
    # Sealant along longitudinal flange joint, not a painted black outline.
    stations([(TEE/2-.011,-.010),(TEE/2+.011,-.010),(TEE/2+.011,.002),(TEE/2-.011,.002)],[-SPAN/2+.03,0,SPAN/2-.03],'Seal')
    # Bearing pads and real welded flange connector plates.
    for sy in (-1,1):
        for sx in (-1,1):b.box((sx*s,sy*(SPAN/2-.34),-h-.0625),(.24,.22,.025),'Seal')
    for y in (-6.1,0,6.1):b.box((x-.075,y,-.048),(.12,.10,.008),'Steel')
    b.finish()


def beam(r,edge=False):
    b=Mesh(r.name+'__Mesh',r);L=3*TEE-.82
    sec=[(-.16,-.12),(.16,-.12),(.16,-.685),(.46,-.685),(.46,-.80),(-.46,-.80),(-.46,-.685),(-.16,-.685)]
    if edge:sec=[(-.16,-.12),(.16,-.12),(.16,-.80),(-.46,-.80),(-.46,-.685),(-.16,-.685)]
    b.prism([(-L/2,y,z) for y,z in sec],(L,0,0));b.finish()


def column_body(r,height=FLOOR):
    b=Mesh(r.name+'__Mesh',r);w=.762;ch=.02
    sec=[(-w/2+ch,-w/2),(w/2-ch,-w/2),(w/2,-w/2+ch),(w/2,w/2-ch),
         (w/2-ch,w/2),(-w/2+ch,w/2),(-w/2,w/2-ch),(-w/2,-w/2+ch)]
    b.prism([(x,y,0) for x,y in sec],(0,0,height))
    # Paint is physically on the column, shallow surface film on lower 1.2m.
    for level in range(math.ceil(height/FLOOR)):
        h=min(1.2,height-level*FLOOR)
        if h>.03:b.box((0,-w/2-.001,level*FLOOR+h/2),(w-.06,.002,h),'Blue')
    return b


def corbel_parts(b):
    for sign in (-1,1):
        poly=[(sign*.37,-.38,FLOOR-1.60),(sign*.69,-.38,FLOOR-.97),(sign*.69,-.38,FLOOR-.825),(sign*.37,-.38,FLOOR-.825)]
        b.prism(poly,(0,.76,0));b.box((sign*.54,0,FLOOR-.8125),(.26,.50,.025),'Seal')


def column(r,corbels=True):
    b=column_body(r)
    if corbels:corbel_parts(b)
    b.finish()


def corbel_pair(r):
    b=Mesh(r.name+'__Mesh',r);corbel_parts(b);b.finish()


def spandrel(r,refined=False):
    b=Mesh(r.name+'__Mesh',r);L=3*TEE-.035
    # Cast panel: sloped cap, chamfered bottom arrises, recessed horizontal band.
    sec=[(-.13,-.34),(.13,-.34),(.13,.98),(.10,1.06),(-.10,1.08),(-.13,1.02)]
    if refined:sec=[(-.13,-.34),(.13,-.34),(.13,.15),(.122,.15),(.122,.17),(.13,.17),(.13,.98),(.10,1.06),(-.10,1.08),(-.13,1.02),(-.13,.17),(-.122,.17),(-.122,.15),(-.13,.15)]
    b.prism([(-L/2,y,z) for y,z in sec],(L,0,0))
    for x in (-L/2+.35,L/2-.35):
        b.box((x,.18,-.17),(.24,.16,.16),'Concrete');b.box((x,.175,-.07),(.16,.12,.018),'Steel')
    b.finish()


def cables(r):
    b=Mesh(r.name+'__Mesh',r);L=3*TEE-.025
    for x in (-L/2+.13,0,L/2-.13):
        b.box((x,0,.55),(.09,.09,1.1),'Steel');b.box((x,0,.018),(.20,.20,.036),'Steel')
    for z in (.28,.51,.74,.97):
        b.tube([(-L/2+.13,0,z),(0,0,z-.008),(L/2-.13,0,z)],.0095,'Steel')
    b.beam((-L/2,0,1.09),(L/2,0,1.09),.055,.055)
    b.finish()


def pt_guard(r):
    b=Mesh(r.name+'__Mesh',r);L=3*TEE-.025
    section=[(-.09,-.22),(.09,-.22),(.09,.54),(.07,.55),(-.07,.56),(-.09,.54)]
    b.prism([(-L/2,y,z) for y,z in section],(L,0,0))
    for x in (-L/2+.13,0,L/2-.13):
        b.box((x,0,.825),(.09,.09,.55),'Steel');b.box((x,0,.568),(.20,.20,.036),'Steel')
    for z in (.74,.97):b.tube([(-L/2+.13,0,z),(0,0,z-.008),(L/2-.13,0,z)],.0095,'Steel')
    b.beam((-L/2,0,1.09),(L/2,0,1.09),.055,.055);b.finish()


def ptdeck(r):
    b=Mesh(r.name+'__Mesh',r);w=TEE
    sec=[(-w/2,0),(w/2,0),(w/2,-.22),(-w/2,-.22)];ys=[-SPAN/2,0,SPAN/2]
    vs=[(x,y,z) for y in ys for x,z in sec]
    fs=[(3,2,1,0),(8,9,10,11)]+[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(2) for i in range(4)]
    b.geom(vs,fs,'Deck')
    # Formed slab edge: shallow recessed tendon anchor patches at beam ends.
    for side in (-1,1):
        for x in (-.9,-.3,.3,.9):b.box((x,side*(SPAN/2+.001),-.10),(.12,.004,.08),'Patch')
    b.finish()


def ptbeam(r):
    b=Mesh(r.name+'__Mesh',r)
    sec=[(-.34,-.21),(.34,-.21),(.34,-.25),(.305,-.25),(.305,-.76),(-.305,-.76),(-.305,-.25),(-.34,-.25)]
    n=len(sec);vs=[(x,y,z) for x in (-SPAN/2,0,SPAN/2) for y,z in sec]
    fs=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(2) for i in range(n)]
    b.geom(vs,fs);b.finish()


def fixture(r):
    b=Mesh(r.name+'__Mesh',r);b.box((0,0,-.045),(.12,1.24,.09),'Steel')
    b.box((0,0,-.096),(.10,1.16,.018),'Light')
    for y in (-.55,.55):b.box((0,y,-.11),(.135,.025,.04),'Steel')
    for x in (-.04,.04):b.tube([(x,-.45,0),(x,-.45,.40)],.0035,'Steel',6)
    b.finish();root(r.name+'__Emitter',(0,0,-.12),r,socket_kind='light_emitter')


def wheelstop(r):
    b=Mesh(r.name+'__Mesh',r);s=[(-.12,0),(.12,0),(.10,.105),(.06,.13),(-.06,.13),(-.10,.105)]
    b.prism([(-.9,y,z) for y,z in s],(1.8,0,0))
    for x in (-.65,.65):b.box((x,0,.132),(.04,.04,.004),'Steel')
    b.finish()


def drain(r):
    b=Mesh(r.name+'__Mesh',r);b.box((0,0,-.014),(.42,.42,.028),'Steel')
    for i in range(9):b.box((-.17+i*.042,0,.003),(.017,.35,.006),'Seal')
    b.finish()


def gate(r):
    b=Mesh(r.name+'__Housing',r);b.box((-.23,0,.47),(.46,.39,.94),'Yellow')
    b.box((-.23,0,.96),(.48,.42,.05),'Steel');b.tube([(0,-.23,.78),(0,.23,.78)],.07,'Steel',12);b.finish()
    pv=root(r.name+'__GateArm',(0,0,.78),r,pivot_axis='Y',range_degrees=[-90.,0.])
    c=Mesh(r.name+'__Arm',pv);c.box((1.57,0,0),(3.14,.075,.10),'White')
    for x in (.45,1.25,2.05,2.85):c.box((x,-.038,0),(.32,.002,.102),'Red')
    c.finish()


def ticket(r,pay=False):
    b=Mesh(r.name+'__Mesh',r);h=1.58 if pay else 1.18
    b.box((0,0,h/2),(.48,.40,h),'Blue');b.box((0,0,h+.025),(.51,.43,.05),'Steel')
    b.box((0,-.205,h-.28),(.32,.014,.22),'Seal');b.box((0,-.214,h-.28),(.26,.005,.15),'Glass')
    b.box((0,-.216,h-.52),(.22,.025,.028),'Steel');b.box((.14,-.22,h-.46),(.065,.04,.065),'Yellow')
    b.finish()


def tower(r,levels=4,elevator=True,refined=False):
    b=Mesh(r.name+'__Fabric',r);H=(levels-1)*FLOOR+3.0
    # 5.6 x 5.4m tower: two 1.30m concrete flights, 1.142m between
    # handrails, and full-depth landings. Rear faces the garage.
    if not refined:b.box((2.7,0,H/2),(.20,5.4,H))
    else:
        for yy in (-1.78,1.78):b.box((2.7,yy,H/2),(.20,1.84,H))
    # Ground exit pierces the stair's side at its lower landing; there is no
    # door trying to pass underneath the half-level return landing.
    if not refined:
        b.box((-2.7,0,(H+2.2)/2),(.20,5.4,H-2.2))
        b.box((-2.7,-.725,1.1),(.20,3.95,2.2))
    else:
        # A glazed return exposes the two flights to the public street. The
        # existing exit jamb, landing, stair widths and pivots stay in place.
        for yy in (-2.56,1.11):b.box((-2.7,yy,H/2),(.20,.28,H))
        b.box((-2.7,1.83,(H+2.2)/2),(.20,1.04,H-2.2))
    b.box((-2.7,2.545,1.1),(.20,.31,2.2))
    b.box((.25,0,H/2),(.20,5.4,H))
    b.box((1.50,-2.60,H/2),(2.40,.20,H))
    # Rear wall has actual 1.12m door apertures per level.
    for x,w in ((-2.355,.69),(-.57,.64),(.40,.30),(2.375,.65)):
        b.box((x,2.60,H/2),(w,.20,H))
    if refined:b.box((-.05,2.60,H/2),(.40,.20,H))
    for lev in range(levels):
        z=lev*FLOOR
        if refined:b.box((-1.45,2.68,z+2.195),(1.18,.10,.09),'Steel')
        head=min(FLOOR,H-z)
        b.box((1.30,2.60,z+(2.22+head)/2),(1.50,.20,head-2.22))
        b.box((-1.45,2.60,z+(2.20+head)/2),(1.12,.20,head-2.20))
        rear=1.28;front=rear-9*.2794
        b.box((-1.225,(rear+2.5)/2,z-.08),(2.75,2.5-rear,.16),'Deck')
        if lev<levels-1:b.box((-1.225,(-2.5+front)/2,z+FLOOR/2-.08),(2.75,front+2.5,.16),'Deck')
        # Ten risers / nine treads per half-level. A single sawtooth section
        # includes the sloping waist and terminal riser; no floating boxes.
        if lev<levels-1:
            rise=FLOOR/20;run=.2794
            for flight in (0,1):
                xx=-1.95 if flight==0 else -.53;direction=-1 if flight==0 else 1
                start=rear if flight==0 else front;base=z+flight*FLOOR/2
                section=[(start,base)]
                for i in range(9):
                    section.extend([(start+direction*i*run,base+(i+1)*rise),(start+direction*(i+1)*run,base+(i+1)*rise)])
                end=start+direction*9*run
                section.extend([(end,base+10*rise),(end+direction*.10,base+10*rise),(end+direction*.10,base+9*rise-.16),(start,base-.16)])
                b.prism([(xx-.65,yy,zz) for yy,zz in section],(1.30,0,0))
                a=(xx,start,base+rise+.90);c=(xx,end,base+10*rise+.90)
                for side in (-1,1):
                    aa=(a[0]+side*.59,a[1],a[2]);cc=(c[0]+side*.59,c[1],c[2]);b.tube([aa,cc],.019,'Steel')
                    for j in (0,3,6,9):
                        t=j/9;pt=Vector(aa).lerp(Vector(cc),t);b.tube([(pt.x,pt.y,base+(j+1)*rise-.025),pt],.015,'Steel')
        # Stair door at actual back-wall jamb. Outward swing into clear end bay.
        pv=root(f'{r.name}__StairDoor_L{lev+1}',(-2.00,2.715,z),r,pivot_axis='Z',range_degrees=[0.,95.])
        d=Mesh(pv.name+'__Leaf',pv)
        # Closed hollow plate around a real vision aperture. A glass patch
        # over an uncut solid leaf would never transmit the stair interior.
        outer=[(0,.025),(1.10,.025),(1.10,2.14),(0,2.14)]
        inner=[(.36,1.245),(.74,1.245),(.74,1.695),(.36,1.695)]
        vertices=[(x,y,zz) for y in (-.0225,.0225) for loop in (outer,inner) for x,zz in loop]
        faces=[]
        for j in range(4):
            k=(j+1)%4
            faces.extend([(j,k,k+4,j+4),(j+8,j+12,k+12,k+8),(j,j+8,k+8,k),(j+4,k+4,k+12,j+12)])
        d.geom(vertices,faces,'Blue');d.box((.55,0,1.47),(.38,.006,.45),'Glass')
        d.beam((.2,-.08,1.02),(.88,-.08,1.02),.025,.04)
        if refined:door_pull(d)
        d.finish()
        # Elevator doors slide in front of a recessed dark car opening.
        b.box((1.30,2.515,z+1.08),(1.50,.08,2.16),'Seal')
        for sign in (-1,1):
            pv=root(f'{r.name}__ElevatorDoor_L{lev+1}_{sign}',(1.30,2.78,z),r,slide_axis='X',range_m=[0.,sign*.72])
            d=Mesh(pv.name+'__Leaf',pv);d.box((sign*.355,0,1.0825),(.70,.035,2.115),'Steel');d.finish()
        b.box((1.30,2.81,z+2.22),(1.65,.14,.10),'Steel')
    # Glazed stair face, individually divided by floor and mullion.
    for lev in range(levels):
        z=lev*FLOOR
        b.box((-1.32,-2.675,z+1.5),(2.62,.025,2.98),'Glass')
        b.box((-1.32,-2.71,z+.08),(2.78,.07,.16),'Steel')
        if lev<levels-1:b.box((-1.32,-2.66,z+3.175),(2.62,.10,.37),'Steel' if refined else 'Blue')
        for x in (-2.61,-1.32,-.03):b.box((x,-2.71,z+1.5),(.06,.07,3.0),'Steel')
    b.box((0,0,H+.10),(5.8,5.6,.20));b.finish()
    # Hinge at the opposite jamb: the open leaf moves away from the garage
    # corner column when this core is placed on either end of the building.
    pv=root(r.name+'__StreetDoor',(-2.815,1.28,0),r,pivot_axis='Z',range_degrees=[0.,95.]);pv.rotation_euler.z=math.pi/2
    d=Mesh(pv.name+'__Leaf',pv);d.box((.55,0,1.0825),(1.10,.045,2.115),'Blue');d.beam((.2,-.08,1.02),(.88,-.08,1.02),.025,.04)
    if refined:door_pull(d)
    d.finish()
    root(r.name+'__StreetThreshold',(-2.85,1.83,0),r,socket_kind='pedestrian_threshold')
    root(r.name+'__GarageStairThreshold',(-1.45,2.85,0),r,socket_kind='pedestrian_threshold')
    root(r.name+'__GarageLiftThreshold',(1.30,2.85,0),r,socket_kind='accessible_threshold')
    if refined:
        from tower_detail import add
        add(r,levels,H)


def jobs(levels=4):
    return dict(DoubleTee=tee,InvertedT=beam,LBeam=lambda r:beam(r,True),ColumnCorbel=column,CorbelPair=corbel_pair,ColumnPlain=lambda r:column(r,False),
                PTColumn=lambda r:column(r,False),PTSlab=ptdeck,PTBeam=ptbeam,Spandrel=spandrel,
                CableBarrier=cables,PTGuard=pt_guard,Fixture=fixture,WheelStop=wheelstop,Drain=drain,Gate=gate,
                Ticket=ticket,PayStation=lambda r:ticket(r,True),Tower=lambda r:tower(r,levels))
