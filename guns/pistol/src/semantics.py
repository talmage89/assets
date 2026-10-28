"""Intended states and transitions, tested independently of authored key poses."""
import math,bpy
from mathutils import Matrix,Vector
from kit import weapon as W
from interface import CLIPS,transition,interrupt
import interface
from guns.common import interface_checks

def delta(arm,name):
    b=arm.pose.bones[name];return b.matrix@b.bone.matrix_local.inverted()
def scale(arm,name):return arm.pose.bones[name].matrix.to_scale().length/math.sqrt(3)
def check(arm):
    interface_checks.manifest(interface)
    rows=[]
    for clip,spec in CLIPS.items():
        for tick in range(spec['frames']*2+1):
            f=tick*.5;W.pose(arm,clip,f)
            interface_checks.scene_frame(arm,clip,f)
            chamber=not (clip in ('IdleOpen','IdleEmpty','Charge') or (clip=='FireLast' and f>=2)
                or (clip in ('Fire','FireSemi') and 2<=f<8) or (clip=='ReloadEmpty' and f<118))
            top=not (clip in ('FireLast','IdleOpen','IdleEmpty','Charge') or (clip=='ReloadEmpty' and f<47))
            assert abs(scale(arm,'ChamberRound')-int(chamber))<2e-6,(clip,f,'chamber')
            assert abs(scale(arm,'TopRound')-int(top))<2e-6,(clip,f,'top round')
            if clip=='ReloadEmpty' and f<=110:
                assert abs(delta(arm,'Slide').translation.y+.034)<2e-6,(clip,f,'slide hold')
                assert abs(delta(arm,'SlideStop').to_quaternion().angle-math.radians(7))<2e-5
            if clip in ('Fire','FireSemi','FireLast') and 2<=f<=10:
                assert abs(delta(arm,'Trigger').to_quaternion().angle-math.radians(10))<2e-5,(clip,f,'trigger hold')
        rows.append(dict(clip=clip,intermediate_samples=spec['frames']*2+1))
    paths=[('Fire','Idle'),('FireLast','ReloadEmpty'),('ReloadEmpty','Idle'),
           ('Reload','Idle'),('Inspect','Idle'),('IdleEmpty','Charge'),('Charge','IdleOpen')]
    for left,right in paths:
        W.pose(arm,left,CLIPS[left]['frames']);end={b.name:delta(arm,b.name).copy() for b in arm.pose.bones}
        W.pose(arm,right,0)
        assert max(abs(end[b.name][i][j]-delta(arm,b.name)[i][j]) for b in arm.pose.bones for i in range(4) for j in range(4))<2e-6,(left,right)
        assert transition(CLIPS[left]['start'],left)==CLIPS[right]['start']
    assert transition(transition('last_ready','FireLast'),'ReloadEmpty')=='ready'
    assert transition(transition('ready','Fire'),'Reload')=='ready'
    for clip in ('Reload','ReloadEmpty'):
        for f in (28,40,73,90):
            token=interrupt(clip,f);W.pose(arm,clip,f)
            before=bpy.data.objects['Socket_Magazine'].matrix_world.copy()
            W.pose(arm,None,0);W.pose(arm,token['clip'],token['frame'])
            after=bpy.data.objects['Socket_Magazine'].matrix_world
            assert max(abs(before[i][j]-after[i][j]) for i in range(4) for j in range(4))<1e-7
    # Ejection reference is inside the moving port's Y interval at the event;
    # shot muzzle reference agrees with the in-battery crown.
    for clip in ('Fire','FireLast'):
        W.pose(arm,clip,CLIPS[clip]['events']['eject'])
        e=bpy.data.objects['Socket_Ejection'].matrix_world.translation
        slide=delta(arm,'Slide');local=slide.inverted()@e
        assert .033<=local.y<=.068 and .0485<=local.z<=.069,(clip,local)
        W.pose(arm,clip,CLIPS[clip]['events']['shot'])
        crown=delta(arm,'Barrel')@Vector((0,.137,.0535))
        assert (crown-bpy.data.objects['Socket_Muzzle'].matrix_world.translation).length<2e-6
    W.pose(arm,None,0)
    return dict(passed=True,clips=rows,transitions=[list(p) for p in paths],interrupted_reload_resumes=8,
                event_socket_checks=['shot crown','eject moving port'],whole_weapon_motion='external only')
