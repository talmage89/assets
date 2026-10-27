"""One family foliage definition; species response lives in shared atlas tiles."""
from kit import foliage


def foliage_material(images):
    mat=foliage.material(
        images['BaseColor'], images['Normal'], images['ORM'],
        name='Shrubs foliage and sepals', roughness=.30, specular=.12,
        transmission=.12, normal_strength=1.0,
        back_multiplier=(1.18,1.14,1.18,1), back_saturation=.68,
        edge_fade=(.10,.26))

    # True hydrangea leaf backs are paler and matte; atlas coordinates restrict
    # this response to broad blades/core sprays. Accepted boxwood tiles are zero.
    n=mat.node_tree.nodes;l=mat.node_tree.links
    uv=n.new('ShaderNodeTexCoord');split=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],split.inputs[0])
    def compare(socket,operation,value):
        node=n.new('ShaderNodeMath');node.operation=operation;node.inputs[1].default_value=value;l.new(socket,node.inputs[0]);return node.outputs[0]
    def mul(a,b):
        node=n.new('ShaderNodeMath');node.operation='MULTIPLY';l.new(a,node.inputs[0]);l.new(b,node.inputs[1]);return node.outputs[0]
    mask=mul(compare(split.outputs['X'],'GREATER_THAN',.2499),compare(split.outputs['X'],'LESS_THAN',.7501))
    mask=mul(mask,compare(split.outputs['Y'],'GREATER_THAN',.4999));mask=mul(mask,compare(split.outputs['Y'],'LESS_THAN',.7501))
    geom=next(node for node in n if node.type=='NEW_GEOMETRY');mask=mul(mask,geom.outputs['Backfacing'])
    bs=n['Leaf reflective surface'];original=bs.inputs['Base Color'].links[0].from_socket
    pale=n.new('ShaderNodeHueSaturation');pale.inputs['Saturation'].default_value=.72;pale.inputs['Value'].default_value=1.32;l.new(original,pale.inputs['Color'])
    tint=n.new('ShaderNodeMixRGB');l.new(mask,tint.inputs[0]);l.new(original,tint.inputs[1]);l.new(pale.outputs[0],tint.inputs[2]);l.new(tint.outputs[0],bs.inputs['Base Color'])
    rough=n.new('ShaderNodeMix');rough.data_type='FLOAT';rough.inputs[3].default_value=.88
    l.new(mask,rough.inputs[0]);l.new(bs.inputs['Roughness'].links[0].from_socket,rough.inputs[2]);l.new(rough.outputs[0],bs.inputs['Roughness'])
    return mat
