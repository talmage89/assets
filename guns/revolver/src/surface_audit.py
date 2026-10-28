"""Actual exported ray/UV texels at wear sites, separate from image/light values."""
import json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.geometry import barycentric_transform
from mathutils.bvhtree import BVHTree
from PIL import Image
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V
arm=V.import_glb(BASE/'export/revolver.glb')
images={c:np.asarray(Image.open(BASE/'textures'/('T_MeridianSix_'+c+'.png')).convert('RGB')) for c in ('BaseColor','Normal','ORM')}
def surface():
 vertices=[];triangles=[];uvs=[];dg=bpy.context.evaluated_depsgraph_get()
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
  ev=ob.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();offset=len(vertices)
  vertices.extend(ev.matrix_world@v.co for v in mesh.vertices)
  for t in mesh.loop_triangles:
   triangles.append(tuple(offset+i for i in t.vertices));uvs.append([mesh.uv_layers.active.data[i].uv.copy() for i in t.loops])
  ev.to_mesh_clear()
 return BVHTree.FromPolygons(vertices,triangles,all_triangles=True),vertices,triangles,uvs
def sample(name,origin,direction,tree):
 bvh,vertices,triangles,uvs=tree;point,normal,index,distance=bvh.ray_cast(Vector(origin),Vector(direction),.2)
 assert point is not None,name
 vs=[vertices[i] for i in triangles[index]];ts=[Vector((v.x,v.y,0)) for v in uvs[index]]
 uv=barycentric_transform(point,*vs,*ts);px=min(2047,max(0,int(uv.x*2048)));py=min(2047,max(0,2047-int(uv.y*2048)))
 texels={c:a[py,px].tolist() for c,a in images.items()}
 return dict(point_m=list(point),normal=list(normal),uv=list(uv[:2]),pixel=[px,py],texels=texels)
W.pose(arm,'Idle',0);tree=surface();rows={}
for name,y in [('stop_track_dark',.04373),('stop_track_center',.044),('cylinder_unworn',.0460)]:rows[name]=sample(name,(.060,y,.0482),(-1,0,0),tree)
for name,y in [('muzzle_holster',.181),('barrel_satin',.145)]:rows[name]=sample(name,(.04,y,.061),(-1,0,0),tree)
rows['rubber_texture']=sample('rubber texture',(-.08,-.035,-.046),(1,0,0),tree)
rows['rubber_hand']=sample('rubber hand',(0,.04,-.022),(0,-1,0),tree)
# Near the accepted upper molding lip: steel must not project into rubber.
for name,y,z in [('rubber_lip_web',-.020,.038),('rubber_lip_side',-.024,.034)]:
 rows[name]=sample(name,(-.08,y,z),(1,0,0),tree)
W.pose(arm,'Reload',88);tree=surface()
xf=arm.matrix_world@arm.pose.bones['Cylinder'].matrix@arm.pose.bones['Cylinder'].bone.matrix_local.inverted()
for name,p in [('cylinder_carbon',(.006,.0922,.061)),('cylinder_clean_face',(.0085,.0922,.06292))]:
 rows[name]=sample(name,xf@Vector(p),xf.to_3x3()@Vector((0,-1,0)),tree)
rows['topstrap_carbon']=sample('topstrap carbon',(0,.081,.067),(0,0,1),tree)
for name,row in rows.items():
 rgb=np.array(row['texels']['BaseColor']);row['base_luma_byte']=float(rgb@np.array([.2126,.7152,.0722]))
 row['ao'],row['roughness'],row['metallic']=(np.array(row['texels']['ORM'])/255).tolist()
checks=dict(rubber_lip_finish=all(rows[k]['metallic']<.05 and rows[k]['base_luma_byte']<70 for k in ('rubber_lip_web','rubber_lip_side')),
 stop_track_contrast=rows['cylinder_unworn']['base_luma_byte']-rows['stop_track_dark']['base_luma_byte']>20,
 carbon_core=rows['cylinder_carbon']['metallic']<.5 and rows['cylinder_clean_face']['base_luma_byte']-rows['cylinder_carbon']['base_luma_byte']>35,
 rubber_hand_polish=rows['rubber_texture']['roughness']-rows['rubber_hand']['roughness']>.1,
 muzzle_polish=rows['barrel_satin']['roughness']-rows['muzzle_holster']['roughness']>.05)
result=dict(passed=all(checks.values()),scope='actual final GLB triangle ray hits and embedded-atlas UV locations; view visibility is judged separately in hero renders',checks=checks,samples=rows)
(BASE/'build/surface-audit.json').write_text(json.dumps(result,indent=2))
print('SHIPPING SURFACE TEXELS',checks,{n:(round(r['base_luma_byte'],1),round(r['roughness'],3),round(r['metallic'],3)) for n,r in rows.items()})
assert result['passed'],checks
