"""Canonical three-map export with per-surface dielectric reflection strength.

The kit already bakes arbitrary opaque BaseColor alpha. Link that data to
Principled specular through the inverse glTF factor conversion. Blender exports
KHR_materials_specular referencing the same image; OPAQUE ignores its alpha
for coverage. No additional image, material, geometry or animation is made.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from kit import export
original=export.atlas_material
def atlas_material(*args,**kwargs):
    material=original(*args,**kwargs);nt=material.node_tree;surface=nt.nodes['SURFACE']
    color=surface.inputs['Base Color'].links[0].from_node
    factor=nt.nodes.new('ShaderNodeMath');factor.operation='MULTIPLY';factor.inputs[1].default_value=.5
    factor.label='Opaque BaseColor alpha: glTF specular factor / 2'
    nt.links.new(color.outputs['Alpha'],factor.inputs[0]);nt.links.new(factor.outputs[0],surface.inputs['Specular IOR Level'])
    return material
export.atlas_material=atlas_material
if __name__=='__main__':export.main()
