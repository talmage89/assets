"""Replace only bake-source ammunition with regular, dense source revolutions."""
import bpy
from guns.common.ammo9_bake import parts
from build import HEADS

def replace():
 materials={m.name.removeprefix('CP_').split('.')[0]:m
            for ob in bpy.context.scene.objects if ob.type=='MESH'
            for m in ob.data.materials if m and m.name.startswith('CP_')}
 for name,bone in [('Magazine_TopRound','TopRound'),('Magazine_SecondRound','SecondRound'),
                   ('Magazine_ThirdRound','ThirdRound'),('ChamberRound','ChamberRound')]:
  for dense in parts(name,HEADS[bone],materials=materials,bone=bone):
   target=bpy.data.objects[dense['low_target']];target.data=dense.data.copy()
   target.vertex_groups.clear();group=target.vertex_groups.new(name=bone)
   group.add(list(range(len(target.data.vertices))),1,'REPLACE')
   bpy.data.objects.remove(dense,do_unlink=True)
 for name,fired in [('Cartridge_Proof',False),('Case_Proof',True)]:
  target=bpy.data.objects[name];dense=parts(name,(0,0,0),materials=materials,fired=fired)
  bpy.ops.object.select_all(action='DESELECT')
  for ob in dense:ob.select_set(True)
  bpy.context.view_layer.objects.active=dense[0];bpy.ops.object.join()
  joined=bpy.context.object;target.data=joined.data.copy();bpy.data.objects.remove(joined,do_unlink=True)
