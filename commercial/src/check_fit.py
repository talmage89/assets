"""Owner-authorized READ-ONLY cylinder fit. Never save or export the reference."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils.bvhtree import BVHTree
from mathutils import Vector
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,required=True);a.add_argument('--source',type=Path,default=Path('build/look/station-101.blend'));a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 before=hashlib.sha256(a.reference.read_bytes()).hexdigest()
 source=a.source;bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
 cage=bpy.data.objects['PropaneCage'];ob=bpy.data.objects['PropaneCage__Mesh'];inv=cage.matrix_world.inverted()
 vs=[inv@ob.matrix_world@v.co for v in ob.data.vertices];ob.data.calc_loop_triangles()
 tree=BVHTree.FromPolygons(vs,[tuple(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
 bottom=tree.ray_cast(Vector((0,0,.20)),Vector((0,0,-1)))[0].z
 ceiling=tree.ray_cast(Vector((0,0,.20)),Vector((0,0,1)))[0].z
 actual_height=ceiling-bottom
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.reference.resolve()))
 ps=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
 lo=[min(v[k] for v in ps) for k in range(3)];hi=[max(v[k] for v in ps) for k in range(3)];dim=[b-a for a,b in zip(lo,hi)]
 # Shelf cell clearance is measured against the owner's real imported envelope.
 cell=[.44,.74,actual_height];gaps=[a-b for a,b in zip(cell,dim)]
 assert min(gaps)>0,'Owner cylinder does not fit cage shelf cell'
 assert before==hashlib.sha256(a.reference.read_bytes()).hexdigest()
 Path('build/tank-fit.json').write_text(json.dumps(dict(reference_sha256=before,actual_reference_bounds_m=[lo,hi],actual_reference_dimensions_m=dim,declared_horizontal_cell_and_measured_height_m=cell,actual_shelf_surfaces_m=[bottom,ceiling],clearance_m=gaps,scope='AABB fit to declared horizontal bay; shelf height ray-measured on actual cage. Reference never joined, baked, saved or exported'),indent=2))
 print('OWNER TANK FIT',dim,gaps)
 bpy.ops.wm.read_factory_settings(use_empty=True)
