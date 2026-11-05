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
from kit.lod_mesh import barycentric,topology


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


def audit(config):
    cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
    base=Document(source);base.select(cfg.get('include_nodes'));fields={}
    for mi,pi,p in base.primitives():
        attrs,faces=base.arrays(p)
        tree=BVHTree.FromPolygons([Vector(p) for p in attrs['POSITION']],faces.tolist(),all_triangles=True)
        uv_keys=[k for k in attrs if k.startswith('TEXCOORD_')]
        fields[mi,pi]=(attrs,faces,tree,np.unique(signatures(attrs,uv_keys)))
    rows=[];errors=[]
    for row in m['levels'][1:]:
        if row.get('impostor'):
            rows.append(dict(level=row['level'],scope='unlit billboard; source surface normals intentionally replaced'))
            continue
        doc=Document(out/row['path']);angles=[];max_distance=0.;uv_degenerate=0;exact_total=0;tangent_dot=0.;tangent_length_error=0.;max_uv_error=0.;inherited_tangents=0
        preceding=m['levels'][1:row['level']+1]
        surface_radius=sum(r.get('surface_tolerance_m',.35*m['height_m']/(1080*r['screen_height'])) for r in preceding)*1.01+2e-6
        uv_limit=sum(max(1/2048,.35/(1080*r['screen_height'])) for r in preceding)+1e-6
        if rig_data(doc)!=rig_data(base):errors.append(f'LOD{row["level"]}: skin bind data or animation changed')
        for mi,pi,p in doc.primitives():
            attrs,triangles=doc.arrays(p);src,faces,tree,known=fields[mi,pi]
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
                    uv_error=max((float(np.max(np.abs(attrs[k][vi]-weights@src[k][faces[ii]]))) for k in uv_keys),default=0.)
                    dot=float(np.dot(attrs['NORMAL'][vi],normal))/max(np.linalg.norm(attrs['NORMAL'][vi]),1e-30)
                    pairs.append((uv_error,math.degrees(math.acos(np.clip(dot,-1,1)))))
                best_uv=min(p[0] for p in pairs)
                max_uv_error=max(max_uv_error,best_uv)
                angle=min(p[1] for p in pairs if p[0]<=best_uv+1e-6)
                angles.append(angle)
        maximum=float(max(angles,default=0));p95=float(np.percentile(angles,95)) if angles else 0.
        # A large outlier often means the wrong side of a hard edge. P95 gates
        # a broad field change; switch renders remain the stricter appearance
        # test for glossy faces and normal-map/tangent interactions.
        if maximum>45 or p95>10:errors.append(f'LOD{row["level"]}: source normal field changed ({maximum:.3f} max / {p95:.3f} p95 degrees)')
        if max_uv_error>uv_limit:errors.append(f'LOD{row["level"]}: source UV field changed ({max_uv_error:.6f})')
        if tangent_dot>1e-3 or tangent_length_error>2e-4:errors.append(f'LOD{row["level"]}: invalid tangent basis')
        rows.append(dict(level=row['level'],vertices=len(angles),exact_source_vertices=exact_total,
            projected_vertices=len(angles)-exact_total,max_degrees=maximum,p95_degrees=p95,degenerate_uv_triangles=uv_degenerate,
            max_tangent_normal_dot=tangent_dot,max_tangent_length_error=tangent_length_error,
            inherited_invalid_tangent_vertices=inherited_tangents,
            max_uv_correspondence_error=max_uv_error,uv_correspondence_limit=uv_limit,
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
