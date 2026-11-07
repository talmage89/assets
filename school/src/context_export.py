"""Export local form copies; preserve original foliage UV/alpha silhouettes."""
import sys,math,json
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from geometry import consolidate
kind=sys.argv[sys.argv.index('--')+1]
source=Path('build/context/car.blend') if kind=='car' else Path('build/context/shrub/source.blend')
bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get()
foliage=None
if kind=='shrub':
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    from kit.export import atlas_material
    get_settings_group();foliage=atlas_material('Shrubs',Path('build/context/shrub/shrubs/textures/analytic').resolve(),.45,True)
for ob in list(bpy.context.scene.objects):
    if ob.type!='MESH':continue
    if kind=='car' and any(term in ob.name for term in ('Brake rotor','Brake caliper','Wheel lug','Shoulder tread')):
        # Parked context at school viewing distances: retain the authored body,
        # wheels, tires and glass; omit small brake/lug internals from this local
        # form copy. Canonical vehicle source and deliveries remain untouched.
        bpy.data.objects.remove(ob,do_unlink=True);continue
    if ob.modifiers:
        ob.data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.modifiers.clear()
    if kind=='car':
        ob.data.calc_loop_triangles()
        if len(ob.data.loop_triangles)>800:
            lod=ob.modifiers.new('Parked school context LOD','DECIMATE');lod.ratio=.68;lod.use_collapse_triangulate=True
    if kind=='shrub':
        keep=ob.data.uv_layers.get('BakeUV') or ob.data.uv_layers.active
        for uv in list(ob.data.uv_layers):
            if uv!=keep:ob.data.uv_layers.remove(uv)
        if keep:keep.name='UVMap'
        for attr in list(ob.data.color_attributes):ob.data.color_attributes.remove(attr)
        for i,ma in enumerate(list(ob.data.materials)):
            if ma and 'foliage' in ma.name.lower():ob.data.materials[i]=foliage
    for ma in ob.data.materials:
        if not ma or not ma.use_nodes:continue
        bs=next((n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bs:
            if kind=='car':
                for key in ('Base Color','Normal','Metallic','Roughness'):
                    for link in list(bs.inputs[key].links):ma.node_tree.links.remove(link)
                c=(.19,.09,.047) if 'paint' in ma.name.lower() else (.018,.020,.018) if any(q in ma.name.lower() for q in ('rubber','tire','frame')) else (.32,.34,.33) if any(q in ma.name.lower() for q in ('wheel','chrome')) else (.085,.10,.10)
                bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.40
            elif any(term in ma.name.lower() for term in ('wood','stems')):
                for key in ('Base Color','Normal','Roughness'):
                    for link in list(bs.inputs[key].links):ma.node_tree.links.remove(link)
                bs.inputs['Base Color'].default_value=(.08,.06,.031,1);bs.inputs['Roughness'].default_value=.9
            bs.inputs['Emission Strength'].default_value=0
    if not ob.data.uv_layers:
        uv=ob.data.uv_layers.new(name='UVMap')
        for f in ob.data.polygons:
            axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
            for li in f.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
if kind=='car':
    colors={}
    for ob in bpy.context.scene.objects:
        ob['asset_set']='SchoolContext'
        if ob.type!='MESH':continue
        for i,old in enumerate(list(ob.data.materials)):
            if not old or not old.use_nodes:continue
            bs=next((n for n in old.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if not bs:continue
            keys=('Base Color','Roughness','Metallic','Transmission Weight','IOR','Coat Weight')
            values=[tuple(bs.inputs[k].default_value) if k=='Base Color' else float(bs.inputs[k].default_value) for k in keys]
            key=repr(values)
            if key not in colors:
                ma=bpy.data.materials.new('School context vehicle '+('paint ' if 'paint' in old.name.lower() else '')+str(len(colors)));ma.use_nodes=True
                p=ma.node_tree.nodes.get('Principled BSDF')
                for k,v in zip(keys,values):p.inputs[k].default_value=v
                colors[key]=ma
            ob.data.materials[i]=colors[key]
consolidate('SchoolContext' if kind=='car' else 'School')
triangles=0
for ob in bpy.context.scene.objects:
    if ob.type=='MESH':ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles)
Path('build/context',kind+'.json').write_text(json.dumps(dict(triangles=triangles,stage='local context from original family scripts',car_lod_ratio=.68 if kind=='car' else None),indent=2))
bpy.ops.export_scene.gltf(filepath=str(Path('build/context',kind+'.glb').resolve()),export_format='GLB',export_extras=True,export_animations=False,export_attributes=True,export_tangents=True)
