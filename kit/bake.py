"""GPU Cycles high-to-low atlas bake. The external owner reference is never loaded."""
import argparse,json,sys,time,runpy
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import gpu,bake_groups,atlas
from kit.image_io import write_png,linear_to_srgb


def main():
    p=argparse.ArgumentParser();p.add_argument('--low',required=True);p.add_argument('--high',required=True)
    p.add_argument('--out',required=True);p.add_argument('--asset',required=True)
    p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=32)
    p.add_argument('--config')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.low).resolve()));sc=bpy.context.scene
    cfg=runpy.run_path(a.config) if a.config else {}
    policy=cfg.get('BAKE_POLICY',{});roots=policy.get('moving_roots',[]) if policy.get('isolate_moving',False) else []
    originals=[o for o in sc.objects if o.type=='MESH' and 'asset_set' in o and not atlas.tiled_spec(o.name,cfg)]
    spacing=bake_groups.offsets(originals,roots,policy.get('padding_m',.1)) if roots else {}
    copies=[];group_counts={}
    for ob in list(sc.objects):
        if ob.type!='MESH' or 'asset_set' not in ob or atlas.tiled_spec(ob.name,cfg):continue
        copy=ob.copy();copy.data=ob.data.copy();copy.name='Bake copy '+ob.name;sc.collection.objects.link(copy)
        group=bake_groups.owner(ob,roots);group_counts[group]=group_counts.get(group,0)+1
        world=ob.matrix_world.copy();world.translation+=spacing.get(group,Vector((0,0,0)))
        copy.parent=None;copy.matrix_world=world;copy.modifiers.clear();copies.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in copies:ob.select_set(True)
    bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();target=copies[0];target.name='Atlas bake target'
    # Join retains world-space normals and the already-packed target UVs.
    for ob in list(sc.objects):
        if ob!=target:bpy.data.objects.remove(ob,do_unlink=True)
    target.data.materials.clear();material=bpy.data.materials.new('Bake target');material.use_nodes=True
    target.data.materials.append(material)
    for face in target.data.polygons:face.material_index=0
    target.data.uv_layers.active=target.data.uv_layers['BakeUV'];target.data.uv_layers['BakeUV'].active_render=True
    node=material.node_tree.nodes.new('ShaderNodeTexImage');material.node_tree.nodes.active=node
    before=set(bpy.data.objects)
    with bpy.data.libraries.load(str(Path(a.high).resolve()),link=False) as (source,destination):destination.objects=list(source.objects)
    source_objects=[ob for ob in destination.objects if ob]
    for ob in source_objects:sc.collection.objects.link(ob)
    bpy.context.view_layer.update()
    sources=[ob for ob in source_objects if ob.type=='MESH' and 'asset_set' in ob and not atlas.tiled_spec(ob.name,cfg)]
    if len({ob.get('asset_set') for ob in sources})!=1:raise ValueError('Bake one atlas set at a time')
    for ob in source_objects:
        if ob.type=='MESH' and atlas.tiled_spec(ob.name,cfg):ob.hide_render=True
    for ob in sources:
        ob.hide_render=False
        for modifier in ob.modifiers:
            if modifier.type=='ARMATURE':modifier.show_render=modifier.show_viewport=False
    coordinate_frames=bake_groups.referenced_frames(sources,roots) if roots else []
    ghosts=[]
    for ob in sources:
        group=bake_groups.owner(ob,roots)
        if group=='stationary':continue
        # Keep a rest-position shadow copy for stationary contact AO only.
        ghost=ob.copy();ghost.data=ob.data.copy();ghost['source_vertex_count']=len(ob.data.vertices)
        ghost.name='Stationary AO occluder '+ob.name
        sc.collection.objects.link(ghost);world=ob.matrix_world.copy()
        ghost.parent=None;ghost.matrix_world=world;ghost.modifiers.clear();ghost.hide_render=True
        ghosts.append(ghost)
        ob.parent=None;ob.matrix_world=world
        ob.matrix_world.translation+=spacing[group]
    bake_groups.translate_frames(coordinate_frames,spacing)
    bpy.context.view_layer.update()
    # Selected-to-active incurs a scene synchronization for every source object.
    # Consolidate objects sharing a coordinate frame, retaining object-space
    # material masks, PrintUV, normals and world placement exactly.
    frames={}
    for ob in sources:
        key=tuple(round(v,7) for row in ob.matrix_world for v in row)
        frames.setdefault(key,[]).append(ob)
    original_count=len(sources);sources=[]
    for members in frames.values():
        bpy.ops.object.select_all(action='DESELECT')
        for ob in members:
            ob.select_set(True)
            for modifier in list(ob.modifiers):
                if modifier.type=='ARMATURE':ob.modifiers.remove(modifier)
                else:
                    bpy.context.view_layer.objects.active=ob
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
        bpy.context.view_layer.objects.active=members[0];bpy.ops.object.join()
        sources.append(members[0])
    assert all(len(ob.data.vertices)==ob['source_vertex_count'] for ob in ghosts),'AO shadow geometry changed during source consolidation'
    print('BAKE_SOURCES',original_count,'objects ->',len(sources),'coordinate frames',flush=True)
    mats={m for ob in sources for m in ob.data.materials if m}
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
    sc.render.bake.use_selected_to_active=True;sc.render.bake.use_clear=True
    sc.render.bake.cage_extrusion=policy.get('cage_m',cfg.get('BAKE_CAGE',.006));sc.render.bake.max_ray_distance=policy.get('ray_distance_m',cfg.get('BAKE_RAY',.018))
    sc.render.bake.margin=12;sc.render.bake.margin_type='EXTEND'
    if not sc.world:sc.world=bpy.data.worlds.new('Bake world')
    if hasattr(sc.world,'light_settings'):sc.world.light_settings.distance=policy.get('ao_distance_m',.035)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in sources:ob.select_set(True)
    target.select_set(True);bpy.context.view_layer.objects.active=target
    stats={};images={}
    def route(channel):
        for m in mats:
            nt=m.node_tree;output=nt.nodes['OUT']
            if channel is None:nt.links.new(nt.nodes['SURFACE'].outputs['BSDF'],output.inputs['Surface'])
            else:
                emission=nt.nodes.get('BAKE_EMIT') or nt.nodes.new('ShaderNodeEmission');emission.name='BAKE_EMIT'
                nt.links.new(nt.nodes['OUT_'+channel].outputs[0],emission.inputs['Color'])
                nt.links.new(emission.outputs[0],output.inputs['Surface'])
    def bake(name,kind,channel=None):
        image=bpy.data.images.new('Bake '+name,a.size,a.size,alpha=True,float_buffer=True)
        image.colorspace_settings.name='Non-Color';node.image=image
        route(channel);start=time.time()
        options=dict(type=kind)
        if kind=='NORMAL':options.update(normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
        for ghost in ghosts:ghost.hide_render=kind!='AO'
        bpy.ops.object.bake(**options)
        values=np.empty(a.size*a.size*4,np.float32);image.pixels.foreach_get(values)
        values=np.flipud(values.reshape(a.size,a.size,4)).copy();images[name]=values
        stats[name]=dict(seconds=time.time()-start,min=float(values[:,:,:3].min()),max=float(values[:,:,:3].max()))
        print('BAKED',name,stats[name],flush=True)
    bake('BaseColor','EMIT','base');write_png(out/f'T_{a.asset}_BaseColor.png',linear_to_srgb(images['BaseColor'][:,:,:3]))
    bake('Roughness','EMIT','rough');bake('Metallic','EMIT','metal');bake('AO','AO')
    orm=np.stack([images['AO'][:,:,0],images['Roughness'][:,:,0],images['Metallic'][:,:,0]],axis=2)
    write_png(out/f'T_{a.asset}_ORM.png',orm)
    # Free intermediate CPU buffers before the large tangent-normal pass.
    for name in ['Roughness','Metallic','AO']:
        images.pop(name);bpy.data.images.remove(bpy.data.images['Bake '+name])
    bake('Normal','NORMAL')
    normal=images['Normal'][:,:,:3];normal[images['Normal'][:,:,3]<.5]=(.5,.5,1)
    write_png(out/f'T_{a.asset}_Normal.png',normal,16)
    stats['projection_policy']=dict(isolate_moving=bool(roots),moving_roots=roots,target_meshes_by_group=group_counts,stationary_ao_occluders=len(ghosts),explicit_coordinate_frames=len(coordinate_frames),offsets_m={k:list(v) for k,v in spacing.items()})
    stats['size']=a.size;stats['samples']=a.samples;stats['device']=sc.cycles.device
    stats['source_meshes']=original_count;stats['bake_frames']=len(sources);stats['source_materials']=len(mats)
    (out/'bake-report.json').write_text(json.dumps(stats,indent=2))
    route(None)

if __name__=='__main__':main()
