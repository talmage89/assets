"""Actual shader evaluation repairs bounded misses, never distant surfaces."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
import numpy as np
from kit.lod_transfer import repair,raster


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    from kit import gpu
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=1
    def plane(name,z):
        mesh=bpy.data.meshes.new(name);mesh.from_pydata([(0,0,z),(1,0,z),(1,1,z),(0,1,z)],[],[(0,1,2,3)]);mesh.update()
        uv=mesh.uv_layers.new(name='LOD_SourceUV0');uv.data.foreach_set('uv',np.array([[0,0],[1,0],[1,1],[0,1]],np.float32).ravel())
        ob=bpy.data.objects.new(name,mesh);sc.collection.objects.link(ob);return ob
    source=plane('source',0);target=plane('target',.02)
    mat=bpy.data.materials.new('original shader');mat.use_nodes=True;source.data.materials.append(mat)
    nt=mat.node_tree;bsdf=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output');emit=nt.nodes.new('ShaderNodeEmission')
    uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='LOD_SourceUV0';split=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(uv.outputs[0],split.inputs[0])
    color=nt.nodes.new('ShaderNodeCombineColor');nt.links.new(split.outputs[0],color.inputs[0]);color.inputs[1].default_value=.2
    nt.links.new(color.outputs[0],bsdf.inputs['Base Color'])
    def route(channel):
        if channel in ('NormalField','CoatNormalField'):
            geometry=nt.nodes.new('ShaderNodeNewGeometry');encode=nt.nodes.new('ShaderNodeVectorMath');encode.operation='MULTIPLY_ADD'
            encode.inputs[1].default_value=(.5,.5,.5);encode.inputs[2].default_value=(.5,.5,.5)
            socket=bsdf.inputs['Coat Normal' if channel=='CoatNormalField' else 'Normal']
            nt.links.new(socket.links[0].from_socket if socket.is_linked else geometry.outputs['Normal'],encode.inputs[0])
            nt.links.new(encode.outputs[0],emit.inputs['Color']);nt.links.new(emit.outputs[0],out.inputs['Surface']);return
        for link in list(emit.inputs['Color'].links):nt.links.remove(link)
        if channel=='BaseColor':nt.links.new(color.outputs[0],emit.inputs['Color'])
        else:emit.inputs['Color'].default_value={'Alpha':(1,1,1,1),'ORM':(.6,.2,.1,1),'Emission':(0,0,0,1)}[channel]
        nt.links.new(emit.outputs[0],out.inputs['Surface'])
    size=16;mask=np.zeros((size,size),bool)
    for yy,xx,*unused in raster(target,size):mask[yy,xx]=True
    arrays={k:np.zeros((size,size,1 if k=='Alpha' else 3),np.float32) for k in ['BaseColor','Alpha','ORM','Emission','Normal']}
    result=repair(source,target,arrays,mask,size,.03,route,batch_size=128)
    assert result['repaired']==size*size,result
    assert .0199<result['max_distance_m']<.0201,result
    assert np.max(np.abs(arrays['Alpha']-1))<1e-5
    assert np.max(np.abs(arrays['BaseColor'][:,:,0]-(np.arange(size)+.5)[None,:]/size))<1e-4
    assert np.max(np.abs(arrays['BaseColor'][:,:,1]-.2))<1e-4
    assert np.max(np.abs(arrays['ORM']-np.array([.6,.2,.1])))<1e-4
    assert np.max(np.abs(arrays['Normal']-np.array([.5,.5,1])))<1e-4
    # An oblique cage and a non-axis-aligned original shading normal must
    # reconstruct the original world direction after its tangent-space bake.
    # Unit length and blue-map variation alone do not prove this transport.
    target.rotation_euler.y=.35;bpy.context.view_layer.update()
    wanted=np.array([.24,.18,.95]);wanted/=np.linalg.norm(wanted)
    direction=nt.nodes.new('ShaderNodeCombineXYZ')
    for socket,value in zip(direction.inputs,wanted):socket.default_value=float(value)
    nt.links.new(direction.outputs[0],bsdf.inputs['Normal'])
    oblique={k:np.zeros_like(v) for k,v in arrays.items()}
    oblique['CoatNormal']=np.zeros_like(oblique['Normal'])
    result=repair(source,target,oblique,mask,size,.5,route)
    assert result['repaired']==size*size,result
    for yy,xx,p,n,t,b,footprint in raster(target,size):
        tangent=oblique['Normal'][yy,xx]*2-1
        world=t*tangent[:,0,None]+b*tangent[:,1,None]+n*tangent[:,2,None]
        assert np.max(np.abs(world-wanted))<1e-4,(world.min(axis=0),world.max(axis=0),wanted)
        coat=oblique['CoatNormal'][yy,xx]*2-1
        coatworld=t*coat[:,0,None]+b*coat[:,1,None]+n*coat[:,2,None]
        assert np.max(np.abs(coatworld-[0,0,1]))<1e-4,'coat normal incorrectly reused base normal'
    target.rotation_euler.y=0;nt.nodes.remove(direction);bpy.context.view_layer.update()
    # A ray may hit an opaque neighbor: alpha alone cannot identify the wrong
    # surface. The baked source position makes that false hit measurable.
    arrays['Position']=np.full((size,size,3),-.2);arrays['BaseColor'][:]=1
    result=repair(source,target,arrays,mask,size,.03,route,batch_size=128)
    assert result['repaired']==size*size,result
    assert np.max(np.abs(arrays['BaseColor'][:,:,0]-(np.arange(size)+.5)[None,:]/size))<1e-4
    assert np.max(np.abs(arrays['Position'][:,:,2]))<1e-6
    # Both a hidden lining and the paint above it can face outward. A reduced
    # cage between them is closer to the lining, but must carry the visible
    # exterior paint. Hemisphere filtering alone chooses the wrong layer.
    exterior=bpy.data.meshes.new('paint over hidden lining')
    exterior.from_pydata([(0,0,.015),(1,0,.015),(1,1,.015),(0,1,.015),(0,0,.03),(1,0,.03),(1,1,.03),(0,1,.03)],[],[(0,1,2,3),(4,5,6,7)]);exterior.update()
    layer=exterior.uv_layers.new(name='LOD_SourceUV0');layer.data.foreach_set('uv',np.array([[.99,.99]]*4+[[0,0],[1,0],[1,1],[0,1]],np.float32).ravel())
    exterior.materials.append(mat);previous=source.data;source.data=exterior
    arrays['Alpha'][:]=0
    result=repair(source,target,arrays,mask,size,.03,route)
    assert result['repaired']==size*size,result
    assert np.max(np.abs(arrays['BaseColor'][:,:,0]-(np.arange(size)+.5)[None,:]/size))<1e-4,'hidden lining replaced visible paint'
    assert np.max(np.abs(arrays['Position'][:,:,2]-.03))<1e-6
    source.data=previous;arrays['Alpha'][:]=0
    result=repair(source,target,arrays,mask,size,.03,route)
    assert repair(source,target,arrays,mask,size,.03,route)['candidates']==0
    # The nearest back side of a thin part is not the matching outward
    # surface. Give that side a deliberately different UV field.
    mesh=bpy.data.meshes.new('two-sided correspondence')
    mesh.from_pydata([(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,.015),(1,0,.015),(1,1,.015),(0,1,.015)],[],[(0,1,2,3),(4,7,6,5)]);mesh.update()
    layer=mesh.uv_layers.new(name='LOD_SourceUV0');layer.data.foreach_set('uv',np.array([[0,0],[1,0],[1,1],[0,1]]+[[.99,.99]]*4,np.float32).ravel())
    mesh.materials.append(mat);source.data=mesh;arrays['Alpha'][:]=0
    result=repair(source,target,arrays,mask,size,.03,route)
    assert result['repaired']==size*size,result
    assert np.max(np.abs(arrays['BaseColor'][:,:,0]-(np.arange(size)+.5)[None,:]/size))<1e-4
    assert np.max(np.abs(arrays['Position'][:,:,2]))<1e-6
    arrays['Alpha'][:]=0;target.location.z=.1;bpy.context.view_layer.update()
    result=repair(source,target,arrays,mask,size,.03,route)
    assert result['candidates']==0 and not arrays['Alpha'].any(),result
    # A tiny source chart next to unrelated texels must not be extrapolated
    # across by a coarse target texel's repair footprint.
    blue=plane('small original blue chart',0);blue.data.materials.append(mat)
    uv=blue.data.uv_layers['LOD_SourceUV0']
    for item in uv.data:item.uv=item.uv*.2+__import__('mathutils').Vector((.4,.4))
    texture=bpy.data.images.new('original chart with unrelated surroundings',width=128,height=128,alpha=True,float_buffer=True)
    pixels=np.ones((128,128,4),np.float32);pixels[:,:,:3]=(.8,.1,.1);pixels[50:79,50:79,:3]=(.05,.2,.8);texture.pixels.foreach_set(pixels.ravel())
    color=nt.nodes.new('ShaderNodeTexImage');color.image=texture;uvnode=nt.nodes.new('ShaderNodeUVMap');uvnode.uv_map='LOD_SourceUV0';nt.links.new(uvnode.outputs[0],color.inputs['Vector'])
    target.location=(-1,-1,0);target.scale=(3,3,1);bpy.context.view_layer.update()
    tiny_arrays={k:np.zeros((1,1,v.shape[2]),np.float32) for k,v in arrays.items()}
    result=repair(blue,target,tiny_arrays,np.ones((1,1),bool),1,.03,route)
    assert result['repaired']==1,result
    assert np.max(np.abs(tiny_arrays['BaseColor'][0,0]-[.05,.2,.8]))<.01,('source chart extrapolated into unrelated texels',tiny_arrays['BaseColor'])
    print('LOD TRANSFER PASS: original shader UV fields, tangent normal frame, bounded distance, batching')

if __name__=='__main__':main()
