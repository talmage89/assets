"""Bounded nearest-surface repair for missed or wrong selected-to-active hits.

Original delivered shader fields are evaluated by Cycles on tiny source-facing
patches. Their UVs, tint and split normals come from the nearest original
triangle; no replacement color or normal is invented. Source-hit positions detect rays that hit an opaque neighbor. Work streams
through small patch atlases in batches, and only
points within the level's geometric budget may be repaired.
"""
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def unit(v):
    return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),1e-20)


def raster(target,size):
    """Native texel-center samples, including the actual target tangent frame."""
    mesh=target.data;mesh.calc_loop_triangles();uvname=mesh.uv_layers.active.name
    mesh.calc_tangents(uvmap=uvname)
    uv=np.array([x.uv[:] for x in mesh.uv_layers[uvname].data],float)
    positions=np.array([v.co[:] for v in mesh.vertices],float)
    matrix=np.array(target.matrix_world);positions=positions@matrix[:3,:3].T+matrix[:3,3]
    normals=unit(np.array([x.vector[:] for x in mesh.corner_normals])@np.linalg.inv(matrix[:3,:3]))
    tangent=unit(np.array([x.tangent[:] for x in mesh.loops])@matrix[:3,:3].T)
    signs=np.array([x.bitangent_sign for x in mesh.loops])
    for tri in mesh.loop_triangles:
        loops=np.array(tri.loops);u=uv[loops].copy();u[:,1]=1-u[:,1]
        lo=np.maximum(0,np.floor(u.min(axis=0)*size-.5).astype(int));hi=np.minimum(size-1,np.ceil(u.max(axis=0)*size-.5).astype(int))
        if np.any(hi<lo):continue
        yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];q=np.stack(((xx+.5)/size,(yy+.5)/size),axis=-1)
        edge=(u[1:]-u[0]).T;det=np.linalg.det(edge)
        if abs(det)<1e-14:continue
        w=(q-u[0])@np.linalg.inv(edge).T;w=np.concatenate([1-w.sum(axis=2,keepdims=True),w],axis=2)
        inside=np.min(w,axis=2)>=-1e-6
        if not inside.any():continue
        yy=yy[inside];xx=xx[inside];w=w[inside]
        p=positions[np.array(tri.vertices)];area=np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))
        n=unit(w@normals[loops]);t=unit(w@tangent[loops]);t=unit(t-n*np.sum(n*t,axis=1,keepdims=True))
        b=np.cross(n,t)*np.where(w@signs[loops]>=0,1,-1)[:,None]
        yield yy,xx,w@p,n,t,b,np.sqrt(area/max(abs(det),1e-20))/size


def repair(source,target,arrays,mask,size,tolerance,route,batch_size=16384):
    missing=mask & (arrays['Alpha'][:,:,0]<.001)
    if not missing.any() and 'Position' not in arrays:return dict(candidates=0,repaired=0,max_distance_m=0.)
    mesh=source.data;mesh.calc_loop_triangles();mesh.calc_tangents(uvmap='LOD_SourceUV0')
    matrix=np.array(source.matrix_world);vertices=np.array([v.co[:] for v in mesh.vertices],float)
    vertices=vertices@matrix[:3,:3].T+matrix[:3,3]
    faces=np.array([t.vertices[:] for t in mesh.loop_triangles],int)
    loops=np.array([t.loops[:] for t in mesh.loop_triangles],int)
    slots=np.array([t.material_index for t in mesh.loop_triangles],int)
    tree=BVHTree.FromPolygons([Vector(p) for p in vertices],faces.tolist(),all_triangles=True)
    ns=unit(np.array([x.vector[:] for x in mesh.corner_normals])@np.linalg.inv(matrix[:3,:3]))
    ts=unit(np.array([x.tangent[:] for x in mesh.loops])@matrix[:3,:3].T)
    uvs={layer.name:np.array([x.uv[:] for x in layer.data],float) for layer in mesh.uv_layers}
    colors={}
    for layer in mesh.color_attributes:
        a=np.array([x.color[:] for x in layer.data],np.float32)
        if layer.domain=='POINT':a=a[np.array([l.vertex_index for l in mesh.loops])]
        colors[layer.name]=a
    def records():
        visited=np.zeros_like(mask)
        for yy,xx,p,n,t,b,footprint in raster(target,size):
            take=mask[yy,xx] & ~visited[yy,xx]
            visited[yy[take],xx[take]]=True
            for y,x,point,nn,tt,bb in zip(yy[take],xx[take],p[take],n[take],t[take],b[take]):
                if not missing[y,x] and 'Position' not in arrays:continue
                q,source_face_normal,fi,dist=tree.find_nearest(Vector(point))
                if fi is None or dist>tolerance:continue
                # Thin closed parts have two nearby sides. Correspondence
                # must agree with the cage's outward hemisphere.
                cosine=float(np.dot(source_face_normal,nn))
                if cosine<.85:
                    radius=tolerance if cosine<=.05 else min(tolerance,dist+tolerance*.125)
                    compatible=[hit for hit in tree.find_nearest_range(Vector(point),radius) if np.dot(hit[1],nn)>.05]
                    if not compatible:continue
                    q,source_face_normal,fi,dist=min(compatible,key=lambda hit:(hit[3]/tolerance)**2+.5*(1-float(np.dot(hit[1],nn)))**2)
                if not missing[y,x] and np.linalg.norm(arrays['Position'][y,x]-np.array(q))<=tolerance*.05:continue
                tri=vertices[faces[fi]];e=tri[1:]-tri[0];gram=e@e.T
                if abs(np.linalg.det(gram))<1e-24:continue
                bw=np.linalg.solve(gram,e@(np.array(q)-tri[0]));bw=np.array([1-bw.sum(),*bw])
                yield (int(y),int(x),np.array(q),fi,bw,nn,tt,bb,footprint,float(dist))
    from itertools import islice
    pending=records();batch=list(islice(pending,batch_size))
    if not batch:return dict(candidates=0,repaired=0,max_distance_m=0.)
    scene=bpy.context.scene;old_hidden={o:o.hide_render for o in scene.objects if o.type=='MESH'}
    for o in old_hidden:o.hide_render=True;o.select_set(False)
    old_selection=scene.render.bake.use_selected_to_active;old_cage=scene.render.bake.use_cage;old_margin=scene.render.bake.margin
    scene.render.bake.use_selected_to_active=False;scene.render.bake.use_cage=False;scene.render.bake.margin=0
    bake_nodes=[]
    for material in dict.fromkeys(m for m in source.data.materials if m):
        old=material.node_tree.nodes.active;node=material.node_tree.nodes.new('ShaderNodeTexImage');material.node_tree.nodes.active=node
        bake_nodes.append((material,node,old))
    repaired=0;maximum=0.;candidates=0
    while batch:
        count=len(batch);candidates+=count
        fi=np.array([r[3] for r in batch]);bw=np.array([r[4] for r in batch]);li=loops[fi]
        n=unit(np.einsum('ni,nij->nj',bw,ns[li]));t=unit(np.einsum('ni,nij->nj',bw,ts[li]))
        t=unit(t-n*np.sum(n*t,axis=1,keepdims=True));b=np.cross(n,t)
        q=np.array([r[2] for r in batch]);foot=np.array([r[8] for r in batch])
        corners=np.array([[-.5,-.5],[.5,-.5],[.5,.5],[-.5,.5]])
        delta=(t[:,None,:]*corners[None,:,0,None]+b[:,None,:]*corners[None,:,1,None])*foot[:,None,None]
        pp=(q[:,None,:]+delta).reshape(-1,3);ff=np.arange(count*4).reshape(-1,4)
        data=bpy.data.meshes.new('LOD nearest source patches');data.from_pydata(pp.tolist(),[],ff.tolist());data.update()
        for polygon,slot in zip(data.polygons,slots[fi]):polygon.use_smooth=True;polygon.material_index=int(slot)
        for material in source.data.materials:data.materials.append(material)
        data.normals_split_custom_set(np.repeat(n,4,axis=0).tolist())
        edge=vertices[faces[fi]][:,1:]-vertices[faces[fi]][:,:1]
        gram=edge@np.transpose(edge,(0,2,1));grad=np.linalg.solve(gram,edge)
        shift=np.einsum('nkj,nij->nki',delta,grad)
        corner_w=np.concatenate([1-(bw[:,None,1:]+shift).sum(axis=2,keepdims=True),bw[:,None,1:]+shift],axis=2)
        for name,values in uvs.items():
            uv=np.einsum('nki,nij->nkj',corner_w,values[li]).reshape(-1,2)
            layer=data.uv_layers.new(name=name);layer.data.foreach_set('uv',uv.astype(np.float32).ravel())
        for name,values in colors.items():
            value=np.einsum('ni,nij->nj',bw,values[li]);layer=data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='CORNER')
            layer.data.foreach_set('color',np.repeat(value,4,axis=0).astype(np.float32).ravel())
        yy=np.array([r[0] for r in batch]);xx=np.array([r[1] for r in batch]);uv=np.empty((count,4,2))
        patch_size=2**int(np.ceil(np.log2(max(2,np.sqrt(count)))))
        py=np.arange(count)//patch_size;px=np.arange(count)%patch_size
        uv[:,:,0]=(px[:,None]+np.array([0,1,1,0]))/patch_size
        uv[:,:,1]=1-(py[:,None]+np.array([1,1,0,0]))/patch_size
        layer=data.uv_layers.new(name='LOD_TransferBake');layer.data.foreach_set('uv',uv.astype(np.float32).ravel());data.uv_layers.active=layer;layer.active_render=True
        ob=bpy.data.objects.new('LOD nearest source patches',data);scene.collection.objects.link(ob);ob.select_set(True);ob.hide_render=False;bpy.context.view_layer.objects.active=ob
        result={}
        for channel in ['Alpha','BaseColor','ORM','Emission',*(['Transmission'] if 'Transmission' in arrays else []),*(['Clearcoat'] if 'Clearcoat' in arrays else []),*(['CoatNormal'] if 'CoatNormal' in arrays else []),'Normal']:
            route(channel+'Field' if channel in ('Normal','CoatNormal') else channel)
            im=bpy.data.images.new('LOD nearest '+channel,width=patch_size,height=patch_size,alpha=True,float_buffer=True);im.colorspace_settings.name='Non-Color'
            for material,node,old in bake_nodes:node.image=im;material.node_tree.nodes.active=node
            bpy.ops.object.bake(type='EMIT')
            values=np.empty(patch_size*patch_size*4,np.float32);im.pixels.foreach_get(values);values=values.reshape(patch_size,patch_size,4)[::-1]
            result[channel]=values[py,px,:3].copy();bpy.data.images.remove(im)
        valid=result['Alpha'][:,0]>.001
        for channel in result:
            if channel in ('Normal','CoatNormal'):
                wn=unit(result[channel]*2-1);tn=np.array([r[5] for r in batch]);tt=np.array([r[6] for r in batch]);tb=np.array([r[7] for r in batch])
                wn*=np.where(np.sum(wn*tn,axis=1)>=0,1,-1)[:,None]
                value=np.stack([np.sum(wn*tt,axis=1),np.sum(wn*tb,axis=1),np.sum(wn*tn,axis=1)],axis=1)*.5+.5
            else:value=result[channel]
            arrays[channel][yy[valid],xx[valid],:min(arrays[channel].shape[2],3)]=value[valid,:min(arrays[channel].shape[2],3)]
        if 'Position' in arrays:arrays['Position'][yy[valid],xx[valid]]=q[valid]
        repaired+=int(valid.sum())
        if valid.any():maximum=max(maximum,max(batch[i][9] for i in np.where(valid)[0]))
        bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(data)
        batch=list(islice(pending,batch_size))
    for material,node,old in bake_nodes:material.node_tree.nodes.remove(node);material.node_tree.nodes.active=old
    for ob,hidden in old_hidden.items():ob.hide_render=hidden
    scene.render.bake.use_selected_to_active=old_selection;scene.render.bake.use_cage=old_cage;scene.render.bake.margin=old_margin
    return dict(candidates=candidates,repaired=repaired,max_distance_m=maximum)
