"""Measured form evidence, independent of serialization equality."""
import math
from mathutils import Vector
import bpy
from kit import motion
from contacts import part

def audit():
 eye=bpy.data.objects['Socket_Eye'].matrix_world
 point=eye.translation;forward=(eye.to_3x3()@Vector((0,1,0))).normalized()
 up=(eye.to_3x3()@Vector((0,0,1))).normalized()
 stock=motion.surface(part('Stock'))
 hit=stock['tree'].ray_cast(point,Vector((0,0,-1)),.15)
 assert hit[0] is not None,'Eye station must lie over the actual comb'
 height=point.z-hit[0].z
 assert .035<height<.050,(height,hit)
 # A convex camera frustum and triangles wholly below its lower plane cannot
 # contain stock. This catches the old wood obstruction even if the bead ray
 # itself happens to clear the receiver. Lens/aspect match the aimed shot.
 half_tangent=(36/1.6)/2/55
 lower_margin=max((p-point).dot(up)+half_tangent*(p-point).dot(forward)
                  for p in stock['points'])
 assert lower_margin<-.001,('Stock crosses aimed lower frustum plane',lower_margin)
 guard=motion.surface(part('Trigger_Plate'))['tree']
 def ray(p,d):
  h=guard.ray_cast(Vector(p),Vector(d),.10)
  assert h[0] is not None,(p,d)
  return h[0]
 # Exclude the trigger and safety by measuring only the casting's triangles.
 origin=(.0045,.084,-.016)
 top=ray(origin,(0,0,1));bottom=ray(origin,(0,0,-1))
 left=ray((0,.084,-.016),(0,-1,0));right=ray((0,.084,-.016),(0,1,0))
 inner=ray((0,.084,-.016),(0,0,-1));outer=ray((0,.084,-.050),(0,0,1))
 opening_height=top.z-bottom.z;opening_length=right.y-left.y;wall=inner.z-outer.z
 opening_max=max(ray((0,.084,z),(0,1,0)).y-ray((0,.084,z),(0,-1,0)).y for z in (-.020,-.016,-.012,-.008,-.006))
 assert .020<opening_height<.030 and .050<opening_length<.070,(opening_height,opening_length)
 assert .0035<wall<.0055,wall
 wood=motion.surface(part('Forend_Wood'));size=wood['hi']-wood['lo']
 assert .218<size.y<.222 and .038<size.x<.041 and .044<size.z<.047,size
 pad=motion.surface(part('Recoil_Pad'))['tree'];axis=Vector((0,1,.11)).normalized();center=Vector((0,-.2484,-.056))
 front=pad.ray_cast(center,axis,.04);back=pad.ray_cast(center,-axis,.04)
 assert front[0] is not None and back[0] is not None,(front,back)
 thickness=(front[0]-back[0]).length
 assert .023<thickness<.026,thickness
 shoulder=bpy.data.objects['Socket_Butt'].matrix_world.translation
 shoulder_gap=pad.find_nearest(shoulder)[3]
 assert shoulder_gap<.0002,shoulder_gap
 return dict(eye_position_m=list(point),comb_point_m=list(hit[0]),eye_above_comb_m=height,
  optical_pitch_degrees=math.degrees(math.atan2(forward.z,forward.y)),
  stock_aimed_lower_plane_max_m=lower_margin,guard_opening_height_m=opening_height,
  guard_opening_length_m=opening_length,guard_opening_max_length_m=opening_max,guard_bow_wall_m=wall,forend_size_m=list(size),
  pad_normal_thickness_m=thickness,pad_back_pitch_degrees=math.degrees(math.atan2(abs(back[1].z),abs(back[1].y))),
  shoulder_socket_pad_distance_m=shoulder_gap)
