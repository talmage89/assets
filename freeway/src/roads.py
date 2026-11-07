"""Alignment-driven surface skins, speed-change lanes, ramps and earthwork."""
import math,random
from mathutils import Vector
import geom as Q
from plan import *

def seq(a,b,step):
    n=max(1,math.ceil((b-a)/step));return [a+(b-a)*i/n for i in range(n+1)]

def auxiliary(p,s):
    if p.kind!='diamond':return 0
    a=abs(s)
    if a<280 or a>737.44:return 0
    return LANE*min(1,(737.44-a)/91.44)

def patch(b,p,s0,s1,u0,u1,role='White',lift=.006):
    b.surface([p.xyz(s0,u0,lift),p.xyz(s0,u1,lift),p.xyz(s1,u1,lift),p.xyz(s1,u0,lift)],role)

def road(p,name,s0,s1,mark=True,bank=None):
    if bank is not None:
        original=p
        class Transition:
            def __getattr__(self,key):return getattr(original,key)
            def xyz(self,s,u,z=0):
                c=original.center(s);n,_=original.frame(s);e=bank[0]+(bank[1]-bank[0])*(s-s0)/(s1-s0)
                return (c[0]+n[0]*u,c[1]+n[1]*u,c[2]+e*u+z)
        p=Transition()
    rt=Q.root(name,module_kind='roadway',station_start=s0,station_end=s1);b=Q.Batch(name+'__Mesh',rt)
    if bank is not None:rt['bank_start_end']=list(bank)
    joints=[j*JOINT for j in range(math.floor(s0/JOINT)+1,math.ceil(s1/JOINT)) if s0<j*JOINT<s1]
    stations=sorted(set([s0,s1]+joints+[v for v in (280.,646.,737.44,-280.,-646.,-737.44) if s0<v<s1]))
    rng=random.Random(p.seed*10000+round(s0*100))
    for a,c in zip(stations,stations[1:]):
        for side in (-1,1):
            m=p.median/2;edges=[m,m+LEFT,m+LEFT+LANE,m+LEFT+2*LANE]
            for k,(ua,ub) in enumerate(zip(edges,edges[1:])):
                # Concrete joints are sealed visible lines laid over the base
                # at 15 ft intervals; top-level skins remain continuous.
                color=1 if p.pavement=='Asphalt' else rng.uniform(.89,1.015)
                b.surface([p.xyz(a,side*ua),p.xyz(a,side*ub),p.xyz(c,side*ub),p.xyz(c,side*ua)],p.pavement,tint=(color,color,color,1))
            edge=edges[-1];aa=auxiliary(p,a);ac=auxiliary(p,c)
            b.surface([p.xyz(a,side*edge),p.xyz(a,side*(edge+aa+RIGHT)),p.xyz(c,side*(edge+ac+RIGHT)),p.xyz(c,side*edge)],'Asphalt')
            if p.pavement=='Concrete' and abs(a/JOINT-round(a/JOINT))<1e-5:
                patch(b,p,a,a+.012,side*m,side*edge,'Joint',.001)
            if p.pavement=='Concrete':
                for u in edges[1:]:patch(b,p,a,c,side*(u-.004),side*(u+.004),'Joint',.0015)
            else:
                # Paver longitudinal joint on the lane division, fine enough
                # to read at shoulder distance rather than as a black stripe.
                u=side*(m+LEFT+LANE);patch(b,p,a,c,u-.009,u+.009,'Joint',.001)
    if mark:
        for side in (-1,1):
            u=side*(p.median/2+LEFT)
            patch(b,p,s0,s1,u-LINE/2,u+LINE/2,'Yellow')
            edge=p.median/2+LEFT+2*LANE
            for a,c in zip(stations,stations[1:]):
                ua=side*(edge+auxiliary(p,a));uc=side*(edge+auxiliary(p,c))
                b.surface([p.xyz(a,ua-LINE/2,.006),p.xyz(a,ua+LINE/2,.006),p.xyz(c,uc+LINE/2,.006),p.xyz(c,uc-LINE/2,.006)],'White')
            u=side*(p.median/2+LEFT+LANE)
            for j in range(math.floor(s0/CYCLE),math.ceil(s1/CYCLE)):
                a=max(s0,j*CYCLE);c=min(s1,j*CYCLE+DASH)
                if c>a:patch(b,p,a,c,u-LINE/2,u+LINE/2)
                # Raised marker after the dash, outside marking paint.
                s=j*CYCLE+DASH+.5
                if s0<=s<s1:
                    pt=p.xyz(s,u,.012);b.box(pt,(.10,.10,.018),'White')
            # Wide dotted line separates an added lane from through traffic.
            for j in range(math.floor(s0/(12*FT)),math.ceil(s1/(12*FT))):
                a=max(s0,j*12*FT);c=min(s1,j*12*FT+3*FT)
                if c>a and auxiliary(p,(a+c)/2)>0:
                    u=side*edge;patch(b,p,a,c,u-LINE,u+LINE)
            # Milled rumble forms at 12 in pitch: geometry cards at the gate,
            # replaced by the extended Ground normal/decal strip at look-dev.
            for s in seq(s0,s1-.3048,.3048):
                u=side*(edge+auxiliary(p,s)+.3048+.4064/2)
                patch(b,p,s,s+.1778,u-.2032,u+.2032,'Drain',.001)
    b.finish();Q.socket(rt,'S',p.center(s0));Q.socket(rt,'N',p.center(s1))
    return rt

def ramp(p,name,side,entry=False):
    pts=ramp_points(p,side,entry);rt=Q.root(name,module_kind='ramp');b=Q.Batch(name+'__Mesh',rt)
    # 16 ft single ramp, 4 ft inner and 6 ft outer shoulder. Tapers into the
    # mainline aux lane at the low end and flares for queueing at the terminal.
    for i,(a,c) in enumerate(zip(pts,pts[1:])):
        def cross(v,index):
            pre=pts[max(0,index-1)];post=pts[min(len(pts)-1,index+1)]
            d=Vector((post[0]-pre[0],post[1]-pre[1],0)).normalized()
            n=Vector((d.y,-d.x,0));return n
        na,nc=cross(a,i),cross(c,i+1)
        def pp(v,n,u,extra=0):
            pt=Vector(v)+n*u;pt.z-=abs(u)*.02;pt.z+=extra
            # Shoulder clipping at the merge removes duplicated mainline faces.
            if abs(v[1])>228 and abs(pt.x)<p.edge+.01:
                pt.x=side*(p.edge+.01)
            return pt
        left=-3.6576;right=4.2672
        b.surface([pp(a,na,left),pp(a,na,right),pp(c,nc,right),pp(c,nc,left)],'Asphalt')
        for u,ma in [(-2.4384,'Yellow'),(2.4384,'White')]:
            b.surface([pp(a,na,u-LINE/2,.006),pp(a,na,u+LINE/2,.006),pp(c,nc,u+LINE/2,.006),pp(c,nc,u-LINE/2,.006)],ma)
    b.finish();Q.curve(rt,name,pts);Q.socket(rt,'Start',pts[0]);Q.socket(rt,'End',pts[-1]);return rt

def terrain(p):
    rt=Q.root('Earthwork',module_kind='terrain');b=Q.Batch('Cut slopes and drainage',rt)
    stations=seq(-p.length/2,p.length/2,8.)
    for side in (-1,1):
        for a,c in zip(stations,stations[1:]):
            def section(s):
                edge=p.edge+auxiliary(p,s);ground=7.0 if p.kind=='diamond' else 0.
                base=p.xyz(s,side*edge)[2]
                inner=[(side*edge,base-.015),(side*(edge+1.6),base-.36),(side*(edge+3.0),base-.36)]
                # In the diamond, terrain actually follows the ramp elevation.
                if p.kind=='diamond' and 16<=abs(s)<=280:
                    entry=(s*side)>0;rows=ramp_points(p,side,entry,192)
                    q=min(rows,key=lambda v:abs(v[1]-s));u=abs(q[0]);h=q[2]
                    inside=max(edge+3.05,u-4.4);outside=u+4.9
                    return inner+[(side*inside,h-.10),(side*outside,h-.10),(side*max(outside+1,110),ground),(side*2400,ground)]
                return inner+[(side*(edge+max(12.,abs(ground-base)*4)),ground),(side*110,ground),(side*220,ground),(side*2400,ground)]
            aa,cc=section(a),section(c)
            for j in range(6):
                # Leave a real corridor for the branch paving. The narrow
                # earth shoulder is closed below the ramp, not across its top.
                if p.kind=='diamond' and 16<=abs((a+c)/2)<=280 and j==3:continue
                u0,z0=aa[j];u1,z1=aa[j+1];v0,h0=cc[j];v1,h1=cc[j+1]
                def pos(s,u,z):
                    v=list(p.xyz(s,u));v[2]=z;return v
                ma='Drain' if j==1 else 'Lawn'
                b.surface([pos(a,u0,z0),pos(a,u1,z1),pos(c,v1,h1),pos(c,v0,h0)],ma,tint=(.83,.87,.76,1))
    # End extensions use the same grade and width. They create real horizon
    # continuity in the two eye-height heroes, rather than a backdrop at fence.
    for a,c in [(-p.length/2-1800,-p.length/2),(p.length/2,p.length/2+1800)]:
        for side in (-1,1):
            b.surface([p.xyz(a,side*p.median/2),p.xyz(a,side*p.edge),p.xyz(c,side*p.edge),p.xyz(c,side*p.median/2)],p.pavement)
        for u0,u1 in [(-2400,-p.edge),(p.edge,2400)]:
            ground=7.0 if p.kind=='diamond' else 0
            points=[p.xyz(a,u0),p.xyz(a,u1),p.xyz(c,u1),p.xyz(c,u0)]
            b.surface([(x,y,ground) for x,y,z in points],'Lawn',tint=(.8,.84,.73,1))
    b.finish();return rt

def arterial(p):
    rt=Q.root('JuniperArterial',module_kind='arterial');b=Q.Batch('Five lane arterial and approaches',rt)
    # Bridge owns -30..30. The approaches are full skins; terminal branch
    # paving reaches the edge rather than ending behind an arbitrary curb.
    for xa,xb in [(-420,-30),(30,420)]:
        for ya,yb in [(-10.668,-8.382),(-8.382,0),(0,8.382),(8.382,10.668)]:
            z0=BRIDGE_Z-.02*min(abs(ya),8.382);z1=BRIDGE_Z-.02*min(abs(yb),8.382)
            walk=abs(ya+yb)>=16.7;segments=[(xa,xb)]
            if walk:
                for tx in (-p.terminal,p.terminal):
                    new=[]
                    for a,c in segments:
                        lo,hi=tx-16.60,tx+16.60
                        if c<=lo or a>=hi:new.append((a,c))
                        else:
                            if a<lo:new.append((a,lo))
                            if c>hi:new.append((hi,c))
                    segments=new
            for a,c in segments:b.surface([(a,ya,z0),(c,ya,z0),(c,yb,z1),(a,yb,z1)],'Concrete' if walk else 'Asphalt')
    # Continuous two-way center lane: paired double yellow, with broken
    # inner lines. No incompatible freeway white/yellow pattern is reused.
    for y in (-1.6764,1.6764):
        for sign in (-1,1):
            yy=y+sign*.10
            spans=[(-420,420)] if sign==(1 if y>0 else -1) else [(x,x+3.048) for x in seq(-420,416,12.192)]
            for xa,xb in spans:b.surface([(xa,yy-.05,BRIDGE_Z-.02*abs(yy)+.008),(xb,yy-.05,BRIDGE_Z-.02*abs(yy)+.008),(xb,yy+.05,BRIDGE_Z-.02*abs(yy)+.008),(xa,yy+.05,BRIDGE_Z-.02*abs(yy)+.008)],'Yellow')
    for y in (-5.0292,5.0292):
        for x in seq(-420,417,12.192):
            b.surface([(x,y-.0762,BRIDGE_Z-.02*abs(y)+.008),(x+3.048,y-.0762,BRIDGE_Z-.02*abs(y)+.008),(x+3.048,y+.0762,BRIDGE_Z-.02*abs(y)+.008),(x,y+.0762,BRIDGE_Z-.02*abs(y)+.008)],'White')
    for sx in (-1,1):
        for sy in (-1,1):
            if sx*sy<0: # off-ramp incoming approach only
                x=sx*p.terminal;y=sy*14.0;z=7.18236+(14-8.382)/(16-8.382)*(7.35-7.18236)+.006
                b.surface([(x-2.4384,y-.3048,z),(x+2.4384,y-.3048,z),(x+2.4384,y+.3048,z),(x-2.4384,y+.3048,z)],'White')
        for dx,ya,yb in [(-18.,-8.382,-1.68),(18.,1.68,8.382)]:
            x=sx*p.terminal+dx
            b.surface([(x-.3048,ya,BRIDGE_Z-.02*abs(ya)+.006),(x+.3048,ya,BRIDGE_Z-.02*abs(ya)+.006),(x+.3048,yb,BRIDGE_Z-.02*abs(yb)+.006),(x-.3048,yb,BRIDGE_Z-.02*abs(yb)+.006)],'White')
        # Actual paved terminal intersection joins off/on branches through
        # the arterial sidewalk reservation; two 40 ft radius fillets.
        for sy in (-1,1):
            b.surface([(sx*p.terminal-4.4,sy*8.382,7.18),(sx*p.terminal+4.4,sy*8.382,7.18),(sx*p.terminal+4.4,sy*16,7.35),(sx*p.terminal-4.4,sy*16,7.35)],'Asphalt')
            for turn in (-1,1):
                radius=12.192;cx=sx*p.terminal+turn*(4.4+radius);cy=sy*(8.382+radius)
                arc=[]
                for j in range(13):
                    t=j/12*math.pi/2
                    x=cx-turn*radius*math.cos(t);y=cy-sy*radius*math.sin(t)
                    z=7.18236+max(0,min(1,(abs(y)-8.382)/(16-8.382)))*.16764
                    arc.append((x,y,z))
                corner=(sx*p.terminal+turn*4.4,sy*8.382,7.18236)
                for aa,cc in zip(arc,arc[1:]):b.surface([corner,aa,cc],'Asphalt')
                # Cast curb and a walk follow the curved return. They do not
                # bridge the open ramp mouth or obstruct the turning sweep.
                for aa,cc in zip(arc,arc[1:]):
                    for begin,width,ma,lift in [(0,.1524,'Concrete',.1524),(.1524,1.6764,'Concrete',.16)]:
                        def outside(v,w):
                            dx,dy=v[0]-cx,v[1]-cy;ll=math.hypot(dx,dy)
                            return (v[0]-dx/ll*w,v[1]-dy/ll*w,v[2]+lift)
                        b.surface([outside(aa,begin),outside(cc,begin),outside(cc,width),outside(aa,width)],ma)
                        if begin==0:b.face([aa,cc,outside(cc,0),outside(aa,0)],ma)
    b.finish();return rt

def placement_wear(p):
    """Construction evidence only; per-scene joints/retrofit patches, no smears."""
    rt=Q.root('MaintenancePlacement',module_kind='decals');b=Q.Batch('Placement-owned repair evidence',rt);rng=random.Random(p.seed)
    if p.pavement=='Concrete':
        for side in (-1,1):
            for lane in range(2):
                u=p.lane(side,lane)
                for j in range(-round(p.length/2/JOINT),round(p.length/2/JOINT)):
                    if rng.random()>.22:continue
                    s=j*JOINT
                    for wheel in (-.82,.82):
                        for dx in (-.23,0,.23):
                            uu=u+wheel+dx;patch(b,p,s-.48,s+.48,uu-.045,uu+.045,'Concrete',.003)
    # GroundTrim placed chart, independent of repeated road-piece UVs.
    for i in range(24):
        s=rng.uniform(-p.length*.46,p.length*.46);side=rng.choice([-1,1]);u=side*(p.edge-.7)
        a,c=s-.6,s+.9;ua,ub=u-.25,u+.25
        b.surface([p.xyz(a,ua,.004),p.xyz(a,ub,.004),p.xyz(c,ub,.004),p.xyz(c,ua,.004)],'GroundTrim',uv=[(.50,.25),(1,.25),(1,.50),(.50,.50)])
    b.finish();return rt
