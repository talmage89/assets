"""Opt-in LOD builder/check CLI; source delivery is an immutable dependency.

blender -b --factory-startup --python-exit-code 1 --python kit/lod.py -- \
    build --config asset/src/lod.json
Same command with `check` measures fresh imports and validates rendered evidence.
Configuration paths are relative to the configuration's asset directory.
"""
import argparse
import copy
import hashlib
import json
import os
import sys
import fnmatch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from kit.lod_io import Document, digest, distance


def tool_digests():
    names=('lod.py','lod_io.py','lod_mesh.py','lod_impostor.py','lod_render.py','foliage.py',
           'detachable_textures.py','image_io.py')
    return {name:digest(ROOT/'kit'/name) for name in names}


def configuration(path):
    path=Path(path).resolve();cfg=json.loads(path.read_text());root=path.parent.parent
    levels=cfg['levels']
    if not levels or any(not 0<x['ratio']<1 or not 0<x['screen_height']<1 for x in levels):
        raise ValueError('Levels need positive ratios and screen heights below one')
    if any(b['ratio']>a['ratio'] or b['screen_height']>=a['screen_height'] for a,b in zip(levels,levels[1:])):
        raise ValueError('Levels must be ordered from near to far')
    source=(root/cfg['source']).resolve();out=(root/cfg.get('output','export/lod')).resolve()
    if out==source.parent or source.is_relative_to(out):raise ValueError('Output must not contain LOD0')
    return cfg,root,source,out


def textures(doc,out,max_size=None):
    """One content-addressed external copy across new levels; LOD0 stays embedded.

Building tiling maps keep their canonical external URIs. Embedded near maps
are copied byte for byte once; far sets filter in the existing kit's channel
spaces. BaseColor alpha is always independent data for opaque vehicle paint.
Alpha foliage is retained full size unless an explicit impostor is selected.
"""
    import io
    import numpy as np
    from PIL import Image
    from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
    paths={}
    for i,entry in enumerate(doc.data.get('images',[])):
        if 'uri' in entry and max_size is None:continue
        raw=doc.image(i);hsh=hashlib.sha256(raw).hexdigest()[:16]
        size='full' if max_size is None else str(max_size)
        dest=out/'textures'/f'{hsh}-{size}.png';dest.parent.mkdir(parents=True,exist_ok=True)
        # Rebuild generated copies even if a previous run left a truncated or
        # edited cache file. Source resources are always read-only.
        im=Image.open(io.BytesIO(raw));w,h=im.size
        if max_size is None or max(w,h)<=max_size:dest.write_bytes(raw)
        else:
            try:a=read_png(raw)
            except ValueError:a=np.asarray(im).astype(np.float32)/255
            factor=max(w,h)//max_size
            if w%factor or h%factor or factor<1:raise ValueError('Texture reduction requires integral ratio')
            role=entry.get('name','')
            if 'Normal' in role:a=a*2-1
            elif 'ORM' in role:a[:,:,1]**=2
            elif 'BaseColor' in role:a[:,:,:3]=srgb_to_linear(a[:,:,:3])
            else:raise ValueError('Reduced image needs BaseColor/Normal/ORM role in name')
            a=a.reshape(h//factor,factor,w//factor,factor,a.shape[2]).mean(axis=(1,3))
            if 'Normal' in role:
                a/=np.maximum(np.linalg.norm(a,axis=2,keepdims=True),1e-8);a=a*.5+.5
            elif 'ORM' in role:a[:,:,1]=np.sqrt(a[:,:,1])
            else:a[:,:,:3]=linear_to_srgb(a[:,:,:3])
            write_png(dest,a)
        paths[i]=dest
    return paths


def build(config):
    import bpy
    from kit.lod_mesh import simplify_parts
    cfg,root,source,out=configuration(config);out.mkdir(parents=True,exist_ok=True)
    original=Document(source);baseline=original.dependencies()
    original.select(cfg.get('include_nodes'))
    # Existing baseline may never silently adapt to a changed source.
    bp=out/'baseline.json'
    if bp.exists() and json.loads(bp.read_text())!=baseline:
        raise ValueError('LOD0/resources changed since baseline; review and remove LOD output explicitly')
    bp.write_text(json.dumps(baseline,indent=2)+'\n')
    bounds=original.bounds(cfg.get('include_nodes'));height=float(bounds[1][1]-bounds[0][1])
    manifest=dict(schema=1,source=os.path.relpath(source,out),baseline=baseline,
                  config_sha256=digest(config),height_m=height,kind=cfg['kind'],
                  convention='separate glTF/BIN; LOD0 is original',tools=tool_digests(),levels=[])
    analysis=[]
    zero=Document(source).stats()
    if cfg.get('include_nodes'):
        selected=original.stats()
        zero.update(triangles=selected['triangles'],placed_triangles=selected['placed_triangles'],
                    scope='Selected roots; byte/material/image costs describe the complete immutable source container')
    manifest['levels'].append(dict(level=0,path=os.path.relpath(source,out),**zero))
    for li,spec in enumerate(cfg['levels'],1):
        filename=f'{cfg.get("name",source.stem)}_LOD{li}.gltf';path=out/filename
        if spec.get('impostor'):
            import subprocess
            command=[str(ROOT/'kit/with_gpu.sh'),bpy.app.binary_path,'-b','--factory-startup',
                     '--python-exit-code','1','--python',str(ROOT/'kit/lod_impostor.py'),
                     '--','--source',str(source),'--out',str(path)]
            subprocess.run(command,check=True)
            stats=Document(path).stats()
            manifest['levels'].append(dict(level=li,path=filename,screen_height=spec['screen_height'],
                pixels_1080=1080*spec['screen_height'],distance_m=distance(height,spec['screen_height']),
                target_triangles=2,impostor=True,sha256=digest(path),**stats))
            continue
        doc=Document(out/manifest['levels'][-1]['path']);reports=[];switch=spec['screen_height']
        if li==1:doc.select(cfg.get('include_nodes'))
        dist=distance(height,switch);max_error=height/(1080*switch)*cfg.get('max_surface_pixels',.35)
        protected=set()
        # Preserve moving geometry itself, in addition to its frame. This keeps
        # engineered bearings and near-clearance fits intact on both sides of
        # the switch; far maps may still have a lower resolution.
        for ni,node in enumerate(doc.data['nodes']):
            current=ni
            while True:
                extras=doc.data['nodes'][current].get('extras',{})
                if any(k in extras for k in ('pivot_axis','slide_axis','socket_kind')) or any(fnmatch.fnmatchcase(doc.data['nodes'][current].get('name',''),pattern) for pattern in cfg.get('protected_nodes',[])):
                    if 'mesh' in node:protected.add(node['mesh'])
                    break
                if current not in doc.parents:break
                current=doc.parents[current]
        for mi,pi,p in doc.primitives():
            attrs,faces=doc.arrays(p)
            mat=doc.data.get('materials',[])[p.get('material',0)]
            if mi in protected:
                row=dict(status='retained',reason='moving/socket geometry protected',triangles=len(faces))
            elif mat.get('alphaMode') in ('MASK','BLEND'):
                row=dict(status='retained',reason='alpha coverage protected',triangles=len(faces))
            else:
                uv_limit=max(1/2048,.35/(1080*switch))
                preceding=manifest['levels'][-1]['triangles']/manifest['levels'][0]['triangles']
                ratio=min(.999,spec['ratio']/preceding)
                new,tri,row=simplify_parts(attrs,faces,ratio,max_error,uv_limit,cfg.get('drop_subpixel',False))
                if row['status']=='simplified':doc.replace(p,new,tri)
            reports.append(dict(mesh=doc.data['meshes'][mi].get('name',str(mi)),primitive=pi,**row))
        doc.save(path,image_paths=textures(doc,out,spec.get('texture_size')))
        stats=Document(path).stats(cfg.get('include_nodes'))
        row=dict(level=li,path=filename,screen_height=switch,pixels_1080=switch*1080,
                 distance_m=dist,target_triangles=round(manifest['levels'][0]['triangles']*spec['ratio']),
                 surface_tolerance_m=max_error,target_met=stats['triangles']<=round(manifest['levels'][0]['triangles']*spec['ratio']),**stats)
        analysis.append(dict(level=li,primitives=reports))
        row['sha256']=digest(path);manifest['levels'].append(row)
        print('LOD',li,stats['triangles'],'target',row['target_triangles'],flush=True)
    if Document(source).dependencies()!=baseline:raise ValueError('LOD0 changed during build')
    report_dir=root/'build/lod'/cfg.get('name',source.stem);report_dir.mkdir(parents=True,exist_ok=True)
    (report_dir/'simplification.json').write_text(json.dumps(analysis,indent=2,allow_nan=False)+'\n')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
    print('LOD manifest',out/'manifest.json',flush=True)


def check(config, require_renders=True):
    import bpy
    import numpy as np
    from kit.lod_mesh import topology
    cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
    errors=[];base=Document(source);original={}
    base.select(cfg.get('include_nodes'))
    unchanged=Document(source).dependencies()==m['baseline']
    if not unchanged:errors.append('LOD0 dependency bytes changed')
    if digest(config)!=m['config_sha256']:errors.append('stale configuration')
    if m.get('tools')!=tool_digests():errors.append('stale LOD tool recipe')
    for mi,pi,p in base.primitives(): original[mi,pi]=topology(*base.arrays(p))[0]
    reports=[]
    for row in m['levels'][1:]:
        path=out/row['path'];doc=Document(path);stats=doc.stats(cfg.get('include_nodes'))
        if digest(path)!=row['sha256']:errors.append(f'{path.name}: bytes changed')
        if stats['triangles']>m['levels'][row['level']-1]['triangles']:errors.append('triangle count increased down chain')
        if any(stats[k]!=row[k] for k in stats if k in row):errors.append(f'{path.name}: stale package stats')
        if row.get('impostor'):
            expected=copy.deepcopy(base.data['nodes'])
            for n in expected:n.pop('mesh',None)
            if doc.data['nodes'][:-1]!=expected:errors.append('impostor lost original transform nodes')
        else:
            if doc.data['nodes']!=base.data['nodes']:errors.append('node names/pivots/extras/hierarchy changed')
            if doc.data.get('materials')!=base.data.get('materials'):errors.append('material boundaries/settings changed')
        topo=[]
        for mi,pi,p in doc.primitives():
            attrs,faces=doc.arrays(p);r,_=topology(attrs,faces)
            if any(not np.isfinite(v).all() for v in attrs.values()):errors.append('nonfinite vertex attributes')
            if row.get('impostor'):
                b=dict(degenerate=0,slivers=0,nonmanifold_edges=0,winding_disagreements=0,boundary_edges=4)
            else:b=original[mi,pi]
            for key in ('degenerate','slivers','nonmanifold_edges','winding_disagreements'):
                if r[key]>b[key]:errors.append(f'{path.name}: new {key}')
            if r['boundary_edges']>b['boundary_edges']:errors.append(f'{path.name}: new open edges')
            normals=attrs.get('NORMAL')
            if normals is None or np.max(np.abs(np.linalg.norm(normals,axis=1)-1))>2e-4:
                errors.append(f'{path.name}: nonunit normals')
            topo.append(dict(mesh=mi,primitive=pi,**r))
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(path),import_pack_images=False)
        mesh_names={n.get('name') for n in doc.data['nodes'] if 'mesh' in n}
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name in mesh_names]
        actual=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
        if actual!=stats['placed_triangles']:errors.append(f'{path.name}: import triangle count {actual}')
        # Independently measure actual imported surfaces and pivot frames against
        # this level's raw accessors, not constants copied from the source scene.
        from mathutils.kdtree import KDTree
        convert=np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]],float)
        inverse=convert.T;position_error=0.;pivot_error=0.;vertices_checked=0;pivots_checked=0
        joints={j for skin in doc.data.get('skins',[]) for j in skin['joints']}
        for ni,node in enumerate(doc.data['nodes']):
            if ni in joints:continue
            ob=bpy.data.objects.get(node.get('name',''))
            if ob is None:
                errors.append(f'{path.name}: missing imported node '+node.get('name',''));continue
            if 'mesh' in node:
                if ob.type!='MESH':errors.append('Imported mesh is missing');continue
                points=[]
                for p in doc.data['meshes'][node['mesh']]['primitives']:
                    pos=doc.accessor(p['attributes']['POSITION'])
                    matrix=convert@(np.eye(4) if 'skin' in node else doc.world(ni))
                    points.extend(pos@matrix[:3,:3].T+matrix[:3,3])
                tree=KDTree(len(points))
                for j,pt in enumerate(points):tree.insert(pt,j)
                tree.balance()
                for v in ob.data.vertices:
                    position_error=max(position_error,tree.find(ob.matrix_world@v.co)[2]);vertices_checked+=1
            elif ob.type=='EMPTY':
                expected=convert@doc.world(ni)@inverse
                pivot_error=max(pivot_error,float(np.max(np.abs(np.array(ob.matrix_world)-expected))));pivots_checked+=1
        if position_error>2e-5:errors.append(f'{path.name}: imported surface position drift {position_error}')
        if pivot_error>2e-5:errors.append(f'{path.name}: imported pivot drift {pivot_error}')
        reports.append(dict(level=row['level'],triangles_reimported=actual,topology=topo,
            imported_position_error_m=position_error,imported_pivot_matrix_error=pivot_error,
            imported_vertices_checked=vertices_checked,imported_pivots_checked=pivots_checked))
    render_path=root/cfg.get('renders','renders/lod')/'metrics.json'
    if require_renders:
        if not render_path.exists():errors.append('missing switch-distance renders')
        else:
            renders=json.loads(render_path.read_text())
            if renders['manifest_sha256']!=digest(out/'manifest.json'):errors.append('stale rendered evidence')
            if renders.get('renderer_sha256')!=digest(ROOT/'kit/lod_render.py'):errors.append('stale renderer recipe')
            if not renders['passed']:errors.append('render differences exceed threshold')
            for file,h in renders['files'].items():
                p=render_path.parent/file
                if not p.exists() or digest(p)!=h:errors.append('render missing or changed: '+file)
    report=dict(passed=not errors,errors=errors,manifest_sha256=digest(out/'manifest.json'),lod0_byte_identical=unchanged,levels=reports)
    (out/'check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('LOD CHECK',report['passed'],errors,flush=True)
    if errors:raise RuntimeError('; '.join(errors))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','check'])
    p.add_argument('--config',required=True);p.add_argument('--geometry-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.action=='build':build(a.config)
    else:check(a.config,not a.geometry_only)


if __name__=='__main__':main()
