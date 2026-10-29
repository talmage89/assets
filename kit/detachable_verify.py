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
    image = image.copy()
    if color: image[:,:,:3] = srgb_to_linear(image[:,:,:3])
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
            # UVs may translate/scale only, including negative chart winding.
            assert np.max(np.abs(db-scale*da)) < 2e-7, 'Nonuniform UV transform'
            ta=np.linalg.solve(da,p[1:]-p[0]);tb=np.linalg.solve(db,p[1:]-p[0])
            ta/=np.maximum(np.linalg.norm(ta,axis=1,keepdims=True),1e-20)
            tb/=np.maximum(np.linalg.norm(tb,axis=1,keepdims=True),1e-20)
            tangent_error=max(tangent_error,float(np.max(np.abs(ta-tb))))
            tangent_angle=max(tangent_angle,float(np.degrees(np.arccos(np.clip(np.sum(ta*tb,axis=1),-1,1))).max()))
    assert all(not v for v in lookup.values())
    # Static origins/hierarchy and full transforms must be preserved.
    assert old.json['nodes'] == new.json['nodes'], 'Detachable origin or nodes changed'
    am,bm=maps(old),maps(new);errors={}
    density_ratios=np.array(uv_scales)*bm['BaseColor'].shape[0]/am['BaseColor'].shape[0]
    assert density_ratios.min() >= .999, 'Delivered texel density decreased'
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
                tangent_direction_max_delta=tangent_error,tangent_direction_max_angle_degrees=tangent_angle,surface_errors=errors)


def audit(path, canonical_folder, asset, layout_path):
    """Check standalone PNGs, padding, bounds and inverse-mapped atlas samples."""
    g=GLB(Path(path));layout=json.loads(Path(layout_path).read_text());size=layout['size']
    assert size in (512,1024)
    images=maps(g);assert len(g.json['images'])==3
    assert all(image.shape[:2]==(size,size) for image in images.values())
    assert not g.json.get('skins') and not g.json.get('animations')
    assert all(s['minFilter']==9729 and s['magFilter']==9729 and
               s['wrapS']==33071 and s['wrapT']==33071 for s in g.json['samplers'])
    atlas_size=layout['source_size'];rectangles=[]
    for row in layout['islands']:
        origin=np.array(row['destination_origin']);shape=np.array(row['shape']);pad=row['padding']
        assert pad>=2
        lo=origin-pad;hi=origin+shape+pad
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
    return dict(size=size,triangles=len(new_uv)//len(BARYCENTRIC),surface_samples=len(new_uv),
                padding_px=layout['padding_px'],source_density_px_m=layout['source_density_px_m'],
                density_px_m=layout['density_px_m'],max_surface_error=errors,
                sampling=layout['sampling'])
