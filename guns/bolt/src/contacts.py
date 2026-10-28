"""Required visual engagements measured on evaluated surfaces."""
import bpy
from mathutils import Vector
from kit import weapon as W,assembly,motion
def measure(arm):
 rows=[]
 def contact(a,b,limit,label):
  d,method=assembly.distance(bpy.data.objects[a],bpy.data.objects[b])
  rows.append(dict(kind=label,parts=[a,b],distance_m=d,limit_m=limit,method=method,passed=d<=limit))
 W.pose(arm,'Idle',0)
 for name in ('Bolt_Lug','Bolt_Lug.001'):
  contact(name,'Receiver',.00022,'locked lug seat')
  # Ray from the actual rear lug plane toward its opposing receiver abutment.
  s=motion.surface(bpy.data.objects[name]);p=(s['lo']+s['hi'])/2;p.y=.198
  r=motion.surface(bpy.data.objects['Receiver'])['tree'].ray_cast(p+Vector((0,.0001,0)),Vector((0,-1,0)),.001)
  rows.append(dict(kind='opposing lug/seat faces',part=name,hit_m=list(r[0]) if r[0] else None,
       normal=list(r[1]) if r[1] else None,passed=r[0] is not None and r[1].y>.7))
 for lip in ('Magazine_FeedLip','Magazine_FeedLip.001'):
  contact(lip,'Magazine_TopRound_Case',.00016,'case retained by lip curl')
  contact(lip,'Magazine_Shell',.00016,'lip attached to magazine shell')
 contact('Magazine_Follower','Magazine_ReserveRound_Case',.00016,'follower supports ammunition')
 contact('Magazine_CatchShoulder','Magazine_Catch',.00016,'seated catch shoulder')
 contact('Bipod_StudPin','Sling_Stud.001',.00016,'bipod captures stud eye')
 contact('Bipod_Saddle','Stock_Mold',.0006,'bipod bears on forend')
 for part in ('Ring_Lower','Ring_Upper','Ring_Lower.001','Ring_Upper.001'):
  contact(part,'Scope_Body',.00016,'30 mm tube seated in steel ring')
 for part in ('Ring_Foot','Ring_Foot.001'):
  contact(part,'Scope_Base',.00016,'ring foot supported on extended one-piece base')
 contact('Scope_Base','Receiver',.00016,'one-piece base supported on receiver bridges')
 contact('Stock_Mold','Receiver',.00022,'receiver bedding')
 contact('Safety_Stem','Safety_PivotPin',.00015,'safety on pivot pin')
 for clip,frame in [('Idle',0),('BipodDeploy',78)]:
  W.pose(arm,clip,frame)
  for suffix in ('','.001'):
   contact('Bipod_ReturnSpring'+suffix,'Bipod_SpringTail'+suffix,.001,'return spring connected at '+clip)
 W.pose(arm,'Idle',0)
 # A retained cartridge is wider than the aperture and contained in length.
 a=motion.surface(bpy.data.objects['Magazine_FeedLip']);b=motion.surface(bpy.data.objects['Magazine_FeedLip.001'])
 gap=min(abs(p.x) for p in a['points'])+min(abs(p.x) for p in b['points'])
 case=motion.surface(bpy.data.objects['Magazine_TopRound_Case']);diam=case['hi'].x-case['lo'].x
 rows.append(dict(kind='retaining aperture',gap_m=gap,case_diameter_m=diam,passed=gap<diam-.001))
 W.pose(arm,'Reload',62)
 d,method=assembly.distance(bpy.data.objects['Magazine_CatchShoulder'],bpy.data.objects['Magazine_Catch'])
 rows.append(dict(kind='withdrawn magazine disengages catch',distance_m=d,passed=d>.05,method=method))
 W.pose(arm,None,0);return rows
