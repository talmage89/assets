"""Car-family direct surface bake on the finalized UV skin; no optical projection rays.

Source coordinates are frozen by cars/src/prepare_bake.py. This checkpoint
retains quick channels; fine look development is intentionally deferred.
"""
import argparse,json,sys,time
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import gpu
from kit.bake import require_attribute_coordinates
from kit.image_io import write_png,linear_to_srgb

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=12)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));sc=bpy.context.scene
    obs=[o for o in sc.objects if o.type=='MESH' and o.get('asset_set')=='SchoolBus'];mats={m for o in obs for m in o.data.materials if m};require_attribute_coordinates(mats)
    high=bpy.data.objects.get('Dense front mold')
    if high is None:raise ValueError('Independent dense front mold missing')
    hood=bpy.data.objects['Compound hood shell'];low=hood.copy();low.data=hood.data.copy()
    low.name='Front normal target';sc.collection.objects.link(low);low.hide_render=True
    high.hide_render=True
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs:ob.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();target=obs[0]
    for ob in list(sc.objects):
        if ob not in [target,low,high]:bpy.data.objects.remove(ob,do_unlink=True)
    uv=target.data.uv_layers['BakeUV'];target.data.uv_layers.active=uv;uv.active_render=True
    target.data.calc_loop_triangles();mask=Image.new('L',(a.size,a.size),0);draw=ImageDraw.Draw(mask)
    for tri in target.data.loop_triangles:draw.polygon([(uv.data[i].uv.x*a.size,(1-uv.data[i].uv.y)*a.size) for i in tri.loops],fill=255)
    interior=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
    nodes={}
    for m in mats:n=m.node_tree.nodes.new('ShaderNodeTexImage');m.node_tree.nodes.active=n;nodes[m]=n
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
    sc.render.bake.use_selected_to_active=False;sc.render.bake.use_clear=True;sc.render.bake.margin=8;sc.render.bake.margin_type='EXTEND'
    stats={};channels={}
    def bake(name,kind,channel=None):
        im=bpy.data.images.new('Bus bake '+name,a.size,a.size,alpha=True,float_buffer=True);im.colorspace_settings.name='Non-Color'
        for m in mats:
            nt=m.node_tree;nodes[m].image=im
            if channel:
                em=nt.nodes.get('Bus channel') or nt.nodes.new('ShaderNodeEmission');em.name='Bus channel'
                for link in list(em.inputs['Color'].links):nt.links.remove(link)
                src=nt.nodes.get('OUT_'+channel)
                if src:nt.links.new(src.outputs[0],em.inputs['Color'])
                else:em.inputs['Color'].default_value=(1,1,1,1)
                nt.links.new(em.outputs[0],nt.nodes['OUT'].inputs['Surface'])
            else:nt.links.new(nt.nodes['SURFACE'].outputs[0],nt.nodes['OUT'].inputs['Surface'])
        started=time.time();bpy.ops.object.bake(type=kind,**(dict(normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z') if kind=='NORMAL' else {}))
        values=np.empty(a.size*a.size*4,np.float32);im.pixels.foreach_get(values);values=np.flipud(values.reshape(a.size,a.size,4)).copy();channels[name]=values
        stats[name]=dict(seconds=time.time()-started,checked_interior_texels=int(interior.sum()),missing_alpha_interior=int(np.count_nonzero(interior&(values[:,:,3]<.5))))
        if name=='base':stats[name]['unfilled_black_interior']=int(np.count_nonzero(interior&(np.max(values[:,:,:3],axis=2)<1e-8)))
        if name=='normal':stats[name]['backward_interior']=int(np.count_nonzero(interior&(values[:,:,2]<.499)))
        bpy.data.images.remove(im);print('BUS_BAKE',name,stats[name],flush=True)
    bake('base','EMIT','base');bake('alpha','EMIT','paint_coverage');bake('rough','EMIT','rough');bake('metal','EMIT','metal');bake('ao','AO');bake('normal','NORMAL')
    from front_normal_bake import project
    target.hide_render=True
    geometric,chosen,front_report=project(low,high,a.size,a.samples)
    # Rotate the exact-surface micro-normal into the dense mold's normal frame.
    # Rodrigues' formula uses v = Z cross N and c = Z dot N; this preserves
    # both the material's chips/seams and the sculpted mold curvature.
    direct=channels['normal'][chosen,:3]*2-1;dense=geometric[chosen,:3]*2-1
    dense/=np.maximum(np.linalg.norm(dense,axis=1,keepdims=True),1e-8)
    axis=np.c_[-dense[:,1],dense[:,0],np.zeros(len(dense))]
    rotated=direct+np.cross(axis,direct)+np.cross(axis,np.cross(axis,direct))/np.maximum(1+dense[:,2:3],1e-6)
    rotated/=np.maximum(np.linalg.norm(rotated,axis=1,keepdims=True),1e-8)
    channels['normal'][chosen,:3]=np.clip(rotated*.5+.5,0,1)
    front_report['normal_composition']='Dense geometric normal rotation composed with direct material micro-normal'
    print('BUS_FRONT_NORMAL',front_report,flush=True)
    write_png(out/'T_SchoolBus_BaseColor.png',np.concatenate([linear_to_srgb(channels['base'][:,:,:3]),channels['alpha'][:,:,:1]],axis=2))
    write_png(out/'T_SchoolBus_ORM.png',np.stack([channels['ao'][:,:,0],channels['rough'][:,:,0],channels['metal'][:,:,0]],axis=2))
    nm=channels['normal'];invalid=(nm[:,:,3]<.5)|(nm[:,:,2]<.5);nm[invalid,:3]=(.5,.5,1)
    write_png(out/'T_SchoolBus_Normal.png',nm[:,:,:3],16)
    (out/'bake-report.json').write_text(json.dumps(dict(channels=stats,front_projection=front_report,size=a.size,samples=a.samples,device=sc.cycles.device,method='Frozen-attribute direct surface channels, dense mold normal projection composed on the hood'),indent=2))
    if stats['base']['unfilled_black_interior'] or any(row['missing_alpha_interior'] for row in stats.values()):raise ValueError('Unfilled interior bake texels')
if __name__=='__main__':main()
