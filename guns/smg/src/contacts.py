"""Required support contacts on actual evaluated surfaces, independent of export."""
import math,bpy
from mathutils import Vector
from kit import weapon as W,motion,assembly

def part(n):return next(o for o in bpy.context.scene.objects if o.type=='MESH' and (o.name==n or o.get('part_name')==n))
def measure(arm):
 rows=[]
 def contact(a,b,tol,kind,clip='Idle',frame=0):
  W.pose(arm,clip,frame);d,method=assembly.distance(part(a),part(b))
  rows.append(dict(kind=kind,parts=[a,b],clip=clip,frame=frame,distance_m=d,limit_m=tol,method=method,passed=d<=tol))
 for clip,f in [('Idle',0),('Fire',7),('FireLast',12),('ReloadEmpty',181)]:
  contact('Bolt_Face','Chamber_Seat',.0001,'bolt closed against chamber seat',clip,f)
 W.pose(arm,'Idle',0)
 a=motion.surface(part('Bolt_Face'));b=motion.surface(part('Chamber_Seat'));samples=[]
 for x,z in ((.007,.095),(-.007,.095),(0,.102)):
  origin=Vector((x,.173,z));up=Vector((0,1,0))
  face=a['tree'].ray_cast(origin,up,.006);seat=b['tree'].ray_cast(origin,up,.006)
  assert face[0] is not None and seat[0] is not None,(face,seat)
  d=(face[0]-seat[0]).length;assert d<.0004,(face,seat)
  samples.append(dict(bolt_point_m=list(face[0]),seat_point_m=list(seat[0]),gap_m=d))
 rows.append(dict(kind='three chamber-side facing-plane rays',samples=samples,passed=True))
 for side,name in [(1,'Magazine_TopRound_Case'),(-1,'Magazine_SecondRound_Case')]:
  contact('Magazine_FeedLip'+str(side),name,.00016,'formed steel lip retains staggered cartridge')
  contact('Magazine_FeedLip'+str(side),'Magazine_Body',.0002,'lip joins stamped shell')
 contact('Magazine_Follower','Magazine_ThirdRound_Case',.00015,'follower supports staggered display stack')
 contact('MagazineRelease_Catch','Magazine_Body',.00018,'magazine seated on catch ledge')
 # Retention is directional: the lip reaches over the case shoulder, and the
 # case cannot pass directly upward through the retaining land.
 W.pose(arm,'Idle',0)
 for side,name,cx,cz in [(1,'Magazine_TopRound_Case',.0044,.080),(-1,'Magazine_SecondRound_Case',-.0044,.0753)]:
  lip=motion.surface(part('Magazine_FeedLip'+str(side)))
  x=cx+side*.003
  hit=lip['tree'].ray_cast(Vector((x,.138,cz+.010)),Vector((0,0,-1)),.015)
  assert hit[0] is not None,(side,'no overhanging feed lip')
  d=motion.surface(part(name))['tree'].find_nearest(hit[0])[3]
  assert d<.001,(side,d)
  rows.append(dict(kind='overhanging retaining lip ray',side=side,point_m=list(hit[0]),case_gap_m=d,passed=True))
 # Magazine catch's support face is checked independently of minimum distance.
 well=motion.surface(part('Magazine_Body'));catch=motion.surface(part('MagazineRelease_Catch'));samples=[]
 for y in (.140,.143,.145):
  p=Vector((-.0116,y,.053));d=Vector((0,0,1))
  h=well['tree'].ray_cast(p,d,.004);c=catch['tree'].ray_cast(p,d,.004)
  assert h[0] is not None and c[0] is not None,(h,c)
  gap=(h[0]-c[0]).length
  assert h[1].z<-.8 and c[1].z>.8 and gap<.00018,(h,c,gap)
  samples.append(dict(magazine_ledge_m=list(h[0]),catch_land_m=list(c[0]),gap_m=gap))
 rows.append(dict(kind='opposing magazine catch support faces',samples=samples,passed=True))
 contact('Cocking_Tube','Handle_Stem',.00015,'handle seated in locking notch','Charge',50)
 W.pose(arm,'Charge',50)
 stem=motion.surface(part('Handle_Stem'));tube=motion.surface(part('Cocking_Tube'));samples=[]
 for r in (.0088,.0090,.0092):
  x=-r*math.cos(math.radians(35));z=.122+r*math.sin(math.radians(35))
  p=Vector((x,.2155,z));h=tube['tree'].ray_cast(p,Vector((0,-1,0)),.004)
  assert h[0] is not None,h
  gap=stem['tree'].find_nearest(h[0])[3]
  assert h[1].y>.8 and gap<.00018,(h,gap)
  samples.append(dict(notch_wall_m=list(h[0]),normal=list(h[1]),stem_gap_m=gap))
 rows.append(dict(kind='locking notch opposing-face rays',samples=samples,passed=True))
 W.pose(arm,'Reload',34)
 d,_=assembly.distance(part('Magazine_Body'),part('MagazineRelease_Catch'));assert d>.02,d
 rows.append(dict(kind='withdrawn magazine clears catch',distance_m=d,passed=True))
 # Optical ray goes through both rear walls and first meets the front blade.
 W.pose(arm,'Idle',0);eye=bpy.data.objects['Socket_Eye'].matrix_world.translation;hits=[]
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or o.get('bake_only') or o.parent!=arm or 'bone' not in o:continue
  if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())<.001:continue
  h=motion.surface(o)['tree'].ray_cast(eye,Vector((0,1,0)),.8)
  if h[0] is not None:hits.append((h[3],o.get('part_name',o.name)))
 assert hits and min(hits)[1]=='Sight_FrontPost',sorted(hits)[:6]
 rows.append(dict(kind='actual Eye ray through aperture first meets front post',distance_m=min(hits)[0],part=min(hits)[1],passed=True))
 W.pose(arm,None,0)
 if not all(r['passed'] for r in rows):raise AssertionError([r for r in rows if not r['passed']])
 return rows
