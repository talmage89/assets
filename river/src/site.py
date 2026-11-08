"""Approaches, connected paths, outfalls, floodwall and bank-card planting."""
import math
import random
import geometry as G
from channel import surface_z


def road(p,parent):
    b=G.Batch('ApproachRoadAndWalks',parent,'site')
    for side in (-1,1):
        a=side*p.length/2;c=side*145
        for y0,y1 in ((-3.3528,0),(0,3.3528)):
            b.geom([(x,y,p.deck_z-.02*abs(y)) for x,y in ((a,y0),(c,y0),(c,y1),(a,y1))],[(0,1,2,3)],'asphalt',up=True)
        for s in (-1,1):
            b.box(((a+c)/2,s*4.2672,p.deck_z+.009144),(abs(c-a),1.524,.1524))
    # Road-paint module is Ground's existing worn paint chart (bound below).
    for y in (-.0762,.0762):
        b.geom([(-145,y-.05,p.deck_z+.002),(145,y-.05,p.deck_z+.002),(145,y+.05,p.deck_z+.002),(-145,y+.05,p.deck_z+.002)],[(0,1,2,3)],'paint_yellow')
    for y in (-3.18,3.18):
        b.geom([(-145,y-.05,p.deck_z-.02*abs(y)+.003),(145,y-.05,p.deck_z-.02*abs(y)+.003),(145,y+.05,p.deck_z-.02*abs(y)+.003),(-145,y+.05,p.deck_z-.02*abs(y)+.003)],[(0,1,2,3)],'paint_white')
    b.finish()


def fixtures(p,parent):
    rt=G.root('BankPublicWorks',parent=parent)
    b=G.Batch('FloodwallTrailAndAccess',rt,'site');trail=[]
    for i in range(150):
        y=-150+i*2;yy=y+2
        edge=lambda v:p.center(v)-p.halfwidth(v)
        x=edge(y);xx=edge(yy)
        if p.kind=='downtown':
            # Riverwalk below Main Street with 6m poured bays and a real cap.
            b.geom([(x-1,y,-.3),(xx-1,yy,-.3),(xx-1,yy,.65),(x-1,y,.65)],[(0,1,2,3)],'concrete',(.63,.64,.60,1))
            b.geom([(x-1.12,y,.65),(xx-1.12,yy,.65),(xx-4.2,yy,.65),(x-4.2,y,.65)],[(0,1,2,3)],'concrete',(.80,.80,.75,1))
            wall_top=.65 if abs((y+yy)/2)<8 else 3.70
            b.geom([(x-4.2,y,.50),(xx-4.2,yy,.50),(xx-4.2,yy,wall_top),(x-4.2,y,wall_top)],[(0,1,2,3)],'concrete',(.65,.65,.60,1))
            b.geom([(x-4.03,y,wall_top+.025),(xx-4.03,yy,wall_top+.025),(xx-4.55,yy,wall_top+.025),(x-4.55,y,wall_top+.025)],[(0,1,2,3)],'concrete',(.72,.72,.67,1))
            trail.append((x-2.6,y,.65))
            if abs(y)>9:
                b.cylinder((x-1.2,y,1.15),.024,1,'steel',8)
                for z in (.80,1.65):b.tube([(x-1.2,y,z),(xx-1.2,yy,z)],.022,'steel',6)
                for j in range(1,18):
                    t=j/18;bx=(1-t)*x+t*xx-1.2
                    b.box((bx,y+2*t,1.225),(.019,.019,.85),'steel')
        else:
            x-=7;xx-=7;z=p.bed(x,y)+.035;zz=p.bed(xx,yy)+.035
            if abs(y)>12:
                b.geom([(x-1,y,z),(xx-1,yy,zz),(xx+1,yy,zz),(x+1,y,z)],[(0,1,2,3)],'bank',(.93,.90,.82,1))
            trail.append((x,y,z))
    # 30in storm drain through a concrete endwall. The opening has no disk.
    for y in (-33,59):
        x=p.center(y)+p.halfwidth(y)*1.13;z=p.bed(x,y)
        b.box((x+.1,y,z+.1),(.35,2.1,.25))
        for side in (-1,1):b.box((x+.1,y+side*.65,z+.68),(.35,.40,1.15))
        b.box((x+.1,y,z+1.20),(.35,1.7,.22))
        rings=[[(xx,y+r*math.cos(k*math.tau/20),z+.58+r*math.sin(k*math.tau/20)) for k in range(20)] for xx,r in ((x+.65,.4318),(x-.12,.4318),(x-.12,.381),(x+.65,.381))]
        b.loft(rings,'concrete',caps=False)
    if p.kind=='edge':
        # Small worn fishing landing and 12%-slope boat launch into shallow edge.
        y=-36;x=p.center(y)-p.halfwidth(y)
        b.geom([(x-18,y-2,2.10),(x-18,y+2,2.10),(x+.8,y+2,-.12),(x+.8,y-2,-.12)],[(0,1,2,3)],'concrete',(.66,.65,.58,1))
        G.root('BoatLaunch',(x-5,y,2.10-2.22*13/18.8),rt,socket_kind='launch')
        fy=33;fx=p.center(fy)-p.halfwidth(fy)
        G.root('FishingSpot',(fx-2,fy+5,surface_z(p,fx-2,fy+5)+.02),rt,socket_kind='fishing')
    b.finish();G.path('RiverbankTrail',trail,rt,'walk')
    return rt


def plants(p,parent):
    rng=random.Random(p.seed+18);b=G.Batch('BankGrassReedsCattails',parent,'vegetation')
    # Dense low colonies, wide enough to read as cover; no lone wire tufts.
    for i in range(22000):
        y=rng.uniform(-149,149);side=(-1,1)[i%2]
        if abs(y)<8:continue
        u=side*rng.uniform(1.0,1.47)
        if p.kind=='downtown' and side<0:continue
        x=p.center(y)+u*p.halfwidth(y);z=surface_z(p,x,y)
        if p.kind=='edge':
            if side<0 and abs(x-(p.center(y)-p.halfwidth(y)-7))<1.15:continue
            ramp_edge=p.center(-36)-p.halfwidth(-36)
            if abs(y+36)<2.15 and ramp_edge-18.1<x<ramp_edge+.9:continue
        if z<.06 or z>2.8:continue
        if math.sin(y*.13+u*19)+math.sin(y*.33-u*8)<-.9:continue
        reed=z<.65 and i%3==0;h=rng.uniform(.55,1.15) if reed else rng.uniform(.15,.45)
        w=rng.uniform(.35,.65) if reed else rng.uniform(.55,.95);yaw=rng.uniform(0,6.28)
        k=rng.randrange(14,16) if reed else rng.randrange(12);a=(k%4)/4;c=(k//4)/4
        uv=[(a+.002,c+.002),(a+.248,c+.002),(a+.248,c+.248),(a+.002,c+.248)]
        for angle in (yaw,yaw+math.pi/2):
            dx=math.cos(angle)*w/2;dy=math.sin(angle)*w/2
            b.geom([(x-dx,y-dy,z-.02),(x+dx,y+dy,z-.02),(x+dx+.09,y+dy,z+h),(x-dx+.09,y-dy,z+h)],[(0,1,2,3)],'plants',uv=uv)
    b.finish()
