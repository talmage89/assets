"""Actual Cycles shader proof for supplied glTF normal/tangent rest frames."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
import numpy as np
from kit.lod_io import Document
from kit.lod_shading import restore,CONVERT
from kit.image_io import write_png,read_png


def main():
    from kit import gpu
    out=Path(__file__).resolve().parents[1]/'build/lod-shading-test';out.mkdir(parents=True,exist_ok=True)
    vectors={'base':np.array([.3,.4,np.sqrt(.75)]),'coat':np.array([-.25,.2,np.sqrt(1-.25**2-.2**2)])}
    for label,vector in vectors.items():write_png(out/(label+'.png'),np.broadcast_to(vector*.5+.5,(8,8,3)).copy())
    vectors={k:read_png(out/(k+'.png'))[0,0,:3]*2-1 for k in vectors}
    stub=out/'stub.gltf'
    stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0])],nodes=[dict(name='FramePanel',mesh=0)],meshes=[dict(primitives=[dict(attributes={},indices=0,material=0)])],accessors=[],buffers=[],bufferViews=[],
        materials=[dict(name='FrameFields',pbrMetallicRoughness=dict(baseColorFactor=[.3,.3,.3,1],metallicFactor=0,roughnessFactor=.8),normalTexture=dict(index=0),extensions={'KHR_materials_clearcoat':dict(clearcoatFactor=.5,clearcoatNormalTexture=dict(index=1))})],
        images=[dict(uri='base.png'),dict(uri='coat.png')],textures=[dict(source=0),dict(source=1)],extensionsUsed=['KHR_materials_clearcoat'])))
    positions=np.array([[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]],np.float32)
    faces=np.array([[0,1,2],[0,2,3]],np.uint32)
    records=[]
    def fixture(label,tangent,hand=1,placed=False):
        doc=Document(stub)
        attrs=dict(POSITION=positions,NORMAL=np.tile([0,0,1],(4,1)).astype(np.float32),
                   TANGENT=np.tile([*tangent,hand],(4,1)).astype(np.float32),TEXCOORD_0=np.array([[0,1],[1,1],[1,0],[0,0]],np.float32))
        doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,faces)
        if placed:doc.data['nodes'][0].update(translation=[2,1,-3],rotation=[0,np.sin(np.pi/4),0,np.cos(np.pi/4)])
        path=out/(label+'.gltf');doc.save(path);return path
    def bake(path,adapt,label,channel):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
        receipt=restore(Document(path)) if adapt else None
        ob=bpy.data.objects['FramePanel'];mat=ob.data.materials[0];nt=mat.node_tree
        bsdf=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');slot=bsdf.inputs['Normal' if channel=='base' else 'Coat Normal']
        field=slot.links[0].from_socket
        encode=nt.nodes.new('ShaderNodeVectorMath');encode.operation='MULTIPLY_ADD';encode.inputs[1].default_value=(.5,.5,.5);encode.inputs[2].default_value=(.5,.5,.5);nt.links.new(field,encode.inputs[0])
        emission=nt.nodes.new('ShaderNodeEmission');nt.links.new(encode.outputs[0],emission.inputs['Color']);output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');nt.links.new(emission.outputs[0],output.inputs['Surface'])
        image=bpy.data.images.new('Actual delivered frame',width=32,height=32,alpha=True,float_buffer=True);image.colorspace_settings.name='Non-Color'
        active=nt.nodes.new('ShaderNodeTexImage');active.image=image;nt.nodes.active=active
        sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=1;sc.cycles.use_denoising=False
        sc.render.bake.use_selected_to_active=False;sc.render.bake.margin=0
        bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
        bpy.context.view_layer.update();bpy.ops.object.bake(type='EMIT')
        data=np.empty(32*32*4,np.float32);image.pixels.foreach_get(data);data=data.reshape(32,32,4)
        mask=data[:,:,3]>.99;actual=data[:,:,:3][mask]*2-1;actual/=np.maximum(np.linalg.norm(actual,axis=1,keepdims=True),1e-20)
        write_png(out/(label+'-'+channel+'.png'),data[::-1]);return actual,receipt
    cases=[('aligned',[1,0,0],1,False),('rotated',[0,1,0],1,False),('mirrored',[0,1,0],-1,False),('placed',[0,1,0],1,True)]
    for label,tangent,hand,placed in cases:
        path=fixture(label,tangent,hand,placed);doc=Document(path);matrix=doc.world(0)
        for channel,value in vectors.items():
            t=np.array(tangent,float);n=np.array([0,0,1.]);b=np.cross(n,t)*hand
            expected=(t*value[0]+b*value[1]+n*value[2])@matrix[:3,:3].T@CONVERT.T;expected/=np.linalg.norm(expected)
            actual,receipt=bake(path,True,label+'-restored',channel)
            error=float(np.max(np.abs(actual-expected)));assert error<2e-5,(label,channel,error,receipt)
            records.append(dict(case=label,channel=channel,max_vector_error=error,receipt=receipt))
            if label in ('aligned','rotated'):
                native,_=bake(path,False,label+'-native',channel)
                if label=='aligned':assert np.max(np.abs(native-actual))<2e-5
                else:assert np.max(np.abs(native-actual))>.2
    (out/'report.json').write_text(json.dumps(records,indent=2)+'\n')
    print('LOD PROVIDED SHADING FRAME FIXTURE PASS',max(r['max_vector_error'] for r in records),flush=True)


if __name__=='__main__':main()
