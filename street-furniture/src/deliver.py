"""Stock glTF, four canonical shared images, two material states per piece.

Opaque: 2048 BaseColor/Normal/ORM. Glazing and print share the 1024 graphics
image on TEXCOORD_1; reserved ORM cells on TEXCOORD_0 select transmission.
That second state omits occlusion, so ORM.R is available as transmission.
"""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import model as G

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='build/finalized.blend');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    ims={k:bpy.data.images.load(str(Path('textures/ship/T_StreetFurniture_'+k+'.png').resolve()),check_existing=True) for k in ('BaseColor','Normal','ORM','Graphics')}
    for k in ('Normal','ORM'):ims[k].colorspace_settings.name='Non-Color'
    def make(name,overlay=False):
        m=bpy.data.materials.new(name);m.use_nodes=True;ns=m.node_tree.nodes;ls=m.node_tree.links;p=ns.get('Principled BSDF')
        uv=ns.new('ShaderNodeUVMap');uv.uv_map='BakeUV';guv=ns.new('ShaderNodeUVMap');guv.uv_map='GraphicsUV'
        def tex(key,coord):
            n=ns.new('ShaderNodeTexImage');n.image=ims[key];ls.new(coord,n.inputs['Vector']);return n
        b=tex('Graphics' if overlay else 'BaseColor',guv.outputs[0] if overlay else uv.outputs[0]);ls.new(b.outputs['Color'],p.inputs['Base Color'])
        orm=tex('ORM',uv.outputs[0]);sep=ns.new('ShaderNodeSeparateColor');ls.new(orm.outputs[0],sep.inputs[0]);ls.new(sep.outputs['Green'],p.inputs['Roughness']);ls.new(sep.outputs['Blue'],p.inputs['Metallic'])
        norm=tex('Normal',uv.outputs[0]);nm=ns.new('ShaderNodeNormalMap');nm.uv_map='BakeUV';ls.new(norm.outputs[0],nm.inputs['Color']);ls.new(nm.outputs[0],p.inputs['Normal'])
        if overlay:
            ls.new(sep.outputs['Red'],p.inputs['Transmission Weight']);p.inputs['IOR'].default_value=1.49
        else:
            group=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree');group.interface.new_socket(name='Occlusion',in_out='INPUT',socket_type='NodeSocketFloat');gn=ns.new('ShaderNodeGroup');gn.node_tree=group;ls.new(sep.outputs['Red'],gn.inputs['Occlusion'])
        return m
    opaque=make('StreetFurniture');overlay=make('StreetFurniture_GraphicsGlazing',True)
    processed=set()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.data in processed:continue
        processed.add(ob.data)
        if 'asset_set' in ob or ob.name.startswith('Row_') and ob.get('bake_surface'):
            # Row members share canonical mesh data with the standalone boxes.
            for uv in list(ob.data.uv_layers):
                if uv.name!='BakeUV':ob.data.uv_layers.remove(uv)
            ob.data.materials.clear();ob.data.materials.append(opaque)
            for face in ob.data.polygons:face.material_index=0
        else:
            original=[tuple(v.uv) for v in ob.data.uv_layers.active.data]
            glass_faces={f.index for f in ob.data.polygons if 'Glazing' in ob.data.materials[f.material_index].name}
            for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
            bake=ob.data.uv_layers.new(name='BakeUV');graphic=ob.data.uv_layers.new(name='GraphicsUV')
            for face in ob.data.polygons:
                glass=face.index in glass_faces
                for li in face.loop_indices:
                    u,v=original[li]
                    bake.data[li].uv=(.01+u*.48,.981+v*.014) if glass else (.75,.988)
                    graphic.data[li].uv=((264+u*240)/1024,1-(952-v*176)/1024) if glass else ((u-.5)*2,v)
            ob.data.materials.clear();ob.data.materials.append(overlay)
            for face in ob.data.polygons:face.material_index=0
        ob.data.uv_layers.active=ob.data.uv_layers['BakeUV'];ob.data.uv_layers['BakeUV'].active_render=True
    roots=[o for o in bpy.context.scene.objects if o.parent is None]
    out=Path('export');out.mkdir(exist_ok=True)
    opts=dict(export_format='GLTF_SEPARATE',export_texture_dir='textures',export_extras=True,export_animations=False,export_tangents=True,export_yup=True)
    bpy.ops.export_scene.gltf(filepath=str((out/'StreetFurniture.gltf').resolve()),**opts)
    for rt in roots:
        bpy.ops.object.select_all(action='DESELECT')
        for ob in [rt,*rt.children_recursive]:ob.select_set(True)
        old=rt.location.copy();rt.location=(0,0,0)
        bpy.ops.export_scene.gltf(filepath=str((out/(rt.name+'.gltf')).resolve()),use_selection=True,**opts);rt.location=old
    data=json.loads(Path('build/game.json').read_text());data['stage']='Final shared-atlas glTF, baked at 4096 / shipped at 2048 plus 1024 graphics'
    for row in data['pieces'].values():row['materials']=['StreetFurniture','StreetFurniture_GraphicsGlazing']
    Path('build/manifest.json').write_text(json.dumps(data,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/delivery.blend').resolve()))
if __name__=='__main__':main()
