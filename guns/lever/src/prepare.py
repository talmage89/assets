"""Kit atlas preparation, retaining named surfaces for construction audits."""
import sys,json
from pathlib import Path
import bpy,bmesh
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit import weapon as W,model as M,finalize
sys.path.insert(0,str(BASE/'src'))
from build import repair_float_normals

def main():
 out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/lever.blend'))
 arm=bpy.data.objects['LeverArmature'];W.pose(arm,None,0)
 arm['delivery_variant']='lever'
 for ob in bpy.context.scene.objects:
  if ob.name.startswith('Socket_'):ob['delivery_variant']='lever'
 for name,offset in [('cartridge',.13),('case',.19)]:
  previous=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'build'/(name+'.glb')))
  ob=next(o for o in bpy.data.objects if o not in previous and o.type=='MESH')
  ob.name='Standalone_'+name;ob.location.x=offset
  pivot=M.pivot(name+'Root',(offset,0,0));pivot['static_root']=True
  pivot['delivery_variant']=name;pivot['atlas_staging_offset']=(offset,0,0)
  M.attach(ob,pivot,asset_set='Lever')
 cleanup={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.name in ('Stock','Lever_Hub','Lever_FingerLoop','Upper_Tang')]:
  saved=ob.data.attributes.new('DeliveryNormal','FLOAT_VECTOR','CORNER')
  saved.data.foreach_set('vector',[v for row in ob.data.corner_normals for v in row.vector])
  before=len(ob.data.polygons);bm=bmesh.new();bm.from_mesh(ob.data)
  bmesh.ops.dissolve_degenerate(bm,dist=.000002,edges=list(bm.edges))
  bmesh.ops.triangulate(bm,faces=list(bm.faces),ngon_method='EAR_CLIP')
  collinear=0
  for _ in range(32):
   candidate=None
   for face in bm.faces:
    if len(face.verts)!=3 or face.calc_area()>1e-11:continue
    a,b=max(face.edges,key=lambda e:e.calc_length()).verts;c=next(v for v in face.verts if v not in (a,b))
    edge=b.co-a.co
    if not edge.length_squared:continue
    t=(c.co-a.co).dot(edge)/edge.length_squared
    if 0<t<1 and (c.co-a.co-t*edge).length<1e-7:candidate=c;break
   if candidate is None:break
   bmesh.ops.dissolve_verts(bm,verts=[candidate],use_face_split=False,use_boundary_tear=False)
   bmesh.ops.triangulate(bm,faces=list(bm.faces),ngon_method='EAR_CLIP');collinear+=1
  bm.to_mesh(ob.data);bm.free()
  ob.data.normals_split_custom_set([r.vector[:] for r in ob.data.attributes['DeliveryNormal'].data])
  ob.data.attributes.remove(ob.data.attributes['DeliveryNormal'])
  cleanup[ob.name]=dict(before=before,after=len(ob.data.polygons),dissolve_distance_m=.000002,collinear_vertices=collinear,maximum_collinear_offset_m=1e-7)
 (out/'cleanup.json').write_text(json.dumps(cleanup,indent=2))
 unpacked=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(unpacked))
 # Keep wood padding beside wood. Reserved carving regions prevent thin
 # stock-tip UV slivers from inheriting a polished-metal neighbor after 2K
 # filtering. These are regions of the same single shared PBR set.
 groups={'lever':(.01,.01,.88,.56),'stock':(.01,.58,.60,.99),
         'forend':(.62,.58,.88,.99),'cartridge':(.90,.02,.99,.47),'case':(.90,.52,.99,.98)};packed=[]
 def group(ob):
  if ob.name.startswith('Standalone_'):return ob.name.removeprefix('Standalone_')
  if ob.name in ('Stock','Forend'):return ob.name.lower()
  return 'lever'
 for name,rect in groups.items():
  bpy.ops.wm.open_mainfile(filepath=str(unpacked))
  for ob in list(bpy.context.scene.objects):
   if ob.type=='MESH' and group(ob)!=name:bpy.data.objects.remove(ob,do_unlink=True)
  source=out/(name+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(source))
  angle=12
  cfg=out/(name+'-uv.py');cfg.write_text('UV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.003\nUV_SMART_ANGLE='+str(angle)+'\nUV_PACK_SHAPE="AABB"\nUV_PRIORITY={"Receiver":1.45,"Stock":1.65,"Forend":1.65,"Lever_FingerLoop":1.4,"Rear_":1.5,"Hammer":1.5,"Tube_Round":.30,"Chamber_Live":.40,"Carrier_Live":.70,"Insert_Live":.8,"Barrel":.85,"Magazine_Tube":.55}\n')
  dest=out/(name+'-uv.blend')
  sys.argv=['blender','--','--source',str(source),'--config',str(cfg),'--out',str(dest),'--report',str(out/(name+'-uv.json')),'--size','2048','--target-density','100000','--margin','.0015']
  finalize.main()
  mapping=[(ob.name,ob.data.name) for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('asset_set')]
  packed.append((dest,mapping))
 bpy.ops.wm.open_mainfile(filepath=str(unpacked))
 for path,mapping in packed:
  with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.meshes=[mesh for name,mesh in mapping]
  for (name,_),mesh in zip(mapping,dst.meshes):bpy.data.objects[name].data=mesh
 repairs={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  count=repair_float_normals(ob)
  if count:repairs[ob.name]=count
 (out/'normal-repairs.json').write_text(json.dumps(repairs,indent=2))
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
 print('BRACKEN ATLAS PREPARED',flush=True)
if __name__=='__main__':main()
