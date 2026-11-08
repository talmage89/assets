"""Cheap distant continuation, explicitly separate from the measured 300m reach.

This closes the inspection cameras with terrain, water, native town and trees.
It is presentation context and can be discarded by a world-streaming engine.
"""
import geometry as G
import context


def add(p,parent):
    rt=G.root('DistantWorldContinuation',parent=parent,presentation_only=True)
    ground=G.Batch('DistantValleySkins',rt,'context');water=G.Batch('DistantWaterContinuation',rt,'context')
    for side in (-1,1):
        ys=[side*(p.reach/2+i*10) for i in range(66)]
        for a,c in zip(ys,ys[1:]):
            la,ra=p.water_edges(a);lc,rc=p.water_edges(c)
            for ba,bc in (([p.center(a)-500,la-8,la],[p.center(c)-500,lc-8,lc]),
                          ([ra,ra+8,p.center(a)+500],[rc,rc+8,p.center(c)+500])):
                for j in range(2):
                    vs=[(ba[j],a,p.bed(ba[j],a)),(ba[j+1],a,p.bed(ba[j+1],a)),(bc[j+1],c,p.bed(bc[j+1],c)),(bc[j],c,p.bed(bc[j],c))]
                    ground.geom(vs,[(0,1,2,3)],'grass',(.56,.62,.44,1),smooth=True)
            water.geom([(la,a,p.water_z(a)),(ra,a,p.water_z(a)),(rc,c,p.water_z(c)),(lc,c,p.water_z(c))],[(0,1,2,3)],'water',smooth=True)
    # Lateral continuation is below the native bank skins at their boundary.
    for side in (-1,1):
        x0=side*125;x1=side*500
        ground.geom([(x0,-150,2.0),(x1,-150,2.0),(x1,150,2.0),(x0,150,2.0)],[(0,1,2,3)],'grass',(.53,.60,.42,1))
    ground.finish();water.finish()
    rng=__import__('random').Random(p.seed+818)
    for i in range(30):
        side=(-1,1)[i%2];y=side*rng.uniform(156,255);x=p.center(y)+(-1 if i%3 else 1)*rng.uniform(p.width*.65,100)
        context.instance(context.REPO/'trees/export/RedMaple.glb','Distant floodplain maple '+str(i),
                         (x,y,p.bed(x,y)-.04),rt,rng.uniform(0,360),rng.uniform(.75,1.15),category='vegetation')
    for i in range(8):
        side=(-1,1)[i%2];y=side*(163+(i//2)*24);x=(-1 if i%3 else 1)*62
        context.instance(context.REPO/'school/build/context/houses-ranch.glb','Beyond reach neighbor '+str(i),
                         (x,y,p.bed(x,y)-.025),rt,90 if x<0 else -90)
    return rt
