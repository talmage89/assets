"""Maple-compatible entry point; oak adds a matte back to the shared shader."""
from kit.foliage import material as shared_material


def material(*args,**kwargs):
    mat=shared_material(*args,**kwargs)
    if not kwargs.get('name','').startswith('Pin oak'):return mat
    nt=mat.node_tree;n=nt.nodes;l=nt.links
    bs=n['Leaf reflective surface'];rough=bs.inputs['Roughness']
    front=rough.links[0].from_socket if rough.links else rough.default_value
    back=n.new('ShaderNodeMix');back.name='Matte leaf underside';back.data_type='FLOAT'
    geom=next(x for x in n if x.type=='NEW_GEOMETRY')
    l.new(geom.outputs['Backfacing'],back.inputs[0])
    if hasattr(front,'is_output'):
        minimum=n.new('ShaderNodeMath');minimum.operation='MAXIMUM';minimum.inputs[1].default_value=.48
        l.new(front,minimum.inputs[0]);l.new(minimum.outputs[0],back.inputs[2])
    else:back.inputs[2].default_value=front
    back.inputs[3].default_value=.76
    l.new(back.outputs[0],rough)
    trans=n['Thin leaf diffuse transmission'];incoming=trans.inputs['Color'].links[0].from_socket
    tint=n.new('ShaderNodeMixRGB');tint.name='Leaf transmission spectrum';tint.blend_type='MULTIPLY'
    tint.inputs[0].default_value=1;tint.inputs[2].default_value=(1.4,1.2,.7,1)
    l.new(incoming,tint.inputs[1]);l.new(tint.outputs[0],trans.inputs['Color'])
    return mat
