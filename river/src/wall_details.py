"""Poured wall bays, tie recesses, flood residue and working public access."""
import math
import random
import geometry as G
from weather import chart


def add(p,parent):
    if p.kind!='downtown':return
    rng=random.Random(p.seed+815);b=G.Batch('FloodwallConstructionAndAccess',parent,'site')
    for side in (-1,1):
        def pos(y,z,off=4.194):return (p.center(y)+side*(p.halfwidth(y)+off),y,z)
        def patch(y,z,w,h,k,color):
            b.geom([pos(yy,zz) for yy,zz in ((y-w/2,z-h),(y+w/2,z-h),(y+w/2,z),(y-w/2,z))],
                   [(0,1,2,3)],'maintenance',color,uv=chart(k))
        for y in range(-144,145,6):
            if abs(y)<10 or -90<y<-78:continue
            # 12mm sealed contraction joints in 6m pours.
            b.geom([pos(yy,z) for yy,z in ((y-.006,.66),(y+.006,.66),(y+.006,3.69),(y-.006,3.69))],
                   [(0,1,2,3)],'rubber')
            for dy in (1.4,4.5):
                for z in (1.2,2.65):
                    # At 42mm these are texture detail: one two-triangle
                    # recess chart, rather than a capped 28-triangle tube.
                    uv=[(.002,.752),(.022,.752),(.022,.772),(.002,.772)]
                    b.geom([pos(yy,zz) for yy,zz in ((y+dy-.026,z-.026),(y+dy+.026,z-.026),
                        (y+dy+.026,z+.026),(y+dy-.026,z+.026))],[(0,1,2,3)],'maintenance',uv=uv)
            if y%18==0:patch(y+.7,1.30,3.7,.22,0,(.49,.55,.39,1))
            if rng.random()<.43:
                patch(y+rng.uniform(-.12,.16),3.67,rng.uniform(.12,.30),rng.uniform(.7,2.3),0,(.83,.82,.75,1))
                if rng.random()<.5:patch(y+.14,3.64,.065,rng.uniform(.6,1.6),1,(1,1,.97,1))
        # Covered tags remain visible as mismatched roller-painted rectangles,
        # with diffuse ragged edges from the original alpha maintenance chart.
        for y,w in ((-56,2.1),(-41,3.5),(31,2.8),(107,2.2)):
            patch(y,2.12,w,1.10,3,(.73,.76,.74,1))
        for y in (-33,59):
            patch(y,1.22,.78,.56,0,(.49,.56,.36,1))
            patch(y+.18,1.17,.12,.47,1,(.92,.94,.84,1))
        # Embedded wall ladder: 32mm rails, 20mm rungs, bolted stand-offs.
        ly=-49 if side<0 else 39
        for dy in (-.27,.27):
            b.tube([pos(ly+dy,.78,3.96),pos(ly+dy,4.22,3.96),pos(ly+dy,4.22,4.55)],.016,'steel',8)
            for z in (1.0,2.1,3.3):b.beam(pos(ly+dy,z,4.23),pos(ly+dy,z,3.96),.04,.025)
        for i in range(11):b.tube([pos(ly-.27,.90+i*.29,3.96),pos(ly+.27,.90+i*.29,3.96)],.010,'steel',8)
        # Full stair climbs beside the wall; the top landing enters a break
        # in the wall rather than terminating against a solid retaining face.
        steps=18;start=-88;run=6.;top=3.775+p.water_z(-81);rise=(top-.65)/steps
        for i in range(steps):
            y=start+(i+.5)*run/steps;z=.65+(i+1)*rise
            x=pos(y,z,3.35)[0]
            b.box((x,y,(.65+z)/2),(1.32,run/steps,z-.65),'concrete',(.73,.74,.70,1))
        for off in (2.73,3.97):
            pts=[pos(start,.65+.94,off),pos(start+run,top+.94,off),pos(-80,top+.94,off)]
            b.tube(pts,.021,'steel',8)
            for t in (0,.25,.5,.75,1):
                y=start+t*run;z=.65+t*(top-.65)
                b.tube([pos(y,z,off),pos(y,z+.94,off)],.019,'steel',8)
        coords=[pos(y,top,off) for y,off in ((-82,2.65),(-82,4.6),(-80,4.6),(-80,2.65))]
        b.geom(coords,[(0,1,2,3)],'concrete',(.73,.74,.70,1),up=True)
        # Shielded bulkhead lamps and conduit, mounted over the low walk.
        for y in range(-136,145,18):
            if abs(y)<12:continue
            x=pos(y,2.85,4.08)[0]
            b.box((x,y,2.85),(.16,.26,.31),'steel')
            b.box((x-side*.09,y,2.84),(.025,.18,.18),'white')
            b.tube([pos(y,.70,4.15),pos(y,2.72,4.15)],.012,'steel',6)
            for z in (.82,2.6):b.box((pos(y,z,4.16)[0],y,z),(.05,.055,.07),'steel')
    b.finish()
