"""Independent evaluated-surface contacts and longitudinal placement audit."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
import bpy
from mathutils import Vector
from kit import motion,assembly,weapon as W
from trigger_check import gap

def dimensions(arm):
    W.pose(arm,'Idle',0)
    def surf(name):return motion.surface(bpy.data.objects[name])
    bolt=surf('Bolt_Body');case=surf('Magazine_TopRound_Case');bullet=surf('Magazine_TopRound_Bullet')
    chamber=surf('ChamberRound_Case')
    shell=surf('Magazine_Shell')['tree']
    origin=Vector((0,(case['lo'].y+bullet['hi'].y)/2,.010))
    back=shell.ray_cast(origin,Vector((0,-1,0)),.2)[0]
    front=shell.ray_cast(origin,Vector((0,1,0)),.2)[0]
    if 'Magazine_Binder' in bpy.data.objects:
        hit=surf('Magazine_Binder')['tree'].ray_cast(origin,Vector((0,1,0)),.2)[0]
        if hit is not None and (front is None or hit.y<front.y):front=hit
    assert back is not None and front is not None
    closed=bolt['hi'].y
    mouth=surf('Barrel')['lo'].y
    tip=bullet['hi'].y;head=case['lo'].y
    ramp=surf('Feed_Ramp')['lo'].y if 'Feed_Ramp' in bpy.data.objects else None
    W.pose(arm,'Fire',70);open_face=surf('Bolt_Body')['hi'].y
    W.pose(arm,None,0)
    return dict(closed_bolt_face_y_m=closed,chamber_case_head_y_m=chamber['lo'].y,
        magazine_case_head_y_m=head,magazine_tip_y_m=tip,
        closed_face_to_magazine_head_m=closed-head,
        tip_to_chamber_mouth_m=mouth-tip,
        tip_to_ramp_m=None if ramp is None else ramp-tip,
        rear_inside_y_m=back.y,front_inside_y_m=front.y,
        internal_length_m=front.y-back.y,head_to_rear_wall_m=head-back.y,
        tip_to_front_wall_m=front.y-tip,bolt_draw_m=closed-open_face,
        open_face_behind_head_m=head-open_face,
        method='evaluated triangle bounds and rays to actual inner wall/binder surfaces')

def contacts(arm):
    rows=[]
    def pair(clip,f,a,b,limit,kind):
        W.pose(arm,clip,f)
        d,method=assembly.distance(bpy.data.objects[a],bpy.data.objects[b])
        if d>limit:
            d=gap(motion.surface(bpy.data.objects[a]),motion.surface(bpy.data.objects[b]));method='triangle vertex/face and edge/edge minimum'
        rows.append(dict(clip=clip,frame=f,parts=[a,b],kind=kind,
            distance_m=d,limit_m=limit,method=method,passed=d<=limit))
    for clip in ('Fire','FireLast'):
        for f in (46,50,56,60,61.6,62,62.5):
            pair(clip,f,'CycleCase_Case','Bolt_Extractor_Hook',.00022,'case rim retained by extractor')
    for clip,begin,end in [('Fire',76,104),('ReloadEmpty',195,219)]:
        # Times include pickup, lip retention, ramp travel, mouth entry and seat.
        for ratio in (.04,.08,.12,.18,.25,.35,.45,.6,.75,.9,.98):
            f=begin+(end-begin)*ratio
            pair(clip,f,'Magazine_TopRound_Case','Bolt_Body',.00022,'case head on bolt face')
            case=motion.surface(bpy.data.objects['Magazine_TopRound_Case'])
            bolt=motion.surface(bpy.data.objects['Bolt_Body'])
            gap_m=case['lo'].y-bolt['hi'].y
            rows.append(dict(clip=clip,frame=f,kind='rim rear plane coincides with bolt face',
                signed_gap_m=gap_m,distance_m=abs(gap_m),limit_m=.00002,passed=abs(gap_m)<=.00002,
                method='actual minimum case Y minus actual maximum bolt-face Y'))
        for ratio in (.04,.08,.12):
            f=begin+(end-begin)*ratio
            for suffix in ('','.001'):
                pair(clip,f,'Magazine_TopRound_Case','Magazine_FeedLip'+suffix,.00022,'case retained under feed lip')
        for ratio in (.2,.28,.36):
            f=begin+(end-begin)*ratio
            # Both pieces together form the cartridge's lower envelope.
            W.pose(arm,clip,f)
            ramp=motion.surface(bpy.data.objects['Feed_Ramp'])
            distances=[gap(motion.surface(bpy.data.objects[n]),ramp)
                       for n in ('Magazine_TopRound_Case','Magazine_TopRound_Bullet')]
            rows.append(dict(clip=clip,frame=f,kind='cartridge supported by ramp',
                distance_m=min(distances),limit_m=.0003,passed=min(distances)<=.0003))
        for ratio in (.55,.75,.95):
            pair(clip,begin+(end-begin)*ratio,'Magazine_TopRound_Case','Barrel',.00035,'case guided by chamber mouth')
        for f in (end,end+3,end+7):
            for suffix in ('','.001'):
                pair(clip,f,'Magazine_ReserveRound_Case','Magazine_FeedLip'+suffix,.00022,'next case retained under lips')
            pair(clip,f,'Magazine_ReserveRound_Case','Magazine_Follower',.00022,'raised follower supports next case')
    W.pose(arm,None,0)
    return rows

def handoff(arm):
    """Measure an engine's case spawn frame and velocity from evaluated keys."""
    def frame(f):
        W.pose(arm,'Fire',f);b=arm.pose.bones['CycleCase']
        d=arm.matrix_world@b.matrix@b.bone.matrix_local.inverted()@arm.matrix_world.inverted()
        return d@Vector((0,.2095,.065)),d.to_quaternion()
    p0,q0=frame(63.99);p1,q1=frame(64.01);p,q=frame(64)
    velocity=(p1-p0)/(.02/60);dq=q1@q0.inverted()
    if dq.w<0:dq.negate()
    angular=dq.axis*(dq.angle/(.02/60))
    case=motion.surface(bpy.data.objects['CycleCase_Case'])
    receiver=motion.surface(bpy.data.objects['Receiver'])
    row=dict(event_frame=64,origin_m=list(p),rotation_wxyz=list(q),
        linear_velocity_m_s=list(velocity),angular_velocity_rad_s=list(angular),
        case_min_right_m=case['lo'].x,receiver_max_right_m=receiver['hi'].x,
        outside_clearance_m=case['lo'].x-receiver['hi'].x,
        passed=case['lo'].x>receiver['hi'].x+.0002,
        method='evaluated case bounds and central differences of evaluated spawn frame')
    flight=[]
    for f in (64,64.5,65,65.5,65.9):
        W.pose(arm,'Fire',f);case=motion.surface(bpy.data.objects['CycleCase_Case'])
        clearance=case['lo'].x-receiver['hi'].x
        flight.append(dict(frame=f,outside_clearance_m=clearance,passed=clearance>.0002))
    row['last_visible_flight']=flight;row['passed'] &= all(r['passed'] for r in flight)
    W.pose(arm,None,0);return row

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--dimensions-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=bpy.data.objects['B24Armature']
    result=dict(dimensions=dimensions(arm))
    if not a.dimensions_only:result['contacts']=contacts(arm)
    Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['dimensions'],indent=2))
    print('BAD CONTACTS',*[r for r in result.get('contacts',[]) if not r['passed']],sep='\n')
