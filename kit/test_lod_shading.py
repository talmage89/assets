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


def sidedness_fixture(out):
    """Measure actual front/back visibility, rather than importer flags."""
    from kit import gpu
    from mathutils import Vector
    from PIL import Image
    stub=out/'sidedness-stub.gltf'
    stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0])],
        nodes=[dict(name='SidedPanel',mesh=0)],meshes=[dict(primitives=[dict(attributes={},indices=0,material=0)])],
        accessors=[],buffers=[],bufferViews=[],materials=[dict(name='SidedMaterial',emissiveFactor=[.2,.4,.6],
        pbrMetallicRoughness=dict(baseColorFactor=[0,0,0,1],metallicFactor=0,roughnessFactor=1))])))
    attrs=dict(POSITION=np.array([[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]],np.float32),
               NORMAL=np.tile([0,0,1],(4,1)).astype(np.float32))
    faces=np.array([[0,1,2],[0,2,3]],np.uint32);records=[]
    for label,double,y,expected in [('single-front',False,-3,1),('single-back',False,3,0),('double-back',True,3,1)]:
        doc=Document(stub);doc.data['materials'][0]['doubleSided']=double
        doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,faces)
        path=out/(label+'.gltf');doc.save(path)
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
        receipt=restore(Document(path));assert receipt['one_sided_materials']==int(not double),receipt
        material=bpy.data.objects['SidedPanel'].data.materials[0];count=len(material.node_tree.nodes)
        restore(Document(path));assert len(material.node_tree.nodes)==count,'Repeated restoration wrapped material twice'
        sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=1
        sc.cycles.use_denoising=False;sc.render.resolution_x=64;sc.render.resolution_y=64
        sc.render.resolution_percentage=100;sc.render.film_transparent=True
        sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
        sc.render.threads_mode='FIXED';sc.render.threads=4
        camera=bpy.data.objects.new('Sidedness camera',bpy.data.cameras.new('Sidedness camera'))
        sc.collection.objects.link(camera);sc.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=3
        camera.location=(0,y,0);camera.rotation_euler=(-Vector(camera.location)).to_track_quat('-Z','Y').to_euler()
        image=out/(label+'.png');sc.render.filepath=str(image);bpy.ops.render.render(write_still=True)
        alpha=float(np.asarray(Image.open(image).convert('RGBA'),np.float32)[24:40,24:40,3].mean()/255)
        assert abs(alpha-expected)<1e-6,(label,alpha,expected)
        records.append(dict(case=label,center_alpha=alpha,expected_alpha=expected,receipt=receipt))
    (out/'sidedness.json').write_text(json.dumps(records,indent=2)+'\n')
    print('LOD GLTF SIDEDNESS PASS',records,flush=True)


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
        # EMIT leaves opaque black outside atlas charts; alpha alone is not a
        # coverage mask. Measure only independently rasterized mesh UV texels.
        from kit.lod_transfer import raster as uv_raster
        mask=np.zeros((32,32),bool)
        for yy,xx,*unused in uv_raster(ob,32):mask[31-yy,xx]=True
        mask &= data[:,:,3]>.99
        actual=data[:,:,:3][mask]*2-1;actual/=np.maximum(np.linalg.norm(actual,axis=1,keepdims=True),1e-20)
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
    # The proxy baker must sample supplied source frames too, not only the
    # final comparison renderer. Re-import its resulting tangent map natively.
    from kit.lod_atlas import bake as bake_atlas
    path=fixture('atlas-source',[0,1,0]);doc=Document(path)
    doc.data['nodes'][0]['extras']=dict(lod_sources=[0])
    delivered=out/'atlas-delivered.gltf'
    transfer=bake_atlas(doc,path,delivered,64,projection_m=.02);doc.save(delivered)
    for channel,value in vectors.items():
        expected=np.array([-value[1],value[0],value[2]])@CONVERT.T
        expected/=np.linalg.norm(expected)
        actual,_=bake(delivered,False,'atlas-native',channel)
        error=float(np.max(np.abs(actual-expected)))
        assert error<.025,('atlas ignored supplied source tangent',channel,error)
        records.append(dict(case='atlas-source',channel=channel,max_vector_error=error,receipt=transfer['source_shading_frame']))

    # Force every texel through the bounded nearest-source patch route. The
    # shader attributes carrying the supplied tangent must survive that route.
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
    restore(Document(path));source=bpy.data.objects['FramePanel']
    source.data.uv_layers.active.name='LOD_SourceUV0'
    mat=source.data.materials[0];nt=mat.node_tree
    for node in nt.nodes:
        if node.type=='NORMAL_MAP':node.uv_map='LOD_SourceUV0'
    bsdf=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
    output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
    emission=nt.nodes.new('ShaderNodeEmission')
    encode=nt.nodes.new('ShaderNodeVectorMath');encode.operation='MULTIPLY_ADD'
    encode.inputs[1].default_value=(.5,.5,.5);encode.inputs[2].default_value=(.5,.5,.5)
    def route(channel):
        color=emission.inputs['Color']
        for link in list(color.links):nt.links.remove(link)
        if channel in ('NormalField','CoatNormalField'):
            slot=bsdf.inputs['Normal' if channel=='NormalField' else 'Coat Normal']
            nt.links.new(slot.links[0].from_socket,encode.inputs[0])
            nt.links.new(encode.outputs[0],color)
        else:color.default_value=(1,1,1,1)
        nt.links.new(emission.outputs[0],output.inputs['Surface'])
    target=source.copy();target.data=source.data.copy();bpy.context.scene.collection.objects.link(target)
    target.location.y-=.02;bpy.context.view_layer.update()
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=1
    from kit.lod_transfer import repair,raster
    arrays=dict(Alpha=np.zeros((16,16,1),np.float32),Normal=np.zeros((16,16,3),np.float32),CoatNormal=np.zeros((16,16,3),np.float32))
    transfer=repair(source,target,arrays,np.ones((16,16),bool),16,.03,route,coverage=True)
    assert transfer['repaired']==256,transfer
    for channel,key in [('base','Normal'),('coat','CoatNormal')]:
        value=vectors[channel];expected=np.array([-value[1],value[0],value[2]])@CONVERT.T;expected/=np.linalg.norm(expected)
        error=0.
        for yy,xx,p,n,t,b,foot in raster(target,16):
            decoded=arrays[key][yy,xx]*2-1
            actual=t*decoded[:,0,None]+b*decoded[:,1,None]+n*decoded[:,2,None]
            actual/=np.linalg.norm(actual,axis=1,keepdims=True)
            error=max(error,float(np.max(np.abs(actual-expected))))
        assert error<2e-4,('nearest patch ignored supplied source tangent',channel,error)
        records.append(dict(case='nearest-source',channel=channel,max_vector_error=error,receipt=transfer))
    (out/'report.json').write_text(json.dumps(records,indent=2)+'\n')
    print('LOD PROVIDED SHADING FRAME FIXTURE PASS',max(r['max_vector_error'] for r in records),flush=True)
    sidedness_fixture(out)


if __name__=='__main__':main()
