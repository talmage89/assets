"""Swap only the four original manufacture fields for bake-loss inspection.

This deliberately renders the exported geometry with 4096 source fields, and
labels it as source material inspection. It is never a shipped-material view.
"""
import bpy
from pathlib import Path
from textures import SETS

def install():
    changed=[]
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        nodes=mat.node_tree.nodes;links=mat.node_tree.links
        for node in list(nodes):
            if node.type!='TEX_IMAGE' or not node.image:continue
            for name,spec in SETS.items():
                if name not in node.image.name:continue
                channel=next((c for c in ('BaseColor','Normal','ORM') if c in node.image.name),None)
                if not channel:continue
                if channel=='Normal':
                    bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');h=nodes.new('ShaderNodeTexImage');h.image=bpy.data.images.load(str((Path('textures/source')/f'T_{name}_Height.png').resolve()),check_existing=True);h.image.colorspace_settings.name='Non-Color'
                    bump=nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=spec['height'];links.new(h.outputs[0],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
                else:
                    node.image=bpy.data.images.load(str((Path('textures/source')/f'T_{name}_{channel}.png').resolve()),check_existing=True);node.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
                    if name=='FreewayMaintenance' and channel=='BaseColor':
                        alpha=nodes.new('ShaderNodeTexImage');alpha.image=bpy.data.images.load(str(Path('textures/source/T_FreewayMaintenance_Alpha.png').resolve()),check_existing=True);alpha.image.colorspace_settings.name='Non-Color'
                        bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');links.new(alpha.outputs[0],bs.inputs['Alpha'])
                changed.append((mat.name,name,channel))
    return changed
