"""Attribute-weighted QEM for LODs sampling immutable source maps.

Geometric vertices own split attribute wedges. An edge collapse transports all
wedges together; it preserves UV chart and material membership. Collapses
along seams are synchronized across both sides, including curved seams. Continuous normal wedges carry weighted fields; bounded vertex updates retain
source UV interpolation and synchronize every corner at a geometric vertex. No unwrap, texture resampling or shader change.
"""
import heapq
import numpy as np


def _limit(limits,key,material=0):
    if not isinstance(limits,dict):return float(limits)
    value=limits[key]
    return float(value[str(int(round(float(material))))] if isinstance(value,dict) else value)


def _triangle_limits(attrs,faces,meters_per_pixel,texture_size):
    """Half a sampled-mip texel per source triangle/layer (isotropic)."""
    p=attrs['POSITION'][faces].astype(float)
    area=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)
    result={}
    for key,values in attrs.items():
        if not key.startswith('TEXCOORD_'):continue
        u=values[faces].astype(float);a=u[:,1]-u[:,0];b=u[:,2]-u[:,0]
        uvarea=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])
        footprint=texture_size*np.sqrt(uvarea/np.maximum(area,1e-30))*meters_per_pixel
        result[key]=.5*np.maximum(1.,footprint)/texture_size
    return result


def _uv_error(target,source,source_face,bary,limits,weights=None):
    material=target['_LOD_MATERIAL'][0] if weights is None and '_LOD_MATERIAL' in target else (target['_LOD_MATERIAL'][0,0] if '_LOD_MATERIAL' in target else 0)
    return max((float(np.max(np.abs((v if weights is None else weights@v)-bary@source[k][source_face])))/_limit(limits,k,material) for k,v in target.items() if k.startswith('TEXCOORD_')),default=0.)


def _frame_limits(points,meters_per_pixel):
    """Tight on broad faces; subpixel faces can spend more angular error."""
    edge=points[1:]-points[0];area=np.linalg.norm(np.cross(edge[0],edge[1]))
    longest=max(np.linalg.norm(points[i]-points[j]) for i,j in ((0,1),(1,2),(2,0)))
    width=area/max(longest*meters_per_pixel,1e-20)
    return min(45.,max(3.,15/max(width,1e-8))),min(45.,max(5.,25/max(width,1e-8)))


def _field_error(target,source,faces,positions,gradients,hits,limits,frame_limits=(3.,5.),data_tolerance=.01):
    """Vectorized original-field correspondence on bounded BVH candidates."""
    if not hits:return 1e6,1e6
    ids=np.array([h[2] for h in hits],int);points=np.array([h[0][:] for h in hits],float)
    material=int(round(float(target.get('_LOD_MATERIAL',np.zeros(1))[0])))
    if '_LOD_MATERIAL' in source:
        take=source['_LOD_MATERIAL'][faces[ids,0],0]==material;ids=ids[take];points=points[take]
    if not len(ids):return 1e6,1e6
    edge=np.einsum('ni,nij->nj',points-positions[faces[ids,0]],gradients[ids])
    bary=np.column_stack([1-edge.sum(axis=1),edge]);ff=faces[ids]
    normal=np.einsum('ni,nij->nj',bary,source['NORMAL'][ff]);wanted=target['NORMAL']
    valid=normal@wanted>=np.cos(np.radians(frame_limits[0]))*np.maximum(np.linalg.norm(normal,axis=1)*np.linalg.norm(wanted),1e-20)
    if 'TANGENT' in target and 'TANGENT' in source:
        tangent=np.einsum('ni,nij->nj',bary,source['TANGENT'][ff,:3]);wanted_t=target['TANGENT'][:3]
        valid &= tangent@wanted_t>=np.cos(np.radians(frame_limits[1]))*np.maximum(np.linalg.norm(tangent,axis=1)*np.linalg.norm(wanted_t),1e-20)
        valid &= np.abs(np.einsum('ni,ni->n',bary,source['TANGENT'][ff,3])-target['TANGENT'][3])<1e-4
    if not valid.any():return 1e6,1e6
    bary=bary[valid];ff=ff[valid];ids=ids[valid];uv=np.zeros(len(ff));data=np.zeros(len(ff))
    for k,value in target.items():
        if k.startswith('TEXCOORD_'):
            error=np.max(np.abs(value-np.einsum('ni,nij->nj',bary,source[k][ff])),axis=1)/(limits[k][ids] if isinstance(limits,dict) and isinstance(limits[k],np.ndarray) else _limit(limits,k,material))
            uv=np.maximum(uv,error)
        elif k.startswith(('COLOR_','_WIND')):
            error=np.max(np.abs(value-np.einsum('ni,nij->nj',bary,source[k][ff])),axis=1);data=np.maximum(data,error)
    best=int(np.argmin(np.maximum(uv,data/data_tolerance)));return float(uv[best]),float(data[best])

def collapse(attrs, faces, ratio, uv_weight=10., normal_weight=.5, max_error=None, uv_limit=None,meters_per_pixel=None,seam_sliding=True,data_tolerance=None):
    """Reduce one construction component, retaining its source vertex records.

    Position is normalized by the component diameter. Attribute residual planes
    add UV/normal error to the geometric quadric (area weighted). A topological
    link test and local orientation/quality tests guard every accepted collapse.
    Endpoints avoid independently optimized seams drifting apart.
    """
    data_tolerance=(.02 if seam_sliding else .01) if data_tolerance is None else data_tolerance
    # Exported Mikk tangents can differ at otherwise continuous corners.
    # Those numerical splits are not UV seams; retain one original record.
    signature=np.column_stack([np.round(v,3 if k=='TANGENT' else 6) for k,v in attrs.items()])
    _,first,remap=np.unique(signature,axis=0,return_index=True,return_inverse=True)
    attrs={k:v[first] for k,v in attrs.items()};faces=remap[faces].astype(np.uint32)
    tree=None
    if max_error is not None:
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
        from kit.lod_mesh import barycentric
        tree=BVHTree.FromPolygons([Vector(p) for p in attrs['POSITION']],faces.tolist(),all_triangles=True)
    pos=attrs['POSITION'].astype(float)
    _,first,geo=np.unique(np.round(pos,6 if seam_sliding else 8),axis=0,return_index=True,return_inverse=True)
    reference_pos=pos.copy()
    points=pos[first];clusters=[{i} for i in range(len(points))];scale=max(float(np.linalg.norm(np.ptp(pos,axis=0))),1e-8)
    center=points.mean(axis=0)
    values=[(pos-center)/scale];weights=[]
    for key,a in attrs.items():
        if key.startswith('TEXCOORD_'):w=uv_weight
        elif key=='NORMAL':w=normal_weight
        elif key.startswith(('COLOR_','_WIND')):w=1.
        else:continue
        values.append(a.astype(float)*w);weights.extend([w]*a.shape[1])
    data=np.column_stack(values);dim=data.shape[1];hom=np.column_stack([data,np.ones(len(data))])
    q=np.zeros((len(pos),dim+1,dim+1),float);quv=np.zeros_like(q);qc=np.zeros_like(q)
    t=data[faces,:3];edge1=t[:,1]-t[:,0];edge2=t[:,2]-t[:,0]
    cross=np.cross(edge1,edge2);areas=np.linalg.norm(cross,axis=1)
    normals=cross/np.maximum(areas[:,None],1e-30)
    planes=np.zeros((len(faces),dim+1));planes[:,:3]=normals
    planes[:,-1]=-np.einsum('ij,ij->i',normals,t[:,0])
    fq=np.einsum('fi,fj,f->fij',planes,planes,areas)
    geometric=fq.copy();uvquad=np.zeros_like(fq);colorquad=np.zeros_like(fq)
    channels=[]
    for key,value in attrs.items():
        if key.startswith('TEXCOORD_') or key=='NORMAL' or key.startswith(('COLOR_','_WIND')):channels.extend([key]*value.shape[1])
    # Affine attribute gradient in the original triangle's plane. Its residual
    # is zero throughout that triangle, rather than just at its vertices.
    edges=np.stack([edge1,edge2],axis=1)
    inverse=np.linalg.pinv(edges)
    source_gradients=inverse/scale
    for channel in range(3,dim):
        delta=np.stack([data[faces[:,1],channel]-data[faces[:,0],channel],data[faces[:,2],channel]-data[faces[:,0],channel]],axis=1)
        gradient=np.einsum('fij,fj->fi',inverse,delta)
        r=np.zeros_like(planes);r[:,:3]=-gradient;r[:,channel]=1
        r[:,-1]=np.einsum('ij,ij->i',gradient,t[:,0])-data[faces[:,0],channel]
        field_quad=np.einsum('fi,fj,f->fij',r,r,areas);fq+=field_quad
        if channels[channel-3].startswith('TEXCOORD_'):
            material=attrs.get('_LOD_MATERIAL',np.zeros((len(pos),1)))[faces[:,0],0]
            limits=(uv_limit[channels[channel-3]] if isinstance(uv_limit,dict) and isinstance(uv_limit[channels[channel-3]],np.ndarray) else np.array([_limit(uv_limit,channels[channel-3],m) for m in material])) if uv_limit is not None else np.ones(len(faces))
            uvquad+=field_quad/limits[:,None,None]**2
        elif channels[channel-3].startswith(('COLOR_','_WIND')):colorquad+=field_quad
    qg=np.zeros_like(q);support=np.zeros(len(pos))
    for j in range(3):
        np.add.at(q,faces[:,j],fq);np.add.at(qg,faces[:,j],geometric);np.add.at(quv,faces[:,j],uvquad);np.add.at(qc,faces[:,j],colorquad);np.add.at(support,faces[:,j],areas)
    tri=faces.copy();alive=np.ones(len(tri),bool);incident=[set() for _ in points]
    for fi,face in enumerate(geo[tri]):
        for g in face:incident[int(g)].add(fi)
    edge_counts={}
    for face in geo[tri]:
        for x,y in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0])):
            e=tuple(sorted((int(x),int(y))));edge_counts[e]=edge_counts.get(e,0)+1
    boundary={g for e,n in edge_counts.items() if n==1 for g in e}
    # Screen-aware path slides boundary vertices along their own source edge.
    # Legacy calls retain their historical exact boundary behavior.
    fixed=set(boundary) if max_error is None or not seam_sliding else set()
    if '_LOD_KEEP' in attrs:fixed.update(int(geo[v]) for v in np.flatnonzero(attrs['_LOD_KEEP'][:,0]))
    current={k:v.astype(float).copy() for k,v in attrs.items()}
    original_points=points.copy()
    face_area=areas.copy()*scale**2
    source_area=float(face_area.sum());target_area=source_area
    source_vertex_area=np.bincount(geo[faces].ravel(),weights=np.repeat(face_area/3,3),minlength=len(points))
    face_excess=np.zeros(len(faces));reverse_excess=np.zeros(len(points));total_excess=0.
    structural=(max_error*.75/2)*.999 if max_error is not None else 0.
    weighted=[(k,uv_weight if k.startswith('TEXCOORD_') else normal_weight if k=='NORMAL' else 1.) for k in attrs if k.startswith('TEXCOORD_') or k=='NORMAL' or k.startswith(('COLOR_','_WIND'))]
    versions=np.zeros(len(points),np.int64);heap=[];serial=0;remaining=len(tri);rejected=0;updated=0
    def neighbors(g):
        return {int(v) for fi in incident[g] for v in geo[tri[fi]] if v!=g}
    def wedges(g):return {int(v) for fi in incident[g] for v in tri[fi] if geo[v]==g}
    def mapping(a,b):
        if b in fixed:return None
        common=incident[a]&incident[b]
        if not common or (not seam_sliding and len(common) not in (1,2)):return None
        opposite={int(g) for fi in common for g in geo[tri[fi]] if g not in (a,b)}
        if neighbors(a)&neighbors(b)!=opposite:return None
        if seam_sliding:
            # Preserve local incidence classes, not merely global edge totals.
            # Removing two faces at a three-face junction must not expose the
            # remaining face while unrelated open boundaries disappear.
            for g in (neighbors(a)|neighbors(b))-{a,b}:
                ca=len(incident[a]&incident[g]);cb=len(incident[b]&incident[g])
                count=len(((incident[a]|incident[b])&incident[g])-common)
                if count==1 and ca!=1 and cb!=1:return None
                if count>2 and max(ca,cb)<=2:return None
        pair={}
        for fi in common:
            f=tri[fi];gg=geo[f];wa=int(f[np.flatnonzero(gg==a)[0]]);wb=int(f[np.flatnonzero(gg==b)[0]])
            if wb in pair and pair[wb]!=wa:return None
            pair[wb]=wa
        unmatched=wedges(b)-set(pair)
        # Join only redundant frame splits within a continuous UV chart.
        # A real normal/tangent discontinuity remains a separate corner even
        # when its UV is continuous: the old normal map was baked in that frame.
        for wb in list(unmatched):
            for other,wa in list(pair.items()):
                keys=[k for k in current if k.startswith(('TEXCOORD_','COLOR_','_WIND','_LOD_'))]
                if any(np.max(np.abs(current[k][wb]-current[k][other]))>1e-6 for k in keys):continue
                if any(current[k][wb,:3]@current[k][other,:3]<np.cos(np.radians(1))*np.linalg.norm(current[k][wb,:3])*np.linalg.norm(current[k][other,:3]) for k in ('NORMAL','TANGENT') if k in current):continue
                if 'TANGENT' in current and current['TANGENT'][wb,3]!=current['TANGENT'][other,3]:continue
                pair[wb]=wa;unmatched.remove(wb);break
        if unmatched:
            if max_error is None or (not seam_sliding and np.linalg.norm(points[a]-points[b])>max_error*.75):return None
            pair.update({wb:wb for wb in unmatched})
        boundary_b={g for g in neighbors(b) if len(incident[b]&incident[g])==1}
        if boundary_b and a not in boundary_b:return None
        return pair,common
    source_incident=[[] for _ in pos]
    for fi,face in enumerate(faces):
        for v in face:source_incident[v].append(fi)
    def values_for(a,b,pairs,t):
        if not seam_sliding:
            result={wa:{k:current[k][wa].copy() for k in attrs if k!='POSITION'} for wa in wedges(a)|set(pairs.values())}
            seen=set()
            for wb,wa in pairs.items():
                if t and wa in seen:return None
                seen.add(wa)
                if wb==wa or not t:continue
                fields=result[wa]
                for k in fields:
                    if k not in ('_LOD_MATERIAL','_LOD_KEEP'):fields[k]=(1-t)*current[k][wa]+t*current[k][wb]
                if 'NORMAL' in fields:fields['NORMAL']/=max(np.linalg.norm(fields['NORMAL']),1e-20)
                if 'TANGENT' in fields:
                    tt=fields['TANGENT'];nn=fields['NORMAL'];tt[:3]-=nn*(tt[:3]@nn)
                    if np.linalg.norm(tt[:3])<1e-10:return None
                    tt[:3]/=np.linalg.norm(tt[:3]);tt[3]=1 if tt[3]>=0 else -1
            return result
        result={wa:{k:current[k][wa].copy() for k in attrs if k!='POSITION'} for wa in wedges(a)|set(pairs.values())}
        partners={}
        for wb,wa in pairs.items():partners.setdefault(wa,[]).append(wb)
        point=(1-t)*points[a]+t*points[b]
        for wa,partners_b in partners.items():
            fields=result[wa]
            if not t and partners_b!=[wa]:continue
            if partners_b==[wa]:
                # A normal/tangent wedge can terminate at b while the same UV
                # chart continues at a with another frame split. Carry its own
                # affine source field to the common edge point, rather than
                # pinning the UV at b or merging incompatible normal corners.
                ids=np.array(source_incident[wa],int)
                if not len(ids):return None
                projected=np.einsum('ni,nij->nj',point-reference_pos[faces[ids,0]],source_gradients[ids])
                bary=np.column_stack([1-projected.sum(1),projected])
                world=np.einsum('ni,nij->nj',bary,reference_pos[faces[ids]])
                score=np.linalg.norm(world-point,axis=1)/max(max_error or 1.,1e-20)+np.maximum(-bary,0).sum(1)
                chosen=int(np.argmin(score));weights_b=bary[chosen];source_face=faces[ids[chosen]]
                for k in fields:
                    if k not in ('_LOD_MATERIAL','_LOD_KEEP'):fields[k]=weights_b@attrs[k][source_face]
            elif t:
                for k in fields:
                    if k not in ('_LOD_MATERIAL','_LOD_KEEP'):fields[k]=(1-t)*current[k][wa]+t*np.mean(current[k][partners_b],axis=0)
            if 'NORMAL' in fields:fields['NORMAL']/=max(np.linalg.norm(fields['NORMAL']),1e-20)
            if 'TANGENT' in fields:
                tt=fields['TANGENT'];nn=fields['NORMAL'];tt[:3]-=nn*(tt[:3]@nn)
                if np.linalg.norm(tt[:3])<1e-10:return None
                tt[:3]/=np.linalg.norm(tt[:3]);tt[3]=1 if tt[3]>=0 else -1
        return result
    def frame(fields,point):
        return np.concatenate([(point-center)/scale,*[fields[k]*w for k,w in weighted],[1.]])
    def quadrics(a,pairs):
        result={wa:[q[wa].copy(),qg[wa].copy(),quv[wa].copy(),qc[wa].copy(),support[wa]] for wa in wedges(a)|set(pairs.values())}
        for wb,wa in pairs.items():
            if wb==wa:continue
            for i,source in enumerate((q,qg,quv,qc)):result[wa][i]+=source[wb]
            result[wa][4]+=support[wb]
        return result
    def offer_legacy(a,b):
        nonlocal serial
        if not incident[a] or not incident[b]:return
        m=mapping(a,b)
        if m is None:return
        pairs,common=m;combined=quadrics(a,pairs)
        for t in ((0.,.5) if max_error is not None and a not in fixed else (0.,)):
            fields=values_for(a,b,pairs,t)
            if fields is None:continue
            point=points[a].copy()
            if t:
                matrix=np.zeros((3,3));linear=np.zeros(3)
                for wa,field in fields.items():
                    h=frame(field,center);qq=combined[wa][0]
                    matrix+=qq[:3,:3];linear+=qq[:3]@h
                regularizer=max(float(np.trace(matrix))*1e-10,1e-20)
                anchor=((points[a]+points[b])*.5-center)/scale
                point=np.linalg.solve(matrix+np.eye(3)*regularizer,-linear+anchor*regularizer)*scale+center
                if not np.isfinite(point).all() or np.any(point<reference_pos.min(axis=0)-max_error) or np.any(point>reference_pos.max(axis=0)+max_error):continue
            cost=0.;valid=True
            for wa,field in fields.items():
                h=frame(field,point);qq,gg,uu,cc,area=combined[wa];area=max(area,1e-30)
                if max_error is not None and (h@gg@h>area*(max_error/scale)**2 or h@uu@h>area*uv_weight**2 or h@cc@h>area*data_tolerance**2):valid=False;break
                cost+=max(0.,float(h@qq@h))
            if valid:
                serial+=1;heapq.heappush(heap,(cost,a,b,int(versions[a]),int(versions[b]),serial,t,*map(float,point)))
    def offer(a,b):
        if not seam_sliding:return offer_legacy(a,b)
        nonlocal serial
        if not incident[a] or not incident[b]:return
        m=mapping(a,b)
        if m is None:return
        pairs,common=m;combined=quadrics(a,pairs)
        # Optimize one common edge parameter; each UV/normal side evaluates
        # its own field at that same position. The former free 3D solve with
        # midpoint attributes introduced UV drift even on planar charts.
        parameters=[0.]
        if max_error is not None and a not in fixed and (a not in boundary or b in boundary):
            f0=values_for(a,b,pairs,0.);f1=values_for(a,b,pairs,1.)
            if f0 is not None and f1 is not None:
                numerator=denominator=0.
                for wa in f0:
                    h0=frame(f0[wa],points[a]);delta=frame(f1[wa],points[b])-h0;qq=combined[wa][0]
                    numerator+=float(delta@qq@h0);denominator+=float(delta@qq@delta)
                optimum=float(np.clip(-numerator/max(denominator,1e-30),0,1))
                parameters=sorted(set([0.,optimum,.5]))
        for t in parameters:
            fields=values_for(a,b,pairs,t)
            if fields is None:continue
            point=(1-t)*points[a]+t*points[b]
            cost=0.;valid=True
            for wa,field in fields.items():
                h=frame(field,point);qq,gg,uu,cc,area=combined[wa];area=max(area,1e-30)
                # Attribute quadrics extrapolate the incident face gradients.
                # On curved charts that estimate can exceed the true sampled
                # error by orders of magnitude. Use it to rank candidates;
                # source-side UV/frame/color samples below enforce the bounds.
                if max_error is not None and h@gg@h>area*(max_error/scale)**2:valid=False;break
                cost+=max(0.,float(h@qq@h))
            if valid:
                serial+=1;heapq.heappush(heap,(cost,a,b,int(versions[a]),int(versions[b]),serial,t,*map(float,point)))
    edges=set()
    for face in geo[tri]:
        for a,b in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0])):edges.add(tuple(sorted((int(a),int(b)))))
    for a,b in sorted(edges):offer(a,b);offer(b,a)
    from kit.lod_constraints import inventory
    constraints=inventory(attrs,faces,fixed=fixed,eligible={entry[2] for entry in heap},geometry_remap=geo)
    target=max(4,round(len(faces)*ratio));accepted=0
    samples=(np.array([1/3]*3),np.array([.5,.5,0]),np.array([0,.5,.5]),np.array([.5,0,.5]))
    while heap and remaining>target:
        cost,a,b,va,vb,_,t,*point=heapq.heappop(heap);point=np.array(point)
        if va!=versions[a] or vb!=versions[b] or not incident[a] or not incident[b]:continue
        m=mapping(a,b)
        if m is None:continue
        pairs,common=m
        if remaining-len(common)<4:continue
        affected=incident[a]|incident[b];fields=values_for(a,b,pairs,t)
        if fields is None:continue
        valid=True;new_faces={};new_geometry=[];new_areas={};new_excess={}
        if tree is not None and (t or any(wb==wa for wb,wa in pairs.items())):
            hits=tree.find_nearest_range(Vector(point),max_error+1e-7)
            for field in fields.values():
                best_uv,best_data=_field_error(field,attrs,faces,reference_pos,source_gradients,hits,uv_limit,data_tolerance=data_tolerance)
                if best_uv>.999 or best_data>data_tolerance:valid=False;break
        if not valid:rejected+=1;continue
        for fi in affected-common:
            old=tri[fi];new=np.array([pairs.get(int(v),int(v)) for v in old],np.uint32)
            p0=pos[old];p1=pos[new].copy();p1[np.isin(geo[old],[a,b])]=point
            cv={k:np.array([fields[int(v)][k] if int(v) in fields else current[k][v] for v in new]) for k in attrs if k!='POSITION'}
            n0=np.cross(p0[1]-p0[0],p0[2]-p0[0]);n1=np.cross(p1[1]-p1[0],p1[2]-p1[0]);length=np.linalg.norm(n1)
            longest=max(np.sum((p1[i]-p1[j])**2) for i,j in ((0,1),(1,2),(2,0)))
            if length<1e-14 or length/max(longest,1e-30)<1e-5 or n0@n1<=.1*np.linalg.norm(n0)*length or n1@cv['NORMAL'].sum(axis=0)<-1e-10:valid=False;break
            for k,v in cv.items():
                if not k.startswith('TEXCOORD_'):continue
                x=current[k][old];ex=x[1:]-x[0];ey=v[1:]-v[0]
                det0=ex[0,0]*ex[1,1]-ex[0,1]*ex[1,0];det1=ey[0,0]*ey[1,1]-ey[0,1]*ey[1,0]
                if abs(det0)>1e-14 and (abs(det1)<1e-14 or det0*det1<=0):valid=False;break
            if not valid:break
            if tree is not None:
                excess=0.
                frame_limits=_frame_limits(p1,meters_per_pixel or max_error*.75/2)
                for w in samples:
                    p=w@p1;hit=tree.find_nearest(Vector(p))
                    if hit[3]>max_error:valid=False;break
                    if hit[3]>structural:excess+=length/4
                    target_fields={k:w@v for k,v in cv.items()}
                    best_uv,best_data=_field_error(target_fields,attrs,faces,reference_pos,source_gradients,[hit],uv_limit,frame_limits,data_tolerance)
                    if best_uv>1. or best_data>data_tolerance:
                        best_uv,best_data=_field_error(target_fields,attrs,faces,reference_pos,source_gradients,tree.find_nearest_range(Vector(p),max_error+1e-7),uv_limit,frame_limits,data_tolerance)
                    if best_uv>1. or best_data>data_tolerance:valid=False;break
                if not valid:break
            new_faces[fi]=new;new_geometry.extend(p1);new_areas[fi]=length;new_excess[fi]=excess if tree is not None else 0.
        touched=neighbors(a)|neighbors(b)|{a,b};next_excess=total_excess;next_area=target_area;new_reverse={}
        if valid and tree is not None and new_geometry:
            local_ids=set().union(*(incident[g] for g in touched))-common
            surrounding=[]
            for fi in local_ids:
                if fi in affected:surrounding.extend(new_geometry[list(new_faces).index(fi)*3:list(new_faces).index(fi)*3+3])
                else:surrounding.extend(pos[tri[fi]])
            local=BVHTree.FromPolygons([Vector(p) for p in surrounding],np.arange(len(surrounding)).reshape(-1,3).tolist(),all_triangles=True)
            original_ids=set().union(*(clusters[g] for g in touched))
            for g in original_ids:
                d=local.find_nearest(Vector(original_points[g]))[3]
                if d>max_error:valid=False;break
                new_reverse[g]=source_vertex_area[g] if d>structural else 0.
            next_area=target_area-sum(face_area[fi] for fi in affected)+sum(new_areas.values())
            next_excess=total_excess-sum(face_excess[fi] for fi in affected)-sum(reverse_excess[g] for g in original_ids)+sum(new_excess.values())+sum(new_reverse.values())
            if next_excess>(source_area+next_area)*.05:valid=False
        if not valid:rejected+=1;continue
        target_area=next_area;total_excess=max(0.,next_excess)
        for fi in affected:face_area[fi]=new_areas.get(fi,0.);face_excess[fi]=new_excess.get(fi,0.)
        for g,v in new_reverse.items():reverse_excess[g]=v
        for fi in affected:
            for g in set(map(int,geo[tri[fi]])):incident[g].discard(fi)
            if fi in common:alive[fi]=False;remaining-=1
            else:tri[fi]=new_faces[fi]
        for wa,values in fields.items():
            pos[wa]=point;geo[wa]=a
            for k,v in values.items():current[k][wa]=v
            hom[wa]=frame(values,point)
        points[a]=point
        for fi in affected-common:
            for g in set(map(int,geo[tri[fi]])):incident[g].add(fi)
        for wb,wa in pairs.items():
            if wb!=wa:q[wa]+=q[wb];qg[wa]+=qg[wb];quv[wa]+=quv[wb];qc[wa]+=qc[wb];support[wa]+=support[wb]
        clusters[a].update(clusters[b]);clusters[b].clear();accepted+=1;updated+=bool(t)
        for g in touched:versions[g]+=1
        update=set()
        for g in touched:
            for other in neighbors(g):update.add(tuple(sorted((g,other))))
        for x,y in sorted(update):offer(x,y);offer(y,x)
    used,remap=np.unique(tri[alive],return_inverse=True)
    output={k:v[used].astype(attrs[k].dtype) for k,v in current.items()};output['POSITION']=pos[used].astype(np.float32)
    return output,remap.reshape(-1,3).astype(np.uint32),dict(method='split-wedge attribute QEM',uv_weight=uv_weight,normal_weight=normal_weight,color_wind_tolerance=data_tolerance,
        triangles=remaining,constraints=constraints,collapses=accepted,vertex_updates=updated,progressive_area_error_fraction=total_excess/max(source_area+target_area,1e-30),rejected_orientation_or_field=rejected,seams='synchronized wedges, separate shader membership, bounded subpixel junction transport')


def transport_frames(source,faces,candidate,triangles,limits,radius,data_tolerance=.01):
    """Sample LOD0 shading normals/tangents on each reduced UV/material side.

    Exact source corners stay exact, including inherited tangent rounding. New
    vertices use the closest legitimate source correspondence; normal, UV and
    material tests disambiguate reused charts and opposing thin skins.
    """
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    p=source['POSITION'].astype(float);ff=np.asarray(faces)
    tree=BVHTree.FromPolygons([Vector(q) for q in p],ff.tolist(),all_triangles=True)
    gradients=np.linalg.pinv(p[ff[:,1:]]-p[ff[:,:1]])
    output={k:v.copy() for k,v in candidate.items()};changes=[]
    known={}
    for i,point in enumerate(p):known.setdefault(tuple(point),[]).append(i)
    for i,point in enumerate(candidate['POSITION'].astype(float)):
        if any(all(np.array_equal(candidate[k][i],source[k][j]) for k in source) for j in known.get(tuple(point),[])):continue
        normal=candidate['NORMAL'][i];hits=tree.find_nearest_range(Vector(point),radius+1e-7)
        options=[]
        for q,unused,fi,distance in hits:
            face=ff[fi]
            if '_LOD_MATERIAL' in source and source['_LOD_MATERIAL'][face[0],0]!=candidate['_LOD_MATERIAL'][i,0]:continue
            edge=(np.asarray(q)-p[face[0]])@gradients[fi];w=np.r_[1-edge.sum(),edge]
            n=w@source['NORMAL'][face];n/=max(np.linalg.norm(n),1e-20)
            angle=float(np.degrees(np.arccos(np.clip(n@normal,-1,1))))
            if angle>3.:continue
            uv=0.
            for k in source:
                if k.startswith('TEXCOORD_'):
                    limit=limits[k][fi] if isinstance(limits[k],np.ndarray) else _limit(limits,k,candidate.get('_LOD_MATERIAL',np.zeros((len(candidate['POSITION']),1)))[i,0])
                    uv=max(uv,float(np.max(np.abs(candidate[k][i]-w@source[k][face])))/limit)
            if uv>1. or any(np.max(np.abs(candidate[k][i]-w@source[k][face]))>data_tolerance for k in source if k.startswith(('COLOR_','_WIND'))):continue
            # Distance dominates ties; UV and frame alternatives disambiguate
            # coincident source sheets without jumping to another chart.
            options.append((distance+radius*(uv*.001+angle*.00001),fi,w,n,angle))
        if not options:continue
        _,fi,w,n,angle=min(options,key=lambda x:x[0]);output['NORMAL'][i]=n;changes.append(angle)
        if 'TANGENT' in source:
            tangent=w@source['TANGENT'][ff[fi]];tangent[:3]-=n*(tangent[:3]@n)
            tangent[:3]/=max(np.linalg.norm(tangent[:3]),1e-20);tangent[3]=1 if tangent[3]>=0 else -1
            output['TANGENT'][i]=tangent
    return output,dict(method='LOD0 UV/material-side shading-normal and tangent sampling',vertices=len(changes),max_correction_degrees=max(changes,default=0.))


def _component(aa,ff,ratio,meters_per_pixel,uv_limit,uv_weight,normal_weight,surface_pixels,texture_size,seam_sliding):
    """One connected chart assembly, independent of sibling construction."""
    from kit.lod_mesh import topology
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    data_tolerance=.02 if seam_sliding else .01
    component_limits=_triangle_limits(aa,ff,meters_per_pixel,texture_size) if texture_size is not None else uv_limit
    best,bf=aa,ff;attempts=[]
    if len(ff)>500:print('LOD SHARED component',len(ff),'target',round(len(ff)*ratio),flush=True)
    if len(ff)>=12 and not ('_LOD_KEEP' in aa and aa['_LOD_KEEP'].all()) and not any(k.startswith(('JOINTS_','WEIGHTS_')) for k in aa):
        tree=BVHTree.FromPolygons([Vector(p) for p in aa['POSITION']],ff.tolist(),all_triangles=True)
        before=topology(aa,ff)[0]
        source_positions=aa['POSITION'].astype(float);source_gradients=np.linalg.pinv(source_positions[ff[:,1:]]-source_positions[ff[:,:1]])
        for rr in [ratio,ratio+(1-ratio)*.4,ratio+(1-ratio)*.75]:
            candidate,cf,row=collapse(aa,ff,rr,uv_weight,normal_weight,meters_per_pixel*surface_pixels*(2/.75),component_limits,meters_per_pixel,seam_sliding,data_tolerance)
            if seam_sliding and row['collapses']:
                candidate,row['normal_transport']=transport_frames(aa,ff,candidate,cf,component_limits,meters_per_pixel*surface_pixels*(2/.75),data_tolerance)
            uv_error=field_error=distance=0.;samples=[];sample_weights=[]
            for w in [np.array([1/3]*3),np.array([.5,.5,0]),np.array([0,.5,.5]),np.array([.5,0,.5])]:
                for f in cf:
                    p=w@candidate['POSITION'][f];q,n,fi,d=tree.find_nearest(Vector(p));distance=max(distance,d)
                    points=candidate['POSITION'][f];samples.append(d);sample_weights.append(float(np.linalg.norm(np.cross(points[1]-points[0],points[2]-points[0])))/4)
                    choices=tree.find_nearest_range(Vector(p),max(1e-6,d+1e-6,meters_per_pixel*surface_pixels*(2/.75)))
                    target_fields={k:w@v[f] for k,v in candidate.items() if k!='POSITION'}
                    best_uv,best_field=_field_error(target_fields,aa,ff,source_positions,source_gradients,choices,component_limits,_frame_limits(points,meters_per_pixel),data_tolerance)
                    uv_error=max(uv_error,min(best_uv,1e6));field_error=max(field_error,min(best_field,1e6))
            target_tree=BVHTree.FromPolygons([Vector(p) for p in candidate['POSITION']],cf.tolist(),all_triangles=True)
            reverse=[target_tree.find_nearest(Vector(p))[3] for p in aa['POSITION']]
            distance=max(distance,max(reverse,default=0.))
            points=aa['POSITION'][ff];areas=np.linalg.norm(np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0]),axis=1)
            weights=np.bincount(ff.ravel(),weights=np.repeat(areas/3,3),minlength=len(aa['POSITION']))
            samples.extend(reverse);sample_weights.extend(weights)
            order=np.argsort(samples);cumulative=np.array(sample_weights)[order].cumsum()
            p95=float(np.array(samples)[order][min(len(order)-1,int(np.searchsorted(cumulative,cumulative[-1]*.95)))])
            after=topology(candidate,cf)[0];reasons=[]
            if distance>meters_per_pixel*surface_pixels*(2/.75) or p95>meters_per_pixel*surface_pixels:reasons.append('surface distance')
            if uv_error>1.:reasons.append('UV/normal/tangent correspondence')
            if field_error>data_tolerance:reasons.append('color/Wind interpolation')
            for k in ('boundary_edges','nonmanifold_edges','degenerate','slivers','winding_disagreements','degenerate_uv'):
                if after[k]>before[k]:reasons.append(k)
            row.update(uv_error=uv_error,uv_error_units='fraction of each material/layer half-mip-texel limit; max 1',field_error=field_error,surface_error_m=distance,surface_area_p95_m=p95,reasons=reasons)
            attempts.append(row)
            if not reasons:best,bf=candidate,cf;break
    if len(ff)>500:print('LOD SHARED result',len(bf),flush=True)
    return best,bf,dict(source_triangles=len(ff),triangles=len(bf),attempts=attempts)


def _cached_component(aa,ff,ratio,meters_per_pixel,uv_limit,uv_weight,normal_weight,surface_pixels,texture_size,seam_sliding):
    """Exact content cache; no surface or appearance gate is skipped."""
    import hashlib,json,marshal,bpy
    from pathlib import Path
    from kit.lod_io import digest
    args=(ratio,meters_per_pixel,uv_limit,uv_weight,normal_weight,surface_pixels,texture_size,seam_sliding)
    h=hashlib.sha256(json.dumps(dict(args=args,runtime=(list(bpy.app.version),np.__version__)),sort_keys=True).encode())
    for fn in (_component,collapse,_limit,_uv_error,_field_error,_frame_limits,_triangle_limits,transport_frames):
        h.update(marshal.dumps((fn.__code__,fn.__defaults__,fn.__kwdefaults__)))
    for name in ('lod_mesh.py','lod_constraints.py'):h.update(digest(Path(__file__).with_name(name)).encode())
    for k,v in sorted({**aa,'indices':ff}.items()):
        h.update(k.encode());h.update(str(v.dtype).encode());h.update(str(v.shape).encode());h.update(np.ascontiguousarray(v).tobytes())
    folder=Path(__file__).resolve().parents[1]/'build/lod-shared-cache/components';folder.mkdir(parents=True,exist_ok=True)
    path=folder/(h.hexdigest()+'.npz');report=path.with_suffix('.json')
    if path.exists() and report.exists():
        meta=json.loads(report.read_text())
        if meta.get('sha256')==digest(path):
            with np.load(path,allow_pickle=False) as data:return {k:data[k].copy() for k in aa},data['indices'].copy(),meta['report']
    out,tri,row=_component(aa,ff,*args)
    np.savez_compressed(path,indices=tri,**out)
    report.write_text(json.dumps(dict(sha256=digest(path),report=row),allow_nan=False)+'\n')
    return out,tri,row


def _reduce(attrs,faces,ratio,meters_per_pixel,uv_limit,uv_weight=10.,normal_weight=.5,surface_pixels=.75,texture_size=None,seam_sliding=True):
    """Component-local measured acceptance; failed charts keep their source mesh."""
    from kit.lod_mesh import components,topology,barycentric
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    data_tolerance=.02 if seam_sliding else .01
    fields={k:[] for k in attrs};triangles=[];offset=0;reports=[]
    for ids in components(attrs,faces):
        vertices,indices=np.unique(faces[ids],return_inverse=True)
        aa={k:a[vertices] for k,a in attrs.items()};ff=indices.reshape(-1,3).astype(np.uint32)
        best,bf,row=_cached_component(aa,ff,ratio,meters_per_pixel,uv_limit,uv_weight,normal_weight,surface_pixels,texture_size,seam_sliding)
        reports.append(row)
        for k in fields:fields[k].append(best[k])
        triangles.append(bf+offset);offset+=len(best['POSITION'])
    result={k:np.concatenate(v) for k,v in fields.items()};tri=np.concatenate(triangles)
    return result,tri,dict(status='simplified',triangles=len(tri),components=reports,uv_weight=uv_weight,normal_weight=normal_weight,field_limits_degrees=dict(normal='clamp(15 / face width pixels, 3, 45)',tangent='clamp(25 / face width pixels, 5, 45)',vertex_normal=3,vertex_tangent=5))


def reduce(attrs,faces,ratio,meters_per_pixel,uv_limit,uv_weight=10.,normal_weight=.5,surface_pixels=.75,texture_size=None,seam_sliding=True):
    """Content-checked geometry cache; appearance and final checks still run."""
    import hashlib,json,bpy
    from pathlib import Path
    from kit.lod_io import digest
    recipe=dict(ratio=ratio,meters_per_pixel=meters_per_pixel,uv_limit=uv_limit,uv_weight=uv_weight,normal_weight=normal_weight,surface_pixels=surface_pixels,texture_size=texture_size,seam_sliding=seam_sliding,
                runtime=dict(blender=list(bpy.app.version),numpy=np.__version__),
                tool=hashlib.sha256(b''.join(__import__('marshal').dumps((f.__code__,f.__defaults__,f.__kwdefaults__)) for f in (collapse,_component,_cached_component,_reduce,_limit,_uv_error,_field_error,_frame_limits,_triangle_limits,transport_frames))).hexdigest(),mesh_tool=digest(Path(__file__).with_name('lod_mesh.py')),constraints_tool=digest(Path(__file__).with_name('lod_constraints.py')))
    h=hashlib.sha256(json.dumps(recipe,sort_keys=True).encode())
    for k,v in sorted({**attrs,'indices':faces}.items()):
        h.update(k.encode());h.update(str(v.dtype).encode());h.update(str(v.shape).encode());h.update(np.ascontiguousarray(v).tobytes())
    folder=Path(__file__).resolve().parents[1]/'build/lod-shared-cache';folder.mkdir(parents=True,exist_ok=True)
    path=folder/(h.hexdigest()+'.npz');report=path.with_suffix('.json')
    if path.exists() and report.exists():
        meta=json.loads(report.read_text())
        if meta.get('sha256')==digest(path):
            with np.load(path,allow_pickle=False) as data:return {k:data[k].copy() for k in attrs},data['indices'].copy(),meta['report']
    out,tri,row=_reduce(attrs,faces,ratio,meters_per_pixel,uv_limit,uv_weight,normal_weight,surface_pixels,texture_size,seam_sliding)
    np.savez_compressed(path,indices=tri,**out)
    report.write_text(json.dumps(dict(sha256=digest(path),report=row),allow_nan=False)+'\n')
    return out,tri,row


def meshes(doc,ratio,meters_per_pixel,feature_pixels=1.5,surface_pixels=.75,seam_sliding=True):
    """Synchronize collapses across material seams within each rigid mesh.

    Material IDs are discrete wedges, not interpolated shader values. Alpha,
    transmission and powered surfaces retain their source vertices. Compatible
    primitive attributes share one geometric collapse, then split by material.
    """
    from kit.lod_mesh import uv_budget,components,topology
    reports=[];source_size=max((max(im['size']) for im in doc.stats()['images']),default=2048)
    for mi,mesh in enumerate(doc.data['meshes']):
        from kit.lod_constraints import contact_points
        contacts,protected_features,contact_edges=contact_points([doc.arrays(p) for p in mesh['primitives']],split=True) if seam_sliding else (set(),set(),0)
        groups={}
        for pi,p in enumerate(mesh['primitives']):
            attrs,faces=doc.arrays(p)
            if set(attrs)&{'_LOD_MATERIAL','_LOD_KEEP'}:raise ValueError('Source uses reserved LOD transport attributes')
            if any(k.startswith(('JOINTS_','WEIGHTS_')) for k in attrs):
                reports.append(dict(mesh=mesh.get('name',mi),primitive=pi,triangles=len(faces),status='retained skin'));continue
            groups.setdefault(tuple(sorted(attrs)),[]).append((pi,p,attrs,faces))
        for entries in groups.values():
            chunks=[];triangles=[];offset=0
            for pi,p,attrs,faces in entries:
                material=p.get('material',0);mat=doc.data.get('materials',[])[material]
                retain=mat.get('alphaMode') in ('MASK','BLEND') or any(v>0 for v in mat.get('emissiveFactor',[0,0,0])) or mat.get('extensions',{}).get('KHR_materials_transmission',{}).get('transmissionFactor',0)>0
                aa={**attrs,'_LOD_MATERIAL':np.full((len(attrs['POSITION']),1),material,np.float32),
                    '_LOD_KEEP':np.full((len(attrs['POSITION']),1),retain,np.float32)}
                pins=np.array([tuple(v) in contacts for v in np.round(attrs['POSITION'].astype(float),6)])
                aa['_LOD_KEEP'][pins]=1
                chunks.append(aa);triangles.append(faces.astype(np.uint32)+offset);offset+=len(attrs['POSITION'])
            aa={k:np.concatenate([c[k] for c in chunks]) for k in chunks[0]};ff=np.concatenate(triangles)
            from kit.lod_shells import preserve,protect_powered
            powered_assemblies=protect_powered(aa,ff,doc.data.get('materials',[]),meters_per_pixel)
            # Remove complete tiny closed components only; source print sheets
            # and powered/glass constructions are protected regardless of size.
            keep=[];removed=[]
            for ids in components(aa,ff):
                vertices=np.unique(ff[ids]);points=aa['POSITION'][vertices]
                diameter=float(np.linalg.norm(np.ptp(points,axis=0))/meters_per_pixel)
                if diameter<feature_pixels and not aa['_LOD_KEEP'][vertices].any() and not any(tuple(p) in protected_features for p in np.round(points.astype(float),6)) and len(ids)<len(ff):
                    vv,ii=np.unique(ff[ids],return_inverse=True)
                    if topology(dict(POSITION=points),ii.reshape(-1,3))[0]['boundary_edges']==0:removed.append(dict(triangles=len(ids),diameter_pixels=diameter));continue
                keep.extend(ids)
            if keep:
                vv,ii=np.unique(ff[sorted(keep)],return_inverse=True);aa={k:v[vv] for k,v in aa.items()};ff=ii.reshape(-1,3).astype(np.uint32)
            budgets={};uv_limit={}
            for _,p,source_attrs,source_faces in entries:
                material=str(p.get('material',0));budget=uv_budget(source_attrs,source_faces,meters_per_pixel,source_size);budgets[material]=budget
                for key,value in budget.items():uv_limit.setdefault(key,{})[material]=value['normalized_tolerance']
            target_ratio=min(.999,ratio*sum(len(f) for _,_,_,f in entries)/len(ff))
            out,tri,row=reduce(aa,ff,target_ratio,meters_per_pixel,uv_limit,surface_pixels=surface_pixels,texture_size=source_size,seam_sliding=seam_sliding)
            out,tri,retained_skins=preserve(aa,ff,out,tri,row,meters_per_pixel)
            for pi,p,attrs,faces in entries:
                material=p.get('material',0);ids=out['_LOD_MATERIAL'][tri,0]
                if np.any(ids!=ids[:,:1]):raise ValueError('Collapse crossed a material boundary')
                selected=tri[ids[:,0]==material]
                if len(entries)>1 and sum(pp.get('material',0)==material for _,pp,_,_ in entries)>1:raise ValueError('Duplicate material primitive in joint reduction')
                if not len(selected):
                    # Avoid silently losing an entire shader/primitive group.
                    selected_attrs,selected_faces=attrs,faces
                else:
                    vv,ii=np.unique(selected,return_inverse=True);selected_attrs={k:v[vv] for k,v in out.items() if k not in ('_LOD_MATERIAL','_LOD_KEEP')};selected_faces=ii.reshape(-1,3).astype(np.uint32)
                doc.replace(p,selected_attrs,selected_faces)
            reports.append(dict(mesh=mesh.get('name',mi),source_contact_edges=contact_edges,source_contact_vertices=len(protected_features),hard_contact_vertices=len(contacts),primitives=[pi for pi,_,_,_ in entries],uv_budgets=budgets,removed_features=removed,retained_source_skins=retained_skins,powered_assemblies=powered_assemblies,component_trials=row))
    return reports
