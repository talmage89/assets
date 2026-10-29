"""Intended animation states, independent of matching the source to the import."""
import math
import bpy
from mathutils import Matrix,Vector
from kit import weapon as W
from guns.common.interface_v1_7 import manifest
import interface as I
from parameters import OPEN,LIFT
def check(arm):
 schema=manifest(I);samples=0
 for name,s in I.CLIPS.items():
  for frame in sorted({0,s['frames'],*s['events'].values(),*[i+.5 for i in range(s['frames'])]}):
   W.pose(arm,name,frame);st=I.snapshot(name,frame)
   root=arm.pose.bones['Root'].matrix_basis
   assert max(abs(root[i][j]-Matrix.Identity(4)[i][j]) for i in range(4) for j in range(4))<1e-5
   # Import visibility uses the rigid bone scale, independent of display mesh.
   for i,side in enumerate(('R','L')):
    expected=st['chambers'][i]
    for prefix,which in [('Live','loaded'),('Hull','fired')]:
     visible=min(abs(v) for v in arm.pose.bones[prefix+side].matrix.to_scale())>.001
     assert visible==(expected==which),(name,frame,prefix+side,expected)
   for socket in ('Socket_Shell','Socket_ShellL','Socket_ChamberR','Socket_ChamberL'):
    assert abs(bpy.data.objects[socket].matrix_world.determinant())>.9,(name,frame,socket)
   samples+=1
  # Each clip retains its own complete initial/end control pose.
  for frame,stname in [(0,s['start']),(s['frames'],s['end'])]:
   W.pose(arm,name,frame);st=I.STATES[stname]
   b=arm.pose.bones['Barrels'];deform=b.matrix@b.bone.matrix_local.inverted()
   angle=math.degrees(math.atan2(deform[2][1],deform[1][1]))
   assert abs(angle-(OPEN if st['action']=='open' else 0))<.005,(name,frame,angle)
   def delta(key):
    bb=arm.pose.bones[key];return bb.matrix@bb.bone.matrix_local.inverted()
   assert (delta('Safety').translation-Vector((0,-.005 if st['safety']=='safe' else 0,0))).length<3e-6,(name,frame,'safety detent')
   lever=delta('TopLever');angle=math.degrees(math.atan2(lever[1][0],lever[0][0]))
   assert abs(angle-(25 if st['action']=='open' else 0))<.005,(name,frame,'top lever',angle)
   assert (delta('LockBolt').translation-Vector((0,-.024 if st['action']=='open' else 0,0))).length<3e-6,(name,frame,'bites')
   relative=delta('Barrels').inverted_safe()@delta('Extractor')
   assert (relative.translation-Vector((0,LIFT*.001 if st['action']=='open' else 0,0))).length<3e-6,(name,frame,'extractor')
  token=I.interrupt(name,s['frames']/2);assert token['state']==I.snapshot(name,s['frames']/2)
 # Explicit semantic continuity for the canonical two-shot/manual reload cycle.
 state='ready'
 for clip in ('Fire','FireLeft','Open','Unload','Reload','Close','Safety'):
  state=I.transition(state,clip)
 assert state=='ready'
 for clip,trigger in [('Fire','Trigger'),('FireLeft','TriggerRear')]:
  W.pose(arm,clip,5);bb=arm.pose.bones[trigger];d=bb.matrix@bb.bone.matrix_local.inverted()
  angle=math.degrees(math.atan2(d[2][1],d[1][1]));assert abs(angle+13)<.005,(clip,'pull direction',angle)
 W.pose(arm,'Idle',0);return dict(passed=True,samples=samples,schema=schema)
