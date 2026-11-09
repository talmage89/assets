"""Opt-in transfer of reference-plus-coverage factory paint from deliveries.

The proxy stores two independent linear derivatives: RGB tint coverage and
clean metallic coverage. Ordinary PBR fields remain the reference fallback.
No source image or material is rewritten. Runtime uniforms retain the delivered
decoder's node names; the family helper can delegate its proxy installation here.
"""
import json
import bpy

DECODE = 'reference_plus_coverage_delta'


def image_node(material, role):
    return next(n for n in material.node_tree.nodes
                if n.type == 'TEX_IMAGE' and n.image and role in n.image.name)


def install_paint(m):
    nt = m.node_tree
    if nt.nodes.get('Factory delta'):
        return
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    base = image_node(m, 'BaseColor')
    orm = image_node(m, 'ORM')
    split = nt.nodes.new('ShaderNodeSeparateColor')
    nt.links.new(orm.outputs['Color'], split.inputs[0])
    proxy = bool(m.get('lod_factory_coverage'))
    if proxy:
        coverage = image_node(m, 'FactoryCoverage')
        fields = nt.nodes.new('ShaderNodeSeparateColor')
        nt.links.new(coverage.outputs['Color'], fields.inputs[0])
        paint, metal = fields.outputs['Green'], fields.outputs['Blue']
    else:
        paint, metal = base.outputs['Alpha'], split.outputs['Blue']
    delta = nt.nodes.new('ShaderNodeCombineXYZ'); delta.name = 'Factory delta'
    scale = nt.nodes.new('ShaderNodeVectorMath'); scale.operation = 'SCALE'
    nt.links.new(delta.outputs[0], scale.inputs[0]); nt.links.new(paint, scale.inputs['Scale'])
    add = nt.nodes.new('ShaderNodeVectorMath'); add.operation = 'ADD'
    nt.links.new(base.outputs['Color'], add.inputs[0]); nt.links.new(scale.outputs[0], add.inputs[1])
    clamp = nt.nodes.new('ShaderNodeVectorMath'); clamp.operation = 'MAXIMUM'
    clamp.inputs[1].default_value = (0, 0, 0)
    nt.links.new(add.outputs[0], clamp.inputs[0]); nt.links.new(clamp.outputs[0], bs.inputs['Base Color'])
    multiply = nt.nodes.new('ShaderNodeMath'); multiply.operation = 'MULTIPLY'
    multiply.name = 'Factory metallic'; nt.links.new(metal, multiply.inputs[0])
    result = multiply.outputs[0]
    if proxy:
        # Preserve dielectric dirt and all nonpaint metallic response.
        residual = nt.nodes.new('ShaderNodeMath'); residual.operation = 'MULTIPLY_ADD'
        nt.links.new(metal, residual.inputs[0])
        residual.inputs[1].default_value = -float(m['lod_factory_reference_metallic'])
        nt.links.new(split.outputs['Blue'], residual.inputs[2])
        total = nt.nodes.new('ShaderNodeMath'); total.operation = 'ADD'
        nt.links.new(result, total.inputs[0]); nt.links.new(residual.outputs[0], total.inputs[1])
        result = total.outputs[0]
    else:
        for key, a, b in [('Coat Weight', .90, .10), ('Coat Roughness', -.35, .385)]:
            value = nt.nodes.new('ShaderNodeMath'); value.operation = 'MULTIPLY_ADD'
            value.inputs[1].default_value = a; value.inputs[2].default_value = b
            nt.links.new(paint, value.inputs[0]); nt.links.new(value.outputs[0], bs.inputs[key])
        for link in list(bs.inputs['Coat Normal'].links): nt.links.remove(link)
    nt.links.new(result, bs.inputs['Metallic'])
    # Named source sockets are consumed only by the opt-in atlas route.
    marker = nt.nodes.new('ShaderNodeCombineColor'); marker.name = 'Factory coverage fields'
    nt.links.new(paint, marker.inputs[0]); nt.links.new(metal, marker.inputs[1])
    marker.inputs[2].default_value = 0


def apply(preset=None, lights=True):
    """Restore the documented delivery decode in a temporary imported scene."""
    paints = [m for m in bpy.data.materials if m.get('paint_decode') == DECODE]
    if len(paints) != 1: raise ValueError('Factory adapter requires exactly one paint contract')
    m = paints[0]; install_paint(m)
    colors, metallic = json.loads(m['paint_colors']), json.loads(m['paint_metallic'])
    if preset is None:
        preset=next(k for k,v in colors.items() if list(v)==list(m['paint_reference_color']))
    for socket, value, reference in zip(m.node_tree.nodes['Factory delta'].inputs,
                                      colors[preset], m['paint_reference_color']):
        socket.default_value = value - reference
    m.node_tree.nodes['Factory metallic'].inputs[1].default_value = metallic[preset]
    for lamp in bpy.data.materials:
        if not lamp.get('lamp_strength'): continue
        nt = lamp.node_tree; bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
        if lamp.get('lamp_alpha_semantic') == 'emission_strength_over_80':
            base = image_node(lamp, 'BaseColor')
            power = nt.nodes.get('Lamp power')
            if power is None:
                power = nt.nodes.new('ShaderNodeMath'); power.name = 'Lamp power'
                power.operation = 'MULTIPLY'; nt.links.new(base.outputs['Alpha'], power.inputs[0])
                nt.links.new(power.outputs[0], bs.inputs['Emission Strength'])
            power.inputs[1].default_value = lamp['lamp_strength'] if lights else 0
            if lamp.get('emission_color_override') and not nt.nodes.get('Factory lamp color'):
                policy = json.loads(lamp['emission_color_override'])
                low = nt.nodes.new('ShaderNodeMath'); low.operation = 'GREATER_THAN'
                high = nt.nodes.new('ShaderNodeMath'); high.operation = 'LESS_THAN'
                for node, key in [(low, 'alpha_min'), (high, 'alpha_max')]:
                    node.inputs[1].default_value = policy[key]
                    nt.links.new(base.outputs['Alpha'], node.inputs[0])
                select = nt.nodes.new('ShaderNodeMath'); select.operation = 'MULTIPLY'
                nt.links.new(low.outputs[0], select.inputs[0]); nt.links.new(high.outputs[0], select.inputs[1])
                mix = nt.nodes.new('ShaderNodeMixRGB'); mix.name = 'Factory lamp color'
                mix.inputs[2].default_value = (*policy['linear_rgb'], 1)
                nt.links.new(select.outputs[0], mix.inputs[0]); nt.links.new(base.outputs['Color'], mix.inputs[1])
                nt.links.new(mix.outputs[0], bs.inputs['Emission Color'])
        else:
            bs.inputs['Emission Strength'].default_value = lamp['lamp_strength'] if lights else 0
    return m


def coverage_socket(nt):
    node = nt.nodes.get('Factory coverage fields')
    return node.outputs[0] if node else None
