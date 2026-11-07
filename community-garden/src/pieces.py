"""Dressed lumber, hollow block, hand-built infrastructure and garden tools."""
import math,random
from mathutils import Vector
import geometry as Q

FT=.3048


def bed(name,w=1.2192,d=2.4384,h=.23495,edge='lumber',seed=10):
    rt=Q.root(name,'bed');rt['planting_envelope_m']=[w,d,h];rt['edge']=edge
    rng=random.Random(seed);wood='OldWood' if seed%2 else 'Wood'
    if edge in ('lumber','board'):
        thick=.0381 if edge=='lumber' else .01905
        if edge=='board':h=.1397
        # Butt-jointed boards fit between the full-length sides. Posts sit
        # inside, and the two lag heads enter them through each board end.
        for x in (-w/2+thick/2,w/2-thick/2):
            ob=Q.box('Full dressed side board',(x,0,h/2),(thick,d,h),rt,wood,.0015)
            # Sparse physically split cut ends are narrow wedges in geometry.
            for end in (-1,1):
                z=h*.68;yy=end*(d/2-.045)
                Q.mesh('Open end check',[(x-thick/2-.0002,yy,z-.001),(x-thick/2-.0002,yy-end*.17,z),(x-thick/2-.0002,yy,z+.002)],[(0,1,2)],rt,'Soil')
        for y in (-d/2+thick/2,d/2-thick/2):Q.box('Butted end board',(0,y,h/2),(w-2*thick,thick,h),rt,wood,.0015)
        if edge=='lumber':
            for x in (-w/2+thick+.04445,w/2-thick-.04445):
                for y in (-d/2+thick+.04445,d/2-thick-.04445):
                    Q.box('Internal 4x4 corner post',(x,y,(h+.025)/2),(.0889,.0889,h+.025),rt,'EndWood',.002)
                    for z in (.060,h-.055):
                        sx=-1 if x<0 else 1
                        Q.cyl('Lag screw washer',(sx*(w/2-.001),y,z),(sx*(w/2+.003),y,z),.008,rt,'Zinc',8)
                        sy=-1 if y<0 else 1
                        Q.cyl('End board lag screw washer',(x,sy*(d/2-.001),z),(x,sy*(d/2+.003),z),.008,rt,'Zinc',8)
        # Open-topped volume; no wastefully modeled underside or buried wall.
        soilh=h-.025
    elif edge=='block':
        bw,bl,bh=.193675,.396875,.193675
        soilh=.17;h=bh
        # Each CMU has two open cells, 25mm webs, thin bed joint and staggered
        # orientation at corners. The apertures have walls and visible soil.
        for side in (-1,1):
            for j in range(max(1,round(d/.4064))):
                y=-d/2+(j+.5)*d/round(d/.4064);x=side*(w/2-bw/2)
                cmu(rt,x,y,bw,bl,bh)
            for j in range(max(1,round((w-2*bw)/.4064))):
                x=-w/2+bw+(j+.5)*(w-2*bw)/max(1,round((w-2*bw)/.4064))
                # Rotate one hollow block about its own center for the ends.
                tmp=Q.root('End CMU');cmu(tmp,0,0,bw,bl,bh);Q.join(tmp)
                Q.instance(tmp,'Transverse hollow block',(x,side*(d/2-bw/2),0),90,rt)
                for o in [*tmp.children_recursive,tmp]:Q.G.bpy.data.objects.remove(o,do_unlink=True)
    elif edge=='accessible':
        # 34in work height, shallow tray at 27.5in clear underneath. Working
        # strip is 18in reach from either long side, without a soil-filled box.
        h=.8636;soilh=h-.030
        for x in (-w/2+.04445,w/2-.04445):
            for y in (-d/2+.04445,d/2-.04445):
                Q.box('Accessible bed 4x4 leg',(x,y,.36),(.0889,.0889,.72),rt,'Wood',.002)
        # Five 38x25mm galvanized bearers support the floor at 16in spacing.
        # Their lower faces and the bolted timber aprons retain 27.45in clear.
        for x in (-.8128,-.4064,0,.4064,.8128):
            Q.box('Galvanized transverse tray bearer',(x,0,.7100),(.0381,d-.0762,.0254),rt,'Zinc',.001)
        Q.box('Supported 19mm tray floor',(0,0,.732225),(w-.0762,d-.0762,.01905),rt,'Wood',.001)
        for y in (-d/2+.01905,d/2-.01905):Q.box('Accessible bolted long apron',(0,y,.78045),(w,.0381,.1663),rt,'Wood',.0015)
        for x in (-w/2+.01905,w/2-.01905):Q.box('Accessible tray end',(x,0,.78045),(.0381,d-.0762,.1663),rt,'Wood',.0015)
        for x in (-w/2+.04445,w/2-.04445):
            for sy in (-1,1):
                for z in (.751,.825):Q.cyl('Tray apron carriage bolt',(x,sy*(d/2-.002),z),(x,sy*(d/2+.004),z),.008,rt,'Zinc',8)
        rt['working_height_m']=h;rt['undertray_clearance_m']=.6973
    else:soilh=.032;h=.05
    # Small undulations keep beds from reading as rigid featureless trays.
    v=[];faces=[];nx,ny=6,12
    inset=.205 if edge=='block' else .045 if edge in ('lumber','accessible') else .025
    for j in range(ny+1):
        for i in range(nx+1):
            x=(-w/2+inset)+(w-2*inset)*i/nx;y=(-d/2+inset)+(d-2*inset)*j/ny
            z=soilh+.005*math.sin(x*17+y*9)+rng.uniform(-.003,.003)
            v.append((x,y,z))
    for j in range(ny):
        for i in range(nx):
            k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1))
    Q.mesh('Cultivated soil actual surface',v,faces,rt,'Soil',upward=True)
    rt['soil_surface_m']=soilh
    Q.join(rt);return rt


def cmu(rt,x,y,w,l,h):
    t=.025
    for side in (-1,1):Q.box('CMU shell',(x+side*(w-t)/2,y,h/2),(t,l,h),rt,'Block')
    for z in (-l/2+t/2,0,l/2-t/2):Q.box('CMU cross web',(x,y+z,h/2),(w-2*t,t,h),rt,'Block')


def cage():
    rt=Q.root('TomatoCage','support')
    for j,z in enumerate((.35,.68,1.01,1.34)):Q.ring('Resistance welded cage hoop',z,.20+j*.032,rt,wire=.0025,segments=24)
    for k in range(4):
        a=k*math.pi/2
        Q.tube('5mm cage leg',[(.18*math.cos(a),.18*math.sin(a),0),(.20*math.cos(a),.20*math.sin(a),.35),(.296*math.cos(a),.296*math.sin(a),1.34)],.0025,rt,s=4)
    Q.join(rt);return rt


def trellis(teepee=False,foot_radius=.52):
    rt=Q.root('BeanTeepee' if teepee else 'BeanTrellis','support')
    if teepee:
        for j in range(5):
            a=j*math.tau/5;foot=Vector((math.cos(a)*foot_radius,math.sin(a)*foot_radius,0));top=Vector((0,0,2.12))
            Q.cyl('Bamboo pole with driven foot',foot+(foot-top).normalized()*.20,top,.0125,rt,'Wood',7)
        for z in (.55,1,1.5):Q.ring('Slack lashing ring',z,foot_radius*(1-z/2.12),rt,'Straw',.0015,segments=18)
    else:
        for x in (-.95,.95):Q.box('Trellis 2x2 driven stake',(x,0,.96),(.0381,.0381,2.32),rt,'Wood')
        Q.box('Trellis top crossbar',(0,0,2.08),(2.04,.0381,.0381),rt,'Wood')
        for j in range(13):
            x=-.9+j*.15;Q.tube('Tensioned vertical garden twine',[(x,0,.08),(x,.014,1.10),(x,0,2.08)],.00125,rt,'Straw',3)
        for z in (.40,.8,1.2,1.6):Q.tube('Sagging horizontal twine',[(-.95,0,z),(-.45,0,z-.025),(0,0,z-.035),(.45,0,z-.025),(.95,0,z)],.00125,rt,'Straw',3)
    Q.join(rt);return rt


def compost():
    rt=Q.root('CompostThreeBay','infrastructure');w=1.05
    for x in (-1.575,-.525,.525,1.575):
        for y in (-.49,.49):Q.box('Compost 4x4 post',(x,y,.52),(.075,.075,1.04),rt,'OldWood')
        for j in range(7):Q.box('Gapped pallet division slat',(x,0,.08+j*.14),(.019,.98,.09),rt,'OldWood')
    for k in range(3):
        x=(k-1)*w
        for j in range(7):Q.box('Back pallet slat',(x,.50,.08+j*.14),(1.02,.019,.09),rt,'OldWood')
        for j in range((3,5,2)[k]):Q.box('Removable front slat',(x,-.50,.08+j*.14),(.99,.025,.09),rt,'Wood')
        # Unequal mound crowns, one active bay, one brown-dry, one finished.
        h=(.64,.83,.30)[k];verts=[(x-.04,.02,h*.95)];faces=[];n=16
        for row,(radius,height) in enumerate(((.55,.92),(.81,.72),(.97,.36),(1,.015/h))):
            for q in range(n):
                a=q*math.tau/n;rough=1+.025*math.sin(q*3.7+k)
                z=h*height+(.018*math.sin(q*2.4+k+row) if row<3 else 0)
                verts.append((x+.48*radius*rough*math.cos(a),.46*radius*rough*math.sin(a),z))
        faces.extend((0,1+q,1+(q+1)%n) for q in range(n))
        for row in range(3):
            for q in range(n):
                a=1+row*n+q;b=1+row*n+(q+1)%n;c=b+n;d=a+n;faces.append((a,d,c,b))
        heap=Q.mesh('Settled irregular compost heap',verts,faces,rt,'Soil' if k!=1 else 'Chip')
        Q.G.smooth(heap,80)
    Q.join(rt);return rt


def standpipe():
    rt=Q.root('Standpipe','infrastructure')
    Q.cyl('Galvanized standpipe',(0,0,0),(0,0,.90),.0167,rt,s=12)
    for z in (.06,.78):Q.cyl('Pipe collar',(0,0,z-.024),(0,0,z+.024),.023,rt,s=12)
    Q.cyl('Twin bib header',(-.17,0,.88),(.17,0,.88),.018,rt,s=10)
    for x in (-.17,.17):
        Q.cyl('Brass bib casting',(x,0,.88),(x,-.10,.88),.018,rt,'Brass',10)
        a=Vector((x,-.09,.86));b=Vector((x,-.13,.825));length=(b-a).length
        nipple=Q.G.lathe('Bored hose thread nipple',[(0,.0083),(0,.013),(length,.013),(length,.0083)],Q.M['Brass'],10,closed=True)
        nipple.location=a;nipple.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();Q.own(nipple,rt)
        Q.cyl('Valve stem',(x,-.04,.89),(x,-.04,.935),.004,rt,'Brass',8)
        knob=Q.root('BibWheel_Left' if x<0 else 'BibWheel_Right','pivot',rt);knob.location=(x,-.04,.938)
        knob['pivot_axis']='Z';knob['range_degrees']=[0,720]
        Q.ring('Hose bib hand wheel',0,.033,knob,'Red',.004,segments=12)
        for a in (0,math.pi/2):Q.cyl('Valve wheel spoke',(-.031*math.cos(a),-.031*math.sin(a),0),(.031*math.cos(a),.031*math.sin(a),0),.003,knob,'Red',5)
        Q.join(knob)
    # A 5/8in hose follows gravity to the ground, coils without floating,
    # then trails along the service margin. No taut suspended line.
    floor=.0092
    pts=Q.G.bezier((-.17,-.13,.825),(-.18,-.24,.54),(.70,-.84,floor),(.70,-.62,floor),steps=18)
    for j in range(1,75):
        a=j*math.tau*3/74;r=.38+.085*j/74
        pts.append((.32+r*math.cos(a),-.62+r*math.sin(a),floor))
    pts+=Q.G.bezier(pts[-1],(.79,-.40,floor),(1.20,-.32,floor),(1.26,-.10,floor),steps=8)[1:]
    Q.tube('Slack 5/8in garden hose',pts,.0103,rt,'Hose',6)
    Q.socket(rt,'Socket_Standpipe',(-.36,-.46,0))
    Q.join(rt);return rt


def barrel():
    rt=Q.root('RainBarrel','infrastructure')
    profile=[(.06,.23),(.08,.275),(.20,.29),(.70,.29),(.84,.255),(.87,.255),(.87,.238),(.84,.238),(.12,.26),(.095,.23)]
    Q.own(Q.G.lathe('Molded rain barrel shell',profile,Q.M['Blue'],20,closed=True),rt)
    Q.cyl('Closed barrel floor',(0,0,.060),(0,0,.075),.235,rt,'Blue',20)
    for z in (.20,.70):Q.ring('Molded barrel reinforcement',z,.291,rt,'Blue',.010,segments=24)
    lid=Q.root('BarrelLid','pivot',rt);lid.location=(0,0,.872);lid['slide_axis']='Z';lid['range_m']=[0,.30]
    Q.own(Q.G.lathe('Rain inlet annular lid',[(0,.060),(0,.263),(.018,.263),(.018,.060)],Q.M['Roof'],24,closed=True),lid)
    Q.own(Q.G.lathe('Lid seating gasket',[(-.003,.240),(-.003,.260),(.003,.260),(.003,.240)],Q.M['Roof'],20,closed=True),lid)
    tap=Q.G.lathe('Bored barrel tap',[(0,.008),(0,.014),(.06,.014),(.06,.008)],Q.M['Brass'],10,closed=True)
    tap.location=(0,-.28,.17);tap.rotation_euler=Vector((0,-1,0)).to_track_quat('Z','Y').to_euler();Q.own(tap,rt)
    Q.cyl('Barrel tap valve spindle',(0,-.30,.177),(0,-.30,.193),.003,rt,'Brass',6)
    handle=Q.root('BarrelTapLever','pivot',rt);handle.location=(0,-.30,.187);handle['pivot_axis']='Z';handle['range_degrees']=[0,90]
    Q.box('Rain tap lever',(.018,0,.006),(.055,.012,.012),handle,'Steel',.002)
    for x in (-.18,.18):Q.box('Barrel masonry plinth',(x,0,.035),(.16,.5,.07),rt,'Block')
    Q.join(handle);Q.join(lid);Q.join(rt);return rt


def bench():
    rt=Q.root('ShadeBench','furniture')
    for x in (-.65,.65):
        for y in (-.17,.17):Q.beam('Bench splayed leg',(x,y*1.35,0),(x,y,.43),.055,rt,'Wood')
        Q.box('Bench seat bearer',(x,0,.405),(.055,.49,.055),rt,'Wood')
        Q.beam('Bench back upright',(x,.19,.25),(x,.30,.88),.045,rt,'Wood')
    for y in (-.16,0,.16):Q.box('Bench seat board',(0,y,.452),(1.72,.145,.0381),rt,'OldWood',.003)
    for z in (.65,.82):Q.box('Bench back board',(0,.28,z),(1.72,.025,.14),rt,'OldWood',.002)
    Q.join(rt);return rt


def board():
    rt=Q.root('BulletinBoard','infrastructure')
    for x in (-.57,.57):Q.box('Notice 4x4 post',(x,0,.90),(.0889,.0889,1.8),rt,'OldWood',.002)
    Q.box('Notice plywood panel',(0,0,1.32),(1.07,.025,.70),rt,'Wood')
    for x in (-.55,.55):Q.box('Panel side batten',(x,-.023,1.32),(.06,.025,.78),rt,'Wood')
    for z in (.94,1.70):Q.box('Panel end batten',(0,-.023,z),(1.15,.025,.06),rt,'Wood')
    Q.box('Sloped notice rain cap',(0,0,1.76),(1.30,.30,.035),rt,'Roof')
    for x,z in ((-.27,1.40),(.18,1.25)):
        Q.box('Community notice paper',(x,-.014,z),(.27,.001,.31),rt,'White')
        Q.text(rt,'WORK DAY' if x<0 else 'SEEDS',(x,-.016,z),.035,'Steel')
    Q.join(rt);return rt


def bucket():
    rt=Q.root('Bucket','tool')
    Q.own(Q.G.lathe('Open 5 gallon pail',[(0,.117),(.008,.12),(.35,.151),(.36,.153),(.36,.147),(.016,.113)],Q.M['White'],16,closed=True),rt)
    Q.cyl('Sealed pail floor',(0,0,.008),(0,0,.016),.115,rt,'White',16)
    Q.ring('Rolled pail lip',.351,.151,rt,'White',.008,segments=20)
    Q.tube('Wire bail',[(-.15,0,.28),(-.155,0,.43),(-.10,0,.51),(.10,0,.51),(.155,0,.43),(.15,0,.28)],.0025,rt,'Steel',5)
    Q.join(rt);return rt


def can():
    rt=Q.root('WateringCan','tool')
    Q.own(Q.G.lathe('Pressed can body',[(.015,.13),(.03,.145),(.30,.145),(.325,.115),(.325,.095),(.30,.125),(.035,.125)],Q.M['Zinc'],16,closed=True),rt)
    Q.cyl('Sealed can floor',(0,0,.015),(0,0,.022),.133,rt,'Zinc',16)
    Q.ring('Can standing rolled seam',.008,.132,rt,'Zinc',.008,segments=20)
    Q.tube('Arched carrying handle',[(-.13,0,.28),(-.14,0,.44),(0,0,.49),(.14,0,.44),(.13,0,.28)],.012,rt,'Zinc',7)
    Q.tube('Long taper spout',[(0,-.12,.06),(0,-.21,.15),(0,-.40,.38)],.021,rt,'Zinc',8)
    Q.sphere('Perforated watering rose',(0,-.42,.40),.044,rt,'Zinc',scale=(1,.4,1),segments=12,rings=5)
    Q.join(rt);return rt


def wheelbarrow():
    rt=Q.root('Wheelbarrow','tool')
    loops=[]
    for z,w,d in ((.35,.30,.44),(.37,.35,.50),(.56,.57,.75),(.665,.63,.83),(.68,.63,.83)):
        loops.append([(x,y+.04,z) for x,y in Q.G.rounded_rectangle(w,d,min(w,d)*.21,n=2)])
    # Actual drawn tray with a rim and 1.5mm sheet gauge, open on top.
    ob=Q.G.loft('Pressed steel tapered barrow tray',loops,Q.M['Green'],caps=False)
    solid=ob.modifiers.new('Steel tray gauge','SOLIDIFY');solid.thickness=.0015;Q.own(ob,rt)
    Q.own(Q.G.profile('Tray rounded bottom',Q.G.rounded_rectangle(.30,.44,.063,n=2),.3485,.3515,Q.M['Green'],'Z'),rt)
    rim=loops[-1]+[loops[-1][0]];Q.tube('Rolled wheelbarrow tray rim',rim,.006,rt,'Green',6)
    for side in (-1,1):
        Q.beam('Timber wheelbarrow handle',(side*.20,-.57,.29),(side*.30,.87,.63),.035,rt,'Wood',.045)
        Q.beam('Parked barrow leg',(side*.24,.32,0),(side*.23,.28,.43),.026,rt,'Steel')
    Q.cyl('Wheelbarrow axle',(-.24,-.46,.18),(.24,-.46,.18),.01,rt,'Zinc',8)
    wheel=Q.root('BarrowWheel','pivot',rt);wheel.location=(0,-.46,.18);wheel['pivot_axis']='X';wheel['range_degrees']=[-360,360]
    Q.cyl('Rubber wheel',(-.052,0,0),(.052,0,0),.18,wheel,'Roof',18)
    Q.cyl('Steel wheel hub',(-.057,0,0),(.057,0,0),.066,wheel,'Zinc',12)
    Q.join(rt);Q.join(wheel);return rt


def rowcover():
    rt=Q.root('RowCover','tool')
    for y in (-.8,0,.8):
        Q.tube('Hooped row cover support',[(.49*math.cos(j*math.pi/12),y,.48*math.sin(j*math.pi/12)) for j in range(13)],.004,rt,'Zinc',5)
    v=[];f=[]
    for j in range(9):
        y=-.84+j*.21
        for k in range(13):
            a=k*math.pi/12;z=.48*math.sin(a)-.035*math.sin(math.pi*(j%4)/4)*math.sin(a)
            v.append((.495*math.cos(a),y,z+.008))
    for j in range(8):
        for k in range(12):i=j*13+k;f.append((i,i+1,i+14,i+13))
    Q.mesh('Fabric sag between hoops',v,f,rt,'White',upward=True);Q.join(rt);return rt


def pinwheel():
    rt=Q.root('Pinwheel','tool');Q.box('Pinwheel stake',(0,0,.45),(.019,.019,.90),rt,'Wood')
    pivot=Q.root('PinwheelRotor','pivot',rt);pivot.location=(0,-.022,.85);pivot['pivot_axis']='Y';pivot['range_degrees']=[-360,360]
    for j in range(4):
        a=j*math.pi/2;v=[]
        for x,z,y in ((0,0,0),(.14,0,0),(.14,.14,0),(.04,.08,-.045)):
            v.append((x*math.cos(a)-z*math.sin(a),y,x*math.sin(a)+z*math.cos(a)))
        Q.mesh('Bent pinwheel vane',v,[(0,1,2),(0,2,3)],pivot,('Red','Blue','Yellow','White')[j])
    Q.cyl('Pinwheel axle',(0,-.05,.85),(0,.018,.85),.004,rt,'Zinc',8)
    Q.join(pivot);Q.join(rt);return rt


def library():
    out={}
    for name,edge,w,d,h in [('Raised4x8','lumber',1.2192,2.4384,.23495),('Raised4x8Tall','lumber',1.2192,2.4384,.28575),('Block4x8','block',1.2192,2.4384,.193675),('Accessible8x3','accessible',2.4384,.9144,.8636),('Ground10x20','board',3.048,6.096,.1397),('GroundBare10x20','none',3.048,6.096,.032)]:out[name]=bed(name,w,d,h,edge)
    for fn in (cage,trellis,compost,standpipe,barrel,bench,board,bucket,can,wheelbarrow,rowcover,pinwheel):
        r=fn();out[r.name]=r
    r=trellis(True);out[r.name]=r
    return out
