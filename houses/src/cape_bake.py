"""Generate original 4K wall-shingle fields, Cycles bake, filter to 512.

Each half's normal field is authored in its own metric coordinates; baking
through a Normal Map node avoids treating unlike rectangular repeats as a
single square height surface. No photographic image enters this process.
"""
import argparse,json,sys,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]


def bake(size,samples):
    import bpy,numpy as np
    from kit import gpu
    from kit.image_io import write_png,linear_to_srgb
    from cape_shingle_fields import shingle_tile
    source=Path('build/cape/delivery/procedural');shingle_tile(source,size)
    out=Path('textures/cape-bake');out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
    sc.render.engine='CYCLES';sc.cycles.samples=samples;gpu.enable();sc.render.bake.margin=0
    bpy.ops.mesh.primitive_plane_add(size=1.2192);ob=bpy.context.object
    mat=bpy.data.materials.new('CapeShingleBake');mat.use_nodes=True;ob.data.materials.append(mat)
    ns=mat.node_tree.nodes;ls=mat.node_tree.links;output=ns.get('Material Output');report={}
    for channel in ('BaseColor','Normal','ORM'):
        image=bpy.data.images.new('Bake '+channel,width=size,height=size,float_buffer=True);image.colorspace_settings.name='Non-Color'
        target=ns.new('ShaderNodeTexImage');target.image=image;ns.active=target
        texture=ns.new('ShaderNodeTexImage');texture.image=bpy.data.images.load(str((source/f'T_CapeShingle_{channel}.png').resolve()))
        texture.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
        if channel=='Normal':
            shader=ns.new('ShaderNodeBsdfPrincipled');normal=ns.new('ShaderNodeNormalMap');ls.new(texture.outputs['Color'],normal.inputs['Color']);ls.new(normal.outputs['Normal'],shader.inputs['Normal'])
        else:
            shader=ns.new('ShaderNodeEmission');ls.new(texture.outputs['Color'],shader.inputs['Color'])
        ls.new(shader.outputs[0],output.inputs['Surface'])
        bpy.ops.object.bake(type='NORMAL' if channel=='Normal' else 'EMIT')
        a=np.empty(size*size*4,dtype='float32');image.pixels.foreach_get(a);a=a.reshape(size,size,4)[::-1,:,:3]
        if channel=='BaseColor':a=linear_to_srgb(a)
        path=out/f'T_CapeShingle_{channel}.png';write_png(path,a,bits=16 if channel=='Normal' else 8)
        report[channel]=dict(size=size,bytes=path.stat().st_size)
        ns.remove(target);ns.remove(texture);ns.remove(shader);bpy.data.images.remove(image)
    (out/'bake.json').write_text(json.dumps(dict(engine='CYCLES',size=size,samples=samples,channels=report),indent=2))


def filtered():
    subprocess.run([sys.executable,str(HERE.parents[1]/'kit/downsample.py'),'--source','textures/cape-bake','--out','textures/cape-ship','--asset','CapeShingle','--size','512'],check=True)
    from kit.image_io import read_png,write_png
    folder=Path('textures/cape-ship');rows=[]
    for channel in ('BaseColor','Normal','ORM'):
        source=folder/f'T_CapeShingle_{channel}.png';a=read_png(source)
        for name,region in (('CapeCement',a[:256]),('CapeCedar',a[256:])):
            path=folder/f'T_{name}_{channel}.png';write_png(path,region)
            rows.append(dict(path=str(path),width=512,height=256,bytes=path.stat().st_size))
        source.unlink()
    (folder/'regions.json').write_text(json.dumps(dict(images=rows,gpu_mib=1,method='Exact integer crop of filtered baked regions; ordinary repeating UVs, same allocation as one 512-square triple'),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('bake','filter'));p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=8)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    bake(a.size,a.samples) if a.stage=='bake' else filtered()
