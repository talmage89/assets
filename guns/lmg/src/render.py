import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import shots,interface
from guns.common.render import main
if __name__=='__main__':
 from kit import weapon_presentation as P
 from mathutils import Matrix
 import bpy
 original=P.pose
 def layered(arm,clip,frame,**kw):
  original(arm,clip,frame,**kw)
  # Compose imported clip matrices. This preserves glTF bone-axis conversion.
  selected=getattr(shots,'ACTIVE_LAYERS',{})
  if selected:
   keep={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
   for bone,(action,f) in selected.items():
    original(arm,action,f,**kw);keep[bone]=arm.pose.bones[bone].matrix_basis.copy()
   arm.animation_data.action=None
   for name,matrix in keep.items():arm.pose.bones[name].matrix_basis=matrix
   bpy.context.view_layer.update()
 P.pose=layered
 main(shots,interface)
