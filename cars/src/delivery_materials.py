"""Runtime factory factors for the baked GLB, with no source shader dependency.

The GLB's default RGB is Atlantic. Its neutral paint coverage is BaseColor A.
Changing a uniform factory factor adds A*(tint-reference) in linear light;
this is equivalent to tint*A + contamination and preserves colored deposits.
Only the three embedded images and material extras are used here.
"""
import json
import bpy


def paint_material():
    return next(m for m in bpy.data.materials if m.get('paint_decode')=='reference_plus_coverage_delta')


def colors():return json.loads(paint_material()['paint_colors'])


def install():
    m=paint_material();nt=m.node_tree
    if nt.nodes.get('Factory delta'):return
    bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');bs.name='SURFACE'
    tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    orm=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'ORM' in n.image.name)
    delta=nt.nodes.new('ShaderNodeCombineXYZ');delta.name='Factory delta'
    scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE'
    nt.links.new(delta.outputs[0],scale.inputs[0]);nt.links.new(tex.outputs['Alpha'],scale.inputs['Scale'])
    add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD'
    nt.links.new(tex.outputs['Color'],add.inputs[0]);nt.links.new(scale.outputs[0],add.inputs[1])
    nonnegative=nt.nodes.new('ShaderNodeVectorMath');nonnegative.operation='MAXIMUM';nonnegative.inputs[1].default_value=(0,0,0)
    nt.links.new(add.outputs[0],nonnegative.inputs[0]);nt.links.new(nonnegative.outputs[0],bs.inputs['Base Color'])
    split=nt.nodes.new('ShaderNodeSeparateColor');nt.links.new(orm.outputs[0],split.inputs[0])
    metal=nt.nodes.new('ShaderNodeMath');metal.name='Factory metallic';metal.operation='MULTIPLY'
    nt.links.new(split.outputs['Blue'],metal.inputs[0]);nt.links.new(metal.outputs[0],bs.inputs['Metallic'])
    for socket,a,b in [('Coat Weight',.90,.10),('Coat Roughness',-.35,.385)]:
        value=nt.nodes.new('ShaderNodeMath');value.operation='MULTIPLY_ADD';value.inputs[1].default_value=a;value.inputs[2].default_value=b
        nt.links.new(tex.outputs['Alpha'],value.inputs[0]);nt.links.new(value.outputs[0],bs.inputs[socket])
    # The coat remains smooth above the baked under-coat flake/micro-normal.
    for link in list(bs.inputs['Coat Normal'].links):nt.links.remove(link)
    m['vehicle_paint']=True
    for lamp in bpy.data.materials:
        if lamp.get('lamp_alpha_semantic')!='emission_strength_over_80':continue
        tree=lamp.node_tree;surface=next(n for n in tree.nodes if n.type=='BSDF_PRINCIPLED')
        image=next(n for n in tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
        power=tree.nodes.new('ShaderNodeMath');power.name='Lamp power';power.operation='MULTIPLY'
        tree.links.new(image.outputs['Alpha'],power.inputs[0]);power.inputs[1].default_value=0
        tree.links.new(power.outputs[0],surface.inputs['Emission Strength'])


def apply(preset='Atlantic',lights=False):
    install();m=paint_material();tint=colors()[preset];ref=list(m['paint_reference_color'])
    for socket,a,b in zip(m.node_tree.nodes['Factory delta'].inputs,tint,ref):socket.default_value=a-b
    m.node_tree.nodes['Factory metallic'].inputs[1].default_value=json.loads(m['paint_metallic'])[preset]
    m.diffuse_color=(*tint,1)
    for mat in bpy.data.materials:
        if mat.get('lamp_strength'):
            bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            power=mat.node_tree.nodes.get('Lamp power')
            if power:power.inputs[1].default_value=mat['lamp_strength'] if lights else 0
            else:bs.inputs['Emission Strength'].default_value=mat['lamp_strength'] if lights else 0
    return dict(preset=preset,linear_tint=tint,metallic=json.loads(m['paint_metallic'])[preset],
                method='shared baked RGB + coverage alpha * (factory tint - reference tint)',lights=lights)


def eevee_glass():
    """Thin-sheet Fresnel fallback for stacked panes in a screen-space renderer.

    Uses only the imported tint, roughness and normal textures. Eevee cannot
    follow the nested cover/projector refraction paths that Cycles follows.
    """
    for material in bpy.data.materials:
        if not material.use_nodes:continue
        tree=material.node_tree
        bs=next((n for n in tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs or bs.inputs['Transmission Weight'].default_value<=0:continue
        transparent=tree.nodes.new('ShaderNodeBsdfTransparent')
        tree.links.new(bs.inputs['Base Color'].links[0].from_socket,transparent.inputs['Color'])
        glossy=tree.nodes.new('ShaderNodeBsdfAnisotropic');glossy.inputs['Color'].default_value=(1,1,1,1)
        tree.links.new(bs.inputs['Roughness'].links[0].from_socket,glossy.inputs['Roughness'])
        fresnel=tree.nodes.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=bs.inputs['IOR'].default_value
        if bs.inputs['Normal'].is_linked:
            normal=bs.inputs['Normal'].links[0].from_socket
            tree.links.new(normal,glossy.inputs['Normal']);tree.links.new(normal,fresnel.inputs['Normal'])
        mix=tree.nodes.new('ShaderNodeMixShader');tree.links.new(fresnel.outputs[0],mix.inputs[0])
        tree.links.new(transparent.outputs[0],mix.inputs[1]);tree.links.new(glossy.outputs[0],mix.inputs[2])
        output=next(n for n in tree.nodes if n.type=='OUTPUT_MATERIAL');tree.links.new(mix.outputs[0],output.inputs['Surface'])
        material.surface_render_method='DITHERED';material.use_transparency_overlap=True;material.use_transparent_shadow=True
