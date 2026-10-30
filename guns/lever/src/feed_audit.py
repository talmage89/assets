"""Independent evaluated-triangle contacts, placement and case handoff.

Contact tests establish construction. Source/import comparisons in verify.py
separately establish serialization. No authoring constant is a measurement.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector,Matrix

ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,motion,assembly
import interface


def surf(name):return motion.surface(bpy.data.objects[name])

def center(arm,name,front=False):
    """Center an actual axial end ring, using bind vertices for attribution."""
    ob=bpy.data.objects[name]
    points=[ob.matrix_world@v.co for v in ob.data.vertices]
    axial=bpy.data.objects[name.replace('_FlatNose','_Case')]
    # glTF splits corners at UV/normal seams. Those duplicate points must not
    # weight the axis fit or the ring center toward a particular radial edge.
    cloud=np.unique(np.round([tuple(axial.matrix_world@v.co) for v in axial.data.vertices],8),axis=0)
    eigenvalues,eigenvectors=np.linalg.eigh(np.cov(cloud.T))
    axis=Vector(eigenvectors[:,-1]);axis*=1 if axis.y>0 else -1
    projections=[p.dot(axis) for p in points]
    station=(max if front else min)(projections)
    indices=[i for i,p in enumerate(projections) if abs(p-station)<2e-7]
    posed=surf(name)['points']
    unique={tuple(round(v,9) for v in posed[i]):posed[i] for i in indices}
    return sum(unique.values(),Vector())/len(unique)

def dimensions(arm):
    W.pose(arm,'Idle',0)
    closed=surf('Bolt_Body')['hi'].y
    tube=surf('Tube_Round1_Case');nose=surf('Tube_Round1_FlatNose')
    tube_head=center(arm,'Tube_Round1_Case')
    barrel=surf('Barrel');tray_low=surf('Carrier_Cradle')
    low_z=tray_low['tree'].ray_cast(Vector((0,.150,.030)),Vector((0,0,-1)),.04)[0]
    W.pose(arm,'Cycle',28)
    low_head=center(arm,'Carrier_Live_Case');low_tip=center(arm,'Carrier_Live_FlatNose',True)
    W.pose(arm,'Cycle',36)
    head=center(arm,'Carrier_Live_Case');tip=center(arm,'Carrier_Live_FlatNose',True)
    opened=surf('Bolt_Body')['hi'].y
    minimum=surf('Carrier_Live_Case')['lo'].y
    tray_high=surf('Carrier_Cradle')
    result=dict(cartridge_length_m=nose['hi'].y-tube['lo'].y,
        tube_head_m=list(tube_head),tube_to_breech_axis_separation_m=.0,
        closed_bolt_face_y_m=closed,open_bolt_face_y_m=opened,bolt_draw_m=closed-opened,
        presented_head_m=list(head),presented_tip_m=list(tip),
        low_carrier_head_m=list(low_head),low_carrier_tip_m=list(low_tip),
        carrier_head_rise_m=head.z-low_head.z,carrier_nose_rise_m=tip.z-low_tip.z,
        low_cartridge_pitch_degrees=math.degrees(math.atan2(low_tip.z-low_head.z,low_tip.y-low_head.y)),
        presented_rear_plane_y_m=minimum,open_face_behind_presented_rim_m=minimum-opened,
        bolt_face_to_presented_head_m=closed-minimum,
        cartridge_pitch_degrees=math.degrees(math.atan2(tip.z-head.z,tip.y-head.y)),
        tray_low_bounds_m=dict(lo=list(tray_low['lo']),hi=list(tray_low['hi'])),
        tray_high_bounds_m=dict(lo=list(tray_high['lo']),hi=list(tray_high['hi'])),
        low_tray_inner_floor_m=list(low_z) if low_z is not None else None,
        method='evaluated triangle bounds, end-ring centers and actual tray ray')
    W.pose(arm,'Idle',0)
    chamber=center(arm,'Chamber_Live_Case')
    result['tube_to_breech_axis_separation_m']=chamber.z-tube_head.z
    W.pose(arm,'Fire',3)
    case=surf('Extracted_Case_Case');result['fired_case_length_m']=case['hi'].y-case['lo'].y
    W.pose(arm,None,0)
    return result

def contacts(arm):
    rows=[]
    def pair(clip,f,a,b,limit,kind):
        W.pose(arm,clip,f)
        d,method=assembly.distance(bpy.data.objects[a],bpy.data.objects[b])
        rows.append(dict(clip=clip,frame=f,parts=[a,b],kind=kind,distance_m=d,
                         limit_m=limit,method=method,passed=d<=limit))
    for clip,spec in interface.CLIPS.items():
        feeding=clip in ('Cycle','Chamber','ReloadEmpty') or (clip.startswith('Cycle') and clip not in ('CycleEmpty','CycleLast'))
        if feeding:
            offset=72 if clip=='ReloadEmpty' else 0
            for f in (0,8,12):pair(clip,offset+f,'Carrier_Live_Case','Tube_Stop',.0002,'tube round held at stop')
            for f in (28,30,32,34,36,38):
                pair(clip,offset+f,'Carrier_Live_Case','Carrier_Cradle',.00025,'rim supported by lifting tray')
            for f in (39,40,41,42,43,44,45,46,47,48,49):
                pair(clip,offset+f,'Carrier_Live_Case','Bolt_Body',.0002,'rim driven by bolt face')
                W.pose(arm,clip,offset+f)
                distance=abs(surf('Carrier_Live_Case')['lo'].y-surf('Bolt_Body')['hi'].y)
                rows.append(dict(clip=clip,frame=offset+f,kind='actual rear rim plane on bolt face',
                    distance_m=distance,limit_m=.000025,passed=distance<=.000025))
            for f in (41,42,43,44,45,46,47,48):
                W.pose(arm,clip,offset+f)
                distances=[assembly.distance(bpy.data.objects[n],bpy.data.objects['Barrel'])[0]
                           for n in ('Carrier_Live_Case','Carrier_Live_Jacket','Carrier_Live_FlatNose')]
                distance=min(distances)
                rows.append(dict(clip=clip,frame=offset+f,kind='cartridge guided by chamber mouth',
                    distance_m=distance,limit_m=.00035,passed=distance<=.00035))
            n=1 if clip=='ReloadEmpty' else interface.STATES[spec['start']]['tube']
            if n>1:
                for f in (28,29):pair(clip,offset+f,'Tube_Round1_Case','Tube_Cutoff',.0002,'next rim retained by cutoff')
                for f in (30,36,48):pair(clip,offset+f,'Tube_Round1_Case','Tube_Stop',.0002,'next rim retained by stop')
            # Coincident delivery handoff, measured on both actual mesh rings.
            W.pose(arm,clip,offset+49.999)
            before=center(arm,'Carrier_Live_Case')
            W.pose(arm,clip,offset+50)
            after=center(arm,'Chamber_Live_Case')
            distance=(before-after).length
            rows.append(dict(clip=clip,frame=offset+50,kind='continuous chamber ownership handoff',
                             distance_m=distance,limit_m=.00003,passed=distance<.00003))
        if clip.startswith('Cycle') and clip!='CycleEmpty':
            for f in (6,10,14,18,19,20,21):
                pair(clip,f,'Extracted_Case_Case','Bolt_ExtractorHook',.00025,'extractor retains fired rim')
            pair(clip,19,'Extracted_Case_Case','Bolt_Ejector',.0002,'lower ejector contacts rear rim before tipping')
    def live_heads(clip,f):
        W.pose(arm,clip,f)
        names=[(f'Tube{i}',f'Tube_Round{i}_Case') for i in range(1,7)]+[
            ('CarrierRound','Carrier_Live_Case'),('ChamberRound','Chamber_Live_Case'),('InsertRound','Insert_Live_Case')]
        return [(center(arm,name),center(arm,name.replace('_Case','_FlatNose'),True))
                for bone,name in names if min(abs(v) for v in arm.pose.bones[bone].matrix.to_scale())>.5]
    for clip,spec in interface.CLIPS.items():
        commits=[v for key,v in spec['events'].items() if 'commit' in key or key=='shell_release']
        if clip=='ReloadEmpty':commits.append(100)
        for frame in sorted(set(commits)):
            before=live_heads(clip,frame-.001);after=live_heads(clip,frame)
            metric=lambda p,q:max((p[i]-q[i]).length for i in (0,1))
            distance=max([min(metric(p,q) for q in after) for p in before]+
                         [min(metric(p,q) for q in before) for p in after])
            rows.append(dict(clip=clip,frame=frame,kind='coincident complete live-round head/nose pose set at slot handoff',
                count_before=len(before),count_after=len(after),distance_m=distance,limit_m=.00003,
                passed=len(before)==len(after) and distance<=.00003))
    rows.append(dict(kind='whole fired case outside port at eject',**handoff(arm)))
    W.pose(arm,None,0)
    return rows

def case_frame(arm,f):
    W.pose(arm,'Cycle',f);b=arm.pose.bones['FiredGuide']
    return arm.matrix_world@b.matrix@b.bone.matrix_local.inverted()@Matrix.Translation((0,.200,.048))

def handoff(arm):
    p=case_frame(arm,24);a=case_frame(arm,23.99);b=case_frame(arm,24.01)
    velocity=(b.translation-a.translation)/(.02/60)
    dq=b.to_quaternion()@a.to_quaternion().inverted()
    if dq.w<0:dq.negate()
    angular=dq.axis*(dq.angle/(.02/60))
    W.pose(arm,'Cycle',24)
    case=surf('Extracted_Case_Case');receiver=surf('Receiver')
    clearance=case['lo'].z-receiver['hi'].z
    head=center(arm,'Extracted_Case_Case')
    axis=(center(arm,'Extracted_Case_Case',True)-head).normalized()
    direction=p.to_3x3()@Vector((0,1,0))
    axis_error=math.atan2(axis.cross(direction).length,axis.dot(direction))
    center_error=(head-p.translation).length
    result=dict(event_frame=24,spawn_matrix_asset_frame=[list(r) for r in p],
        origin_m=list(p.translation),rotation_wxyz=list(p.to_quaternion()),
        linear_velocity_m_s=list(velocity),angular_velocity_rad_s=list(angular),
        whole_case_above_receiver_m=clearance,head_frame_error_m=center_error,axis_error_rad=axis_error,
        passed=clearance>.0002 and center_error<.000002 and axis_error<.0001,
        method='actual case/receiver bounds and central differences of evaluated head frame')
    W.pose(arm,None,0)
    return result

def audit(arm):
    result=dict(dimensions=dimensions(arm),contacts=contacts(arm),case_handoff=handoff(arm))
    result['passed']=all(r['passed'] for r in result['contacts']) and result['case_handoff']['passed']
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/lever.blend');p.add_argument('--out',default='build/feed-audit.json');p.add_argument('--dimensions-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    arm=bpy.data.objects['LeverArmature']
    result=dict(dimensions=dimensions(arm),passed=True) if a.dimensions_only else audit(arm)
    Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['dimensions'],indent=2))
    print('BAD CONTACTS',*[r for r in result.get('contacts',[]) if not r['passed']],sep='\n')
    print('HANDOFF',result.get('case_handoff'))
    assert result['passed']
