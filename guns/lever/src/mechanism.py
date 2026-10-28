"""Visible, deliberately incomplete lever-action internals and controls."""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
from kit import model as M
import geometry as G
from geometry import MAT, reg, box, lathe, profile, cut, cutbox
from dimensions import HEADS, TUBE_PITCH
from guns.common import ammo_3030


def lever():
    # One forging with two apertures. The long finger opening has nearly
    # straight sides and tight rounded ends, rather than an ellipse hung from
    # a hook. A wide, continuously tapering S web joins it to the pivot.
    # Dimensions are class estimates from rest/open photographs, in mm.
    angle=math.radians(12)
    def place(u,v):return (u*math.cos(angle)-v*math.sin(angle)-6,
                           u*math.sin(angle)+v*math.cos(angle)-30.5)
    def capsule(length,width,outer=False):
        r=width/2;a=length/2-r
        # The concealed upper rail is relieved beneath the accepted lower
        # tang. Full 3.3 mm side depth remains on the hand-ridden lower rail;
        # its outside, never the accepted aperture, supplies the extra depth.
        def height(t):return r*math.sin(t)-(1.1*max(0,math.sin(t))**2 if outer else 0)
        return [place(a+r*math.cos(t),height(t))
                for t in [-math.pi/2+math.pi*i/16 for i in range(17)]]+[
                place(-a+r*math.cos(t),height(t))
                for t in [math.pi/2+math.pi*i/16 for i in range(17)]]
    loop=profile('Lever_FingerLoop',capsule(110.6,35.6,True),-4.1,4.1,raw=True)
    loop['boolean_solver']='EXACT'
    cut(loop,profile('tool',capsule(104,29),-8,8,raw=True))
    # Outer and inner edges are independent curves: the forging thickens
    # organically at the throat instead of showing intersecting tube ends.
    outer=(M.bezier((124,5),(130,-8),(126,-30),(111,-43),10)+
           M.bezier((111,-43),(96,-58.8),(62,-56.7),(49,-35),12)[1:]+
           M.bezier((51,-34),(44,-25),(42,-20),(35,-20),6)[1:]+
           [(35,-10),(49,-6),(58,-4)]+
           M.bezier((58,-4),(62,-20),(56,-31),(72,-38),8)[1:]+
           M.bezier((72,-38),(88,-46),(108,-34),(113,-18),10)[1:]+
           M.bezier((113,-18),(117,-6),(115,0),(118,5),6)[1:])
    cut(loop,profile('tool',outer,-4.1,4.1,raw=True),'UNION')
    # Machine the opening last: the broad S throat must join the perimeter,
    # rather than shortening the finger aperture where the two seeds overlap.
    cut(loop,profile('tool',capsule(104,29),-8,8,raw=True))
    cut(loop,lathe('tool',[(-8,0),(-8,2.75),(8,2.75),(8,0)],axis='X',center=(124,-1),n=32,raw=True))
    reg(loop,'Lever',radius=.38,segments=2)
    bm=bmesh.new();bm.from_mesh(loop.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.01)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.01)
    bmesh.ops.dissolve_limit(bm,angle_limit=.005,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(loop.data);bm.free()
    # Ease only the actual perimeter, after cleaning Boolean edge chains.
    # A pre-cleanup bevel clamped to zero; the loop then had knife edges.
    weight=loop.data.attributes.get('bevel_weight_edge') or loop.data.attributes.new('bevel_weight_edge','FLOAT','EDGE')
    adjacent={}
    for f in loop.data.polygons:
        for i in f.loop_indices:adjacent.setdefault(loop.data.loops[i].edge_index,[]).append(f.normal.x)
    for e in loop.data.edges:
        ns=adjacent[e.index]
        weight.data[e.index].value=float(any(abs(n)>.99 for n in ns) and any(abs(n)<.01 for n in ns))
    bevel=loop.modifiers.new('Forged perimeter roll','BEVEL');bevel.limit_method='WEIGHT'
    bevel.width=.28;bevel.segments=3;bevel.use_clamp_overlap=False;M.apply(loop)
    loop.data.normals_split_custom_set([(0,0,0)]*len(loop.data.loops));M.smooth(loop,42)
    G.dense(loop)
    hub=lathe('Lever_Hub',[(-5,0),(-5,6.2),(5,6.2),(5,0)],bone='Lever',axis='X',center=(124,-1),n=40,raw=True)
    cut(hub,lathe('tool',[(-6,0),(-6,2.75),(6,2.75),(6,0)],axis='X',center=(124,-1),n=32,raw=True));reg(hub,'Lever')
    box('Lever_LatchLand',(-4,53,-6),(4,60,-3),'dark','Lever',r=.2)
    box('Tang_LatchSeat',(-4,52.5,-3),(4,60.5,-1.5),'dark',r=.15)
    # Dropping lower link, front pivot and side rails. Its open position makes
    # space for a rifle cartridge, rather than leaving a fixed bottom plate.
    path=[(195,5),(174,2),(144,0),(115,-1),(96,2)]
    for side in (-1,1):
        ob=G.sweep('Link_Rail',path,2.6,6.2,bone='Link')
        for v in ob.data.vertices:v.co.x+=side*7.0
        cut(ob,lathe('tool',[(-12,0),(-12,2.5),(12,2.5),(12,0)],axis='X',center=(195,5),n=24,raw=True))
    box('Link_RearBridge',(-7.0,95,-.9),(7.0,101,4.4),'dark','Link',r=.6)
    lathe('Link_PivotPin',[(-15,0),(-15,2.35),(15,2.35),(15,0)],'dark',axis='X',center=(195,5),n=24)


def bolt_lock_carrier():
    ob=box('Bolt_Body',(-9.5,79.5,40),(9.5,200,56),'dark','Bolt',r=0,raw=True)
    # Long underside hammer race, relieved rear, and forward bolt face.
    cutbox(ob,(-7.8,77,36),(7.8,195,54.6),.6)
    cutbox(ob,(-10,79,39),(10,87,43),.3)
    cutbox(ob,(-10,173.8,30),(10,185,49.4),.3)
    reg(ob,'Bolt',radius=.55)
    box('Bolt_Extractor',(-8.8,178,55.7),(-5.9,198.4,57.0),'dark','Bolt',r=.25)
    box('Bolt_ExtractorHook',(-8.6,198,49),(-6.2,200,55),'dark','Bolt',r=.15)
    lathe('FiringPin_Tail',[(79.7,0),(79.7,.75),(86,.75),(86,0)],'dark','Bolt',center=(0,48),n=24)
    lock=box('Locking_Block',(-10.1,176,-5),(10.1,184,49),'dark','LockingBlock',r=0,raw=True)
    # The block's top bears on an underside recess and its rear on the seat.
    cutbox(lock,(-8.5,175,-3),(8.5,185,54),.5);reg(lock,'LockingBlock',radius=.3)
    cutbox(lock,(8.3,175,4),(10.5,185,36),.1)
    dogleg=[(8.5,-5),(10.1,-5),(10.1,4),(13.6,12),(13.6,28),(10.1,36),
            (10.1,49),(8.5,49),(8.5,35.5),(11.8,27),(11.8,13),(8.5,4.5)]
    cut(lock,profile('tool',dogleg,176,184,axis='Y',raw=True),'UNION')
    for s in (-1,1):
        lo,hi=sorted((s*8.5,s*9.5))
        box('Bolt_LockAbutment',(lo,174,43),(hi,176,49),'steel','Bolt',r=.15)
    # Top-pose carrier cradle: inverse-rotate the rest geometry. At +20 degrees
    # the actual trough and cartridge lie horizontally on the chamber axis.
    loops=[]
    for y in (124.0,125.5,182.0,185.0):
        section=[]
        for i in range(21):
            a=math.pi+math.pi*i/20
            section.append((7.1*math.cos(a),y,48+7.1*math.sin(a)))
        for i in range(20,-1,-1):
            a=math.pi+math.pi*i/20
            section.append((6.25*math.cos(a),y,48+6.25*math.sin(a)))
        loops.append(section)
    tray=M.loft('Carrier_Cradle',loops,MAT['steel'])
    G.rotate_points(tray,HEADS['Carrier'],-20);reg(tray,'Carrier')
    arm=G.sweep('Carrier_Arm',[(85,7),(111,12),(153,17)],7.3,3.4,'dark','Carrier')
    cut(arm,lathe('tool',[(-8,0),(-8,2.5),(8,2.5),(8,0)],axis='X',center=(85,7),n=24,raw=True))
    lathe('Carrier_Hub',[(-3.65,2.5),(-3.65,3.3),(3.65,3.3),(3.65,2.5)],'dark','Carrier',axis='X',center=(85,7),n=24,closed=True)
    # This connecting web is built in rest space and bears against the trough.
    box('Carrier_Web',(-3.4,144,15),(3.4,155,19.8),'dark','Carrier',r=.5)
    lathe('Carrier_Pin',[(-10,0),(-10,2.4),(10,2.4),(10,0)],'dark',axis='X',center=(85,7),n=24)


def hammer_trigger_gate():
    # Forged hammer: a changing compound cage plus thumb-spur volume. A dense
    # union retains rounded shoulders; the low copy pays only for silhouette.
    loops=[]
    for z,w,cy,d in [(27.3,6.6,70,10),(28,7.0,70,12),(30,7.4,70,13),
                      (35,7.5,70.5,12),(40,7.1,71.5,11),
                      (45,7.5,73,12),(49,8.0,73,12),(51,8,72,11)]:
        loops.append([(x,cy+y,z) for x,y in M.rounded_rectangle(w,d,1.7,5)])
    ob=M.loft('Hammer',loops,MAT['blue']);G.subdivide(ob,2)
    spur=G.sweep('hammer spur seed',M.bezier((73,44),(72,51),(62,53),(53,59.5),20),10.5,4.6,'blue')
    G.PARTS.remove(spur);cut(ob,spur,'UNION')
    rem=ob.modifiers.new('Forged hammer union','REMESH');rem.mode='VOXEL';rem.voxel_size=.35;M.apply(ob)
    smooth=ob.modifiers.new('Forging shoulder relaxation','SMOOTH');smooth.factor=.5;smooth.iterations=3;M.apply(ob)
    # Photo-derived table inclination: roughly 13 degrees in the accepted
    # 44-degree cocked pose. The rest table therefore returns at -31 degrees.
    # Keep the curved neck below the table's lowest crowned valley, so it
    # cannot blank out the middle of the checkering.
    table_angle=math.radians(-31)
    def table(u,v):return (58+u*math.cos(table_angle)-v*math.sin(table_angle),
                          58+u*math.sin(table_angle)+v*math.cos(table_angle))
    cut(ob,profile('tool',[table(-11.5,-1.4),table(11.5,-1.4),table(11.5,20),table(-11.5,20)],-6.5,6.5,raw=True))
    cut(ob,lathe('tool',[(-8,0),(-8,2.75),(8,2.75),(8,0)],axis='X',center=(70,30),n=32,raw=True))
    cutbox(ob,(-8,79.7,40),(8,90,58),.1)
    G.dense(ob);G.reduce(ob,1400);reg(ob,'Hammer')
    box('Hammer_StrikeLand',(-3.2,78.8,46),(3.2,79.7,50),'dark','Hammer',r=.12)
    # Curved thumb-spur table with 1 mm checkering. Keep the shallow relief in
    # this inspection mesh so the requested native macro can actually judge it.
    # A shared corner grid plus one peak per diamond is a closed heightfield,
    # not floating decoration. Later the dense field can move into the normal.
    nx,ny=12,20;verts=[];faces=[]
    def point(i,j,relief=0):
        x=-6+i;u=j-ny/2
        y,z=table(u,-.018*x*x-.006*u*u+relief)
        return (x,y,z)
    for j in range(ny+1):
        for i in range(nx+1):verts.append(point(i,j))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i;b=a+1;c=b+nx+1;d=a+nx+1
            peak=len(verts);verts.append(point(i+.5,j+.5,.24))
            faces.extend([(a,b,peak),(b,c,peak),(c,d,peak),(d,a,peak)])
    edge=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[
        ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
    bottom=[]
    for v in edge:
        x,y,z=verts[v];bottom.append(len(verts));verts.append((x,y+2*math.sin(table_angle),z-2*math.cos(table_angle)))
    for k,a in enumerate(edge):
        b=edge[(k+1)%len(edge)];faces.append((a,b,bottom[(k+1)%len(edge)],bottom[k]))
    faces.append(tuple(reversed(bottom)))
    pad=reg(M.mesh('Hammer_ThumbPad',verts,faces,MAT['blue']),'Hammer')
    for f in pad.data.polygons:f.use_smooth=False
    G.dense(pad)
    pad['checkering_pitch_mm']=1.0
    lathe('Hammer_PivotPin',[(-4.4,0),(-4.4,2.6),(4.4,2.6),(4.4,0)],'dark',axis='X',center=(70,30),n=24)
    # Visible sear engagement proxy, intentionally omitting working fire-control
    # internals. It establishes a supported pose, not a functioning lock design.
    land=box('Hammer_SearLand',(3,60,28),(7,62,30),'dark','Hammer',r=0)
    G.rotate_points(land,HEADS['Hammer'],-44)
    half=box('Hammer_HalfCockLand',(3,60,28),(7,62,30),'dark','Hammer',r=0)
    G.rotate_points(half,HEADS['Hammer'],-12)
    toe=box('Hammer_HalfCockToe',(3,60,28),(4,66,30),'dark','Hammer',r=0)
    G.rotate_points(toe,HEADS['Hammer'],-12)
    box('Sear_Nose',(5,62,28),(7,65,30),'dark','Sear',r=0)
    arm=G.sweep('Sear_VisualArm',[(66,29),(68,22),(73,10),(81,-3)],2.0,2.0,'dark','Sear')
    for v in arm.data.vertices:v.co.x+=8.5
    box('Sear_Bridge',(5,64,28),(9.5,66,30),'dark','Sear',r=0)
    lathe('Sear_Hub',[(5,1.85),(5,3.8),(9.5,3.8),(9.5,1.85)],'dark','Sear',axis='X',center=(83,0),n=24,closed=True)
    # Concave front faces +Y; lower tip returns forward. Rounded rectangular
    # cross-sections give a broad blade with flat sides, never a wire trigger.
    path=M.bezier((83,0),(90,-3),(89,-7),(87,-10),6)
    path+=M.bezier((87,-10),(83,-18),(82,-24),(86,-30),18)[1:]
    trigger=G.sweep('Trigger_Blade',path,6.0,3.7,'blue','Trigger',section_segments=2)
    cut(trigger,lathe('tool',[(-8,0),(-8,1.85),(8,1.85),(8,0)],axis='X',center=(83,0),n=24,raw=True))
    lathe('Trigger_Hub',[(-3.1,1.85),(-3.1,3.8),(3.1,3.8),(3.1,1.85)],'dark','Trigger',axis='X',center=(83,0),n=24,closed=True)
    lathe('Trigger_Pin',[(-9,0),(-9,1.75),(9,1.75),(9,0)],'dark',axis='X',center=(83,0),n=24)
    # Rear-hinged spring cover. The hinge runs vertically and the nose presses
    # inward; actual reveal remains around the rounded aperture.
    shape=[(y+147.7,z+20) for y,z in M.rounded_rectangle(50.2,12.8,6.0,10)]
    gate=profile('Loading_Gate',shape,14.8,15.70,'blue','LoadingGate',r=.16)
    cut(gate,lathe('tool',[(14,0),(14,.9),(26,.9),(26,0)],axis='Z',center=(15.2,122),n=24,raw=True))
    lathe('Gate_Hinge',[(16,.9),(16,1.4),(24,1.4),(24,.9)],'dark','LoadingGate',axis='Z',center=(15.2,122),n=24,closed=True)
    lathe('Gate_HingePin',[(14.5,0),(14.5,.8),(25.5,.8),(25.5,0)],'dark',axis='Z',center=(15.2,122),n=24)
    G.screw('LoadingGate_Screw',(15.3,118.8,20),1.5)


def ammunition():
    for i in range(6):
        ammo_3030.build('Tube_Round'+str(i+1),HEADS['Tube'+str(i+1)],MAT,G.reg,'Tube'+str(i+1),hidden=True)
    for name,bone in [('Chamber_Live','ChamberRound'),('Carrier_Live','CarrierRound'),('Insert_Live','InsertRound')]:
        base=(0,125,48) if bone=='CarrierRound' else (HEADS[bone] if bone!='InsertRound' else (0,0,0))
        parts=ammo_3030.build(name,base,MAT,G.reg,bone)
        if bone=='CarrierRound':
            for ob in parts:G.rotate_points(ob,HEADS['Carrier'],-20)
        if bone=='InsertRound':
            # InsertGuide supplies the full socket frame; its display child
            # alone uses zero-scale visibility. Rest mesh sits at the guide.
            for ob in parts:
                ob.data.transform(Matrix.Translation(Vector(HEADS['InsertGuide'])))
    ammo_3030.build('Extracted_Case',HEADS['FiredCase'],MAT,G.reg,'FiredCase',fired=True)
    # Follower's rear face touches the final cartridge's flat nose. Spring is
    # omitted inside the opaque tube rather than modeled as wasted geometry.
    y=HEADS['Follower'][1]
    lathe('Magazine_Follower',[(y,0),(y,6.7),(y+5,6.7),(y+6,6.3),(y+6,0)],'dark','Follower',center=(0,20),n=32)


def hammer_inlet():
    """Machine the original stock head and upper tang for their swept hammer.

    The cutter is generated only from our own parts, with .3–.7 mm clearance.
    Its convex envelope makes one rounded internal mortise, avoiding a row of
    sharp intersecting boxes. Both the dense and game stock receive this cut.
    """
    import bmesh
    def remove_machining_crumbs(ob):
        bm=bmesh.new();bm.from_mesh(ob.data);unseen=set(bm.verts);removed=0
        while unseen:
            seed=unseen.pop();group={seed};todo=[seed]
            while todo:
                for e in todo.pop().link_edges:
                    for v in e.verts:
                        if v in unseen:unseen.remove(v);group.add(v);todo.append(v)
            faces={f for v in group for f in v.link_faces}
            span=max(max(v.co[k] for v in group)-min(v.co[k] for v in group) for k in range(3))
            # The race-floor / swept-pocket intersection can leave a tiny
            # detached tetrahedron. Remove only these bounded machining chips,
            # never an unsupported tongue, fork or visible construction part.
            if len(group)<=4 and len(faces)<=4 and span<1.5 and sum(f.calc_area() for f in faces)<1:
                removed+=len(faces);bmesh.ops.delete(bm,geom=list(group),context='VERTS')
        if removed:bm.to_mesh(ob.data);ob['machining_crumb_faces_removed']=removed
        bm.free()
    def remove_collinear_slivers(ob):
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        removed=0
        for _ in range(64):
            candidate=None
            for f in bm.faces:
                if len(f.verts)!=3 or f.calc_area()>=1e-5:continue
                a,b=max(f.edges,key=lambda e:e.calc_length()).verts
                c=next(v for v in f.verts if v not in (a,b));edge=b.co-a.co
                if edge.length_squared<1e-20:continue
                t=(c.co-a.co).dot(edge)/edge.length_squared
                if 0<t<1 and (c.co-(a.co+t*edge)).length<.0001:candidate=c;break
            if candidate is None:break
            # Remove a vertex less than .1 micrometer off its opposite edge.
            # Such ill-conditioned triangles reversed winding after float GLB
            # conversion. Dissolve/retriangulate their fan, keeping it closed.
            bmesh.ops.dissolve_verts(bm,verts=[candidate],use_face_split=False,use_boundary_tear=False)
            bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');removed+=1
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        ob['collinear_vertices_dissolved']=removed
    pivot=Vector(HEADS['Hammer']);points=[]
    for ob in G.PARTS:
        if ob['bone']!='Hammer':continue
        for angle in range(0,91,2):
            rotation=Matrix.Rotation(math.radians(angle),4,'X')
            for v in ob.data.vertices:
                p=pivot+rotation@(v.co-pivot)
                radial=p-pivot
                if radial.length:radial=radial.normalized()*.35
                p+=radial
                points.extend([(abs(p.x)+.35,p.y,p.z),(-abs(p.x)-.35,p.y,p.z)])
    bm=bmesh.new()
    for p in points:bm.verts.new(p)
    result=bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
    bmesh.ops.delete(bm,geom=list(result.get('geom_interior',[])),context='VERTS')
    mesh=bpy.data.meshes.new('Original hammer clearance envelope');bm.to_mesh(mesh);bm.free()
    # The margin already includes .35 mm radial and .35 mm transverse relief.
    # Budget the hidden cutter, rather than decimating its finished bearing
    # seams afterwards. The unchanged all-clip sweep tests the actual result.
    envelope=bpy.data.objects.new('Hammer clearance budget',mesh);bpy.context.collection.objects.link(envelope)
    G.reduce(envelope,180);mesh=envelope.data.copy();bpy.data.objects.remove(envelope,do_unlink=True)
    for name in ('Stock','Upper_Tang'):
        ob=bpy.data.objects[name]
        tool=bpy.data.objects.new('tool',mesh.copy());bpy.context.collection.objects.link(tool)
        cut(ob,tool)
        if name=='Upper_Tang':remove_machining_crumbs(ob)
        if name in G.HIGH:
            hi=bpy.data.objects.new('Dense stock inlet',G.HIGH[name].copy());bpy.context.collection.objects.link(hi)
            hi['boolean_solver']='EXACT'
            tool=bpy.data.objects.new('tool',mesh.copy());bpy.context.collection.objects.link(tool)
            cut(hi,tool)
            if name=='Upper_Tang':remove_machining_crumbs(hi);remove_collinear_slivers(hi)
            G.triangulate_cuts(hi);M.smooth(hi,42);G.HIGH[name]=hi.data.copy();bpy.data.objects.remove(hi,do_unlink=True)

        # Preserve silhouette while paying for the inlet only once. Remove
        # numerical Boolean slivers before reduction, in millimeter space.
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.002)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.002)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(ob.data);bm.free()
        if name=='Upper_Tang':
            remove_collinear_slivers(ob)
            tri=ob.modifiers.new('Stable concave machining triangles','TRIANGULATE');tri.ngon_method='CLIP';M.apply(ob)
            G.dense(ob)
        M.smooth(ob,42)
