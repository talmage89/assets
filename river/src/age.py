"""Coarse caused maintenance evidence for the form gate, no final look-dev."""
import math
import random
import geometry as G


def add(p,parent):
    rng=random.Random(p.seed+2010);b=G.Batch('PlacedMaintenance',parent,'site')
    cracks=(.5,0,.625,.25);patch=(.25,.25,.5,.5)
    for j in range(p.spans+1):
        x=-p.length/2+j*p.span
        for side in (-1,1):
            a,c=cracks[0]+.001,cracks[2]-.001;v0,v1=.002,.248
            b.geom([(x-.9,side*.25,p.deck_z-.003),(x+.9,side*.25,p.deck_z-.003),(x+.9,side*3.0,p.deck_z-.057),(x-.9,side*3.0,p.deck_z-.057)],[(0,1,2,3)],'decal',uv=[(a,v0),(c,v0),(c,v1),(a,v1)])
    for j in range(22):
        x=rng.uniform(-135,135);y=rng.choice((-1,1))*rng.uniform(.35,2.8);w=rng.uniform(.4,1.3);h=rng.uniform(.25,.70)
        a,v,c,d=patch
        pts=[(xx,yy,p.deck_z-.02*abs(yy)+.006) for xx,yy in ((x-w,y-h),(x+w,y-h),(x+w,y+h),(x-w,y+h))]
        b.geom(pts,[(0,1,2,3)],'decal',uv=[(a+.002,v+.002),(c-.002,v+.002),(c-.002,d-.002),(a+.002,d-.002)])
    # Discrete joint leaks: several narrow gravity tracks, terminating at
    # physical cap faces. They are intentionally coarse temporary solids.
    for j in range(1,p.spans):
        x=-p.length/2+j*p.span
        for side in (-1,1):
            y=side*(p.deck_width/2-.3)
            for k in range(7):
                xx=x+rng.uniform(-.55,.55);w=rng.uniform(.012,.043);z=2.687-rng.uniform(.22,.65)
                b.geom([(xx-w,y,2.66),(xx+w,y,2.66),(xx+w*.4,y,z),(xx-w*.5,y,z-.10)],[(0,1,2,3)],'algae')
    # A waterline and high-water stain wrap the actual pier section, never a
    # planar billboard floating in front of it.
    for j in range(1,p.spans):
        x=-p.length/2+j*p.span
        if p.pier=='columns':
            for y in (-p.deck_width*.29,0,p.deck_width*.29):
                rings=[[(x+.601*math.cos(i*math.tau/32),y+.601*math.sin(i*math.tau/32),z+.012*math.sin(i*1.7)) for i in range(32)] for z in (-.06,.26)]
                b.loft(rings,'algae',caps=False)
    b.finish()
