"""Carved walnut, machined receiver, barrel, bands and open iron sights."""
import math
import json
import bpy
import bmesh
from mathutils import Vector
from kit import model as M
import geometry as G
from geometry import MAT, reg, box, profile, lathe, cut, cutbox, screw
from dimensions import BORE, BREECH, MUZZLE, TUBE


RECEIVER_ROWS=[(65,15.4,4.0,50),(66,15.6,4.0,53),(70,15.75,3.8,56),
          (90,15.75,3.8,56),(112,15.75,3.8,56),(117,15.75,3.0,56),
          (124,15.75,0,56),(131,15.75,-.5,56),(166,15.75,-.5,56),
          (179,15.75,0,56),(185,15.75,3,56),(190,15.75,6.8,56),
          (193,15.75,8.3,59.5),(196,15.75,9,61.6),
          (202,15.6,9.5,61.6),(205,15.1,10,60.7)]


def receiver_field(point):
    """Analytic outer forging normal; independent of irregular cut triangles."""
    def distance(p):
        x,y,z=p;y=max(65,min(205,y))
        a,b=next((a,b) for a,b in zip(RECEIVER_ROWS,RECEIVER_ROWS[1:]) if a[0]<=y<=b[0])
        t=(y-a[0])/(b[0]-a[0]);w,lo,hi=[a[k]+t*(b[k]-a[k]) for k in (1,2,3)]
        r=2.2+5.8*max(0,min(1,(y-190)/6))
        qx=abs(x)-(w-r);qz=abs(z-(lo+hi)/2)-((hi-lo)/2-r)
        return math.hypot(max(qx,0),max(qz,0))+min(max(qx,qz),0)-r
    p=Vector(point);d=distance(p);epsilon=.01;gradient=[]
    for k in range(3):
        a=p.copy();b=p.copy();a[k]+=epsilon;b[k]-=epsilon
        gradient.append((distance(a)-distance(b))/(2*epsilon))
    n=Vector(gradient)
    return d,n.normalized() if n.length else Vector((0,0,1))


def receiver():
    # Forging profile: raised rear heel, lower action belly, then a rounded
    # front ring. The rails themselves stay level with the accepted bolt.
    rows=RECEIVER_ROWS
    loops=[[(x,y,(lo+hi)/2+z) for x,z in M.rounded_rectangle(w*2,hi-lo,2.2+5.8*max(0,min(1,(y-190)/6)),6)] for y,w,lo,hi in rows]
    ob=M.loft('Receiver',loops,MAT['blue'])
    # Continuous open top and lower linkage aperture; the long flat cheeks
    # have real thickness and small rolled machining corners.
    cutbox(ob,(-10.6,33,8),(10.6,196,80),1.4)
    cutbox(ob,(-10.7,57,-10),(10.7,206,23),1)
    cutbox(ob,(-7.3,29,30),(7.3,85,68),1.0)
    cutbox(ob,(-10.3,28,38.8),(10.3,85,58),.7)
    cut(ob,lathe('tool',[(190,0),(190,12.7),(210,12.7),(210,0)],n=64,raw=True))
    cut(ob,lathe('tool',[(190,0),(190,10.3),(209,10.3),(209,0)],center=(0,TUBE),n=48,raw=True))
    gate=[(y+147.7,z+20) for y,z in M.rounded_rectangle(51.4,13.6,6.3,10)]
    cut(ob,profile('tool',gate,10,20,raw=True))
    cutbox(ob,(10.5,171,12.5),(12.2,204,27.5),.4)
    cutbox(ob,(10.4,174.8,-20),(14.2,185.2,37.2),.25)
    cut(ob,lathe('tool',[(14.5,0),(14.5,1.55),(25.5,1.55),(25.5,0)],axis='Z',center=(15.2,122),n=24,raw=True))
    # Side-plate screws and pins are countersunk in the actual cheeks.
    sites=[(74,15,3.15),(92,38,2.55),(148,40,2.65),(185,16,2.5)]
    for side in (-1,1):
        for y,z,r in sites:
            lo,hi=sorted((side*14.9,side*18))
            cut(ob,lathe('tool',[(lo,0),(lo,r+.22),(hi,r+.22),(hi,0)],axis='X',center=(y,z),n=24,raw=True))
        for y,z in [(75,28),(91,30)]:
            lo,hi=sorted((side*15.25,side*15.8))
            lathe('Receiver_Pin',[(lo,0),(lo,1.25),(hi,1.25),(hi,0)],'dark',axis='X',center=(y,z),n=16)
    for y,z,r in sites:
        for side in (-1,1):screw('Receiver_Screw',(side*15.15,y,z),r,direction=side)
    # Exact overlapping machining cuts can retain coincident edge chains.
    # Weld in millimeter space before bevel/reduction, rather than shipping
    # thousands of zero-area triangles or allowing a decimator to stall.
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    # Broad longitudinal rolls are already in the forging's section cage.
    # Ease only the front/rear end perimeters. Beveling every intersecting
    # internal machining edge produced zero-area overlapping bevel ribbons.
    weight=ob.data.attributes.new('bevel_weight_edge','FLOAT','EDGE')
    for edge in ob.data.edges:
        ys=[ob.data.vertices[i].co.y for i in edge.vertices]
        weight.data[edge.index].value=float(all(abs(y-65)<.001 for y in ys) or all(abs(y-205)<.001 for y in ys))
    bevel=ob.modifiers.new('Forging end rolls','BEVEL');bevel.limit_method='WEIGHT';bevel.width=.18;bevel.segments=2
    M.apply(ob);reg(ob)
    G.dense(ob);G.reduce(ob,3000)
    # Real pin bore at the lever's front pivot.
    lathe('Lever_PivotPin',[(-8.5,0),(-8.5,2.65),(8.5,2.65),(8.5,0)],'dark','Link',axis='X',center=(124,-1),n=24)
    # Guide lands expose the locking block and the carrier through the top.
    for side in (-1,1):
        lo,hi=sorted((side*7.6,side*10.4))
        box('Carrier_Raceway',(lo,113,7),(hi,173,11),'dark',r=.35)
        a,b=sorted((side*9.7,side*11.0))
        box('Lock_Seat',(a,184,43),(b,186,49),'dark',r=.15)


def barrel_magazine():
    # The barrel includes a visible bore, chamber counterbore and crown return.
    lathe('Barrel',[(BREECH,6.45),(BREECH,12.3),(225,12.3),(285,11.6),
          (600,9.9),(706.8,9.2),(708,8.9),(708,4.1),(707.4,3.85),
          (266,3.85),(257,4.5),(252,4.3),(239.7,4.3),(236.6,5.2),
          (203.1,5.46),(201.62,5.6),(201.62,6.45)],n=48,closed=True)
    lathe('Magazine_Tube',[(204,9.5),(204,10.3),(230,8.1),(694,8.1),(694,7.1),(230,7.1)],center=(0,TUBE),n=48,closed=True)
    lathe('Magazine_Cap',[(694,0),(694,8.1),(697,8.3),(698,8.0),(698,0)],center=(0,TUBE),n=48)
    screw('Magazine_CapScrew',(0,698.1,TUBE),1.7,axis='Y')


def bands():
    """Fitted sleeves: hulls of actual section cuts, with 1.3 mm steel gauge."""
    def section(ob,y):
        ob.data.calc_loop_triangles();points=[]
        for tri in ob.data.loop_triangles:
            vs=[ob.data.vertices[i].co for i in tri.vertices]
            for p,q in zip(vs,vs[1:]+vs[:1]):
                if (p.y-y)*(q.y-y)<0:
                    h=p+(q-p)*((y-p.y)/(q.y-p.y));points.append((h.x,h.z))
        return points
    def hull(points):
        points=sorted(set(points))
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        lower=[];upper=[]
        for p in points:
            while len(lower)>1 and cross(lower[-2],lower[-1],p)<=1e-5:lower.pop()
            lower.append(p)
        for p in reversed(points):
            while len(upper)>1 and cross(upper[-2],upper[-1],p)<=1e-5:upper.pop()
            upper.append(p)
        return lower[:-1]+upper[:-1]
    for name,y,members in [('Forend_Band',432,['Forend','Barrel']),('Muzzle_Band',667,['Magazine_Tube','Barrel'])]:
        inner=hull([p for member in members for p in section(bpy.data.objects[member],y)])
        # Uniform arclength stations keep a sleeve's shallow curvature without
        # paying for every triangulation intersection in the wooden section.
        lengths=[(Vector(inner[(i+1)%len(inner)])-Vector(p)).length for i,p in enumerate(inner)]
        total=sum(lengths);sampled=[];count=40 if name=='Forend_Band' else 32
        for j in range(count):
            target=total*j/count;edge=0
            while target>lengths[edge] and edge<len(inner)-1:target-=lengths[edge];edge+=1
            a=Vector(inner[edge]);b=Vector(inner[(edge+1)%len(inner)])
            sampled.append(tuple(a+(b-a)*(target/lengths[edge])))
        inner=sampled
        outer=[]
        for i,p in enumerate(inner):
            a=Vector(inner[i-1]);b=Vector(p);c=Vector(inner[(i+1)%len(inner)])
            prev=(b-a).normalized();nex=(c-b).normalized()
            n0=Vector((prev.y,-prev.x));n1=Vector((nex.y,-nex.x));n=(n0+n1).normalized()
            outer.append(tuple(b+n*(1.3/max(.6,n.dot(n0)))))
        loops=[[(x,yy,z) for x,z in contour] for yy,contour in [(y-4,outer),(y+4,outer),(y+4,inner),(y-4,inner)]]
        ob=M.ring_loft(name,loops,MAT['blue']);reg(ob,radius=.18,segments=1)
        xmax=max(x for x,z in outer)
        screw(name+'_Screw',(xmax-.25,y,20 if name=='Forend_Band' else 36),1.9)


STOCK=[(-254.2,20.4,-108,8),(-253.5,20.5,-108,8),
       (-248,20.8,-105,9),(-231,21.3,-97,10.5),(-205,21.4,-83,13),
       (-172,20.8,-66,17),(-137,19.9,-49,21.5),(-111,18.9,-37,25),
       (-90,18.1,-30,27),(-72,17.4,-26,27.5),(-64,16.5,-24.3,25),
       (-54,15.6,-23,21),(-42,15.1,-21,20.5),(-25,15,-17,23.5),
       (-10,15.1,-12.4,27),(8,15.35,-7,34),(28,15.5,-2.4,40),
       (47,15.5,.5,45),(62,15.4,.5,50),(65,15.4,.5,50),(65.5,15.4,.5,50)]


def butt_y(y,z):
    # Shallow carbine crescent. Keep the accepted heel/toe and pull-height
    # coordinates; the extra shoulder relief acts below finger height.
    t=max(0,min(1,(-230-y)/24.2))
    extra=5.2*math.sin(math.pi*max(0,min(1,(z+108)/91)))**2 if z < -17 else 0
    return y+t*(3.7*(1-((z+50)/58)**2)+extra)


def stock_section(y,w,lo,hi,n=48):
    # Broad carved flanks, rounded comb, narrower rounded toe. Four changing
    # three-dimensional cage arcs replace the pointed ellipse. The lower
    # side is straighter and narrower than the cheek; no profile extrusion.
    h=hi-lo;roundness=max(0,min(1,(y+90)/80))
    side_top=.19+.10*roundness
    toe_width=.80+.12*roundness
    half=(M.bezier((0,hi),(.66*w,hi),(w,hi-.045*h),(w,hi-side_top*h),12)+
          M.bezier((w,hi-side_top*h),(w,hi-.43*h),(toe_width*w,lo+.24*h),(toe_width*w,lo+.14*h),12)[1:]+
          M.bezier((toe_width*w,lo+.14*h),(.72*w,lo+.015*h),(.27*w,lo),(0,lo),12)[1:])
    contour=half+[(-x,z) for x,z in reversed(half[1:-1])]
    return [(x,y,z) for x,z in contour]


def inlet_tang(stock,name,upper=True):
    """Steel top/bottom conforms to the actual uncut subdivided walnut.

    Build the inlaid tongue from surface rays, then cut a 0.03 mm reveal.
    Topmost metal lies inside the wood's former envelope, including its edges.
    """
    from kit.motion import surface
    tree=surface(stock)['tree'];loops=[]
    ys=[-44,-43,-40,-35,-25,-15,-5,5,15,25,35,43,50,57,63,66]
    for y in ys:
        width=(9.6 if y<=30 else 9.6+(min(65,y)-30)/35*18.4) if upper else 8.0
        # Round the tongue's aft end in plan, while keeping its bearing lands.
        if y < -40:width*=max(.08,math.sqrt(max(0,1-((y+40)/4.1)**2)))
        xs=[-width/2+width*j/8 for j in range(9)];top=[]
        for x in xs:
            p=tree.ray_cast(Vector((x,min(y,64),100 if upper else -150)),Vector((0,0,-1 if upper else 1)),300)[0]
            assert p is not None,(name,x,y)
            top.append((x,y,p.z+(-.045 if upper else .045)))
        depth=-3.5 if upper else 2.0
        loops.append(top+[(x,yy,z+depth) for x,yy,z in reversed(top)])
    tang=M.loft(name,loops,MAT['blue']);tang['boolean_solver']='EXACT'
    reg(tang)
    if not upper:G.dense(tang);G.reduce(tang,300)
    return tang


def furniture():
    ob=M.loft('Stock', [stock_section(*r) for r in STOCK],MAT['wood'])
    ob['boolean_solver']='EXACT'
    G.subdivide(ob,3)
    # Deform the ENTIRE subdivided end cap, including its interior vertices.
    # Warping only the cage perimeter left a chordal wood cap protruding
    # through the curved steel plate in the first exported macro.
    for v in ob.data.vertices:v.co.y=butt_y(v.co.y,v.co.z)
    # Budget the OUTER carved surface before machining. Reducing an already
    # inletted stock moved narrow bearing walls away from the metal. Both
    # retained dense wood and game wood receive the same final metal cutters.
    carved=ob.copy();carved.data=ob.data.copy();bpy.context.collection.objects.link(carved)
    carved.name='Dense carved stock';G.reduce(ob,2100)
    from sections import extract
    ob['uninletted_sections_mm']=json.dumps({str(y):[[[v/1000 for v in p] for p in line]
        for line in extract(ob,y)] for y in (-35,-5,25)})
    def machine(tool):
        dense_tool=tool.copy();dense_tool.data=tool.data.copy();bpy.context.collection.objects.link(dense_tool)
        cut(carved,dense_tool);cut(ob,tool)
    # Fit to unrelieved wood, before the hammer/race clearances are machined.
    for name,upper in [('Upper_Tang',True),('Lower_Tang',False)]:
        tang=inlet_tang(ob,name,upper)
        if upper:
            # Buried integral fork carries both receiver cheeks; the broad
            # head follows the wood rather than lying on top of it.
            for lo,hi in [((-4.4,24.7,32),(4.4,34,37)),
                          ((-13,30,31),(13,35,34)),
                          ((-13,34,31),(-11,66,34)),
                          ((11,34,31),(13,66,34))]:
                cut(tang,box('tool',lo,hi,raw=True),'UNION')
        G.reduce(tang,700 if upper else 300)
        # Inlet the unrelieved solid, rather than scaling an already hollow
        # part and accidentally enlarging its internal voids. Offset its own
        # exterior normals by 0.03 mm for a narrow, physically sensible reveal.
        tool=tang.copy();tool.data=tang.data.copy();bpy.context.collection.objects.link(tool)
        tool.data.update()
        normals=[v.normal.copy() for v in tool.data.vertices]
        for v,n in zip(tool.data.vertices,normals):v.co+=n*.03
        # A flush tongue is slightly inside the original wood envelope. Open
        # its inlet right through that envelope: merely inflating the buried
        # steel left a 15-micrometer wood skin over the metal (z-fighting).
        from kit.motion import surface
        tree=surface(ob)['tree']
        for v in tool.data.vertices:
            p=tree.ray_cast(Vector((v.co.x,min(v.co.y,64),100 if upper else -150)),
                            Vector((0,0,-1 if upper else 1)),300)[0]
            if p is not None and ((upper and v.co.z>p.z-.9) or (not upper and v.co.z<p.z+.6)):
                v.co.z+=5 if upper else -5
        machine(tool)
        if upper:cutbox(tang,(-10.25,-13,38.52),(10.25,67,61),.7)
    # Independent clearance avoids coplanar cuts at the steel race's floor.
    for lo,hi,r in [((-10.35,-13,38.6),(10.35,67,61),.5),((4.5,58,21),(10.8,67,35),.4)]:
        tool=box('tool',lo,hi,raw=True);M.bevel(tool,r,4);M.apply(tool);machine(tool)
    from kit.motion import surface
    tree=surface(ob)['tree']
    head=surface(bpy.data.objects['Upper_Tang'])['tree'].ray_cast(Vector((0,-15,100)),Vector((0,0,-1)),200)[0]
    foot=surface(bpy.data.objects['Lower_Tang'])['tree'].ray_cast(Vector((0,-15,-100)),Vector((0,0,1)),200)[0]
    screw('Stock_TangScrew',(0,-15,head.z-.55),2.2,axis='Z')
    lathe('Stock_TangScrewShank',[(foot.z,0),(foot.z,1.45),(head.z,1.45),(head.z,0)],axis='Z',center=(0,-15),n=16)
    bore=lambda:lathe('tool',[(-100,0),(-100,1.50),(100,1.50),(100,0)],axis='Z',center=(0,-15),n=16,raw=True)
    machine(bore())
    for name in ('Upper_Tang','Lower_Tang'):
        tang=bpy.data.objects[name];cut(tang,bore());G.dense(tang)
    G.HIGH[ob.name]=carved.data.copy();bpy.data.objects.remove(carved,do_unlink=True)
    reg(ob)
    def plate_mesh(name,steps,sides):
        verts=[];faces=[];rings=[]
        for y in (-254.1,-257.2):
            disk=[]
            for j in range(steps+1):
                if j==0:
                    disk.append([len(verts)]);verts.append((0,butt_y(y,-50),-50));continue
                r=j/steps;ring=[]
                for i in range(sides):
                    a=math.tau*i/sides;c,s=math.cos(a),math.sin(a)
                    outline=stock_section(-254.2,20.4,-108,8)
                    # Same outline as the stock end: no separate oval disc.
                    p=outline[i*len(outline)//sides]
                    x=r*p[0];z=-50+r*(p[2]+50)
                    ring.append(len(verts));verts.append((x,butt_y(y,z),z))
                disk.append(ring)
            rings.append(disk)
            for i in range(sides):faces.append((disk[0][0],disk[1][i],disk[1][(i+1)%sides]))
            for a,b in zip(disk[1:],disk[2:]):
                for i in range(sides):faces.append((a[i],b[i],b[(i+1)%sides],a[(i+1)%sides]))
        a,b=rings[0][-1],rings[1][-1]
        for i in range(sides):faces.append((a[i],a[(i+1)%sides],b[(i+1)%sides],b[i]))
        return M.mesh(name,verts,faces,MAT['blue'])
    plate=plate_mesh('Butt_Plate',5,72);reg(plate)
    for z in (-9,-88):
        y=butt_y(-256.7,z)
        slope=(butt_y(-257.2,z+.01)-butt_y(-257.2,z-.01))/.02
        angle=-math.degrees(math.atan(slope))
        tool=lathe('tool',[(y-2,0),(y-2,2.78),(y+.8,2.78),(y+.8,0)],axis='Y',center=(0,z),n=20,raw=True)
        G.rotate_points(tool,(0,y,z),angle);cut(plate,tool)
        ob_screw=screw('Butt_Screw',(0,y,z),2.6,axis='Y',direction=-1)
        G.rotate_points(ob_screw,(0,y,z),angle)
    G.dense(plate)
    # Forend cage: each section changes in width, fullness and channel roll.
    rows=[(205.2,15.0,0.3,43),(206,15.0,0.3,43),(211,16.2,-.1,43.5),
          (226,18.5,-1.8,43.7),(250,19,-2,43.5),(286,19.2,-2,43.1),
          (350,18.8,-1.7,42.5),(403,18.1,-1,41.8),(427,17.9,-.5,41.3),
          (436,17.3,0,40.8),(443,14.2,1.7,38.2),(447,11.7,4.2,35.6),(447.8,11.7,4.2,35.6)]
    loops=[]
    for y,w,lo,hi in rows:
        section=[]
        for i in range(64):
            a=math.tau*i/64;c,s=math.cos(a),math.sin(a)
            x=w*math.copysign(abs(c)**.84,c)
            z=(hi+lo)/2+(hi-lo)/2*math.copysign(abs(s)**.85,s)
            # Broad rounded lands beside the barrel channel, never knife lips.
            if s>0 and abs(x)<12.8:
                channel=BORE-math.sqrt(max(0,12.8**2-x*x))
                h=max(0,min(1,.5+.5*(channel-z)/2.2))
                z=channel*(1-h)+z*h-2.2*h*(1-h)
            section.append((x,y,z))
        loops.append(section)
    fore=M.loft('Forend',loops,MAT['wood']);G.subdivide(fore,2)
    cut(fore,lathe('tool',[(202,0),(202,10.6),(230,8.35),(451,8.35),(451,0)],center=(0,TUBE),n=64,raw=True))
    G.dense(fore);G.reduce(fore,3600);reg(fore)


def sights():
    # Barrel dovetail, sprung leaf and stepped elevation wedge are distinct
    # constructions; the buckhorn has an actual center notch.
    dovetail=[(329,56.9),(339,56.9),(338,61.6),(330,61.6)]
    profile('Rear_Dovetail',dovetail,-7,7,r=.2)
    cut(bpy.data.objects['Barrel'],profile('tool',dovetail,-7.04,7.04,raw=True))
    path=[(334,61.5),(329,62.4),(318,63.1),(300,63.3),(284,64)]
    leaf=G.sweep('Rear_SpringLeaf',path,8,1.35,'blue')
    ladder=[(299,59.4),(321,59.4),(321,60.6),(317,60.6),(317,61.1),
            (313,61.1),(313,61.7),(309,61.7),(309,62.2),(305,62.2),(305,62.7),(299,62.7)]
    profile('Rear_Elevator',ladder,-3.7,3.7,'dark',r=.12)
    box('Elevator_ThumbTab',(-8,299,59.4),(3.7,302,60.7),'dark',r=.35)
    horn=[(-11,63.7),(-11.1,68),(-10.1,72.9),(-8.5,75.8),(-7.8,75.5),
          (-8.9,72.7),(-9.2,70.3),(-8.0,68.1),(-4.4,66.5),(-1.8,66.5),(-1.8,64.6),
          (1.8,64.6),(1.8,66.5),(4.4,66.5),(8.0,68.1),(9.2,70.3),
          (8.9,72.7),(7.8,75.5),(8.5,75.8),(10.1,72.9),(11.1,68),(11,63.7)]
    profile('Rear_Buckhorn',horn,282.5,283.6,axis='Y',r=.10)
    screw('Rear_BladeScrew',(0,284.6,62.9),1.1,axis='Y')
    # Original shallow ramp, pinned blade, and rounded brass bead.
    ramp=[(673,55.6),(698,55.6),(698,61.2),(691,63),(680,62.8),(673,59)]
    ob=profile('Front_Ramp',ramp,-4,4,raw=True)
    tool=bpy.data.objects['Barrel'].copy();tool.data=tool.data.copy();bpy.context.collection.objects.link(tool)
    cut(ob,tool);reg(ob,radius=.35)
    box('Front_Blade',(-1.05,689,61.4),(1.05,691.1,66.1),r=.18)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=1.05,location=(0,690,66))
    ob=bpy.context.object;ob.name='Front_Bead';ob.data.materials.append(MAT['brass']);reg(ob)
    screw('Ramp_Screw',(0,678,60.4),1.4,axis='Z')
