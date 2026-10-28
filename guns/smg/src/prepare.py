"""Pack the accepted parts and two ammunition templates through kit.finalize."""
import sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,model as M,finalize
out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/smg.blend'))
arm=bpy.data.objects['SMGArmature'];W.pose(arm,None,0);arm['delivery_variant']='smg'
for ob in list(bpy.context.scene.objects):
 if ob.get('bake_only'):bpy.data.objects.remove(ob,do_unlink=True)
 elif ob.name.startswith('Socket_'):ob['delivery_variant']='smg'
for name,x in [('cartridge',.4),('case',.5)]:
 original=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'build'/(name+'.glb')))
 ob=next(o for o in bpy.data.objects if o not in original and o.type=='MESH');ob.name=name.title()+'_Proof'
 if 'bone' in ob:del ob['bone']
 ob.data.transform(Matrix.Translation((x,0,0)))
 pivot=M.pivot(name.title()+'Root',(x,0,0));pivot['static_root']=True
 pivot['delivery_variant']=name;pivot['atlas_staging_offset']=(x,0,0)
 M.attach(ob,pivot,asset_set='SMG')
# Remove only microscopic collapsed Boolean edges from the bake target.
# The accepted source stays unchanged; retain its corner normal field.
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 field=ob.data.attributes.new('Delivery normals','FLOAT_VECTOR','CORNER')
 for row,n in zip(field.data,ob.data.corner_normals):row.vector=n.vector
 bm=bmesh.new();bm.from_mesh(ob.data)
 bmesh.ops.dissolve_degenerate(bm,dist=.00001 if ob.name.startswith('Grip_TexturePanel') else .000002,edges=list(bm.edges))
 bm.to_mesh(ob.data);bm.free()
 ob.data.normals_split_custom_set([row.vector[:] for row in ob.data.attributes['Delivery normals'].data])
 ob.data.attributes.remove(ob.data.attributes['Delivery normals'])
unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
regions={'smg':(.01,.01,.77,.99),'magazine':(.79,.24,.99,.99),
 'cartridge':(.79,.01,.885,.22),'case':(.90,.01,.99,.22)}
def group(o):
 if o.name in ('Cartridge_Proof','Case_Proof'):return o.name.split('_')[0].lower()
 return 'magazine' if o.get('bone') in ('Magazine','Follower','TopRound','SecondRound','ThirdRound') else 'smg'
master=[]
for name,rect in regions.items():
 bpy.ops.wm.open_mainfile(filepath=str(unpacked))
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and group(ob)!=name:bpy.data.objects.remove(ob,do_unlink=True)
 src=out/(name+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
 cfg=out/(name+'-uv.py');cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.001\nUV_PACK_SHAPE="AABB"\nUV_SMART_ASPECT=False\nUV_SMART_ANGLE=30\nUV_PRIORITY={"Receiver_Shell":1.5,"Cocking_Tube":1.4,"Grip_Texture":1.6,"Lower_Mold":1.25,"Stock_Mold":.75,"Bolt_":.8,"Magazine_Body":1.4}\n')
 dst=out/(name+'-uv.blend')
 sys.argv=['blender','--','--source',str(src),'--config',str(cfg),'--out',str(dst),'--report',str(out/(name+'-uv.json')),'--size','2048','--target-density','100000','--margin','.0015']
 try:finalize.main()
 except RuntimeError:
  from kit.uv import signed_area
  for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.uv_layers]:
   layer=ob.data.uv_layers.active
   for tri in ob.data.loop_triangles:
    area=abs(signed_area([layer.data[i].uv for i in tri.loops]))
    if area<1e-12:print('UV_TINY',ob.name,tri.polygon_index,area,tri.area,flush=True)
  raise
 master.append((dst,[(o.name,o.data.name) for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]))
bpy.ops.wm.open_mainfile(filepath=str(unpacked))
for path,mapping in master:
 with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.meshes=[mesh for name,mesh in mapping]
 for (name,_),mesh in zip(mapping,dst.meshes):bpy.data.objects[name].data=mesh
# Reseed only opposing/tangent corner normals introduced by UV edit operations.
repairs={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
 ns=[n.vector.copy() for n in ob.data.corner_normals];count=0
 for f in ob.data.polygons:
  for i in f.loop_indices:
   if ns[i].dot(f.normal)<.05:ns[i]=f.normal.copy();count+=1
 if count:ob.data.normals_split_custom_set(ns);repairs[ob.name]=count
bpy.context.scene['delivery_normal_repairs']=str(repairs)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
