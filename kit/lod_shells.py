"""Conservative source-skin ordering guard for shared-map reduction.

Internal source sheets can be hidden inside the original outer skin. A pixel-
sized displacement may expose their backs even when distance and normal-field
tests pass. Refine or retain constructions whose sampled visibility changes.
This is not a claim that the source is intersection-free.
"""
import numpy as np
from contextlib import contextmanager
from contextvars import ContextVar

_BACKFACE_GUARD=ContextVar('lod_source_backface_guard',default=True)


@contextmanager
def backface_policy(enabled,materials):
    """Scope an auxiliary ordering guard; assembly topology always stays on.

    A double-sided source may legitimately expose a back face without a hole.
    Only a measured image/pose comparison can approve disabling this guard;
    the builder also requires every used source material to be double-sided.
    Context-local state avoids changing the geometric reduction/cache itself.
    """
    if type(enabled) is not bool:raise ValueError('backface_guard must be a boolean')
    if not enabled and (not materials or not all(m.get('doubleSided',False) is True for m in materials)):
        raise ValueError('Disabling backface_guard requires every used source material to be double-sided')
    token=_BACKFACE_GUARD.set(enabled)
    try:yield
    finally:_BACKFACE_GUARD.reset(token)


_REFINEMENT=ContextVar('lod_source_refinement',default=None)


@contextmanager
def refinement_policy(ratio,surface_pixels,texture_size,*,source=None,reflective_surface_pixels=None,enabled=True):
    """Refine failed skins before restoring a whole source construction.

    Optional reflective caps allocate finer geometry to source components with
    median metallic >= .75 and roughness < .35. This is a sampling-priority rule;
    native image checks still decide whether the result is adequate.
    """
    import math
    def positive(value):
        return type(value) in (int,float) and math.isfinite(value) and value>0
    if type(enabled)is not bool or not positive(ratio)or ratio>=1 or not positive(surface_pixels):
        raise ValueError('Invalid source-refinement policy')
    if type(texture_size)is not int or texture_size<1:raise ValueError('Invalid source texture size')
    if reflective_surface_pixels is not None:
        if not enabled or source is None or not positive(reflective_surface_pixels)or reflective_surface_pixels>surface_pixels:
            raise ValueError('Reflective surface cap needs seam sliding, source materials and a positive cap no larger than the base allowance')
    policy=dict(ratio=ratio,surface_pixels=surface_pixels,texture_size=texture_size,
                reflective_surface_pixels=reflective_surface_pixels,source=source,images={}) if enabled else None
    token=_REFINEMENT.set(policy)
    try:yield
    finally:_REFINEMENT.reset(token)


def _reflective_surface(attrs,faces,policy):
    """Read immutable glTF roughness/metallic fields at original corners."""
    if policy['reflective_surface_pixels']is None:return None
    from kit.detachable_verify import sample
    from kit.image_io import read_png
    source=policy['source'];vertices=np.unique(faces);metal=[];rough=[]
    for index in np.unique(attrs['_LOD_MATERIAL'][vertices,0]).astype(int):
        ids=vertices[attrs['_LOD_MATERIAL'][vertices,0]==index]
        pbr=source.data['materials'][index].get('pbrMetallicRoughness',{})
        mf=pbr.get('metallicFactor',1.);rf=pbr.get('roughnessFactor',1.)
        info=pbr.get('metallicRoughnessTexture')
        if info is None:
            metal.extend([mf]*len(ids));rough.extend([rf]*len(ids));continue
        texture=source.data['textures'][info['index']];image_index=texture['source']
        if image_index not in policy['images']:policy['images'][image_index]=read_png(source.image(image_index))
        image=policy['images'][image_index]
        if image.shape[2]<3:image=np.repeat(image[:,:,:1],3,axis=2)
        transform=info.get('extensions',{}).get('KHR_texture_transform',{})
        if set(info.get('extensions',{}))-{'KHR_texture_transform'}:raise ValueError('Unsupported roughness texture extension')
        layer='TEXCOORD_'+str(transform.get('texCoord',info.get('texCoord',0)))
        uv=attrs[layer][ids].astype(float)*transform.get('scale',[1.,1.])
        angle=transform.get('rotation',0.);c,s=np.cos(angle),np.sin(angle)
        uv=uv@np.array([[c,s],[-s,c]])+transform.get('offset',[0.,0.])
        sampler=source.data.get('samplers',[])[texture['sampler']] if 'sampler'in texture else {}
        size=np.array([image.shape[1],image.shape[0]])
        for axis,key in enumerate(('wrapS','wrapT')):
            wrap=sampler.get(key,10497)
            if wrap==33648:uv[:,axis]=1-np.abs(uv[:,axis]%2-1)
            if wrap in (33071,33648):uv[:,axis]=np.clip(uv[:,axis],.5/size[axis],1-.5/size[axis])
            elif wrap!=10497:raise ValueError('Unsupported roughness texture wrap')
        filtering=sampler.get('magFilter',9729)
        if filtering==9728:uv=(np.floor(uv*size)+.5)/size
        elif filtering!=9729:raise ValueError('Unsupported roughness texture filter')
        values=sample(image,uv)
        metal.extend(values[:,2]*mf);rough.extend(values[:,1]*rf)
    metallic=float(np.median(metal));roughness=float(np.median(rough))
    if metallic<.75 or roughness>=.35:return None
    return dict(metallic_median=metallic,roughness_median=roughness,
                surface_pixels=min(policy['surface_pixels'],policy['reflective_surface_pixels']))


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


def visible_patch(original,target,points,face,direction,radius,meters_per_pixel):
    """Measure the newly visible region, rather than its containing triangle.

    A broad triangle can emerge only through a subpixel slit. Its full projected
    altitude is not the width of that slit. Sample half-switch-pixel cells and
    require an exposed patch more than three pixels wide in both directions.
    Final camera/image gates remain independent of these auxiliary rays.
    """
    from mathutils import Vector
    direction=np.asarray(direction,float)
    axis=np.eye(3)[np.argmin(np.abs(direction))];u=np.cross(direction,axis);u/=np.linalg.norm(u);v=np.cross(direction,u)
    anchor=points.mean(0);flat=np.column_stack([(points-anchor)@u,(points-anchor)@v])
    lo=flat.min(0);span=flat.max(0)-lo
    step=max(meters_per_pixel*.5,float(span.max())/256,1e-8)
    shape=np.maximum(1,np.ceil(span/step).astype(int));mask=np.zeros((shape[1],shape[0]),bool)
    for y in range(shape[1]):
        for x in range(shape[0]):
            point=anchor+u*(lo[0]+(x+.5)*step)+v*(lo[1]+(y+.5)*step)
            origin=Vector(point+direction*radius);ray=Vector(-direction)
            hit=target.ray_cast(origin,ray,radius*2)
            if hit[2]!=face:continue
            ref=original.ray_cast(origin,ray,radius*2)
            if ref[2] is not None and np.dot(ref[1],direction)>.1:mask[y,x]=True
    count=int(mask.sum());interior=mask;erosions=0
    while interior.any():
        padded=np.pad(interior,1)
        eroded=np.logical_and.reduce([padded[dy:dy+mask.shape[0],dx:dx+mask.shape[1]] for dy in range(3) for dx in range(3)])
        if not eroded.any():break
        erosions+=1;interior=eroded
    width=(2*erosions+1)*step/meters_per_pixel if count else 0.
    return dict(newly_exposed_area_pixels=count*(step/meters_per_pixel)**2,
                exposed_patch_width_pixels=width,grid_step_pixels=step/meters_per_pixel,
                grid_samples=int(mask.size),exceeds_three_pixels=bool(width>3.))



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
                patch=visible_patch(original,target,points[offset],int(fi),direction,radius,meters_per_pixel) if meters_per_pixel else {}
                if patch and not patch['exceeds_three_pixels']:continue
                return dict(**patch,face=int(fi),direction=direction.tolist(),face_area_m2=float(area[fi]*.5),
                            projected_width_pixels=float(width[offset]/meters_per_pixel) if meters_per_pixel else None,
                            source_face=int(reference[2]),
                            source_facing_cosine=float(np.dot(reference[1],direction)),
                            target_facing_cosine=float(normal[fi]@direction))
    return None


def _edges(attrs,faces,labels):
    """Same one-micrometer incidence convention as lod_mesh.topology."""
    keys=[tuple(v) for v in np.round(attrs['POSITION'].astype(float),6)];result={}
    for fi,face in enumerate(faces):
        for a,b in zip(face,np.roll(face,-1)):
            key=tuple(sorted((keys[a],keys[b])))
            if key[0]==key[1]:continue
            row=result.setdefault(key,[0,set()]);row[0]+=1;row[1].add(int(labels[fi]))
    return result


def preserve(source,faces,reduced,triangles,report,meters_per_pixel=0.):
    """Keep source ordering and contacts, using finer candidates where possible."""
    from kit.lod_mesh import components
    groups=components(source,faces);policy=_REFINEMENT.get()
    if len(groups)!=len(report['components']):raise ValueError('Component receipt changed')
    candidates=[];cursor=0;reflective=[];surface_caps={};trials=[];retained={};refined={}
    for index,(ids,row)in enumerate(zip(groups,report['components'])):
        count=row['triangles'];ff=triangles[cursor:cursor+count];cursor+=count
        vertices,remap=np.unique(ff,return_inverse=True)
        candidates.append(({k:v[vertices]for k,v in reduced.items()},remap.reshape(-1,3).astype(np.uint32)))
    if cursor!=len(triangles):raise ValueError('Component triangle receipt changed')
    def source_component(index):
        vertices,remap=np.unique(faces[groups[index]],return_inverse=True)
        return {k:v[vertices]for k,v in source.items()},remap.reshape(-1,3).astype(np.uint32)
    def reduce_component(index,ratio,pixels):
        from kit.lod_shared import _cached_component
        aa,ff=source_component(index)
        return _cached_component(aa,ff,ratio,meters_per_pixel,None,report.get('uv_weight',10.),
                                 report.get('normal_weight',.5),pixels,policy['texture_size'],True)
    def assemble():
        chunks=[];output=[];labels=[];offset=0
        for index,ids in enumerate(groups):
            if index in retained:aa,ff=source,faces[ids]
            else:aa,ff=refined.get(index,candidates[index])
            vertices,indices=np.unique(ff,return_inverse=True)
            chunks.append({k:v[vertices]for k,v in aa.items()})
            output.append(indices.reshape(-1,3).astype(np.uint32)+offset);offset+=len(vertices)
            labels.extend([index]*len(ff))
        return {k:np.concatenate([c[k]for c in chunks])for k in source},np.concatenate(output),labels
    if policy and policy['reflective_surface_pixels']is not None:
        for index,ids in enumerate(groups):
            aa,ff=source_component(index)
            if len(ids)<12 or aa['_LOD_KEEP'].all():continue
            response=_reflective_surface(aa,ff,policy)
            if response is None:continue
            out,tf,receipt=reduce_component(index,policy['ratio'],response['surface_pixels'])
            reflective.append(dict(component=index,source_triangles=len(ids),initial_triangles=len(candidates[index][1]),
                                   triangles=len(tf),**response,component_trial=receipt))
            surface_caps[index]=response['surface_pixels'];candidates[index]=(out,tf)
    assembled,af,labels=assemble();context=_visibility_context(source,faces,assembled,af)
    cursor=0
    for index,ids in enumerate(groups):
        count=len(candidates[index][1]);exposure=None
        if _BACKFACE_GUARD.get()and len(ids)>count:
            exposure=exposed_backfaces(source,faces,assembled,af,meters_per_pixel,np.arange(cursor,cursor+count),context)
        cursor+=count
        if exposure is not None:retained[index]=dict(component=index,source_triangles=len(ids),rejected_triangles=count,
            reason='reduction exposes previously hidden back faces',exposure=exposure)
    if policy:
        for index in list(retained):
            ids=groups[index];initial=len(candidates[index][1])
            if len(ids)-initial<64:continue
            for fraction in (.15,.30,.45,.60,.75,.9):
                ratio=policy['ratio']+(1-policy['ratio'])*fraction
                out,tf,receipt=reduce_component(index,ratio,surface_caps.get(index,policy['surface_pixels']))
                if len(tf)>=len(ids):continue
                rejected=retained.pop(index);refined[index]=(out,tf)
                candidate,cf,labels=assemble();exposure=exposed_backfaces(source,faces,candidate,cf,meters_per_pixel)
                trials.append(dict(component=index,source_triangles=len(ids),initial_triangles=initial,ratio=ratio,
                                   triangles=len(tf),exposure=exposure,component_trial=receipt))
                if exposure is None:break
                refined.pop(index);retained[index]=rejected
    source_labels=np.empty(len(faces),int)
    for index,ids in enumerate(groups):source_labels[ids]=index
    original=_edges(source,faces,source_labels)
    original_bad={kind:{edge for edge,(count,_)in original.items()if(count==1 if kind=='boundary'else count>2)}for kind in('boundary','nonmanifold')}
    while True:
        attrs,ff,labels=assemble();current=_edges(attrs,ff,labels);violations={};implicated=set();samples=[]
        for kind in('boundary','nonmanifold'):
            bad={edge for edge,(count,_)in current.items()if(count==1 if kind=='boundary'else count>2)}
            if len(bad)<=len(original_bad[kind]):continue
            violations[kind]=dict(source=len(original_bad[kind]),candidate=len(bad))
            for edge in bad-original_bad[kind]:
                implicated.update(current[edge][1]);implicated.update(original.get(edge,[0,set()])[1])
                if len(samples)<8:samples.append([list(map(float,p))for p in edge])
        if not violations:
            if policy:report['source_surface_refinement']=dict(initial_triangles=len(triangles),triangles=len(ff),
                reflective_surfaces=reflective,skin_density_trials=trials)
            return attrs,ff,list(retained.values())
        implicated.difference_update(retained)
        if not implicated:raise ValueError('Assembled topology cannot be repaired from its source components')
        for index in sorted(implicated):
            retained[index]=dict(component=index,source_triangles=len(groups[index]),rejected_triangles=len(refined.get(index,candidates[index])[1]),
                reason='independent reductions create new assembled edge contacts',edge_counts=violations,edge_samples_m=samples)


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
