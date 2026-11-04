"""Bake the accepted original stone/coping field at 4K; ship one 512 pair."""
import argparse
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]


def bake(size=4096,samples=8):
    import bpy
    import numpy as np
    from kit import gpu
    from kit.image_io import write_png,linear_to_srgb
    from split_atlas import author
    source=Path('build/split/delivery/procedural');author(source)
    out=Path('textures/split-bake');out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
    sc.render.engine='CYCLES';sc.cycles.samples=samples;gpu.enable();sc.render.bake.margin=0
    bpy.ops.mesh.primitive_plane_add(size=1.3716)
    ob=bpy.context.object;mat=bpy.data.materials.new('Original stone bake');mat.use_nodes=True;ob.data.materials.append(mat)
    nt=mat.node_tree;output=nt.nodes.get('Material Output');report=[]
    for channel in ('BaseColor','Normal'):
        image=bpy.data.images.new('Stone bake '+channel,width=size,height=size,float_buffer=True);image.colorspace_settings.name='Non-Color'
        target=nt.nodes.new('ShaderNodeTexImage');target.image=image;nt.nodes.active=target
        texture=nt.nodes.new('ShaderNodeTexImage');texture.image=bpy.data.images.load(str((source/f'T_SplitStone_{channel}.png').resolve()))
        texture.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
        shader=nt.nodes.new('ShaderNodeBsdfPrincipled' if channel=='Normal' else 'ShaderNodeEmission')
        if channel=='Normal':
            normal=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(texture.outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs[0],shader.inputs['Normal'])
        else:nt.links.new(texture.outputs['Color'],shader.inputs['Color'])
        nt.links.new(shader.outputs[0],output.inputs['Surface']);bpy.ops.object.bake(type='NORMAL' if channel=='Normal' else 'EMIT')
        a=np.empty(size*size*4,dtype='float32');image.pixels.foreach_get(a);a=a.reshape(size,size,4)[::-1,:,:3]
        if channel=='BaseColor':a=linear_to_srgb(a)
        path=out/f'T_SplitStone_{channel}.png';write_png(path,a,bits=16 if channel=='Normal' else 8)
        report.append(dict(channel=channel,size=size,bytes=path.stat().st_size))
        nt.nodes.remove(target);nt.nodes.remove(texture);nt.nodes.remove(shader);bpy.data.images.remove(image)
    (out/'bake.json').write_text(json.dumps(dict(engine='CYCLES',size=size,samples=samples,channels=report,source='Original accepted 512 field, GPU resampled at 4096 before channel-correct shipping filter'),indent=2))


def filtered():
    import numpy as np
    from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
    out=Path('textures/split-ship');out.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','Normal'):
        a=read_png(Path('textures/split-bake')/f'T_SplitStone_{channel}.png')
        # Same linear-color/vector-normal box filter as kit/downsample.py;
        # this pair has scalar ORM and deliberately allocates no third map.
        h,w,_=a.shape;assert h==w and h%512==0;factor=h//512
        a=srgb_to_linear(a) if channel=='BaseColor' else a*2-1
        result=a.reshape(512,factor,512,factor,3).mean(axis=(1,3))
        if channel=='BaseColor':result=linear_to_srgb(result)
        else:result=result/np.maximum(np.linalg.norm(result,axis=2,keepdims=True),1e-8)*.5+.5
        write_png(out/f'T_SplitStone_{channel}.png',result)
    (out/'delivery.json').write_text(json.dumps(dict(images=2,size=512,gpu_mib=2/3,scalar_roughness=.91,scalar_metallic=0),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('bake','filter'));p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=8)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    bake(a.size,a.samples) if a.stage=='bake' else filtered()
