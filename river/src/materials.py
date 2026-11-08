"""Quick exported PBR; canonical Ground maps remain read-only."""
from pathlib import Path
import bpy
from kit import tiling
import geometry as G


def plain(name,c,rough=.8,metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;m['tiling_vertex_tint']=False
    b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1)
    b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal
    return m


def volume_from_extras(material):
    """Uniform physical coefficients in 1/m; one HG phase closure in 5.2.

    Equivalent to adding classic absorption and scatter nodes. Using one
    coefficient node avoids Cycles' conservative two-volume closure estimate.
    """
    node=material.node_tree.nodes.new('ShaderNodeVolumeCoefficients')
    node.phase='HENYEY_GREENSTEIN'
    color=material['river_volume_color'];density=material['river_volume_density']
    node.inputs['Absorption Coefficients'].default_value=tuple((1-c)*density for c in color)
    node.inputs['Scatter Coefficients'].default_value=tuple(c*material['river_scatter_density'] for c in material['river_scatter_color'])
    node.inputs['Anisotropy'].default_value=material['river_scatter_anisotropy']
    out=next(n for n in material.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
    material.node_tree.links.new(node.outputs[0],out.inputs['Volume'])


def palette(repo):
    # Complete importer settings group before tiling creates its AO socket.
    from io_scene_gltf2.blender.com.material_helpers import create_settings_group
    if not bpy.data.node_groups.get('glTF Material Output'):create_settings_group('glTF Material Output')
    for role,key in [('concrete','Concrete'),('asphalt','Asphalt'),('grass','Lawn')]:
        G.M[role]=tiling.material(key,repo/'ground/textures/ship',tint=True)
    for role,key in [('bridge_concrete','FreewayConcrete'),('zinc','FreewayZinc')]:
        G.M[role]=tiling.material(key,repo/'freeway/textures/ship',tint=True)
    bank=tiling.material('RiverBank',Path('textures/checkpoint'),tint=True)
    bank.use_backface_culling=False;G.M['bank']=bank
    # Quarry faces use the existing fine mineral field, never the bed's clasts.
    G.M['riprap']=G.M['bridge_concrete'].copy();G.M['riprap'].name='River_quarry_stone'
    for role,color in [('paint_yellow',(.9,.66,.08)),('paint_white',(1,1,1))]:
        ma=tiling.material('GroundTrim',repo/'ground/textures/ship',alpha=True,tint=False)
        ma.name='River_'+role
        bs=ma.node_tree.nodes.get('Principled BSDF');links=ma.node_tree.links
        source=bs.inputs['Base Color'].links[0].from_socket
        mix=ma.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
        mix.inputs[2].default_value=(*color,1);links.new(source,mix.inputs[1]);links.new(mix.outputs[0],bs.inputs['Base Color'])
        G.M[role]=ma
    G.M['decal']=tiling.material('GroundTrim',repo/'ground/textures/ship',alpha=True,tint=False)
    for role,c,r,m in [('steel',(.26,.285,.28),.44,1),('rubber',(.012,.014,.011),.87,0),
                         ('wood',(.10,.068,.035),.95,0),('algae',(.065,.075,.026),.9,0),
                         ('rust',(.13,.058,.024),.95,0),('foam',(.48,.49,.40),.7,0),
                         ('hay',(.24,.205,.09),.97,0),
                         ('yellow',(.60,.39,.036),.7,0),('white',(.58,.58,.49),.8,0)]:
        G.M[role]=plain('River_'+role,c,r,m)
    plants=plain('River_bank_cards',(.1,.13,.035));plants.use_backface_culling=False
    b=plants.node_tree.nodes.get('Principled BSDF');tex=plants.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(Path('textures/checkpoint/T_RiverPlants_BaseColor.png').resolve()),check_existing=True)
    plants.node_tree.links.new(tex.outputs['Color'],b.inputs['Base Color'])
    plants.node_tree.links.new(tex.outputs['Alpha'],b.inputs['Alpha']);plants.surface_render_method='DITHERED'
    G.M['plants']=plants
    foam=plants.copy();foam.name='River_foam';foam.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.66
    G.M['foam']=foam
    maintenance=plants.copy();maintenance.name='River_maintenance';maintenance['tiling_vertex_tint']=True
    maintenance.surface_render_method='DITHERED'
    nodes=maintenance.node_tree.nodes;links=maintenance.node_tree.links
    bs=nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.92
    image=next(n for n in nodes if n.type=='TEX_IMAGE');vc=nodes.new('ShaderNodeVertexColor');vc.layer_name='Tint'
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    links.new(image.outputs['Color'],mix.inputs[1]);links.new(vc.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],bs.inputs['Base Color'])
    G.M['maintenance']=maintenance
    water=plain('River_water',(.92,.94,.82),.14)
    b=water.node_tree.nodes.get('Principled BSDF');b.inputs['Transmission Weight'].default_value=1
    b.inputs['IOR'].default_value=1.333
    tex=water.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(Path('textures/checkpoint/T_RiverWater_Normal.png').resolve()),check_existing=True);tex.image.colorspace_settings.name='Non-Color'
    nm=water.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=1.2
    water.node_tree.links.new(tex.outputs['Color'],nm.inputs['Color']);water.node_tree.links.new(nm.outputs['Normal'],b.inputs['Normal'])
    water['river_volume_color']=[.55,.64,.24];water['river_volume_density']=.85
    water['river_scatter_color']=[.60,.67,.27];water['river_scatter_density']=.55;water['river_scatter_anisotropy']=.20
    water['river_flow_attribute']='_FLOW';G.M['water']=water
    water['river_flow_speed_range']=[.15,1.15]
    water['river_flow_normal_range']=[.28,1.65]
    water['river_flow_roughness_range']=[.065,.19]
    volume_from_extras(water)
