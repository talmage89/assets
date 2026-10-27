"""Low-detail crew-cab interior: real volumes, restrained shader detail."""
import math
import bpy
from mathutils import Vector
from kit import model as G
from kit.vehicle import samples
from forms import roof,hermite,windshield
import pickup_spec as S
from detail_helpers import box,tube,loop,print_quad


def build(b):
    def cushion(name,x,y,width,depth,z0,z1,mat):
        loops=[]
        for z,scale in [(z0,.91),((z0+z1)/2,1),(z1,.94)]:
            loops.append([(x+u,y+v,z) for u,v in G.rounded_rectangle(width*scale,depth*scale,min(.065,width*.15),4 if b.high else 3)])
        return b.add(G.smooth(G.loft(name,loops,mat)),category='interior')
    for side,x in [('L',-.480),('R',.480)]:
        for dx in [-.17,.17]:box(b,'Seat rail_'+side+str(dx),(x+dx,-.46,.716),(.043,.590,.049),b.m['frame'],'interior',radius=.003)
        cushion('Front seat cushion_'+side,x,-.485,.535,.620,.753,.923,b.m['cloth'])
        loops=[]
        for z,y,w,d in [(.905,-.192,.485,.16),(1.08,-.126,.527,.166),(1.32,-.038,.480,.140),(1.455,.015,.422,.125)]:
            loops.append([(x+u,y+v,z) for u,v in G.rounded_rectangle(w,d,.046,4 if b.high else 3)])
        b.add(G.smooth(G.loft('Front backrest_'+side,loops,b.m['cloth'])),category='interior')
        for sign in [-1,1]:
            xx=x+sign*.075;tube(b,'Headrest stem_'+side+str(sign),[(xx,.015,1.40),(xx,.035,1.54)],.006,b.m['chrome'],'interior',sides=6)
        cushion('Front headrest_'+side,x,.030,.269,.142,1.490,1.675,b.m['cloth'])
        # Bolster seams follow the front of the actual backrest, not rigid panels.
        for sign in [-1,1]:
            pts=[(x+sign*.156,yy-.002,zz) for zz,yy in [(1.00,-.239),(1.10,-.210),(1.29,-.125),(1.40,-.067)]]
            tube(b,'Seat bolster seam_'+side+str(sign),pts,.0018,b.m['seat_side'],'interior',sides=4)
        box(b,'Seat buckle_'+side,(x+(-.27 if x>0 else .27),-.175,.901),(.034,.055,.055),b.m['plastic'],'interior',radius=.007)
    cushion('Rear bench cushion',0,.585,1.485,.525,.780,.925,b.m['cloth'])
    loops=[]
    for z,y,w,d in [(.90,.815,1.48,.13),(1.13,.844,1.46,.155),(1.435,.868,1.40,.115)]:
        loops.append([(u,y+v,z) for u,v in G.rounded_rectangle(w,d,.045,4 if b.high else 3)])
    b.add(G.smooth(G.loft('Rear bench back',loops,b.m['cloth'])),category='interior')
    for i,x in enumerate([-.486,0,.486]):
        for dx in [-.060,.060]:tube(b,'Rear headrest stalk_'+str(i)+str(dx),[(x+dx,.862,1.40),(x+dx,.868,1.525)],.0055,b.m['chrome'],'interior',sides=6)
        cushion('Rear headrest_'+str(i),x,.867,.248,.125,1.475,1.635,b.m['cloth'])
    # Cowl/dash shell with a sloping crash pad and its lower knee bolster.
    profile=[(-1.365,.935),(-1.365,1.295),(-1.27,1.342),(-1.02,1.318),(-.906,1.198),(-.948,1.008),(-1.09,.952)]
    ob=G.profile('Dashboard shell',profile,-.860,.860,b.m['interior'],axis='X',radius=.012,segments=3 if b.high else 1);b.add(ob,category='interior')
    box(b,'Center dashboard stack',(0,-.928,1.155),(.390,.058,.277),b.m['seat_side'],'interior',radius=.024)
    print_quad(b,'Alder center display',[(.148,-.895,1.167),(-.148,-.895,1.167),(-.148,-.895,1.292),(.148,-.895,1.292)],b.m['display'],'interior')
    box(b,'Instrument binnacle',(.480,-1.005,1.287),(.365,.135,.124),b.m['plastic'],'interior',radius=.026)
    print_quad(b,'Original instrument face',[(.635,-.932,1.246),(.325,-.932,1.246),(.325,-.932,1.322),(.635,-.932,1.322)],b.m['display'],'interior')
    for x in [-.755,-.252,.252,.755]:
        box(b,'Dash vent '+str(x),(x,-.953,1.271),(.095,.020,.076),b.m['plastic'],'interior',radius=.008)
        for z in [1.25,1.267,1.284]:box(b,'Vent vane '+str(x)+str(z),(x,-.939,z),(.080,.007,.004),b.m['interior_light'],'interior',radius=.0005)
    b.add(G.box('Center console',(0,-.354,.881),(.287,.775,.316),b.m['interior'],.044,3 if b.high else 2),category='interior')
    box(b,'Console arm pad',(0,-.124,1.059),(.282,.370,.060),b.m['seat_side'],'interior',radius=.029)
    for y in [-.48,-.635]:
        loop(b,'Cup holder '+str(y),(0,y,1.046),(1,0,0),(0,1,0),(.052,.052),.006,b.m['plastic'],'interior',segments=16,sides=4)
        box(b,'Cup holder well '+str(y),(0,y,1.018),(.096,.096,.041),b.m['plastic'],'interior',radius=.028)
    tube(b,'Shift lever',[(.095,-.70,1.04),(.095,-.66,1.17)],.013,b.m['frame'],'interior',sides=8)
    box(b,'Shifter grip',(.095,-.656,1.185),(.045,.061,.055),b.m['seat_side'],'interior',radius=.020)
    # Steering plane is tilted toward the driver. 30 mm rim section.
    c=Vector((.480,-.765,1.251));a=Vector((1,0,0));up=Vector((0,-.46,.888)).normalized();normal=a.cross(up).normalized()
    loop(b,'Steering wheel rim',c,a,up,(.174,.174),.015,b.m['rubber'],'interior',segments=32 if b.high else 24,sides=8 if b.high else 6)
    tube(b,'Steering column',[tuple(c+normal*.025),(.480,-1.075,1.070)],.029,b.m['plastic'],'interior',sides=12)
    hub=box(b,'Steering airbag',c,(.157,.069,.131),b.m['seat_side'],'interior',radius=.025)
    for angle in [0,math.pi,1.5*math.pi]:
        q=c+a*(.155*math.cos(angle))+up*(.155*math.sin(angle));mid=c+a*(.080*math.cos(angle))+up*(.080*math.sin(angle))
        tube(b,'Steering spoke '+str(angle),[tuple(mid),tuple(q)],.020,b.m['interior_light'],'interior',sides=4)
    # Inner door cards and armrests move with the outer doors.
    for side,sgn in [('L',-1),('R',1)]:
        for end,ya,yb in [('F',S.DOOR_FRONT,S.DOOR_SPLIT),('R',S.DOOR_SPLIT,S.DOOR_REAR)]:
            parent=bpy.data.objects['Door_'+end+side];y=(ya+yb)/2;w=yb-ya-.105
            outline=[(y+u,1.018+v) for u,v in G.rounded_rectangle(w,.594,.052,3)]
            panel=G.profile('Inner door card_'+end+side,outline,sgn*.900,sgn*.935,b.m['interior'],axis='X');b.add(panel,parent,'interior')
            box(b,'Door armrest_'+end+side,(sgn*.907,y-.030,1.126),(.072,w*.61,.073),b.m['seat_side'],'interior',parent,.022)
            box(b,'Inside latch_'+end+side,(sgn*.889,y-.210,1.233),(.024,.095,.034),b.m['chrome'],'interior',parent,.007)
            box(b,'Lower door pocket_'+end+side,(sgn*.870,y,.827),(.065,w*.71,.098),b.m['plastic'],'interior',parent,.016)
    def lining(u,v):
        x,y,z=roof(.020+.960*u,.018+.907*v)
        return x,y,z-.025
    b.skin('Cab headliner',lining,18,14,b.m['headliner'],(0,0,-1),category='interior',gauge=.002,return_depth=0)
    def header(u,v):
        a=Vector(windshield(.006+.988*u,1))+Vector((0,.009,-.012))
        c=Vector(roof(.020+.960*u,.018))-Vector((0,0,.025))
        return a+(c-a)*v
    b.skin('Windshield header trim',header,20,2,b.m['interior'],(0,0,-1),category='interior',gauge=.0015,return_depth=0)
    box(b,'Rear cab trim',(0,1.008,1.092),(1.72,.023,.770),b.m['interior'],'interior',radius=.012)
    for x in [-.46,.46]:
        box(b,'Sun visor '+str(x),(x,-.610,1.881),(.400,.180,.025),b.m['headliner'],'interior',radius=.011)
        tube(b,'Visor hinge '+str(x),[(x-.16,-.676,1.90),(x-.16,-.676,1.887)],.006,b.m['plastic'],'interior',sides=6)
    box(b,'Cab mirror housing',(0,-.785,1.725),(.227,.046,.074),b.m['plastic'],'interior',radius=.017)
    box(b,'Cab mirror silver',(0,-.758,1.725),(.204,.004,.055),b.m['mirror'],'interior',radius=.012)
