"""Explicit shader coordinates stay fixed while nested modules are isolated.

Run in a clean Blender; this does not bake, render or acquire the GPU.
"""
import sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kit import model as G,bake_groups
bpy.ops.wm.read_factory_settings(use_empty=True)
root=G.pivot('Module',(2,-3,.8));root.rotation_euler.z=.42
frame=G.pivot('Timber frame',(0,0,0));frame.parent=root;frame.location=(.3,.2,.4);frame.rotation_euler.y=.23
mat=bpy.data.materials.new('Explicit timber');mat.use_nodes=True
coord=mat.node_tree.nodes.new('ShaderNodeTexCoord');coord.object=frame
ob=G.box('Board',(.2,.1,.4),(.13,.02,1.8),mat,0);G.attach(ob,root,asset_set='Fixture')
bpy.context.view_layer.update();before=[frame.matrix_world.inverted()@ob.matrix_world@v.co for v in ob.data.vertices]
frames=bake_groups.referenced_frames([ob],['Module'])
world=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=world;ob.matrix_world.translation+=Vector((17.3,0,0))
bake_groups.translate_frames(frames,{'Module':Vector((17.3,0,0))});bpy.context.view_layer.update()
after=[frame.matrix_world.inverted()@ob.matrix_world@v.co for v in ob.data.vertices]
error=max((a-b).length for a,b in zip(before,after));assert error<5e-6,error
assert len(frames)==1
print('PASS: rotated/nested explicit timber coordinates preserved during module isolation; max error',error)
