"""Cheap distant continuation, explicitly separate from the measured 300m reach.

This closes the inspection cameras with terrain, water, native town and trees.
It is presentation context and can be discarded by a world-streaming engine.
"""
import geometry as G
import context
from mathutils import Vector
from mathutils.bvhtree import BVHTree


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
                    ground.geom(vs,[(0,1,2,3)],'grass',(.56,.62,.44,1),smooth=True,up=True)
            water.geom([(la,a,p.water_z(a)),(ra,a,p.water_z(a)),(rc,c,p.water_z(c)),(lc,c,p.water_z(c))],[(0,1,2,3)],'distant_water',smooth=True,up=True)
    # Lateral continuation is below the native bank skins at their boundary.
    for side in (-1,1):
        xs=[side*x for x in (125,145,155,170,190,210,230,300,500)]
        ys=[-150,-22,-15,-7,0,7,15,22,150]
        for x0,x1 in zip(xs,xs[1:]):
            for y0,y1 in zip(ys,ys[1:]):
                points=[(x,y,p.bed(x,y)-.02) for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))]
                ground.geom(points,[(0,1,2,3)],'grass',(.53,.60,.42,1),up=True)
    roads=G.Batch('RoadContinuation',rt,'context')
    for side in (-1,1):
        xs=[side*x for x in (145,155,170,190,210,230,300,500)]
        for a,c in zip(xs,xs[1:]):
            for lo,hi in ((-3.65,0),(0,3.65)):
                roads.geom([(x,y,p.road_z(x)-.02*abs(y)) for x,y in ((a,lo),(c,lo),(c,hi),(a,hi))],[(0,1,2,3)],'asphalt',up=True)
            for y in (-.0762,.0762,-3.18,3.18):
                role='paint_yellow' if abs(y)<.1 else 'paint_white'
                roads.geom([(x,yy,p.road_z(x)-.02*abs(yy)+.003) for x,yy in ((a,y-.05),(c,y-.05),(c,y+.05),(a,y+.05))],[(0,1,2,3)],role,up=True)
    roads.finish()
    soil=ground.finish();water.finish()
    tree=BVHTree.FromPolygons([v.co for v in soil.data.vertices],[list(f.vertices) for f in soil.data.polygons],all_triangles=True)
    def seat(x,y):
        hit=tree.ray_cast(Vector((x,y,100)),Vector((0,0,-1)),120)[0]
        if hit is None:raise ValueError(('Missing distant terrain',x,y))
        return hit.z
    rng=__import__('random').Random(p.seed+818)
    for i in range(30):
        side=(-1,1)[i%2];y=side*rng.uniform(156,255);x=p.center(y)+(-1 if i%3 else 1)*rng.uniform(p.width*.65,100)
        context.instance(context.REPO/'trees/export/RedMaple.glb','Distant floodplain maple '+str(i),
                         (x,y,seat(x,y)-.04),rt,rng.uniform(0,360),rng.uniform(.75,1.15),category='vegetation')
    for i in range(8):
        side=(-1,1)[i%2];y=side*(163+(i//2)*24);x=(-1 if i%3 else 1)*62
        context.instance(context.REPO/'school/build/context/houses-ranch.glb','Beyond reach neighbor '+str(i),
                         (x,y,seat(x,y)-.025),rt,90 if x<0 else -90)
    return rt
