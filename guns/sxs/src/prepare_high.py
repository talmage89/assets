"""Put dense original carved cages on the same rigid rig for source comparison."""
import sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W,model as M
BASE=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/sxs.blend'))
arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
for high in [o for o in bpy.data.objects if o.get('bake_only') and o.get('low_target')]:
 low=bpy.data.objects[high['low_target']];bone=low['bone'];low.data=high.data.copy()
 for modifier in list(low.modifiers):low.modifiers.remove(modifier)
 # The archived cage was copied before the reduced mesh's shading pass.
 # Use continuous sculpt normals rather than the cage's inherited flat faces.
 M.smooth(low,45)
 if low.name=='Forend_Walnut':
  # Preserve the routed lower land after recomputing source smoothness too.
  normals=[n.vector.copy() for n in low.data.corner_normals]
  for face in low.data.polygons:
   if face.normal.z<-.985 and .205<face.center.y<.275 and face.center.z<.024:
    for index in face.loop_indices:normals[index]=face.normal.copy()
  low.data.normals_split_custom_set(normals)
 low.vertex_groups.clear();W.rigid_bind(low,arm,bone)
bpy.context.scene['stage']='Dense source comparison; original wood/control cages on the same visual rig'
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/sculpt.blend'))
