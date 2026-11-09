"""Tapered bark-plated snag, torn root collar and flow-packed upstream wrack."""
import math
import random
from mathutils import Vector


def sweep(batch,points,radii,rng,p,role='bark',sides=12):
    points=list(map(Vector,points));rings=[]
    for i,(point,radius) in enumerate(zip(points,radii)):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        u=tangent.cross(Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))).normalized();v=tangent.cross(u)
        ring=[]
        for j in range(sides):
            angle=j*math.tau/sides
            # Angular plates run along the trunk, with interrupted lifted lips.
            ridge=1+.10*math.sin(j*7.3)+.045*math.sin(j*4.7+i*.8)
            ring.append(point+radius*ridge*(u*math.cos(angle)+v*math.sin(angle)))
        rings.append(ring)
    for i,(a,c) in enumerate(zip(rings,rings[1:])):
        for j in range(sides):
            k=(j+1)%sides;coords=[a[j],a[k],c[k],c[j]]
            value=.70+.24*math.sin(j*9.7+i*.73)**2
            colors=(value*.32,value*.23,value*.15,1)
            batch.geom(coords,[(0,1,2,3)],role,colors,
                uv=[(j/sides,i*.16),(k/sides,i*.16),(k/sides,(i+1)*.16),(j/sides,(i+1)*.16)],smooth=True)
    # Torn pale end grain is recessed behind a broken bark lip.
    for index in (0,-1):
        ring=rings[index];center=points[index]
        if radii[index]<.022:
            batch.geom(list(reversed(ring)) if index==0 else ring,[tuple(range(sides))],role)
            continue
        inner=[center+(point-center)*.77 for point in ring]
        if index==0:inner.reverse();ring=list(reversed(ring))
        batch.geom(inner,[tuple(range(sides))],'wood_end')
        for j in range(sides):
            k=(j+1)%sides
            batch.geom([ring[j],ring[k],inner[k],inner[j]],[(0,1,2,3)],role,(.7,.66,.58,1))


def add(p,batch,cx,cy,tx,ty):
    rng=random.Random(p.seed+round(cx*717));cross=Vector((ty,-tx,0));flow=Vector((tx,ty,0))
    center=Vector((cx,cy,p.water_z(cy)+.035))
    points=[];radii=[]
    for i in range(15):
        t=i/14;point=center+cross*((t-.5)*2.20)-flow*(.025*math.sin(t*5))
        point.z+=.025*math.sin(t*4.6)
        points.append(point);radii.append(.148*(1-.27*t)*(1+.10*math.sin(i*1.7)))
    sweep(batch,points,radii,rng,p,sides=24)
    collar=points[0]
    # Root flare splits into bent, tapered roots with small snapped fibers.
    for i in range(7):
        angle=i*math.tau/7+.15;spread=Vector((0,math.cos(angle),math.sin(angle)))
        direction=(cross*-.30+flow*math.cos(angle)*.30+Vector((0,0,math.sin(angle)*.28)))
        a=collar+direction*.18;c=collar+direction+Vector((-.05,.03,-.03))
        end=c+direction*.75-flow*.07
        sweep(batch,[a,collar+direction*.52,c,end],[.070,.045,.023,.006],rng,p,sides=7)
        if i%2==0:sweep(batch,[c,c+flow*.11+Vector((0,0,.12))],[.018,.003],rng,p,sides=5)
    for i in (3,9):
        a=points[i];delta=-flow*.24+Vector((0,0,.10+i*.005))
        sweep(batch,[a,a+delta*.55,a+delta],[.055,.032,.014],rng,p,sides=8)
    # Matted twigs meet the trunk's upstream face, not evenly spaced pegs.
    for i in range(25):
        along=rng.uniform(-1.0,.9);reach=rng.uniform(.10,.65)
        a=center+cross*along-flow*.09;a.z-=rng.uniform(.01,.08)
        c=a-flow*reach+cross*rng.uniform(-.14,.14);c.z+=rng.uniform(-.015,.055)
        middle=a.lerp(c,.55)+Vector((0,0,rng.uniform(.01,.035)))
        sweep(batch,[a,middle,c],[rng.uniform(.007,.018),.009,.003],rng,p,sides=5)
