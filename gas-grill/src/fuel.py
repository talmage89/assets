"""Grill-owned spring hanger, foot-ring restraint, coupling, regulator and hose.

No cylinder, valve or cylinder markings are generated or imported here.
"""
import math
import bpy
from mathutils import Vector,Matrix
from kit import model as G,rig
from fit_spec import TANK_POSITION,TANK_YAW,TANK_RADIUS,VALVE_FACE,tank_point


def build_fuel(b):
    socket=G.pivot('tank_socket',TANK_POSITION);socket.parent=b.root
    socket.rotation_euler.z=TANK_YAW;socket['socket_kind']='external_tank'
    socket['reference_asset']='owner canonical propane-tank.glb, optional fit only'
    build_hanger(b)
    connection=build_regulator(b)
    # Old original regulator coordinates -> its coupling mating-face frame.
    rebase=Matrix.Translation((0,.018,-.389))
    for ob in connection.children:ob.data.transform(rebase)
    connection.location=tank_point(VALVE_FACE);connection.rotation_euler.z=TANK_YAW
    bpy.context.view_layer.update()
    hose_end=tank_point(VALVE_FACE+Vector((0,-.133,-.059)))
    path=[];steps=40 if b.high else 24
    for i in range(steps+1):
        t=i/steps;angle=TANK_YAW-math.pi/2-math.radians(114)*t**1.3
        radius=.1749+.045*(2*t-t*t)
        z=.3645-.12*math.sin(math.pi*t)-.060*t
        path.append(tuple(TANK_POSITION+Vector((radius*math.cos(angle),radius*math.sin(angle),z))))
    assert (Vector(path[0])-hose_end).length<1e-6
    tangent=Vector((-.249,.511,.317)).normalized()
    control=Vector(path[-1])+tangent*.09
    path+=G.bezier(path[-1],tuple(control),(.278,-.232,.703),(.260,-.277,.748),steps)[1:]
    path=list(reversed(path))  # manifold root -> ferrule
    sides=16 if b.high else 8
    hose=b.tube('LP flexible hose',path,.0052,'rubber',sides)
    samples,distances=rig.arc_samples(path,[0,.2,.4,.6,.8,1])
    mate=tank_point(VALVE_FACE)
    arm=rig.chain('HoseRig',samples+[mate],b.root)
    names=[bone.name for bone in arm.data.bones]
    weights=[]
    for index in range(len(hose.data.vertices)):
        f=distances[index//sides]/distances[-1]*5
        left=min(4,int(f));blend=max(0,min(1,f-left));blend=blend*blend*(3-2*blend)
        weights.append({names[left]:1-blend,names[left+1]:blend})
    rig.bind(hose,arm,weights,export_part='HoseAssembly')
    for ob in list(connection.children):
        rig.bind(ob,arm,[{names[-1]:1.0} for _ in ob.data.vertices],export_part='HoseAssembly')
    bpy.data.objects.remove(connection,do_unlink=True)
    b.cylinder('Manifold hose union',(.260,-.277,.733),(.260,-.277,.754),.009,'brass',6)
    attach=G.pivot('regulator_attach',(0,0,0));attach.parent=arm
    attach.parent_type='BONE';attach.parent_bone=names[-1]
    bpy.context.view_layer.update()
    transform=Matrix.Rotation(TANK_YAW,4,'Z');transform.translation=mate
    attach.matrix_world=b.root.matrix_world@transform
    attach['socket_kind']='coupling mating face; local +Y toward tank'
    arm['hose_length_m']=distances[-1];arm['bone_count']=6
    arm['bone_lengths_m']=[bone.length for bone in arm.data.bones]
    arm['rest_frames']=[v for bone in arm.data.bones for row in bone.matrix_local for v in row]
    arm['hose_rest_points_m']=[v for point in path for v in point]
    print('HOSE_LENGTH_M',distances[-1],flush=True)
    return arm


def build_hanger(b):
    x,y=.344,-.010
    plate=G.profile('Tank scale folded backplate',[(y-.027,.504),(y+.027,.504),(y+.027,.683),(y-.027,.683)],x-.001,x+.001,b.mat('powder'))
    b.add(plate)
    for z in (.523,.664):
        # Formed C straps bridge the right upright to the scale backplate.
        bracket=G.profile('Scale bridge bracket',[(.325,z-.009),(.345,z-.009),(.345,z+.009),(.343,z+.009),(.343,z-.007),(.325,z-.007)],-.235,.010,b.mat('powder'),axis='Y')
        G.bevel(bracket,.0005,b.edges);b.add(bracket)
        b.fastener('Scale mounting bolt',(x+.002,y,z),(1,0,0),radius=.004)
    for yy in (y-.027,y+.027):b.box('Scale folded side flange',(x+.009,yy,.593),(.018,.002,.176),'powder',.0005)
    b.box('Tank scale moving carriage',(x+.018,y,.620),(.012,.047,.048),'powder',.002)
    # J-hook passes outside the handle lip and lifts its underside at z=.436.
    points=[Vector((.362,-.016,.648)),tank_point((-.110,0,.447))]
    points+=list(map(Vector,G.bezier((-.110,0,.447),(-.110,0,.435),(-.110,0,.426),(-.104,0,.428),8 if b.high else 4)[1:]))
    # The previous segment is authored in the canonical tank frame.
    points=points[:2]+[tank_point(p) for p in points[2:]]
    points += [tank_point(p) for p in G.bezier((-.104,0,.428),(-.101,0,.429),(-.098,0,.432),(-.094,0,.432),8 if b.high else 4)[1:]]
    b.tube('Tank collar load hook',[tuple(p) for p in points],.004,'stainless',12 if b.high else 6)
    b.box('Scale spring anchor',(x+.016,y,.674),(.018,.018,.012),'stainless',.001)
    if b.high:
        points=[]
        for i in range(161):
            t=i/160;a=t*math.tau*10
            points.append((x+.018+.007*math.cos(a),y+.007*math.sin(a),.639+t*.027))
        b.tube('Tank scale extension spring',points,.001,'stainless',6)
    label=G.plane_uv('Tank scale graduated plate',[(.367,y-.021,.520),(.367,y+.021,.520),(.367,y+.021,.670),(.367,y-.021,.670)],b.mat('scale_print'));b.add(label)
    b.box('Scale level indicator',(.371,y,.600),(.003,.046,.005),'red',.001)
    # A bolted arm and lined C-cradle retain the actual 210 mm foot ring.
    z=TANK_POSITION.z+.025
    arc=[tuple(TANK_POSITION+Vector((.1095*math.cos(a),.1095*math.sin(a),.025))) for a in [math.radians(220-i*80/(24 if b.high else 10)) for i in range((24 if b.high else 10)+1)]]
    path=[(.313,-.253,z),(.350,-.253,z),(.395,-.150,z),(.400,-.093,z)]+arc
    b.tube('Foot ring retention cradle',path,.0045,'powder',10 if b.high else 6)
    b.box('Foot ring cradle mounting plate',(.313,-.2475,z),(.034,.005,.045),'powder',.002)
    b.fastener('Foot ring cradle anchor',(.313,-.250,z+.012),radius=.004)
    for a in (math.radians(155),math.radians(205)):
        p=TANK_POSITION+Vector((.110*math.cos(a),.110*math.sin(a),.025))
        pad=G.box('Foot ring cradle rubber pad',p,(.010,.016,.014),b.mat('rubber'),.002 if b.high else 0,b.edges)
        pad.rotation_euler.z=a;b.add(pad)


def build_regulator(b):
    connection=G.pivot('Regulator_connection',(0,0,0));connection.parent=b.root
    # Ribbed Type 1 nut threads onto the CGA-791 outlet *inside* the front collar.
    b.lathe('Type 1 coupling nut',[(-.008,.017),(-.010,.023),(-.027,.026),(-.049,.026),(-.058,.017),(-.058,.010)],
            'plastic',64 if b.high else 24,axis='Y',center=(0,.389),closed=True,parent=connection)
    for i in range(10):
        angle=i*math.tau/10
        x=.024*math.cos(angle);z=.389+.024*math.sin(angle)
        rib=G.box('Coupling nut finger rib',(x,-.037,z),(.004,.023,.004),b.mat('plastic'),.0007,b.edges)
        rib.rotation_euler.y=-angle;b.add(rib,connection)
    b.cylinder('Regulator inlet brass stem',(0,-.054,.389),(0,-.079,.389),.008,'brass',24 if b.high else 10,connection)
    b.cylinder('Regulator inlet elbow',(0,-.079,.389),(0,-.091,.394),.009,'zinc',24 if b.high else 10,connection)
    normal=Vector((0,-.47,.883)).normalized()
    transform=normal.to_track_quat('Z','Y').to_matrix().to_4x4();transform.translation=(0,-.106,.379)
    # Two pressed shells, rolled crimp, domed cover and a recessed label land.
    profile=[(-.005,0),(-.005,.021),(-.003,.027),(0,.0305),(.003,.0305),
             (.004,.027),(.010,.025),(.012,.018),(.012,.009),(.012,0)]
    cover=G.lathe('Regulator pressed dome and crimp',profile,b.mat('zinc'),96 if b.high else 32)
    cover.matrix_world=transform;b.add(cover,connection)
    rim=G.lathe('Regulator rolled perimeter seam',[(0,.029),(.001,.031),(.003,.031),(.004,.029)],b.mat('zinc'),96 if b.high else 32,closed=True)
    rim.matrix_world=transform;b.add(rim,connection)
    if b.high:
        for i in range(24):
            a=i*math.tau/24
            p=transform@Vector((.0305*math.cos(a),.0305*math.sin(a),.001))
            b.cylinder('Regulator edge crimp',p,p+normal*.001,.001,'zinc',8,connection)
    # Stamped radial reinforcing ribs and original identification on the cover.
    if b.high:
        for angle in (-.7,.6,2.3):
            line=[transform@Vector((r*math.cos(angle),r*math.sin(angle),.0122-max(0,r-.018)/.007*.002)) for r in (.010,.014,.018,.022)]
            b.tube('Regulator pressed reinforcing rib',[tuple(p) for p in line],.00045,'zinc',6,connection)
        # Original neutral type stamp, generated from an installed open font.
        curve=bpy.data.curves.new('Regulator identification type','FONT')
        curve.body='R1  LP';curve.size=.0042;curve.align_x='CENTER';curve.extrude=0
        curve.font=bpy.data.fonts.load('/usr/share/fonts/TTF/DejaVuSans.ttf')
        text=bpy.data.objects.new('Regulator original pressed stamp',curve);bpy.context.collection.objects.link(text)
        text.matrix_world=transform; text.location=transform@Vector((0,-.002,.0121))
        bpy.context.view_layer.objects.active=text;text.select_set(True)
        bpy.ops.object.convert(target='MESH');text=bpy.context.view_layer.objects.active;text.select_set(False)
        text.data.materials.append(b.mat('zinc'));text['allow_boundary']=True;b.add(text,connection)
    # Vent is a separate small punched feature in the cover.
    vent=transform@Vector((.014,.004,.0122))
    b.cylinder('Regulator diaphragm vent',vent,vent+normal*.0004,.0018,'soot',12 if b.high else 6,connection)
    outlet0=Vector((0,-.124,.360));outlet1=Vector((0,-.134,.350))
    b.cylinder('Regulator outlet hose barb',outlet0,outlet1,.0055,'brass',24 if b.high else 10,connection)
    b.cylinder('Hose swaged steel ferrule',outlet1,Vector((0,-.151,.330)),.007,'stainless',24 if b.high else 12,connection)
    if b.high:
        for t in (.2,.42,.65,.86):
            p=outlet1.lerp(Vector((0,-.151,.330)),t)
            direction=(Vector((0,-.151,.330))-outlet1).normalized()
            b.cylinder('Ferrule crimp groove',p-direction*.0003,p+direction*.0003,.0072,'stainless',16,connection)
    return connection
