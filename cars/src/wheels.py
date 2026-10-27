"""Original 18 x 7.5 six-fork alloy wheel, ISO tire and fixed caliper assembly."""
import math
from kit import model as G
from kit.vehicle import loaded_tire
from mathutils import Vector
from detail_helpers import box,print_quad


def shoulder_blocks(b,name,pos,spin,material,S):
    """Closed tapered lugs embedded in the carcass at both tread shoulders.

    Fine central blocks/sipes remain height only. The lug crowns stay below
    the nominal tread crown and use the same parked contact flattening.
    """
    vertices=[];faces=[];count=28
    for side in [-1,1]:
        for k in range(count):
            angle=math.tau*(k+.25*(side+1))/count;start=len(vertices)
            for depth in [-.007,.002]:
                for axial,radius,delta in [(.093,S.TIRE_RADIUS-.004,-.074),(.127,S.TIRE_RADIUS-.019,-.056),(.127,S.TIRE_RADIUS-.019,.071),(.093,S.TIRE_RADIUS-.004,.074)]:
                    t=angle+delta;rim=S.RIM_INCHES*.0254/2
                    r=radius+depth;r=rim+(r-rim)*(S.HUB_HEIGHT-rim)/(S.TIRE_RADIUS-rim);z=r*math.sin(t)
                    vertices.append((pos[0]+side*axial,pos[1]+r*math.cos(t),pos[2]+z))
            faces.extend(tuple(start+i for i in f) for f in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    ob=G.mesh(name,vertices,faces,material);b.add(ob,spin,'tires')


def build(b,S):
    for side,sign in [('L',-1),('R',1)]:
        for end,y in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            pos=(sign*S.TRACK/2,y,S.HUB_HEIGHT);parent=b.root
            if end=='F':
                axis=Vector((-sign*math.tan(math.radians(12)),math.tan(math.radians(6.5)),1)).normalized()
                ground=Vector((sign*(S.TRACK/2-.040),y-.045,0))
                kingpin=ground+axis*(S.HUB_HEIGHT/axis.z)
                steer=G.pivot('Steer_'+end+side,kingpin,'Z',(-35,35));steer.parent=b.root
                steer.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
                steer['kingpin_axis_vehicle']=list(axis);steer['kingpin_ground_point']=list(ground)
                steer['kingpin_status']='authored 12 degree SAI / 6.5 degree caster, 40 mm scrub; measured on exported axis'
                parent=steer
            spin=G.pivot('Wheel_'+end+side,pos,'X',(-360,360))
            __import__('bpy').context.view_layer.update();world=spin.matrix_world.copy()
            spin.parent=parent;spin.matrix_world=world
            tire=loaded_tire('Tire_'+end+side,pos,S.TIRE_WIDTH,S.TIRE_ASPECT,S.RIM_INCHES,
                b.m['tire_'+side] if b.detail else b.m['rubber'],96 if b.high else 64,S.HUB_HEIGHT,
                profile_indices=None if b.high else [0,1,3,4,5,7,9,10,11,13,14],rolling_radius=S.HUB_HEIGHT)
            b.add(tire,spin,'tires')
            if b.detail:shoulder_blocks(b,'Shoulder tread_'+end+side,pos,spin,b.m['tire_'+side],S)
            cx=pos[0];r=S.RIM_INCHES*.0254/2
            profile=[(-.093,r-.020),(-.093,r+.005),(-.081,r+.005),(.084,r-.008),(.099,r+.006),(.103,r-.015)]
            ob=G.lathe('Wheel barrel_'+end+side,[(cx+sign*x,rr) for x,rr in profile],b.m['wheel'],64 if b.high else 40,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
            b.add(ob,spin,'wheels')
            hub=G.lathe('Wheel center_'+end+side,[(cx+sign*.068,0),(cx+sign*.068,.065),(cx+sign*.118,.065),(cx+sign*.129,.052),(cx+sign*.129,0)],b.m['wheel'],32 if b.high else 24,axis='X',center=(y,S.HUB_HEIGHT))
            b.add(hub,spin,'wheels')
            for k in range(6):
                angle=math.tau*k/6+.15
                # A single cast Y-spoke, with one continuous face and small
                # edge chamfer; overlapping branch strips left bright seams.
                outline=[(.058,-.024),(.114,-.029),(.211,-.046),(.219,-.022),(.146,-.013),(.130,0),(.146,.013),(.219,.022),(.211,.046),(.114,.029),(.058,.024)]
                loops=[]
                for inset,back in [(True,0),(False,-.0018),(False,-.027)]:
                    ring=[]
                    for radial,tangent in outline:
                        if inset:radial=.135+(radial-.135)*.975;tangent*=.94
                        axial=.145-.20*radial+back
                        ring.append((cx+sign*axial,y+radial*math.cos(angle)-tangent*math.sin(angle),S.HUB_HEIGHT+radial*math.sin(angle)+tangent*math.cos(angle)))
                    loops.append(ring)
                b.add(G.loft('Cast spoke_'+end+side+f'_{k}',loops,b.m['wheel']),spin,'wheels')
                if b.detail:
                    a=math.tau*k/6;cy=y+.041*math.cos(a);cz=S.HUB_HEIGHT+.041*math.sin(a)
                    lug=G.lathe('Wheel lug_'+end+side+str(k),[(cx+sign*.125,0),(cx+sign*.125,.0088),(cx+sign*.137,.0088),(cx+sign*.140,.0068),(cx+sign*.140,0)],b.m['chrome'],6,axis='X',center=(cy,cz))
                    b.add(lug,spin,'wheels')
            if b.detail:
                x=cx+sign*.130
                print_quad(b,'Alder center cap_'+end+side,[(x,y-sign*.029,S.HUB_HEIGHT-.010),(x,y+sign*.029,S.HUB_HEIGHT-.010),(x,y+sign*.029,S.HUB_HEIGHT+.010),(x,y-sign*.029,S.HUB_HEIGHT+.010)],b.m['badge'],'wheels',spin)
                # Disc rotates; caliper follows the knuckle but never the wheel.
                rotor=G.lathe('Brake rotor_'+end+side,[(cx+sign*.008,.061),(cx+sign*.008,.161),(cx+sign*.028,.161),(cx+sign*.028,.104),(cx+sign*.045,.091),(cx+sign*.045,.061)],b.m['brake'],48 if b.high else 32,axis='X',center=(y,S.HUB_HEIGHT),closed=True)
                rotor.data.materials.append(b.m['caliper'])
                for f in rotor.data.polygons:
                    radius=sum(math.hypot(rotor.data.vertices[i].co.y-y,rotor.data.vertices[i].co.z-S.HUB_HEIGHT) for i in f.vertices)/len(f.vertices)
                    if radius<.102:f.material_index=1
                b.add(rotor,spin,'brakes')
                # Cast U-section: two pad carriers straddle the disc with a
                # 31 mm open slot; the bridge clears its 161 mm outside radius.
                profile=[(-.015,.112),(-.015,.181),(.052,.181),(.052,.112),
                         (.034,.112),(.034,.168),(.003,.168),(.003,.112)]
                caliper=G.profile('Brake caliper_'+end+side,profile,-.056,.056,b.m['caliper'],axis='Z',radius=.002,segments=2 if b.high else 1)
                angle=math.atan2(.035,.132)
                for vertex in caliper.data.vertices:
                    axial,radial,tangent=vertex.co
                    vertex.co=(cx+sign*axial,y+radial*math.cos(angle)-tangent*math.sin(angle),
                               S.HUB_HEIGHT+radial*math.sin(angle)+tangent*math.cos(angle))
                if sign<0:
                    for face in caliper.data.polygons:face.flip()
                caliper=b.add(caliper,parent,'brakes')
                caliper['wheel_clearance_basis']='Actual axial and radial mesh clearances measured by check_detail.py'
