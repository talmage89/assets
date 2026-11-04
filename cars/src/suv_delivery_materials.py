"""Family atlas decoder plus the X220 dark-substrate projector's lit color."""
import bpy,json
import delivery_materials as family


def install():
    family.install()
    for material in bpy.data.materials:
        if material.get('lamp_alpha_semantic')!='emission_strength_over_80':continue
        policy=json.loads(material['emission_color_override'])
        nt=material.node_tree
        if nt.nodes.get('X220 projector emission'):continue
        image=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
        surface=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
        low=nt.nodes.new('ShaderNodeMath');low.operation='GREATER_THAN';low.inputs[1].default_value=policy['alpha_min']
        high=nt.nodes.new('ShaderNodeMath');high.operation='LESS_THAN';high.inputs[1].default_value=policy['alpha_max']
        for n in [low,high]:nt.links.new(image.outputs['Alpha'],n.inputs[0])
        selection=nt.nodes.new('ShaderNodeMath');selection.operation='MULTIPLY'
        nt.links.new(low.outputs[0],selection.inputs[0]);nt.links.new(high.outputs[0],selection.inputs[1])
        color=nt.nodes.new('ShaderNodeMixRGB');color.name='X220 projector emission'
        color.inputs[2].default_value=(*policy['linear_rgb'],1)
        nt.links.new(selection.outputs[0],color.inputs[0]);nt.links.new(image.outputs['Color'],color.inputs[1])
        nt.links.new(color.outputs[0],surface.inputs['Emission Color'])


def apply(preset='Atlantic',lights=False):
    install();return family.apply(preset,lights)


def eevee_glass():return family.eevee_glass()
