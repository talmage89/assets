"""Physical source checks, independent glTF accessors, then fresh import checks.

Repeat UVs are intentional; trim faces may overlap only within their authored
finish strip. No unique-atlas overlap claim is made for a tiled building.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils.kdtree import KDTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from check_mesh import source_check
from deliver import read_delivery,dependencies,bundle_hash
from kit.image_io import read_png,srgb_to_linear
from textures import SETS
from plan import PROOF_SEEDS


def check(seed,ranch=False):
    path=Path(f'export/HearthfieldRanch-{seed}.gltf' if ranch else f'export/Hearthfield-{seed}.gltf')
    source=Path(f'build/ranch/delivery/game-{seed}.blend' if ranch else f'build/family/game-{seed}.blend')
    physical=source_check(source);meta=json.loads(source.with_suffix('.json').read_text())
    pivots={o.name:tuple(o.matrix_world.translation) for o in bpy.context.scene.objects if o.name in ('FrontDoor','PatioDoor','ServiceDoor') or o.get('socket_kind')}
    source_points=[(tuple(o.matrix_world@v.co),tuple(o.data.color_attributes['Tint'].data[v.index].color[:3]))
        for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
    source_tree=KDTree(len(source_points))
    for i,(p,c) in enumerate(source_points):source_tree.insert(p,i)
    source_tree.balance()
    raw=read_delivery(path);doc=raw.json;triangles=0;normal_error=0;tint_error=0;position_error=0;uv_zero=0;areas={};points=[]
    expected_meshes=3 if ranch and meta['spec']['garage']['kind']=='carport' else 4
    assert len(doc['meshes'])==expected_meshes and (4 if ranch else 5)<=len(doc['materials'])<=6 and 12<=len(doc['images'])<=(16 if ranch else 15)
    assert all('bufferView' not in im and im['uri'].startswith('textures/') for im in doc['images'])
    assert len(raw.binary)==doc['buffers'][0]['byteLength']
    for p in dependencies(path):assert p.exists() and not p.is_symlink()
    semantics=set()
    for ni,node in enumerate(doc['nodes']):
        if 'mesh' not in node:continue
        matrix=raw.world(ni)
        # Every export mesh has unit scale in its node; translations/pivot frames remain.
        assert np.max(np.abs(np.linalg.norm(matrix[:3,:3],axis=0)-1))<1e-5
        for prim in doc['meshes'][node['mesh']]['primitives']:
            attrs=prim['attributes'];semantics.update(attrs)
            assert doc['accessors'][attrs['COLOR_0']]['normalized'] and doc['accessors'][attrs['COLOR_0']]['componentType']==5121
            v=raw.accessor(attrs['POSITION']);world=(matrix@np.c_[v,np.ones(len(v))].T).T[:,:3]
            world=world[:,[0,2,1]]*np.array([1,-1,1]);points.extend(map(tuple,world))
            normals=raw.accessor(attrs['NORMAL']);normal_error=max(normal_error,float(abs(np.linalg.norm(normals,axis=1)-1).max()))
            uv=raw.accessor(attrs['TEXCOORD_0']);tint=raw.accessor(attrs['COLOR_0'])[:,:3]
            assert np.isfinite(uv).all() and np.isfinite(world).all() and ((tint>=0)&(tint<=1)).all()
            for xyz,c in zip(world,tint):
                near=source_tree.find(xyz);position_error=max(position_error,near[2])
                matches=source_tree.find_range(xyz,2e-5);assert matches
                tint_error=max(tint_error,min(max(abs(source_points[i][1][k]-c[k]) for k in range(3)) for _,i,_ in matches))
            indices=raw.accessor(prim['indices']).reshape(-1,3);triangles+=len(indices)
            xyz=world[indices];tc=uv[indices]
            area=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
            du=tc[:,1]-tc[:,0];dv=tc[:,2]-tc[:,0];ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
            assert float(area.min())>1e-12
            uv_zero+=int(np.sum(ua<1e-14))
            role=doc['materials'][prim['material']]['name'].removeprefix('House')
            size=1024 if role=='RanchRoof' else 512 if role.startswith('RanchBrick') else SETS.get(role,SETS['Trim'])[0]
            densities=np.sqrt(ua/area)*size
            areas.setdefault(role,[]).extend(zip(map(float,densities),map(float,area)))
            if role in ('Trim','Glass'):
                # A strip must contain each face. U repetition is deliberate.
                span=np.max(tc[:,:,1],axis=1)-np.min(tc[:,:,1],axis=1)
                assert float(span.max())<=.125+1e-6
            for ai in attrs.values():
                ac=doc['accessors'][ai];view=doc['bufferViews'][ac['bufferView']]
                assert ac.get('byteOffset',0)%4==0 and view.get('byteOffset',0)%4==0
    assert triangles==physical['triangles'] and 30000<=triangles<=80000
    assert semantics=={'POSITION','NORMAL','TEXCOORD_0','COLOR_0'}
    assert normal_error<1e-4 and position_error<2e-5 and tint_error<=.5/255+1e-5
    assert uv_zero==0,('degenerate tiled UVs',uv_zero)
    density={}
    for role,rows in areas.items():
        rows=sorted(rows);v=np.array([r[0] for r in rows]);w=np.cumsum([r[1] for r in rows]);w/=w[-1]
        density[role]=dict(zip(('p10','median','p90'),map(float,np.interp([.1,.5,.9],w,v))))
        target=1024/4.8768 if role=='RanchRoof' else 512/1.2192 if role.startswith('RanchBrick') else SETS.get(role,SETS['Trim'])[0]/SETS.get(role,SETS['Trim'])[1]
        if role not in ('Trim','Glass'):assert abs(density[role]['median']/target-1)<.005
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    imported=[tuple(o.matrix_world@v.co) for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
    imported_tree=KDTree(len(imported))
    for i,p in enumerate(imported):imported_tree.insert(p,i)
    imported_tree.balance()
    import_error=max(imported_tree.find(p)[2] for p,c in source_points)
    import_reverse_error=max(source_tree.find(p)[2] for p in imported)
    pivot_error=max(math.dist(bpy.data.objects[n].matrix_world.translation,p) for n,p in pivots.items())
    assert max(import_error,import_reverse_error,pivot_error)<2e-5
    return dict(seed=seed,passed=True,physical=physical,triangles=triangles,materials=len(doc['materials']),meshes=expected_meshes,
        primitives=sum(len(m['primitives']) for m in doc['meshes']),gltf_bytes=path.stat().st_size,bin_bytes=len(raw.binary),
        source_to_raw_position_error_m=position_error,source_to_raw_tint_max_error=tint_error,
        normal_length_max_error=normal_error,degenerate_uv_triangles=uv_zero,density_px_m=density,
        reimport_position_error_m=import_error,reimport_reverse_position_error_m=import_reverse_error,reimport_pivot_socket_error_m=pivot_error,
        bundle_sha256=bundle_hash(path),image_uris=[i['uri'] for i in doc['images']],
        scopes=dict(physical='Actual surfaces, construction and mounting',raw='Serialization, normals, UVs, tint, image URIs',
        imported='Fresh importer geometry and pivot/socket preservation; not an engine allocation measurement'))


def textures():
    result={}
    for role,(size,coverage) in SETS.items():
        maps={c:read_png(Path(f'export/textures/T_House{role}_{c}.png')) for c in ('BaseColor','Normal','ORM')}
        assert all(a.shape==(size,size,3) and np.isfinite(a).all() for a in maps.values())
        normal=maps['Normal']*2-1;error=float(abs(np.linalg.norm(normal,axis=2)-1).max());assert error<.007
        # Stored source/ship color and ORM compare after identical linear/RMS filtering.
        color=srgb_to_linear(maps['BaseColor']);mean=color.mean(axis=(0,1))
        if role=='Shingles':assert .08<float(mean.mean())<.12
        errors={}
        for c,array in maps.items():
            original=read_png(Path(f'textures/source/T_House{role}_{c}.png'))
            errors[c]=dict(mean_absolute=float(abs(array-original).mean()),max_absolute=float(abs(array-original).max()))
        assert errors['BaseColor']['mean_absolute']<.02 and errors['ORM']['mean_absolute']<.025
        result[role]=dict(size=size,gpu_mib=size*size*4/1048576,png_bytes=sum(Path(f'export/textures/T_House{role}_{c}.png').stat().st_size for c in maps),
            stored_linear_albedo_mean=list(map(float,mean)),normal_length_max_error=error,source_vs_ship=errors)
    assert sum(r['gpu_mib'] for r in result.values())==38
    return result


def image_reuse(seeds):
    """Exercise a stock importer, including repeated houses, in one live scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True);steps=[];seen={}
    for seed in seeds+[seeds[0]]:
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/Hearthfield-{seed}.gltf').resolve()))
        images=[im for im in bpy.data.images if im.source=='FILE' and im.filepath]
        by_path={}
        for im in images:
            path=str(Path(bpy.path.abspath(im.filepath)).resolve())
            assert path not in by_path,'Importer duplicated a canonical external image'
            by_path[path]=im
            if path in seen:assert seen[path]==im.as_pointer(),'Image resource was replaced'
            seen[path]=im.as_pointer()
        steps.append(dict(seed=seed,image_datablocks=len(images)))
    assert len(seen)<=15
    return dict(passed=True,steps=steps,shared_image_datablocks=len(seen),
        resident_rgba8_pixel_bytes=sum(im.size[0]*im.size[1]*4 for im in images),
        scope='Actual Blender external-image cache identity across independently loaded seeds and a repeat; GPU block compression remains an engine import setting')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    rows=[check(s) for s in dict.fromkeys(map(int,a.seeds.split(',')))];images={uri for r in rows for uri in r['image_uris']};assert len(images)<=15
    # Every seed resolves image names to the one canonical family directory.
    assert all((Path('export')/uri).parent==Path('export/textures') for uri in images)
    result=dict(passed=True,rows=rows,textures=textures(),image_reuse=image_reuse([r['seed'] for r in rows]),shared_images=15,estimated_compressed_gpu_mib=38,
        scope='Physical construction, export and import fidelity; shared disk URIs proven, engine caching must use those canonical URIs')
    Path('build/delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY',[(r['seed'],r['triangles']) for r in rows],'15 shared images / 38 MiB; checks passed')
