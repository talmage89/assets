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
from kit.lod_io import Document, digest, distance, residency, shared_material_bindings


def tool_digests():
    names=('lod_shading.py','lod_constraints.py','lod_shared.py','lod_shells.py','lod.py','lod_io.py','lod_foliage.py','lod_mesh.py','lod_scene.py','lod_layout.py','lod_gpu.py','lod_atlas.py','lod_transfer.py','lod_impostor_fit.py','lod_impostor.py','lod_render.py','foliage.py',
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
        zero['container_materials']=zero['materials'];zero['container_draw_calls']=zero['draw_calls']
        zero.update(triangles=selected['triangles'],placed_triangles=selected['placed_triangles'],
                    materials=selected['materials'],draw_calls=selected['draw_calls'],
                    scope='Selected roots for triangles/materials/draws; bytes/images/mesh allocation describe the complete immutable source container')
    manifest['levels'].append(dict(level=0,path=os.path.relpath(source,out),**zero))
    for li,spec in enumerate(cfg['levels'],1):
        filename=f'{cfg.get("name",source.stem)}_LOD{li}.gltf';path=out/filename
        if spec.get('impostor'):
            from kit.lod_gpu import locked
            from kit.lod_impostor import build as build_impostor
            with locked():build_impostor(source,path,spec.get('impostor')=='crossed')
            stats=Document(path).stats()
            item=dict(level=li,path=filename,screen_height=spec['screen_height'],
                pixels_1080=1080*spec['screen_height'],distance_m=distance(height,spec['screen_height']),
                target_triangles=8 if spec.get('impostor')=='crossed' else 2,impostor=True,crossed=spec.get('impostor')=='crossed',sha256=digest(path),**stats)
            if item['crossed']:
                alt=path.with_name(path.stem+'_CameraFacing.gltf');altstats=Document(alt).stats()
                item['alternatives']=[dict(level=li,path=alt.name,alternative='camera-facing',impostor=True,crossed=False,
                    target_triangles=2,screen_height=spec['screen_height'],distance_m=item['distance_m'],sha256=digest(alt),**altstats)]
            manifest['levels'].append(item)
            continue
        doc=Document(source);doc.select(cfg.get('include_nodes'));reports=[];switch=spec['screen_height']
        dist=distance(height,switch);meters_per_pixel=height/(1080*switch)
        max_error=meters_per_pixel*spec.get('surface_pixels',cfg.get('max_surface_pixels',.75))
        from kit.lod_scene import merge_static,proxy,shell_static
        assembly=None
        if spec.get('proxy'):
            assembly=proxy(doc,spec.get('proxy_budget',spec['target_triangles']),meters_per_pixel,spec.get('preserve_concavity',[]),spec.get('proxy_remesh',False))
        elif spec.get('leaf_cards'):
            from kit.lod_foliage import build as build_foliage
            reports=build_foliage(doc,round(manifest['levels'][0]['triangles']*spec['ratio']),meters_per_pixel,spec.get('leaf_scale_exponent',.4),spec.get('leaf_selection','balanced'))
        elif cfg.get('screen_space'):
            from kit.lod_mesh import reduce_screen,uv_budget
            assembly=merge_static(doc,cfg.get('protected_nodes',[]),cfg.get('include_nodes',[]))
            if not spec.get('rebake'):
                from kit.lod_shared import meshes
                reports=meshes(doc,spec['ratio'],meters_per_pixel,cfg.get('feature_pixels',1.5),spec.get('surface_pixels',cfg.get('max_surface_pixels',.75)),seam_sliding=spec.get('seam_sliding',cfg.get('seam_sliding',True)))
            else:
                if spec.get('static_shell'):assembly['shells']=shell_static(doc,spec['ratio'],meters_per_pixel)
                static_meshes={n['mesh'] for n in doc.data['nodes'] if 'mesh' in n and n.get('extras',{}).get('lod_static_shell')}
                for mi,pi,p in doc.primitives():
                    attrs,faces=doc.arrays(p)
                    mat=doc.data.get('materials',[])[p.get('material',0)]
                    if mi in static_meshes:
                        reports.append(dict(mesh=mi,primitive=pi,status='static shell',triangles=len(faces)));continue
                    if mat.get('alphaMode') in ('MASK','BLEND') or (any(k.startswith(('JOINTS_','WEIGHTS_')) for k in attrs) and not spec.get('rebake')):
                        row=dict(status='retained',reason='alpha/skin retained',triangles=len(faces))
                    else:
                        budgets=uv_budget(attrs,faces,meters_per_pixel,spec.get('texture_size',2048))
                        new,tri,row=reduce_screen(attrs,faces,spec['ratio'],meters_per_pixel,
                             cfg.get('feature_pixels',1.5),rebake=spec.get('rebake',False),uv_limit=min((b['normalized_tolerance'] for b in budgets.values()),default=1),
                             surface_pixels=spec.get('surface_pixels',cfg.get('max_surface_pixels',.75)))
                        row['uv_budgets']=budgets
                        doc.replace(p,new,tri)
                    reports.append(dict(mesh=doc.data['meshes'][mi].get('name',str(mi)),primitive=pi,**row))
        else:
            for mi,pi,p in doc.primitives():
                attrs,faces=doc.arrays(p)
                mat=doc.data.get('materials',[])[p.get('material',0)]
                if any(k.startswith(('JOINTS_','WEIGHTS_')) for k in attrs) or mat.get('alphaMode') in ('MASK','BLEND'):
                    row=dict(status='retained',triangles=len(faces))
                else:
                    new,tri,row=simplify_parts(attrs,faces,spec['ratio'],max_error,max(1/2048,.35/(1080*switch)),cfg.get('drop_subpixel',False))
                    if row['status']=='simplified':doc.replace(p,new,tri)
                reports.append(dict(mesh=doc.data['meshes'][mi].get('name',str(mi)),primitive=pi,**row))
        if spec.get('rebake') or spec.get('proxy'):
            temp=root/'build/lod'/cfg.get('name',source.stem)/f'LOD{li}-geometry.gltf';temp.parent.mkdir(parents=True,exist_ok=True)
            doc.save(temp,image_paths=textures(doc,temp.parent))
            cache=path.parent/(path.stem+'-maps')/'bake.json'
            recipe=dict(input_dependencies=Document(temp).dependencies(),source_dependencies=Document(source).dependencies(),
                        baker_sha256=digest(ROOT/'kit/lod_atlas.py'),layout_sha256=digest(ROOT/'kit/lod_layout.py'),transfer_sha256=digest(ROOT/'kit/lod_transfer.py'),
                        proxy=bool(spec.get('proxy')),composite_alpha=bool(spec.get('static_shell')),size=spec.get('texture_size',2048),projection_m=max_error*2)
            valid=False
            if cache.exists() and path.exists():
                old=json.loads(cache.read_text())
                valid=old.get('recipe')==recipe and all((cache.parent/f'T_{path.stem}_{k}.png').exists() and digest(cache.parent/f'T_{path.stem}_{k}.png')==v['sha256'] for k,v in old.get('maps',{}).items())
            if not valid:
                from kit.lod_gpu import locked
                from kit.lod_atlas import bake as bake_atlas
                baked=Document(temp)
                with locked():bake_atlas(baked,source,path,spec.get('texture_size',2048),
                    proxy=bool(spec.get('proxy')),projection_m=max_error*2,composite_alpha=bool(spec.get('static_shell')))
                baked.save(path)
                report=json.loads(cache.read_text());report['recipe']=recipe;cache.write_text(json.dumps(report,indent=2)+'\n')
        else:doc.save(path,image_paths=textures(doc,out,spec.get('texture_size')))
        stats=Document(path).stats()
        target=spec.get('target_triangles',round(manifest['levels'][0]['triangles']*spec['ratio']))
        row=dict(level=li,path=filename,screen_height=switch,pixels_1080=switch*1080,
                 distance_m=dist,target_triangles=target,surface_tolerance_m=max_error,
                 meters_per_pixel=meters_per_pixel,rebaked=bool(spec.get('rebake')),proxy=bool(spec.get('proxy')),
                 shared_maps=not bool(spec.get('rebake') or spec.get('proxy')),assembly=assembly,leaf_cards=bool(spec.get('leaf_cards')),target_met=stats['triangles']<=target,**stats)
        if row['shared_maps']:row['canonical_material_bindings']=shared_material_bindings(Document(source),Document(path))
        analysis.append(dict(level=li,primitives=reports))
        row['sha256']=digest(path);manifest['levels'].append(row)
        print('LOD',li,stats['triangles'],'target',row['target_triangles'],flush=True)
    if Document(source).dependencies()!=baseline:raise ValueError('LOD0 changed during build')
    if tool_digests()!=manifest['tools']:raise ValueError('LOD tool changed during build; rerun with a stable recipe')
    report_dir=root/'build/lod'/cfg.get('name',source.stem);report_dir.mkdir(parents=True,exist_ok=True)
    (report_dir/'simplification.json').write_text(json.dumps(analysis,indent=2,allow_nan=False)+'\n')
    manifest['resident']=residency(manifest['levels'])
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
    print('LOD manifest',out/'manifest.json',flush=True)


def check(config, require_renders=True):
    import bpy
    import numpy as np
    from kit.lod_mesh import topology,world_geometry,shell_volumes
    cfg,root,source,out=configuration(config);m=json.loads((out/'manifest.json').read_text())
    errors=[];base=Document(source);original={}
    base.select(cfg.get('include_nodes'))
    unchanged=Document(source).dependencies()==m['baseline']
    if not unchanged:errors.append('LOD0 dependency bytes changed')
    if digest(config)!=m['config_sha256']:errors.append('stale configuration')
    if m.get('tools')!=tool_digests():errors.append('stale LOD tool recipe')
    for mi,pi,p in base.primitives(): original[mi,pi]=topology(*base.arrays(p))[0]
    if m.get('resident')!=residency(m['levels']):errors.append('stale resident memory accounting')
    if not residency(m['levels'])['passed']:errors.append('intermediate levels add texture allocations')
    reports=[]
    for row in m['levels'][1:]+[a for r in m['levels'] for a in r.get('alternatives',[])]:
        path=out/row['path'];doc=Document(path);stats=doc.stats()
        if digest(path)!=row['sha256']:errors.append(f'{path.name}: bytes changed')
        if stats['triangles']>m['levels'][row['level']-1]['triangles']:errors.append('triangle count increased down chain')
        if any(stats[k]!=row[k] for k in stats if k in row):errors.append(f'{path.name}: stale package stats')
        if row.get('impostor'):
            expected=copy.deepcopy(base.data['nodes'])
            for n in expected:n.pop('mesh',None)
            if doc.data['nodes'][:-1]!=expected:errors.append('impostor lost original transform nodes')
        elif row.get('rebaked') or row.get('proxy') or row.get('assembly'):
            def frame(node):
                n=copy.deepcopy(node);n.pop('mesh',None)
                children=[c for c in n.get('children',[]) if c<len(base.data['nodes'])]
                if children:n['children']=children
                else:n.pop('children',None)
                if row.get('proxy'):n.pop('skin',None)
                if 'extras' in n:
                    n['extras']={k:v for k,v in n['extras'].items() if not k.startswith('lod_')}
                    if not n['extras']:n.pop('extras')
                return n
            if [frame(n) for n in doc.data['nodes'][:len(base.data['nodes'])]]!=[frame(n) for n in base.data['nodes']]:errors.append('canonical names/pivots/extras/hierarchy changed')
        else:
            if doc.data['nodes']!=base.data['nodes']:errors.append('node names/pivots/extras/hierarchy changed')
            if doc.data.get('materials')!=base.data.get('materials'):errors.append('material boundaries/settings changed')
        if row.get('shared_maps') and doc.data.get('materials')!=base.data.get('materials'):errors.append('shared LOD material settings changed')
        if row.get('shared_maps') and not {i['sha256'] for i in stats['images']}<={i['sha256'] for i in m['levels'][0]['images']}:errors.append('intermediate level adds images')
        if row.get('shared_maps') and row.get('canonical_material_bindings')!=shared_material_bindings(Document(source),doc):errors.append('stale canonical material bindings')
        topo=[]
        for mi,pi,p in doc.primitives():
            attrs,faces=doc.arrays(p);r,_=topology(attrs,faces)
            if any(not np.isfinite(v).all() for v in attrs.values()):errors.append('nonfinite vertex attributes')
            if row.get('impostor'):
                b=dict(degenerate=0,slivers=0,nonmanifold_edges=0,winding_disagreements=0,boundary_edges=16 if row.get('crossed') else 4)
            elif row.get('rebaked') or row.get('proxy') or row.get('assembly'):
                b={k:sum(v[k] for v in original.values()) for k in ('degenerate','slivers','nonmanifold_edges','winding_disagreements','boundary_edges')}
                if row.get('proxy'):b.update(boundary_edges=0,nonmanifold_edges=0,degenerate=0,slivers=0,winding_disagreements=0)
            else:b=original[mi,pi]
            for key in ('degenerate','slivers','nonmanifold_edges','winding_disagreements'):
                if r[key]>b[key]:errors.append(f'{path.name}: new {key}')
            if not (row.get('rebaked') or row.get('proxy') or row.get('assembly')) and r['boundary_edges']>b['boundary_edges']:errors.append(f'{path.name}: new open edges')
            normals=attrs.get('NORMAL')
            if normals is None or np.max(np.abs(np.linalg.norm(normals,axis=1)-1))>2e-4:
                errors.append(f'{path.name}: nonunit normals')
            topo.append(dict(mesh=mi,primitive=pi,**r))
        assembly_topology=[]
        if row.get('rebaked') or row.get('proxy') or row.get('assembly'):
            for ni,node in enumerate(doc.data['nodes']):
                if 'mesh' not in node:continue
                current,_=topology(*world_geometry(doc,[ni]))
                source_ids=node.get('extras',{}).get('lod_sources',[ni])
                previous,_=topology(*world_geometry(base,source_ids))
                limit=0 if row.get('proxy') or node.get('extras',{}).get('lod_static_shell') else previous['boundary_edges']
                if current['boundary_edges']>limit:errors.append(f'{path.name}: new open assembly edges: '+node.get('name',''))
                if current['nonmanifold_edges']>(0 if row.get('proxy') or node.get('extras',{}).get('lod_static_shell') else previous['nonmanifold_edges']):
                    errors.append(f'{path.name}: nonmanifold shell: '+node.get('name',''))
                if row.get('proxy') or node.get('extras',{}).get('lod_static_shell'):
                    volumes=shell_volumes(*world_geometry(doc,[ni]))
                    floor=(m['height_m']/(1080*row['screen_height']))**3*1e-8
                    current['shell_volume']=dict(components=len(volumes),minimum_m3=min(volumes,default=0),nonpositive=sum(v<=floor for v in volumes))
                    if any(v<=floor for v in volumes):errors.append(f'{path.name}: inward or collapsed shell: '+node.get('name',''))
                assembly_topology.append(dict(node=node.get('name'),before=previous,after=current))
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
        reports.append(dict(level=row['level'],triangles_reimported=actual,topology=topo,assembly_topology=assembly_topology,
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
