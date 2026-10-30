"""Intended intermediate states, independent of source/import agreement."""
import math,bpy
from kit import weapon as W
from interface import CLIPS,transition,interrupt
import interface
from guns.common import interface_checks
def delta(arm,name):
 b=arm.pose.bones[name];return b.matrix@b.bone.matrix_local.inverted()
def scale(arm,name):return arm.pose.bones[name].matrix.to_scale().length/math.sqrt(3)
def check(arm):
 interface_checks.manifest(interface);rows=[]
 for clip,spec in CLIPS.items():
  for tick in range(spec['frames']*2+1):
   f=tick*.5;W.pose(arm,clip,f);interface_checks.scene_frame(arm,clip,f)
   ch=not (clip=='IdleEmpty' or (clip=='Fire' and 3<=f<104) or
               (clip=='FireLast' and f>=3) or (clip=='ReloadEmpty' and f<219))
   top=not (clip in ('IdleEmpty','FireLast') or (clip=='ReloadEmpty' and f<116))
   for name,state in [('CycleCase',clip in ('Fire','FireLast') and 3<=f<66),('ChamberRound',ch),('TopRound',top and not ((clip=='Fire' and 104<=f<122) or (clip=='ReloadEmpty' and 219<=f<242))),('ReserveRound',top)]:
    assert abs(scale(arm,name)-int(state))<3e-6,(clip,f,name)
   if clip=='Reload':assert abs(delta(arm,'BoltTravel').translation.y)<3e-6,(clip,f,'chambered reload opens bolt')
   if clip=='ReloadEmpty' and 48<=f<=195:
    assert abs(delta(arm,'BoltTravel').translation.y+.104)<3e-6,(clip,f,'bolt hold')
   if clip in ('Fire','FireLast'):
    if 42<=f<=108:assert abs(delta(arm,'Bolt').to_quaternion().angle-math.pi/2)<3e-5,(clip,f,'lift hold')
    if 64<=f<=76:assert abs(delta(arm,'BoltTravel').translation.y+.104)<3e-6,(clip,f,'draw hold')
  rows.append(dict(clip=clip,samples=spec['frames']*2+1))
 paths=[('Fire','Idle'),('FireLast','ReloadEmpty'),('ReloadEmpty','Idle'),('Reload','Idle'),
        ('Inspect','Idle'),('BipodDeploy','BipodFold'),('BipodFold','Idle')]
 for left,right in paths:
  W.pose(arm,left,CLIPS[left]['frames']);before={b.name:delta(arm,b.name).copy() for b in arm.pose.bones}
  W.pose(arm,right,0)
  assert max(abs(before[b.name][i][j]-delta(arm,b.name)[i][j]) for b in arm.pose.bones for i in range(4) for j in range(4))<3e-6,(left,right)
  assert transition(CLIPS[left]['start'],left)==CLIPS[right]['start']
 for clip in ('Reload','ReloadEmpty'):
  for f in (42,88,116,140):
   W.pose(arm,clip,f);before=bpy.data.objects['Socket_Magazine'].matrix_world.copy();token=interrupt(clip,f)
   W.pose(arm,None,0);W.pose(arm,token['clip'],token['frame'])
   assert max(abs(before[i][j]-bpy.data.objects['Socket_Magazine'].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
 W.pose(arm,None,0)
 return dict(passed=True,clips=rows,transitions=paths,reload_resumes=8)
