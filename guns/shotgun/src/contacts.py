"""Required visible contacts, measured on evaluated source OR imported meshes."""
import math,bpy
from mathutils import Vector
from kit import weapon as W, motion, assembly
def part(name):
 return next(o for o in bpy.context.scene.objects if o.type=='MESH' and (o.get('part_name')==name or o.name==name))
def measure(arm):
 rows=[]
 def contact(a,b,limit,kind,clip,frame):
  W.pose(arm,clip,frame);d,method=assembly.distance(part(a),part(b))
  rows.append(dict(kind=kind,parts=[a,b],clip=clip,frame=frame,distance_m=d,limit_m=limit,method=method,passed=d<=limit))
 for f in (30,35.5,38,40):contact('CarrierShell_Head','Carrier_Tray',.0004,'carrier supports rim','Fire',f)
 for f in (30,40):
  W.pose(arm,'Fire',f);b=arm.pose.bones['Carrier'];xf=b.matrix@b.bone.matrix_local.inverted()
  up=xf.to_3x3()@Vector((0,0,1));origin=xf@Vector((.004,.1597,.010))
  tray=motion.surface(part('Carrier_Tray'));rim=motion.surface(part('CarrierShell_Head'))
  hit=tray['tree'].ray_cast(origin,-up,.012)
  assert hit[0] is not None and hit[1].dot(up)>.8,(f,hit)
  distance=rim['tree'].find_nearest(hit[0])[3];assert distance<.0004,(f,distance)
  rows.append(dict(kind='upward cradle face under rim',clip='Fire',frame=f,point=list(hit[0]),
   normal=list(hit[1]),rim_distance_m=distance,passed=True))
 for f in (44,60):
  contact('ShellStop_Tip_ShellStopL','TubeShell1_Head',.00018,'retained tube rim','Fire',f)
 for clip,f in [('Idle',0),('Fire',60),('FireLast',66),('ReloadEmpty',78)]:
  contact('Bolt_Lock','Barrel_LockSeat',.00018,'battery engagement',clip,f)
 for clip,f in [('Idle',0),('Fire',18),('Fire',26),('Fire',50),('ReloadEmpty',26),('Inspect',106)]:
  W.pose(arm,clip,f);b=arm.pose.bones['Forend'];xf=b.matrix@b.bone.matrix_local.inverted()
  block=motion.surface(part('Action_SlideBlock'));bolt=motion.surface(part('Bolt_Body'));samples=[]
  for x in (-.003,0,.003):
   origin=xf@Vector((x,.219,.037));up=xf.to_3x3()@Vector((0,0,1))
   a=block['tree'].ray_cast(origin,up,.006);c=bolt['tree'].ray_cast(origin,up,.006)
   assert a[0] is not None and c[0] is not None and a[1].dot(up)>.9 and c[1].dot(up)<-.9,(clip,f,a,c)
   d=(a[0]-c[0]).length;assert d<.00018,(clip,f,d)
   samples.append(dict(block_point=list(a[0]),bolt_point=list(c[0]),gap_m=d))
  rows.append(dict(kind='action slide block / bolt opposing bearing faces',clip=clip,frame=f,
   method='three opposing bearing-face rays; avoids vertex-only minimum bounds',samples=samples,passed=True))
 W.pose(arm,'Idle',0)
 # Independent facing-plane rays on actual triangles, rather than an unrelated
 # nearest corner, prove that the lock's upper face reaches the seat underside.
 seat=motion.surface(part('Barrel_LockSeat'));lock=motion.surface(part('Bolt_Lock'));samples=[]
 for x,y in [(0,.223),(.003,.221),(-.003,.225)]:
  hit=seat['tree'].ray_cast(Vector((x,y,.060)),Vector((0,0,1)),.006)
  samples.append(None if hit[0] is None else dict(point=list(hit[0]),normal=list(hit[1]),lock_distance_m=lock['tree'].find_nearest(hit[0])[3]))
 assert all(s and s['normal'][2]<-.8 and s['lock_distance_m']<.00018 for s in samples),samples
 rows.append(dict(kind='opposing battery faces',samples=samples,passed=True))
 # The latches alternate; the right interceptor is retracted in battery.
 rim=motion.surface(part('TubeShell1_Head'))
 for side in (-1,):
  tip=motion.surface(part('ShellStop_Tip_ShellStop'+('L' if side<0 else 'R')))
  hit=rim['tree'].ray_cast(Vector((side*.010,.253,.013)),Vector((0,1,0)),.005)
  assert hit[0] is not None and hit[1].y<-.8,hit
  d=tip['tree'].find_nearest(hit[0])[3];assert d<.00018,d
  rows.append(dict(kind='opposing latch and rim face',point=list(hit[0]),normal=list(hit[1]),tip_distance_m=d,passed=True))
 for clip,f in [('Idle',0),('Fire',15.5),('Fire',26),('Fire',51.5),('ReloadEmpty',26)]:
  W.pose(arm,clip,f)
  for n in ('Forend_Bearing','Forend_Bearing.001'):
   d,method=assembly.distance(part(n),part('Magazine_Tube'))
   assert .00001<d<.0002,(clip,f,n,d)
   rows.append(dict(kind='forend bearing on tube',clip=clip,frame=f,part=n,gap_m=d,method=method,passed=True))
 # The optical ray must reach the brass bead before any roof or stock surface.
 W.pose(arm,'Idle',0);socket=bpy.data.objects['Socket_Eye'];eye=socket.matrix_world.translation;hits=[]
 forward=(socket.matrix_world.to_3x3()@Vector((0,1,0))).normalized()
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or 'bone' not in o or o.get('bake_only'):continue
  if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())<.001:continue
  h=motion.surface(o)['tree'].ray_cast(eye,forward,1.1)
  if h[0] is not None:hits.append((h[3],o.get('part_name',o.name)))
 assert hits and min(hits)[1]=='Bead',sorted(hits)[:5]
 rows.append(dict(kind='actual Eye ray first reaches bead',hit=min(hits)[1],distance_m=min(hits)[0],passed=True))
 from feed_audit import contacts as feed_contacts
 rows.extend(feed_contacts(arm))
 W.pose(arm,None,0)
 assert all(r['passed'] for r in rows),rows
 return rows
