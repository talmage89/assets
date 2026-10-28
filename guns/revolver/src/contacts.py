"""Actual triangle-surface construction evidence; independent of round trip."""
import math,bpy
from mathutils import Vector
from kit import weapon as W,motion,assembly
def part(name):return next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_name',o.name)==name)
def measure(arm):
 rows=[]
 def contact(a,b,limit,kind):
  d,method=assembly.distance(part(a),part(b))
  row=dict(kind=kind,a=a,b=b,distance_m=d,limit_m=limit,method=method,passed=d<=limit)
  rows.append(row)
 def ray(surface,p,d,maximum=.02):
  h=surface['tree'].ray_cast(Vector(p),Vector(d),maximum)
  assert h[0] is not None,(p,d)
  return h
 W.pose(arm,'Idle',0)
 barrel=motion.surface(part('Barrel'));cylinder=motion.surface(part('Cylinder_Fluted'))
 # Opposing annular front faces, away from chamber voids and the crane.
 gaps=[]
 for x,z in [(.0058,.061),(-.0058,.061),(0,.0668)]:
  start=(x,.0823,z)
  a=ray(cylinder,start,(0,-1,0));b=ray(barrel,start,(0,1,0))
  gaps.append(dict(cylinder=list(a[0]),cone=list(b[0]),gap_m=(b[0]-a[0]).length))
 assert all(.00012<g['gap_m']<.00030 for g in gaps),gaps
 rows.append(dict(kind='cylinder / forcing cone gap',samples=gaps,passed=True))
 # Actual inner surfaces determine both centers from opposing cross rays.
 def center(s,y,z):
  p=Vector((0,y,z));hits=[ray(s,p,d,.009)[0] for d in [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]]
  return Vector(((hits[0].x+hits[1].x)/2,y,(hits[2].z+hits[3].z)/2))
 bc=center(barrel,.100,.061);cc=center(cylinder,.081,.061)
 error=math.hypot(bc.x-cc.x,bc.z-cc.z)
 assert error<.00008,(bc,cc)
 rows.append(dict(kind='chamber / bore coaxial from inner surfaces',barrel_center=list(bc),chamber_center=list(cc),error_m=error,passed=True))
 for clip,f in [('Idle',0),('Fire',24),('Fire2',24),('FireLast',24),('CockHammer',32)]:
  W.pose(arm,clip,f)
  contact('CylinderStop','Cylinder_Fluted',.00035,'stop seated in bolt notch: '+clip)
  c=motion.surface(part('Cylinder_Fluted'));stop=motion.surface(part('CylinderStop'))
  origin=(0,.044,.029)
  roof=ray(c,origin,(0,0,1),.003);tip=ray(stop,origin,(0,0,1),.003)
  gap=roof[0].z-tip[0].z
  assert roof[1].z<-.85 and tip[1].z>.85 and 0<=gap<.00015,(clip,roof,tip)
  rows.append(dict(kind='opposing stop top / notch roof',clip=clip,frame=f,stop_point=list(tip[0]),
   notch_point=list(roof[0]),gap_m=gap,passed=True))
  contact('CylinderStop_Bearing','CylinderStop_Pin',.00015,'stop rocker bearing / pin: '+clip)
 # Cartridge front rim face bears on the actual rear face in its counterbore.
 W.pose(arm,'Idle',0)
 for i in range(6):
  contact('Live'+str(i)+'_Case','Cylinder_Fluted',.00010,'rim seated / chamber '+str(i))
  case=motion.surface(part('Live'+str(i)+'_Case'))
  # A ray starts inside the rim and reaches its front bearing plane. The
  # same ray reaches the opposing counterbore face on the cylinder.
  from parameters import chamber
  x,y,z=chamber(i);t=math.pi/2+i*math.tau/6
  origin=Vector(((x+5.3*math.cos(t))*.001,.0392,(z+5.3*math.sin(t))*.001))
  rim=ray(case,origin,(0,1,0),.003);seat=ray(cylinder,origin,(0,1,0),.003)
  distance=(rim[0]-seat[0]).length
  assert rim[1].y>.85 and seat[1].y<-.85 and distance<.0001,(i,rim,seat)
  rear=min(p.y for p in cylinder['points']);depth=seat[0].y-rear
  flush=min(p.y for p in case['points'])-rear
  assert .0013<depth<.0015 and abs(flush)<.0001,(i,depth,flush)
  rows.append(dict(kind='opposing rim / counterbore faces',chamber=i,rim=list(rim[0]),seat=list(seat[0]),gap_m=distance,counterbore_depth_m=depth,case_head_flush_error_m=flush,passed=True))
 contact('Crane_Yoke','Crane_ClosedSeat',.00020,'closed crane heel against frame seat')
 contact('Latch_CenterPin','Extractor_LatchHub',.00015,'center latch pin shoulder on star hub')
 contact('Hammer_Body','Hammer_RestSeat',.0007,'hammer against rest seat')
 contact('Trigger_Shoe','Trigger_RestStop',.00015,'trigger hidden land against stop')
 # Eye is exactly at the notch's top, sees the blade centered above the bore.
 eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
 sight=motion.surface(part('FrontSight_PinnedRamp'));rear=motion.surface(part('RearSight_NotchBody'))
 top=max(p.z for p in sight['points']);backtop=max(p.z for p in rear['points'])
 assert abs(top-backtop)<.0001 and abs(eye.z-backtop)<.0001,(top,backtop,eye)
 rear_station=min(p.y for p in rear['points'])
 rows.append(dict(kind='aligned front and rear tops at Eye height',front_top_m=top,rear_top_m=backtop,eye_m=list(eye),notch_distance_m=rear_station-eye.y,passed=True))
 # No forging, cylinder or hammer crosses a ray just below the front top.
 origin=Vector((eye.x,eye.y,eye.z-.0003));hits=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or 'bone' not in ob:continue
  if arm.pose.bones[ob['bone']].matrix.to_scale().length<.01:continue
  h=motion.surface(ob)['tree'].ray_cast(origin,Vector((0,1,0)),1.0)
  if h[0] is not None:hits.append((h[3],ob.get('part_name',ob.name)))
 assert hits and min(hits)[1]=='FrontSight_PinnedRamp',sorted(hits)[:5]
 rows.append(dict(kind='Eye ray first reaches front blade',first_hit=min(hits),passed=True))
 # Required support at full extraction and at the loader's seated pose.
 W.pose(arm,'Reload',58)
 for i in range(6):contact('Extractor_Star','Case'+str(i)+'_Case',.00015,'star bears on extracted rim '+str(i))
 W.pose(arm,'Reload',142)
 for i in range(6):contact('Speedloader_RimClip'+str(i),'LoaderRound'+str(i)+'_Case',.00015,'loader retains rim '+str(i))
 W.pose(arm,None,0)
 return dict(passed=all(r['passed'] for r in rows),measurements=rows)
