"""Independent ray-hit patches projected into the declared comparison camera."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source))
else:V.import_glb(source)
arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
triangles=[];verts=[];dg=bpy.context.evaluated_depsgraph_get()
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();offset=len(verts)
 verts.extend(ev.matrix_world@v.co for v in mesh.vertices)
 triangles.extend(tuple(offset+i for i in t.vertices) for t in mesh.loop_triangles);ev.to_mesh_clear()
tree=BVHTree.FromPolygons(verts,triangles,all_triangles=True)
cal=json.loads((BASE/'build/photo-cameras.json').read_text())['used_photo'];shot=cal['shot']
data=bpy.data.cameras.new('Value projection');cam=bpy.data.objects.new('Value projection',data);bpy.context.scene.collection.objects.link(cam)
cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));data.sensor_fit='HORIZONTAL';data.sensor_width=36;data.lens=shot['lens']
sc=bpy.context.scene;sc.camera=cam;sc.render.resolution_x=1600;sc.render.resolution_y=round(1600/shot['aspect']);sc.render.resolution_percentage=100
bpy.context.view_layer.update();rows={}
for name,y,z,dy,dz in [('frame',.018,.041,.002,.002),('barrel',.140,.063,.004,.0015),('rubber_texture',-.027,-.032,.003,.003),('rubber_hand',-.013,.019,.002,.002),('sight',.0280,.081,.0003,.0005)]:
 hits=[];pixels=[]
 for yy,zz in [(y-dy,z-dz),(y+dy,z-dz),(y+dy,z+dz),(y-dy,z+dz)]:
  hit=tree.ray_cast(Vector((-.08,yy,zz)),Vector((1,0,0)),.16)
  assert hit[0] is not None,(name,yy,zz)
  hits.append(list(hit[0]));uv=world_to_camera_view(sc,cam,hit[0]);pixels.append([uv.x,1-uv.y])
 rows[name]=dict(actual_surface_points_m=hits,normalized_polygon=pixels)
Path(a.out).write_text(json.dumps(dict(source=str(source),camera='used_photo',patches=rows),indent=2));print('RAY-HIT VALUE LOCI',a.out)
