"""Replace the three reduced molds with their retained dense sources for review."""
import sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/smg.blend'))
for h in [o for o in bpy.context.scene.objects if o.get('bake_only') and o.get('low_target')]:
 ob=bpy.data.objects[h['low_target']];ob.data=h.data.copy();ob.vertex_groups.clear()
 vg=ob.vertex_groups.new(name='Root');vg.add(list(range(len(ob.data.vertices))),1,'REPLACE')
bpy.context.scene['stage']='dense mold inspection, constant materials, no bake'
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/sculpt.blend'))
