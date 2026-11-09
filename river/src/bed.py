"""Graded interlocking scour armor and a sparse rounded alluvial silhouette."""
import math
import random
import geometry as G


def armor(p,batch):
    from channel import stone,surface_z
    rng=random.Random(p.seed+512)
    # Offset rows place a continuous single blanket rather than random islands.
    # The median stone is ~0.55m across; its lower half keys into the slope.
    step=.51
    for side in (-1,1):
        for row in range(46):
            y=-p.deck_width/2-5.5+row*step
            if y>p.deck_width/2+5.5:continue
            for column in range(26):
                offset=-7+column*step+(row%2)*step/2
                x=side*(p.length/2+offset)+rng.uniform(-.12,.12)
                yy=y+rng.uniform(-.12,.12)
                if abs(x)>p.length/2-.8 and abs(yy)<p.deck_width/2+.20:continue
                z=surface_z(p,x,yy);r=rng.uniform(.34,.51)
                stone(batch,x,yy,z-.015,r,rng,water_z=p.water_z(yy))
                # Chinking grade lies lower between the armor stones.
                if rng.random()<.25:
                    xx=x+side*step*.43;sy=yy+step*.4;sz=surface_z(p,xx,sy)
                    stone(batch,xx,sy,sz-.02,rng.uniform(.11,.21),rng,water_z=p.water_z(sy))
    for j in range(1,p.spans):
        center=-p.length/2+j*p.span
        for row in range(round(p.deck_width/.49)):
            y=-p.deck_width*.52+row*.49
            for column in range(9):
                x=center-2.1+column*.49+(row%2)*.245
                x+=rng.uniform(-.05,.05);yy=y+rng.uniform(-.05,.05)
                stone(batch,x,yy,surface_z(p,x,yy)-.02,rng.uniform(.28,.43),rng,water_z=p.water_z(yy))


def cobbles(p,batch):
    from channel import surface_z
    rng=random.Random(p.seed+811)
    for i in range(72):
        y=rng.uniform(p.bar_y-25,p.bar_y+25)
        x=p.center(y)-p.outside*p.halfwidth(y)*rng.uniform(.60,1.035)
        z=surface_z(p,x,y)
        if z<p.water_z(y)-.26:continue
        radius=rng.uniform(.045,.14);aspect=rng.uniform(.7,1.4);rings=[]
        for t in (-.35,.10,.65,.91):
            r=radius*math.sqrt(1-t*t)
            rings.append([(x+r*math.cos(a),y+r*aspect*math.sin(a),z+radius*(t-.1)) for a in [j*math.tau/7 for j in range(7)]])
        value=rng.uniform(.50,.82)
        batch.loft(rings,'riprap',(value*.97,value,value*1.04,1),smooth=True)


def seedlings(p,parent):
    from channel import surface_z
    rng=random.Random(p.seed+819);b=G.Batch('BarGrassAndWillowSeedlings',parent,'vegetation')
    for i in range(125):
        y=rng.uniform(p.bar_y-19,p.bar_y+19)
        x=p.center(y)-p.outside*p.halfwidth(y)*rng.uniform(.88,1.08)
        z=surface_z(p,x,y)
        if z-p.water_z(y)<.18:continue
        h=rng.uniform(.12,.43);chart=rng.randrange(4);u=chart*.25
        for angle in (rng.random()*math.tau,rng.random()*math.tau):
            dx=math.cos(angle)*h*.6;dy=math.sin(angle)*h*.6
            b.geom([(x-dx,y-dy,z),(x+dx,y+dy,z),(x+dx*.75,y+dy*.75,z+h),(x-dx*.75,y-dy*.75,z+h)],
                   [(0,1,2,3)],'plants',uv=[(u+.002,.002),(u+.248,.002),(u+.248,.248),(u+.002,.248)])
    if b.v:b.finish()
