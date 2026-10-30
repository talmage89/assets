"""Independent source/imported surface placement, contacts and case handoff."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,motion,assembly
from kit.gltf import GLB
import interface
from feed import PIVOT_BEGIN

def part(name):return next(o for o in bpy.context.scene.objects if o.type=='MESH' and (o.name==name or o.get('part_name')==name))
def surf(name):return motion.surface(part(name))
def center(name,front=False):
    ob=part(name);points=[ob.matrix_world@v.co for v in ob.data.vertices]
    station=(max if front else min)(p.y for p in points)
    indices=[i for i,p in enumerate(points) if abs(p.y-station)<2e-7]
    posed=surf(name)['points']
    unique={tuple(round(v,9) for v in posed[i]):posed[i] for i in indices}
    return sum(unique.values(),Vector())/len(unique)

def dimensions(arm):
    W.pose(arm,'Idle',0)
    closed=surf('Bolt_Face')['hi'].y;first=center('TubeShell1_Head');second=center('TubeShell2_Head')
    nose=center('TubeShell1_Hull',True);low_tray=surf('Carrier_Tray')
    floor=low_tray['tree'].ray_cast(Vector((.004,.1597,.010)),Vector((0,0,-1)),.025)[0]
    barrel=surf('Barrel');radii=[]
    for y in (.300,.305,.310,.315):
        hit=barrel['tree'].ray_cast(Vector((0,y,.049)),Vector((-1,0,0)),.020)[0]
        assert hit is not None
        radii.append(dict(y_m=y,inside_radius_m=abs(hit.x)))
    W.pose(arm,'Fire',26);opened=surf('Bolt_Face')['hi'].y
    W.pose(arm,'Fire',30);low_head=center('CarrierShell_Head');low_nose=center('CarrierShell_Hull',True)
    W.pose(arm,'Fire',40);head=center('CarrierShell_Head');tip=center('CarrierShell_Hull',True)
    rear=surf('CarrierShell_Head')['lo'].y
    result=dict(closed_bolt_face_y_m=closed,open_bolt_face_y_m=opened,bolt_draw_m=closed-opened,
        loaded_shell_length_m=nose.y-first.y,tube_pitch_m=second.y-first.y,
        adjacent_tube_round_gap_m=second.y-nose.y,tube_head_m=list(first),
        low_carrier_head_m=list(low_head),low_carrier_tip_m=list(low_nose),
        tube_to_low_carrier_axis_m=low_head.z-first.z,
        presented_head_m=list(head),presented_tip_m=list(tip),
        carrier_head_rise_m=head.z-low_head.z,carrier_nose_rise_m=tip.z-low_nose.z,
        presented_pitch_degrees=math.degrees(math.atan2(tip.z-head.z,tip.y-head.y)),
        presented_rear_plane_y_m=rear,open_face_behind_presented_rim_m=rear-opened,
        bolt_face_to_presented_rim_m=closed-rear,
        low_tray_bounds_m=dict(lo=list(low_tray['lo']),hi=list(low_tray['hi'])),
        low_tray_support_m=list(floor),chamber_radius_samples=radii,
        method='evaluated triangle bounds, actual end-ring centers and inner-wall rays')
    # The standalone exterior is identical before/after the feed correction.
    standalone=Path(__file__).resolve().parents[1]/'build/hull.glb'
    raw=GLB(standalone)
    points=[Vector(p) for m in raw.json['meshes'] for prim in m['primitives'] for p in raw.accessor(prim['attributes']['POSITION'])]
    result['fired_hull_length_m']=max(p.z for p in points)-min(p.z for p in points)
    W.pose(arm,None,0);return result

def contacts(arm):
    rows=[]
    def pair(clip,f,a,b,limit,kind):
        W.pose(arm,clip,f);distance,method=assembly.distance(part(a),part(b))
        rows.append(dict(clip=clip,frame=f,kind=kind,parts=[a,b],distance_m=distance,
                         method=method,limit_m=limit,passed=distance<=limit))
    for clip,spec in interface.CLIPS.items():
        if clip.startswith('Fire'):
            for f in (10,14,20,PIVOT_BEGIN,22,22.5,23):
                pair(clip,f,'FiredHull_Head','Extractor_Claw',.00025,'extractor retains fired rim')
            pair(clip,PIVOT_BEGIN,'FiredHull_Head','Ejector_Shoulder',.00025,'rim reaches receiver ejector')
        feeding=(clip.startswith('Fire') and clip!='FireLast') or clip=='ReloadEmpty'
        if feeding:
            empty=clip=='ReloadEmpty';begin,end=(46,50) if empty else (40,44)
            if not empty:
                for f in (0,12,24):pair(clip,f,'CarrierShell_Head','ShellStop_Tip_ShellStopL',.0002,'first shell held by left latch')
            for f in ((36,38,40,42,44,46) if empty else (30,32,35,38,40)):
                pair(clip,f,'CarrierShell_Head','Carrier_Tray',.00035,'tray supports lifting shell rim')
            for i in range(16):
                f=begin+(end-begin)*i/16
                pair(clip,f,'CarrierShell_Head','Bolt_Face',.0002,'bolt face drives shell head')
                W.pose(arm,clip,f);distance=abs(surf('CarrierShell_Head')['lo'].y-surf('Bolt_Face')['hi'].y)
                rows.append(dict(clip=clip,frame=f,kind='actual rear head plane on bolt face',distance_m=distance,
                                 limit_m=.00003,passed=distance<=.00003))
            W.pose(arm,clip,end-.001);before=center('CarrierShell_Head')
            W.pose(arm,clip,end);after=center('ChamberShell_Head');distance=(before-after).length
            rows.append(dict(clip=clip,frame=end,kind='coincident seated shell ownership handoff',distance_m=distance,
                             limit_m=.00004,passed=distance<=.00004))
            if not empty:
                n=interface.STATES[spec['start']]['tube']
                name='TubeShell1_Head' if n>1 else 'Magazine_Follower'
                for f in (30,32,36,40):pair(clip,f,name,'ShellStop_Tip_ShellStopR',.0002,'right interceptor holds following head')
                for f in (44,50,60):pair(clip,f,name,'ShellStop_Tip_ShellStopL',.0002,'left latch retains returned head')
        if clip=='Inspect':
            for f in (100,106,116):pair(clip,f,'ChamberShell_Head','Extractor_Claw',.00025,'partial rack retains live rim')
    def live_heads(clip,f):
        W.pose(arm,clip,f)
        names=[(f'Tube{i}',f'TubeShell{i}_Head') for i in range(1,5)]+[
            ('CarrierShell','CarrierShell_Head'),('InsertShell','InsertShell_Head'),('ChamberShell','ChamberShell_Head')]
        return [(center(name),center(name.replace('_Head','_Hull'),True))
                for bone,name in names if min(abs(v) for v in arm.pose.bones[bone].matrix.to_scale())>.5]
    for clip,spec in interface.CLIPS.items():
        commits=[v for key,v in spec['events'].items() if 'commit' in key or key=='shell_release']
        for f in sorted(set(commits)):
            before=live_heads(clip,f-.001);after=live_heads(clip,f)
            metric=lambda p,q:max((p[i]-q[i]).length for i in (0,1))
            distance=max([min(metric(p,q) for q in after) for p in before]+[min(metric(p,q) for q in before) for p in after])
            rows.append(dict(clip=clip,frame=f,kind='continuous complete live-shell head/nose pose set at indexing',
                count_before=len(before),count_after=len(after),distance_m=distance,limit_m=.00004,
                passed=len(before)==len(after) and distance<=.00004))
    rows.append(dict(kind='whole fired hull outside port at eject',**handoff(arm)))
    W.pose(arm,None,0)
    return rows

def case_frame(arm,f):
    W.pose(arm,'Fire',f);bone=arm.pose.bones['FiredGuide']
    return arm.matrix_world@bone.matrix@bone.bone.matrix_local.inverted()@Matrix.Translation((0,.2411,.049))

def handoff(arm):
    frame=case_frame(arm,24);a=case_frame(arm,23.99);b=case_frame(arm,24.01)
    velocity=(b.translation-a.translation)/(.02/60)
    dq=b.to_quaternion()@a.to_quaternion().inverted()
    if dq.w<0:dq.negate()
    angular=dq.axis*(dq.angle/(.02/60))
    W.pose(arm,'Fire',24)
    minimum=min(surf(n)['lo'].x for n in ('FiredHull_Head','FiredHull_Primer','FiredHull_Hull'))
    receiver=surf('Receiver');clearance=minimum-receiver['hi'].x
    center_error=(center('FiredHull_Head')-frame.translation).length
    axis=(center('FiredHull_Hull',True)-center('FiredHull_Head')).normalized()
    direction=frame.to_3x3()@Vector((0,1,0))
    axis_error=math.atan2(axis.cross(direction).length,axis.dot(direction))
    result=dict(event_frame=24,spawn_matrix_asset_frame=[list(r) for r in frame],
        origin_m=list(frame.translation),rotation_wxyz=list(frame.to_quaternion()),
        linear_velocity_m_s=list(velocity),angular_velocity_rad_s=list(angular),
        whole_hull_right_clearance_m=clearance,head_frame_error_m=center_error,axis_error_rad=axis_error,
        passed=clearance>.0002 and center_error<.000002 and axis_error<.0001,
        method='all actual hull surfaces against receiver bounds; end ring and evaluated frame central differences')
    W.pose(arm,None,0);return result

def audit(arm):
    result=dict(dimensions=dimensions(arm),contacts=contacts(arm),case_handoff=handoff(arm))
    result['passed']=all(r['passed'] for r in result['contacts']) and result['case_handoff']['passed']
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/shotgun.blend');p.add_argument('--out',default='build/feed-audit.json');p.add_argument('--dimensions-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=bpy.data.objects['ShotgunArmature']
    result=dict(dimensions=dimensions(arm),passed=True) if a.dimensions_only else audit(arm)
    Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['dimensions'],indent=2))
    print('BAD CONTACTS',*[r for r in result.get('contacts',[]) if not r['passed']],sep='\n')
    print('HANDOFF',result.get('case_handoff'));assert result['passed']
