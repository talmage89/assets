"""Lot-owned fleet variation; native paint-coverage decode and immutable cars.

Five canonical colors come from each car's extras. Three restrained optional
factory tints extend that same coverage interface for the requested period mix.
Weights are an authored 1995–2015 neighborhood mix, not survey statistics.
"""
import json,random

COLORS=dict(Oxblood=(.19,.018,.012),Pine=(.035,.085,.045),Sand=(.31,.25,.16))
MIX=('Aluminum',)*18+('Graphite',)*19+('Carbon',)*17+('Porcelain',)*18+('Atlantic',)*14+('Oxblood',)*8+('Pine',)*3+('Sand',)*3


def selection(seed,number,slot=0):
    r=random.Random(seed*100003+number*397+slot*1301)
    # Three bodies repeat across a whole park, but neighboring drives cycle
    # bodies and use independently seeded paint, never one repeated fleet.
    return (number+slot+seed)%3,r.choice(MIX)


def paint(lib,root,preset):
    found=set()
    for ob in root.children_recursive:
        if ob.type!='MESH':continue
        for slot in ob.material_slots:
            original=slot.material
            if not original or original.get('paint_decode')!='reference_plus_coverage_delta':continue
            colors=dict(json.loads(original['paint_colors']),**COLORS)
            key=('park paint',original.name,preset)
            if key not in lib.paint:
                ma=original.copy();ma.name='Park factory '+preset+' '+original.name;nt=ma.node_tree
                bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
                tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
                delta=nt.nodes.new('ShaderNodeCombineXYZ')
                for socket,a,b in zip(delta.inputs,colors[preset],original['paint_reference_color']):socket.default_value=a-b
                scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE'
                nt.links.new(delta.outputs[0],scale.inputs[0]);nt.links.new(tex.outputs['Alpha'],scale.inputs['Scale'])
                add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD'
                nt.links.new(tex.outputs['Color'],add.inputs[0]);nt.links.new(scale.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Base Color'])
                bs.inputs['Metallic'].default_value=json.loads(original.get('paint_metallic','{}')).get(preset,.10)
                ma['park_factory_color']=preset;lib.paint[key]=ma
            slot.link='OBJECT';slot.material=lib.paint[key];found.add(preset)
    assert found,('Native paint coverage missing',root.name)
    root['factory_color']=preset
    return preset
