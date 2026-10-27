"""Low-detail boxed frame, suspension, drivetrain, exhaust and suspended spare."""
import math
import bpy
from kit import model as G
from kit.vehicle import samples
from detail_helpers import box,tube
import pickup_spec as S


def build(b):
    # Welded boxed rails: channel plus closure sheet, with a real kick-up above
    # the rear axle. Tops stay below the raised .680 m cab floor.
    stations=[(-2.65,.510),(-2.25,.550),(-1.60,.585),(.60,.585),(1.10,.725),(1.40,.770),(2.20,.770),(2.75,.640)]
    csec=[(-.035,-.070),(.035,-.070),(.035,-.064),(-.029,-.064),(-.029,.064),(.035,.064),(.035,.070),(-.035,.070)]
    for sign in [-1,1]:
        x=sign*.430
        loops=[[(x+sign*u,y,z+v) for u,v in csec] for y,z in stations]
        b.add(G.loft('Boxed frame channel_'+str(sign),loops,b.m['frame']),category='underbody')
        loops=[[(x+sign*u,y,z+v) for u,v in [(.029,-.064),(.035,-.064),(.035,.064),(.029,.064)]] for y,z in stations]
        b.add(G.loft('Frame closure_'+str(sign),loops,b.m['frame']),category='underbody')
        for y in [-1.15,.35]:box(b,'Cab frame mount_'+str(sign)+str(y),(x,y,.668),(.105,.095,.026),b.m['rubber'],'underbody',radius=.005)
        # Rear leaf pack and brackets; the central saddle sits on the axle tube.
        for leaf in range(3):
            pts=[]
            for t in samples(10):
                y=.89+1.58*t;z=.466+.184*(2*t-1)**2+leaf*.007
                pts.append((y,z))
            ob=G.sheet('Rear leaf '+str(sign)+'_'+str(leaf),pts,.053,.006,b.m['frame']);ob.location.x=sign*.588
            b.add(ob,category='underbody')
        for y in [.89,2.47]:box(b,'Leaf hanger_'+str(sign)+str(y),(sign*.525,y,.674),(.190,.076,.120),b.m['frame'],'underbody',radius=.005)
        box(b,'Axle spring saddle_'+str(sign),(sign*.588,S.REAR_AXLE,.454),(.080,.140,.025),b.m['frame'],'underbody',radius=.004)
        for dy in [-.045,.045]:tube(b,'Leaf U-bolt_'+str(sign)+str(dy),[(sign*.556,S.REAR_AXLE+dy,.423),(sign*.556,S.REAR_AXLE+dy,.510),(sign*.620,S.REAR_AXLE+dy,.510),(sign*.620,S.REAR_AXLE+dy,.423)],.006,b.m['brake'],'underbody',sides=6)
        box(b,'Rear shock upper mount_'+str(sign),(sign*.490,1.37,.750),(.100,.075,.080),b.m['frame'],'underbody',radius=.004)
        box(b,'Front strut tower_'+str(sign),(sign*.490,S.FRONT_AXLE,.733),(.125,.125,.240),b.m['frame'],'underbody',radius=.008)
        tube(b,'Rear shock body_'+str(sign),[(sign*.520,1.37,.748),(sign*.577,1.57,.550)],.025,b.m['frame'],'underbody',sides=10)
        tube(b,'Rear shock rod_'+str(sign),[(sign*.565,1.53,.586),(sign*.627,S.REAR_AXLE,.423)],.011,b.m['chrome'],'underbody',sides=8)
        # Independent front control arms and a coil-over proxy hidden in the well.
        for z in [.347,.482]:
            pts=[(sign*.437,S.FRONT_AXLE-.19,z+.030),(sign*.808,S.FRONT_AXLE,z),(sign*.437,S.FRONT_AXLE+.19,z+.030)]
            tube(b,'Front wishbone_'+str(sign)+str(z),pts,.020,b.m['frame'],'underbody',sides=8)
        tube(b,'Front strut_'+str(sign),[(sign*.520,S.FRONT_AXLE,.824),(sign*.650,S.FRONT_AXLE-.090,.370)],.041,b.m['frame'],'underbody',sides=12)
        tube(b,'Steering tie rod_'+str(sign),[(sign*.365,S.FRONT_AXLE+.09,.429),(sign*.790,S.FRONT_AXLE+.08,.414)],.0105,b.m['brake'],'underbody',sides=8)
        tube(b,'Rear axle tube_'+str(sign),[(sign*.105,S.REAR_AXLE,S.HUB_HEIGHT),(sign*.809,S.REAR_AXLE,S.HUB_HEIGHT)],.0508,b.m['frame'],'underbody',sides=12)
        for end,y in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            parent=bpy.data.objects['Steer_F'+('L' if sign<0 else 'R')] if end=='F' else b.root
            tube(b,'Hub bearing spindle_'+end+str(sign),[(sign*.795,y,S.HUB_HEIGHT),(sign*.929,y,S.HUB_HEIGHT)],.040,b.m['caliper'],'underbody',parent,sides=8)
            tube(b,'Brake carrier_'+end+str(sign),[(sign*.845,y,S.HUB_HEIGHT),(sign*.852,y+.109,S.HUB_HEIGHT+.035)],.014,b.m['caliper'],'underbody',parent,sides=6)
            if end=='F':tube(b,'Steering knuckle_'+str(sign),[(sign*.808,y,.347),(sign*.808,y,.482)],.023,b.m['caliper'],'underbody',parent,sides=8)
    for y,z in [(-2.30,.52),(-1.30,.585),(.42,.585),(1.20,.75),(2.25,.77),(2.70,.65)]:
        box(b,'Frame crossmember '+str(y),(0,y,z),(.87,.090,.095),b.m['frame'],'underbody',radius=.006)
    # The bumper/recovery and receiver loads reach the rails through mounts.
    box(b,'Front crash beam',(0,-2.780,.620),(1.50,.090,.120),b.m['frame'],'underbody',radius=.006 if b.high else 0)
    for sign in [-1,1]:
        box(b,'Front crash mount '+str(sign),(sign*.430,-2.690,.560),(.100,.240,.100),b.m['frame'],'underbody',radius=.003 if b.high else 0)
        box(b,'Hitch rail bracket '+str(sign),(sign*.430,2.690,.570),(.080,.080,.150),b.m['frame'],'underbody',radius=.003 if b.high else 0)
        tube(b,'Engine mount '+str(sign),[(sign*.430,-1.950,.635),(sign*.290,-1.950,.795)],.030,b.m['rubber'],'underbody',sides=6)
        tube(b,'Front halfshaft '+str(sign),[(sign*.120,S.FRONT_AXLE,S.HUB_HEIGHT),(sign*.805,S.FRONT_AXLE,S.HUB_HEIGHT)],.029,b.m['frame'],'underbody',sides=8)
    frontdiff=G.lathe('Front differential',[(-.120,0),(-.120,.070),(-.060,.132),( .060,.132),(.120,.070),(.120,0)],b.m['frame'],24 if b.high else 16,axis='X',center=(S.FRONT_AXLE,S.HUB_HEIGHT))
    b.add(frontdiff,category='underbody')
    bell=G.lathe('Bell housing',[(-1.680,0),(-1.680,.155),(-1.490,.120),(-1.490,0)],b.m['caliper'],24 if b.high else 12,axis='Y',center=(0,.710))
    b.add(bell,category='underbody')
    # Lowest actual axle surface targets the cited provisional 226 mm clearance.
    pumpkin=G.lathe('Rear differential',[( -.147,0),(-.147,.100),(-.093,.155),(0,S.HUB_HEIGHT-S.GROUND_CLEARANCE_TARGET),(.093,.155),(.147,.10),(.147,0)],b.m['frame'],32 if b.high else 24,axis='X',center=(S.REAR_AXLE,S.HUB_HEIGHT))
    b.add(pumpkin,category='underbody')
    tube(b,'Propeller shaft',[(0,-1.26,.558),(0,1.54,.408)],.039,b.m['frame'],'underbody',sides=12)
    box(b,'Engine casting',(0,-1.934,.929),(.580,.630,.370),b.m['caliper'],'underbody',radius=.042)
    box(b,'Engine sump',(0,-1.915,.709),(.420,.440,.109),b.m['frame'],'underbody',radius=.022)
    skid=G.sheet('Front formed skid',[(-2.49,.495),(-2.30,.480),(-2.15,.280),(-1.985,.249),(-1.82,.280),(-1.65,.515)],.590,.004,b.m['frame'])
    skid.modifiers['Sheet gauge'].use_even_offset=False;b.add(skid,category='underbody')
    for y,z in [(-2.30,.490),(-1.65,.530)]:box(b,'Skid frame mount '+str(y),(0,y,z),(.870,.055,.050),b.m['frame'],'underbody',radius=.003)
    box(b,'Transmission casing',(0,-1.335,.590),(.270,.390,.225),b.m['caliper'],'underbody',radius=.035)
    box(b,'Fuel tank',(.250,.020,.541),(.368,1.040,.195),b.m['plastic'],'underbody',radius=.045)
    for y in [-.32,.37]:box(b,'Fuel tank strap '+str(y),(.250,y,.438),(.373,.037,.006),b.m['frame'],'underbody',radius=.002)
    # Exhaust follows the chassis and rises over the live axle before exiting.
    tube(b,'Exhaust run',[(-.23,-2.10,.704),(-.23,-1.36,.457),(-.29,.32,.457),(-.31,1.33,.632),(-.47,2.25,.581),(-.82,2.60,.581)],.030,b.m['brake'],'underbody',sides=10)
    box(b,'Exhaust muffler',(-.290,.38,.466),(.178,.565,.122),b.m['brake'],'underbody',radius=.040)
    tail=G.lathe('Open exhaust outlet',[(-.800,.040),(-.973,.040),(-.973,.0382),(-.800,.0382)],b.m['chrome'],32 if b.high else 20,axis='X',center=(2.60,.581),closed=True);b.add(tail,category='underbody')
    # Unloaded horizontal spare: original carcass, steel center and hanger.
    spare=G.lathe('Suspended spare tire',[(.490,.235),(.490,.330),(.520,.385),(.645,.385),(.674,.330),(.674,.235)],b.m['rubber'],32 if b.high else 20,axis='Z',center=(0,2.19),closed=True);b.add(spare,category='underbody')
    wheel=G.lathe('Spare steel rim',[(.629,.08),(.629,.225),(.652,.225),(.674,.08)],b.m['frame'],24,axis='Z',center=(0,2.19),closed=True);b.add(wheel,category='underbody')
    tube(b,'Spare hanger',[(0,2.19,.642),(0,2.25,.790)],.0035,b.m['frame'],'underbody',sides=8)
    box(b,'Spare hanger saddle',(0,2.19,.641),(.265,.037,.018),b.m['frame'],'underbody',radius=.004)
