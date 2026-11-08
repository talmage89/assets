"""Parallel-pane colored shadow transmission for Cycles look renders.

Camera rays retain imported refraction. Straight shadow rays approximate the
negligible lateral offset of the finite parallel panes, retaining their tint
and Fresnel loss instead of losing direct daylight to unsampled caustics.
"""
import bpy

def install(materials=None):
    for mat in bpy.data.materials if materials is None else materials:
        if not mat.use_nodes:continue
        nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs or not (mat.get('vehicle_glass') or bs.inputs['Transmission Weight'].default_value>0):continue
        if nt.nodes.get('Parallel pane shadow'):continue
        out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        physical=out.inputs['Surface'].links[0].from_socket
        tint=nt.nodes.new('ShaderNodeGamma');tint.inputs['Gamma'].default_value=.5
        base=bs.inputs['Base Color']
        if base.is_linked:nt.links.new(base.links[0].from_socket,tint.inputs['Color'])
        else:tint.inputs['Color'].default_value=base.default_value
        fresnel=nt.nodes.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=bs.inputs['IOR'].default_value
        loss=nt.nodes.new('ShaderNodeMath');loss.operation='SUBTRACT';loss.inputs[0].default_value=1
        nt.links.new(fresnel.outputs[0],loss.inputs[1])
        color=nt.nodes.new('ShaderNodeVectorMath');color.operation='SCALE'
        nt.links.new(tint.outputs[0],color.inputs[0]);nt.links.new(loss.outputs[0],color.inputs['Scale'])
        transparent=nt.nodes.new('ShaderNodeBsdfTransparent');nt.links.new(color.outputs[0],transparent.inputs[0])
        path=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');mix.name='Parallel pane shadow'
        nt.links.new(path.outputs['Is Shadow Ray'],mix.inputs[0]);nt.links.new(physical,mix.inputs[1])
        nt.links.new(transparent.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
