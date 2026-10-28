"""Independent intended state/hold/count assertions at half-frame intervals."""
import math,bpy
from mathutils import Matrix,Vector
from kit import weapon as W
from guns.common.interface_checks import scene_frame
from guns.common.interface_v1_1 import manifest
import interface as I
def delta(arm,name):
 b=arm.pose.bones[name];return b.matrix@b.bone.matrix_local.inverted()
def visible(arm,name):return arm.pose.bones[name].matrix.to_scale().length/math.sqrt(3)
def check(arm):
 manifest(I);rows=[]
 for clip,s in I.CLIPS.items():
  for tick in range(s['frames']*2+1):
   f=tick*.5;W.pose(arm,clip,f);scene_frame(arm,clip,f)
   n=I.STATES[s['start']]['tube'];ch=I.STATES[s['start']]['chamber'];ca=False;ins=False;hidden=False
   if clip.startswith('Fire'):
    ch=int(f<24 or (clip!='FireLast' and f>=44))
    ca=clip!='FireLast' and 30<=f<44
    if clip!='FireLast' and f>=30:n-=1
    if 2<=f<=8:assert abs(delta(arm,'Trigger').to_quaternion().angle-math.radians(12))<5e-5
    if 26<=f<=44:assert abs(delta(arm,'Forend').translation.y+.096)<2e-6,(clip,f,'pump hold')
   elif clip=='ReloadEmpty':
    ch=int(f>=50);ca=36<=f<50
    n=sum(f>=v for v in (144,216,288,360))
    for start in (84,156,228,300):
     if start+12<=f<start+60:ins=True
     if start+44<=f<start+60:hidden=True
    if 26<=f<=50:assert abs(delta(arm,'Bolt').translation.y+.096)<2e-6,(clip,f,'empty hold')
   elif clip.startswith('Reload'):
    n=I.STATES[s['start']]['tube']+int(f>=60);ins=12<=f<60;hidden=44<=f<60
   expected={'ChamberShell':ch,'CarrierShell':ca,'InsertShell':ins,
     **{'Tube'+str(k):k<=n and not hidden for k in range(1,5)}}
   for name,v in expected.items():assert abs(visible(arm,name)-int(v))<2e-5,(clip,f,name,visible(arm,name),v)
   # Riding hand frame follows the complete deformation, not just its position.
   hand=bpy.data.objects['Socket_SupportHand'].matrix_world
   expected_hand=delta(arm,'Forend')@Matrix.Translation(Vector((-.019,.428,-.009)))
   assert max(abs(hand[i][j]-expected_hand[i][j]) for i in range(4) for j in range(4))<2e-6,(clip,f,'hand socket')
  rows.append(dict(clip=clip,samples=s['frames']*2+1))
 # Exact safe interruption boundaries are mechanically closed and hand clear.
 exits=[]
 for clip,s in I.CLIPS.items():
  for phase in s.get('interruptible',[]):
   f=(phase['begin']+phase['end'])/2;token=I.interrupt(clip,f);W.pose(arm,clip,f)
   for b in ('Bolt','Forend'):assert delta(arm,b).translation.length<2e-6
   assert visible(arm,'InsertShell')<1e-5
   assert abs(delta(arm,'Carrier').to_quaternion().angle)<2e-5
   W.pose(arm,token['exit_clip'],0)
   assert I.CLIPS[token['exit_clip']]['start']==phase['state']
   exits.append(dict(clip=clip,frame=f,exit_clip=token['exit_clip'],state=phase['state']))
 for clip,f in [('Reload',28.5),('ReloadEmpty',116.5)]:
  token=I.interrupt(clip,f);assert token['exit_state'] is None
  W.pose(arm,clip,f);before=bpy.data.objects['Socket_Shell'].matrix_world.copy()
  W.pose(arm,'Idle',0);W.pose(arm,token['clip'],token['frame'])
  assert max(abs(before[i][j]-bpy.data.objects['Socket_Shell'].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
 assert I.transition('last_ready','FireLast')=='empty_closed'
 assert I.transition('empty_closed','ReloadEmpty')=='ready'
 W.pose(arm,None,0)
 return dict(passed=True,clips=rows,samples=sum(r['samples'] for r in rows),safe_exits=exits,inflight_resume_checks=2)
