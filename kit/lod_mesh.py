"""Blender decimation with measured geometry and corner-field transport.

The legacy path preserves original charts at delivery precision. Opt-in screen
reduction uses switch-pixel tolerances, removes small features, and permits a
new chart/normal cage when the caller rebakes the immutable delivered shading.
Skin influences retain discrete joints with normalized transported weights.
"""
import math
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree


def topology(attrs, faces):
    """Geometric edge incidence across coincident split vertices, local meters."""
    v = attrs['POSITION']; keys = [tuple(np.round(p, 6)) for p in v]
    edges = {}; degenerate = 0; slivers = 0; flipped = 0
    t = v[faces]; cross = np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
    areas = np.linalg.norm(cross,axis=1)
    lengths = np.stack([np.sum((t[:,a]-t[:,b])**2,axis=1) for a,b in [(0,1),(1,2),(2,0)]])
    quality = areas / np.maximum(lengths.max(axis=0),1e-30)
    degenerate = int((areas<1e-14).sum()); slivers = int((quality<1e-5).sum())
    uv_degenerate=0;uv_by_layer={}
    for key,values in attrs.items():
        if key.startswith('TEXCOORD_'):
            uv=values[faces].astype(float);a=uv[:,1]-uv[:,0];b=uv[:,2]-uv[:,0]
            count=int((np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])<1e-14).sum())
            uv_by_layer[key]=count;uv_degenerate+=count
    if 'NORMAL' in attrs:
        n = attrs['NORMAL'][faces].sum(axis=1)
        flipped = int((np.einsum('ij,ij->i',cross,n)<-1e-10).sum())
    for face in faces:
        for a,b in [(face[0],face[1]),(face[1],face[2]),(face[2],face[0])]:
            key = tuple(sorted((keys[a],keys[b])))
            if key[0] != key[1]: edges[key] = edges.get(key,0)+1
    boundary = [e for e,n in edges.items() if n==1]
    return dict(boundary_edges=len(boundary), nonmanifold_edges=sum(n>2 for n in edges.values()),
                degenerate=degenerate,degenerate_uv=uv_degenerate,degenerate_uv_by_layer=uv_by_layer,
                slivers=slivers,winding_disagreements=flipped), boundary


def barycentric(p, tri):
    a,b,c = tri; u=b-a; v=c-a; q=p-a
    uu=np.dot(u,u); uv=np.dot(u,v); vv=np.dot(v,v)
    det=uu*vv-uv*uv
    if abs(det)<1e-24: return np.array([1.,0,0])
    y=(vv*np.dot(q,u)-uv*np.dot(q,v))/det
    z=(uu*np.dot(q,v)-uv*np.dot(q,u))/det
    return np.array([1-y-z,y,z])


def world_geometry(doc,node_ids):
    """Geometry across material seams in the delivered rest frame."""
    points=[];normals=[];triangles=[];offset=0
    for ni in node_ids:
        node=doc.data['nodes'][ni]
        if 'mesh' not in node:continue
        matrix=np.eye(4) if 'skin' in node else doc.world(ni)
        for p in doc.data['meshes'][node['mesh']]['primitives']:
            a,f=doc.arrays(p);points.append(a['POSITION']@matrix[:3,:3].T+matrix[:3,3])
            n=a['NORMAL']@np.linalg.inv(matrix[:3,:3]);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-20);normals.append(n)
            triangles.append(f.astype(np.uint32)+offset);offset+=len(a['POSITION'])
    return dict(POSITION=np.concatenate(points),NORMAL=np.concatenate(normals)),np.concatenate(triangles)


def simplify(attrs, faces, ratio, max_error, mode='COLLAPSE', max_uv_error=1/2048, screen_space=False, rebake=False):
    original = dict(triangles=len(faces), status='retained')
    # Skins keep all delivered weights and topology. Separate static parts still
    # simplify. Alpha cards are also protected: collapsing them thins coverage.
    if (any(k.startswith(('JOINTS_', 'WEIGHTS_')) for k in attrs) and not screen_space) or len(faces)<12:
        return attrs, faces, original
    mesh = bpy.data.meshes.new('LOD candidate')
    # glTF stores split corners as separate vertices. Reconstruct shared
    # geometric topology while retaining every discontinuity as CORNER data.
    # Otherwise a flat-shaded delivered box becomes twelve isolated triangles
    # and a decimator cannot simplify even a planar strip.
    _,first,remap=np.unique(np.round(attrs['POSITION'],8),axis=0,return_index=True,return_inverse=True)
    mesh.from_pydata(attrs['POSITION'][first].tolist(),[],remap[faces].tolist()); mesh.update()
    corner_source=faces.ravel()
    for key,values in attrs.items():
        if key=='POSITION':continue
        # Corner-domain fields survive native collapse interpolation. FLOAT_COLOR
        # is linear data, including Wind and independent alpha, never sRGB color.
        typ={2:'FLOAT_VECTOR',3:'FLOAT_VECTOR',4:'FLOAT_COLOR'}[values.shape[1]]
        layer=mesh.attributes.new('LOD_'+key,typ,'CORNER')
        values=values[corner_source]
        padded=np.pad(values,((0,0),(0,1))) if values.shape[1]==2 else values
        layer.data.foreach_set('color' if typ=='FLOAT_COLOR' else 'vector',padded.astype(np.float32).ravel())
        if key.startswith('TEXCOORD_'):
            uv=mesh.uv_layers.new(name=key)
            uv.data.foreach_set('uv',values.astype(np.float32).ravel())
    ob=bpy.data.objects.new('LOD candidate',mesh); bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active=ob; ob.select_set(True)
    bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table();bm.edges.ensure_lookup_table()
    # Collapse costs include a strong boundary penalty. This is only a hint;
    # exact boundary positions and edge coverage are independently checked below.
    locked={v.index for e in bm.edges if e.is_boundary for v in e.verts}
    boundary_locked=locked.copy()
    # Protect discontinuous normals even when an exporter shared the vertices.
    for e in bm.edges:
        if len(e.link_faces)==2 and e.calc_face_angle(0)>math.radians(35):
            locked.update(v.index for v in e.verts)
    bm.free()
    # UV seams are corner discontinuities after geometric reconstruction.
    edge_uv={}
    for face in mesh.polygons:
        for j,li in enumerate(face.loop_indices):
            lj=face.loop_indices[(j+1)%len(face.loop_indices)]
            vi,vj=mesh.loops[li].vertex_index,mesh.loops[lj].vertex_index
            key=tuple(sorted((vi,vj)))
            signature=[]
            for uv in mesh.uv_layers:
                a,b=tuple(uv.data[li].uv),tuple(uv.data[lj].uv)
                signature.append((a,b) if vi<vj else (b,a))
            if key in edge_uv and edge_uv[key]!=signature:locked.update(key)
            edge_uv[key]=signature
    if screen_space:locked=boundary_locked
    group=ob.vertex_groups.new(name='Protected')
    interior=[i for i in range(len(mesh.vertices)) if i not in locked]
    if interior:group.add(interior,1,'REPLACE')
    modifier=ob.modifiers.new('Constrained collapse','DECIMATE');modifier.decimate_type=mode
    if mode=='DISSOLVE':
        modifier.angle_limit=1e-4;modifier.delimit={'NORMAL','MATERIAL','SEAM','SHARP','UV'}
    else:
        modifier.ratio=ratio
        if interior:
            modifier.vertex_group=group.name;modifier.vertex_group_factor=1000
        modifier.use_collapse_triangulate=True
    evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); result=evaluated.to_mesh()
    result.calc_loop_triangles()
    loops=np.array([t.loops[:] for t in result.loop_triangles],np.uint32).ravel()
    vertices=np.array([l.vertex_index for l in result.loops],np.uint32)[loops]
    positions=np.array([v.co[:] for v in result.vertices],np.float64)[vertices]
    tris=np.arange(len(positions),dtype=np.uint32).reshape(-1,3)
    mapped={}
    for key,values in attrs.items():
        if key=='POSITION':continue
        width=4 if values.shape[1]==4 else 3
        a=np.empty((len(result.loops),width),np.float32)
        result.attributes['LOD_'+key].data.foreach_get('color' if width==4 else 'vector',a.ravel())
        a=a[loops,:values.shape[1]].copy()
        if key in ('NORMAL','TANGENT'):
            a[:,:3]/=np.maximum(np.linalg.norm(a[:,:3],axis=1,keepdims=True),1e-20)
            if key=='TANGENT':a[:,3]=np.where(a[:,3]>=0,1,-1)
        mapped[key]=a
    # Deduplicate only complete identical corner signatures for efficient glTF.
    fields={'POSITION':positions.astype(np.float32),**mapped};keys=list(fields)
    signature=np.concatenate([fields[k] for k in keys],axis=1)
    _,first,remap=np.unique(signature,axis=0,return_index=True,return_inverse=True)
    positions=positions[first];mapped={k:a[first] for k,a in mapped.items()};tris=remap[tris].astype(np.uint32)
    evaluated.to_mesh_clear();bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(mesh)
    source=attrs['POSITION'].astype(float)
    bvh=BVHTree.FromPolygons([Vector(p) for p in source],faces.tolist(),all_triangles=True)
    # Every candidate vertex, edge midpoint and centroid is projected onto LOD0.
    # Reuse the barycentric field for normals/UV/colors/Wind, including tangents.
    err=0.; uv_error=0.;field_error=0.;surface_samples=[];surface_weights=[]
    for vi,p in enumerate(positions):
        q,_,i,d=bvh.find_nearest(Vector(p))
        if i is None: raise ValueError('Cannot project LOD candidate')
        err=max(err,d)
        # Native collapse averages corner attributes independently of its QEM
        # optimum position. Reproject the delivered field at that actual point.
        # Native corner values identify the chart/normal side at coincident
        # seams; they are hints, not the final UVs or shading normals.
        candidates=bvh.find_nearest_range(Vector(p),max(1e-6,d+1e-6))
        chosen=None;best=float('inf')
        for qq,nn,ii,dd in candidates:
            ww=barycentric(np.array(qq),source[faces[ii]])
            score=0.
            for k in mapped:
                if k.startswith('TEXCOORD_'):
                    score+=float(np.linalg.norm(mapped[k][vi]-ww@attrs[k][faces[ii]]))
            if 'NORMAL' in attrs:
                n=ww@attrs['NORMAL'][faces[ii]];n/=max(np.linalg.norm(n),1e-20)
                score+=2*(1-float(np.dot(n,mapped['NORMAL'][vi])))
            if score<best:best=score;chosen=(ii,ww)
        ii,ww=chosen
        for key in mapped:
            if not key.startswith('JOINTS_'):continue
            weight_key='WEIGHTS_'+key.split('_',1)[1];influences={}
            for source_vertex,bary in zip(faces[ii],np.maximum(ww,0)):
                for joint,weight in zip(attrs[key][source_vertex],attrs[weight_key][source_vertex]):
                    influences[int(joint)]=influences.get(int(joint),0)+float(bary*weight)
            ordered=sorted(influences.items(),key=lambda p:(-p[1],p[0]))[:4]
            mapped[key][vi]=0;mapped[weight_key][vi]=0
            total=sum(weight for joint,weight in ordered)
            for j,(joint,weight) in enumerate(ordered):mapped[key][vi,j]=joint;mapped[weight_key][vi,j]=weight/max(total,1e-20)
        for k in mapped:
            if k.startswith(('JOINTS_','WEIGHTS_')):continue
            if rebake and k in ('NORMAL','TANGENT'):
                # Native corner normals identify the surviving side of a thin
                # shell better than nearest-point projection after its bevel
                # has collapsed. The bake transports the complete source
                # shading into this new tangent frame.
                continue
            value=ww@attrs[k][faces[ii]]
            if k in ('NORMAL','TANGENT'):
                if k=='TANGENT':
                    normal=ww@attrs['NORMAL'][faces[ii]];normal/=max(np.linalg.norm(normal),1e-20)
                    value[:3]-=normal*np.dot(normal,value[:3])
                value[:3]/=max(np.linalg.norm(value[:3]),1e-20)
                if k=='TANGENT':value[3]=1 if value[3]>=0 else -1
            mapped[k][vi]=value
    out={'POSITION':positions.astype(np.float32), **mapped}
    basis_repairs=0
    if rebake:
        # Collapse transports smooth corner normals; when a tiny bevel goes,
        # that interpolation can point a surviving corner through its own
        # face. Split that corner and use its new face's tangent frame. The
        # appearance bake carries the original smooth shading in that frame.
        t=positions[tris];gn=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
        gn/=np.maximum(np.linalg.norm(gn,axis=1,keepdims=True),1e-20)
        corner_normals=out['NORMAL'][tris]
        bad=np.einsum('fvi,fi->fv',corner_normals,gn)<1e-5
        basis_repairs=int(bad.sum())
        if basis_repairs:
            out={k:v[tris.ravel()].copy() for k,v in out.items()}
            out['NORMAL'][bad.ravel()]=np.repeat(gn,3,axis=0)[bad.ravel()]
            if 'TANGENT' in out:
                tt=out['TANGENT'][:,:3];nn=out['NORMAL']
                tt-=nn*np.sum(nn*tt,axis=1,keepdims=True)
                zero=np.linalg.norm(tt,axis=1)<1e-8
                if zero.any():
                    axes=np.eye(3)[np.argmin(np.abs(nn[zero]),axis=1)];tt[zero]=np.cross(axes,nn[zero])
                tt/=np.maximum(np.linalg.norm(tt,axis=1,keepdims=True),1e-20)
            positions=out['POSITION'].astype(float);tris=np.arange(len(positions),dtype=np.uint32).reshape(-1,3)
    # Validate interpolation over candidate triangles. This catches a collapse
    # spanning unrelated UV islands, not just errors at the retained vertices.
    for weights in [(1/3,1/3,1/3),(.5,.5,0),(0,.5,.5),(.5,0,.5)]:
        w=np.array(weights)
        for tri in tris:
            p=w@positions[tri];q,_,i,d=bvh.find_nearest(Vector(p));err=max(err,d)
            surface_samples.append(d)
            t=positions[tri];surface_weights.append(float(np.linalg.norm(np.cross(t[1]-t[0],t[2]-t[0])))/4)
            bw=barycentric(np.array(q),source[faces[i]])
            uv_keys=[k for k in attrs if k.startswith('TEXCOORD_')]
            data_keys=[k for k in attrs if k.startswith(('COLOR_','_WIND'))]
            if (uv_keys or data_keys) and not rebake:
                # Coincident backs, seam endpoints and overlaid decals can be
                # equidistant. Test all nearby source triangles; never let an
                # arbitrary BVH tie select a different chart.
                candidates=bvh.find_nearest_range(Vector(p),max(1e-6,d+1e-6))
                best=float('inf');best_field=float('inf')
                for qq,nn,ii,dd in candidates:
                    ww=barycentric(np.array(qq),source[faces[ii]])
                    e=max((float(np.max(np.abs(w@out[k][tri]-ww@attrs[k][faces[ii]]))) for k in uv_keys),default=0.)
                    data_error=max((float(np.max(np.abs(w@out[k][tri]-ww@attrs[k][faces[ii]]))) for k in data_keys),default=0.)
                    if e<best-1e-6:best=e;best_field=data_error
                    elif e<=best+1e-6:best_field=min(best_field,data_error)
                uv_error=max(uv_error,best)
                field_error=max(field_error,best_field)
    before,boundary0=topology(attrs,faces); after,boundary1=topology(out,tris)
    # Test old chart/crease vertices are still present, not just the aggregate
    # number of open edges. Candidate boundary edges must cover the same paths.
    tree=BVHTree.FromPolygons([Vector(p) for p in positions],tris.tolist(),all_triangles=True)
    reverse_distances=[tree.find_nearest(Vector(p))[3] for p in source]
    reverse=max(reverse_distances,default=0)
    area=np.linalg.norm(np.cross(source[faces[:,1]]-source[faces[:,0]],source[faces[:,2]]-source[faces[:,0]]),axis=1)
    vertex_area=np.bincount(faces.ravel(),weights=np.repeat(area/3,3),minlength=len(source))
    surface_samples.extend(reverse_distances);surface_weights.extend(vertex_area)
    order=np.argsort(surface_samples);errors=np.array(surface_samples)[order];weights=np.array(surface_weights)[order]
    cumulative=weights.cumsum();p95_error=float(errors[min(len(errors)-1,int(np.searchsorted(cumulative,cumulative[-1]*.95)))])
    boundary_error=0.
    for edges,other in [(boundary0,boundary1),(boundary1,boundary0)]:
        if not edges:continue
        if not other:boundary_error=float('inf');break
        a=np.array([e[0] for e in other]);b=np.array([e[1] for e in other]);ab=b-a
        centers=KDTree(len(other))
        for j,c in enumerate((a+b)*.5):centers.insert(c,j)
        centers.balance()
        for e in edges:
            for p in [np.array(e[0]),np.array(e[1]),(np.array(e[0])+e[1])*.5]:
                ids=[j for _,j,_ in centers.find_n(p,min(12,len(other)))]
                aa=a[ids];v=ab[ids];denom=np.maximum(np.sum(v*v,axis=1),1e-30)
                t=np.clip(np.sum((p-aa)*v,axis=1)/denom,0,1)
                boundary_error=max(boundary_error,float(np.linalg.norm(aa+t[:,None]*v-p,axis=1).min()))
    reason=[]
    # Localized bevel deletion can exceed the structural budget at a handful
    # of samples. It shares the two-pixel small-feature ceiling, while 95% of
    # the sampled surface area must remain inside 3/4 pixel. Image and alpha
    # overlap gates judge the full asset, including the omitted features.
    surface_failed=(p95_error>max_error or max(err,reverse)>max_error*(2/.75)) if rebake else max(err,reverse)>max_error
    if surface_failed:
        reason.append('surface distance')
    # Material primitives meet along open boundary paths. Unlike a silhouette
    # approximation, a drift here can create a real crack between materials.
    if boundary_error>(max_error if screen_space else 3e-6): reason.append('boundary drift')
    if uv_error>max_uv_error and not rebake: reason.append('UV field deviation')
    # Vertex weathering/AO is an interpolated surface field too. Re-triangulating
    # identical planar positions can otherwise introduce broad triangular bands.
    if field_error>.01 and not rebake:reason.append('color/Wind field deviation')
    for key in ('degenerate',*(() if rebake else ('degenerate_uv',)),'slivers','nonmanifold_edges','winding_disagreements'):
        if after[key]>before[key]:reason.append(key)
    if not rebake and any(n>before['degenerate_uv_by_layer'].get(k,0) for k,n in after['degenerate_uv_by_layer'].items()):
        reason.append('degenerate UV layer')
    report=dict(triangles=len(tris), candidate_triangles=len(tris), mode=mode, surface_error_m=max(err,reverse),surface_area_p95_m=p95_error,rebaked_corner_basis_repairs=basis_repairs, uv_error=uv_error,field_error=field_error,
                boundary_error_m=boundary_error if math.isfinite(boundary_error) else None, before=before, after=after)
    if reason:return attrs,faces,dict(report,status='rejected',reason=reason,triangles=len(faces))
    return out,tris,dict(report,status='simplified')


def simplify_parts(attrs,faces,ratio,max_error,max_uv_error,drop_subpixel=False,*,screen_space=False,feature_error=None,rebake=False):
    """Accept/reject per connected construction component, not whole atlas.

A failed bolt must not discard a valid body reduction. Components are computed
on coincident geometric vertices, never across separated moving objects or
materials. All corner splits remain in each component's delivered data.
"""
    if any(k.startswith(('JOINTS_','WEIGHTS_')) for k in attrs) and not screen_space:
        return attrs,faces,dict(status='retained',reason='skin data protected',triangles=len(faces))
    _,remap=np.unique(np.round(attrs['POSITION'],7),axis=0,return_inverse=True)
    parents=list(range(int(remap.max())+1))
    def root(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for t in remap[faces]:
        r=root(t[0]);parents[root(t[1])]=r;parents[root(t[2])]=r
    groups={}
    for i,t in enumerate(remap[faces]):groups.setdefault(root(t[0]),[]).append(i)
    fields={k:[] for k in attrs};triangles=[];offset=0;reports=[];dropped=0
    for ids in groups.values():
        old=faces[ids];vertices,indices=np.unique(old,return_inverse=True)
        aa={k:a[vertices] for k,a in attrs.items()};ff=indices.reshape(-1,3).astype(np.uint32)
        # Disconnected fine fittings/decal components may disappear only when
        # their entire 3D diameter is below the configured projected pixel
        # tolerance. Never remove the only component or all geometry of a node.
        if drop_subpixel and len(groups)>1 and np.linalg.norm(np.ptp(aa['POSITION'],axis=0))<(feature_error or max_error):
            dropped+=len(ff);continue
        best,bf=aa,ff;attempts=[]
        if len(ff)>=12:
            for rr in [ratio,1-(1-ratio)*.9,1-(1-ratio)*.5,1-(1-ratio)*.2]:
                new,tri,row=simplify(aa,ff,rr,max_error,max_uv_error=max_uv_error,screen_space=screen_space,rebake=rebake);attempts.append(row)
                if row['status']=='simplified' and len(tri)<len(bf):best,bf=new,tri;break
            # Planar dissolve sometimes beats a gentle collapse on a stamped
            # plate. Always compare the independently checked result.
            new,tri,row=simplify(aa,ff,1,max_error,mode='DISSOLVE',max_uv_error=max_uv_error,screen_space=screen_space,rebake=rebake);attempts.append(row)
            if row['status']=='simplified' and len(tri)<len(bf):best,bf=new,tri
            reports.append(dict(source_triangles=len(ff),triangles=len(bf),attempts=attempts))
        for k in fields:fields[k].append(best[k])
        triangles.append(bf+offset);offset+=len(best['POSITION'])
    if not triangles:return attrs,faces,dict(status='retained',triangles=len(faces),reason='would remove entire primitive')
    out={k:np.concatenate(a) for k,a in fields.items()};tri=np.concatenate(triangles)
    return out,tri,dict(status='simplified' if len(tri)<len(faces) else 'retained',
                       triangles=len(tri),components=len(groups),dropped_subpixel_triangles=dropped,components_tested=reports)


def components(attrs, faces):
    """Geometric islands, independent of UV/normal splits; stable source order."""
    _,remap=np.unique(np.round(attrs['POSITION'],7),axis=0,return_inverse=True)
    parent=np.arange(int(remap.max())+1)
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for t in remap[faces]:
        r=root(t[0]);parent[root(t[1])]=r;parent[root(t[2])]=r
    groups={}
    for i,t in enumerate(remap[faces]):groups.setdefault(root(t[0]),[]).append(i)
    return list(groups.values())


def reduce_screen(attrs,faces,ratio,meters_per_pixel,feature_pixels=1.5,rebake=False,uv_limit=.001,surface_pixels=.75):
    """Level-sized trial. Component size is a pruning criterion, not a veto.

    A new atlas permits removing UV charts; it never claims preservation of
    their old UVs. All appearance must be transferred and judged after export.
    """
    groups=components(attrs,faces);keep=[];removed=[]
    for ids in groups:
        points=attrs['POSITION'][np.unique(faces[ids])]
        diameter=float(np.linalg.norm(np.ptp(points,axis=0)))/meters_per_pixel
        centered=points-points.mean(axis=0)
        _,axes=np.linalg.eigh(centered.T@centered)
        extent=np.sort(np.ptp(centered@axes,axis=0)/meters_per_pixel)
        # A long narrow trim/fitting can have a large diameter yet contribute
        # only a subpixel line. Keep long structural bars; the render gate
        # judges shorter trim and wafer-like knob skirts after baking.
        thin=extent[1]<feature_pixels and extent[2]<48
        local,remap=np.unique(faces[ids],return_inverse=True)
        boundary=topology(dict(POSITION=attrs['POSITION'][local]),remap.reshape(-1,3))[0]['boundary_edges']
        if len(groups)>1 and not boundary and (diameter<feature_pixels or thin):removed.append(dict(triangles=len(ids),diameter_pixels=diameter,principal_extents_pixels=extent.tolist(),kind='thin detail' if thin else 'small island'))
        else:keep.extend(ids)
    if not keep:keep=list(range(len(faces)));removed=[]
    ff=faces[sorted(keep)];vertices,indices=np.unique(ff,return_inverse=True)
    aa={k:v[vertices] for k,v in attrs.items()};ff=indices.reshape(-1,3).astype(np.uint32)
    ratio=min(.999,ratio*len(faces)/len(ff));trials=[]
    if rebake:
        a,f,row=simplify_parts(aa,ff,ratio,meters_per_pixel*surface_pixels,uv_limit,False,screen_space=True,rebake=True)
        return a,f,dict(status=row['status'],triangles=len(f),removed_features=removed,component_trials=row)
    # The render check decides whether omitted features matter. Surface samples
    # constrain the retained structure, never the distance to an omitted screw.
    for rr in [ratio,ratio+(1-ratio)*.25,ratio+(1-ratio)*.5]:
        a,f,row=simplify(aa,ff,rr,meters_per_pixel*surface_pixels,max_uv_error=uv_limit,screen_space=True,rebake=rebake)
        trials.append(row)
        if row['status']=='simplified':break
    return a,f,dict(status='simplified',triangles=len(f),removed_features=removed,trials=trials)


def uv_budget(attrs,faces,meters_per_pixel,texture_size):
    """Half a texel of the estimated trilinear mip, in normalized UV units.

    Surface/UV area estimates the average isotropic footprint; render checks
    remain authoritative at grazing angles and on anisotropic charts.
    """
    p=attrs['POSITION'][faces].astype(float)
    area=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1).sum()
    budgets={}
    for key,values in attrs.items():
        if not key.startswith('TEXCOORD_'):continue
        u=values[faces].astype(float);a=u[:,1]-u[:,0];b=u[:,2]-u[:,0]
        uv_area=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0]).sum()
        density=texture_size*np.sqrt(uv_area/max(area,1e-30))
        footprint=max(1.,density*meters_per_pixel)
        budgets[key]=dict(texels_per_meter=float(density),sampled_mip=float(np.log2(footprint)),
                          texel_tolerance=.5,normalized_tolerance=.5*footprint/texture_size)
    return budgets
