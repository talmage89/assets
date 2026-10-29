"""Independent raw-GLB texture sampling and detachable delivery checks."""
import io
import json
import copy
from pathlib import Path

import numpy as np
from PIL import Image

from kit.gltf import GLB
from kit.image_io import srgb_to_linear


def maps(g):
    """Follow material texture indices, not image order or image names."""
    material = g.json['materials'][0]
    pbr = material['pbrMetallicRoughness']
    indices = dict(BaseColor=pbr['baseColorTexture']['index'],
                   Normal=material['normalTexture']['index'],
                   ORM=pbr['metallicRoughnessTexture']['index'])
    assert material['occlusionTexture']['index'] == indices['ORM']
    return {channel:np.array(Image.open(io.BytesIO(g.image(
        g.json['textures'][index]['source'])))).astype(float)/255
        for channel,index in indices.items()}


def sample(image, coordinates, *, color=False):
    """glTF top-left UV, repeat wrapping, texel-center bilinear sampling."""
    if color:
        image = image.copy()
        image[:,:,:3] = srgb_to_linear(image[:,:,:3])
    height,width,_ = image.shape
    xy = np.asarray(coordinates)*[width,height]-.5
    lo = np.floor(xy).astype(int); fraction = xy-lo
    x,y = lo.T; u,v = fraction.T
    return ((image[y%height,x%width]*(1-u[:,None]) +
             image[y%height,(x+1)%width]*u[:,None])*(1-v[:,None]) +
            (image[(y+1)%height,x%width]*(1-u[:,None]) +
             image[(y+1)%height,(x+1)%width]*u[:,None])*v[:,None])


BARYCENTRIC = np.array([(1,0,0),(0,1,0),(0,0,1),(.5,.5,0),(.5,0,.5),(0,.5,.5),
                        (1/3,1/3,1/3),(.6,.1,.3),(.05,.9,.05),(.05,.05,.9)])


def _triangles(g):
    rows = []
    for mesh in g.json['meshes']:
        for primitive in mesh['primitives']:
            attributes = {k:g.accessor(v) for k,v in primitive['attributes'].items()}
            for indices in g.accessor(primitive['indices']).reshape(-1,3):
                rows.append({k:v[indices] for k,v in attributes.items()})
    return rows


def compare(before, after, *, tolerance=.25/255):
    """Match actual oriented corner geometry; sample the same surface points.

    Normals are compared in their tangent frame; the independent triangle
    Jacobian proves unchanged tangent orientation/handedness. No layout report
    is used as evidence for the old/new surface correspondence.
    """
    old,new = GLB(Path(before)),GLB(Path(after))
    def material_settings(g):
        result=[]
        for original in g.json['materials']:
            material=copy.deepcopy(original);material.pop('name',None)
            pbr=material['pbrMetallicRoughness']
            channel_sources={g.json['textures'][index]['source']:channel for channel,index in
                [('BaseColor',pbr['baseColorTexture']['index']),
                 ('Normal',material['normalTexture']['index']),
                 ('ORM',pbr['metallicRoughnessTexture']['index'])]}
            def normalize(node):
                if isinstance(node,dict):
                    for key,value in node.items():
                        if key.endswith('Texture') and isinstance(value,dict) and 'index' in value:
                            source=g.json['textures'][value['index']]['source']
                            value['index']=channel_sources[source]
                        else:normalize(value)
                elif isinstance(node,list):
                    for value in node:normalize(value)
            normalize(material);result.append(material)
        return result
    assert material_settings(old)==material_settings(new), 'Material factors or extensions changed'
    am,bm=maps(old),maps(new)
    expected_scale=am['BaseColor'].shape[0]/bm['BaseColor'].shape[0]
    a,b = _triangles(old),_triangles(new)
    assert len(a) == len(b)
    def key(row):
        p = np.concatenate([row['POSITION'],row['NORMAL']],axis=1)
        corners = [tuple(float(x) for x in v) for v in p]
        start = min(range(3),key=corners.__getitem__)
        return tuple(corners[start:]+corners[:start]),start
    lookup = {}
    for row in a:
        k,start = key(row);lookup.setdefault(k,[]).append((row,start))
    old_uv = [];new_uv = [];tangent_error = 0.;tangent_angle=0.;uv_scales=[]
    source_texel_areas=[];uv_error_px=0.
    for row in b:
        k,start = key(row);assert k in lookup and lookup[k], 'Geometry or normals changed'
        previous,old_start = lookup[k].pop()
        p = np.roll(previous['POSITION'],-old_start,axis=0)
        auv = np.roll(previous['TEXCOORD_0'],-old_start,axis=0).astype(float)
        buv = np.roll(row['TEXCOORD_0'],-start,axis=0).astype(float)
        old_uv.extend(BARYCENTRIC@auv);new_uv.extend(BARYCENTRIC@buv)
        da,db = auv[1:]-auv[0],buv[1:]-buv[0]
        if abs(np.linalg.det(da)) > 1e-14:
            scale = float(np.sum(da*db)/np.sum(da*da))
            assert scale > 0, 'Mirrored or rotated UVs'
            uv_scales.append(float(np.sqrt(abs(np.linalg.det(db)/np.linalg.det(da)))))
            source_texel_areas.append(abs(np.linalg.det(da))*am['BaseColor'].shape[0]**2*.5)
            # UVs may translate/scale only, including negative chart winding.
            # Both old and new glTF V coordinates are rounded after Blender's
            # 1-v conversion. Bound that storage error in delivered pixels,
            # rather than fitting a scale to already rounded skinny edges.
            error=float(np.max(np.abs(db-expected_scale*da))*bm['BaseColor'].shape[0])
            uv_error_px=max(uv_error_px,error)
            assert error < .001, 'Nonuniform UV transform'
            ta=np.linalg.solve(da,p[1:]-p[0]);tb=np.linalg.solve(db,p[1:]-p[0])
            ta/=np.maximum(np.linalg.norm(ta,axis=1,keepdims=True),1e-20)
            tb/=np.maximum(np.linalg.norm(tb,axis=1,keepdims=True),1e-20)
            tangent_error=max(tangent_error,float(np.max(np.abs(ta-tb))))
            tangent_angle=max(tangent_angle,float(np.degrees(np.arccos(np.clip(np.sum(ta*tb,axis=1),-1,1))).max()))
    assert all(not v for v in lookup.values())
    # Static origins/hierarchy and full transforms must be preserved.
    assert old.json['nodes'] == new.json['nodes'], 'Detachable origin or nodes changed'
    errors={}
    density_ratios=np.array(uv_scales)*bm['BaseColor'].shape[0]/am['BaseColor'].shape[0]
    # Subtexel slivers amplify float V-flip errors when divided by their tiny
    # area. They still obey the same absolute pixel transform bound above and
    # every surface/map sample below; report their ratios without mistaking
    # that ill-conditioned percentage for a resolution change.
    resolved=density_ratios[np.array(source_texel_areas)>=1]
    if len(resolved):assert resolved.min() >= .999, 'Delivered texel density decreased'
    for channel in am:
        values=sample(am[channel],old_uv,color=channel=='BaseColor')
        target=sample(bm[channel],new_uv,color=channel=='BaseColor')
        assert values.shape==target.shape
        error=np.abs(values-target)
        errors[channel]=dict(max=float(error.max()),rmse=float(np.sqrt((error**2).mean())))
        assert error.max() <= tolerance,(channel,errors[channel])
    assert tangent_angle < .5, tangent_angle
    return dict(triangles=len(a),samples=len(old_uv),geometry_and_origin_identical=True,
                measured_density_ratio_min=float(density_ratios.min()),
                measured_density_ratio_max=float(density_ratios.max()),
                resolved_density_ratio_min=float(resolved.min()) if len(resolved) else None,
                maximum_uniform_transform_error_px=uv_error_px,
                tangent_direction_max_delta=tangent_error,tangent_direction_max_angle_degrees=tangent_angle,surface_errors=errors)


def audit(path, canonical_folder, asset, layout_path, *, gun=None):
    """Check standalone PNGs, padding, bounds and inverse-mapped atlas samples."""
    g=GLB(Path(path));layout=json.loads(Path(layout_path).read_text());size=layout['size']
    assert size in (512,1024)
    images=maps(g);assert len(g.json['images'])==3
    assert all(image.shape[:2]==(size,size) for image in images.values())
    assert not g.json.get('skins') and not g.json.get('animations')
    if gun is not None:
        assert samplers(g)==samplers(GLB(Path(gun))), 'Sampler differs from main gun'
    else:
        assert all(s.get('minFilter')==9987 and s.get('magFilter')==9729
                   for s in samplers(g).values())
    atlas_size=layout['source_size'];rectangles=[]
    for row in layout['islands']:
        origin=np.array(row['destination_origin']);shape=np.array(row['shape']);pad=row['padding']
        assert pad>=8
        lo=origin-pad;hi=lo+np.array(row.get('guard_shape',shape+2*pad))
        assert np.all(hi>=origin+shape+pad)
        grid=layout.get('mip_grid_px',1)
        assert np.all(lo%grid==0) and np.all(hi%grid==0)
        assert np.all(lo>=0) and np.all(hi<=size)
        rectangles.append((lo,hi))
    lows=np.array([a for a,b in rectangles]);highs=np.array([b for a,b in rectangles])
    for i in range(len(rectangles)):
        assert not np.any(np.all(highs[i]>lows[:i],axis=1)&
                          np.all(highs[:i]>lows[i],axis=1)), 'Island guards overlap'
    origins=np.array([row['destination_origin'] for row in layout['islands']])
    ends=origins+np.array([row['shape'] for row in layout['islands']])
    source_uv=[];new_uv=[]
    for tri in _triangles(g):
        points=tri['TEXCOORD_0'].astype(float).copy();points[:,1]=1-points[:,1]
        assert np.all(points>=0) and np.all(points<=1)
        pixels=points*size
        candidates=np.flatnonzero(np.all(pixels.min(axis=0)>=origins-1e-3,axis=1)&
                                  np.all(pixels.max(axis=0)<=ends+1e-3,axis=1))
        assert len(candidates)==1, 'Triangle escaped its protected chart'
        row=layout['islands'][int(candidates[0])];offset=np.array(row['source_origin'])-row['destination_origin']
        a=(BARYCENTRIC@pixels+offset)/atlas_size;b=BARYCENTRIC@points
        a[:,1]=1-a[:,1];b[:,1]=1-b[:,1]
        source_uv.extend(a);new_uv.extend(b)
    errors={}
    for channel,image in images.items():
        source=np.array(Image.open(Path(canonical_folder)/f'T_{asset}_{channel}.png')).astype(float)/255
        delta=np.abs(sample(source,source_uv,color=channel=='BaseColor')-
                     sample(image,new_uv,color=channel=='BaseColor'))
        errors[channel]=float(delta.max());assert delta.max()<.25/255,(channel,delta.max())
    footprint = _footprint([t['TEXCOORD_0'].astype(float)*size for t in _triangles(g)],(size,size))
    vectors = images['Normal'][~footprint,:3]*2-1
    unit_error = float(np.max(np.abs(np.linalg.norm(vectors,axis=1)-1)))
    assert unit_error < .007, ('Generated normal is not unit length',unit_error)
    return dict(size=size,triangles=len(new_uv)//len(BARYCENTRIC),surface_samples=len(new_uv),
                padding_px=layout['padding_px'],source_density_px_m=layout['source_density_px_m'],
                density_px_m=layout['density_px_m'],max_surface_error=errors,
                sampling=layout['sampling'],filled_texels=int((~footprint).sum()),
                generated_normal_max_unit_error=unit_error)


def samplers(g):
    """Resolve each material channel's actual sampler, including implicit defaults."""
    material = g.json['materials'][0]
    pbr = material['pbrMetallicRoughness']
    indices = dict(BaseColor=pbr['baseColorTexture']['index'],
                   Normal=material['normalTexture']['index'],
                   ORM=pbr['metallicRoughnessTexture']['index'])
    return {channel:copy.deepcopy(g.json.get('samplers',[])[texture['sampler']])
            if 'sampler' in texture else {} for channel,index in indices.items()
            for texture in [g.json['textures'][index]]}


def mip_chain(image, *, color=False):
    """Box-filtered hardware-style mip chain; sRGB RGB averages in linear light.

    Alpha and data channels are linear. Normal mip texels remain the encoded
    vector averages used by ordinary GPU mip generation; the shader normalizes
    after lookup. This deliberately does not sharpen or renormalize each mip.
    """
    image = image.astype(np.float64).copy()
    if color: image[:,:,:3] = srgb_to_linear(image[:,:,:3])
    chain = [image]
    while min(image.shape[:2]) > 1 and all(n%2 == 0 for n in image.shape[:2]):
        h,w,c = image.shape
        image = image.reshape(h//2,2,w//2,2,c).mean(axis=(1,3))
        chain.append(image)
    return chain


def _footprint(triangles, shape):
    """Rasterize raw exported triangles, with their conservative bilinear support.

    Independent of Blender mesh loops and the extraction report's ownership.
    The triangle/square separating-axis test retains even subpixel slivers.
    """
    w,h = map(int,shape); mask = np.zeros((h,w),bool)
    cross = lambda a,b:a[...,0]*b[...,1]-a[...,1]*b[...,0]
    for points in triangles:
        lo = np.maximum(np.floor(points.min(axis=0)-.5).astype(int),0)
        hi = np.minimum(np.ceil(points.max(axis=0)+.5).astype(int),(w,h))
        if np.any(hi<=lo): continue
        yy,xx = np.mgrid[lo[1]:hi[1],lo[0]:hi[0]]
        centers = np.stack((xx+.5,yy+.5),axis=-1)
        a,b,c = points; determinant = cross(b-a,c-a)
        if abs(determinant)<1e-15: continue
        hit = np.ones(xx.shape,bool)
        for start,end in ((a,b),(b,c),(c,a)):
            edge = end-start
            hit &= cross(edge,centers-start)*np.sign(determinant) >= -.5*(abs(edge[0])+abs(edge[1]))-1e-7
        mask[lo[1]:hi[1],lo[0]:hi[0]] |= hit
    expanded = np.pad(mask,1)
    return np.logical_or.reduce([expanded[dy:dy+h,dx:dx+w]
                                for dy in range(3) for dx in range(3)])


def _isolated_patch(pixels, mask, origin, level, *, normal=False):
    """One island alone, extended without a gutter limit on an aligned canvas.

    The canvas contains every box/bilinear tap at the requested maximum LOD,
    plus two whole mip blocks on all sides. Its origin is on the *actual*
    atlas/standalone mip grid, so intra-island phase differences are not bleed.
    A separate owner wavefront implements the deterministic Chebyshev fill.
    """
    block = 2**level; shape = np.array(mask.shape[::-1])
    low = (np.asarray(origin)//block-2)*block
    high = ((np.asarray(origin)+shape+block-1)//block+2)*block
    w,h = map(int,high-low); x,y = map(int,np.asarray(origin)-low)
    owners = np.full((h,w),-1,np.int32)
    indices = np.arange(mask.size,dtype=np.int32).reshape(mask.shape)
    owners[y:y+mask.shape[0],x:x+mask.shape[1]][mask] = indices[mask]
    seed = owners>=0
    while np.any(owners<0):
        previous = owners.copy()
        # Images here are top-down; extraction operates bottom-up. Reverse
        # the vertical tie order to describe the same island extension.
        for dy,dx in ((1,0),(0,-1),(0,1),(-1,0),(1,-1),(1,1),(-1,-1),(-1,1)):
            target = owners[max(0,dy):h+min(0,dy),max(0,dx):w+min(0,dx)]
            source = previous[max(0,-dy):h-max(0,dy),max(0,-dx):w-max(0,dx)]
            hit = (target<0)&(source>=0)
            target[hit] = source[hit]
        assert not np.array_equal(previous,owners), 'Empty isolated-island seed'
    result = pixels.reshape(-1,pixels.shape[-1])[owners].copy()
    if normal:
        vectors = result[~seed,:3]*2-1
        lengths = np.linalg.norm(vectors,axis=1,keepdims=True)
        vectors = np.divide(vectors,lengths,out=np.zeros_like(vectors),where=lengths>1e-12)
        vectors[lengths[:,0]<=1e-12] = (0,0,1)
        # Reference includes the same unavoidable 8-bit padding quantization.
        result[~seed,:3] = np.floor((vectors*.5+.5)*255+.5)/255
    return result,low


def mip_bleed(path, canonical_folder, asset, layout_path, *, gun=None,
              tolerance=1/255, minimum_level=3, enforce=True):
    """Pointwise mip bleed versus an unlimited isolated-island reference.

    Compare every ten-point triangle sample and channel at every integer LOD.
    Test through the level where the smallest island is two texels, and at
    least through mip 3, even for subpixel islands. This is stronger than the
    item's smallest-island cutoff. Error is max absolute channel difference in
    linear RGBA / encoded tangent normal / linear ORM. The new error may exceed
    the canonical error by at most one 8-bit step (1/255), *at the same surface
    point*, never just an aggregate maximum. Different integer packing phases
    get independently aligned ideal reference chains.
    """
    g = GLB(Path(path)); layout = json.loads(Path(layout_path).read_text())
    size = layout['size']; source_size = layout['source_size']
    if gun is not None:
        assert samplers(g)==samplers(GLB(Path(gun))), 'Sampler differs from main gun'
    actual = maps(g)
    source = {c:np.asarray(Image.open(Path(canonical_folder)/f'T_{asset}_{c}.png')).astype(float)/255
              for c in actual}
    chains = {c:mip_chain(a,color=c=='BaseColor') for c,a in actual.items()}
    old_chains = {c:mip_chain(a,color=c=='BaseColor') for c,a in source.items()}
    rows = layout['islands']
    shapes = np.array([r['shape'] for r in rows],int)
    origins = np.array([[r['destination_origin'][0],size-r['destination_origin'][1]-r['shape'][1]] for r in rows],int)
    old_origins = np.array([[r['source_origin'][0],source_size-r['source_origin'][1]-r['shape'][1]] for r in rows],int)
    ends = origins+shapes; groups = [[] for _ in rows]
    for tri in _triangles(g):
        pixels = tri['TEXCOORD_0'].astype(float)*size
        candidates = np.flatnonzero(np.all(pixels.min(axis=0)>=origins-1e-3,axis=1)&
                                    np.all(pixels.max(axis=0)<=ends+1e-3,axis=1))
        assert len(candidates)==1, 'Triangle escaped protected chart'
        groups[int(candidates[0])].append(pixels)
    cutoffs = []
    for triangles in groups:
        extent = np.ptp(np.asarray(triangles).reshape(-1,2),axis=0)
        cutoffs.append(max(0,int(np.floor(np.log2(max(float(extent.min()),1e-12)/2)))))
    limit = max(minimum_level,min(cutoffs))
    levels = {}; total_samples = 0
    for index,(triangles,shape,origin,old_origin) in enumerate(zip(groups,shapes,origins,old_origins)):
        assert triangles, 'Unused island rectangle'
        relative = np.asarray(triangles)-origin
        mask = _footprint(relative,shape); assert mask.any()
        points = (BARYCENTRIC[None,:,:]@np.asarray(triangles)).reshape(-1,2)
        previous_points = points-origin+old_origin
        total_samples += len(points)*(limit+1)
        for channel,atlas in source.items():
            h,w = mask.shape; ox,oy = old_origin
            pixels = atlas[np.arange(oy,oy+h)%source_size][:,np.arange(ox,ox+w)%source_size]
            # Both references use exactly the same island's original pixels.
            for old,grid_origin,locations,chain in ((True,old_origin,previous_points,old_chains[channel]),
                                                   (False,origin,points,chains[channel])):
                isolated,low = _isolated_patch(pixels,mask,grid_origin,limit,normal=channel=='Normal')
                ideal = mip_chain(isolated,color=channel=='BaseColor')
                errors = []
                for level in range(limit+1):
                    reference = sample(ideal[level],(locations-low)/np.array(isolated.shape[1::-1]))
                    observed = sample(chain[level],locations/(source_size if old else size))
                    errors.append(np.max(np.abs(observed-reference),axis=1))
                if old: baseline_errors = errors
                else:
                    for level,(before,after) in enumerate(zip(baseline_errors,errors)):
                        row = levels.setdefault(str(level),dict(samples=0,atlas=0.,standalone=0.,excess=-1.,channels={}))
                        metrics = row['channels'].setdefault(channel,dict(atlas=0.,standalone=0.,excess=-1.))
                        metrics['atlas'] = max(metrics['atlas'],float(before.max()))
                        metrics['standalone'] = max(metrics['standalone'],float(after.max()))
                        metrics['excess'] = max(metrics['excess'],float((after-before).max()))
                        row['atlas'] = max(row['atlas'],metrics['atlas'])
                        row['standalone'] = max(row['standalone'],metrics['standalone'])
                        row['excess'] = max(row['excess'],metrics['excess'])
                        if channel=='BaseColor': row['samples'] += len(points)
                        if enforce:
                            assert np.all(after<=before+tolerance),(Path(path).name,index,channel,level,
                                'New mip bleed exceeds atlas',float((after-before).max()),tolerance)
    return dict(tolerance=tolerance,metric='pointwise max absolute linear RGBA / encoded normal / ORM',
                sampler=samplers(g),item_smallest_island_cutoff=min(cutoffs),
                tested_minimum_level=minimum_level,maximum_level=max(map(int,levels)),
                samples_across_levels=total_samples,levels=levels,
                passed=all(r['excess']<=tolerance for r in levels.values()))
