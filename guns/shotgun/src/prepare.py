"""Pack the accepted gun and exterior shells with the kit atlas finalizer.

Keep named parts for independent construction tests. Export alone consolidates
the skin. Separate reserved shell regions use the same three-map allocation.
"""
import sys,json
from pathlib import Path
import bpy,bmesh
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit import weapon as W,model as G,finalize

out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/shotgun.blend'))
arm=bpy.data.objects['ShotgunArmature'];W.pose(arm,None,0)
for ob in list(bpy.context.scene.objects):
 if ob.get('bake_only'):bpy.data.objects.remove(ob,do_unlink=True)
arm['delivery_variant']='shotgun'
for ob in bpy.context.scene.objects:
 if ob.name.startswith('Socket_'):ob['delivery_variant']='shotgun'
for name,offset in [('shell',.13),('hull',.19)]:
 original=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'build'/(name+'.glb')))
 mesh=next(o for o in bpy.data.objects if o not in original and o.type=='MESH')
 mesh.name='Standalone_'+name;mesh.location.x=offset
 root=G.pivot(name+'Root',(offset,0,0));root['static_root']=True
 root['delivery_variant']=name;root['atlas_staging_offset']=(offset,0,0)
 G.attach(mesh,root,asset_set='Shotgun')
# Boolean intersections retain sub-micrometer slivers in the inspection mesh.
# Dissolve only edges below 2 micrometers; retain authored corner normals.
cleanup={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 if ob.name not in ('Receiver','Bolt_Body'):continue
 attr=ob.data.attributes.new('Delivery normals','FLOAT_VECTOR','CORNER')
 for row,normal in zip(attr.data,ob.data.corner_normals):row.vector=normal.vector
 before=len(ob.data.polygons)
 bm=bmesh.new();bm.from_mesh(ob.data)
 bmesh.ops.dissolve_degenerate(bm,dist=.000002,edges=list(bm.edges))
 bm.to_mesh(ob.data);bm.free()
 ob.data.normals_split_custom_set([r.vector[:] for r in ob.data.attributes['Delivery normals'].data])
 ob.data.attributes.remove(ob.data.attributes['Delivery normals'])
 cleanup[ob.name]=dict(before=before,after=len(ob.data.polygons))
(out/'cleanup.json').write_text(json.dumps(cleanup,indent=2))
unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
regions={'shotgun':(.01,.01,.88,.99),'shell':(.90,.02,.99,.45),'hull':(.90,.50,.99,.98)}
def group(ob):
 return ob.name.removeprefix('Standalone_') if ob.name.startswith('Standalone_') else 'shotgun'
master=[]
for name,rect in regions.items():
 bpy.ops.wm.open_mainfile(filepath=str(unpacked))
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and group(ob)!=name:bpy.data.objects.remove(ob,do_unlink=True)
 src=out/(name+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
 cfg=out/(name+'-uv.py')
 cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.005\nUV_PACK_SHAPE="AABB"\nUV_SMART_ANGLE=30\nUV_PRIORITY={"Receiver":1.30,"Stock":1.65,"Forend_Wood":1.75,"TubeShell":.35,"ChamberShell":.40,"CarrierShell":.8,"InsertShell":.8,"Barrel_Extension":.55,"Barrel":.80,"Magazine_Tube":.65,"Forend_Sleeve":.45,"Forend_Bearing":.50,"Magazine_Follower":.40}\n')
 dst=out/(name+'-uv.blend')
 sys.argv=['blender','--','--source',str(src),'--config',str(cfg),'--out',str(dst),
  '--report',str(out/(name+'-uv.json')),'--size','2048','--target-density','100000','--margin','.002']
 finalize.main()
 mapping=[(ob.name,ob.data.name) for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('asset_set')]
 master.append((dst,mapping))
bpy.ops.wm.open_mainfile(filepath=str(unpacked))
for path,mapping in master:
 with bpy.data.libraries.load(str(path),link=False) as (source,destination):destination.meshes=[mesh for ob,mesh in mapping]
 for (name,_),mesh in zip(mapping,destination.meshes):bpy.data.objects[name].data=mesh
# Reject invalid shading instead of concealing it with the tangent bake.
repairs={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
 normals=[n.vector.copy() for n in ob.data.corner_normals];count=0
 for face in ob.data.polygons:
  for i in face.loop_indices:
   if normals[i].dot(face.normal)<.03:normals[i]=face.normal.copy();count+=1
 if count:ob.data.normals_split_custom_set(normals);repairs[ob.name]=count
bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
(out/'normal-repairs.json').write_text(json.dumps(repairs,indent=2))
print('HEARTH DELIVERY PREPARED',flush=True)
