"""Bake prepared procedural channels directly on the finalized SUV surface.

No projection ray can hit a sheet's back, a gauge rim or a nearby optic. Original
object/generated/print coordinates are ordinary attributes stored before UV work.
The accepted body normal fields remain geometry data. Fine relief is derived
from an emitted meter-height atlas with physical UV Jacobians, preserving tire
lettering even when attribute-coordinate shader differentials are unavailable.
"""
import argparse,json,sys,time
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from kit.bake import require_attribute_coordinates
from kit.image_io import write_png,linear_to_srgb


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=24)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));sc=bpy.context.scene
    meshes=[o for o in sc.objects if o.type=='MESH' and o.get('asset_set')=='SUV' and (not o.name.startswith('Tire_') or o.name=='Tire_FR')]
    materials={m for ob in meshes for m in ob.data.materials if m};require_attribute_coordinates(materials)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in meshes:ob.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();target=meshes[0]
    for ob in list(sc.objects):
        if ob!=target:bpy.data.objects.remove(ob,do_unlink=True)
    uv=target.data.uv_layers['BakeUV'];target.data.uv_layers.active=uv;uv.active_render=True
    nodes={}
    for mat in materials:
        node=mat.node_tree.nodes.new('ShaderNodeTexImage');mat.node_tree.nodes.active=node;nodes[mat]=node
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
    sc.render.bake.use_selected_to_active=False;sc.render.bake.use_clear=True;sc.render.bake.margin=12;sc.render.bake.margin_type='EXTEND'
    if not sc.world:sc.world=bpy.data.worlds.new('X220 bake world')
    if hasattr(sc.world,'light_settings'):sc.world.light_settings.distance=.03
    mask=Image.new('L',(a.size,a.size),0);draw=ImageDraw.Draw(mask);target.data.calc_loop_triangles()
    for tri in target.data.loop_triangles:draw.polygon([(float(uv.data[i].uv.x)*a.size,(1-float(uv.data[i].uv.y))*a.size) for i in tri.loops],fill=255)
    interior=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
    stats={};images={}
    def route(channel):
        for mat in materials:
            nt=mat.node_tree
            if channel is None:nt.links.new(nt.nodes['SURFACE'].outputs[0],nt.nodes['OUT'].inputs['Surface']);continue
            emission=nt.nodes.get('DIRECT_BAKE') or nt.nodes.new('ShaderNodeEmission');emission.name='DIRECT_BAKE'
            source=nt.nodes.get('OUT_'+channel)
            for link in list(emission.inputs['Color'].links):nt.links.remove(link)
            if source:
                output=source.outputs[0]
                if channel=='height':
                    scaled=nt.nodes.get('HEIGHT_ENCODE') or nt.nodes.new('ShaderNodeMath');scaled.name='HEIGHT_ENCODE';scaled.operation='MULTIPLY_ADD';scaled.inputs[1].default_value=100;scaled.inputs[2].default_value=.5
                    nt.links.new(output,scaled.inputs[0]);output=scaled.outputs[0]
                nt.links.new(output,emission.inputs['Color'])
            elif channel=='paint_coverage':emission.inputs['Color'].default_value=(1,1,1,1)
            else:raise ValueError('Missing direct channel '+channel+' / '+mat.name)
            nt.links.new(emission.outputs[0],nt.nodes['OUT'].inputs['Surface'])
    def bake(name,kind,channel=None):
        image=bpy.data.images.new('Direct '+name,a.size,a.size,alpha=True,float_buffer=True);image.colorspace_settings.name='Non-Color'
        for node in nodes.values():node.image=image
        route(channel);started=time.time();options=dict(type=kind)
        if kind=='NORMAL':options.update(normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
        bpy.ops.object.bake(**options)
        values=np.empty(a.size*a.size*4,np.float32);image.pixels.foreach_get(values);values=np.flipud(values.reshape(a.size,a.size,4)).copy()
        images[name]=values;stats[name]=dict(seconds=time.time()-started,checked_interior_texels=int(interior.sum()),alpha_missed_interior_texels=int(np.count_nonzero(interior&(values[:,:,3]<.5))))
        if name=='Normal':stats[name]['backward_interior_texels']=int(np.count_nonzero(interior&(values[:,:,2]<.499)))
        print('DIRECT_BAKED',name,stats[name],flush=True);bpy.data.images.remove(image)
    bake('BaseColor','EMIT','base');bake('BaseColorAlpha','EMIT','paint_coverage')
    base=np.concatenate([linear_to_srgb(images.pop('BaseColor')[:,:,:3]),images.pop('BaseColorAlpha')[:,:,:1]],axis=2)
    write_png(out/'T_AlderX220_BaseColor.png',base)
    bake('Roughness','EMIT','rough');bake('Metallic','EMIT','metal');bake('AO','AO')
    orm=np.stack([images.pop('AO')[:,:,0],images.pop('Roughness')[:,:,0],images.pop('Metallic')[:,:,0]],axis=2);write_png(out/'T_AlderX220_ORM.png',orm)
    bake('Height','EMIT','height');raw=images.pop('Height');valid_height=raw[:,:,3]>.5;height=(raw[:,:,0]-.5)/100
    write_png(out/'T_AlderX220_Height.png',raw[:,:,:1].repeat(3,axis=2),16)
    from suv_height_normal import derive
    normal,normal_report=derive(target,height,sample_valid=valid_height)
    write_png(out/'T_AlderX220_Normal.png',normal,16)
    stats['Normal']=normal_report
    if any(v.get('alpha_missed_interior_texels',0) for v in stats.values()):raise ValueError('Direct bake has unfilled interior pixels')
    if normal_report['minimum_tangent_z']<=0:raise ValueError('Height normal left its tangent hemisphere')
    stats.update(method='Direct finalized-surface procedural bake; no selected-to-active projection',size=a.size,samples=a.samples,device=sc.cycles.device,source_meshes=len(meshes),source_materials=len(materials))
    (out/'bake-report.json').write_text(json.dumps(stats,indent=2))
if __name__=='__main__':main()
