"""Exterior bounds, eye sight ray and actual source surface gaps."""
import json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,assembly
from check import bounds
BASE=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/lmg.blend'));arm=bpy.data.objects['HarrowArmature'];W.pose(arm,'Idle',0)
rows={}
for n in ['Barrel_Exterior','Receiver_Sheet','Stock_Sculpt','PistolGrip_Sculpt','Handguard_Sculpt','FeedCover_Shell','Box_Shell','Trigger_Blade']:
 a,b=bounds(bpy.data.objects[n]);rows[n]=dict(bounds_mm=[(a*1000).tolist(),(b*1000).tolist()],dimensions_mm=((b-a)*1000).tolist())
eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
rear=bounds(bpy.data.objects['RearSight_Aperture']);post=bounds(bpy.data.objects['FrontSight_Post'])
# Ray visibility in actual geometry; aperture and top of front post are allowed.
from mathutils.bvhtree import BVHTree
hits=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or o.get('bake_only'):continue
 if o.name.startswith('Belt_'):continue
 dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
 vs=[ev.matrix_world@v.co for v in me.vertices];fs=[t.vertices for t in me.loop_triangles]
 if fs:
  hit=BVHTree.FromPolygons(vs,fs,all_triangles=True).ray_cast(eye,Vector((0,1,0)),.635)
  if hit[0] is not None:hits.append(dict(part=o.name,distance_mm=hit[3]*1000,hit_mm=[v*1000 for v in hit[0]]))
 ev.to_mesh_clear()
comb=bpy.data.objects['Stock_Sculpt'];vs,edges,tree=assembly.surface(comb)
cheek=tree.ray_cast(eye,Vector((0,0,-1)),.20)
result=dict(exterior=rows,eye_mm=[v*1000 for v in eye],
 eye_behind_actual_rear_rim_mm=(rear[0][1]-eye.y)*1000,
 eye_above_comb_mm=cheek[3]*1000 if cheek[0] is not None else None,
 sight_ray_hits=sorted(hits,key=lambda r:r['distance_mm']),
 limitation='Eye distance is an authored provisional estimate; available aiming candidates use optics or obscure the cheek. Not a measured iron-sight cheek-weld claim.')
(BASE/'build/measurements.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
