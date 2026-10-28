"""UV preparation through kit.finalize; rigid ownership and named parts survive."""
import sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from kit import weapon as W,finalize
out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/revolver.blend'))
arm=bpy.data.objects['RevolverArmature'];W.pose(arm,None,0)
arm['delivery_variant']='revolver'
for ob in bpy.context.scene.objects:
 if ob.name.startswith('Socket_'):ob['delivery_variant']='revolver'
p=bpy.context.scene;p['stage']='UV preparation; complete staged revolver'
source=out/'unpacked.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
sys.argv=['blender','--','--source',str(source),'--out',str(out/'finalized.blend'),
 '--config',str(BASE/'src/config.py'),'--report',str(out/'uv.json'),
 '--size','2048','--target-density','100000','--margin','.0017']
finalize.main()
# Preserve usable winding at microscopic corners after smoothing-fan encoding.
repairs={}
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
 normals=[n.vector.copy() for n in ob.data.corner_normals];changed=0
 for face in ob.data.polygons:
  for index in face.loop_indices:
   if normals[index].dot(face.normal)<.06:normals[index]=face.normal.copy();changed+=1
 if changed:ob.data.normals_split_custom_set(normals);repairs[ob.name]=changed
bpy.context.scene['delivery_normal_corner_repairs']=str(repairs)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
