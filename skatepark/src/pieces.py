"""Poured and fabricated ride geometry, parameterized from cited sections."""
import math,json
import bpy
from mathutils import Vector
from geometry import *
FT=.3048
COPING=.060325

def angle_edge(rt,n,x,y,z,length,axis='Y'):
    # One bent 3/16 inch angle with a continuous outside arris.
    a=.0508;t=.0047625
    pts=[(0,0),(-a,0),(-a,-t),(-t,-t),(-t,-a),(0,-a)]
    o=profile(n,pts,-length/2,length/2,rt,'Steel',axis='Y')
    o.location=(x,y,z)
    if axis=='X':o.rotation_euler.z=-math.pi/2
    return o

def quarter(name='Quarter_4ft',h=4*FT,r=7*FT,w=16*FT,deck=5*FT,prefab=False):
    rt=root(name);a=math.acos(1-h/r);run=r*math.sin(a);N=40
    curve=[(-run/2+r*math.sin(t*a/N),r*(1-math.cos(t*a/N))) for t in range(N+1)]
    if not prefab:
        profile(name+' formed concrete',curve+[(run/2+deck,h),(run/2+deck,-.15),(-run/2,-.15)],-w/2,w/2,rt)
        # Smooth only the curved riding faces; vertical end returns stay flat.
        ob=rt.children[0]
        for p in ob.data.polygons:
            if p.normal.z>.01 and abs(p.normal.x)<.1:p.use_smooth=True
    else:
        # Hollow steel rib frame, enclosed in ventilated panels, 6mm riding sheet.
        for x in (-w/2+.04,0,w/2-.04):
            path=[(x,y+.065*math.sin(a*j/N),z-.065*math.cos(a*j/N)) for j,(y,z) in enumerate(curve) if j%4==0]
            tube('Curved 50mm steel stringer',path,.025,rt,'Zinc',8)
            for y in (-run/2+.3,run/2-.15,run/2+deck-.08):
                top=h-.045 if y>run/2 else r-math.sqrt(max(0,r*r-(y+run/2)**2))-.045
                if top>.08:beam('Square tube uprights',(x,y,.04),(x,y,top),.0508,rt)
            beam('Lower perimeter', (x,-run/2+.65,.0254),(x,run/2+deck-.08,.0254),.0508,rt)
        for j in range(1,10):
            y,z=curve[j*4];theta=a*j*4/N;y+=.075*math.sin(theta);z-=.075*math.cos(theta)
            beam('Transverse 50mm joist',(-w/2,y,z),(w/2,y,z),.0508,rt)
        # Panels are assembled separately; seams are real 2mm gaps.
        for k in range(4):
            xa=-w/2+k*w/4+.001;xb=xa+w/4-.002
            prof=curve[4:];verts=[(x,y,z) for x in (xa,xb) for y,z in prof];L=len(prof)
            ob=mesh('6mm phenolic riding sheet',verts,[(j,j+L,j+L+1,j+1) for j in range(L-1)],rt,'Composite',True)
            mesh('Separate deck riding sheet',[(xa,run/2+.006,h),(xb,run/2+.006,h),(xb,run/2+deck,h),(xa,run/2+deck,h)],[(0,1,2,3)],rt,'Composite')
            # Gauge belongs underneath the riding surface.
            # Exposed 6mm end gauges; the enclosed underside has no wasted skin.
            for j in (0,L-1):
                ya,za=prof[j];mesh('6mm sheet end gauge',[(xa,ya,za),(xb,ya,za),(xb,ya,za-.006),(xa,ya,za-.006)],[(0,1,2,3)],rt,'Composite')
            for j in (5,12,20,29,38):
                y,z=curve[j];t=a*j/N;normal=Vector((0,-math.sin(t),math.cos(t)))
                for x in (xa+.04,xb-.04):
                    p=Vector((x,y,z))+normal*.0002
                    cyl('Recessed riding screw',p-normal*.001,p,.0048,rt,'Zinc',6)
        for x in (-w/2,w/2):
            profile('Galvanized side enclosure',curve+[(run/2+deck,h),(run/2+deck,.015),(-run/2,.015)],x-.0015,x+.0015,rt,'Paint')
            for j in range(5):
                y=-run/2+.60+j*(run+deck-.70)/4
                top=h if y>=run/2 else r-math.sqrt(max(0,r*r-(y+run/2)**2))
                if top>.09:
                    s=1 if x>0 else -1;cyl('Side panel tamper resistant fastener',(x,y,top*.48),(x+s*.004,y,top*.48),.0055,rt,'Zinc',6)
            # Open horizontal ventilation gaps in the rear panel.
        for z in (.10,.35,.60,.85,1.10):
            if z<h:box('Rear ventilated enclosure',(0,run/2+deck,z),(w,.003,.20),rt,'Paint',0)
        back_y,back_z=curve[4];front_y=-run/2-.15
        profile('3mm flush bottom transition plate',[(front_y,.0003),(back_y,back_z),(back_y,back_z-.003),(front_y,-.0027)],-w/2,w/2,rt,'Zinc')
        for x in (-w/2+.05,w/2-.05):
            for y in (-run/2-.10,run/2+.10):cyl('Base anchor',(x,y,.002),(x,y,.012),.008,rt,'Zinc',6)
        # Rear deck guard: vertical pickets, measured 42-inch height.
        gy=run/2+deck-.04
        for x in (-w/2,0,w/2):beam('Guard posts',(x,gy,h),(x,gy,h+1.0668),.05,rt,'Paint')
        beam('Guard top',(-w/2,gy,h+1.0668),(w/2,gy,h+1.0668),.05,rt,'Paint')
        for j in range(1,40):beam('Vertical guard picket',(-w/2+j*w/40,gy,h+.12),(-w/2+j*w/40,gy,h+1.04),.019,rt,'Paint')
    # Reveal 9.5mm above deck and beyond riding tangent; circular OD is real.
    cyl('2-3/8 inch coping',(-w/2,run/2-.0206,h-.0206),(w/2,run/2-.0206,h-.0206),COPING/2,rt,s=20)
    socket(rt,'Approach',(0,-run/2,0));socket(rt,'Deck',(0,run/2+deck,h),kind='grid_connection')
    return describe(rt,[w,run+deck],height_m=h,transition_radius_m=r,deck_m=deck,profile_run_m=run,ground_cut_json=json.dumps([] if prefab else [[-w/2,w/2,-run/2,run/2+deck]]),construction='steel frame / 6mm composite' if prefab else 'formed reinforced concrete')

def bank(name='Bank_3ft',h=3*FT,w=16*FT,deck=5*FT,angle=20,rail=False):
    rt=root(name);rad=.18;t=math.radians(angle);run=h/math.tan(t)+rad*math.tan(t/2);toe=-run/2;lip=run/2
    # 180mm toe fillet, tangent to the 20deg plane.
    fillet=[(toe+rad*math.sin(t*j/8),rad*(1-math.cos(t*j/8))) for j in range(9)]
    profile('Bank continuous pour',fillet+[(lip,h),(lip+deck,h),(lip+deck,-.15),(toe,-.15)],-w/2,w/2,rt)
    angle_edge(rt,'Bank lip steel armor',0,lip,h,w,'X')
    if rail:
        y0=toe-.40;y1=lip+.45;z0=.56;z1=h+.56
        tube('Welded round down rail',[(0,y0-.15,z0),(0,y0,z0),(0,y1,z1),(0,y1+.15,z1)],.0254,rt,s=16)
        for t in (.16,.85):
            y=y0+(y1-y0)*t;z=z0+(z1-z0)*t
            base=max(0,min(h,h-(lip-y)*math.tan(math.radians(angle))))
            cyl('Downrail welded support',(0,y,base),(0,y,z),.021,rt,s=12)
    socket(rt,'Approach',(0,toe,0));socket(rt,'Deck',(0,lip+deck,h),kind='grid_connection')
    return describe(rt,[w,run+deck],height_m=h,bank_angle_degrees=angle,deck_m=deck,ground_cut_json=json.dumps([[-w/2,w/2,toe,lip+deck]]))

def ledge(name='Ledge_18in',h=1.5*FT,w=2*FT,length=12*FT,prefab=False):
    rt=root(name)
    if prefab:
        for x in (-w/2+.025,w/2-.025):
            for y in (-length/2+.1,0,length/2-.1):beam('Welded grindbox legs',(x,y,0),(x,y,h-.02),.05,rt,'Paint')
        box('Composite grindbox lid',(0,0,h-.003),(w,length,.006),rt,'Composite',0)
        for x in (-w/2,w/2):box('Grindbox side',(x,0,h/2),(.003,length,h),rt,'Paint',0)
    else:box('Cast ledge body',(0,0,h/2),(w,length,h),rt,r=.004)
    for s in (-1,1):
        ob=angle_edge(rt,'2 inch angle armor',s*w/2,0,h,length)
        if s<0:ob.rotation_euler.z=math.pi
    for y in (-length/2+.04,length/2-.04):
        for x in (-w/2+.04,w/2-.04):cyl('Armor recessed fixing',(x,y,h-.002),(x,y,h+.0005),.004,rt,'Steel',6)
    socket(rt,'Line_In',(0,-length/2-3,0));socket(rt,'Line_Out',(0,length/2+3,0))
    return describe(rt,[w,length],height_m=h,angle_leg_m=.0508,angle_gauge_m=.0047625,ground_cut_json=json.dumps([] if prefab else [[-w/2,w/2,-length/2,length/2]]))

def manual():
    rt=root('ManualPad');w,l,h=6*FT,12*FT,FT
    box('Manual pad monolithic pour',(0,0,h/2),(w,l,h),rt,r=.006)
    for s in (-1,1):angle_edge(rt,'Pad edge armor',s*w/2,0,h,l)
    socket(rt,'Line_In',(0,-l/2-3,0));socket(rt,'Line_Out',(0,l/2+3,0))
    return describe(rt,[w,l],height_m=h,ground_cut_json=json.dumps([[-w/2,w/2,-l/2,l/2]]))

def stairs(n=4):
    rt=root('Stairs_'+str(n));rise=.1524;tread=.3048;w=3.048;landing=2.4384;run=n*tread;h=n*rise
    # upper deck is +Y, descent toward -Y. Each riser belongs to a single solid.
    poly=[(-run/2,-.15),(-run/2,0)]
    for i in range(n):poly += [(-run/2+i*tread,(i+1)*rise),(-run/2+(i+1)*tread,(i+1)*rise)]
    poly += [(run/2+landing,h),(run/2+landing,-.15)]
    profile('Stair and upper landing pour',poly,-w/2,w/2,rt)
    # Handrail has horizontal extensions and rounded returns, not unsupported poles.
    y0=-run/2-.35;y1=run/2+.40;z0=.70;z1=h+.70
    path=[(0,y0-.18,z0-.16),(0,y0-.18,z0-.04),(0,y0-.14,z0),(0,y0,z0),(0,y1,z1),(0,y1+.18,z1)]
    tube('2 inch OD stair rail',path,.0254,rt,s=16)
    for y,base in ((-run/2+.12,rise),(run/2+.2,h)):
        z=z0+(z1-z0)*(y-y0)/(y1-y0)
        cyl('Embedded stair rail post',(0,y,base),(0,y,z),.022225,rt,s=14)
    # Hubba is at stair side, rises with the slope, and continues on the landing.
    x=w/2+.20;hl=.42
    profile('Hubba cast body',[(-run/2,0),(-run/2,hl),(run/2,h+hl),(run/2+1.0,h+hl),(run/2+1.0,0)],x-.20,x+.20,rt)
    beam('Hubba steel top armor',(x,-run/2,hl),(x,run/2,h+hl),.4064,rt,'Steel',.00635)
    box('Hubba landing armor',(x,run/2+.5,h+hl),(.4064,1,.00635),rt,'Steel',0)
    for y in (-run/2,run/2):socket(rt,'Ride_'+str(y),(w*.25,y+(-3 if y<0 else 3),0 if y<0 else h))
    socket(rt,'Landing',(0,run/2+landing,h),kind='grid_connection')
    return describe(rt,[w+.4,run+landing],riser_m=rise,tread_m=tread,height_m=h,steps=n,rail_od_m=.0508,ground_cut_json=json.dumps([[-w/2,w/2,-run/2,run/2+landing],[x-.2,x+.2,-run/2,run/2+1.0],[-w/2,w/2,run/2+landing,run/2+landing+h/math.tan(math.radians(20))]]))

def flatrail(name='FlatBar',length=12*FT,h=1.5*FT):
    rt=root(name);box('Rectangular 2x3 inch grind tube',(0,0,h),(.0508,length,.0762),rt,'Steel',.004)
    for y in (-length*.36,length*.36):
        cyl('Rail welded stanchion',(0,y,.01),(0,y,h-.0381),.0222,rt,s=12)
        box('Rail bolt flange',(0,y,.006),(.18,.22,.012),rt,'Steel',.004)
        for x in (-.065,.065):cyl('Recessed slab anchor',(x,y,.012),(x,y,.021),.007,rt,'Zinc',6)
    socket(rt,'Line_In',(0,-length/2-3,0));socket(rt,'Line_Out',(0,length/2+3,0))
    return describe(rt,[.18,length],height_m=h,rail_section_m=[.0508,.0762])

def pyramid(name='Pyramid',h=.762,prefab=False):
    rt=root(name);topx,topy=1.2192,1.8288;run=h/math.tan(math.radians(20));wx=topx+run;wy=topy+run
    v=[(-wx,-wy,0),(wx,-wy,0),(wx,wy,0),(-wx,wy,0),(-topx,-topy,h),(topx,-topy,h),(topx,topy,h),(-topx,topy,h)]
    ob=mesh('Four 20 degree banks and flat top',v,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],rt,'Composite' if prefab else 'Concrete')
    if prefab:
        for a,b in ((0,4),(1,5),(2,6),(3,7)):
            beam('Box section hip frame',v[a],v[b],.0508,rt)
        for x in (-topx,topx):
            for y in (-topy,topy):beam('Funbox upright',(x,y,0),(x,y,h-.006),.0508,rt)
        for j in range(9):
            t=j/8;y=-wy+(wy-topy)*t;z=h*t
            beam('Funbox transverse framing',(-wx+(wx-topx)*t,y,z-.035),(wx-(wx-topx)*t,y,z-.035),.05,rt)
        for s in (-1,1):box('Funbox bottom steel plate',(0,s*(wy-.1),.0015),(2*wx,.3,.003),rt,'Zinc',0)
    # Low rectangular grind box on one shoulder, independent ride path beside it.
    for x in (-topx,topx):beam('Funbox top arris',(x,-topy,h),(x,topy,h),.05,rt,'Steel',.00635)
    socket(rt,'Approach',(0,-wy-3,0));socket(rt,'Exit',(0,wy+3,0))
    return describe(rt,[wx*2,wy*2],height_m=h,bank_angle_degrees=20,ground_cut_json=json.dumps([] if prefab else [[-wx,wx,-wy,wy]]))

def spine():
    h,r,w=5*FT,5*FT,12*FT;rt=root('Spine_5ft');a=math.acos(1-h/r);run=r*math.sin(a)
    # True back-to-back transitions meet at one coping; no impossible vertical fin.
    left=[(-run+r*math.sin(a*j/40),r*(1-math.cos(a*j/40))) for j in range(41)]
    poly=left+[(-y,z) for y,z in reversed(left[:-1])]+[(run,-.15),(-run,-.15)]
    profile('Back to back formed transitions',poly,-w/2,w/2,rt)
    cyl('Shared spine coping',(-w/2,0,h),(w/2,0,h),COPING/2,rt,s=20)
    socket(rt,'Approach',(0,-run,0));socket(rt,'Exit',(0,run,0))
    return describe(rt,[w,2*run],height_m=h,transition_radius_m=r,ground_cut_json=json.dumps([[-w/2,w/2,-run,run]]))

def hip():
    rt=root('Hip_90');r=7*FT;h=4*FT;a=math.acos(1-h/r);run=r*math.sin(a);v=[];f=[];N=20;K=30
    # Convex 90-degree corner transition, radial sections meet adjacent quarters.
    for j in range(N+1):
        t=a*j/N;rho=run-r*math.sin(t)
        for k in range(K+1):
            phi=k*math.pi/2/K;v.append((rho*math.cos(phi),rho*math.sin(phi),r*(1-math.cos(t))))
    for j in range(N):
        for k in range(K):
            i=j*(K+1)+k;f.append((i,i+1,N*(K+1)) if j==N-1 else (i,i+1,i+K+2,i+K+1))
    mesh('Radial hip transition',v,f,rt,smooth=True)
    return describe(rt,[run,run],height_m=h,transition_radius_m=r)

def launch():return quarter('Prefab_Launch',h=.762,r=2.4384,w=2.4384,deck=.6096,prefab=True)

def library():
    return [quarter(),quarter('Quarter_5ft',5*FT,8*FT),bank(),bank('Bank_Rail',rail=True),ledge(),manual(),stairs(),stairs(5),flatrail(),pyramid(),spine(),hip(),quarter('Prefab_Quarter',prefab=True),launch(),ledge('Prefab_GrindBox',prefab=True),pyramid('Prefab_Funbox',prefab=True)]
