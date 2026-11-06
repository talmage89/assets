"""Conservative source-skin ordering guard for shared-map reduction.

Internal source sheets can be hidden inside the original outer skin. A pixel-
sized displacement may expose their backs even when distance and normal-field
tests pass. Retain constructions whose sampled visibility ordering changes.
This is not a claim that the source is intersection-free.
"""
import numpy as np


def _visibility_context(source,faces,reduced,triangles):
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    p=source['POSITION'].astype(float);q=reduced['POSITION'].astype(float)
    original=BVHTree.FromPolygons([Vector(v) for v in p],faces.tolist(),all_triangles=True)
    target=BVHTree.FromPolygons([Vector(v) for v in q],triangles.tolist(),all_triangles=True)
    tt=q[triangles];normal=np.cross(tt[:,1]-tt[:,0],tt[:,2]-tt[:,0]);area=np.linalg.norm(normal,axis=1)
    normal/=np.maximum(area[:,None],1e-30);centers=tt.mean(1)
    radius=max(float(np.linalg.norm(np.ptp(p[np.unique(faces)],axis=0))),.001)*2
    return original,target,normal,area,centers,radius


def exposed_backfaces(source,faces,reduced,triangles,meters_per_pixel=0.,face_indices=None,context=None):
    """Measure newly exposed back faces at face centers from 14 directions."""
    from mathutils import Vector
    original,target,normal,area,centers,radius=context or _visibility_context(source,faces,reduced,triangles)
    selected=np.arange(len(triangles)) if face_indices is None else np.asarray(face_indices,int)
    directions=[np.eye(3)[i]*s for i in range(3) for s in (-1,1)]
    directions += [np.array([x,y,z],float)/np.sqrt(3) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
    points=reduced['POSITION'][triangles[selected]].astype(float)
    edges=np.roll(points,-1,axis=1)-points
    for direction in directions:
        cosine=normal[selected]@direction
        longest=np.linalg.norm(edges-np.einsum('nki,i->nk',edges,direction)[:,:,None]*direction,axis=2).max(axis=1)
        width=area[selected]*np.abs(cosine)/np.maximum(longest,1e-20)
        eligible=(cosine<-.1)&(area[selected]*.5>(meters_per_pixel*.5)**2)&(width>meters_per_pixel*3)
        for offset in np.flatnonzero(eligible):
            fi=selected[offset]
            origin=Vector(centers[fi]+direction*radius);ray=Vector(-direction)
            hit=target.ray_cast(origin,ray,radius*2)
            if hit[2]!=fi:continue
            reference=original.ray_cast(origin,ray,radius*2)
            if reference[2] is not None and np.dot(reference[1],direction)>.1:
                return dict(face=int(fi),direction=direction.tolist(),face_area_m2=float(area[fi]*.5),
                            projected_width_pixels=float(width[offset]/meters_per_pixel) if meters_per_pixel else None,
                            source_face=int(reference[2]),
                            source_facing_cosine=float(np.dot(reference[1],direction)),
                            target_facing_cosine=float(normal[fi]@direction))
    return None


def preserve(source,faces,reduced,triangles,report,meters_per_pixel=0.):
    """Restore risky source components after the cached independent reduction."""
    from kit.lod_mesh import components
    chunks=[];output=[];offset=cursor=0;retained=[]
    groups=components(source,faces)
    if len(groups)!=len(report['components']):raise ValueError('Component receipt changed')
    context=_visibility_context(source,faces,reduced,triangles)
    for ids,row in zip(groups,report['components']):
        count=row['triangles'];candidate=triangles[cursor:cursor+count];cursor+=count
        exposure=None
        if len(ids)>count:
            # Judge assembled visibility. A cone's base, for example, covers
            # internal surfaces that would appear exposed in an isolated body.
            exposure=exposed_backfaces(source,faces,reduced,triangles,meters_per_pixel,np.arange(cursor-count,cursor),context)
        use_source=exposure is not None
        attrs=source if use_source else reduced;ff=faces[ids] if use_source else candidate
        vertices,indices=np.unique(ff,return_inverse=True)
        chunks.append({k:v[vertices] for k,v in attrs.items()})
        output.append(indices.reshape(-1,3).astype(np.uint32)+offset);offset+=len(vertices)
        if use_source:retained.append(dict(source_triangles=len(ids),rejected_triangles=count,
            reason='reduction exposes previously hidden back faces',exposure=exposure))
    if cursor!=len(triangles):raise ValueError('Component triangle receipt changed')
    return {k:np.concatenate([c[k] for c in chunks]) for k in source},np.concatenate(output),retained


def protect_powered(attrs,faces,materials,meters_per_pixel):
    """Keep a powered lens and its neighboring occluders as one visual assembly."""
    from kit.lod_mesh import components
    groups=components(attrs,faces);bounds=[];retained=[]
    powered={i for i,m in enumerate(materials) if any(v>0 for v in m.get('emissiveFactor',[0,0,0]))}
    emitting=faces[np.isin(attrs['_LOD_MATERIAL'][faces[:,0],0].astype(int),list(powered))]
    for ids in (components(attrs,emitting) if len(emitting) else []):
        vertices=np.unique(emitting[ids])
        p=attrs['POSITION'][vertices];bounds.append((p.min(0)-meters_per_pixel*.5,p.max(0)+meters_per_pixel*.5))
    for ids in groups:
        vertices=np.unique(faces[ids]);p=attrs['POSITION'][vertices];lo,hi=p.min(0),p.max(0)
        if not any(np.all(lo<=b) and np.all(hi>=a) for a,b in bounds):continue
        triangles=attrs['POSITION'][faces[ids]];low,high=triangles.min(1),triangles.max(1)
        if not any(np.any(np.all(low<=b,axis=1)&np.all(high>=a,axis=1)) for a,b in bounds):continue
        if not attrs['_LOD_KEEP'][vertices].all():retained.append(dict(triangles=len(ids),reason='component bounds overlap powered-source bounds plus half a switch pixel'))
        attrs['_LOD_KEEP'][vertices]=1
    return retained
