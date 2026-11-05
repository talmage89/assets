"""Appearance transfer from immutable delivered glTF onto new LOD charts.

Runs under the shared GPU lock. Each independently moving source/target pair
is translated together before projection, so a door cannot sample its body.
Only imported PBR nodes and shipped images are baked, never high-detail assets.
"""
import copy
import json
import math
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

import bpy
import bmesh
import numpy as np
from mathutils import Matrix
from PIL import Image,ImageFilter

from kit.image_io import write_png,linear_to_srgb
from kit.lod_io import Document,digest

CONVERT=np.array([[1,0,0],[0,0,-1],[0,1,0]],float)


def object_from_arrays(name,attrs,faces,matrix=None):
    """Rebuild split normals and coordinates; return a corner-indexed mesh."""
    mesh=bpy.data.meshes.new(name)
    positions=attrs['POSITION'].astype(float)
    normals=attrs['NORMAL'].astype(float)
    if matrix is not None:
        positions=positions@matrix[:3,:3].T+matrix[:3,3]
        normals=normals@np.linalg.inv(matrix[:3,:3])
        normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-20)
    positions=positions@CONVERT.T;normals=normals@CONVERT.T
    # glTF has split corner vertices. Restore geometric adjacency before
    # unwrap; otherwise every triangle becomes a separate padded UV island.
    _,first,remap=np.unique(np.round(positions,8),axis=0,return_index=True,return_inverse=True)
    mesh.from_pydata(positions[first].tolist(),[],remap[faces].tolist());mesh.update()
    for p in mesh.polygons:p.use_smooth=True
    mesh.normals_split_custom_set(normals[faces.ravel()].tolist())
    ob=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(ob)
    return ob


def bake(doc,source,path,size,*,proxy=False,projection_m=.02,composite_alpha=False):
    """Replace charts/maps, keeping near-level material response and pivots.

    doc extras on each mesh node contain lod_sources (original node indices).
    Source import is read-only. All derived maps are local to the new level.
    """
    from kit import gpu
    source=Path(source);path=Path(path);dest=path.parent/(path.stem+'-maps');dest.mkdir(parents=True,exist_ok=True)
    original=Document(source)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()),import_pack_images=False)
    sc=bpy.context.scene
    source_objects={n.get('name'):bpy.data.objects.get(n.get('name','')) for n in original.data['nodes'] if 'mesh' in n}
    bpy.context.view_layer.update()
    for ob in source_objects.values():
        if ob:
            world=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=world
    # Pin delivered UV indices before joining. In particular, adding a second
    # emission UV layer must not change implicit BaseColor/alpha/normal UV0.
    uv_names={}
    for ob in source_objects.values():
        if not ob:continue
        for i,layer in enumerate(ob.data.uv_layers):
            uv_names[layer.name]='LOD_SourceUV'+str(i);layer.name='LOD_SourceUV'+str(i)
    for material in {m for ob in source_objects.values() if ob for m in ob.data.materials if m}:
        nt=material.node_tree
        for node in list(nt.nodes):
            if node.type=='UVMAP':node.uv_map=uv_names.get(node.uv_map,node.uv_map)
            elif node.type=='NORMAL_MAP':node.uv_map=uv_names.get(node.uv_map,'LOD_SourceUV0')
            elif node.type=='TEX_IMAGE' and not node.inputs['Vector'].is_linked:
                uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='LOD_SourceUV0';nt.links.new(uv.outputs['UV'],node.inputs['Vector'])
    for o in list(sc.objects):
        if o not in source_objects.values():bpy.data.objects.remove(o,do_unlink=True)
    targets=[];records=[];high=[]
    bounds=original.bounds();spacing=float(np.linalg.norm(bounds[1]-bounds[0]))*3+1
    used=set()
    for ni,node in enumerate(doc.data['nodes']):
        if 'mesh' not in node:continue
        source_ids=node.get('extras',{}).get('lod_sources',[ni])
        shift=np.array([len(targets)*spacing,0,0])
        for si in source_ids:
            name=original.data['nodes'][si].get('name');ob=source_objects.get(name)
            if ob is None:continue
            if si in used:raise ValueError('Source node assigned to multiple bake groups')
            used.add(si);high.append(ob)
            world=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=world
            # Freeze skin in the delivered rest pose; its original rig remains
            # in the output document. Imported bone helpers are never sources.
            for mod in list(ob.modifiers):
                if mod.type=='ARMATURE':ob.modifiers.remove(mod)
            ob.matrix_world.translation+=__import__('mathutils').Vector(shift)
        for p in doc.data['meshes'][node['mesh']]['primitives']:
            attrs,faces=doc.arrays(p)
            ob=object_from_arrays('LOD chart target',attrs,faces,np.eye(4) if 'skin' in node else doc.world(ni))
            ob.location+=__import__('mathutils').Vector(shift)
            targets.append(ob);records.append((p,attrs,faces,ob,np.eye(4) if 'skin' in node else doc.world(ni)))
    for si,ob in source_objects.items():
        if ob not in high and ob.name in sc.objects:bpy.data.objects.remove(ob,do_unlink=True)
    if not targets or not high:raise ValueError('Empty atlas projection')
    # A shared UV pack across all parts, with a mip-safe physical gutter.
    bpy.ops.object.select_all(action='DESELECT')
    for ob in targets:ob.select_set(True)
    bpy.context.view_layer.objects.active=targets[0]
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=4/size,correct_aspect=False,scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    for p,attrs,faces,ob,matrix in records:
        uv=np.empty((len(ob.data.loops),2),np.float32);ob.data.uv_layers.active.data.foreach_get('uv',uv.ravel());uv[:,1]=1-uv[:,1]
        # Corner expansion deliberately preserves hard normals and other data.
        new={k:v[faces.ravel()] for k,v in attrs.items() if not k.startswith(('TEXCOORD_','COLOR_')) and k!='TANGENT'}
        new['TEXCOORD_0']=uv
        # Serialize the actual bake cage's split normals, then restore that
        # exact frame after projection-target joining. Edit-mode unwrap and
        # custom-normal encoding must never create a different shipped basis.
        cn=np.array([n.vector[:] for n in ob.data.corner_normals],np.float64)
        new['NORMAL']=(cn@CONVERT@matrix[:3,:3]).astype(np.float32)
        new['NORMAL']/=np.maximum(np.linalg.norm(new['NORMAL'],axis=1,keepdims=True),1e-20)
        layer=ob.data.attributes.new('LOD_BakeNormal','FLOAT_VECTOR','CORNER')
        layer.data.foreach_set('vector',cn.astype(np.float32).ravel())
        keys=list(new);signature=np.concatenate([new[k] for k in keys],axis=1)
        _,first,remap=np.unique(signature,axis=0,return_index=True,return_inverse=True)
        new={k:v[first] for k,v in new.items()}
        doc.replace(p,new,remap.reshape(-1,3).astype(np.uint32))
        p['attributes']={k:v for k,v in p['attributes'].items() if k in new}
    # Join projection targets only after collecting the UVs for serialization.
    bpy.context.view_layer.objects.active=targets[0];bpy.ops.object.join();target=targets[0]
    frame=np.empty((len(target.data.loops),3),np.float32)
    target.data.attributes['LOD_BakeNormal'].data.foreach_get('vector',frame.ravel())
    target.data.normals_split_custom_set(frame.tolist())
    target.data.materials.clear();mat=bpy.data.materials.new('LOD bake target');mat.use_nodes=True
    target.data.materials.append(mat)
    for p in target.data.polygons:p.material_index=0
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');mat.node_tree.nodes.active=tex
    # Joining imported sources preserves their UVs, normal maps and vertex data.
    bpy.ops.object.select_all(action='DESELECT')
    for ob in high:ob.select_set(True)
    bpy.context.view_layer.objects.active=high[0];bpy.ops.object.join();high=high[0]
    mats={m for m in high.data.materials if m}
    hm=np.array(high.matrix_world);hp=np.array([v.co[:] for v in high.data.vertices])@hm[:3,:3].T+hm[:3,3]
    position_lo=hp.min(axis=0);position_span=np.maximum(np.ptp(hp,axis=0),.001);position_nodes={}
    routes=[]
    for m in mats:
        nt=m.node_tree;output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        bsdf=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bsdf is None:raise ValueError('Atlas baker requires imported metallic/roughness PBR: '+m.name)
        original_socket=output.inputs['Surface'].links[0].from_socket
        emit=nt.nodes.new('ShaderNodeEmission');combine=nt.nodes.new('ShaderNodeCombineColor')
        ao=next((n.inputs.get('Occlusion') for n in nt.nodes if n.type=='GROUP' and n.inputs.get('Occlusion') is not None),None)
        routes.append((nt,output,bsdf,original_socket,emit,combine,ao))
    sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=8;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=4
    sc.render.bake.use_selected_to_active=True;sc.render.bake.use_clear=True
    sc.render.bake.use_cage=True
    sc.render.bake.cage_extrusion=projection_m;sc.render.bake.max_ray_distance=projection_m*2
    sc.render.bake.margin=4;sc.render.bake.margin_type='EXTEND'
    high.select_set(True);target.select_set(True);bpy.context.view_layer.objects.active=target
    def connect(nt,src,dest):
        for link in list(dest.links):nt.links.remove(link)
        if src is None:dest.default_value=1
        elif src.is_linked:nt.links.new(src.links[0].from_socket,dest)
        else:
            v=src.default_value
            dest.default_value=tuple(v) if hasattr(v,'__len__') else (v,v,v,1) if dest.type=='RGBA' else v
    def route(channel):
        for nt,output,bsdf,original_socket,emit,combine,ao in routes:
            if channel=='Normal':nt.links.new(original_socket,output.inputs['Surface']);continue
            if channel=='Position':
                if nt not in position_nodes:
                    geometry=nt.nodes.new('ShaderNodeNewGeometry');subtract=nt.nodes.new('ShaderNodeVectorMath');subtract.operation='SUBTRACT';subtract.inputs[1].default_value=position_lo
                    divide=nt.nodes.new('ShaderNodeVectorMath');divide.operation='DIVIDE';divide.inputs[1].default_value=position_span
                    nt.links.new(geometry.outputs['Position'],subtract.inputs[0]);nt.links.new(subtract.outputs[0],divide.inputs[0]);position_nodes[nt]=divide.outputs[0]
                nt.links.new(position_nodes[nt],emit.inputs['Color'])
            elif channel in ('ORM','Clearcoat'):
                sockets=[ao,bsdf.inputs['Roughness'],bsdf.inputs['Metallic']] if channel=='ORM' else [bsdf.inputs['Coat Weight'],bsdf.inputs['Coat Roughness'],None]
                for i,s in enumerate(sockets):
                    dest_socket=combine.inputs[i]
                    for link in list(dest_socket.links):nt.links.remove(link)
                    if s is None:dest_socket.default_value=1 if channel=='ORM' else 0
                    elif s.is_linked:nt.links.new(s.links[0].from_socket,dest_socket)
                    else:dest_socket.default_value=s.default_value
                nt.links.new(combine.outputs[0],emit.inputs['Color'])
            else:
                socket=bsdf.inputs[dict(BaseColor='Base Color',Alpha='Alpha',Emission='Emission Color',Transmission='Transmission Weight')[channel]]
                connect(nt,socket,emit.inputs['Color'])
                # Emissive strength is a material extension; bake it into HDR
                # color, then encode a common strength for the new atlas.
                if channel=='Emission':connect(nt,bsdf.inputs['Emission Strength'],emit.inputs['Strength'])
            if channel!='Emission':
                for link in list(emit.inputs['Strength'].links):nt.links.remove(link)
                emit.inputs['Strength'].default_value=1
            nt.links.new(emit.outputs[0],output.inputs['Surface'])
    arrays={};report={}
    alpha_names={m.get('name') for m in original.data.get('materials',[]) if m.get('alphaMode')=='BLEND'}
    underlay=(proxy or composite_alpha) and any(m.name in alpha_names for m in mats)
    channels=('BaseColor','Alpha','Position','ORM','Emission',*(('Transmission',) if proxy or composite_alpha else ()),*(('Clearcoat',) if proxy else ()),'Normal')
    if underlay:channels+=('BaseColorUnder','EmissionUnder','ORMUnder','NormalUnder','AlphaUnder','PositionUnder','TransmissionUnder',*(('ClearcoatUnder',) if proxy else ()))
    for label in channels:
        channel=label.removesuffix('Under')
        if label=='BaseColorUnder':
            # Composite translucent graphics onto their real backing. Emission
            # routing alone cannot see through alpha=0 source decals.
            under=high.copy();under.data=high.data.copy();sc.collection.objects.link(under)
            bm=bmesh.new();bm.from_mesh(under.data)
            bmesh.ops.delete(bm,geom=[f for f in bm.faces if under.data.materials[f.material_index].name in alpha_names],context='FACES')
            bm.to_mesh(under.data);bm.free()
            high.hide_render=True;high.select_set(False);under.select_set(True)
            bpy.context.view_layer.objects.active=target
        route(channel)
        im=bpy.data.images.new('LOD '+label,width=size,height=size,alpha=True,float_buffer=True)
        im.colorspace_settings.name='Non-Color';tex.image=im
        opts=dict(type='NORMAL',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z') if channel=='Normal' else dict(type='EMIT')
        bpy.ops.object.bake(**opts)
        a=np.empty(size*size*4,np.float32);im.pixels.foreach_get(a);a=a.reshape(size,size,4)[::-1].copy()
        arrays[label]=a[:,:,:1 if channel in ('Alpha','Transmission') else 3].copy()
        if channel=='Position':arrays[label]=(arrays[label]*position_span+position_lo).astype(np.float32)
        del a
        bpy.data.images.remove(im)
    # Fill only padding from real covered texels, never hide projection misses.
    from kit.detachable_textures import _pull_push
    # Source positions expose both empty rays and opaque neighboring hits.
    # Evaluate each real layer before alpha compositing, so a fractional decal
    # cannot become a hole or lose the emission/material of its own backing.
    from kit.lod_transfer import repair,raster
    exact=np.zeros((size,size),bool)
    for yy,xx,*unused in raster(target,size):exact[yy,xx]=True
    mask=exact;interior=np.asarray(Image.fromarray(mask.astype(np.uint8)*255).filter(ImageFilter.MinFilter(3)))>0
    primary={k:v for k,v in arrays.items() if not k.endswith('Under')}
    report['nearest_transfer']=repair(high,target,primary,mask,size,projection_m*4/3,route)
    if underlay:
        backing={k.removesuffix('Under'):v for k,v in arrays.items() if k.endswith('Under')}
        arrays.clear()
        report['nearest_underlay']=repair(under,target,backing,mask,size,projection_m*4/3,route)
        opacity=np.clip(primary['Alpha'],0,1);below=np.clip(backing['Alpha'],0,1)*(1-opacity)
        combined=opacity+below
        for channel in primary:
            if channel in ('Alpha','Position'):continue
            primary[channel]=(primary[channel]*opacity+backing[channel]*below)/np.maximum(combined,1e-20)
        primary['Alpha']=combined
        del backing
    arrays=primary
    del arrays['Position']
    visible=mask & (arrays['Alpha'][:,:,0]>.001)
    if not visible.any():raise ValueError('Appearance projection covered no visible surface')
    base=_pull_push(arrays['BaseColor'][:,:,:3],visible)
    alpha=_pull_push(arrays['Alpha'][:,:,:1],mask)
    orm=_pull_push(arrays['ORM'][:,:,:3],visible)
    normal=_pull_push(arrays['Normal'][:,:,:3],visible)*2-1
    normal/=np.maximum(np.linalg.norm(normal,axis=2,keepdims=True),1e-20)
    emission=_pull_push(arrays['Emission'][:,:,:3],visible)
    strength=max(1.,float(emission.max()));has_emission=bool(emission.max()>.001)
    transmission=_pull_push(arrays['Transmission'][:,:,:1],visible) if proxy or composite_alpha else None
    has_transmission=(proxy or composite_alpha) and bool(transmission.max()>.001)
    clearcoat=_pull_push(arrays['Clearcoat'],visible) if proxy else None
    has_clearcoat=proxy and bool(clearcoat[:,:,0].max()>.001)
    files={}
    for name,a in [('BaseColor',np.concatenate([linear_to_srgb(base),alpha],axis=2)),('ORM',orm),('Normal',normal*.5+.5)]+([('Emission',linear_to_srgb(emission/strength))] if has_emission else [])+([('Transmission',np.repeat(transmission,3,axis=2))] if has_transmission else [])+([('Clearcoat',clearcoat)] if has_clearcoat else []):
        f=dest/f'T_{path.stem}_{name}.png';write_png(f,np.clip(a,0,1));files[name]=f
    oldmaterials=copy.deepcopy(doc.data.get('materials',[]))
    doc.data['images']=[dict(name=k,uri=os.path.relpath(v,doc.path.parent)) for k,v in files.items()]
    doc.data['textures']=[dict(source=i,sampler=0) for i in range(len(files))]
    doc.data['samplers']=[dict(magFilter=9729,minFilter=9987,wrapS=10497,wrapT=10497)]
    ids={name:i for i,name in enumerate(files)}
    materials=[{}] if proxy else oldmaterials
    for mi,m in enumerate(materials):
        # Transmission/IOR/specular factors stay on near materials. Base, ORM,
        # alpha, emission and normals have been evaluated from delivered nodes.
        pbr=m.setdefault('pbrMetallicRoughness',{})
        pbr.update(baseColorTexture=dict(index=ids['BaseColor']),metallicRoughnessTexture=dict(index=ids['ORM']),baseColorFactor=[1,1,1,1],roughnessFactor=1,metallicFactor=1)
        m['normalTexture']=dict(index=ids['Normal']);m['occlusionTexture']=dict(index=ids['ORM'])
        if (proxy or composite_alpha) and np.any(interior & (alpha[:,:,0]<.5)):
            m['alphaMode']='MASK';m['alphaCutoff']=.5
        if has_transmission:
            m.setdefault('extensions',{})['KHR_materials_transmission']=dict(transmissionFactor=1,transmissionTexture=dict(index=ids['Transmission']))
            if 'KHR_materials_transmission' not in doc.data.setdefault('extensionsUsed',[]):doc.data['extensionsUsed'].append('KHR_materials_transmission')
        if proxy and has_transmission:
            iors={old.get('extensions',{}).get('KHR_materials_ior',{}).get('ior',1.5) for old in oldmaterials if old.get('extensions',{}).get('KHR_materials_transmission',{}).get('transmissionFactor',0)>0}
            if len(iors)==1 and next(iter(iors))!=1.5:
                m.setdefault('extensions',{})['KHR_materials_ior']=dict(ior=next(iter(iors)))
                if 'KHR_materials_ior' not in doc.data.setdefault('extensionsUsed',[]):doc.data['extensionsUsed'].append('KHR_materials_ior')
        if has_clearcoat:
            m.setdefault('extensions',{})['KHR_materials_clearcoat']=dict(clearcoatFactor=1,clearcoatRoughnessFactor=1,clearcoatTexture=dict(index=ids['Clearcoat']),clearcoatRoughnessTexture=dict(index=ids['Clearcoat']),clearcoatNormalTexture=dict(index=ids['Normal']))
            if 'KHR_materials_clearcoat' not in doc.data.setdefault('extensionsUsed',[]):doc.data['extensionsUsed'].append('KHR_materials_clearcoat')
        if has_emission:
            m['emissiveTexture']=dict(index=ids['Emission']);m['emissiveFactor']=[1,1,1]
            m.setdefault('extensions',{})['KHR_materials_emissive_strength']=dict(emissiveStrength=strength)
            if 'KHR_materials_emissive_strength' not in doc.data.setdefault('extensionsUsed',[]):doc.data['extensionsUsed'].append('KHR_materials_emissive_strength')
        else:
            m.pop('emissiveTexture',None);m['emissiveFactor']=[0,0,0]
        m['name']=f'LOD_Proxy' if proxy else f'LOD_Atlas_{mi}'
    doc.data['materials']=materials
    if proxy:
        for _,_,p in doc.primitives():p['material']=0
    report.update(baked_channels=list(channels),used_underlay=underlay,source_sha256=digest(source),size=size,projection_m=projection_m,isolated_groups=len(used),
                  uv_covered_texels=int(mask.sum()),zero_alpha_interior_texels=int(np.count_nonzero(interior & (arrays['Alpha'][:,:,0]<.01))),
                  maps={k:dict(bytes=v.stat().st_size,sha256=digest(v)) for k,v in files.items()})
    (dest/'bake.json').write_text(json.dumps(report,indent=2)+'\n')
    print('LOD ATLAS',path.stem,size,report,flush=True)
    return report


if __name__=='__main__':
    import argparse,sys
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--source',required=True)
    p.add_argument('--out',required=True);p.add_argument('--size',type=int,required=True)
    p.add_argument('--projection',type=float,required=True);p.add_argument('--proxy',action='store_true');p.add_argument('--composite-alpha',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);doc=Document(a.input)
    bake(doc,a.source,a.out,a.size,proxy=a.proxy,projection_m=a.projection,composite_alpha=a.composite_alpha);doc.save(a.out)
