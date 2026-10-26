"""Consolidate static assemblies, preserve pivots/skin/sockets, embed one PBR atlas."""
import argparse,json,sys,runpy
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import model as G


def atlas_material(asset,folder):
    material=bpy.data.materials.new(asset);material.use_nodes=True
    nt=material.node_tree;nt.nodes.clear()
    surface=nt.nodes.new('ShaderNodeBsdfPrincipled');surface.name='SURFACE'
    output=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(surface.outputs[0],output.inputs['Surface'])
    uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='UVMap'
    images={}
    for channel in ('BaseColor','Normal','ORM'):
        texture=nt.nodes.new('ShaderNodeTexImage')
        texture.image=bpy.data.images.load(str(folder/f'T_{asset}_{channel}.png'),check_existing=True)
        texture.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
        nt.links.new(uv.outputs[0],texture.inputs['Vector']);images[channel]=texture
    nt.links.new(images['BaseColor'].outputs['Color'],surface.inputs['Base Color'])
    separate=nt.nodes.new('ShaderNodeSeparateColor');nt.links.new(images['ORM'].outputs['Color'],separate.inputs['Color'])
    nt.links.new(separate.outputs['Green'],surface.inputs['Roughness']);nt.links.new(separate.outputs['Blue'],surface.inputs['Metallic'])
    normal=nt.nodes.new('ShaderNodeNormalMap');normal.uv_map='UVMap'
    nt.links.new(images['Normal'].outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs[0],surface.inputs['Normal'])
    group=bpy.data.node_groups.get('glTF Material Output')
    if not group:
        group=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree')
        group.interface.new_socket('Occlusion',in_out='INPUT',socket_type='NodeSocketFloat')
    occlusion=nt.nodes.new('ShaderNodeGroup');occlusion.node_tree=group
    nt.links.new(separate.outputs['Red'],occlusion.inputs['Occlusion'])
    return material


def moving_parent(ob):
    if ob.parent and ob.parent.type=='ARMATURE':return ob.parent
    parent=ob.parent
    while parent:
        if 'pivot_axis' in parent or 'slide_axis' in parent:return parent
        parent=parent.parent
    parent=ob.parent
    while parent:
        if parent.get('static_root'):return parent
        parent=parent.parent
    return ob.parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--textures',required=True)
    p.add_argument('--asset',required=True);p.add_argument('--out',required=True);p.add_argument('--report',required=True)
    p.add_argument('--config')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    sc=bpy.context.scene
    cfg=runpy.run_path(a.config) if a.config else {}
    variant=cfg.get('EXPORT_VARIANT',0)
    for ob in list(sc.objects):
        if 'variant_id' in ob:
            if ob['variant_id']!=variant:bpy.data.objects.remove(ob,do_unlink=True)
            else:
                offset=Vector(ob.get('bake_offset',(0,0,0)))
                # Manufacturing meshes have already been rebased to assembly coordinates.
                for v in ob.data.vertices:v.co-=offset
                ob['bake_only']=False
    objects=[o for o in sc.objects if o.type=='MESH' and 'asset_set' in o]
    material=atlas_material(a.asset,Path(a.textures).resolve());groups={}
    overrides=cfg.get('MATERIAL_OVERRIDES',{});palette={}
    for prefix,settings in overrides.items():
        extra=material.copy();extra.name=a.asset+' '+prefix
        shader=extra.node_tree.nodes['SURFACE']
        if settings.get('emission_strength',0):
            color=shader.inputs['Base Color'].links[0].from_socket
            extra.node_tree.links.new(color,shader.inputs['Emission Color'])
            shader.inputs['Emission Strength'].default_value=settings['emission_strength']
        shader.inputs['Transmission Weight'].default_value=settings.get('transmission',0)
        shader.inputs['IOR'].default_value=settings.get('ior',1.5)
        palette[prefix]=extra
    if overrides:
        # Assign before consolidation: Blender remaps the material slots while
        # joining, so static glass/emissive faces need no extra mesh objects.
        for ob in objects:
            chosen=next((palette[prefix] for prefix in overrides if ob.name.startswith(prefix)),material)
            ob.data.materials.clear();ob.data.materials.append(chosen)
            for face in ob.data.polygons:face.material_index=0
    for ob in objects:
        parent=moving_parent(ob);name=ob.get('export_part',parent.name+'Mesh')
        groups.setdefault((parent,name),[]).append(ob)
    for (parent,name),members in groups.items():
        asset_set=members[0].get('asset_set',a.asset)
        bpy.ops.object.select_all(action='DESELECT')
        for ob in members:ob.select_set(True)
        bpy.context.view_layer.objects.active=members[0];bpy.ops.object.join();ob=members[0]
        if parent.type=='ARMATURE':ob.name=cfg.get('EXPORT_SKIN_NAMES',{}).get(parent.name,ob.get('export_part','HoseAssembly'))
        else:
            G.attach(ob,parent,asset_set=asset_set);ob.name=name
        ob.data.name=ob.name;ob['asset_set']=asset_set
        for layer in list(ob.data.uv_layers):
            if layer.name!='BakeUV':ob.data.uv_layers.remove(layer)
        ob.data.uv_layers['BakeUV'].name='UVMap'
        ob.data.uv_layers.active=ob.data.uv_layers['UVMap'];ob.data.uv_layers['UVMap'].active_render=True
        if not overrides:
            ob.data.materials.clear();ob.data.materials.append(material)
            for face in ob.data.polygons:face.material_index=0
        for attribute in list(ob.data.color_attributes):ob.data.color_attributes.remove(attribute)
    # Remove empty manufacturing helper frames once their geometry is consolidated.
    keep={o.name for o in sc.objects if o.get('socket_kind') or o.get('static_root') or o.parent is None}
    for _ in range(4):
        for ob in list(sc.objects):
            if ob.type=='EMPTY' and not ob.children and ob.name not in keep and 'pivot_axis' not in ob and 'slide_axis' not in ob:
                bpy.data.objects.remove(ob,do_unlink=True)
    bpy.context.view_layer.update();report={'asset':a.asset,'meshes':{},'nodes':{},'rigs':{}}
    for ob in sc.objects:
        if ob.type=='MESH':
            ob.data.calc_loop_triangles()
            points=[ob.matrix_world@Vector(v) for v in ob.bound_box]
            report['meshes'][ob.name]=dict(triangles=len(ob.data.loop_triangles),bounds=[list(map(min,zip(*points))),list(map(max,zip(*points)))],vertices_world=[list(ob.matrix_world@v.co) for v in ob.data.vertices])
        if ob.type=='MESH' and any(m.type=='ARMATURE' for m in ob.modifiers):
            report['meshes'][ob.name]['weights']=[{ob.vertex_groups[g.group].name:g.weight for g in v.groups if g.weight>1e-7} for v in ob.data.vertices]
        if ob.type in ('EMPTY','ARMATURE'):report['nodes'][ob.name]=[list(row) for row in ob.matrix_world]
        if ob.type=='ARMATURE':
            report['rigs'][ob.name]={bone.name:dict(parent=bone.parent.name if bone.parent else None,
                head=list(ob.matrix_world@bone.head_local),tail=list(ob.matrix_world@bone.tail_local),
                rest_matrix=[list(row) for row in ob.matrix_world@bone.matrix_local]) for bone in ob.data.bones}
    report['triangles']=sum(v['triangles'] for v in report['meshes'].values())
    report['materials']=sorted({m.name for ob in sc.objects if ob.type=='MESH' for m in ob.data.materials if m});report['source']=a.source
    path=Path(a.out).resolve();path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_yup=True,
        export_apply=False,export_texcoords=True,export_normals=True,export_tangents=True,
        export_materials='EXPORT',export_image_format='AUTO',export_skins=True,export_animations=False,
        export_def_bones=True,export_extras=True,export_cameras=False,export_lights=False)
    if overrides:
        from kit.glb_textures import compact
        report['texture_views']=compact(path,Path(a.report).parent)
    report['bytes']=path.stat().st_size
    Path(a.report).write_text(json.dumps(report,indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.report).with_suffix('.blend').resolve()))
    print('EXPORTED',path,report['triangles'],'triangles',report['bytes'],'bytes',flush=True)

if __name__=='__main__':main()
