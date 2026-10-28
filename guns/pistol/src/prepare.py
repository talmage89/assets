"""Prepare the accepted game mesh and one reserved atlas through kit.finalize.

Pack explicit frame/slide, magazine and case rectangles through the established
finalizer, merge only generated mesh data, then use the kit baker/exporter.
"""
import sys
from pathlib import Path
import bpy,bmesh
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parent.parent;sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))
from kit import weapon as W,model as G,finalize
out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/pistol.blend'));arm=bpy.data.objects['PistolArmature'];W.pose(arm,None,0)
arm['delivery_variant']='pistol'
for ob in bpy.context.scene.objects:
 if ob.name.startswith('Socket_'):ob['delivery_variant']='pistol'
original=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'build/case.glb'))
case=[o for o in bpy.data.objects if o not in original and o.type=='MESH'][0]
case.name='Case_Proof';case.location.x=.3
root=G.pivot('CaseRoot',(.3,0,0));root['static_root']=True;root['delivery_variant']='case';root['atlas_staging_offset']=(.3,0,0)
G.attach(case,root,asset_set='Pistol')
# Remove microscopic collapsed Boolean edges from the delivery bake target.
# Carry the authored normal field through BMesh just as kit.finalize does.
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 saved=ob.data.attributes.new('Delivery normals','FLOAT_VECTOR','CORNER')
 for row,n in zip(saved.data,ob.data.corner_normals):row.vector=n.vector
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.dissolve_degenerate(bm,dist=.000002,edges=list(bm.edges));bm.to_mesh(ob.data);bm.free()
 ob.data.normals_split_custom_set([r.vector[:] for r in ob.data.attributes['Delivery normals'].data]);ob.data.attributes.remove(ob.data.attributes['Delivery normals'])
unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
regions={'pistol':(.02,.02,.755,.98),'magazine':(.78,.19,.98,.98),'case':(.78,.02,.98,.16)}
def group(o):
 if o.name.startswith('Case_Proof'):return 'case'
 return 'magazine' if o.get('bone') in ('Magazine','TopRound','ReserveRound','Follower') else 'pistol'
master=[]
def args(values):sys.argv=['blender','--',*map(str,values)]
for name,rect in regions.items():
 bpy.ops.wm.open_mainfile(filepath=str(unpacked))
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and group(ob)!=name:bpy.data.objects.remove(ob,do_unlink=True)
 src=out/(name+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
 cfg=out/(name+'-uv.py');cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.005\nUV_PACK_SHAPE="AABB"\nUV_SMART_ANGLE=40\nUV_PRIORITY={"Sight_":1.35,"Slide_":1.25,"Barrel_Hood":1.25,"Frame_Grip":1.1}\n')
 dst=out/(name+'-uv.blend')
 args(['--source',src,'--config',cfg,'--out',dst,'--report',out/(name+'-uv.json'),'--size',2048,'--target-density',100000,'--margin',.003]);finalize.main()
 mapping=[(o.name,o.data.name) for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
 master.append((dst,mapping))
bpy.ops.wm.open_mainfile(filepath=str(unpacked))
for path,mapping in master:
 with bpy.data.libraries.load(str(path),link=False) as (source,destination):destination.meshes=[mesh for ob,mesh in mapping]
 for (name,_),mesh in zip(mapping,destination.meshes):bpy.data.objects[name].data=mesh
# UV finalization re-encodes smoothing fans at a few narrow Boolean corners.
# Reseed only near-tangent/opposing corners on the actual finalized triangles,
# before baking, so the tangent normal map uses the same field as delivery.
normal_corner_repairs={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]:
 normals=[n.vector.copy() for n in ob.data.corner_normals];changed=0
 for face in ob.data.polygons:
  for index in face.loop_indices:
   if normals[index].dot(face.normal)<.20:
    normals[index]=face.normal.copy();changed+=1
 if changed:ob.data.normals_split_custom_set(normals);normal_corner_repairs[ob.name]=changed
low=out/'finalized.blend';bpy.ops.wm.save_as_mainfile(filepath=str(low))
print('C9 DELIVERY PREPARED',sum(len(f.vertices)-2 for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set') for f in o.data.polygons),'triangles',flush=True)
