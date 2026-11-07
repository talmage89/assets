"""Original modular post/deck system and play events. No imported geometry."""
import math
import bpy
from mathutils import Vector
import geometry as F
from geometry import box,cyl,tube,loft,lathe,bolt,empty
from dimensions import *

def post(rt,h=2.45):
    lathe(rt,'127 mm galvanized post / .120 wall',[(0,.06045),(0,.0635),(h-.018,.0635),(h-.018,.06045)],s=16,closed=True)
    lathe(rt,'Riveted die-cast domed cap',[(h-.025,.0629),(h-.025,.067),(h-.007,.067),(h+.009,.053),(h+.016,0)],s=16)
    for a in (0,120,240):
        t=math.radians(a);cyl(rt,'Cap blind rivet',(.063*math.cos(t),.063*math.sin(t),h-.014),(.069*math.cos(t),.069*math.sin(t),h-.014),.003,'zinc',6)
    empty(rt,rt.name+'_Ground',(0,0,0),'post_center')

def deck(rt,grid=GRID):
    side=grid-POST_OD;z=0;half=grid/2
    # Solid skin with actual gauge; hemmed downturned flange, open underside.
    p=G=None
    ob=box(rt,'12 gauge punched plastisol deck',(0,0,-DECK_GAUGE/2),(side,side,DECK_GAUGE),'deck',.001,mat='Deck');ob['role']='deck_top'
    for s in (-1,1):
        box(rt,'Downturned deck flange',(s*(side-.009)/2,0,-TRAY_DEPTH/2),(.009,side,TRAY_DEPTH),'deck',.002)
        box(rt,'Downturned deck flange',(0,s*(side-.009)/2,-TRAY_DEPTH/2),(side-.018,.009,TRAY_DEPTH),'deck',.002)
        box(rt,'Returned lower tray hem',(0,s*(side-.018)/2,-TRAY_DEPTH),(side,.020,.008),'deck',.002)
    for x in (-half,half):
        for y in (-half,half):
            F.clamp(rt,x,y,-.052)
            box(rt,'Deck slotted corner hanger',(x*.88,y*.88,-.052),(.13,.13,.024),'deck',.002)
            bolt(rt,(x*.83,y*.83,-.03),(0,0,1))
            empty(rt,rt.name+f'_Post_{x}_{y}',(x,y,0),'deck_post_center')
    box(rt,'Underside hat stiffener',(0,0,-.055),(side,.038,.06),'deck',.002)

def barrier(rt,panel=False,grid=GRID):
    half=grid/2
    for z in (.065,BARRIER_HEIGHT):cyl(rt,'Welded barrier rail',(-half+.07,0,z),(half-.07,0,z),GRIP_OD/2,'rail',10)
    if panel:
        box(rt,'Rounded molded infill',(0,0,.52),(GRID-.20,.039,.83),'blue',.018,'Molded')
        for x in (-.40,.40):
            for z in (.18,.86):bolt(rt,(x,-.025,z))
    else:
        n=math.ceil((grid-.2792)/.084)+1
        for i in range(n):
            x=-(grid-.2792)/2+i*(grid-.2792)/(n-1);cyl(rt,'Vertical nonclimbable infill',(x,0,.065),(x,0,BARRIER_HEIGHT),BAR_OD/2,'rail',6)
    for x in (-half,half):
        for z in (.065,BARRIER_HEIGHT):F.clamp(rt,x,0,z)
    rt['barrier_height_m']=BARRIER_HEIGHT;rt['bottom_opening_m']=.065-GRIP_OD/2

def roof(rt,shade=False):
    if shade:
        # Tensioned fabric has catenary-like sag between four high/low corners.
        loops=[];n=10
        for j in range(n+1):
            y=-1.1+2.2*j/n;loop=[]
            for i in range(n+1):
                x=-1.1+2.2*i/n;z=.13*(x*y)+.30-.24*(1-(x/1.1)**2)*(1-(y/1.1)**2)
                loop.append((x,y,z))
            loops.append(loop)
        loft(rt,'Tensioned concave shade membrane',loops,'blue',caps=False,closed=False)
        for y in (-1.1,1.1):tube(rt,'Shade edge cable',[(x,y,.13*x*y+.30) for x in [-1.1,-.55,0,.55,1.1]],.011,'zinc',6)
        for x in (-1.1,1.1):
            for y in (-1.1,1.1):cyl(rt,'Shade strut',(x*.55,y*.55,-.38),(x,y,.13*x*y+.30),.024,'steel',8)
    else:
        # Rounded hipped shell with overhang, drip return and reinforcing ribs.
        loops=[]
        for z,w,r in [(-.034,1.78,.11),(0,1.86,.12),(.10,1.81,.15),(.62,.38,.12),(.69,.25,.10)]:
            loops.append([(x,y,z) for x,y in F.G.rounded_rectangle(w,w,r,3)])
        loft(rt,'Rotomolded hip roof closed shell',loops,'red')
        for x in (-1,1):
            for y in (-1,1):
                tube(rt,'Roof reinforcing ridge',[(x*.84,y*.84,.045),(x*.44,y*.44,.42),(x*.10,y*.10,.685)],.018,'red',6,'Molded')
        for x in (-HALF,HALF):
            for y in (-HALF,HALF):box(rt,'Roof bolted corner socket',(x,y,-.09),(.15,.15,.17),'steel',.006)

def steps(rt,height=1.2192):
    N=8;run=1.95;w=.90
    for i in range(N):
        z=height*(i+1)/N;y=-run+(i+.5)*run/N
        box(rt,'Plastisol closed stair tread',(0,y,z-.022),(w,run/N+.014,.044),'deck',.003)
        box(rt,'Closed riser / no trapped head opening',(0,y+run/N/2,z-height/N/2),(w,.025,height/N),'deck',.002)
    for x in (-w/2,w/2):
        tube(rt,'Stair stringer',[(x,-run,.03),(x,0,height-.10)],.036,'steel',8)
        tube(rt,'Stair continuous returned handrail',[(x,-run-.08,.20),(x,-run-.08,.82),(x,-run,.88),(x,0,height+.88),(x,.10,height+.88)],GRIP_OD/2,'rail',8)
        for i in (0,3,7):
            y=-run+(i+.5)*run/N;z=height*(i+1)/N
            cyl(rt,'Handrail support',(x,y,z),(x,y,z+.82),.016,'rail',8)
    for x in (-.45,.45):cyl(rt,'Stair foot into grade',(x,-run,.0),(x,-run,.22),.034,'steel',8)
    interface_bridge(rt,height,w)
    empty(rt,rt.name+'_Top',(0,0,height),'deck_entry')

def transfer(rt):
    # Low platform at 16 inches, second at 24 with unobstructed transfer side.
    for y,h in [(-.90,.4064),(-.30,.6096)]:
        box(rt,'Transfer platform',(0,y,h-.035),(1.05,.60,.070),'deck',.012)
        for x in (-.43,.43):
            for yy in (y-.21,y+.21):cyl(rt,'Transfer legs',(x,yy,0),(x,yy,h-.04),.025,'steel',8)
    for x in (-.48,.48):tube(rt,'Transfer grab loop',[(x,-.30,.61),(x,-.30,.97),(x,-.12,1.05),(x,.03,.97),(x,.03,.61)],GRIP_OD/2,'rail',8)
    interface_bridge(rt,.6096,1.05)
    empty(rt,rt.name+'_Transfer',(0,-.9,.4064),'transfer_seat')

def ramp(rt):
    # Rise 24 inches in 24 feet, 1:12; 1.22 m clear between edge rails.
    run=7.3152;rise=.6096;w=1.30
    for i in range(6):
        a=-run+i*run/6;b=a+run/6;z0=rise*i/6;z1=rise*(i+1)/6
        pts=[(-w/2,a,z0), (w/2,a,z0),(w/2,b,z1),(-w/2,b,z1),(-w/2,a,z0-.07),(w/2,a,z0-.07),(w/2,b,z1-.07),(-w/2,b,z1-.07)]
        ob=F.G.mesh('Ramp punched tray segment',pts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],F.M['Deck']);F.own(ob,rt,'deck','Deck')
    for x in (-w/2,w/2):
        for h in (.66,.90):tube(rt,'Dual height ramp handrail',[(x,-run-.15,h),(x,-run,h),(x,0,rise+h),(x,.15,rise+h)],GRIP_OD/2,'rail',8)
        for i in range(7):
            y=-run+i*run/6;z=rise*i/6
            cyl(rt,'Ramp post to footing',(x,y,0),(x,y,z+.92),.025,'steel',8)
        # Infill closes both open sides without horizontal climbable bars.
        for i in range(57):
            y=-run+i*run/56;z=rise*i/56;cyl(rt,'Ramp infill',(x,y,z+.08),(x,y,z+.88),.0095,'rail',6)
        tube(rt,'Ramp wheel edge curb',[(x,-run,.06),(x,0,rise+.06)],.040,'deck',6)
    rt['slope_ratio']=1/12;rt['clear_width_m']=w-GRIP_OD
    empty(rt,rt.name+'_Top',(0,0,rise),'ramp_deck_connection')

def hood(rt,height):
    y=0
    # Closed rounded entrance hood: no flat extruded cutout.
    points=[(-.44,0,height+.12),(-.43,0,height+.55),(-.31,0,height+.79),(0,0,height+.89),(.31,0,height+.79),(.43,0,height+.55),(.44,0,height+.12)]
    smooth=[]
    # Cardinal cubic interpolation through the compound entrance arch.
    for i in range(len(points)-1):
        a=Vector(points[max(0,i-1)]);b=Vector(points[i]);c=Vector(points[i+1]);d=Vector(points[min(len(points)-1,i+2)])
        for j in range(3):
            t=j/3;smooth.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
    smooth.append(points[-1]);tube(rt,'Thick molded sit-down hood',smooth,.073,'red',8,'Molded')
    # The hood's cast ears span to the post collars, rather than floating.
    for x in (-1,1):
        for z in (.12,.77):cyl(rt,'Hood mounting shoulder',(x*.40,0,height+z),(x*.61,0,height+z),.025,'red',8,'Molded')
    for x in (-HALF,HALF):
        for dz in (.12,.77):F.clamp(rt,x,0,height+dz)
    for side in (-1,1):
        cheek=[]
        for dz,w,d in [(.03,.18,.11),(.12,.20,.17),(.65,.18,.13),(.78,.14,.10)]:
            cheek.append([(side*.445+x,y,height+dz) for x,y in F.G.rounded_rectangle(w,d,min(w,d)*.35,2)])
        loft(rt,'Molded entrance cheek / closed side gap',cheek,'red')
    for x in (-.45,.45):cyl(rt,'Entrance grab rail',(x,-.03,height+.10),(x,-.03,height+.68),GRIP_OD/2,'rail',8)

def slide_path(height,kind):
    if kind=='spiral':
        # Tangent entry begins along -Y; 270 degree descending helix then exit.
        pts=[];rad=1.05;turn=1.5*math.pi
        for i in range(33):
            t=i/32;ang=-turn*t
            pts.append((rad-rad*math.cos(ang),rad*math.sin(ang),height-(height-.22)*(3*t*t-2*t*t*t)))
        end=Vector(pts[-1]);direction=(end-Vector(pts[-2]));direction.z=0;direction.normalize()
        pts += [tuple(end+direction*.40),tuple(end+direction*.80)]
        return [(0,.18,height)]+pts
    L=(height-.22)/.43+.75;pts=[]
    for i in range(33):
        t=i/32;y=-L*t
        # Flat entry and exit, compound wave remains monotonic.
        u=min(1,max(0,(t-.09)/.78));f=3*u*u-2*u*u*u
        z=height-(height-.22)*f
        if kind=='wave':z+=.07*math.sin(4*math.pi*u)*math.sin(math.pi*u)**2
        pts.append((0,y,z))
    if height<.7:pts.append((0,pts[-1][1]-.25,.22))
    return [(0,.18,height)]+pts

def slide(rt,height=1.2192,kind='straight'):
    pts=slide_path(height,kind);loops=[]
    # Broad compound U, rolled shoulder and thick return; width flares at toe.
    profile=[(-.32,.30),(-.39,.29),(-.415,.25),(-.41,.10),(-.36,.01),(-.28,-.035),(0,-.050),(.28,-.035),(.36,.01),(.41,.10),(.415,.25),(.39,.29),(.32,.30),(.315,.27),(.345,.245),(.35,.13),(.30,.055),(.23,.018),(0,0),(-.23,.018),(-.30,.055),(-.35,.13),(-.345,.245),(-.315,.27)]
    # Sweep profile is horizontal in transverse section, floor follows centerline.
    for i,p in enumerate(pts):
        d=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)]);d.z=0;d.normalize();cross=Vector((-d.y,d.x,0))
        flare=1+.12*max(0,(i/(len(pts)-1)-.82)/.18)
        loops.append([tuple(Vector(p)+cross*x*flare+Vector((0,0,z*(1-.40*max(0,(i/(len(pts)-1)-.88)/.12))))) for x,z in profile])
    loft(rt,'Compound rotomolded '+kind+' chute / closed return',loops[-6:] if kind=='tube' else loops,'green' if kind=='wave' else 'red')
    lip=loops[-1][13:]+[loops[-1][0]]
    tube(rt,'Rolled rounded slide exit lip',lip,.018,'green' if kind=='wave' else 'red',5,'Molded')
    if kind=='tube':
        interface_bridge(rt,height,.75)
        # Replace open top span with a hollow circular barrel above floor.
        for k in range(5,len(pts)-6,12):
            center=Vector(pts[k])+Vector((0,0,.37));u=Vector((1,0,0));v=Vector((0,0,1))
            points=[center+u*.414*math.cos(j*math.tau/16)+v*.414*math.sin(j*math.tau/16) for j in range(17)]
            tube(rt,'Bolted tube seam flange',points,.018,'red',4,'Molded')
        ls=[]
        for p in pts[0:-3:2]:ls.append([(p[0]+.39*math.cos(j*math.tau/16),p[1],p[2]+.37+.39*math.sin(j*math.tau/16)) for j in range(16)])
        ob=loft(rt,'Enclosed tube barrel / 0.744 vertical bore',ls,'red',caps=False)
        mod=ob.modifiers.new('Rotomolded barrel gauge','SOLIDIFY');mod.thickness=.018;F.G.apply(ob)
    hood(rt,height)
    for i in (len(pts)//2,len(pts)-3):
        p=Vector(pts[i]);cyl(rt,'Slide steel saddle support',(p.x,p.y,0),(p.x,p.y,p.z-.05),.030,'steel',10)
        box(rt,'Slide saddle bracket',(p.x,p.y,p.z-.052),(.38,.15,.025),'zinc',.003)
    rt['height_m']=height;rt['slide_kind']=kind
    rt['path_m']=[list(p) for p in pts]
    empty(rt,rt.name+'_Entry',(0,.15,height),'slide_entry')
    empty(rt,rt.name+'_Exit',pts[-1],'slide_exit')

def arch(rt,height=1.2192):
    interface_bridge(rt,height,.90)
    n=15;run=2.05
    def path(x):return [(x,-run*math.cos(t*math.pi/2),height*math.sin(t*math.pi/2)) for t in [i/n for i in range(n+1)]]
    for x in (-.42,.42):tube(rt,'Bent arch ladder side',path(x),.024,'rail',10)
    for i in range(1,10):
        t=i/10;y=-run*math.cos(t*math.pi/2);z=height*math.sin(t*math.pi/2)
        cyl(rt,'32mm welded arch rung',(-.42,y,z),(.42,y,z),.016,'rail',8)
        for s in (-1,1):empty(rt,rt.name+f'_HandFoot_{i}_{s}',(s*.27,y,z),'child_hand_foot')

def ladder(rt,height=1.2192):
    interface_bridge(rt,height,.75)
    for x in (-.36,.36):tube(rt,'Vertical ladder rail',[(x,0,0),(x,0,height+.65),(x,.12,height+.75),(x,.24,height+.65)],.019,'rail',8)
    count=math.ceil(height/.28)
    for i in range(1,count+1):
        z=height*i/count;cyl(rt,'Ladder rung',(-.36,0,z),(.36,0,z),.0143,'rail',8)
        for x in (-.22,.22):empty(rt,rt.name+f'_HandFoot_{i}_{x}',(x,0,z),'child_hand_foot')

def net(rt):
    # Diagonal chained square mesh drapes, with actual supporting side rails.
    W=1.02;run=1.65;H=1.2192
    interface_bridge(rt,H,1.02)
    for x in (-W/2,W/2):tube(rt,'Net perimeter rail',[(x,-run,0),(x,0,H),(x,.10,H+.38)],.024,'steel',10)
    def p(u,v):return ((u-.5)*W,-run*(1-v),H*v-.09*math.sin(math.pi*u)*math.sin(math.pi*v))
    for i in range(5):
        u=i/4;tube(rt,'Plastisol chain net warp',[p(u,j/8) for j in range(9)],.009,'rubber',6)
    for j in range(1,6):
        v=j/6;tube(rt,'Plastisol chain net weft',[p(i/8,v) for i in range(9)],.009,'rubber',6)
        for i in range(1,4):
            q=p(i/4,v);lathe(rt,'Captive net junction',[(q[2]-.009,.016),(q[2]+.009,.016)],'zinc',8,center=q[:2])
            empty(rt,rt.name+f'_HandFoot_{j}_{i}',q,'child_hand_foot')

def rock(rt):
    interface_bridge(rt,1.2192,.94)
    loops=[]
    for z,w,y in [(0,.93,-1.23),(.28,.99,-1.02),(.75,.91,-.65),(1.18,1.01,-.17),(1.29,.92,0)]:
        loops.append([(-w/2,y,z),(-w*.23,y-.045,z+.025),(w*.19,y-.02,z-.015),(w/2,y,z),(w/2,y+.07,z),(0,y+.095,z),(-w/2,y+.07,z)])
    loft(rt,'Compound curved molded climbing panel',loops,'blue')
    for i in range(12):
        z=.16+i//3*.29;x=(i%3-1)*.29+(.05 if i//3%2 else 0);y=-1.23+z/1.29*1.23-.055
        loops2=[[(x+r*math.cos(k*math.tau/7),y-d,z+r*.65*math.sin(k*math.tau/7)) for k in range(7)] for r,d in [(.058,0),(.073,.023),(.038,.066)]]
        loft(rt,'Rounded climbing hold',loops2,'yellow');bolt(rt,(x,y-.070,z),r=.005)
        empty(rt,rt.name+f'_HandFoot_{i}',(x,y-.07,z),'child_hand_foot')
    for x in (-.39,.39):cyl(rt,'Rock wall support',(x,-1.23,0),(x,-1.15,.25),.022,'steel',8)

def pole(rt):
    H=1.2192;top=H+1.60
    cyl(rt,'Fire pole dedicated anchored support',(.45,0,0),(.45,0,top),.0635,'steel',16)
    tube(rt,'Bent fire pole / 42mm OD',[(0,-.43,0),(0,-.43,top-.13),(0,-.39,top-.025),(.08,-.29,top+.035),(.32,-.10,top+.035),(.45,0,top-.05)],.021,'zinc',12)
    for z in (H+.12,H+.93):
        F.clamp(rt,.45,0,z)
        cyl(rt,'Fire pole standoff',(.45,-.08,z),(0,-.43,z),.022,'steel',8)
    empty(rt,rt.name+'_Hands',(0,-.43,H+.58),'child_hands')
    empty(rt,rt.name+'_DeckEntry',(0,0,H),'deck_entry')

def overhead(rt,rings=False):
    H=2.05;L=2.44
    for x in (-.43,.43):
        tube(rt,'Overhead ladder side',[(x,0,H),(x,-L,H),(x,-L-.15,H-.15),(x,-L-.15,0)],.026,'steel',10)
        for z in (.28,.54,.80):cyl(rt,'Access rung',(-.43,-L-.15,z),(.43,-L-.15,z),.0143,'rail',8)
    for x in (-.43,.43):cyl(rt,'Overhead near end supporting post',(x,0,0),(x,0,H),.034,'steel',10)
    for i in range(8):
        y=-.17-i*(L-.34)/7
        if rings:
            cyl(rt,'Overhead ring hanger',(0,y,H),(0,y,H-.16),.009,'zinc',8)
            tube(rt,'Hand ring',[(.115*math.cos(k*math.tau/12),y,H-.28+.115*math.sin(k*math.tau/12)) for k in range(13)],.0143,'rail',5)
        else:cyl(rt,'Horizontal ladder rung',(-.43,y,H),(.43,y,H),.0143,'rail',8)
        empty(rt,rt.name+f'_Hands_{i}',(0,y,H-.25 if rings else H),'child_hands')

def panel(rt,kind='wheel'):
    barrier(rt,True)
    if kind=='tic':
        # A three-by-three activity board uses its own drums as the infill.
        for o in list(rt.children):
            if 'Rounded molded infill' in o.name or ('Recessed M10' in o.name and abs(o.location.x)<.45):bpy.data.objects.remove(o,do_unlink=True)
    if kind=='wheel':
        p=empty(rt,rt.name+'_SteeringWheel',(0,-.11,.53),'',axis='Y',limits=(-180,180))
        tube(p,'Steering rim',[(.24*math.cos(i*math.tau/16),0,.24*math.sin(i*math.tau/16)) for i in range(17)],.028,'yellow',8,'Molded')
        for i in range(3):
            t=i*math.tau/3;cyl(p,'Steering spoke',(0,0,0),(.23*math.cos(t),0,.23*math.sin(t)),.021,'yellow',8,'Molded')
        cyl(p,'Steering boss',(0,.14,0),(0,-.04,0),.06,'yellow',12,'Molded')
    elif kind=='tic':
        box(rt,'Activity board lower closure',(0,0,.0475),(1.05,.027,.095),'blue',0,'Molded')
        for x in (-.46,.46):box(rt,'Activity board side closure',(x,0,.50),(.12,.027,.84),'blue',0,'Molded')
        for z in (.24,.51,.78):
            cyl(rt,'Tic-tac-toe spindle',(-.42,-.09,z),(.42,-.09,z),.009,'zinc',8)
            for x in (-.27,0,.27):
                p=empty(rt,rt.name+f'_Tumbler_{x}_{z}',(x,-.09,z),'',axis='X',limits=(-180,180))
                cyl(p,'Rotating play drum',(-.105,0,0),(.105,0,0),.11,'yellow',6,'Molded')
                # Original circle/cross symbols, sculptural and fictional.
                if x==0:tube(p,'Circle symbol',[(.05*math.cos(k*math.tau/8),-.107,.05*math.sin(k*math.tau/8)) for k in range(9)],.007,'blue',3,'Molded')
                else:
                    for s in (-1,1):cyl(p,'Cross symbol',(-.05,-.107,-s*.05),(.05,-.107,s*.05),.008,'blue',3,'Molded')
    else:
        box(rt,'Periscope mounting shelf',(0,-.09,.07),(.18,.22,.035),'steel',.005)
        cyl(rt,'Periscope swivel bearing',(0,-.15,.08),(0,-.15,.18),.082,'steel',12)
        p=empty(rt,rt.name+'_Periscope',(0,-.15,.16),'',axis='Z',limits=(-90,90))
        tube(p,'Compound periscope body',[(0,0,0),(0,-.11,.08),(0,0,.16),(0,0,.80),(0,-.13,.89),(0,-.20,.89)],.07,'yellow',10,'Molded')
        cyl(p,'Recessed scope lens',(0,-.204,.89),(0,-.209,.89),.043,'rubber',12,'Molded')

def swing_frame(rt):
    for x in (-SWING_BAY,0,SWING_BAY):
        for side in (-1,1):
            cyl(rt,'A frame 89mm tube leg',(x,side*1.16,0),(x,0,SWING_H),.04445,'steel',12)
        cyl(rt,'Cast A frame crown',(x-.13,0,SWING_H),(x+.13,0,SWING_H),.09,'steel',12)
    cyl(rt,'Two bay 127mm swing beam',(-SWING_BAY-SWING_OVERHANG,0,SWING_H),(SWING_BAY+SWING_OVERHANG,0,SWING_H),.0635,'steel',16)

def swing(rt,bucket=False):
    # Each seat is an independently reusable subassembly on its real beam axis.
    for x in (-.255,.255):
        lathe(rt,'Split beam hanger',[(x-.025,.0636),(x-.025,.077),(x+.025,.077),(x+.025,.0636)],'zinc',12,axis='X',closed=True)
        box(rt,'Hanger bearing yoke',(x,0,-.093),(.073,.065,.073),'zinc',.009)
        bolt(rt,(x,-.043,-.095))
    z=SWING_SEAT_Z-SWING_H if not bucket else .61-SWING_H
    p=empty(rt,rt.name+'_Pendulum',(0,0,-.13),'',axis='X',limits=(-55,55));p['motion_kind']='rigid_swing_with_chains'
    for side in (-1,1):
        x=side*.255
        # 6mm welded long-link steel; alternating elliptical open-center links.
        # End at each actual suspension attachment: raised belt end / bucket
        # upper rim, rather than the center sitting surface.
        end=z+.40 if bucket else z+.13+.095*(.255/.27)**2
        # True links at the hanger, crossed alpha strips down the long run.
        for i in range(5):
            zz=-(i+.5)*.045;pts=[]
            for k in range(9):
                a=k*math.tau/8;pts.append((x+(.009*math.cos(a) if i%2 else 0),(.009*math.cos(a) if not i%2 else 0),zz+.025*math.sin(a)))
            tube(p,'Connected 6mm swing chain link',pts,.003,'zinc',s=4)
        for axis in (0,1):
            w=.018;top=-.205;bot=end
            vs=[(x-w,0,bot),(x+w,0,bot),(x+w,0,top),(x-w,0,top)] if axis==0 else [(x,-w,bot),(x,w,bot),(x,w,top),(x,-w,top)]
            ob=F.own(F.G.mesh('Plastisol long chain / crossed alpha',vs,[(0,1,2,3)],F.M['Chain']),p,'rubber','Chain');ob['solid']=False
            uv=ob.data.uv_layers.active
            for loop,coord in zip(uv.data,[(0,0),(1,0),(1,(top-bot)/.72),(0,(top-bot)/.72)]):loop.uv=coord
    if bucket:
        # Continuous flexible bucket with two leg apertures made as a lattice
        # of compound curved strips, not holes painted on a solid block.
        ls=[]
        for h,r1,r2 in [(z+.13,.23,.17),(z+.35,.26,.20),(z+.40,.265,.205)]:ls.append([(r1*math.cos(i*math.tau/16),r2*math.sin(i*math.tau/16),h) for i in range(16)])
        ob=loft(p,'Tot bucket enclosing upper belt',ls,'rubber',mat='Molded',caps=False);m=ob.modifiers.new('Bucket molded thickness','SOLIDIFY');m.thickness=.014;F.G.apply(ob)
        box(p,'Bucket sitting saddle',(0,0,z+.13),(.42,.28,.035),'rubber',.016,'Molded')
        for x in (-.20,0,.20):tube(p,'Bucket leg separator',[(x,-.18,z+.28),(x,-.17,z+.08),(x,.17,z+.08),(x,.18,z+.28)],.032,'rubber',8,'Molded')
    else:
        loops=[]
        for j in range(9):
            x=-.27+.54*j/8;h=z+.13+.095*(abs(x)/.27)**2
            loops.append([(x,-.105,h),(x,.105,h),(x,.108,h-.018),(x,-.108,h-.018)])
        loft(p,'Flexible sagged belt seat',loops,'rubber')
    empty(p,rt.name+'_SeatSocket',(0,0,z+.13),'child_seat')

def spring(rt):
    box(rt,'Buried spring anchor cap',(0,0,.035),(.28,.24,.07),'zinc',.009)
    pts=[(.095*math.cos(t),.095*math.sin(t),.09+.36*i/80) for i,t in enumerate([i*10*math.pi/80 for i in range(81)])]
    tube(rt,'Five turn 22mm coil spring',pts,.011,'zinc',6)
    p=empty(rt,rt.name+'_Rider',(0,0,.46),'',axis='X',limits=(-14,14));p['secondary_axis']='Y';p['secondary_range_degrees']=[-12,12]
    # Molded animal form as four rounded cross sections with compound volume.
    ls=[]
    for y,w,h,z in [(-.45,.08,.12,.22),(-.36,.13,.25,.28),(-.16,.16,.19,.17),(.15,.18,.14,.08),(.37,.10,.10,.09)]:
        ls.append([(w*math.cos(i*math.tau/12),y,z+h*math.sin(i*math.tau/12)) for i in range(12)])
    loft(p,'Compound molded spring pony',ls,'blue')
    box(p,'Saddle seat',(0,.10,.22),(.30,.35,.045),'yellow',.020,'Molded')
    cyl(p,'Rider hand grip',(-.24,-.29,.40),(.24,-.29,.40),.0143,'yellow',8,'Molded')
    cyl(p,'Rider foot rest',(-.27,-.20,-.02),(.27,-.20,-.02),.019,'steel',8)
    for x in (-.115,.115):cyl(p,'Pony eye',(x,-.36,.36),(x*1.1,-.36,.36),.018,'rubber',8,'Molded')
    empty(p,rt.name+'_Seat',(0,.1,.245),'child_seat')
    for x in (-.22,.22):
        empty(p,rt.name+f'_Hand_{x}',(x,-.29,.40),'child_hand');empty(p,rt.name+f'_Foot_{x}',(x,-.20,-.02),'child_foot')

def spinner(rt):
    cyl(rt,'Buried spinner stationary column',(0,0,0),(0,0,.55),.07,'zinc',12)
    p=empty(rt,rt.name+'_Roundabout',(0,0,.27),'',axis='Z',limits=(-180,180))
    lathe(p,'Rolled circular plastisol deck',[(-.07,0),(-.07,.88),(-.02,.94),(0,.94),(.015,.88),(.015,0)],'deck',48,mat='Frame')
    for i in range(4):
        a=i*math.pi/2;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0))
        pts=[u*.73+v*.19+Vector((0,0,.02)),u*.73+v*.19+Vector((0,0,.61)),u*.38+v*.19+Vector((0,0,.67)),u*.14+v*.19+Vector((0,0,.61)),u*.14+v*.19+Vector((0,0,.02))]
        tube(p,'Roundabout bent handrail',pts,.019,'rail',8)
        empty(p,rt.name+f'_Hands_{i}',tuple(u*.52+v*.19+Vector((0,0,.66))),'child_hands')

def ramp_segment(rt):
    # One 48-inch bay of an accessible six-bay, 1:12 route, origin at upper lip.
    L=1.2192;w=1.30;rise=.1016
    pts=[(-w/2,-L,-rise),(w/2,-L,-rise),(w/2,0,0),(-w/2,0,0),(-w/2,-L,-rise-.07),(w/2,-L,-rise-.07),(w/2,0,-.07),(-w/2,0,-.07)]
    F.own(F.G.mesh('Ramp punched tray / 1:12',pts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],F.M['Deck']),rt,'deck','Deck')
    for x in (-w/2,w/2):
        for h in (.66,.90):tube(rt,'Dual height ramp handrail',[(x,-L,h-rise),(x,0,h)],GRIP_OD/2,'rail',8)
        for i in range(13):
            y=-L+i*L/12;z=rise*y/L;cyl(rt,'Nonclimbable ramp infill',(x,y,z+.065),(x,y,z+.90),.0095,'rail',6)
        cyl(rt,'Ramp support post',(x,0,-.70),(x,0,.93),.025,'steel',8)
        tube(rt,'Ramp wheel curb',[(x,-L,.045-rise),(x,0,.045)],.025,'deck',6)
    empty(rt,rt.name+'_Upper',(0,0,0),'ramp_joint');empty(rt,rt.name+'_Lower',(0,-L,-rise),'ramp_joint')
    rt['slope_ratio']=1/12;rt['clear_width_m']=w-GRIP_OD

def landing(rt):
    box(rt,'Accessible 60 inch turning landing',(0,0,-.04),(1.524,1.524,.08),'deck',.004,mat='Deck')

def interdeck(rt):
    # Compact original 24 inch connector, 3 closed eight-inch risers.
    for i in range(3):
        y=-.36+i*.24;z=(i+1)*.2032
        box(rt,'Interdeck closed riser',(0,y+.115,z-.1016),(1.05,.025,.2032),'deck',.002)
        if i<2:box(rt,'Interdeck stair tread',(0,y,z-.018),(1.05,.24,.036),'deck',.003)
    for x in (-.51,.51):tube(rt,'Interdeck grip',[(x,-.46,.65),(x,.40,1.27)],.0143,'rail',8)

def roof_riser(rt):
    cyl(rt,'Roof supported post extension',(0,0,-.02),(0,0,.36),.0635,'steel',16)


def neck_guard(rt):
    # Solid short infill beside the accessible landing neck / ramp mouth.
    box(rt,'Landing transition closed guard',(0,0,.49),(.29,.030,.96),'blue',.008,'Molded')
    for x in (-.115,.115):
        for z in (.11,.87):bolt(rt,(x,-.020,z))

def interface_bridge(rt,height,width=.9):
    """Bolted steel/plastisol tongue across the 63.5mm post-center setback."""
    box(rt,'Bolted deck interface tongue',(0,.07,height-.009),(width,.16,.018),'deck',.003)
    for x in (-width*.34,width*.34):bolt(rt,(x,.12,height),(0,0,1),.006)
    empty(rt,rt.name+'_DeckInterface',(0,.12,height),'deck_interface')

def ramp_head_bridge(rt):interface_bridge(rt,0,1.30)
