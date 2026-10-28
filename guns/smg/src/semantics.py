"""Independent intended-state checks, including every half-frame after import."""
import math,bpy
from mathutils import Matrix,Vector
from kit import weapon as W
from guns.common.interface_checks import scene_frame
from guns.common.interface_v1_3 import manifest
import interface as I

def delta(arm,n):
 b=arm.pose.bones[n];return b.matrix@b.bone.matrix_local.inverted()
def scale(arm,n):return arm.pose.bones[n].matrix.to_scale().length/math.sqrt(3)
def check(arm):
 manifest(I);rows=[]
 for clip,s in I.CLIPS.items():
  for tick in range(s['frames']*2+1):
   f=tick*.5;W.pose(arm,clip,f);scene_frame(arm,clip,f)
   chamber=bool(I.STATES[s['start']]['chamber']);loaded=I.STATES[s['start']]['magazine']=='loaded'
   if clip in ('Fire','FireSemi'):chamber=not 2<=f<7
   if clip=='FireAuto':chamber=f>=5
   if clip=='FireLast':chamber=f<2
   if clip=='ReloadEmpty':chamber=f>=181;loaded=f>=100
   for name,want in {'ChamberRound':chamber,**{n:loaded for n in ('TopRound','SecondRound','ThirdRound')}}.items():
    assert abs(scale(arm,name)-int(want))<2e-5,(clip,f,name,scale(arm,name),want)
   if clip.startswith('Fire'):
    assert delta(arm,'ChargingHandle').translation.length<2e-6,(clip,f,'nonreciprocating handle')
    assert delta(arm,'ChargingHandle').to_quaternion().angle<2e-5
    if clip!='FireAuto' and 2<=f<=9:assert abs(delta(arm,'Trigger').to_quaternion().angle-math.radians(12))<5e-5
   if clip=='ReloadEmpty' and 42<=f<=169:
    assert abs(delta(arm,'Bolt').translation.y+.084)<2e-6,(clip,f,'bolt hold')
    assert abs(delta(arm,'ChargingHandle').translation.y+.084)<2e-6
    assert abs(delta(arm,'ChargingHandle').to_quaternion().angle-math.radians(35))<5e-5
   if clip=='Charge' and f>=42:
    assert abs(delta(arm,'Bolt').translation.y+.084)<2e-6
    assert abs(delta(arm,'ChargingHandle').to_quaternion().angle-math.radians(35))<5e-5
   if clip=='Reload':
    assert delta(arm,'Bolt').translation.length<2e-6 and chamber
   # Nonscaling riding frames retain orientation while ammunition changes scale.
   for sock,bone,point in [('Socket_Magazine','Magazine',(0,.143,.080)),
                         ('Socket_ChargingHandle','ChargingHandle',(-.025,.301,.122))]:
    xf=delta(arm,bone)@Matrix.Translation(Vector(point));actual=bpy.data.objects[sock].matrix_world
    assert max(abs(xf[i][j]-actual[i][j]) for i in range(4) for j in range(4))<2e-6,(clip,f,sock)
  rows.append(dict(clip=clip,samples=s['frames']*2+1))
 paths=[('Fire','Idle'),('FireSemi','Reload'),('FireLast','ReloadEmpty'),('ReloadEmpty','Idle'),
  ('Reload','Idle'),('Inspect','Idle'),('IdleEmpty','Charge'),('Charge','IdleOpen'),
  ('SelectorSafe','IdleSafe'),('SelectorSemi','Idle'),('SelectorAuto','IdleAutoReady'),
  ('SelectorAutoSemi','Idle'),('AutoStart','FireAuto'),('FireAuto','IdleAuto'),('AutoStop','IdleAutoReady')]
 for a,b in paths:
  W.pose(arm,a,I.CLIPS[a]['frames']);before={n:delta(arm,n).copy() for n in arm.pose.bones.keys()}
  W.pose(arm,b,0)
  # The auto shot event at frame zero hides the chamber representation discretely.
  for n in before:
   if b=='FireAuto' and n=='ChamberRound':continue
   assert max(abs(before[n][i][j]-delta(arm,n)[i][j]) for i in range(4) for j in range(4))<3e-6,(a,b,n)
  assert I.transition(I.CLIPS[a]['start'],a)==I.CLIPS[b]['start']
 resumes=[]
 for clip,frames in [('Reload',(34.5,55.5,84.5,102)),('ReloadEmpty',(41.5,78.5,99.5,147.5,173.5))]:
  for f in frames:
   token=I.interrupt(clip,f);W.pose(arm,clip,f);before={n:delta(arm,n).copy() for n in arm.pose.bones.keys()}
   W.pose(arm,'Idle',0);W.pose(arm,token['clip'],token['frame'])
   assert max(abs(before[n][i][j]-delta(arm,n)[i][j]) for n in before for i in range(4) for j in range(4))<1e-7
   resumes.append(dict(clip=clip,frame=f))
 W.pose(arm,None,0)
 return dict(passed=True,clips=rows,samples=sum(r['samples'] for r in rows),transitions=paths,resumes=resumes)
