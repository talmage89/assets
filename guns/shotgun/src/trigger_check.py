"""Measured trigger direction, flat blade section, rest stop and pulled guard."""
from mathutils import Vector
from kit import motion,weapon as W,assembly
from contacts import part

def measure(arm):
 W.pose(arm,'Idle',0);shoe=part('Trigger_Shoe');plate=part('Trigger_Plate')
 tree=motion.surface(shoe)['tree']
 def hit(z,front=True):
  p=tree.ray_cast(Vector((.0015,.120 if front else .060,z)),Vector((0,-1 if front else 1,0)),.080)[0]
  assert p is not None,(z,front)
  return p
 upper,middle,lower=[hit(z) for z in (-.008,-.015,-.022)]
 depth=(upper.y+lower.y)/2-middle.y
 back=[hit(z,False) for z in (-.008,-.015,-.022)]
 convex=(back[0].y+back[2].y)/2-back[1].y
 toe=hit(-.024)
 assert depth>.001 and convex>.001,(depth,convex)
 assert toe.y-middle.y>.003,('toe must curl toward muzzle',toe,middle)
 skin=motion.surface(shoe);width=skin['hi'].x-skin['lo'].x
 assert .0059<width<.0061,width
 stop=[]
 for x in (-.0015,0,.0015):
  origin=Vector((x,.079,-.002));direction=Vector((0,-1,0))
  a=tree.ray_cast(origin,direction,.004);b=motion.surface(plate)['tree'].ray_cast(origin,direction,.004)
  assert a[0] is not None and b[0] is not None,(a,b)
  gap=a[0].y-b[0].y
  assert abs(gap)<.00015 and a[1].y<-.8 and b[1].y>.8,(gap,a,b)
  stop.append(dict(trigger_m=list(a[0]),plate_m=list(b[0]),gap_m=gap))
 W.pose(arm,'Fire',2)
 d,method=assembly.distance(shoe,plate)
 assert d>.00002,(d,method)
 # Independent lower-blade samples supplement the all-clip solid sweep.
 lower_points=[p for p in motion.surface(shoe)['points'] if p.z<-.008]
 guard=motion.surface(plate)['tree'];lower_gap=min(guard.find_nearest(p)[3] for p in lower_points)
 assert lower_gap>.0001,lower_gap
 W.pose(arm,'Idle',0)
 return dict(passed=True,front_samples_m=[list(p) for p in (upper,middle,lower)],
  concavity_depth_m=depth,rear_convexity_m=convex,toe_m=list(toe),width_m=width,
  side_depths_m=[a.y-b.y for a,b in zip((upper,middle,lower),back)],
  rest_stop=stop,pulled_plate_clearance_m=d,clearance_method=method,
  pulled_lower_blade_to_guard_vertex_sample_min_m=lower_gap)
