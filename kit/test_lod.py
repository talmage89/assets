"""Real Blender LOD fixture: splits, UV1, Wind, pivots, external/embedded maps.

Run from a fresh process: blender -b --factory-startup --python-exit-code 1
--python kit/test_lod.py. No GPU/bake required. Generated files: build/lod-test.
"""
import copy
import json
import sys
from pathlib import Path

import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod_io import Document,digest,distance
from kit.lod_mesh import simplify_parts,topology
from kit.lod import build,check
from kit.image_io import write_png


def main():
    out=ROOT/'build/lod-test';out.mkdir(parents=True,exist_ok=True)
    texture=out/'map.png';write_png(texture,np.ones((8,8,3),np.float32)*.4)
    # A planar tessellated panel with affine UVs/data is an exact reduction.
    n=12;pos=np.array([(x/n,y/n,0) for y in range(n+1) for x in range(n+1)],np.float32)
    faces=[]
    for y in range(n):
        for x in range(n):
            i=y*(n+1)+x;faces.extend([(i,i+1,i+n+2),(i,i+n+2,i+n+1)])
    faces=np.array(faces,np.uint32)
    uv=pos[:,:2];wind=np.column_stack((uv,uv[:,0]*0,uv[:,1]))
    attrs=dict(POSITION=pos,NORMAL=np.tile((0,0,1),(len(pos),1)).astype(np.float32),
               TANGENT=np.tile((1,0,0,1),(len(pos),1)).astype(np.float32),
               TEXCOORD_0=uv,TEXCOORD_1=uv*3,_WIND=wind.astype(np.float32))
    reduced,tris,report=simplify_parts(attrs,faces,.4,.0001,.0001)
    assert len(tris)<len(faces)*.8,report
    assert topology(reduced,tris)[0]['winding_disagreements']==0
    assert np.max(np.abs(reduced['_WIND'][:,0]-reduced['POSITION'][:,0]))<1e-5
    # Explicit corner split: independent chart on half the panel.
    flat={k:a[faces.ravel()] for k,a in attrs.items()}
    split_faces=np.arange(len(faces)*3,dtype=np.uint32).reshape(-1,3)
    flat['TEXCOORD_0'][len(flat['POSITION'])//2:,0]+=2
    a2,f2,r2=simplify_parts(flat,split_faces,.6,.0001,.0001)
    assert len(f2)<=len(split_faces)
    assert set(a2)==set(attrs)
    # Skin data is retained exactly, even when a ratio asks for reduction.
    skin={**attrs,'JOINTS_0':np.zeros((len(pos),4),np.uint16),
          'WEIGHTS_0':np.tile((1,0,0,0),(len(pos),1)).astype(np.float32)}
    aa,ff,_=simplify_parts(skin,faces,.1,.1,.1)
    assert np.array_equal(ff,faces) and np.array_equal(aa['WEIGHTS_0'],skin['WEIGHTS_0'])
    # Build an original stock glTF with extras and full socket transform.
    stub=out/'stub.gltf'
    stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0,2])],
       nodes=[dict(name='Door',mesh=0,translation=[.2,.4,.1],extras=dict(pivot_axis='Y',range_degrees=[0,90]),children=[1]),
              dict(name='Socket',translation=[.1,.2,.3],rotation=[0,0,.70710678,.70710678],extras=dict(socket_kind='hand')),
              dict(name='Static',mesh=1,translation=[2,0,0])],
       meshes=[dict(name=name,primitives=[dict(attributes={},indices=0,material=0)]) for name in ['Panel','StaticPanel']],
       accessors=[],buffers=[],bufferViews=[],materials=[dict(name='Original',extras=dict(custom='retained'),
          pbrMetallicRoughness=dict(baseColorTexture=dict(index=0)))],
       images=[dict(name='BaseColor',uri='map.png')],textures=[dict(source=0)])))
    doc=Document(stub)
    for mesh in doc.data['meshes']:doc.replace(mesh['primitives'][0],attrs,faces)
    source=out/'fixture.gltf';doc.save(source)
    before=Document(source).dependencies()
    embedded=Document(source);embedded.buffers.append(texture.read_bytes())
    embedded.data['bufferViews'].append(dict(buffer=len(embedded.buffers)-1,byteOffset=0,byteLength=texture.stat().st_size))
    embedded.data['images'][0]=dict(name='BaseColor',mimeType='image/png',bufferView=len(embedded.data['bufferViews'])-1)
    roundtrip=out/'copy.glb';embedded.save(roundtrip)
    second=Document(roundtrip);assert second.data['nodes']==Document(source).data['nodes']
    assert second.image(0)==texture.read_bytes()
    assert np.array_equal(second.arrays(second.data['meshes'][0]['primitives'][0])[0]['_WIND'],wind.astype(np.float32))
    assert Document(source).stats()['texture_gpu_bytes']==112 # 8² + 4² + 2² + 1², block rounded
    try:Document(source).save(source)
    except ValueError:pass
    else:raise AssertionError('Overwrote LOD0')
    alias=out/'alias.gltf';alias.write_bytes(source.read_bytes())
    try:Document(alias).save(source)
    except ValueError:pass
    else:raise AssertionError('Overwrote a referenced source BIN through an alias')
    from kit.lod import textures
    generated=textures(second,out/'reduced-map',4)[0];expected_map=digest(generated)
    generated.write_bytes(b'interrupted PNG write')
    textures(second,out/'reduced-map',4)
    assert digest(generated)==expected_map,'Did not repair truncated generated image'
    asset=out/'asset';(asset/'src').mkdir(parents=True,exist_ok=True)
    config=asset/'src/lod.json';config.write_text(json.dumps(dict(kind='fixture',source='../fixture.gltf',
          output='lod',levels=[dict(ratio=.5,screen_height=.2),dict(ratio=.25,screen_height=.08)])))
    build(config);check(config,require_renders=False)
    from kit.lod_normals import audit as audit_normals
    audit_normals(config)
    manifest=(asset/'lod/manifest.json').read_bytes()
    generated={p.name:digest(p) for p in (asset/'lod').glob('*') if p.is_file() and p.suffix in ('.gltf','.bin')}
    build(config)
    assert manifest==(asset/'lod/manifest.json').read_bytes(),'nondeterministic manifest'
    assert generated=={p.name:digest(p) for p in (asset/'lod').glob('*') if p.is_file() and p.suffix in ('.gltf','.bin')}
    assert before==Document(source).dependencies(),'LOD0 mutated'
    # An actual imported skin creates Blender's bone-display helper mesh. It
    # must not enter counts/rendering. Preserve bind data, weights and a clip.
    sd=Document(source);sd.data['nodes'].append(dict(name='Joint'))
    sd.data['scenes'][0]['nodes'].append(3)
    sd.data['nodes'][2].pop('translation',None);sd.data['nodes'][2]['skin']=0
    sd.replace(sd.data['meshes'][1]['primitives'][0],skin,faces)
    def accessor(values,kind):
        i=len(sd.data['accessors']);desc=dict(componentType=5126,count=len(values),type=kind)
        if kind=='SCALAR':desc.update(min=np.min(values,axis=0).tolist(),max=np.max(values,axis=0).tolist())
        sd.data['accessors'].append(desc)
        sd.replacements[i]=np.asarray(values,np.float32);return i
    bind=accessor(np.eye(4).reshape(1,16),'MAT4')
    sd.data['skins']=[dict(joints=[3],skeleton=3,inverseBindMatrices=bind)]
    times=accessor([[0],[1]],'SCALAR');translations=accessor([[0,0,0],[0,.1,0]],'VEC3')
    sd.data['animations']=[dict(name='SkinMove',samplers=[dict(input=times,output=translations,interpolation='LINEAR')],
          channels=[dict(sampler=0,target=dict(node=3,path='translation'))])]
    skinned=out/'skinned.gltf';sd.save(skinned)
    skinconfig=asset/'src/skin-lod.json';skinconfig.write_text(json.dumps(dict(kind='skin fixture',source='../skinned.gltf',
          output='lod-skin',levels=[dict(ratio=.5,screen_height=.2)])))
    build(skinconfig);check(skinconfig,require_renders=False)
    delivered=Document(asset/'lod-skin/skinned_LOD1.gltf')
    assert delivered.data['animations'][0]['name']=='SkinMove'
    ap=delivered.data['animations'][0]['samplers'][0]
    assert np.array_equal(delivered.accessor(ap['output']),np.array([[0,0,0],[0,.1,0]],np.float32))
    # A damaged delivered winding must be rejected independently of its hash.
    manifest_path=asset/'lod/manifest.json';original_manifest=manifest_path.read_bytes()
    data=json.loads(original_manifest);row=data['levels'][1]
    corrupted=Document(asset/'lod'/row['path']);pr=corrupted.data['meshes'][1]['primitives'][0]
    values,indices=corrupted.arrays(pr);corrupted.replace(pr,values,indices[:,::-1])
    broken=asset/'lod/broken.gltf';corrupted.save(broken)
    row['path']=broken.name;row['sha256']=digest(broken)
    manifest_path.write_text(json.dumps(data))
    try:
        try:check(config,require_renders=False)
        except RuntimeError:pass
        else:raise AssertionError('Flipped faces accepted')
    finally:manifest_path.write_bytes(original_manifest)
    data=json.loads(original_manifest);row=data['levels'][1]
    wrong=Document(asset/'lod'/row['path']);pr=wrong.data['meshes'][1]['primitives'][0]
    values,indices=wrong.arrays(pr);values['NORMAL'][0]*=-1;wrong.replace(pr,values,indices)
    bad=asset/'lod/wrong-normal.gltf';wrong.save(bad);row['path']=bad.name
    manifest_path.write_text(json.dumps(data))
    try:
        try:audit_normals(config)
        except RuntimeError:pass
        else:raise AssertionError('Reversed vertex normal accepted')
    finally:manifest_path.write_bytes(original_manifest)
    audit_normals(config)
    # Negative stale-resource control must fail before rebuilding anything.
    raw=texture.read_bytes();texture.write_bytes(raw+b'changed')
    try:
        try:build(config)
        except ValueError:pass
        else:raise AssertionError('Changed source texture accepted')
    finally:texture.write_bytes(raw)
    assert abs(distance(2,.1)-17.32050807568877)<1e-10
    for value in [0,-.1,2]:
        try:distance(1,value)
        except ValueError:pass
        else:raise AssertionError('Invalid switch accepted')
    # Quaternion-mode imported objects still face the camera; atlas sector is
    # selected without changing alpha or relying on an Euler property ignored
    # by the active rotation mode.
    from kit.lod_impostor import pose
    from mathutils import Vector
    import math
    mesh=bpy.data.meshes.new('billboard fixture')
    mesh.from_pydata([(0,0,0),(1,0,0),(1,0,1),(0,0,1)],[],[(0,1,2,3)])
    uv=mesh.uv_layers.new();uv.data.foreach_set('uv',[0,.75,.125,.75,.125,1,0,1])
    ob=bpy.data.objects.new('billboard fixture',mesh);bpy.context.scene.collection.objects.link(ob)
    ob.rotation_mode='QUATERNION'
    for k,v in dict(lod_billboard=True,sectors=32,columns=8,rows=4).items():ob[k]=v
    pose(55);bpy.context.view_layer.update()
    normal=ob.matrix_world.to_3x3()@Vector((0,-1,0))
    assert normal.dot(Vector((math.sin(math.radians(55)),-math.cos(math.radians(55)),0)))>.99999
    assert min(x.uv.x for x in uv.data)>=.625
    from kit.lod_render import compare
    image=np.zeros((16,16,4),np.float32);image[4:12,4:12]=1
    metric,_=compare(image,image);assert metric['mean']==0 and metric['alpha_mae']==0
    changed=image.copy();changed[4:8,4:12]=0
    metric,_=compare(image,changed);assert metric['alpha_mae']>.1
    print('LOD FIXTURE PASS: exact planar reduction, corner splits, UV1, Wind, skin retention, pivots, deterministic bytes, stale-source rejection')


if __name__=='__main__':main()
