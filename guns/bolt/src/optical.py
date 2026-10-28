"""Check the visual optic's structural passage, including joined GLB meshes."""
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def passage(parts,eye):
 trees=[];dg=bpy.context.evaluated_depsgraph_get()
 for ob in parts:
  if ob.name.startswith(('Lens_','Reticle_')):continue
  world_bounds=[ob.matrix_world@Vector(p) for p in ob.bound_box]
  if max(p.z for p in world_bounds)<eye.z-.008 or min(p.z for p in world_bounds)>eye.z+.008:continue
  ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles()
  points=[ev.matrix_world@v.co for v in mesh.vertices];faces=[]
  for tri in mesh.loop_triangles:
   mat=mesh.materials[tri.material_index] if mesh.materials else None
   if mat and mat.name.startswith(('CP_glass','CP_reticle')):continue
   faces.append(tuple(tri.vertices))
  ev.to_mesh_clear()
  if faces:trees.append((ob.name,BVHTree.FromPolygons(points,faces,all_triangles=True)))
 rows=[]
 for dx in (-.008,0,.008):
  for dz in (-.008,0,.008):
   origin=eye+Vector((dx,0,dz))
   blocked=[name for name,tree in trees if tree.ray_cast(origin,Vector((0,1,0)),.5)[0] is not None]
   assert not blocked,('blocked optical passage',dx,dz,blocked)
   rows.append(dict(offset_m=[dx,dz],blocked_by=blocked))
 return dict(passed=True,rays=rows,meaning='Structural passage only; glass proxies and etched reticle excluded')
