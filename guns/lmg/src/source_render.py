import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import final_shots as shots,interface
from guns.common.render import main
shots.FINAL_STAGE=False
shots.RENDER_STAGE="Dense original procedural source / comparison only"
base_configure=shots.configure_scene
def source_configure(scene,source):
 import bpy
 from mathutils import Matrix
 arm=bpy.data.objects['HarrowArmature']
 from kit import weapon as W
 W.pose(arm,None,0)
 for kind,count in [('Round',17),('Link',16)]:
  template=bpy.data.objects['Belt_'+kind+'_00']
  for i in range(1,count):
   ob=template.copy();ob.data=template.data;ob.name=f'Belt_{kind}_{i:02d}'
   scene.collection.objects.link(ob);ob.parent_bone=f'Belt{kind}{i:02d}';ob['bone']=ob.parent_bone
   bpy.context.view_layer.update();ob.matrix_world=Matrix.Identity(4)
 base_configure(scene,source)
shots.configure_scene=source_configure
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
