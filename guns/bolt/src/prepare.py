"""Prepare the accepted game mesh and one reserved atlas through kit.finalize.

Pack explicit rifle, two magazine panels and case rectangles through the established
finalizer, merge only generated mesh data, then use the kit baker/exporter.
"""
import sys
from pathlib import Path
import bpy,bmesh
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parent.parent;sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))
from kit import weapon as W,model as G,finalize
import geometry as trigger_geometry
from trigger import packing_proxy
from build import finish
out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/bolt.blend'));arm=bpy.data.objects['B24Armature'];W.pose(arm,None,0)
arm['delivery_variant']='bolt'
for ob in bpy.context.scene.objects:
 if ob.name.startswith('Socket_'):ob['delivery_variant']='bolt'
# Reserve the old packing input so every other part keeps its accepted UVs.
# The new blade gets its own previously empty strip between case and magazine.
shoe=bpy.data.objects['Trigger_Shoe'];blade=shoe.data.copy()
trigger_geometry.MAT['steel']=shoe.data.materials[0]
proxy=packing_proxy();finish(proxy);shoe.data=proxy.data
bpy.data.objects.remove(proxy,do_unlink=True)
blade_path=out/'trigger-blade.blend'
holder=bpy.data.objects.new('Trigger blade UV source',blade)
bpy.data.libraries.write(str(blade_path),{holder})
bpy.data.objects.remove(holder,do_unlink=True)
original=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'build/case.glb'))
case=[o for o in bpy.data.objects if o not in original and o.type=='MESH'][0]
case.name='Case_Proof';case.location.x=.3
if 'bone' in case:del case['bone']
root=G.pivot('CaseRoot',(.3,0,0));root['static_root']=True;root['delivery_variant']='case';root['atlas_staging_offset']=(.3,0,0)
G.attach(case,root,asset_set='B24')
# Remove microscopic collapsed Boolean edges from the delivery bake target.
# Carry the authored normal field through BMesh just as kit.finalize does.
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 saved=ob.data.attributes.new('Delivery normals','FLOAT_VECTOR','CORNER')
 for row,n in zip(saved.data,ob.data.corner_normals):row.vector=n.vector
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.dissolve_degenerate(bm,dist=.000002,edges=list(bm.edges));bm.to_mesh(ob.data);bm.free()
 ob.data.normals_split_custom_set([r.vector[:] for r in ob.data.attributes['Delivery normals'].data]);ob.data.attributes.remove(ob.data.attributes['Delivery normals'])
unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
# A guarded gap keeps the shell and other magazine charts in separate
# neighborhoods, each small enough for a lossless 1024 standalone subset.
regions={'bolt':(.01,.01,.79,.99),
         'magazine_shell':(.81,.20,.99,.67),
         'magazine_rest':(.81,.69,.99,.99),
         'case':(.81,.01,.99,.18)}
def group(o):
 if o.name.startswith('Case_Proof'):return 'case'
 if o.name=='Magazine_Shell':return 'magazine_shell'
 return 'magazine_rest' if o.get('bone') in ('Magazine','TopRound','ReserveRound','Follower') else 'bolt'
master=[]
def args(values):sys.argv=['blender','--',*map(str,values)]
for name,rect in regions.items():
 bpy.ops.wm.open_mainfile(filepath=str(unpacked))
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and group(ob)!=name:bpy.data.objects.remove(ob,do_unlink=True)
 src=out/(name+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
 cfg=out/(name+'-uv.py');cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.005\nUV_PACK_SHAPE="AABB"\nUV_SMART_ANGLE='+str(12 if name.startswith('magazine') else 30)+'\nUV_PRIORITY={"Stock_Mold":1.25,"Receiver":1.5,"Scope_Body":1.15,"Turret_":1.45,"Bolt_":1.25,"Barrel":.72,"Bipod_":.85,"Reticle_":2.0,"Lens_":.45}\n')
 dst=out/(name+'-uv.blend')
 args(['--source',src,'--config',cfg,'--out',dst,'--report',out/(name+'-uv.json'),'--size',2048,'--target-density',100000,'--margin',.002]);finalize.main()
 mapping=[(o.name,o.data.name) for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
 master.append((dst,mapping))
bpy.ops.wm.open_mainfile(filepath=str(unpacked))
for path,mapping in master:
 with bpy.data.libraries.load(str(path),link=False) as (source,destination):destination.meshes=[mesh for ob,mesh in mapping]
 for (name,_),mesh in zip(mapping,destination.meshes):bpy.data.objects[name].data=mesh
# Finalize only the corrected shoe; use the established unused atlas gap.
packed=out/'packed-before-trigger.blend';bpy.ops.wm.save_as_mainfile(filepath=str(packed))
with bpy.data.libraries.load(str(blade_path),link=False) as (source,destination):destination.objects=['Trigger blade UV source']
shoe=bpy.data.objects['Trigger_Shoe'];shoe.data=destination.objects[0].data
bpy.data.objects.remove(destination.objects[0],do_unlink=True)
for ob in list(bpy.context.scene.objects):
 if ob.type=='MESH' and ob!=shoe:bpy.data.objects.remove(ob,do_unlink=True)
src=out/'trigger-source.blend';bpy.ops.wm.save_as_mainfile(filepath=str(src))
cfg=out/'trigger-uv.py'
cfg.write_text('UV_ATLAS_RECT=(.81,.182,.99,.198)\nUV_MIN_COVERAGE=.00001\nUV_PACK_SHAPE="AABB"\nUV_SMART_ANGLE=45\n')
dst=out/'trigger-uv.blend'
args(['--source',src,'--config',cfg,'--out',dst,'--report',out/'trigger-uv.json','--size',2048,'--target-density',100000,'--margin',.002]);finalize.main()
mesh_name=bpy.data.objects['Trigger_Shoe'].data.name
bpy.ops.wm.open_mainfile(filepath=str(packed))
with bpy.data.libraries.load(str(dst),link=False) as (source,destination):destination.meshes=[mesh_name]
shoe=bpy.data.objects['Trigger_Shoe'];shoe.data=destination.meshes[0]
shoe.vertex_groups.clear();group=shoe.vertex_groups.new(name='Trigger');group.add(list(range(len(shoe.data.vertices))),1,'REPLACE')
# UV finalization re-encodes smoothing fans at a few narrow Boolean corners.
# Reseed only near-tangent/opposing corners on the actual finalized triangles,
# before baking, so the tangent normal map uses the same field as delivery.
normal_corner_repairs={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]:
 normals=[n.vector.copy() for n in ob.data.corner_normals];changed=0
 for face in ob.data.polygons:
  for index in face.loop_indices:
   if normals[index].dot(face.normal)<.06:
    normals[index]=face.normal.copy();changed+=1
 if changed:ob.data.normals_split_custom_set(normals);normal_corner_repairs[ob.name]=changed
low=out/'finalized.blend';bpy.ops.wm.save_as_mainfile(filepath=str(low))
print('B24 DELIVERY PREPARED',sum(len(f.vertices)-2 for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set') for f in o.data.polygons),'triangles',flush=True)
