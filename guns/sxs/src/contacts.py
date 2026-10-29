"""Independent actual-triangle contacts and visual form gauges, in meters."""
import math
import bpy
from mathutils import Vector
from kit import weapon as W,motion
from parameters import HINGE
def part(name):return next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_name',o.name)==name)
def tree(name):return motion.surface(part(name))['tree']
def ray(name,point,direction,length=.12):
 hit=tree(name).ray_cast(Vector(point),Vector(direction).normalized(),length)
 if hit[0] is None:raise AssertionError(('Missing surface',name,point,direction))
 return hit[0]
def measure(arm):
 rows=[]
 def record(name,value,lo,hi,**extra):
  rows.append(dict(name=name,measured_m=float(value),minimum_m=lo,maximum_m=hi,passed=lo<=value<=hi,**extra))
 for frame in range(73):
  W.pose(arm,'Open',frame)
  # Probe the actual concentric hook bore at an occupied angular station,
  # rather than comparing authored pivot constants with each other.
  center=Vector(tuple(v*.001 for v in HINGE));center.x=0
  b=arm.pose.bones['Barrels'];d=(b.matrix@b.bone.matrix_local.inverted()).to_3x3()@Vector((0,-1,0))
  a=ray('Hinge_Pin',center,d);bpt=ray('Barrel_Hook',center,d)
  record('hook/pin f'+str(frame),(bpt-center).length-(a-center).length,0,.00040)
  # Cups rotate about the knuckle. Rays at the cup's local central angle
  # cross the inner iron and the actual fixed outer cheek.
  for side,x in [('R',.014),('L',-.014)]:
   c=center.copy();c.x=x
   d=(b.matrix@b.bone.matrix_local.inverted()).to_3x3()@Vector((0,1,0))
   a=ray('Action_Body',c+d*.025,-d);bpt=ray('Forend_IronCup_'+side,c,d)
   record('forend iron/knuckle '+side+' f'+str(frame),(bpt-c).length-(a-c).length,0,.00040)
 W.pose(arm,'Idle',0)
 # The two tube skins share a rigid owner, so the cross-bone motion sweep
 # does not test their mutual overlap. Their actual global X extrema give
 # an independent separating-plane proof for the complete joined skins.
 right=motion.surface(part('Barrel_R'))['points'];left=motion.surface(part('Barrel_L'))['points']
 record('joined tube separating-plane gap',min(p.x for p in right)-max(p.x for p in left),-1e-8,.00002)
 # Closed breech planes sampled on actual annular barrel steel and the body.
 for side,x in [('R',.0126),('L',-.0126)]:
  for dx,dz in [(0,.0122),(.0122,0),(-.0122,0)]:
   p=(x+dx,.118,.044+dz)
   a=ray('Barrel_'+side,p,(0,-1,0),.02);b=ray('Action_Body',p,(0,-1,0),.02)
   record('standing breech '+side+str((dx,dz)),abs(a.y-b.y),0,.00015)
  shell=motion.surface(part('Live'+side))
  record('shell head flush '+side,abs(min(p.y for p in shell['points'])-.115),0,.00002)
  # Neck clearance is measured radially on both actual cylindrical skins.
  p=(x,.140,.044);outer=ray('Live'+side,(x+.02,.140,.044),(-1,0,0),.03);inner=ray('Barrel_'+side,p,(1,0,0),.03)
  record('shell inside chamber '+side,inner.x-outer.x,0,.0006)
  shoulder=ray('Barrel_'+side,(x,.114,.0549),(0,1,0),.01)
  rear=ray('Barrel_'+side,(x,.114,.0562),(0,1,0),.01)
  record('actual rim recess depth '+side,shoulder.y-rear.y,.0017,.0019)
 # The locking shoe's front/back spans genuinely enter both visible bite cuts.
 for y,z,name in [(.128,.0111,'Locking_Shoe'),(.140,.0139,'Locking_Shoe_Upper')]:
  end=ray('Breech_Lumps',(0,y,z),(0,1,0),.03)
  shoe=ray(name,(0,y,z),(0,1,0),.03)
  record('bite/shoe bearing '+str(y),end.y-shoe.y,0,.00035)
 # Chambers seat the rims at a real forward shoulder; extractor pads reach
 # those same rim faces. The bases are flush at the standing-breech plane.
 for clip in ('Idle','IdleOpenLoaded'):
  W.pose(arm,clip,0)
  for side in ('R','L'):
   shell=motion.surface(part('Live'+side));pad=tree('Extractor_Rim_'+side)
   points=[p for p in shell['points'] if pad.find_nearest(p)[3]<.00010]
   assert points,(clip,side,'no rim support')
   distances=sorted(pad.find_nearest(p)[3] for p in shell['points'])
   record('shell/extractor '+clip+side,distances[0],0,.00010,support_vertices=len(points))
 W.pose(arm,'Idle',0)
 eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
 comb=ray('Stock_Walnut',eye,(0,0,-1),.1)
 record('eye above actual comb',eye.z-comb.z,.035,.055)
 forward=bpy.data.objects['Socket_Eye'].matrix_world.to_3x3()@Vector((0,1,0))
 # The bead must be hit by an actual axial sight ray.
 hit=tree('Front_Bead').ray_cast(eye,forward,1.0)
 assert hit[0] is not None,'Bead absent on exact optical line'
 # Visibility is separate from hitting a bead tree: every visible rigid skin
 # may occlude the optical ray, and the short forward rib must be visible too.
 visible=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o
  and min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 for name,target in [('bead',hit[0])]+[('rib '+str(y),ray('Solid_TopRib',(0,y,.09),(0,0,-1))) for y in (.50,.65,.74)]:
  delta=target-eye
  blockers=[o.get('part_name',o.name) for o in visible
   if motion.surface(o)['tree'].ray_cast(eye,delta.normalized(),delta.length-.00005)[0] is not None]
  assert not blockers,(name,'sight obstruction',blockers)
 # Stock drop is measured from an actual straightedge across the rib, not
 # from the bead center or a generator constant.
 a=ray('Solid_TopRib',(0,.116,.09),(0,0,-1));b=ray('Solid_TopRib',(0,.774,.09),(0,0,-1))
 datum=lambda y:a.z+(y-a.y)*(b.z-a.z)/(b.y-a.y)
 for name,y,lo,hi in [('comb',-.088,.037,.040),('heel',-.298,.062,.064)]:
  p=ray('Stock_Walnut',(0,y,.09),(0,0,-1),.3)
  record('drop at '+name,datum(y)-p.z,lo,hi,station_y_m=y)
 record('cheek station behind comb nose',-.088-eye.y,.03175,.03810)
 for clip,state in [('Idle','fire'),('IdleSafe','safe')]:
  W.pose(arm,clip,0)
  # Safety guide remains within reach of its cut strap in each detent.
  saf=motion.surface(part('Safety_Guide'));rails=[tree('Safety_Track_R'),tree('Safety_Track_L')]
  gap=min(t.find_nearest(p)[3] for p in saf['points'] for t in rails)
  record('safety detent support '+state,gap,0,.001)
 for clip in ('Idle','Close'):
  W.pose(arm,clip,0 if clip=='Idle' else 72)
  a=motion.surface(part('Top_LeverSpindle'));body=tree('Action_Body')
  gap=min(body.find_nearest(p)[3] for p in a['points']);record('lever returned seat '+clip,gap,0,.001)
 W.pose(arm,'Idle',0)
 return dict(passed=all(r['passed'] for r in rows),records=rows,comb_m=list(comb),eye_m=list(eye))
