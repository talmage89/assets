"""Car-family BaseColor alpha decode; no source shaders or extra images.

Uniform controls select red, amber, headlight, dome and strobe classes. A stock
glTF viewer retains the unlit fallback. The baked alpha values are power/80.
"""
import bpy
CLASSES={'red':14,'amber':10,'headlight':5,'dome':2,'strobe':20}
def apply(**states):
    for m in bpy.data.materials:
        if 'Lamps' not in m.name:continue
        nt=m.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
        if not nt.nodes.get('Bus red state'):
            tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
            total=None
            for name,power in CLASSES.items():
                gate=nt.nodes.new('ShaderNodeMath');gate.operation='COMPARE';gate.inputs[1].default_value=power/80;gate.inputs[2].default_value=.011
                nt.links.new(tex.outputs['Alpha'],gate.inputs[0]);control=nt.nodes.new('ShaderNodeValue');control.name='Bus '+name+' state'
                mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';nt.links.new(gate.outputs[0],mul.inputs[0]);nt.links.new(control.outputs[0],mul.inputs[1])
                if total is None:total=mul.outputs[0]
                else:add=nt.nodes.new('ShaderNodeMath');add.operation='ADD';nt.links.new(total,add.inputs[0]);nt.links.new(mul.outputs[0],add.inputs[1]);total=add.outputs[0]
            nt.links.new(total,bs.inputs['Emission Strength']);nt.links.new(tex.outputs['Color'],bs.inputs['Emission Color'])
        for name,power in CLASSES.items():nt.nodes['Bus '+name+' state'].outputs[0].default_value=power if states.get(name,False) else 0
