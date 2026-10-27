"""Apply static modifiers, triangulate and pack one asset atlas, preserving rigs/pivots."""
import argparse,json,math,sys,runpy
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import uv,atlas


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--config');p.add_argument('--report',required=True);p.add_argument('--size',type=int,default=2048)
    p.add_argument('--target-density',type=float,default=850);p.add_argument('--margin',type=float,default=.0015)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    config=runpy.run_path(a.config) if a.config else {}
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    # Original print sheets bake onto the solid metal immediately behind them.
    # Removing their low duplicates saves atlas area and avoids coplanar surfaces.
    for ob in list(objects):
        if ob.name in config.get('BAKE_DROP_MESHES',()):
            objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
    for ob in objects:
        bpy.context.view_layer.objects.active=ob
        for modifier in list(ob.modifiers):
            if modifier.type!='ARMATURE':bpy.ops.object.modifier_apply(modifier=modifier.name)
        # Edit-mode triangulation/UV operations can re-encode custom split
        # normals against different smoothing fans. Carry the actual vectors
        # as ordinary corner data and reseed them after the last edit operation.
        if ob.data.has_custom_normals:
            normals=[n.vector.copy() for n in ob.data.corner_normals]
            saved=ob.data.attributes.new('UV source normals','FLOAT_VECTOR','CORNER')
            for row,n in zip(saved.data,normals):row.vector=n
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        bm.to_mesh(ob.data);bm.free()
        layer=ob.data.uv_layers.get('BakeUV') or ob.data.uv_layers.new(name='BakeUV')
        ob.data.uv_layers.active=layer;layer.active_render=True
    tiled=[o for o in objects if atlas.tiled_spec(o.name,config)]
    objects=[o for o in objects if o not in tiled]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(config.get('UV_SMART_ANGLE',66)),margin_method='SCALED',island_margin=0,area_weight=0,correct_aspect=config.get('UV_SMART_ASPECT',True),scale_to_bounds=False)
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode='OBJECT')
    priorities=config.get('UV_PRIORITY',{})
    for ob in objects:
        priority=next((v for k,v in priorities.items() if ob.name.startswith(k)),config.get('UV_DEFAULT_PRIORITY',1.0))
        layer=ob.data.uv_layers['BakeUV']
        for loops in uv.islands(ob):
            center=sum((layer.data[i].uv.copy() for i in loops),__import__('mathutils').Vector((0,0)))/len(loops)
            for i in loops:layer.data[i].uv=center+(layer.data[i].uv-center)*priority
        ob['texel_priority']=priority
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,rotate_method='ANY',scale=True,
                          merge_overlap=False,margin_method='FRACTION',margin=a.margin,pin=False,shape_method=config.get('UV_PACK_SHAPE','CONCAVE'))
    bpy.ops.object.mode_set(mode='OBJECT')
    if 'UV_ATLAS_RECT' in config:
        x0,y0,x1,y1=config['UV_ATLAS_RECT']
        for ob in objects:
            for point in ob.data.uv_layers['BakeUV'].data:point.uv=(x0+point.uv.x*(x1-x0),y0+point.uv.y*(y1-y0))
    for ob in objects+tiled:
        saved=ob.data.attributes.get('UV source normals')
        if saved:
            ob.data.normals_split_custom_set([row.vector[:] for row in saved.data])
            ob.data.attributes.remove(saved)
    # Packing fits the atlas; reduce uniformly if a larger prop exceeds its declared density.
    measured=uv.report(objects,a.size)
    median=measured['density_px_m']['50']
    if median>a.target_density*1.05:
        factor=a.target_density/median
        for ob in objects:
            for point in ob.data.uv_layers['BakeUV'].data:point.uv=(point.uv-Vector((.5,.5)))*factor+Vector((.5,.5))
        measured=uv.report(objects,a.size)
    measured['unique_region']=atlas.unique_rect_report(objects,config)
    if not measured['unique_region']['passed']:raise RuntimeError(str(measured['unique_region']))
    measured['tiling']=atlas.tile_report(tiled,config,a.size)
    if not measured['tiling']['passed']:raise RuntimeError(str(measured['tiling']))
    measured['target_density_px_m']=a.target_density
    measured['density_policy']='priority-weighted: exterior/markings above structural and hidden surfaces'
    if measured['coverage']<.20 or measured['outside_triangles'] or measured['degenerate_uv_triangles'] or measured['overlap_fraction']>1e-5:
        raise RuntimeError('UV validation failed: '+str({k:v for k,v in measured.items() if k!='island_measurements'}))
    Path(a.report).parent.mkdir(parents=True,exist_ok=True);Path(a.report).write_text(json.dumps(measured,indent=2))
    bpy.context.scene['stage']='finalized';bpy.context.scene['atlas_size']=a.size
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('UV_FINALIZED',json.dumps({k:v for k,v in measured.items() if k!='island_measurements'}),flush=True)

if __name__=='__main__':main()
