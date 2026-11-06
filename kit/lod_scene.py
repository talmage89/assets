"""LOD-only assembly consolidation and closed proxies in delivered space."""
import copy
import fnmatch
import math

import bpy
import bmesh
import numpy as np

from kit.lod_mesh import topology,components


def merge_static(doc,protected_patterns=(),include_roots=()):
    """Weldable material groups share a mesh; moving frames remain canonical.

    All original named nodes/transforms remain, even when a mesh is rehomed.
    Per-node source provenance also drives isolated appearance transfer.
    """
    groups={};keep=[]
    animated={channel['target']['node'] for clip in doc.data.get('animations',[]) for channel in clip.get('channels',[]) if 'node' in channel.get('target',{})}
    for ni,node in enumerate(doc.data['nodes']):
        if 'mesh' not in node:continue
        moving='skin' in node;current=ni;module=None
        while True:
            n=doc.data['nodes'][current];extra=n.get('extras',{})
            moving|=current in animated or any(k in extra for k in ('pivot_axis','slide_axis','socket_kind')) or any(fnmatch.fnmatchcase(n.get('name',''),p) for p in protected_patterns)
            if n.get('name') in include_roots:module=n['name']
            if current not in doc.parents:break
            current=doc.parents[current]
        if moving:
            keep.append(ni);node.setdefault('extras',{})['lod_sources']=[ni]
        else:groups.setdefault(module or 'Static',[]).append(ni)
    receipt=[]
    for label,ids in groups.items():
        by_material={}
        for ni in ids:
            node=doc.data['nodes'][ni];matrix=doc.world(ni)
            for p in doc.data['meshes'][node['mesh']]['primitives']:
                attrs,faces=doc.arrays(p);attrs={k:v.copy() for k,v in attrs.items()}
                attrs['POSITION']=(attrs['POSITION']@matrix[:3,:3].T+matrix[:3,3]).astype(np.float32)
                for key in ('NORMAL','TANGENT'):
                    if key in attrs:
                        xyz=attrs[key][:,:3]@np.linalg.inv(matrix[:3,:3]);xyz/=np.maximum(np.linalg.norm(xyz,axis=1,keepdims=True),1e-20);attrs[key][:,:3]=xyz
                by_material.setdefault((p.get('material',0),tuple(sorted(attrs))),[]).append((attrs,faces))
            node.pop('mesh')
        primitives=[]
        for (material,keys),pieces in by_material.items():
            offset=0;triangles=[]
            for a,f in pieces:triangles.append(f.astype(np.uint32)+offset);offset+=len(a['POSITION'])
            attrs={k:np.concatenate([a[k] for a,f in pieces]) for k in keys}
            # Complete corner signatures are welded here; geometric welding in
            # the native decimator retains seam values on the corner domain.
            signature=np.concatenate([attrs[k] for k in keys],axis=1)
            _,first,remap=np.unique(signature,axis=0,return_index=True,return_inverse=True)
            attrs={k:v[first] for k,v in attrs.items()};faces=remap[np.concatenate(triangles)].astype(np.uint32)
            p=dict(attributes={},indices=0,material=material);doc.replace(p,attrs,faces);primitives.append(p)
        mesh_index=len(doc.data['meshes']);doc.data['meshes'].append(dict(name='LOD_'+label,primitives=primitives))
        node_index=len(doc.data['nodes']);doc.data['nodes'].append(dict(name='LOD_'+label,mesh=mesh_index,extras=dict(lod_sources=ids,lod_static_merge=True)))
        doc.data['scenes'][doc.data.get('scene',0)].setdefault('nodes',[]).append(node_index)
        receipt.append(dict(output_node='LOD_'+label,source_nodes=[doc.data['nodes'][i].get('name') for i in ids]))
    # Compact mesh indices; retain original node indices, skins and animation.
    used=sorted({n['mesh'] for n in doc.data['nodes'] if 'mesh' in n});mapping={old:new for new,old in enumerate(used)}
    doc.data['meshes']=[doc.data['meshes'][i] for i in used]
    for n in doc.data['nodes']:
        if 'mesh' in n:n['mesh']=mapping[n['mesh']]
    return dict(static_groups=receipt,separate_nodes=[doc.data['nodes'][i].get('name') for i in keep])


def construction_components(attrs,faces):
    """Separate shells meeting at a point or a nonmanifold assembly edge.

    Vertex connectivity joins whole roof assemblies through touching trim and
    makes a convex envelope bridge valleys. Manifold edge adjacency retains
    the actual surfaces; coplanar neighbors can then merge deliberately.
    """
    _,remap=np.unique(np.round(attrs['POSITION'],7),axis=0,return_inverse=True)
    parent=np.arange(len(faces));edges={}
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for fi,face in enumerate(remap[faces]):
        for a,b in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0])):
            edges.setdefault(tuple(sorted((int(a),int(b)))),[]).append(fi)
    for ids in edges.values():
        if len(ids)==2:parent[root(ids[1])]=root(ids[0])
    groups={}
    for fi in range(len(faces)):groups.setdefault(root(fi),[]).append(fi)
    return list(groups.values())


def planar_groups(attrs,faces,meters_per_pixel):
    """Merge neighboring coplanar construction, including separate siding boards.

    A half-pixel depth band can become one shell with new baked charts. Spatial
    adjacency prevents unrelated modules on the same plane filling the air.
    """
    groups=construction_components(attrs,faces);flat=[];parent=list(range(len(groups)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,ids in enumerate(groups):
        pp=attrs['POSITION'][np.unique(faces[ids])];center=pp.mean(axis=0)
        _,axis=np.linalg.eigh((pp-center).T@(pp-center));extent=np.sort(np.ptp((pp-center)@axis,axis=0)/meters_per_pixel)
        if extent[0]>.5 or extent[1]<.5 or extent[2]<2:continue
        n=axis[:,0];n*=1 if n[np.argmax(np.abs(n))]>=0 else -1
        flat.append((i,n,float(center@n),pp.min(axis=0),pp.max(axis=0)))
    for index,(i,n,d,lo,hi) in enumerate(flat):
        for j,nn,dd,ll,hh in flat[:index]:
            if n@nn<.9999 or abs(d-dd)>meters_per_pixel*.5:continue
            if np.any(lo>hh+meters_per_pixel) or np.any(ll>hi+meters_per_pixel):continue
            parent[root(i)]=root(j)
    packed={};counts={}
    for i,ids in enumerate(groups):
        r=root(i);packed.setdefault(r,[]).extend(ids);counts[r]=counts.get(r,0)+1
    return [(ids,counts[r]) for r,ids in packed.items()]


def clean_slivers(mesh,meters_per_pixel):
    """Retriangulate nearly coplanar neighbors without deleting shell faces."""
    bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update()
    for attempt in range(4):
        bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update();bad=[]
        for face in bm.faces:
            vv=[v.co for v in face.verts];area=(vv[1]-vv[0]).cross(vv[2]-vv[0]).length
            longest=max(e.calc_length() for e in face.edges)
            if area/max(longest*longest,1e-30)<1e-5:bad.append(face)
        if not bad:break
        edges=set()
        for face in bad:
            candidates=[e for e in face.edges if len(e.link_faces)==2 and e.link_faces[0].normal.dot(e.link_faces[1].normal)>.9999]
            if candidates:edges.add(max(candidates,key=lambda e:e.calc_length()))
        if edges:bmesh.ops.dissolve_edges(bm,edges=list(edges),use_verts=True,use_face_split=False)
        else:bmesh.ops.dissolve_limit(bm,angle_limit=1e-4,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit=set())
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=meters_per_pixel*.002)
    bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    orientation=orient_closed_shells(bm,meters_per_pixel**3*1e-8)
    bm.to_mesh(mesh);bm.free();mesh.update()
    return orientation


def orient_closed_shells(bm, volume_floor=0.):
    """Orient each closed component outward; discard collapsed zero volumes.

    Consistent adjacent winding alone does not establish outward orientation.
    A collapse can invert a thin closed part, and an entire inward component
    still passes edge incidence and face-versus-normal checks.
    """
    unseen=set(bm.faces);flipped=collapsed=0
    while unseen:
        first=unseen.pop();group={first};pending=[first]
        while pending:
            face=pending.pop()
            for edge in face.edges:
                for other in edge.link_faces:
                    if other in unseen:unseen.remove(other);group.add(other);pending.append(other)
        if any(len(e.link_faces)!=2 for f in group for e in f.edges):continue
        origin=np.array(first.verts[0].co,dtype=np.float64);volume=0.
        for face in group:
            p=np.array([v.co[:] for v in face.verts],dtype=np.float64)-origin
            for i in range(1,len(p)-1):volume+=float(np.dot(p[0],np.cross(p[i],p[i+1])))/6
        if abs(volume)<=volume_floor:
            bmesh.ops.delete(bm,geom=list(group),context='FACES');collapsed+=1
        elif volume<0:
            bmesh.ops.reverse_faces(bm,faces=list(group));flipped+=1
    wire=[e for e in bm.edges if not e.link_faces]
    if wire:bmesh.ops.delete(bm,geom=wire,context='EDGES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    bm.normal_update()
    return dict(flipped=flipped,collapsed=collapsed)


def proxy(doc,target,meters_per_pixel,preserve_concavity=(),remesh=False):
    """Closed construction envelopes with concave tube/return preservation.

    Convex envelopes close open sheets without a high-resolution point volume.
    Closed concave pieces (hoses, bent returns) retain their own coarse surface.
    The shared collapse spends the budget across all retained construction.
    """
    from kit.lod_mesh import world_geometry
    source_ids=[i for i,n in enumerate(doc.data['nodes']) if 'mesh' in n]
    attrs,faces=world_geometry(doc,source_ids);positions=attrs['POSITION']
    protected=[];concave_nodes=[]
    for ni in source_ids:
        node=doc.data['nodes'][ni];keep='skin' in node or any(fnmatch.fnmatchcase(node.get('name',''),p) for p in preserve_concavity)
        if keep:concave_nodes.append(node.get('name'))
        for primitive in doc.data['meshes'][node['mesh']]['primitives']:
            protected.extend([keep]*(len(doc.arrays(primitive)[1])))
    protected=np.array(protected,bool)
    mpp=meters_per_pixel
    bpy.ops.wm.read_factory_settings(use_empty=True)
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    reference=BVHTree.FromPolygons([Vector(p) for p in positions],faces.tolist(),all_triangles=True)
    tt=positions[faces];source_areas=np.linalg.norm(np.cross(tt[:,1]-tt[:,0],tt[:,2]-tt[:,0]),axis=1)*.5
    points=[];triangles=[];offset=0;removed=[];concave=0;envelopes=0;pieces=[]
    groups=planar_groups(attrs,faces,mpp)
    component_index=np.empty(len(faces),np.int32)
    component_area=np.array([source_areas[ids].sum() for ids,count in groups])
    for gi,(ids,count) in enumerate(groups):component_index[ids]=gi
    capped_edges=0;oriented_source_shells=0
    for ids,merged_count in groups:
        ff=faces[ids];unique,remap=np.unique(ff,return_inverse=True);pp=positions[unique];ff=remap.reshape(-1,3)
        _,first,weld=np.unique(np.round(pp,8),axis=0,return_index=True,return_inverse=True);pp=pp[first];ff=weld[ff]
        diameter=float(np.linalg.norm(np.ptp(pp,axis=0))/mpp)
        if diameter<1.5:
            removed.append(dict(triangles=len(ff),diameter_pixels=diameter,reason='subpixel island'));continue
        centered=pp-pp.mean(axis=0);values,axes=np.linalg.eigh(centered.T@centered)
        extent=np.sort(np.ptp(centered@axes,axis=0)/mpp)
        thin=extent[1]<1.5 and extent[2]<48
        if thin:
            own=set(map(int,ids));centers=positions[faces[ids]].mean(axis=1)
            sample=centers[np.linspace(0,len(centers)-1,min(12,len(centers)),dtype=int)]
            area=float(extent[1]*extent[2]*mpp*mpp)
            attached=sum(any(fi not in own and component_area[component_index[fi]]>area*2 for q,n,fi,d in reference.find_nearest_range(Vector(p),mpp*1.5)) for p in sample)
            if attached>=len(sample)*.6:
                removed.append(dict(triangles=len(ff),diameter_pixels=diameter,reason='thin attached feature',attached_samples=attached,samples=len(sample)));continue
        # Restore a real closed thickness to open planar source sheets.
        centroid=pp.mean(axis=0);values,axes=np.linalg.eigh((pp-centroid).T@(pp-centroid))
        hull_points=pp
        if values[0]<max(values[-1],1e-20)*1e-12:
            pad=axes[:,0]*mpp*.025;hull_points=np.concatenate([pp-pad,pp+pad])
        bm=bmesh.new()
        for point in hull_points:bm.verts.new(point)
        bm.verts.ensure_lookup_table()
        hull=bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
        unused=[v for v in bm.verts if not v.link_faces]
        if unused:bmesh.ops.delete(bm,geom=unused,context='VERTS')
        bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        oriented_source_shells+=orient_closed_shells(bm)['flipped']
        hull_volume=abs(bm.calc_volume(signed=True))
        native=bmesh.new()
        for point in pp:native.verts.new(point)
        native.verts.ensure_lookup_table()
        for triangle in ff:
            try:native.faces.new([native.verts[int(i)] for i in triangle])
            except ValueError:pass
        bmesh.ops.remove_doubles(native,verts=list(native.verts),dist=1e-6)
        boundary=[e for e in native.edges if e.is_boundary]
        if boundary:bmesh.ops.holes_fill(native,edges=boundary,sides=0)
        bmesh.ops.triangulate(native,faces=list(native.faces));bmesh.ops.recalc_face_normals(native,faces=list(native.faces))
        oriented_source_shells+=orient_closed_shells(native)['flipped']
        native_closed=bool(native.faces) and all(len(e.link_faces)==2 for e in native.edges)
        source_volume=abs(native.calc_volume(signed=True)) if native_closed else 0
        native_closed=native_closed and source_volume>max(hull_volume,1e-20)*1e-8
        # Large concave shells matter as much as thin tubes: convexifying an
        # L-shaped roof bridges its valley, beyond the projection allowance.
        preserve=merged_count==1 and native_closed and (protected[ids].any() or source_volume<hull_volume*.95)
        planes=[(np.array(f.normal),np.array(f.verts[0].co)) for f in bm.faces]
        mesh=bpy.data.meshes.new('LOD construction envelope')
        if preserve:
            bm.free();native.to_mesh(mesh);concave+=1;capped_edges+=len(boundary)
        else:bm.to_mesh(mesh);bm.free();envelopes+=1
        native.free()
        mesh.update()
        vv=np.array([v.co[:] for v in mesh.vertices],np.float32);tt=np.array([p.vertices[:] for p in mesh.polygons],np.uint32)
        # Separate overlapping manufactured shells retain distinct topology.
        # A tiny inward inset prevents incidental coincident cap edges from
        # becoming a nonmanifold weld in importers (far below one texel/pixel).
        delta=vv-centroid;length=np.linalg.norm(delta,axis=1,keepdims=True)
        vv=vv-delta/np.maximum(length,1e-20)*mpp*.002*(1+(len(pieces)*.61803398875)%1)
        pieces.append(dict(vertices=vv,faces=tt,planes=None if preserve else planes,volume=hull_volume,lo=vv.min(axis=0),hi=vv.max(axis=0)))
        bpy.data.meshes.remove(mesh)
    enclosed=0
    for piece in pieces:
        hidden=False
        for other in pieces:
            if other is piece or other['planes'] is None or other['volume']<=piece['volume']*1.01:continue
            if np.any(piece['lo']<other['lo']-mpp*.001) or np.any(piece['hi']>other['hi']+mpp*.001):continue
            if all(np.max((piece['vertices']-q)@n)<=mpp*.001 for n,q in other['planes']):hidden=True;break
        if hidden:enclosed+=1;continue
        points.extend(piece['vertices']);triangles.extend(piece['faces']+offset);offset+=len(piece['vertices'])
    if not points:raise ValueError('Proxy pruning removed all construction')
    mesh=bpy.data.meshes.new('LOD closed envelopes');mesh.from_pydata(points,[],triangles);mesh.update()
    ob=bpy.data.objects.new('LOD closed envelopes',mesh);bpy.context.scene.collection.objects.link(ob)
    ob.select_set(True);bpy.context.view_layer.objects.active=ob
    envelope_triangles=len(triangles);remeshing=None
    if remesh:
        settings=remesh if isinstance(remesh,dict) else {}
        cell=mpp*settings.get('voxel_pixels',.5);inflation=mpp*settings.get('inflation_pixels',.3)
        if not 0<cell<=mpp or not 0<=inflation<=mpp*.5:raise ValueError('Proxy remesh exceeds switch-pixel allowance')
        expand=ob.modifiers.new('Subpixel shell union','DISPLACE');expand.direction='NORMAL';expand.strength=inflation;expand.mid_level=0
        bpy.ops.object.modifier_apply(modifier=expand.name)
        ob.data.remesh_voxel_size=cell;ob.data.remesh_voxel_adaptivity=0.;ob.data.use_remesh_preserve_volume=True
        bpy.ops.object.voxel_remesh()
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        remeshing=dict(voxel_pixels=cell/mpp,inflation_pixels=inflation/mpp,union_triangles=len(ob.data.polygons))
    pre=len(ob.data.polygons)
    if pre>target:
        mod=ob.modifiers.new('Shared envelope budget','DECIMATE');mod.ratio=target/pre;mod.use_collapse_triangulate=True
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=mpp*1e-5)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces))
    orientation=orient_closed_shells(bm,mpp**3*1e-8)
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    cleaned_orientation=clean_slivers(ob.data,mpp)
    orientation={k:orientation[k]+cleaned_orientation[k] for k in orientation}
    vertices=np.array([v.co[:] for v in ob.data.vertices],np.float32)
    faces=np.array([p.vertices[:] for p in ob.data.polygons],np.uint32)
    for polygon in ob.data.polygons:polygon.use_smooth=True
    ob.data.set_sharp_from_angle(angle=math.radians(35));ob.data.update()
    normals=np.array([n.vector[:] for n in ob.data.corner_normals],np.float32)
    aa=dict(POSITION=vertices[faces.ravel()],NORMAL=normals);ff=np.arange(len(aa['POSITION']),dtype=np.uint32).reshape(-1,3)
    report,_=topology(aa,ff)
    if any(report[k] for k in ('boundary_edges','nonmanifold_edges','degenerate','slivers')):
        raise ValueError('Construction proxy is not clean/closed: '+str(report))
    for ni in source_ids:doc.data['nodes'][ni].pop('mesh',None);doc.data['nodes'][ni].pop('skin',None)
    p=dict(attributes={},indices=0,material=0);doc.data['meshes']=[dict(name='LOD_Proxy',primitives=[p])];doc.replace(p,aa,ff)
    ni=len(doc.data['nodes']);doc.data['nodes'].append(dict(name='LOD_Proxy',mesh=0,extras=dict(lod_sources=source_ids,lod_proxy=True,animation='merged rest pose')))
    doc.data['scenes'][doc.data.get('scene',0)].setdefault('nodes',[]).append(ni)
    doc.data.pop('skins',None);doc.data.pop('animations',None)
    return dict(method='voxel union of construction envelopes' if remesh else 'closed construction envelopes',remeshing=remeshing,requested_budget_triangles=target,preserved_concave_nodes=concave_nodes,envelopes=envelopes,concave_parts=concave,planar_merged_components=sum(n-1 for ids,n in groups),removed_enclosed_parts=enclosed,
        closed_source_boundary_edges=capped_edges,oriented_source_shells=oriented_source_shells,final_shell_orientation=orientation,removed_features=removed,input_envelope_triangles=envelope_triangles,input_reduction_triangles=pre,triangles=len(ff),topology=report,
        merged_parts=[doc.data['nodes'][i].get('name') for i in source_ids])


def shell_static(doc,ratio,meters_per_pixel):
    """Close distant static assemblies before reduction, retaining moving parts.

    Closed envelopes remove enclosed construction and collapse distant returns. Original material IDs are assigned by source correspondence;
    per-pixel PBR appearance is subsequently rebaked onto the new shell.
    """
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from kit.lod_transfer import source_hit
    reports=[]
    for ni,node in enumerate(doc.data['nodes']):
        if 'mesh' not in node or not node.get('extras',{}).get('lod_static_merge'):continue
        source_mesh=node['mesh'];points=[];triangles=[];materials=[];offset=0
        for p in doc.data['meshes'][source_mesh]['primitives']:
            a,f=doc.arrays(p);points.extend(a['POSITION']);triangles.extend(f.astype(np.uint32)+offset)
            materials.extend([p.get('material',0)]*len(f));offset+=len(a['POSITION'])
        reference=BVHTree.FromPolygons([Vector(v) for v in points],triangles,all_triangles=True)
        trial=copy.copy(doc);trial.data=copy.deepcopy(doc.data);trial.replacements=doc.replacements.copy();trial.parents=doc.parents.copy()
        for i,n in enumerate(trial.data['nodes']):
            if i!=ni:n.pop('mesh',None)
        target=max(12,round(len(triangles)*ratio))
        report=proxy(trial,target,meters_per_pixel)
        a,f=trial.arrays(trial.data['meshes'][0]['primitives'][0]);by_material={}
        for ti,face in enumerate(f):
            center=a['POSITION'][face].mean(axis=0);normal=a['NORMAL'][face].mean(axis=0)
            hit=source_hit(reference,center,normal,meters_per_pixel*2)
            q,n,fi,d=hit if hit is not None else reference.find_nearest(Vector(center))
            by_material.setdefault(materials[fi],[]).append(ti)
        primitives=[]
        for mi,ids in sorted(by_material.items()):
            p=dict(attributes={},indices=0,material=mi);doc.replace(p,a,f[ids]);primitives.append(p)
        doc.data['meshes'][source_mesh]=dict(name=node['name'],primitives=primitives)
        node['extras']['lod_static_shell']=True
        reports.append(dict(node=node['name'],**report))
    return reports
