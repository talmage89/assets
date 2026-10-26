"""Re-import GLB and independently verify geometry, UVs, textures, joints and sockets."""
import argparse,json,sys,struct,runpy,io
from PIL import Image
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB
from kit import uv,rig,atlas
from kit.policy import density_bands


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--expected',required=True)
    p.add_argument('--config',required=True);p.add_argument('--out',required=True);p.add_argument('--size',type=int,default=2048)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source).resolve();expected=json.loads(Path(a.expected).read_text())
    cfg=runpy.run_path(a.config);glb=GLB(path);data=glb.json;errors=[]
    def check(condition,message):
        if not condition:errors.append(message)
    check(len(data.get('materials',[]))<=3,'Material budget exceeded')
    check(len(data.get('images',[]))==3,'Expected one BaseColor/Normal/ORM set')
    image_reports=[]
    for i in range(len(data.get('images',[]))):
        binary=glb.image(i);check(binary[:8]==b'\x89PNG\r\n\x1a\n','Texture is not PNG')
        width,height=struct.unpack_from('>II',binary,16)
        check((width,height)==(a.size,a.size),f'Texture {i} size {width}x{height}')
        image_reports.append(dict(name=data['images'][i].get('name',''),width=width,height=height,bytes=len(binary)))
    for i,entry in enumerate(data.get('images',[])):
        pixels=np.asarray(Image.open(io.BytesIO(glb.image(i))).convert('RGB'),dtype=np.float32)/255
        if 'Normal' in entry.get('name',''):
            lengths=np.linalg.norm(pixels*2-1,axis=2)
            check(float(np.max(np.abs(lengths-1)))<.012,'Normal texture vectors are not normalized')
        if 'BaseColor' in entry.get('name',''):
            check(float(pixels.max()-pixels.min())>.2,'BaseColor atlas is flat')
    triangle_count=0;raw_weight_error=0.0;raw_normal_error=0.0;influences=0
    for mesh in data.get('meshes',[]):
        for primitive in mesh['primitives']:
            triangle_count+=data['accessors'][primitive['indices']]['count']//3
            attributes=primitive['attributes'];normal=glb.accessor(attributes['NORMAL'])
            raw_normal_error=max(raw_normal_error,float(np.max(np.abs(np.linalg.norm(normal,axis=1)-1))))
            check('TEXCOORD_0' in attributes,'Missing UV0')
            if 'WEIGHTS_0' in attributes:
                weights=glb.accessor(attributes['WEIGHTS_0']);raw_weight_error=max(raw_weight_error,float(np.max(np.abs(weights.sum(axis=1)-1))))
                influences=max(influences,int(np.max((weights>1e-6).sum(axis=1))))
    check(triangle_count==expected['triangles'],'GLB triangle count changed')
    check(triangle_count<=sum(cfg['BUDGETS'].values()),'Triangle budget exceeded')
    check(raw_normal_error<1e-4,'Non-unit vertex normals')
    check(raw_weight_error<1e-5 and influences<=cfg.get('MAX_SKIN_INFLUENCES',4),'Invalid or excessive skin influences')
    check(len(data.get('skins',[]))==len(expected['rigs']),'Skin count differs from source rigs')
    bind_error=0.0
    for skin_index,skin in enumerate(data.get('skins',[])):
        names=[data['nodes'][i]['name'] for i in skin['joints']]
        wanted=next((r for r in expected['rigs'].values() if set(r)==set(names)),{})
        check(bool(wanted),'Unexpected skin bone names')
        inverse=glb.accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
        mesh_nodes=[i for i,node in enumerate(data['nodes']) if node.get('skin')==skin_index]
        for node in mesh_nodes:
            for joint,ibm in zip(skin['joints'],inverse):
                # glTF skinned vertices ignore the mesh node transform; the
                # exporter supplies world-space bind coordinates.
                residual=glb.world(joint)@ibm
                bind_error=max(bind_error,float(np.max(np.abs(residual-np.eye(4)))))
        by_name={data['nodes'][i]['name']:i for i in skin['joints']}
        for name,row in wanted.items():
            if row['parent']:check(glb.parents.get(by_name[name])==by_name[row['parent']],'Skin hierarchy changed')
    check(bind_error<2e-5,f'Invalid inverse bind/rest pose: {bind_error}')
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
    sc=bpy.context.scene;bpy.context.view_layer.update();meshes=[o for o in sc.objects if o.type=='MESH' and o.name in expected['meshes']]
    forbidden=set(cfg.get('EXCLUDED_NODES',()))
    check(not any(o.name in forbidden for o in sc.objects),'Excluded cylinder geometry present')
    maximum_vertex_error=0.0;maximum_weight_error=0.0;rigid_fitting_vertices=0
    for name,wanted in expected['meshes'].items():
        ob=bpy.data.objects.get(name);check(ob is not None,f'Missing mesh {name}')
        if ob is None:continue
        tree=KDTree(len(wanted['vertices_world']))
        for i,point in enumerate(wanted['vertices_world']):tree.insert(point,i)
        tree.balance()
        for vertex in ob.data.vertices:
            point=ob.matrix_world@vertex.co;distance=tree.find(point)[2]
            maximum_vertex_error=max(maximum_vertex_error,distance)
            if 'weights' in wanted:
                index=tree.find(point)[1];weights={ob.vertex_groups[g.group].name:g.weight for g in vertex.groups if g.weight>1e-7}
                row=wanted['weights'][index]
                for bone in row.keys()|weights.keys():maximum_weight_error=max(maximum_weight_error,abs(row.get(bone,0)-weights.get(bone,0)))
                last=list(next(iter(expected['rigs'].values())))[-1]
                if row=={last:1.0}:rigid_fitting_vertices+=1
        check(all(abs(v-1)<1e-6 for v in ob.scale),f'{name}: unapplied mesh scale')
    check(maximum_weight_error<1e-5,'Re-import changed authored skin weights')
    check(maximum_vertex_error<2e-5,'Re-import changed rest geometry positions')
    socket_error=0.0
    for name in cfg.get('REQUIRED_NODES',()):
        ob=bpy.data.objects.get(name);check(ob is not None,f'Missing pivot/socket {name}')
        if ob and name in expected['nodes']:
            error=float(np.max(np.abs(np.array(ob.matrix_world)-np.array(expected['nodes'][name]))));socket_error=max(socket_error,error)
    check(socket_error<2e-5,'Pivot/socket rest transform changed')
    if cfg.get('DELIVERY_BOUNDS'):
        points=[ob.matrix_world@Vector(v) for ob in meshes for v in ob.bound_box]
        lower=[min(p[i] for p in points) for i in range(3)]
        upper=[max(p[i] for p in points) for i in range(3)]
        bounds=[b-a for a,b in zip(lower,upper)]
        spec=cfg['DELIVERY_BOUNDS']
        check(all(abs(a-b)<=t for a,b,t in zip(bounds,spec['size'],spec['tolerance'])),f'Delivery dimensions outside tolerance: {bounds}')
    arms=[o for o in sc.objects if o.type=='ARMATURE'];check(len(arms)==len(expected['rigs']),'Armature count changed on re-import')
    for arm in arms:
        wanted=expected['rigs'].get(arm.name,{})
        names=list(arm.data.bones.keys());check(set(names)==set(wanted),'Re-import bone names changed')
        for bone in arm.data.bones:
            check((bone.parent.name if bone.parent else None)==wanted[bone.name]['parent'],'Re-import hierarchy changed')
            check((arm.matrix_world@bone.head_local-Vector(wanted[bone.name]['head'])).length<2e-5,'Re-import joint rest position changed')
    tile_meshes=[o for o in meshes if atlas.tiled_spec(o.name,cfg)]
    uv_report=uv.report([o for o in meshes if o not in tile_meshes],a.size,'UVMap')
    unique_region=atlas.unique_rect_report([o for o in meshes if o not in tile_meshes],cfg,'UVMap')
    check(unique_region['passed'],'Invalid unique atlas region: '+str(unique_region['errors']))
    tiles=atlas.tile_report(tile_meshes,cfg,a.size,'UVMap')
    check(tiles['passed'],'Invalid explicitly tiled UVs: '+str(tiles['errors']))
    for ob in tile_meshes:
        spec=atlas.tiled_spec(ob.name,cfg)
        primitive=next(p for m in data['meshes'] if m['name']==ob.name for p in m['primitives'])
        mat=data['materials'][primitive['material']]
        if spec.get('alpha_cutoff') is not None:
            check(mat.get('alphaMode')=='MASK' and abs(mat.get('alphaCutoff',.5)-spec['alpha_cutoff'])<1e-5,'Tile material is not alpha-tested')
            check(mat.get('doubleSided',False)==spec.get('double_sided',True),'Tile backface policy changed')
            texture=mat['pbrMetallicRoughness']['baseColorTexture']['index']
            image_index=data['textures'][texture]['source']
            rgba=np.asarray(Image.open(io.BytesIO(glb.image(image_index))).convert('RGBA'))
            x0,y0,x1,y1=spec['rect'];h,w=rgba.shape[:2]
            alpha=rgba[round((1-y1)*h):round((1-y0)*h),round(x0*w):round(x1*w),3]/255
            check(bool((alpha<spec['alpha_cutoff']).any()) and bool((alpha>=spec['alpha_cutoff']).any()),'Alpha tile lost its holes or wires')
    check(uv_report['overlap_fraction']<1e-6,'UV overlap exceeds subpixel tolerance')
    check(uv_report['outside_triangles']==0 and uv_report['degenerate_uv_triangles']==0,'Invalid UV triangles')
    check(uv_report['coverage']>cfg.get('UV_MIN_COVERAGE',.35),'Atlas coverage too low')
    policy=cfg.get('VERIFY_POLICY',{})
    bands=density_bands(cfg,a.size)
    check(bands['p5_min']<uv_report['density_px_m']['5'] and bands['median_min']<uv_report['density_px_m']['50']<bands['median_max'] and uv_report['density_px_m']['95']<bands['p95_max'],'Texel density outside declared priority bands')
    # Exercise ordinary imported LBS. Attachment must move; manifold stays pinned.
    pose_report={}
    for arm in arms:
        tube=policy.get('tubes',{}).get(arm.name,policy.get('tube',{}))
        points_property=tube.get('rest_points_property','hose_rest_points_m')
        if points_property not in arm:continue
        attachment=next((o for o in sc.objects if o.parent==arm and o.parent_type=='BONE' and o.get('socket_kind')),None)
        check(attachment is not None,'Flexible chain has no bone attachment socket')
        if attachment is None:continue
        rest_attachment=attachment.matrix_world.translation.copy()
        root=arm.matrix_world@arm.data.bones[0].head_local
        radius=tube.get('radius_m',.0052)
        rig.dangling(arm,**cfg.get('RIG_POSES',{}).get(arm.name,{}));moved=(attachment.matrix_world.translation-rest_attachment).length
        root_error=(arm.matrix_world@arm.pose.bones[0].head-root).length
        check(moved>tube.get('minimum_attachment_travel_m',.15) and root_error<tube.get('root_tolerance_m',1e-5),'Hose demonstration did not move fitting with pinned root')
        minimum_radius=1.0;tested_rings=0
        if points_property in arm:
            coords=arm[points_property];centers=[Vector(coords[i:i+3]) for i in range(0,len(coords),3)]
            for ob in meshes:
                if not any(m.type=='ARMATURE' and m.object==arm for m in ob.modifiers):continue
                evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh()
                pairs={tuple(round(v,6) for v in (arm.matrix_world.inverted()@ob.matrix_world@vertex.co)):
                    arm.matrix_world.inverted()@evaluated.matrix_world@me.vertices[vertex.index].co for vertex in ob.data.vertices}
                for i,center in enumerate(centers):
                    tangent=(centers[min(i+1,len(centers)-1)]-centers[max(i-1,0)]).normalized()
                    ring=[posed for rest,posed in pairs.items() if abs((Vector(rest)-center).length-radius)<tube.get('radial_tolerance_m',.00012) and abs((Vector(rest)-center).dot(tangent))<tube.get('plane_tolerance_m',.00015)]
                    if len(ring)<tube.get('minimum_ring_vertices',6):continue
                    centroid=sum(ring,Vector())/len(ring)
                    minimum_radius=min(minimum_radius,min((v-centroid).length for v in ring));tested_rings+=1
                evaluated.to_mesh_clear()
            check(tested_rings>=tube.get('minimum_rings',40) and minimum_radius>tube.get('minimum_posed_radius_m',.0036),'Hose cross-sections collapse in the free-hanging pose')
        pose_report=dict(attachment_travel_m=moved,manifold_error_m=root_error,tested_hose_rings=tested_rings,
                         minimum_posed_ring_radius_m=minimum_radius,rest_radius_m=radius)
        rig.reset(arm)
    result=dict(passed=not errors,errors=errors,source=str(path),bytes=path.stat().st_size,triangles=triangle_count,
        materials=len(data.get('materials',[])),textures=image_reports,normal_unit_error=raw_normal_error,
        skin_weight_sum_error=raw_weight_error,reimport_weight_error=maximum_weight_error,rigid_last_bone_vertices=rigid_fitting_vertices,max_influences=influences,inverse_bind_error=bind_error,
        rest_vertex_error_m=maximum_vertex_error,socket_matrix_error=socket_error,pose=pose_report,
        density_bands_px_m=bands,tiling=tiles,unique_region=unique_region,uv={k:v for k,v in uv_report.items() if k!='island_measurements'})
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if errors:raise RuntimeError('Delivery verification failed')

if __name__=='__main__':main()
