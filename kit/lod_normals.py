"""Independent delivered-accessor normal-field comparison against LOD0.

Vertex correspondences use nearest original surfaces and UVs; coincident chart
ties retain their legitimate split-normal alternatives. This measures geometry
normals, not the appearance of the tangent normal maps (checked by the renders).
"""
import argparse
import copy
import json
import math
import sys
from pathlib import Path

import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document,digest
from kit.lod_mesh import barycentric,topology,uv_budget


def rig_data(doc):
    skins=copy.deepcopy(doc.data.get('skins',[]));clips=copy.deepcopy(doc.data.get('animations',[]))
    for skin in skins:
        if 'inverseBindMatrices' in skin:skin['inverseBindMatrices']=doc.accessor(skin['inverseBindMatrices']).tolist()
    for clip in clips:
        for sampler in clip['samplers']:
            for channel in ('input','output'):sampler[channel]=doc.accessor(sampler[channel]).tolist()
    return skins,clips


def signatures(attrs,uv_keys):
    data=np.ascontiguousarray(np.column_stack([attrs[k] for k in ['POSITION','NORMAL',*uv_keys]]),dtype=np.float32)
    return data.view(np.dtype((np.void,data.shape[1]*data.dtype.itemsize))).ravel()


def tangent_errors(attrs,source):
    """Gate new basis errors; report byte-exact inherited source defects."""
    if 'TANGENT' not in attrs:return 0.,0.,0
    keys=['POSITION','NORMAL','TANGENT',*[k for k in attrs if k.startswith('TEXCOORD_')]]
    def records(values):
        a=np.ascontiguousarray(np.column_stack([values[k] for k in keys]),dtype=np.float32)
        return a.view(np.dtype((np.void,a.shape[1]*a.dtype.itemsize))).ravel()
    tangent=attrs['TANGENT'][:,:3]
    dot=np.abs(np.einsum('ij,ij->i',tangent,attrs['NORMAL']))
    length=np.abs(np.linalg.norm(tangent,axis=1)-1)
    invalid=(dot>1e-3)|(length>2e-4)
    inherited=invalid & np.isin(records(attrs),np.unique(records(source)))
    return float(dot[~inherited].max(initial=0)),float(length[~inherited].max(initial=0)),int(inherited.sum())


def foliage_normals(doc,base,row):
    errors=[];matched=0
    for mi,pi,p in doc.primitives():
        a,f=doc.arrays(p);source=base.arrays(base.data['meshes'][mi]['primitives'][pi])[0]
        if any(not np.isfinite(v).all() for v in a.values()):errors.append('nonfinite foliage attributes')
        if '_WIND' not in a:errors.append('lost foliage Wind')
        if np.max(np.abs(np.linalg.norm(a['NORMAL'],axis=1)-1))>2e-4:errors.append('nonunit foliage normals')
        mat=doc.data['materials'][p.get('material',0)]
        if mat.get('alphaMode') in ('MASK','BLEND'):
            keys=['NORMAL','_WIND',*[k for k in a if k.startswith('TEXCOORD_')]]
            def sig(values):
                v=np.ascontiguousarray(np.column_stack([values[k] for k in keys]),dtype=np.float32)
                return v.view(np.dtype((np.void,v.shape[1]*4))).ravel()
            same=np.isin(sig(a),np.unique(sig(source)))
            matched+=int(same.sum())
            if not same.all():errors.append('leaf UV/normal/Wind corner data changed')
    return dict(level=row['level'],scope='enlarged cards: exact UV, bent normals and Wind; geometry/coverage checked in renders',matched_leaf_vertices=matched),errors


def atlas_normals(doc,base,row):
    """Audit transported near normals and new UVs; proxy cage normals are new.

    Proxy appearance is carried by its tangent-normal bake, whose normalization
    is measured independently. The exported render gates judge that shading.
    """
    from kit.detachable_verify import _image
    angles=[];errors=[];degenerate_uv=0;unit_error=0.;max_distance=0.
    for ni,node in enumerate(doc.data['nodes']):
        if 'mesh' not in node:continue
        source_ids=node.get('extras',{}).get('lod_sources',[ni]);points=[];normals=[];triangles=[];offset=0
        for si in source_ids:
            n=base.data['nodes'][si]
            if 'mesh' not in n:continue
            matrix=np.eye(4) if 'skin' in n else base.world(si)
            for p in base.data['meshes'][n['mesh']]['primitives']:
                a,f=base.arrays(p);v=a['POSITION']@matrix[:3,:3].T+matrix[:3,3]
                nn=a['NORMAL']@np.linalg.inv(matrix[:3,:3]);nn/=np.maximum(np.linalg.norm(nn,axis=1,keepdims=True),1e-20)
                points.extend(v);normals.extend(nn);triangles.extend(f.astype(np.uint32)+offset);offset+=len(v)
        points=np.array(points);normals=np.array(normals);triangles=np.array(triangles)
        tree=BVHTree.FromPolygons([Vector(v) for v in points],triangles.tolist(),all_triangles=True)
        matrix=np.eye(4) if 'skin' in node else doc.world(ni)
        for p in doc.data['meshes'][node['mesh']]['primitives']:
            a,f=doc.arrays(p);r=topology(a,f)[0];degenerate_uv+=r['degenerate_uv']
            if r['degenerate_uv']:errors.append('new atlas contains zero-area UV triangles')
            t=a['POSITION'][f];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
            dot=np.einsum('fvi,fi->fv',a['NORMAL'][f],cross)
            if np.any(dot < -1e-10):errors.append('rebaked tangent frame points through its own face')
            for k,v in a.items():
                if k.startswith('WEIGHTS_') and (np.any(v<0) or np.max(np.abs(v.sum(axis=1)-1))>1e-5):errors.append('invalid interpolated skin weights')
            v=a['POSITION']@matrix[:3,:3].T+matrix[:3,3]
            nn=a['NORMAL']@np.linalg.inv(matrix[:3,:3]);nn/=np.maximum(np.linalg.norm(nn,axis=1,keepdims=True),1e-20)
            # Source correspondence does not use new atlas UVs as if they were
            # original charts. Nearby original normal alternatives disambiguate
            # thin walls; search only at the measured nearest surface distance.
            for point,normal in zip(v,nn):
                q,n,fi,dist=tree.find_nearest(Vector(point));max_distance=max(max_distance,dist)
                pairs=[]
                for qq,unused,ii,dd in tree.find_nearest_range(Vector(point),max(dist+1e-6,1e-6)):
                    w=barycentric(np.array(qq),points[triangles[ii]])
                    source_normal=w@normals[triangles[ii]];source_normal/=max(np.linalg.norm(source_normal),1e-20)
                    pairs.append(float(np.degrees(np.arccos(np.clip(normal@source_normal,-1,1)))))
                angles.append(min(pairs))
    for mat in doc.data.get('materials',[]):
        if 'normalTexture' not in mat:continue
        ti=mat['normalTexture']['index'];image=_image(doc.image(doc.data['textures'][ti]['source']))[:,:,:3]*2-1
        unit_error=max(unit_error,float(np.max(np.abs(np.linalg.norm(image,axis=2)-1))))
    if unit_error>.007:errors.append('nonunit baked normal map')
    maximum=max(angles,default=0.);p95=float(np.percentile(angles,95)) if angles else 0.
    if not row.get('proxy') and rig_data(doc)!=rig_data(base):errors.append('skin bind matrices or animation changed')
    return dict(level=row['level'],scope='new tangent cage: source geometric normal angles reported; baked shading checked in renders',
                max_degrees=maximum,p95_degrees=p95,vertices=len(angles),degenerate_uv_triangles=degenerate_uv,
                baked_normal_max_unit_error=unit_error,max_vertex_surface_distance_m=max_distance),errors


def audit(config):
    cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
    base=Document(source);base.select(cfg.get('include_nodes'));fields={}
    from kit.lod_scene import merge_static
    from kit.lod_shared import _triangle_limits
    shared=Document(source);shared.select(cfg.get('include_nodes'))
    if cfg.get('screen_space'):merge_static(shared,cfg.get('protected_nodes',[]),cfg.get('include_nodes',[]))
    for mi,pi,p in shared.primitives():
        attrs,faces=shared.arrays(p)
        tree=BVHTree.FromPolygons([Vector(p) for p in attrs['POSITION']],faces.tolist(),all_triangles=True)
        uv_keys=[k for k in attrs if k.startswith('TEXCOORD_')]
        fields[mi,pi]=(attrs,faces,tree,np.unique(signatures(attrs,uv_keys)))
    rows=[];errors=[]
    for row in m['levels'][1:]:
        if row.get('impostor'):
            rows.append(dict(level=row['level'],scope='unlit billboard; source surface normals intentionally replaced'))
            continue
        if row.get('rebaked') or row.get('proxy'):
            result,issues=atlas_normals(Document(out/row['path']),base,row);rows.append(result)
            errors.extend(f'LOD{row["level"]}: '+issue for issue in issues);continue
        if row.get('leaf_cards'):
            result,issues=foliage_normals(Document(out/row['path']),base,row);rows.append(result);errors.extend(issues);continue
        doc=Document(out/row['path']);angles=[];max_distance=0.;uv_degenerate=0;exact_total=0;tangent_dot=0.;tangent_length_error=0.;max_uv_error=0.;max_uv_ratio=0.;inherited_tangents=0
        mpp=m['height_m']/(1080*row['screen_height'])
        surface_radius=row.get('surface_tolerance_m',mpp*.75)*(2/.75)*1.01+2e-6
        texture_size=max((max(im['size']) for im in m['levels'][0]['images']),default=2048)
        uv_limits=[]
        if rig_data(doc)!=rig_data(base):errors.append(f'LOD{row["level"]}: skin bind data or animation changed')
        for mi,pi,p in doc.primitives():
            attrs,triangles=doc.arrays(p);src,faces,tree,known=fields[mi,pi]
            budgets=uv_budget(src,faces,mpp,texture_size)
            uv_limit=min((b['normalized_tolerance'] for b in budgets.values()),default=1.)+1e-6
            local_uv_error=0.;local_uv_ratio=0.
            face_limits=_triangle_limits(src,faces,mpp,texture_size)
            layer_limits={k:float(v.max())+1e-6 for k,v in face_limits.items()}
            uv_limits.append(dict(mesh=mi,primitive=pi,normalized_tolerance=uv_limit,layers=layer_limits))
            after=topology(attrs,triangles)[0];before=topology(src,faces)[0]
            uv_degenerate+=after['degenerate_uv']
            if any(n>before['degenerate_uv_by_layer'].get(k,0) for k,n in after['degenerate_uv_by_layer'].items()):
                errors.append(f'LOD{row["level"]}: new zero-area UV triangles')
            for key in src:
                if key.startswith(('JOINTS_','WEIGHTS_')) and not np.array_equal(src[key],attrs.get(key)):
                    errors.append(f'LOD{row["level"]}: protected skin weights changed')
            if 'TANGENT' in attrs:
                dot,length,inherited=tangent_errors(attrs,src)
                tangent_dot=max(tangent_dot,dot);tangent_length_error=max(tangent_length_error,length)
                inherited_tangents+=inherited
            uv_keys=[k for k in attrs if k.startswith('TEXCOORD_')]
            exact=np.isin(signatures(attrs,uv_keys),known);exact_total+=int(exact.sum())
            angles.extend([0.]*int(exact.sum()))
            for vi,point in enumerate(attrs['POSITION']):
                if exact[vi]:continue
                q,n,fi,dist=tree.find_nearest(Vector(point));max_distance=max(max_distance,dist)
                # A simplified fitting can be nearer a neighboring fitting
                # than its own original surface. Search within the cumulative
                # surface budget, then use the delivered UV field to identify
                # correspondence before judging the normal direction.
                candidates=tree.find_nearest_range(Vector(point),max(dist+1e-6,surface_radius))
                pairs=[]
                for qq,nn,ii,dd in candidates:
                    weights=barycentric(np.array(qq),src['POSITION'][faces[ii]].astype(float))
                    normal=weights@src['NORMAL'][faces[ii]];normal/=max(np.linalg.norm(normal),1e-30)
                    raw_errors={k:float(np.max(np.abs(attrs[k][vi]-weights@src[k][faces[ii]]))) for k in uv_keys}
                    uv_error=max((v/(face_limits[k][ii]+1e-6) for k,v in raw_errors.items()),default=0.)
                    dot=float(np.dot(attrs['NORMAL'][vi],normal))/max(np.linalg.norm(attrs['NORMAL'][vi]),1e-30)
                    pairs.append((uv_error,math.degrees(math.acos(np.clip(dot,-1,1))),max(raw_errors.values(),default=0.)))
                best_uv=min(p[0] for p in pairs)
                local_uv_ratio=max(local_uv_ratio,best_uv);max_uv_ratio=max(max_uv_ratio,best_uv)
                raw=min(p[2] for p in pairs if p[0]<=best_uv+1e-6)
                max_uv_error=max(max_uv_error,raw);local_uv_error=max(local_uv_error,raw)
                # A source atlas can legitimately reuse UVs on opposing skins.
                # Choose the normal among all correspondences satisfying the
                # unchanged half-mip-texel bound, not only the smallest UV
                # residual, which can belong to a different physical side.
                angle=min(p[1] for p in pairs if p[0]<=max(1.,best_uv)+1e-6)
                angles.append(angle)
            if local_uv_ratio>1.:errors.append(f'LOD{row["level"]}: source UV field changed in {mi}/{pi} ({local_uv_ratio:.6f} times the half-mip-texel bound)')
        maximum=float(max(angles,default=0));p95=float(np.percentile(angles,95)) if angles else 0.
        # A large outlier often means the wrong side of a hard edge. P95 gates
        # a broad field change; switch renders remain the stricter appearance
        # test for glossy faces and normal-map/tangent interactions.
        if maximum>45 or p95>10:errors.append(f'LOD{row["level"]}: source normal field changed ({maximum:.3f} max / {p95:.3f} p95 degrees)')
        if tangent_dot>1e-3 or tangent_length_error>2e-4:errors.append(f'LOD{row["level"]}: invalid tangent basis')
        rows.append(dict(level=row['level'],vertices=len(angles),exact_source_vertices=exact_total,
            projected_vertices=len(angles)-exact_total,max_degrees=maximum,p95_degrees=p95,degenerate_uv_triangles=uv_degenerate,
            max_tangent_normal_dot=tangent_dot,max_tangent_length_error=tangent_length_error,
            inherited_invalid_tangent_vertices=inherited_tangents,
            max_uv_correspondence_error=max_uv_error,max_uv_error_fraction_of_half_texel=max_uv_ratio,uv_correspondence_limit=max((v['normalized_tolerance'] for v in uv_limits),default=0.),uv_correspondence_limits=uv_limits,
            max_vertex_surface_distance_m=max_distance,
            max_vertex_surface_distance_pixels=max_distance*1080*row['screen_height']/m['height_m']))
    report=dict(passed=not errors,errors=errors,manifest_sha256=digest(out/'manifest.json'),
                auditor_sha256=digest(Path(__file__)),limits_degrees=dict(maximum=45,p95=10),levels=rows)
    (out/'normals-vs-lod0.json').write_text(json.dumps(report,indent=2)+'\n')
    print('LOD NORMAL FIELD',report['passed'],errors,flush=True)
    if errors:raise RuntimeError('; '.join(errors))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);audit(a.config)
