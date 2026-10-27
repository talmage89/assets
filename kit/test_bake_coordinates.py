"""Blender regression: prepared source joining must reject hidden frame reads."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
from kit.bake import require_attribute_coordinates
m=bpy.data.materials.new('Coordinate guard');m.use_nodes=True;nt=m.node_tree
noise=nt.nodes.new('ShaderNodeTexNoise');surface=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');nt.links.new(noise.outputs['Fac'],surface.inputs['Roughness'])
def rejected(fragment):
 try:require_attribute_coordinates([m])
 except ValueError as e:assert fragment in str(e)
 else:raise AssertionError('Unsafe coordinate source was accepted')
rejected('implicit texture coordinates')
attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='Prepared position';nt.links.new(attr.outputs['Vector'],noise.inputs['Vector']);require_attribute_coordinates([m])
# A live coordinate lookup inside a nested node group must also be rejected.
g=bpy.data.node_groups.new('Nested coordinate frame','ShaderNodeTree');g.interface.new_socket('Vector',in_out='OUTPUT',socket_type='NodeSocketVector')
output=g.nodes.new('NodeGroupOutput');tc=g.nodes.new('ShaderNodeTexCoord');g.links.new(tc.outputs['Object'],output.inputs[0]);group=nt.nodes.new('ShaderNodeGroup');group.node_tree=g;nt.links.new(group.outputs[0],noise.inputs['Vector']);rejected('prepared coordinate attributes')
nt.links.new(attr.outputs['Vector'],noise.inputs['Vector']);nt.nodes.remove(group);require_attribute_coordinates([m])
print('BAKE COORDINATE PASS: implicit and nested frame reads rejected; attribute source accepted')
