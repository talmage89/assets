"""Remove concealed backs from fixed game panels, retaining visible gauge rims.

The high source retains complete manufacturing gauge. Collision verification
reconstructs each declared thin gauge from the measured game exterior; visible
panel positions and corner normals remain unchanged. No opaque visible surface
is removed and moving closures use their separate inner carriers and trim panels.
"""
import bpy


def remove_hidden_backs():
 report={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  if ob.parent.name!='AlderX220' and ob.get('part_category')!='doors' and ob.name!='Liftgate outer':continue
  mesh=ob.data;role=mesh.attributes.get('skin_face_role')
  if role is None:continue
  selected=[f for f in mesh.polygons if role.data[f.index].value!=1]
  if len(selected)==len(mesh.polygons):continue
  mesh.calc_loop_triangles();before=len(mesh.loop_triangles)
  faces=[tuple(f.vertices) for f in selected];ns=[tuple(mesh.corner_normals[li].vector) for f in selected for li in f.loop_indices]
  candidate=bpy.data.meshes.new(mesh.name+' exposed game sheet');candidate.from_pydata([v.co for v in mesh.vertices],[],faces);candidate.update()
  for mat in mesh.materials:candidate.materials.append(mat)
  for f,old in zip(candidate.polygons,selected):f.material_index=old.material_index;f.use_smooth=old.use_smooth
  a=candidate.attributes.new('skin_face_role','INT','FACE')
  for d,old in zip(a.data,selected):d.value=role.data[old.index].value
  candidate.normals_split_custom_set(ns);candidate.calc_loop_triangles()
  ob.data=candidate;ob['allow_boundary']=True
  ob['collision_gauge_m']=.003 if ob.get('part_category') in ['fascia','cladding'] else .0009
  ob['game_sheet_reason']='Concealed reverse faces removed; exposed cut rims retained; high manufacturing source has full gauge'
  report[ob.name]=dict(before=before,after=len(candidate.loop_triangles),saved=before-len(candidate.loop_triangles))
  if mesh.users==0:bpy.data.meshes.remove(mesh)
 return report


def simplify_glazing():
 """Dissolve redundant near-planar glass chords, keeping its boundary fixed.

 Re-seed the old interpolated entrance AND exit normal fields after dissolution.
 Accept only closed candidates whose new triangle probes stay within 1.3 mm
 of the old physical laminate. This is not a normal-only curvature repair.
 """
 import math,bmesh
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 from mathutils.geometry import barycentric_transform
 report={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.get('part_category')!='glass':continue
  old=ob.data;old.calc_loop_triangles();before=len(old.loop_triangles)
  ps=[v.co.copy() for v in old.vertices];ts=[tuple(t.vertices) for t in old.loop_triangles]
  ns=[old.corner_normals[li].vector.copy() for t in old.loop_triangles for li in t.loops]
  tree=BVHTree.FromPolygons(ps,ts,all_triangles=True)
  candidate=old.copy();bm=bmesh.new();bm.from_mesh(candidate)
  bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(1.2),verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False,delimit={'NORMAL'})
  bmesh.ops.triangulate(bm,faces=list(bm.faces));closed=all(e.is_manifold for e in bm.edges)
  bm.to_mesh(candidate);bm.free();candidate.update();candidate.calc_loop_triangles()
  error=0
  for tri in candidate.loop_triangles:
   qq=[candidate.vertices[i].co for i in tri.vertices]
   for p in [sum(qq,Vector())/3]+[(a+c)/2 for a,c in zip(qq,qq[1:]+qq[:1])]:error=max(error,tree.find_nearest(p)[3])
  accepted=closed and error<.0013 and len(candidate.loop_triangles)<before
  report[ob.name]=dict(before=before,after=len(candidate.loop_triangles) if accepted else before,maximum_probe_error_m=error,closed=closed,accepted=accepted)
  if accepted:
   custom=[]
   for face in candidate.polygons:
    for li in face.loop_indices:
     p=candidate.vertices[candidate.loops[li].vertex_index].co
     options=[hit for hit in tree.find_nearest_range(p,.015) if hit[1].dot(face.normal)>.25]
     hit,_,fi,_=min(options,key=lambda h:h[3]) if options else tree.find_nearest(p)
     a,c,d=ts[fi]
     n=barycentric_transform(hit,ps[a],ps[c],ps[d],*ns[3*fi:3*fi+3]).normalized()
     custom.append(n if n.dot(face.normal)>.02 else face.normal)
   candidate.normals_split_custom_set(custom);ob.data=candidate
   if old.users==0:bpy.data.meshes.remove(old)
  else:bpy.data.meshes.remove(candidate)
 return report


def simplify_moldings():
 """Keep grain-sized tessellation out of opaque, rough bumper moldings.

 Reject collapse candidates with >1.5 mm bidirectional surface error or
 >0.5 mm border displacement. The painted body is never a candidate.
 """
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 from kit import model as G
 import bmesh
 report={}
 def capture(me):
  me.calc_loop_triangles()
  return BVHTree.FromPolygons([v.co for v in me.vertices],[tuple(t.vertices) for t in me.loop_triangles],all_triangles=True)
 def probes(me):
  me.calc_loop_triangles();result=[v.co.copy() for v in me.vertices]
  result += [sum((me.vertices[i].co for i in t.vertices),Vector())/3 for t in me.loop_triangles]
  return result
 def border(me):
  bm=bmesh.new();bm.from_mesh(me);ps=[v.co.copy() for v in bm.verts if v.is_boundary];bm.free();return ps
 for ob in bpy.context.scene.objects:
  if ob.name not in ['Front lower bumper cladding','Rear lower bumper cladding']:continue
  original=ob.data;oldtree=capture(original);oldprobes=probes(original);oldborder=border(original);before=len(original.loop_triangles)
  attempts=[]
  for ratio in [.55,.7,.85]:
   ob.data=original.copy();mod=ob.modifiers.new('Molding chord allocation','DECIMATE');mod.ratio=ratio;G.apply(ob)
   candidate=ob.data;candidate.calc_loop_triangles();newtree=capture(candidate)
   error=max([newtree.find_nearest(p)[3] for p in oldprobes]+[oldtree.find_nearest(p)[3] for p in probes(candidate)])
   border_error=max([newtree.find_nearest(p)[3] for p in oldborder]+[oldtree.find_nearest(p)[3] for p in border(candidate)],default=0)
   accepted=error<.0015 and border_error<.0005
   attempts.append(dict(ratio=ratio,triangles=len(candidate.loop_triangles),maximum_probe_error_m=error,border_probe_error_m=border_error,accepted=accepted))
   if accepted:
    # The collapse modifier carries FACE provenance; collision gauge
    # reconstruction starts from these actual new exterior triangles.
    ob['allow_boundary']=True
    if original.users==0:bpy.data.meshes.remove(original)
    break
   ob.data=original;bpy.data.meshes.remove(candidate)
  report[ob.name]=dict(before=before,after=len(ob.data.loop_triangles),attempts=attempts)
 return report
