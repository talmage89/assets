"""Real immutable-source bake and fresh-import factory decoder regression.

Run serially through with_gpu.sh; clean build/lod-factory-test first.
"""
import copy
import json
import sys
from pathlib import Path
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from kit.lod_io import Document
from kit.lod_atlas import bake
from kit.image_io import write_png, linear_to_srgb, srgb_to_linear
from kit.detachable_verify import _image, sample
from kit.lod_mesh import barycentric


def fixture(out):
    colors = dict(Porcelain=[.78,.79,.76], Carbon=[.009,.011,.013],
                  Aluminum=[.46,.48,.49], Graphite=[.16,.153,.141], Atlantic=[.012,.037,.071])
    metals = dict(Porcelain=0, Carbon=0, Aluminum=.55, Graphite=.42, Atlantic=.12)
    extras = dict(paint_decode='reference_plus_coverage_delta',paint_reference_color=colors['Atlantic'],
                  paint_colors=json.dumps(colors),paint_metallic=json.dumps(metals))
    base=np.array([*linear_to_srgb(np.array(colors['Atlantic'])*.6+[.01,.02,.03]),.6])
    write_png(out/'T_fixture_BaseColor.png',np.tile(base,(4,4,1)))
    write_png(out/'T_fixture_ORM.png',np.tile([1,.4,.75],(4,4,1)))
    materials=[dict(name='Paint',extras=extras,extensions={'KHR_materials_clearcoat':dict(clearcoatFactor=1)},
                    pbrMetallicRoughness=dict(baseColorTexture=dict(index=0),metallicRoughnessTexture=dict(index=1),metallicFactor=.12)),
               dict(name='Trim',pbrMetallicRoughness=dict(baseColorFactor=[.08,.09,.10,1],metallicFactor=.8,roughnessFactor=.6)),
               dict(name='Glass',pbrMetallicRoughness=dict(baseColorFactor=[.1,.2,.3,1],metallicFactor=0,roughnessFactor=.2),
                    extensions={'KHR_materials_transmission':dict(transmissionFactor=.7)}),
               dict(name='Lamps',pbrMetallicRoughness=dict(baseColorTexture=dict(index=0),metallicFactor=0,roughnessFactor=.4),
                    emissiveTexture=dict(index=0),emissiveFactor=[1,1,1],
                    extensions={'KHR_materials_emissive_strength':dict(emissiveStrength=80)},
                    extras=dict(lamp_strength=80,lamp_alpha_semantic='emission_strength_over_80'))]
    stub=out/'stub.gltf';source=out/'source.gltf'
    stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=list(range(4)))],
        nodes=[dict(name=n,mesh=i) for i,n in enumerate(['Paint box','Trim box','Glass box','Lamp box'])],
        meshes=[dict(primitives=[dict(attributes={},indices=0,material=i)]) for i in range(4)],
        materials=materials,images=[dict(uri='T_fixture_BaseColor.png'),dict(uri='T_fixture_ORM.png')],
        textures=[dict(source=0),dict(source=1)],accessors=[],bufferViews=[],buffers=[],
        extensionsUsed=['KHR_materials_clearcoat','KHR_materials_transmission','KHR_materials_emissive_strength'])))
    d=Document(stub)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.mesh.primitive_cube_add(size=.3)
    ob=bpy.context.object;mesh=ob.data;mesh.calc_loop_triangles()
    positions=np.array([v.co[:] for v in mesh.vertices],np.float32)
    ff=np.array([t.vertices[:] for t in mesh.loop_triangles],np.uint32)
    nn=np.cross(positions[ff[:,1]]-positions[ff[:,0]],positions[ff[:,2]]-positions[ff[:,0]])
    nn/=np.linalg.norm(nn,axis=1,keepdims=True)
    for i,m in enumerate(d.data['meshes']):
        attrs=dict(POSITION=positions[ff.ravel()]+[i*.5,0,0],NORMAL=np.repeat(nn,3,axis=0),
                   TEXCOORD_0=np.tile([[.2,.2],[.8,.2],[.5,.8]],(len(ff),1)))
        d.replace(m['primitives'][0],attrs,np.arange(ff.size,dtype=np.uint32).reshape(-1,3))
    d.save(source)
    target=Document(source);target.data['nodes'][0]['extras']=dict(lod_sources=list(range(4)))
    attrs=[];faces=[];offset=0
    for _,_,p in target.primitives():
        a,f=target.arrays(p);attrs.append(a);faces.append(f+offset);offset+=len(a['POSITION'])
    for node in target.data['nodes'][1:]:node.pop('mesh')
    target.data['meshes']=target.data['meshes'][:1]
    target.replace(target.data['meshes'][0]['primitives'][0],
                   {k:np.concatenate([a[k] for a in attrs]) for k in attrs[0]},np.concatenate(faces))
    return source,target,colors,metals


def main():
    out=ROOT/'build/lod-factory-test';out.mkdir(parents=True,exist_ok=True)
    source,target,colors,metals=fixture(out);before=Document(source).dependencies()
    path=out/'proxy.gltf'
    report=bake(target,source,path,128,proxy=True,projection_m=.02,supersample=2,factory_paint=True)
    target.save(path);d=Document(path);assert Document(source).dependencies()==before
    assert d.stats()['materials']==d.stats()['draw_calls']==1
    m=d.data['materials'][0];assert m['extras']['paint_colors']==json.dumps(colors)
    a,f=d.arrays(next(d.primitives())[2])
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    tree=BVHTree.FromPolygons([Vector(v) for v in a['POSITION']],f.tolist(),all_triangles=True)
    uv=[]
    for i in range(4):
        q,n,fi,dist=tree.find_nearest(Vector((i*.5,0,.15)))
        uv.append(barycentric(np.array(q),a['POSITION'][f[fi]].astype(float))@a['TEXCOORD_0'][f[fi]])
    uv=np.array(uv)
    coverage=sample(_image(d.image(d.data['textures'][m['occlusionTexture']['index']]['source'])),uv)
    assert np.max(np.abs(coverage[:,1:3]-[[.6,.75],[0,0],[0,0],[0,0]]))<.025,coverage
    # The general runtime adapter is evaluated after every fresh import.
    # Family integration is checked by each adoption's delivered-decoder probe.
    from kit import lod_factory as decoder
    results=[]
    for preset in colors:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(path))
        paint=decoder.apply(preset,lights=True);nt=paint.node_tree
        bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
        for lights in (False,True):
            decoder.apply(preset,lights=lights)
            assert abs(bs.inputs['Emission Strength'].default_value-(paint['lamp_strength'] if lights else 0))<1e-4
        assert nt.nodes['Factory metallic'].inputs[1].default_value==metals[preset] or abs(nt.nodes['Factory metallic'].inputs[1].default_value-metals[preset])<1e-6
        assert bs.inputs['Metallic'].is_linked and bs.inputs['Base Color'].is_linked
        # Evaluate the installed decoder in Cycles, then independently sample
        # paint, metallic trim, glass and lamp on the serialized proxy charts.
        scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=8
        from kit import gpu
        gpu.enable();scene.render.bake.use_selected_to_active=False;scene.render.bake.margin=0
        ob=next(o for o in scene.objects if o.type=='MESH')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active=ob;ob.select_set(True)
        output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        emit=nt.nodes.new('ShaderNodeEmission');nt.links.new(emit.outputs[0],output.inputs['Surface'])
        texture=nt.nodes.new('ShaderNodeTexImage');nt.nodes.active=texture
        measurements={}
        for key in ('Base Color','Metallic'):
            nt.links.new(bs.inputs[key].links[0].from_socket,emit.inputs['Color'])
            im=bpy.data.images.new('Decoded field',width=128,height=128,float_buffer=True)
            im.colorspace_settings.name='Non-Color';texture.image=im
            bpy.ops.object.bake(type='EMIT')
            pixels=np.empty(128*128*4,np.float32);im.pixels.foreach_get(pixels)
            value=sample(pixels.reshape(128,128,4)[::-1],uv)[:,:3]
            expected=([np.array(colors['Atlantic'])*.6+[.01,.02,.03]+.6*(np.array(colors[preset])-colors['Atlantic']),
                       [.08,.09,.10],[.1,.2,.3],np.array(colors['Atlantic'])*.6+[.01,.02,.03]]
                      if key=='Base Color' else np.repeat([[.75*metals[preset]],[.8],[0],[0]],3,axis=1))
            assert np.max(np.abs(value-expected))<.035,(preset,key,value,expected)
            measurements[key]=dict(actual=value.tolist(),max_error=float(np.max(np.abs(value-expected))))
            bpy.data.images.remove(im)
        results.append(dict(preset=preset,fresh_import=True,lights=[False,True],fields=measurements))
    (out/'proof.json').write_text(json.dumps(dict(bake=report,routing=results,coverage=coverage.tolist()),indent=2)+'\n')
    print('FACTORY FIXTURE PASS: real coverage/metal bake, immutable source, one draw, five fresh imports, both lamp states')


if __name__=='__main__':main()
