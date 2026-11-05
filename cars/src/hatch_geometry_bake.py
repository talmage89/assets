"""H120 normal-only projection with atlas-sized gutters and kit isolation.

Material/AO channels bake directly on the actual game surface. This pass only
supplies independently approved high-source geometric normals; it deliberately
uses three-pixel padding instead of the generic baker's twelve-pixel margin.
"""
import argparse,json,runpy,sys,time
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import gpu,bake_groups
from kit.bake import require_attribute_coordinates
from kit.image_io import write_png


def main():
    p=argparse.ArgumentParser();p.add_argument('--low',required=True);p.add_argument('--high',required=True);p.add_argument('--out',required=True);p.add_argument('--config',required=True)
    p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=24)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cfg=runpy.run_path(a.config);roots=cfg['BAKE_POLICY']['moving_roots']
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.low).resolve()));sc=bpy.context.scene;bpy.context.view_layer.update()
    low=[o for o in sc.objects if o.type=='MESH' and o.get('asset_set')=='Hatch'];names={o.name for o in low};spacing=bake_groups.offsets(low,roots,.1)
    for ob in low:
        group=bake_groups.owner(ob,roots);world=ob.matrix_world.copy();world.translation+=spacing.get(group,Vector())
        ob.constraints.clear();ob.parent=None;ob.matrix_world=world
    bpy.ops.object.select_all(action='DESELECT')
    for ob in low:ob.select_set(True)
    bpy.context.view_layer.objects.active=low[0];bpy.ops.object.join();target=low[0];target.name='H120 normal atlas target'
    for ob in list(sc.objects):
        if ob!=target:bpy.data.objects.remove(ob,do_unlink=True)
    target.data.materials.clear();mat=bpy.data.materials.new('H120 normal target');mat.use_nodes=True;target.data.materials.append(mat)
    for face in target.data.polygons:face.material_index=0
    uv=target.data.uv_layers['BakeUV'];target.data.uv_layers.active=uv;uv.active_render=True
    image=bpy.data.images.new('H120 geometric normal',a.size,a.size,alpha=True,float_buffer=True);image.colorspace_settings.name='Non-Color'
    node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;mat.node_tree.nodes.active=node
    with bpy.data.libraries.load(str(Path(a.high).resolve()),link=False) as (src,dst):dst.objects=list(src.objects)
    for ob in dst.objects:
        if ob:sc.collection.objects.link(ob)
    bpy.context.view_layer.update();sources=[o for o in dst.objects if o and o.type=='MESH' and o.name in names]
    require_attribute_coordinates({m for o in sources for m in o.data.materials if m})
    # Cache constraint-evaluated matrices before detaching a spring or its target.
    frames={o:o.matrix_world.copy() for o in sources};groups={o:bake_groups.owner(o,roots) for o in sources}
    for ob in sources:
        world=frames[ob];world.translation+=spacing.get(groups[ob],Vector())
        ob.constraints.clear();ob.parent=None;ob.matrix_world=world
    for ob in list(sc.objects):
        if ob!=target and ob not in sources:bpy.data.objects.remove(ob,do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in sources:ob.select_set(True)
    bpy.context.view_layer.objects.active=sources[0];bpy.ops.object.join();high=sources[0]
    target.select_set(True);bpy.context.view_layer.objects.active=target
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
    sc.render.bake.use_selected_to_active=True;sc.render.bake.use_clear=True;sc.render.bake.cage_extrusion=.014;sc.render.bake.max_ray_distance=.040;sc.render.bake.margin=3;sc.render.bake.margin_type='EXTEND'
    started=time.time();bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
    values=np.empty(a.size*a.size*4,np.float32);image.pixels.foreach_get(values);values=np.flipud(values.reshape(a.size,a.size,4)).copy()
    mask=Image.new('L',(a.size,a.size),0);draw=ImageDraw.Draw(mask);target.data.calc_loop_triangles()
    for tri in target.data.loop_triangles:draw.polygon([(float(uv.data[i].uv.x)*a.size,(1-float(uv.data[i].uv.y))*a.size) for i in tri.loops],fill=255)
    interior=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
    missed=int(np.count_nonzero(interior&(values[:,:,3]<.5)));values[values[:,:,3]<.5,:3]=(.5,.5,1)
    write_png(out/'T_AlderH120_Normal.png',values[:,:,:3],16)
    report=dict(method='Isolated high-to-low geometric normal only; exact material channels handled separately',size=a.size,samples=a.samples,device=sc.cycles.device,padding_px=3,source_meshes=len(sources),
        Normal=dict(seconds=time.time()-started,checked_interior_texels=int(interior.sum()),alpha_missed_interior_texels=missed))
    (out/'bake-report.json').write_text(json.dumps(report,indent=2));print('H120_GEOMETRY_BAKE',report)
if __name__=='__main__':main()
