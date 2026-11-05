"""Retail bay, exterior returns, tower and visible tenant fit-outs.

Family storefront/leaf, real wall holes and RTUs are called directly. The
wrappers supply strip-specific dimensions and never change station defaults.
"""
import math
from geometry import *
from building import storefront, glazed_leaf, wall_with_openings, rooftop_unit
from strip_graphics import quad


def coping(name,w,y,z,parent):
    box(name+' cap',(0,y,z+.018),(w,.30,.036),'Trim',parent,.003)
    for s in (-1,1):box(name+' hem',(0,y+s*.142,z-.025),(w,.016,.065),'Trim',parent,.002)
    for i in range(max(1,math.ceil(w/2.4384))):
        box(name+' seam',(-w/2+.20+i*2.4384,y,z+.041),(.022,.306,.020),'Metal',parent,.001)


def column(x,y,parent,style):
    width=.43 if style=='arcade' else .2032
    box('Column masonry plinth',(x,y,.46),(.51,.51,.61),'Wall',parent,.008)
    box('Column plinth cap',(x,y,.80),(.56,.56,.07),'Concrete',parent,.004)
    box('Canopy column',(x,y,1.98),(width,width,2.96),'Wall' if style=='arcade' else 'Trim',parent,.006)
    box('Column shoe',(x,y,.83),(width+.08,width+.08,.09),'Trim',parent,.004)
    box('Column bearing capital',(x,y,3.31),(width+.13,width+.13,.10),'Concrete' if style=='arcade' else 'Trim',parent,.004)


def cover(m,p,parent):
    w=m['width'];walk=p['walk'];style=p['style']
    y=-walk+.24
    column(-w/2,y,parent,style)
    if m.get('end_column'):column(w/2,y,parent,style)
    if style=='mansard':
        # Closed roof gauge and end returns, a steep shingled skirt over the
        # walk, rather than a roof solid floating above a storefront box.
        verts=[(-w/2,-walk,3.17),(w/2,-walk,3.17),(w/2,.10,5.04),(-w/2,.10,5.04),
               (-w/2,-walk,3.10),(w/2,-walk,3.10),(w/2,.10,4.97),(-w/2,.10,4.97)]
        mesh('Mansard shingle roof',verts,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(3,2,6,7)],'Roof',parent)
        box('Mansard lower fascia',(0,-walk,3.12),(w,.085,.24),'Trim',parent,.004)
        box('Mansard soffit',(0,-walk/2,3.12),(w,walk,.055),'White',parent,.002)
        box('Mansard top flashing',(0,.06,5.08),(w,.23,.06),'Metal',parent,.003)
    else:
        box('Covered walk roof',(0,-walk/2,3.43),(w,walk+.22,.18),'Trim',parent,.004)
        box('Canopy soffit',(0,-walk/2,3.325),(w-.02,walk+.15,.035),'White',parent,.001)
        if style!='arcade':
            clip=walk if m.get('corner_end') else 0
            box('Folded canopy fascia',(-clip/2,-walk-.065,3.43),(w-clip,.055,.34),'Primary',parent,.004)
        if style=='arcade':
            radius=(w-.50)/2;rise=.52;spring=2.77
            bottom=[(-radius+2*radius*i/20,spring+rise*math.sqrt(max(0,1-(-1+2*i/20)**2))) for i in range(21)]
            profile=[*bottom,(radius,3.78),(-radius,3.78)]
            vs=[(x,yy,z) for yy in (-walk-.15,-walk+.25) for x,z in profile];n=len(profile)
            fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
            mesh('Arcade segmental arch',vs,fs,'Wall',parent)
            box('Arcade precast cap',(0,-walk+.05,3.82),(w,.47,.08),'Concrete',parent,.004)
    # Trim supports a sequence of real soffit seams and flush white diffusers.
    for i in range(1,5):box('Soffit folded joint',(-w/2+i*w/5,-walk/2,3.298),(.012,walk-.14,.012),'Trim',parent,0)
    for x in (-w*.24,w*.24):
        box('Walk light rim',(x,-walk*.51,3.295),(.36,.25,.035),'Metal',parent,.003)
        box('Walk light lens',(x,-walk*.51,3.274),(.32,.21,.008),'White',parent,.002)


def interior(m,p,parent):
    w=m['width'];key=m['tenant'];deep=7.4
    box('Tenant ceiling',(0,deep/2,3.02),(w-.24,deep,.045),'White',parent,0)
    box('Tenant room floor',(0,deep/2,.153),(w-.24,deep,.012),'Concrete',parent,0)
    box('Interior partition backing',(0,deep,1.56),(w-.25,.075,2.82),'Inside',parent,0)
    # Finish a proper room at the glazed front. The remainder is exterior-shell
    # depth and service space, not falsely advertised as a playable shop.
    for s in (-1,1):
        if (s>0 and not m['partition']) or (s<0 and m.get('open_left')):continue
        box('Room side finish',(s*(w/2-.12),deep/2,1.55),(.045,deep,2.8),'White',parent,0)
    if key!='vacant':
        for yy in (1.6,4.1,6.4):
            for x in (-w*.23,w*.23):box('Tenant ceiling diffuser',(x,yy,2.985),(.85,.26,.012),'Lamp',parent,0)
    def counter(x,y,width=1.7):
        box('Tenant counter',(x,y,.66),(width,.63,1.02),'Primary',parent,.012)
        box('Counter worktop',(x,y,1.195),(width+.07,.70,.045),'White',parent,.004)
        box('Register',(x+.25,y+.12,1.34),(.26,.22,.24),'Black',parent,.006)
    def chair(x,y):
        box('Chair upholstered seat',(x,y,.62),(.52,.50,.10),'Trim',parent,.025,2)
        box('Chair back',(x,y+.23,.90),(.50,.07,.55),'Trim',parent,.022,2)
        cylinder('Chair stem',(x,y,.17),(x,y,.57),.035,'Metal',parent,10)
        for a in (0,math.pi/2):
            beam('Chair base',(x-.30*math.cos(a),y-.30*math.sin(a),.20),(x+.30*math.cos(a),y+.30*math.sin(a),.20),.035,.035,'Metal',parent)
    if key in ('nails','hair'):
        counter(-w*.23,1.8,1.4)
        for j in range(3):
            yy=2.5+j*1.4;chair(w*.20,yy)
            if key=='hair':
                panel('Salon mirror',w*.30,yy+.55,1.56,1.0,1.05,'Metal',parent,.009)
            else:
                box('Manicure desk',(w*.20-.6,yy,.90),(.65,.80,.06),'White',parent,.006)
                for s in (-1,1):box('Manicure desk pedestal',(w*.20-.6,yy+s*.28,.52),(.52,.08,.72),'White',parent,.004)
    elif key=='laundry':
        for s in (-1,1):
            for j in range(4):
                x=s*(w/2-.78);y=1.4+j*1.23
                box('Front load washer cabinet',(x,y,.76),(1.0,.86,1.20),'White',parent,.022)
                face=root('Washer face',(x,y-.447,.80),parent=parent)
                cylinder('Washer bezel',(0,0,0),(0,-.05,0),.34,'Metal',face,24)
                cylinder('Washer black seal',(0,-.051,0),(0,-.063,0),.285,'Black',face,24)
                cylinder('Washer glass',(0,-.064,0),(0,-.068,0),.245,'Glass',face,24)
                panel('Washer control',0,-.012,.44,.46,.13,'Trim',face,.018)
        box('Laundry folding table',(0,4.3,.98),(1.18,2.4,.06),'White',parent,.004)
        for yy in (3.5,5.1):box('Folding table legs',(0,yy,.56),(.85,.08,.80),'Trim',parent,.002)
    elif key=='cleaner':
        counter(-w*.20,1.8,2.3)
        for xx in (-w*.25,w*.18):
            for zz in (.38,1.7):cylinder('Garment rack',(xx,4.0,zz),(xx,6.6,zz),.024,'Metal',parent,8)
            for j in range(12):
                yy=4.1+j*.20
                box('Hanging garment',(xx,yy,1.15),(.70,.07,1.0),'White' if j%3 else 'Primary',parent,.015)
    elif key=='pizza':
        counter(w*.18,3.8,w*.55)
        box('Pizza oven',(w*.22,5.8,1.25),(1.9,1.0,1.7),'Metal',parent,.025)
        for zz in (.95,1.47):panel('Oven dark mouth',w*.22,5.285,zz,1.50,.30,'Black',parent,.018)
        for j in range(2):
            x=-w*.27;y=1.6+j*1.7
            box('Takeout table',(x,y,.92),(.77,.77,.07),'White',parent,.02)
            cylinder('Table pedestal',(x,y,.18),(x,y,.88),.04,'Trim',parent,10)
            for dx in (-.58,.58):chair(x+dx,y)
    elif key=='mattress':
        for j in range(3):
            x=(-.20 if j%2 else .20)*w;y=1.7+j*1.7
            box('Bed display base',(x,y,.35),(1.55,1.65,.38),'Trim',parent,.015)
            box('Mattress display',(x,y,.67),(1.57,1.68,.29),'White',parent,.075,3)
            box('Bed display pillow',(x,y+.52,.88),(1.0,.38,.14),'White',parent,.06,2)
    elif key in ('phone','tax'):
        counter(w*.20,2.2,w*.48)
        for j in range(3):chair(-w*.28,1.4+j*.78)
        box('Work desk',(w*.21,5.0,.92),(2.1,.8,.06),'White',parent,.005)
        box('Computer monitor',(w*.21,5.05,1.30),(.58,.07,.39),'Trim',parent,.01)
    else:
        box('Vacant letting partition',(0,5.3,1.55),(w-.30,.055,2.8),'White',parent,0)


def rear(m,p,parent,ink,layout):
    w,d=m['width'],m['depth'];b=p['building'];roof=b['roof']
    rr=root(m['id']+'_Rear',(0,d-.1016,0),180,parent=parent,kind='RearWall')
    rr['reusable_module']=True
    # Door and scupper are physical apertures in the rear segment.
    wall_with_openings('Rear CMU',w,b['parapet'],[(w*.20,1.016,.1524,2.134),(-w*.28,.30,roof+.005,.17)],rr,mat='Wall')
    door=hinge(m['id']+'_ServiceDoor',(w*.20-.495,-.15,.158),rr,(-100,0))
    box('Rear steel leaf',(.495,0,1.055),(.984,.045,2.10),'Trim',door,.004)
    box('Rear panic bar',(.50,-.06,1.04),(.68,.035,.035),'Metal',door,.003)
    socket(m['id']+'__RearHand',(.77,-.07,1.04),door,'door_handle')
    # Printed address is a small installed open-font diagnostic, not contour mesh.
    quad('Rear tenant address',m['address'],'sign',w*.20,-.135,2.45,.32,.075,rr,ink,layout)
    box('Rear wall pack',(w*.20,-.12,2.95),(.28,.20,.32),'Trim',rr,.022,2)
    box('Rear wall pack lens',(w*.20,-.225,2.86),(.23,.025,.12),'White',rr,.006)
    x=-w*.28
    for s in (-1,1):box('Scupper sleeve jamb',(x+s*.15,-.01,roof+.09),(.012,.39,.17),'Metal',rr,.001)
    for z in (roof+.01,roof+.17):box('Scupper sleeve sill',(x,-.01,z),(.29,.39,.012),'Metal',rr,.001)
    # Open hopper and hollow downpipe, shared station construction vocabulary.
    def loop(width,depth,z):return [(x+xx,-.21+yy,z) for xx,yy in ((-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2))]
    own(G.ring_loft('Open scupper hopper',[loop(.11,.09,roof-.24),loop(.34,.25,roof),loop(.32,.23,roof),loop(.09,.07,roof-.24)],M['Metal']),rr)
    own(G.ring_loft('Hollow downspout',[loop(.10,.08,.18),loop(.10,.08,roof-.24),loop(.09,.07,roof-.24),loop(.09,.07,.18)],M['Metal']),rr)
    for z in (.55,2.1,3.6):box('Downpipe wall strap',(x,-.19,z),(.13,.16,.028),'Trim',rr,.002)
    box('Downpipe splash block',(x,-.50,.05),(.35,.70,.10),'Concrete',rr,.01)
    # Each tenant has its local disconnect/RTU feeder. The utility meters are
    # collected into an accessible common bank at the rear, below.
    sx=-w*.03
    box('Service disconnect',(sx+.56,-.12,1.45),(.31,.20,.62),'Trim',rr,.006)
    box('Disconnect handle',(sx+.56,-.24,1.45),(.055,.045,.18),'Black',rr,.006)
    tube('Service conduit',[(sx+.56,-.13,.05),(sx+.56,-.13,1.1)],.024,'Metal',rr,8)
    tube('Roof unit feeder',[(sx+.56,-.12,1.76),(sx+.56,-.12,roof+.10),(sx+.56,.25,roof+.10)],.022,'Metal',rr,8)
    gx=-w*.44
    box('Gas meter',(gx,-.28,.72),(.34,.22,.43),'Metal',rr,.045,2)
    for s in (-1,1):tube('Gas riser',[(gx+s*.22,-.24,.03),(gx+s*.22,-.24,.97),(gx+s*.1,-.24,.97),(gx+s*.1,-.24,.85)],.022,'Metal',rr,8)
    cylinder('Gas regulator',(gx-.22,-.24,.98),(gx-.22,-.24,1.08),.07,'Metal',rr,12)
    coping('Rear coping',w,d-.1016,b['parapet'],parent)
    return rr


def bay(m,p,ink,layout):
    r=root(m['id'],(*m['origin'],0),m['yaw'],kind='Bay');r['reusable_module']=True
    w,d=m['width'],m['depth'];b=p['building']
    r['tenant']=m['tenant'];r['lease_group']=m['lease_group'];r['nominal_width_m']=w;r['nominal_depth_m']=d
    box('Bay slab',(0,d/2,.0762),(w,d,.1524),'Concrete',r,.005)
    # The shared partition belongs to exactly one bay. Remove it between a
    # combined tenant's bays; there are no duplicated hidden wall slabs.
    if m['partition']:box('Tenant demising wall',(w/2-.075,d/2,1.62),(.15,d,2.94),'Inside',r,0)
    dx=-w*.23;dw=.9144
    wall_with_openings('Front masonry',w,b['parapet'],[(0,w-.60,.20,2.68),(dx,dw+.14,.1524,2.73)],r,.1016)
    for s in (-1,1):
        box('Storefront pier',(s*(w/2-.14),-.06,1.60),(.28,.34,2.90),'Wall',r,.004)
        box('Pier cap',(s*(w/2-.14),-.12,2.95),(.36,.44,.12),'Concrete',r,.004)
        box('Pier water table',(s*(w/2-.14),-.12,.81),(.35,.43,.075),'Concrete',r,.004)
    # Single 36-inch leaf, independent jamb and clear outward landing. Windows
    # retain the station's exact 55mm aluminum profile/head/transom vocabulary.
    entry=glazed_leaf(m['id']+'_Entry',dx,-.06,.158,dw,2.03,r)
    for x in (dx-dw/2-.035,dx+dw/2+.035):box('Entry fixed jamb',(x,-.06,1.46),(.055,.12,2.60),'Trim',r,.002)
    box('Entry door header',(dx,-.06,2.22),(dw+.12,.12,.07),'Trim',r,.002)
    box('Entry fixed head',(dx,-.06,2.7225),(dw+.12,.12,.055),'Trim',r,.002)
    panel('Entry transom',dx,-.06,2.475,dw-.03,.43,'Glass',r,.006)
    lo=-w/2+.31;hi=w/2-.31
    for a,c in ((lo,dx-dw/2-.07),(dx+dw/2+.07,hi)):
        span=c-a;count=max(1,round(span/1.50))
        for j in range(count):storefront('Display storefront',a+(j+.5)*span/count,-.04,span/count-.035,r)
    box('Entry threshold',(dx,-.01,.1524),(dw+.14,.24,.014),'Metal',r,.002)
    quad('Entry tenant address',m['address'],'sign',dx,-.128,2.52,.28,.065,r,ink,layout)
    for lo,hi in ((-w/2,dx-dw/2-.08),(dx+dw/2+.08,w/2)):
        box('Front water table',((lo+hi)/2,-.115,.20),(hi-lo,.10,.085),'Concrete',r,.003)
    for z in (3.06,4.95):box('Sign band reveal',(0,-.035,z),(w,.085,.08),'Concrete',r,.003)
    if m.get('corner_walk_clip'):
        cr=root('Mitered return canopy',(p['walk']/2,0,0),parent=r)
        cover({**m,'width':w-p['walk']},p,cr)
    else:cover(m,p,r)
    # Real sign cabinets / projecting raceway; the replaceable face is a quad.
    sy=-p['walk']+.50 if p['style']=='mansard' else -.20
    sz=3.91 if p['style']=='mansard' else 4.38
    sw=m.get('sign_width',w-.95);sh=.97;sx=m.get('sign_offset',0)
    if not m.get('hosted_sign') and m.get('sign_leader',True):
        box('Tenant sign cabinet',(sx,sy+.065,sz),(sw,.14,sh),'Trim',r,.009)
        # A common carrier accepts any tenant graphic without new geometry.
        # Filled box/panel cells cover the raceway; channel cells expose it.
        box('Sign carrier raceway',(sx,sy-.016,sz+.37),(sw-.20,.055,.06),'Trim',r,.004)
        frame('Sign cabinet extrusion',sx,sy-.023,sz,sw+.03,sh+.03,'Metal',r,.026,.065)
        quad('Tenant replaceable sign',m['tenant'],'sign',sx,sy-.059,sz,sw-.06,sh-.06,r,ink,layout)
    quad('Door hours / lease poster',m['tenant'],'window',dw/2,-.0008,1.51-.158,.52,.44,entry,ink,layout)
    quad('Tenant window notice',m['tenant'],'window',w*.19,-.0438,1.40,1.30,.80,r,ink,layout)
    # The sign band is a wall parapet around a real lower membrane roof.
    box('Roof membrane',(0,d/2,b['roof']),(w-.01,d-.39,.045),'Roof',r,0)
    coping('Front coping',w,.1016,b['parapet'],r)
    rear(m,p,r,ink,layout)
    rooftop_unit('Tenant roof unit',(0,d*.56,b['roof']+.0225),r,(2.05,1.32,1.05))
    for x in (-.48,.48):
        cylinder('Roof vent boot',(x,d*.74,b['roof']+.0225),(x,d*.74,b['roof']+.10),.14,'Black',r,12)
        cylinder('Roof plumbing vent',(x,d*.74,b['roof']+.10),(x,d*.74,b['roof']+.57),.045,'Metal',r,10)
    interior(m,p,r)
    socket(m['id']+'__Entry',(dx,-.18,.1524),r,'pedestrian_entry')
    socket(m['id']+'__RepeatLeft',(-w/2,0,0),r,'bay_joint')
    socket(m['id']+'__RepeatRight',(w/2,0,0),r,'bay_joint')
    return r


def endcap(name,x,p,parent=None,outward=-1):
    b=p['building'];d=b['depth'];r=root(name,(x,b['front']+d/2,0),kind='EndCap',parent=parent);r['reusable_module']=True
    box('End wall',(0,0,b['parapet']/2),(.2032,d,b['parapet']),'Wall',r,.004)
    box('End wainscot',(0,0,.48),(.245,d,.65),'Wall',r,.003)
    box('End water table',(0,0,.83),(.29,d,.07),'Concrete',r,.003)
    for s in (-1,1):box('End coping hem',(s*.142,0,b['parapet']-.025),(.016,d,.065),'Trim',r,.002)
    box('End coping',(0,0,b['parapet']+.018),(.30,d,.036),'Trim',r,.003)
    for yy in (-d*.28,d*.28):
        box('End wall pack',(outward*.16,yy,3.0),(.15,.29,.33),'Trim',r,.02,2)
        box('End wall lens',(outward*.245,yy,2.92),(.018,.23,.12),'White',r,.004)
    return r


def tower(name,x,p,tenant,ink,layout):
    f=p['building']['front'];walk=p['walk'];width=3.7;height=6.72
    r=root(name,(x,f-walk+.12,0),kind='Tower');r['reusable_module']=True
    for s in (-1,1):
        box('Tower masonry pier',(s*(width-.50)/2,.20,2.1),(.50,.72,3.90),'Wall',r,.006)
        box('Tower pier base',(s*(width-.50)/2,.19,.48),(.63,.83,.65),'Wall',r,.008)
        box('Tower capital',(s*(width-.50)/2,.18,3.99),(.68,.89,.16),'Concrete',r,.006)
    box('Raised tower parapet',(0,.20,(4.06+height)/2),(width,.60,height-4.06),'Wall',r,.006)
    for z in (4.12,height-.25):box('Tower recessed belt',(0,-.13,z),(width+.10,.09,.15),'Concrete',r,.004)
    coping('Tower coping',width+.20,.20,height,r)
    panel('Tower sign recess',0,-.107,5.43,3.05,1.15,'Primary',r,.028)
    quad('Tower entry identification',tenant or p['center_name'],'tower' if tenant else 'sign',0,-.139,5.43,2.96,1.06,r,ink,layout)
    return r


def ladder(p):
    b=p['building'];x=b['left']+.70;y=b['rear']+.35
    r=root('RoofLadder',(x,y,0),kind='RoofLadder');r['reusable_module']=True
    for s in (-1,1):
        tube('Ladder side rail',[(s*.25,0,.40),(s*.25,0,5.65),(s*.25,-.20,5.90),(s*.25,-.50,5.90)],.022,'Metal',r,8)
        for z in (.60,2.1,3.6,4.9):beam('Ladder wall bracket',(s*.25,0,z),(s*.25,-.35,z),.035,.035,'Metal',r)
    for i in range(17):cylinder('Ladder rung',(-.25,0,.50+i*.30),(.25,0,.50+i*.30),.016,'Metal',r,8)
    return r


def meter_bank(p,ink,layout):
    # Keep the common utility bank on the rear end-wall station. The rear
    # bays already carry doors, rain leaders and gas services; a long rack
    # across them collides even when every moving-door sweep passes.
    b=p['building'];right=b['left']+b['width'];x=right+.06;y=b['rear']-2.5
    r=root('MeterBank',(x,y,0),90,kind='MeterBank');r['reusable_module']=True
    count=len(p['modules']);width=(count-1)*.38+.38
    box('Meter common trough',(0,-.15,1.14),(width,.27,.30),'Metal',r,.008)
    for i,tenant in enumerate(p['modules']):
        xx=(i-(count-1)/2)*.38
        box('Meter socket enclosure',(xx,-.15,1.63),(.34,.25,.61),'Metal',r,.008)
        cylinder('Sealed tenant meter',(xx,-.28,1.73),(xx,-.35,1.73),.145,'Metal',r,20)
        cylinder('Meter glass dome',(xx,-.355,1.73),(xx,-.373,1.73),.119,'Glass',r,20)
        panel('Meter LCD',xx,-.38,1.75,.15,.055,'Inside',r,.003)
        quad('Meter tenant label',tenant['address'],'sign',xx,-.282,1.42,.21,.047,r,ink,layout)
        cylinder('Meter feeder',(xx,-.15,1.28),(xx,-.15,1.40),.021,'Metal',r,8)
    for xx in (-width*.35,width*.35):
        cylinder('Underground service riser',(xx,-.15,0),(xx,-.15,1.01),.045,'Metal',r,12)
        for z in (.35,.85):
            # Feet bear on the end wainscot / projecting water table. Leave
            # only a half-millimeter assembly tolerance at the wall skin.
            wall_x=right if p['elbow'] else right-.1016+(.245 if z<.8 else .29)/2
            back=x-wall_x-.0005;front=-.29
            box('Service riser wall foot',(xx,(front+back)/2,z),(.14,back-front,.035),'Trim',r,.002)
    return r
