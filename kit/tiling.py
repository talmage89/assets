"""World-continuous UVs and stock glTF PBR for modular tiled families.

No runtime shaders: placement reprojects positions into exported TEXCOORD_0.
Vertical surfaces use an authored chart (e.g. curb chainage/profile height).
"""
from pathlib import Path
import math
import json, struct
import bpy


def world_uv(ob, coverage, axes=(0, 1), offset=(0, 0), project=None, material_filter=None):
    uv = ob.data.uv_layers.active or ob.data.uv_layers.new(name='UVMap')
    for poly in ob.data.polygons:
        if material_filter is not None and not material_filter(ob.data.materials[poly.material_index]): continue
        for li in poly.loop_indices:
            loop = ob.data.loops[li]
            v = ob.data.vertices[loop.vertex_index].co
            p = ob.matrix_world @ v
            if project is not None: p = project(ob, v, p)
            uv.data[loop.index].uv = tuple(p[axis] / coverage + offset[i]
                                             for i, axis in enumerate(axes))


def material(name, folder, alpha=False, tint=False):
    """Three shared images, glTF occlusion group, optional COLOR_0 and alpha."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat['tiling_vertex_tint'] = tint
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    images = {}
    for channel in ('BaseColor', 'Normal', 'ORM'):
        im = bpy.data.images.load(str((Path(folder) / f'T_{name}_{channel}.png').resolve()), check_existing=True)
        im.colorspace_settings.name = 'sRGB' if channel == 'BaseColor' else 'Non-Color'
        node = nodes.new('ShaderNodeTexImage'); node.image = im; node.extension = 'REPEAT'
        images[channel] = node
    color = images['BaseColor'].outputs['Color']
    if tint:
        vc = nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Tint'
        mix = nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs[0].default_value = 1
        links.new(color, mix.inputs[6]); links.new(vc.outputs['Color'], mix.inputs[7]); color = mix.outputs[2]
    links.new(color, bsdf.inputs['Base Color'])
    separate = nodes.new('ShaderNodeSeparateColor'); links.new(images['ORM'].outputs['Color'], separate.inputs[0])
    links.new(separate.outputs['Green'], bsdf.inputs['Roughness'])
    links.new(separate.outputs['Blue'], bsdf.inputs['Metallic'])
    normal = nodes.new('ShaderNodeNormalMap'); links.new(images['Normal'].outputs['Color'], normal.inputs['Color'])
    links.new(normal.outputs['Normal'], bsdf.inputs['Normal'])
    group = bpy.data.node_groups.get('glTF Material Output')
    if group is None:
        group = bpy.data.node_groups.new('glTF Material Output', 'ShaderNodeTree')
        group.interface.new_socket(name='Occlusion', in_out='INPUT', socket_type='NodeSocketFloat')
    ao = nodes.new('ShaderNodeGroup'); ao.node_tree = group
    links.new(separate.outputs['Red'], ao.inputs['Occlusion'])
    if alpha:
        links.new(images['BaseColor'].outputs['Alpha'], bsdf.inputs['Alpha'])
        mat.surface_render_method = 'DITHERED'
    mat.use_backface_culling = True
    return mat


def export(path, objects=None):
    """Export already-finalized meshes with authored UVs; compact image views."""
    from kit.glb_textures import compact
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action='SELECT' if objects is None else 'DESELECT')
    if objects is not None:
        for ob in objects: ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()), export_format='GLB', use_selection=True,
        export_yup=True, export_extras=True, export_animations=False, export_tangents=True,
        export_attributes=True, export_all_vertex_colors=False, export_image_format='AUTO')
    # Blender emits a mesh-wide COLOR_0 on every material primitive, even
    # when one material ignores it. glTF always multiplies COLOR_0; remove it
    # from explicitly untinted primitives before any viewer/import can alter
    # their look or manufacture an unnecessary material variant.
    raw=path.read_bytes();offset=12;chunks=[]
    while offset<len(raw):
        length,kind=struct.unpack_from('<II',raw,offset)
        chunks.append([kind,raw[offset+8:offset+8+length]]);offset+=8+length
    doc=next(c for c in chunks if c[0]==0x4e4f534a);data=json.loads(doc[1])
    old=data.get('materials',[]);unique=[];lookup={};remap={}
    for i,m in enumerate(old):
        key=json.dumps({k:v for k,v in m.items() if k!='name'},sort_keys=True)
        if key not in lookup:lookup[key]=len(unique);unique.append(m)
        remap[i]=lookup[key]
    for m in data.get('meshes',[]):
        for primitive in m['primitives']:
            original=old[primitive['material']]
            if original.get('extras',{}).get('tiling_vertex_tint') is False:
                primitive['attributes'].pop('COLOR_0',None)
            primitive['material']=remap[primitive['material']]
    data['materials']=unique
    payload=json.dumps(data,separators=(',',':')).encode();doc[1]=payload+b' '*(-len(payload)%4)
    payload=b''.join(struct.pack('<II',len(value),kind)+value for kind,value in chunks)
    path.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
    return compact(path, path.parent.parent / 'build')


def edge_error(first, second, tolerance=2e-5, periodic=True, normal_tolerance=None):
    """Compare independently sampled edge positions, normals and UV phase.

    Each row is (position[3], normal[3], uv[2]); no source constants are used.
    The caller supplies corresponding samples on actual imported surfaces.
    """
    import numpy as np
    a, b = np.asarray(first), np.asarray(second)
    if a.shape != b.shape or len(a) < 2:
        raise ValueError('Mismatched or empty edge samples')
    duv = a[:, 6:8] - b[:, 6:8]
    if periodic: duv -= np.round(duv)
    report = dict(samples=len(a), position_m=float(np.linalg.norm(a[:, :3]-b[:, :3], axis=1).max()),
        normal_delta=float(np.linalg.norm(a[:, 3:6]-b[:, 3:6], axis=1).max()),
        uv_delta=float(np.linalg.norm(duv, axis=1).max()))
    report['normal_angle_degrees'] = math.degrees(2*math.asin(min(1,report['normal_delta']/2)))
    report['passed'] = max(report['position_m'], report['uv_delta']) < tolerance and report['normal_delta'] < (normal_tolerance if normal_tolerance is not None else tolerance)
    return report
