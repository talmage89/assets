"""Cheap distant continuation, explicitly separate from the measured 300m reach.

This closes the inspection cameras with terrain, water, native town and trees.
It is presentation context and can be discarded by a world-streaming engine.
"""
import geometry as G
import context
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def water_reach(p,parent,side,ground):
    """Finite closed continuation: same medium, normals and submerged bed.

    This remains presentation context, separate from the 300m game reach.
    Matching the boundary cross-section avoids a flat painted water seam.
    """
    ys=sorted(side*(p.reach/2+i*5) for i in range(131));nx=20;stride=nx+1
    rows=[]
    for y in ys:
        l,r=p.water_edges(y)
        rows.append([(l+(r-l)*j/nx,y,p.water_z(y)) for j in range(stride)])
    top=[v for row in rows for v in row];count=len(top)
    bottom=[(x,y,min(p.bed(x,y)-.02,z-.025)) for x,y,z in top]
    faces=[(i*stride+j,i*stride+j+1,(i+1)*stride+j+1,(i+1)*stride+j)
           for i in range(len(rows)-1) for j in range(nx)]
    ground.geom([(x,y,p.bed(x,y)) for x,y,z in top],faces,'bank',(.48,.4704,.432,1),smooth=True,up=True)
    shell=faces+[tuple(count+k for k in reversed(f)) for f in faces]
    for i in range(len(rows)-1):
        a=i*stride;c=(i+1)*stride
        shell += [(a,c,c+count,a+count),(a+nx,a+nx+count,c+nx+count,c+nx)]
    for i in (0,len(rows)-1):
        for j in range(nx):
            a=i*stride+j;shell.append((a,a+count,a+1+count,a+1))
    b=G.Batch('DistantWaterVolume_'+str(side),parent,'context')
    b.geom(top+bottom,shell,'water',smooth=True);ob=b.finish()
    flow=ob.data.attributes.new('_FLOW',type='FLOAT_VECTOR',domain='POINT')
    for v,a in zip(ob.data.vertices,flow.data):
        tx,ty=p.tangent(v.co.y);speed=p.speed(v.co.x,v.co.y)
        a.vector=(tx*speed,ty*speed,max(0,p.water_z(v.co.y)-p.bed(v.co.x,v.co.y)))
    ob['presentation_only']=True


def add(p,parent):
    rt=G.root('DistantWorldContinuation',parent=parent,presentation_only=True)
    ground=G.Batch('DistantValleySkins',rt,'context')
    for side in (-1,1):
        water_reach(p,rt,side,ground)
        ys=[side*(p.reach/2+i*10) for i in range(66)]
        for a,c in zip(ys,ys[1:]):
            la,ra=p.water_edges(a);lc,rc=p.water_edges(c)
            for ba,bc in (([p.center(a)-500,la-8,la],[p.center(c)-500,lc-8,lc]),
                          ([ra,ra+8,p.center(a)+500],[rc,rc+8,p.center(c)+500])):
                for j in range(2):
                    vs=[(ba[j],a,p.bed(ba[j],a)),(ba[j+1],a,p.bed(ba[j+1],a)),(bc[j+1],c,p.bed(bc[j+1],c)),(bc[j],c,p.bed(bc[j],c))]
                    ground.geom(vs,[(0,1,2,3)],'grass',(.56,.62,.44,1),smooth=True,up=True)
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
    if p.kind=='downtown':
        town=next(o for o in parent.children if o.name=='TownContext')
        front=town['main_street_front_m']
        for side in (-1,1):
            for end in (-1,1):
                for j in range(50):
                    a=end*(150+j*10);c=end*(160+j*10)
                    for x0,x1,role in ((front,front+2,'concrete'),(front+2,front+9.3152,'asphalt'),(front+9.3152,front+11.4,'concrete')):
                        roads.geom([(side*x,y,3.775+p.water_z(y)) for x,y in ((x0,a),(x1,a),(x1,c),(x0,c))],[(0,1,2,3)],role,up=True)
                        ground.geom([(side*x,y,3.70+p.water_z(y)) for x,y in ((x0-.1,a),(x1+.1,a),(x1+.1,c),(x0-.1,c))],[(0,1,2,3)],'grass',(.56,.62,.44,1),up=True)
    roads.finish()
    soil=ground.finish()
    tree=BVHTree.FromPolygons([v.co for v in soil.data.vertices],[list(f.vertices) for f in soil.data.polygons],all_triangles=True)
    def seat(x,y):
        hit=tree.ray_cast(Vector((x,y,100)),Vector((0,0,-1)),120)[0]
        if hit is None:raise ValueError(('Missing distant terrain',x,y))
        return hit.z
    rng=__import__('random').Random(p.seed+818)
    for i in range(64):
        side=(-1,1)[i%2];y=side*rng.uniform(156,300 if i<32 else 650);x=p.center(y)+(-1 if i%3 else 1)*rng.uniform(p.width*.65,100)
        if p.kind=='downtown' and abs(abs(x)-front)<22:continue
        context.instance(context.REPO/'trees/export/RedMaple.glb','Distant floodplain maple '+str(i),
                         (x,y,seat(x,y)-.04),rt,rng.uniform(0,360),rng.uniform(.75,1.15),category='vegetation')
    for i in range(16):
        side=(-1,1)[i%2];y=side*(163+(i//2)*24);x=(-1 if i%3 else 1)*62
        if p.kind=='downtown':x=(-1 if i%3 else 1)*(front-10)
        context.instance(context.REPO/'school/build/context/houses-ranch.glb','Beyond reach neighbor '+str(i),
                         (x,y,seat(x,y)-.025),rt,90 if x<0 else -90)
    return rt
