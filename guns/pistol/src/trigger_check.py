"""Actual blade surfaces: direction, sections, safety bearing and rest stop."""
import bpy
from mathutils import Vector
from kit import motion,weapon as W,assembly

def measure(arm):
 W.pose(arm,'Idle',0)
 shoe=bpy.data.objects['Trigger_Shoe'];frame=bpy.data.objects['Frame_Grip']
 def face(z,front=True,x=.002):
  tree=motion.surface(shoe)['tree']
  hit=tree.ray_cast(Vector((x,.080 if front else .030,z)),Vector((0,-1 if front else 1,0)),.060)
  assert hit[0] is not None,(z,front)
  return hit[0]
 upper,middle,lower=[face(z) for z in (.023,.015,.007)]
 hollow=(upper.y+lower.y)/2-middle.y
 assert hollow>.0006,('muzzle-facing concavity',hollow)
 toe=face(.0035)
 assert toe.y-middle.y>.0015,('forward toe',toe,middle)
 rear=[face(z,False) for z in (.023,.015,.007)]
 convex=(rear[0].y+rear[2].y)/2-rear[1].y
 assert convex>.0006,('grip-facing convex back',convex)
 points=motion.surface(shoe)['points'];width=max(p.x for p in points)-min(p.x for p in points)
 assert .0069<width<.0071,width
 # Opposing rays measure the hidden land against the existing slot-end wall.
 stop=[]
 for x in (-.002,0,.002):
  origin=Vector((x,.054,.0269));direction=Vector((0,1,0))
  a=motion.surface(shoe)['tree'].ray_cast(origin,direction,.004)
  b=motion.surface(frame)['tree'].ray_cast(origin,direction,.004)
  assert a[0] is not None and b[0] is not None,(a,b)
  gap=b[0].y-a[0].y
  assert -.00002<=gap<.00015 and a[1].y>.8 and b[1].y<-.8,(gap,a,b)
  stop.append(dict(shoe_m=list(a[0]),frame_m=list(b[0]),gap_m=gap))
 blade=motion.surface(bpy.data.objects['Trigger_SafetyBlade'])
 blade_width=blade['hi'].x-blade['lo'].x
 gauges=[]
 for z in (.010,.021):
  a=blade['tree'].ray_cast(Vector((0,.060,z)),Vector((0,-1,0)),.030)[0]
  b=blade['tree'].ray_cast(Vector((0,.035,z)),Vector((0,1,0)),.030)[0]
  assert a is not None and b is not None
  gauges.append(dict(z_m=z,front_m=list(a),back_m=list(b),depth_m=a.y-b.y))
 bearing=[];guard=[]
 for frame_number in (0,1,2):
  W.pose(arm,'Fire',frame_number)
  d,method=assembly.distance(bpy.data.objects['Trigger_SafetyBlade'],bpy.data.objects['Trigger_SafetyPivot'])
  assert .00001<d<.00016,(frame_number,d)
  bearing.append(dict(frame=frame_number,gap_m=d,method=method))
  # Clearance is the evaluated whole shoe to the fixed frame; the full clip
  # sweep separately tests solid intersections and the safety's curved pocket.
  if frame_number==2:
   d,method=assembly.distance(shoe,frame)
   assert d>.00005,(d,method)
   lower_points=[p for p in motion.surface(shoe)['points'] if p.z<.022]
   frame_tree=motion.surface(frame)['tree']
   lower_gap=min(frame_tree.find_nearest(p)[3] for p in lower_points)
   assert lower_gap>.001,lower_gap
   guard.append(dict(frame=frame_number,gap_m=d,method=method,lower_blade_to_guard_vertex_sample_min_m=float(lower_gap)))
 W.pose(arm,None,0)
 return dict(passed=True,front_samples_m=[list(p) for p in (upper,middle,lower)],
  concavity_depth_m=hollow,rear_convexity_m=convex,toe_m=list(toe),width_m=width,
  rest_stop=stop,safety_width_m=blade_width,safety_leaf_gauges=gauges,safety_bearing=bearing,pulled_frame_clearance=guard)

def capture(arm):
 """Triangle keys identify source parts, never substitute for imported surfaces."""
 from mathutils.kdtree import KDTree
 W.pose(arm,None,0);records=[];owners={}
 for name in ('Trigger_Shoe','Trigger_SafetyBlade','Trigger_SafetyPivot','Frame_Grip'):
  ob=bpy.data.objects[name];owners[name]=ob['bone'];ob.data.calc_loop_triangles()
  for t in ob.data.loop_triangles:
   records.append((name,ob['bone'],[ob.matrix_world@ob.data.vertices[i].co for i in t.vertices]))
 trees={}
 for bone in set(owners.values()):
  selected=[(i,r) for i,r in enumerate(records) if r[1]==bone];tree=KDTree(len(selected))
  for i,r in selected:tree.insert(sum(r[2],Vector())/3,i)
  tree.balance();trees[bone]=tree
 return records,owners,trees

def imported(arm,reference):
 """Measure one-to-one matched triangles from the actual consolidated GLB."""
 records,owners,trees=reference;W.pose(arm,None,0);mapped={name:[] for name in owners};seen=set();maximum=0
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 for ob in meshes:
  ob.data.calc_loop_triangles()
  for t in ob.data.loop_triangles:
   bone=ob.vertex_groups[max(ob.data.vertices[t.vertices[0]].groups,key=lambda g:g.weight).group].name
   if bone not in trees:continue
   points=[ob.matrix_world@ob.data.vertices[i].co for i in t.vertices]
   _,index,d=trees[bone].find(sum(points,Vector())/3)
   if d>2e-7:continue
   name,_,expected=records[index]
   delta=max(min((p-q).length for q in expected) for p in points)
   assert delta<2e-7 and index not in seen,(name,delta,index)
   seen.add(index);maximum=max(maximum,delta);mapped[name].append(points)
 assert len(seen)==len(records),(len(seen),len(records))
 for ob in meshes:bpy.data.objects.remove(ob,do_unlink=True)
 for name,triangles in mapped.items():
  me=bpy.data.meshes.new('Actual imported '+name)
  me.from_pydata([tuple(p) for tri in triangles for p in tri],[],[(i*3,i*3+1,i*3+2) for i in range(len(triangles))]);me.update()
  ob=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(ob);W.rigid_bind(ob,arm,owners[name])
 result=measure(arm);result['imported_triangles']=len(seen);result['maximum_match_delta_m']=maximum
 result['scope']='actual imported triangles matched one-to-one; measurements independent of serialization'
 return result
