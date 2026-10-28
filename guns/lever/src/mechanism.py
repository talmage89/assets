"""Visible, deliberately incomplete lever-action internals and controls."""
import math
import bpy
from mathutils import Vector, Matrix
from kit import model as M
import geometry as G
from geometry import MAT, reg, box, lathe, profile, cut, cutbox
from dimensions import HEADS, TUBE_PITCH
from guns.common import ammo_3030


def lever():
    # Two apertures distinguish the forward trigger bow and the rear finger
    # opening; forged flat sections have width as well as an edge radius.
    G.sweep('Lever_FingerLoop',G.circle_path(10,-27,48,14,48,10),8.2,3.4,bone='Lever',closed=True,section_segments=2)
    path=M.bezier((52,-16),(49,-43),(109,-47),(116,-13),24)
    path+=M.bezier((116,-13),(120,-5),(121,-2),(124,-1),7)[1:]
    bow=G.sweep('Lever_TriggerBow',path,9.5,4.8,bone='Lever',section_segments=2)
    cut(bow,lathe('tool',[(-8,0),(-8,2.75),(8,2.75),(8,0)],axis='X',center=(124,-1),n=32,raw=True))
    G.sweep('Lever_Spine',[(-38,-23.5),(-21,-19),(0,-13),(26,-6.3),(52,-5.9),(52,-18.5)],8.2,3.2,bone='Lever')
    G.sweep('Lever_RearNeck',[(-38,-33),(-38,-23.5)],8.2,3.2,bone='Lever')
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
    for z,w,cy,d in [(28,7.0,70,12),(30,8,70,13),(35,8,70.5,12),
                      (42,7.2,71.8,10),(46,7.8,73,11),(50,9.0,74.5,12),
                      (52,8.5,74,11)]:
        loops.append([(x,cy+y,z) for x,y in M.rounded_rectangle(w,d,1.7,5)])
    ob=M.loft('Hammer',loops,MAT['blue']);G.subdivide(ob,2)
    spur=G.sweep('hammer spur seed',M.bezier((72,43),(72,54),(76,60),(78,62),16),11.0,7.0,'blue')
    G.PARTS.remove(spur);cut(ob,spur,'UNION')
    rem=ob.modifiers.new('Forged hammer union','REMESH');rem.mode='VOXEL';rem.voxel_size=.5;M.apply(ob)
    smooth=ob.modifiers.new('Forging shoulder relaxation','SMOOTH');smooth.factor=.5;smooth.iterations=3;M.apply(ob)
    cut(ob,lathe('tool',[(-8,0),(-8,2.75),(8,2.75),(8,0)],axis='X',center=(70,30),n=32,raw=True))
    cutbox(ob,(-8,79.7,40),(8,90,58),.1)
    G.dense(ob);G.reduce(ob,1600);reg(ob,'Hammer')
    box('Hammer_StrikeLand',(-3.2,78.8,46),(3.2,79.7,50),'dark','Hammer',r=.12)
    # The thumb pad has actual broad transverse dimensions. Fine crosshatching
    # belongs to the later normal bake; it is retained on a separate high source.
    pad=box('Hammer_ThumbPad',(-6.5,72,58),(6.5,82,62),'blue','Hammer',r=1.0)
    G.dense(pad)
    hi=bpy.data.objects.new('Dense thumb-pad checkering',G.HIGH[pad.name].copy());bpy.context.collection.objects.link(hi)
    for angle in (-45,45):
        for j in range(-9,10):
            tool=profile('tool',[(j*1.1-.16,62.6),(j*1.1+.16,62.6),(j*1.1,61.75)],-16,16,axis='Y',raw=True)
            tool.data.transform(Matrix.Translation(Vector((0,77,0)))@Matrix.Rotation(math.radians(angle),4,'Z'))
            cut(hi,tool)
    G.HIGH[pad.name]=hi.data.copy();bpy.data.objects.remove(hi,do_unlink=True)
    pad['high_detail']='original crossed V cuts; retained for the later normal bake'
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
    trigger=G.sweep('Trigger_Blade',path,4.8,2.4,'blue','Trigger')
    cut(trigger,lathe('tool',[(-8,0),(-8,1.85),(8,1.85),(8,0)],axis='X',center=(83,0),n=24,raw=True))
    lathe('Trigger_Hub',[(-3.1,1.85),(-3.1,3.8),(3.1,3.8),(3.1,1.85)],'dark','Trigger',axis='X',center=(83,0),n=24,closed=True)
    lathe('Trigger_Pin',[(-9,0),(-9,1.75),(9,1.75),(9,0)],'dark',axis='X',center=(83,0),n=24)
    # Rear-hinged spring cover. The hinge runs vertically and the nose presses
    # inward; actual reveal remains around the rounded aperture.
    shape=[(y+148,z+20) for y,z in M.rounded_rectangle(51.8,12.5,5.8,10)]
    gate=profile('Loading_Gate',shape,14.3,15.25,'blue','LoadingGate',r=.3)
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
    for name in ('Stock','Upper_Tang'):
        ob=bpy.data.objects[name]
        tool=bpy.data.objects.new('tool',mesh.copy());bpy.context.collection.objects.link(tool)
        cut(ob,tool)
        if name in G.HIGH:
            hi=bpy.data.objects.new('Dense stock inlet',G.HIGH[name].copy());bpy.context.collection.objects.link(hi)
            tool=bpy.data.objects.new('tool',mesh.copy());bpy.context.collection.objects.link(tool)
            cut(hi,tool);G.HIGH[name]=hi.data.copy();bpy.data.objects.remove(hi,do_unlink=True)

        # Preserve silhouette while paying for the inlet only once. Remove
        # numerical Boolean slivers before reduction, in millimeter space.
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.002)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.002)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(ob.data);bm.free()
        if name=='Stock':G.reduce(ob,5700)
        M.smooth(ob,42)
