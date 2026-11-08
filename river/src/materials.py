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


def palette(repo):
    # Complete importer settings group before tiling creates its AO socket.
    from io_scene_gltf2.blender.com.material_helpers import create_settings_group
    if not bpy.data.node_groups.get('glTF Material Output'):create_settings_group('glTF Material Output')
    for role,key in [('concrete','Concrete'),('asphalt','Asphalt'),('grass','Lawn')]:
        G.M[role]=tiling.material(key,repo/'ground/textures/ship',tint=True)
    bank=tiling.material('RiverBank',Path('textures/checkpoint'),tint=True)
    bank.use_backface_culling=False;G.M['bank']=bank
    for role,c,r,m in [('steel',(.26,.285,.28),.44,1),('rubber',(.012,.014,.011),.87,0),
                         ('wood',(.10,.068,.035),.95,0),('algae',(.065,.075,.026),.9,0),
                         ('rust',(.13,.058,.024),.95,0),('foam',(.48,.49,.40),.7,0),
                         ('yellow',(.60,.39,.036),.7,0),('white',(.58,.58,.49),.8,0)]:
        G.M[role]=plain('River_'+role,c,r,m)
    plants=plain('River_bank_cards',(.1,.13,.035));plants.use_backface_culling=False
    b=plants.node_tree.nodes.get('Principled BSDF');tex=plants.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(Path('textures/checkpoint/T_RiverPlants_BaseColor.png').resolve()),check_existing=True)
    plants.node_tree.links.new(tex.outputs['Color'],b.inputs['Base Color'])
    plants.node_tree.links.new(tex.outputs['Alpha'],b.inputs['Alpha']);plants.surface_render_method='DITHERED'
    G.M['plants']=plants
    water=plain('River_water',(.31,.34,.21),.16)
    b=water.node_tree.nodes.get('Principled BSDF');b.inputs['Transmission Weight'].default_value=1
    b.inputs['IOR'].default_value=1.333
    tex=water.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(Path('textures/checkpoint/T_RiverWater_Normal.png').resolve()),check_existing=True);tex.image.colorspace_settings.name='Non-Color'
    nm=water.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55
    water.node_tree.links.new(tex.outputs['Color'],nm.inputs['Color']);water.node_tree.links.new(nm.outputs['Normal'],b.inputs['Normal'])
    absorb=water.node_tree.nodes.new('ShaderNodeVolumeAbsorption');absorb.inputs['Color'].default_value=(.37,.43,.20,1);absorb.inputs['Density'].default_value=.27
    water.node_tree.links.new(absorb.outputs[0],water.node_tree.nodes.get('Material Output').inputs['Volume'])
    water['river_volume_color']=[.37,.43,.20];water['river_volume_density']=.27
    water['river_flow_attribute']='_FLOW';G.M['water']=water
