"""Actual triangle-ray patches for the delivered paint, lower and magazine."""
import sys,json
import numpy as np
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import motion,weapon as W
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'));W.pose(bpy.data.objects['SMGArmature'],None,0)
rows={}
for sign,label in [(1,'right_photo'),(-1,'left_photo')]:
 patches={'paint':('Receiver_Shell',[(-.018,.094),(.025,.094),(.025,.099),(-.018,.099)]),
 'paint_upper_flank':('Receiver_Shell',[(.010,.114),(.140,.114),(.140,.124),(.010,.124)]),
 'polymer':('Lower_Mold',[(.037,.054),(.060,.054),(.060,.065),(.037,.065)]),
 'polymer_grip':('Lower_Mold',[(-.033,-.039),(-.012,-.039),(-.012,-.015),(-.033,-.015)]),
 'polymer_stock':('Stock_Mold',[(-.21,.075),(-.17,.075),(-.17,.090),(-.21,.090)]),
 'polymer_handguard':('Handguard_Mold',[(.25,.084),(.28,.084),(.28,.096),(.25,.096)]),
 'magazine':('Magazine_Body',[])}
 for s,offset in [(70,-.003),(100,-.003),(100,.003),(70,.003)]:
  y=.143+.12*s/1000+1.6*max(0,s/1000-.020)**2+offset;patches['magazine'][1].append((y,.080-s/1000))
 rows[label]={}
 for key,(part,points) in patches.items():
  tree=motion.surface(bpy.data.objects[part])['tree'];hits=[]
  for y,z in points:
   hit=tree.ray_cast(Vector((sign*.1,y,z)),Vector((-sign,0,0)),.2);assert hit[0] is not None,(part,y,z)
   hits.append(list(hit[0]))
  rows[label][key]=dict(part=part,points_m=hits,method='first hit on actual finalized triangles from the corresponding exterior side')
(BASE/'build/value-loci.json').write_text(json.dumps(rows,indent=2))
# Read-only semantic surfaces for whole-region hero medians. Final layout
# fingerprints independently establish that these triangles equal delivery.
names=[];triangles=[];uvs=[];parts=[]
for ob in sorted(bpy.context.scene.objects,key=lambda o:o.name):
 if ob.type!='MESH' or not ob.get('asset_set') or ob.get('bake_only') or ob.name in ('Cartridge_Proof','Case_Proof'):continue
 evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
 index=len(names);names.append(ob.name);layer=mesh.uv_layers.active
 for triangle in mesh.loop_triangles:
  triangles.append([list(evaluated.matrix_world@mesh.vertices[i].co) for i in triangle.vertices])
  uvs.append([list(layer.data[i].uv) for i in triangle.loops]);parts.append(index)
 evaluated.to_mesh_clear()
np.savez_compressed(BASE/'build/value-surfaces.npz',names=names,triangles=np.array(triangles),uvs=np.array(uvs),parts=parts)
