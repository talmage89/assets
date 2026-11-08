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
        x=rng.uniform(-p.length/2-30,p.length/2+30);y=rng.choice((-1,1))*rng.uniform(.35,2.8);w=rng.uniform(.4,1.3);h=rng.uniform(.25,.70)
        a,v,c,d=patch
        outline=[(-.90,-1),(.65,-.92),(1,-.4),(.93,.77),(.55,1),(-.85,.88),(-1,.16)]
        outline=[(u*rng.uniform(.88,1),t*rng.uniform(.90,1)) for u,t in outline]
        pts=[(x+u*w,y+t*h,p.road_z(x+u*w)-.02*abs(y+t*h)+.006) for u,t in outline]
        uv=[(a+.002+(u+1)/2*(c-a-.004),v+.002+(t+1)/2*(d-v-.004)) for u,t in outline]
        b.geom(pts,[tuple(range(len(pts)))],'decal',uv=uv)
    b.finish()
