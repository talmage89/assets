"""One containment boundary and clipped surface cells, in meters.

Original layouts use published plan relationships, never traced contours.
Cells are clipped analytically to a convex boundary; curved corners retain a
margin outside every required equipment envelope. No internal lawn channels.
"""
import math,random
from mathutils import Vector
from kit import model as G
import geometry as F

def hull(points):
    p=sorted(set(tuple(x) for x in points))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    low=[];high=[]
    for q in p:
        while len(low)>1 and cross(low[-2],low[-1],q)<=0:low.pop()
        low.append(q)
    for q in reversed(p):
        while len(high)>1 and cross(high[-2],high[-1],q)<=0:high.pop()
        high.append(q)
    return low[:-1]+high[:-1]

def boundary(plan):
    # Expand each conservative zone enough to merge the containment, then
    # round the UNION perimeter rather than putting a box around every event.
    if plan['year']==1996:
        pts=[]
        for z in plan['zones']:
            a,b,c,d=z['rect'];m=.32
            pts.extend([(a-m,b-m),(c+m,b-m),(c+m,d+m),(a-m,d+m)])
        pts.extend([(-1.05,plan['surface'][1]),(1.05,plan['surface'][1])])
        return hull(pts)
    m=.90;regions=[]
    for z in plan['zones']:
        a,b,c,d=z['rect'];regions.append((a-m,b-m,c+m,d+m))
    comp=plan['zones'][0]['rect'];regions.append((-.98,plan['surface'][1],.98,comp[1]+.9))
    xs=sorted({v for a,b,c,d in regions for v in (a,c)});ys=sorted({v for a,b,c,d in regions for v in (b,d)})
    occ={(i,j) for i in range(len(xs)-1) for j in range(len(ys)-1) if any(a<(xs[i]+xs[i+1])/2<c and b<(ys[j]+ys[j+1])/2<d for a,b,c,d in regions)}
    edges={}
    for i,j in sorted(occ):
        for neighbor,a,b in [((i,j-1),(xs[i],ys[j]),(xs[i+1],ys[j])),((i+1,j),(xs[i+1],ys[j]),(xs[i+1],ys[j+1])),((i,j+1),(xs[i+1],ys[j+1]),(xs[i],ys[j+1])),((i-1,j),(xs[i],ys[j+1]),(xs[i],ys[j]))]:
            if neighbor not in occ:edges[a]=b
    start=min(edges);p=[start];v=edges[start]
    while v!=start:
        p.append(v);v=edges[v]
        if len(p)>len(edges):raise AssertionError('Open containment perimeter')
    clean=[]
    for i,v in enumerate(p):
        a=p[i-1];b=p[(i+1)%len(p)]
        if abs((v[0]-a[0])*(b[1]-v[1])-(v[1]-a[1])*(b[0]-v[0]))>1e-8:clean.append(v)
    return G.fillet_polygon(clean,1.65,7)

def clip(poly,axis,edge,sign):
    out=[]
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)];da=(a[axis]-edge)*sign;db=(b[axis]-edge)*sign
        if da>=-1e-8:out.append(a)
        if da*db<0:
            t=da/(da-db);out.append(tuple(a[k]+(b[k]-a[k])*t for k in range(2)))
    return out

def cells(p,step=.5):
    # Every boundary and material tile crossing has an explicit edge.
    x0=min(x for x,y in p);x1=max(x for x,y in p);y0=min(y for x,y in p);y1=max(y for x,y in p)
    for i in range(math.floor(x0/step),math.ceil(x1/step)):
        for j in range(math.floor(y0/step),math.ceil(y1/step)):
            q=p
            for ax,e,s in ((0,i*step,1),(0,(i+1)*step,-1),(1,j*step,1),(1,(j+1)*step,-1)):
                if q:q=clip(q,ax,e,s)
            if len(q)>=3:yield q

def halfplane(poly,a,b,inside=True):
    out=[]
    def side(p):return ((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))*(1 if inside else -1)
    for i,p in enumerate(poly):
        q=poly[(i+1)%len(poly)];d=side(p);e=side(q)
        if d>=-1e-9:out.append(p)
        if d*e<0:
            t=d/(d-e);out.append(tuple(p[k]+t*(q[k]-p[k]) for k in range(2)))
    return out

def split_inset(poly):
    def f(p):return ((p[0]-2)/5.9)**2+((p[1]+1)/4.7)**2
    if max(f(p) for p in poly)<1:return [(poly,1)]
    if min(p[0] for p in poly)>7.9 or max(p[0] for p in poly)<-3.9 or min(p[1] for p in poly)>3.7 or max(p[1] for p in poly)<-5.7:return [(poly,0)]
    ring=[(2+5.9*math.cos(i*math.tau/80),-1+4.7*math.sin(i*math.tau/80)) for i in range(80)]
    rest=poly;out=[]
    for i,a in enumerate(ring):
        if not rest:break
        b=ring[(i+1)%len(ring)];q=halfplane(rest,a,b,False)
        if len(q)>=3:out.append((q,0))
        rest=halfplane(rest,a,b,True)
    if len(rest)>=3:out.append((rest,1))
    return out


def build(rt,plan,depressions):
    p=boundary(plan);plan['containment_boundary_m']=[list(q) for q in p]
    plan['surface']=[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)]
    vs=[];fs=[];colors=[]
    def level(x,y):
        if plan['inclusive']:return -.005
        return -.008-sum(d*math.exp(-((x-a)/w)**2-((y-b)/h)**2) for a,b,w,h,d in depressions)+.004*math.sin(2.1*x+plan['seed'])*math.cos(2.8*y)
    for q in cells(p,.5):
        for piece,color in split_inset(q) if plan['inclusive'] else [(q,0)]:
            n=len(vs);vs.extend((x,y,level(x,y)) for x,y in piece);fs.append(tuple(range(n,len(vs))));colors.append(color)
    ob=F.own(G.mesh('Continuous protective containment / no internal borders',vs,fs,F.M['Site']),rt,'rubberfloor' if plan['inclusive'] else 'fiber','Site');ob['role']='protective_surface';ob['depression_centers_m']=[list(v) for v in depressions]
    attribute=ob.data.attributes.new(name='SurfaceInset',type='INT',domain='FACE')
    for d,c in zip(attribute.data,colors):d.value=c
    plan['protected_surface_area_m2']=abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2)
    plan['depressions_m']=[list(v) for v in depressions]
    if F.LOOK:
        from uv_finish import floor
        floor(ob,plan)
    # Stock timber in 1996; molded flexible edging with steel pins in 2005.
    if not plan['inclusive'] and plan['year']!=1996:
        flexible_border(rt,plan,p)
    if not plan['inclusive'] and plan['year']==1996:
        for i,a in enumerate(p):
            b=p[(i+1)%len(p)];L=math.dist(a,b);n=max(1,math.ceil(L/2.4))
            for j in range(n):
                u=Vector(a).lerp(Vector(b),j/n);v=Vector(a).lerp(Vector(b),(j+1)/n);mid=(u+v)/2
                # The walk passes through a real opening at the low boundary.
                if abs(mid.x)<1.10 and mid.y<plan['surface'][1]+.2:continue
                o=F.box(rt,'Pinned timber containment' if plan['year']==1996 else 'Flexible recycled border / recessed pins',(*mid,.044),(L/n-.012,.14,.14),'wood' if plan['year']==1996 else 'rubber',.012,'Site')
                o.rotation_euler.z=math.atan2(v.y-u.y,v.x-u.x)
                if L/n>.40:
                    for w in (u.lerp(v,.12),u.lerp(v,.88)):F.bolt(rt,(*w,.12),(0,0,1),.006)
    if F.LOOK and not plan['inclusive']:
        scatter(rt,plan,p,level)
    # Flat accessible walk and low tapered entry into the fiber enclosure.
    y0=plan['surface'][1];plan['walk_y']=y0-1.65
    ramp=[(-.95,y0-1,.0),(.95,y0-1,.0),(.95,y0+.30,.105),(-.95,y0+.30,.105)]
    if plan['inclusive']:ramp=[(x,y,-.007) for x,y,z in ramp]
    F.own(G.mesh('Accessible containment entry',ramp,[(0,1,2,3)],F.M['Site']),rt,'concrete','Site')
    F.box(rt,'Public sidewalk',(0,plan['walk_y'],-.065),(plan['surface'][2]-plan['surface'][0]+5,1.8,.12),'concrete',.005,'Site')
    plan['depressions_m']=[list(v) for v in depressions]


def scatter(rt,plan,perimeter,level):
    rng=random.Random(plan['seed']+173);vs=[];fs=[]
    def add(x,y,z):
        L=rng.uniform(.018,.045);W=rng.uniform(.003,.008);t=rng.random()*math.tau;u=Vector((math.cos(t),math.sin(t)));v=Vector((-u.y,u.x))
        xy=Vector((x,y));points=[xy-u*L/2,xy+u*L/2-v*W*.3,xy+u*L*.35+v*W,xy-u*L*.45+v*W*.7]
        n=len(vs);vs.extend((q.x,q.y,z+(rng.random()*.003)) for q in points);fs.append(tuple(range(n,n+4)))
    # Foot strokes eject fibers to the edge of the actual seat/exit depressions.
    for x,y,w,h,d in plan['depressions_m']:
        for j in range(32):
            a=rng.random()*math.tau;r=rng.uniform(.75,1.7);xx=x+math.cos(a)*w*r;yy=y+math.sin(a)*h*r;add(xx,yy,level(xx,yy)+.010)
    # Chips carry out through the entry; a few lodge on the border's upper face.
    y0=plan['surface'][1]
    for j in range(100):
        x=rng.uniform(-1.15,1.15);y=y0+rng.uniform(-1.3,.45);add(x,y,.008)
    for j in range(70):
        i=rng.randrange(len(perimeter));a=Vector(perimeter[i]);b=Vector(perimeter[(i+1)%len(perimeter)]);q=a.lerp(b,rng.random());add(q.x,q.y,.127)
    ob=F.own(G.mesh('Loose kicked fibers / exit banks and walk carryout',vs,fs,F.M['Site']),rt,'fiber','Site')
    from uv_finish import floor
    floor(ob,plan);ob['solid']=False


def flexible_border(rt,plan,p):
    vs=[];fs=[]
    for i,q in enumerate(p):
        a=Vector(p[i-1]);b=Vector(p[(i+1)%len(p)]);t=(b-a).normalized();n=Vector((t.y,-t.x))
        for s,z in ((-1,-.025),(1,-.025),(1,.115),(-1,.115)):
            r=Vector(q)+n*(s*.07);vs.append((*r,z))
    distance=0
    for i,q in enumerate(p):
        j=(i+1)%len(p);a=Vector(q);b=Vector(p[j]);mid=(a+b)/2
        if abs(mid.x)<1.10 and mid.y<plan['surface'][1]+.25:continue
        for k in range(4):fs.append((i*4+k,i*4+(k+1)%4,j*4+(k+1)%4,j*4+k))
        distance+=(b-a).length
        if distance>2.4:
            F.bolt(rt,(*mid,.116),(0,0,1),.006);distance=0
    ob=F.own(G.smooth(G.mesh('Continuous flexible containment / pinned 2.4m lengths',vs,fs,F.M['Frame']),45),rt,'rubber','Frame')
