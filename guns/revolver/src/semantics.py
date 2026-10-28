"""Independent intended visual states and subframe tests, source and import."""
import math
import bpy
from mathutils import Matrix
from kit import weapon as W
from guns.common import interface_v1_4,interface_checks
import interface as I
def delta(arm,name):
 b=arm.pose.bones[name];return b.matrix@b.bone.matrix_local.inverted()
def visible(arm,name):return arm.pose.bones[name].matrix.to_scale().length/math.sqrt(3)
def check(arm):
 schema=interface_v1_4.manifest(I);samples=0
 for clip,s in I.CLIPS.items():
  for tick in range(s['frames']*2+1):
   f=tick/2;W.pose(arm,clip,f);interface_checks.scene_frame(arm,clip,f)
   state=I.snapshot(clip,f)
   for i,occupancy in enumerate(state['chambers']):
    # Ejected cases remain visible in free travel after leaving the chamber.
    expected_case=occupancy=='fired' or clip=='Reload' and 60<=f<80
    assert abs(visible(arm,'Live'+str(i))-int(occupancy=='loaded'))<2e-5,(clip,f,i,'live')
    assert abs(visible(arm,'Case'+str(i))-int(expected_case))<2e-5,(clip,f,i,'case')
   for n in ('InsertRound','LoaderBody','LoaderRelease',*('LoaderRound'+str(i) for i in range(6))):
    scale=visible(arm,n);assert min(abs(scale),abs(scale-1))<2e-5,(clip,f,n,scale)
   for name in ('Socket_Cylinder','Socket_Speedloader','Socket_Round'):
    determinant=bpy.data.objects[name].matrix_world.to_3x3().determinant()
    assert abs(determinant-1)<.0001,(clip,f,name,'singular attachment frame',determinant)
   if clip=='Reload' and 40<=f<=180:
    target=Matrix.Rotation(math.radians(-80),3,'Y');actual=delta(arm,'Crane').to_3x3()
    assert max(abs(actual[i][j]-target[i][j]) for i in range(3) for j in range(3))<.001,(clip,f,'open hold')
   if clip=='Reload' and 88<=f<=180:
    assert delta(arm,'Extractor').translation.y<.002,'Star must be returned before inserting'
   samples+=1
  W.pose(arm,clip,s['frames'])
  end=I.STATES[s['end']]
  angle=arm.pose.bones['Cylinder'].rotation_euler.y
  # Imported glTF uses quaternions and may normalize a complete 360° turn.
  xf=delta(arm,'Cylinder').to_3x3()
  expected=Matrix.Rotation(math.radians(end['index']*60),3,'Y')
  assert max(abs(xf[i][j]-expected[i][j]) for i in range(3) for j in range(3))<.001,(clip,'index')
 # Exact intended motion samples, independently interpolated from meaning.
 for clip,frame,index in [('Fire',13,30),('Fire',21,60),('FireLast',21,360),('CockHammer',29,60)]:
  W.pose(arm,clip,frame)
  xf=delta(arm,'Cylinder').to_3x3();target=Matrix.Rotation(math.radians(index),3,'Y')
  assert max(abs(xf[i][j]-target[i][j]) for i in range(3) for j in range(3))<.001,(clip,frame,'index interpolation')
 for clip,frame,bone,angle in [('CockHammer',42,'Trigger',-10),('IdleCocked',0,'Trigger',-10),
  ('FireSingle',3,'Trigger',-15),('Fire',5,'CylinderStop',-22),('Fire',24,'CylinderStop',0),
  ('Reload',40,'CylinderStop',-22)]:
  W.pose(arm,clip,frame);actual=delta(arm,bone).to_3x3();target=Matrix.Rotation(math.radians(angle),3,'X')
  assert max(abs(actual[i][j]-target[i][j]) for i in range(3) for j in range(3))<.001,(clip,frame,bone,'intended rocker / SA pose')
 for f in (40,59.5,105.5,143.5,170):
  token=I.interrupt('Reload',f);W.pose(arm,'Reload',f)
  before=bpy.data.objects['Socket_Cylinder'].matrix_world.copy()
  W.pose(arm,'Idle',0);W.pose(arm,token['clip'],token['frame'])
  after=bpy.data.objects['Socket_Cylinder'].matrix_world
  assert max(abs(before[i][j]-after[i][j]) for i in range(4) for j in range(4))<1e-6
 # Consumers can enter the corresponding endpoint hold without a visible
 # control or cylinder jump; hidden demonstration case-flight keys are not
 # physical attachment references and may reset while invisible.
 controls=('Cylinder','Crane','Trigger','Hammer','CylinderStop','Latch','LatchPin')
 for clip,s in I.CLIPS.items():
  W.pose(arm,clip,s['frames']);end={n:delta(arm,n).copy() for n in controls}
  hold_name=next(n for n,q in I.CLIPS.items() if n.startswith('Idle') and q['start']==s['end'])
  W.pose(arm,hold_name,0)
  assert max(abs(end[n][i][j]-delta(arm,n)[i][j]) for n in controls for i in range(4) for j in range(4))<.00002,(clip,hold_name,'visible control continuity')
 W.pose(arm,None,0)
 return dict(passed=True,schema=schema,half_frame_samples=samples,interrupted_resumes=5,visible_control_transitions=len(I.CLIPS))
