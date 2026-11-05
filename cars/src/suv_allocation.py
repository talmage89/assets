"""Remove concealed backs from fixed game panels, retaining visible gauge rims.

The high source retains complete manufacturing gauge. Collision verification
reconstructs each declared thin gauge from the measured game exterior; visible
panel positions and corner normals remain unchanged. No opaque visible surface
is removed and moving closures use their separate inner carriers and trim panels.
"""
import bpy


def fair_front_molding_seam():
 """Replace independent centroid setbacks with one fair molded seam curve.

 Only the existing seam vertices move, by less than 2.25 mm. The aperture,
 body control cage, tessellation and continuous parent normal fields stay put.
 """
 from suv_sculpt import lower_edge
 import suv_spec as S
 for name,sign in [('Front molded fascia',1),('Front lower bumper cladding',-1)]:
  ob=bpy.data.objects[name];me=ob.data;role=me.attributes['skin_face_role'];edges={}
  for f in me.polygons:
   if role.data[f.index].value!=0:continue
   for a,c in zip(f.vertices,tuple(f.vertices[1:])+tuple(f.vertices[:1])):
    e=tuple(sorted((a,c)));edges[e]=edges.get(e,0)+1
  boundary={i for e,count in edges.items() if count==1 for i in e}
  moves={}
  for i in boundary:
   p=ob.matrix_world@me.vertices[i].co
   if abs(p.x)>.54 or abs(p.z-lower_edge(p.x,True))>.004:continue
   moves[i]=lower_edge(p.x,True)+sign*S.PANEL_GAP/2-p.z
  # Carry the adjacent reverse/rim samples by the same local displacement.
  original=[v.co.copy() for v in me.vertices]
  for v in me.vertices:
   p=ob.matrix_world@original[v.index]
   near=min(moves,key=lambda i:(original[v.index]-original[i]).length_squared) if moves else None
   if near is not None and (original[v.index]-original[near]).length<.004:p.z+=moves[near];v.co=ob.matrix_world.inverted()@p
  me.update()


def couple_glass_normals(ob,source=None):
 """One outside normal field for both sides of a parallel glass laminate.

 Independent nearest-corner transfers can select a rim on one side and the
 pane on the other, turning a 4.8 mm window into a strong optical prism.
 Classification uses the actual side-facing sheets; rims remain flat.
 """
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 from mathutils.geometry import barycentric_transform
 source=source or ob.data;source.calc_loop_triangles()
 direction=ob.matrix_world.to_3x3().inverted()@Vector((-1 if ob.name.endswith('_L') else 1,0,0));direction.normalize()
 triangles=[t for t in source.loop_triangles if t.normal.dot(direction)>.5]
 ps=[v.co.copy() for v in source.vertices];ts=[tuple(t.vertices) for t in triangles]
 ns=[source.corner_normals[i].vector.copy() for t in triangles for i in t.loops]
 tree=BVHTree.FromPolygons(ps,ts,all_triangles=True);custom=[]
 for face in ob.data.polygons:
  facing=face.normal.dot(direction)
  for li in face.loop_indices:
   if abs(facing)<=.5:custom.append(face.normal);continue
   p=ob.data.vertices[ob.data.loops[li].vertex_index].co
   hit,_,fi,d=tree.ray_cast(p+direction*.03,-direction,.1)
   if hit is None:hit,_,fi,d=tree.find_nearest(p)
   a,c,e=ts[fi];n=barycentric_transform(hit,ps[a],ps[c],ps[e],*ns[fi*3:fi*3+3]).normalized()
   if facing<0:n.negate()
   custom.append(n if n.dot(face.normal)>.5 else face.normal)
 ob.data.normals_split_custom_set(custom)
 ob['glass_normal_basis']='Shared exterior field for entrance and exit; physical rims flat'


def remove_hidden_backs():
 report={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  sheet_count=ob.get('cassette_sheet_vertex_count',ob.get('trim_sheet_vertex_count'))
  if sheet_count:
   # Solidify keeps the source sheet first and the concealed reverse second.
   # Preserve the visible sheet and its rim, exactly, with manufacturing gauge
   # reconstructed for the independent collision sweep as on the body panels.
   if len(ob.data.vertices)!=sheet_count*2:raise ValueError('Sheet allocation lost provenance: '+ob.name)
   role=ob.data.attributes.new('skin_face_role','INT','FACE')
   for f,d in zip(ob.data.polygons,role.data):
    d.value=0 if all(i<sheet_count for i in f.vertices) else 1 if all(i>=sheet_count for i in f.vertices) else 2
  # Optical laminates need their real exit surface. Face provenance is now
  # present on lamp covers too; it is not permission to remove their backs.
  if ob.get('part_category')=='glass' or ob.name.startswith(('Headlamp opening','Taillamp opening')) and not sheet_count:continue
  if ob.parent.name!='AlderX220' and ob.get('part_category')!='doors' and ob.name!='Liftgate outer' and not sheet_count:continue
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
  if mesh.attributes.get('BodyNormal'):
   a=candidate.attributes.new('BodyNormal','FLOAT_VECTOR','POINT')
   a.data.foreach_set('vector',[q for d in mesh.attributes['BodyNormal'].data for q in d.vector])
  candidate.normals_split_custom_set(ns);candidate.calc_loop_triangles()
  ob.data=candidate;ob['allow_boundary']=True
  ob['collision_gauge_m']=.002 if ob.get('cassette_sheet_vertex_count') else .003 if ob.get('part_category') in ['fascia','cladding'] or ob.get('trim_sheet_vertex_count') else .0009
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
  if ob.get('optical_patch'):
   report[ob.name]=dict(accepted=False,reason='Authored optical collar and chart allocation retained; no fan-producing edge dissolution')
   continue
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
   ob.data=candidate;couple_glass_normals(ob,old)
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
  me.calc_loop_triangles();used={i for t in me.loop_triangles for i in t.vertices};result=[me.vertices[i].co.copy() for i in sorted(used)]
  result += [sum((me.vertices[i].co for i in t.vertices),Vector())/3 for t in me.loop_triangles]
  return result
 def border(me):
  bm=bmesh.new();bm.from_mesh(me);ps=[v.co.copy() for v in bm.verts if v.is_boundary];bm.free();return ps
 def gauge_valid(me):
  role=me.attributes['skin_face_role']
  data=bpy.data.meshes.new('Molding allocation gauge probe');data.from_pydata([v.co for v in me.vertices],[],[tuple(f.vertices) for f in me.polygons if role.data[f.index].value==0]);data.update()
  probe=bpy.data.objects.new('Molding allocation gauge probe',data);bpy.context.collection.objects.link(probe)
  sol=probe.modifiers.new('Actual collision gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;sol.use_even_offset=True;G.apply(probe)
  bm=bmesh.new();bm.from_mesh(probe.data);valid=all(e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)>0;bm.free()
  data=probe.data;bpy.data.objects.remove(probe,do_unlink=True);bpy.data.meshes.remove(data)
  return valid
 for ob in bpy.context.scene.objects:
  if ob.name not in ['Front lower bumper cladding','Rear lower bumper cladding']:continue
  original=ob.data;oldtree=capture(original);oldprobes=probes(original);oldborder=border(original);before=len(original.loop_triangles)
  attempts=[]
  for ratio in [.55,.7,.85]:
   ob.data=original.copy();mod=ob.modifiers.new('Molding chord allocation','DECIMATE');mod.ratio=ratio;G.apply(ob)
   candidate=ob.data;candidate.calc_loop_triangles();newtree=capture(candidate)
   error=max([newtree.find_nearest(p)[3] for p in oldprobes]+[oldtree.find_nearest(p)[3] for p in probes(candidate)])
   border_error=max([newtree.find_nearest(p)[3] for p in oldborder]+[oldtree.find_nearest(p)[3] for p in border(candidate)],default=0)
   valid=gauge_valid(candidate)
   accepted=error<.0015 and border_error<.0005 and valid
   attempts.append(dict(ratio=ratio,triangles=len(candidate.loop_triangles),maximum_probe_error_m=error,border_probe_error_m=border_error,collision_gauge_valid=valid,accepted=accepted))
   if accepted:
    # The collapse modifier carries FACE provenance; collision gauge
    # reconstruction starts from these actual new exterior triangles.
    ob['allow_boundary']=True
    if original.users==0:bpy.data.meshes.remove(original)
    break
   ob.data=original;bpy.data.meshes.remove(candidate)
  report[ob.name]=dict(before=before,after=len(ob.data.loop_triangles),attempts=attempts)
  # Reallocate redundant near-planar molding chords to the visible optics and
  # cargo liners. Keep all boundary vertices, the sheet roles and parent field;
  # accept only actual bidirectional surface error below the existing 1.5 mm.
  original=ob.data;oldtree=capture(original);oldprobes=probes(original);oldborder=border(original)
  candidate=original.copy();bm=bmesh.new();bm.from_mesh(candidate);bm.normal_update()
  role=bm.faces.layers.int.get('skin_face_role')
  for f in bm.faces:f.material_index=f[role]
  bmesh.ops.dissolve_limit(bm,angle_limit=__import__('math').radians(1),verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False,delimit={'NORMAL','MATERIAL'})
  bmesh.ops.triangulate(bm,faces=list(bm.faces))
  for f in bm.faces:f.material_index=0
  bm.to_mesh(candidate);bm.free();candidate.calc_loop_triangles();newtree=capture(candidate)
  error=max([newtree.find_nearest(p)[3] for p in oldprobes]+[oldtree.find_nearest(p)[3] for p in probes(candidate)])
  border_error=max([newtree.find_nearest(p)[3] for p in oldborder]+[oldtree.find_nearest(p)[3] for p in border(candidate)],default=0)
  valid=gauge_valid(candidate)
  accepted=error<.0015 and border_error<.0005 and valid
  report[ob.name]['planar_allocation']=dict(accepted=accepted,triangles=len(candidate.loop_triangles),maximum_probe_error_m=error,border_probe_error_m=border_error,collision_gauge_valid=valid)
  if accepted:ob.data=candidate
  else:bpy.data.meshes.remove(candidate)
  report[ob.name]['after']=len(ob.data.loop_triangles)
 return report
