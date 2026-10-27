"""Two-sided thin-leaf checkpoint response with glancing-card rejection.

No emission or ambient light painted into the atlas. Diffuse transmission
responds to actual light on the other side. Engines must implement the same
thin-leaf and angle-coverage response on the eventual masked foliage material.
"""
import bpy


def material(image,normal_image=None,orm_image=None, *, name="Maple summer leaf alpha",
             roughness=.70, specular=.18, transmission=.40, normal_strength=.55,
             back_multiplier=(1.50,1.32,2.40,1), back_saturation=.52, edge_fade=(.13,.32)):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    mat.surface_render_method='DITHERED';mat.use_backface_culling=False
    nt=mat.node_tree;nt.nodes.clear();n=nt.nodes;l=nt.links
    tex=n.new('ShaderNodeTexImage');tex.image=image;tex.label='Original branchlets / sRGB albedo and alpha'
    geom=n.new('ShaderNodeNewGeometry')
    underside=n.new('ShaderNodeMixRGB');underside.blend_type='MIX'
    # Pale backs are visible primarily from below, not randomized over
    # the sunlit outer crown. Backfacing alone on crossed cards causes mint.
    split=n.new('ShaderNodeSeparateXYZ');l.new(geom.outputs['Incoming'],split.inputs[0])
    below=n.new('ShaderNodeMapRange');below.clamp=True
    below.inputs['From Min'].default_value=-.05;below.inputs['From Max'].default_value=-.65
    l.new(split.outputs['Z'],below.inputs['Value'])
    back=n.new('ShaderNodeMath');back.operation='MULTIPLY'
    l.new(below.outputs[0],back.inputs[0]);l.new(geom.outputs['Backfacing'],back.inputs[1])
    l.new(back.outputs[0],underside.inputs[0]);l.new(tex.outputs['Color'],underside.inputs[1])
    pale=n.new('ShaderNodeMixRGB');pale.blend_type='MULTIPLY';pale.inputs[0].default_value=1;pale.inputs[2].default_value=back_multiplier
    l.new(tex.outputs['Color'],pale.inputs[1])
    glaucous=n.new('ShaderNodeHueSaturation');glaucous.inputs['Saturation'].default_value=back_saturation
    l.new(pale.outputs[0],glaucous.inputs['Color']);l.new(glaucous.outputs[0],underside.inputs[2])
    bs=n.new('ShaderNodeBsdfPrincipled');bs.name='Leaf reflective surface';bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Specular IOR Level'].default_value=specular;l.new(underside.outputs[0],bs.inputs['Base Color'])
    if normal_image:
        normal=n.new('ShaderNodeTexImage');normal.image=normal_image
        normal.image.colorspace_settings.name='Non-Color'
        nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=normal_strength
        l.new(normal.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs[0],bs.inputs['Normal'])
    if orm_image:
        orm=n.new('ShaderNodeTexImage');orm.image=orm_image;orm.image.colorspace_settings.name='Non-Color'
        sep=n.new('ShaderNodeSeparateColor');l.new(orm.outputs[0],sep.inputs[0]);l.new(sep.outputs['Green'],bs.inputs['Roughness'])
    trans=n.new('ShaderNodeBsdfTranslucent');trans.name='Thin leaf diffuse transmission';l.new(underside.outputs[0],trans.inputs['Color'])
    mix=n.new('ShaderNodeMixShader');mix.name='Leaf transmission fraction';mix.inputs[0].default_value=transmission
    l.new(bs.outputs[0],mix.inputs[1]);l.new(trans.outputs[0],mix.inputs[2])
    # The true plane normal, not the bent lighting normal, detects a slash.
    dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT'
    l.new(geom.outputs['True Normal'],dot.inputs[0]);l.new(geom.outputs['Incoming'],dot.inputs[1])
    absolute=n.new('ShaderNodeMath');absolute.operation='ABSOLUTE';l.new(dot.outputs['Value'],absolute.inputs[0])
    fade=n.new('ShaderNodeMapRange');fade.name='Glancing coverage';fade.interpolation_type='SMOOTHERSTEP';fade.clamp=True
    fade.inputs['From Min'].default_value=edge_fade[0];fade.inputs['From Max'].default_value=edge_fade[1]
    l.new(absolute.outputs[0],fade.inputs['Value'])
    cutoff=n.new('ShaderNodeMath');cutoff.operation='GREATER_THAN';cutoff.inputs[1].default_value=.45;l.new(tex.outputs['Alpha'],cutoff.inputs[0])
    coverage=n.new('ShaderNodeMath');coverage.operation='MULTIPLY';l.new(cutoff.outputs[0],coverage.inputs[0]);l.new(fade.outputs[0],coverage.inputs[1])
    transparent=n.new('ShaderNodeBsdfTransparent');surface=n.new('ShaderNodeMixShader');surface.name='Branchlet coverage'
    l.new(coverage.outputs[0],surface.inputs[0]);l.new(transparent.outputs[0],surface.inputs[1]);l.new(mix.outputs[0],surface.inputs[2])
    out=n.new('ShaderNodeOutputMaterial');l.new(surface.outputs[0],out.inputs[0])
    mat['translucent_fraction']=transmission;mat['edge_fade_cosine']=list(edge_fade)
    return mat
