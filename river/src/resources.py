"""Actual serialized mesh reuse and per-package shared image allocations."""
import hashlib
import json
from pathlib import Path
from PIL import Image
import numpy as np


def textures(value):
    found=set()
    if isinstance(value,dict):
        for key,v in value.items():
            if 'texture' in key.lower() and isinstance(v,dict) and 'index' in v:found.add(v['index'])
            else:found.update(textures(v))
    elif isinstance(value,list):
        for v in value:found.update(textures(v))
    return found


def measure(path):
    path=Path(path);d=json.loads(path.read_text());categories={};all_images={}
    for n in d['nodes']:
        if 'mesh' not in n:continue
        key=n.get('extras',{}).get('river_category','context');mi=n['mesh']
        row=categories.setdefault(key,dict(mesh_instances=0,mesh_indices=set(),placed_triangles=0,unique_triangles=0,materials=set(),images={}))
        count=sum(d['accessors'][pr['indices']]['count']//3 for pr in d['meshes'][mi]['primitives'])
        row['mesh_instances']+=1;row['placed_triangles']+=count
        if mi not in row['mesh_indices']:row['unique_triangles']+=count
        row['mesh_indices'].add(mi)
        row['materials'].update(pr['material'] for pr in d['meshes'][mi]['primitives'])
    for row in categories.values():
        accessors={ai for mi in row['mesh_indices'] for pr in d['meshes'][mi]['primitives'] for ai in [pr['indices'],*pr['attributes'].values()]}
        buffers={d['accessors'][ai]['bufferView'] for ai in accessors}
        row['geometry_buffer_bytes']=sum(d['bufferViews'][i]['byteLength'] for i in buffers)
        ids=set().union(*(textures(d['materials'][mi]) for mi in row['materials']))
        for ti in ids:
            image=d['images'][d['textures'][ti]['source']];file=path.parent/image['uri']
            digest=hashlib.sha256(file.read_bytes()).hexdigest();w,h=Image.open(file).size
            info=dict(uri=image['uri'],size=[w,h],png_bytes=file.stat().st_size,bc8_full_mips_mib=w*h*4/3/1048576)
            row['images'][digest]=info;all_images[digest]=info
        row['unique_meshes']=len(row.pop('mesh_indices'));row['material_states']=len(row.pop('materials'))
        row['shared_image_mib']=sum(v['bc8_full_mips_mib'] for v in row['images'].values())
    scene_bytes=path.stat().st_size+path.with_suffix('.bin').stat().st_size
    png_bytes=sum(v['png_bytes'] for v in all_images.values())
    return dict(categories=categories,unique_images=all_images,shared_image_mib=sum(v['bc8_full_mips_mib'] for v in all_images.values()),
                gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,
                external_png_bytes=png_bytes,standalone_copy_bytes=scene_bytes+png_bytes)


def bearing_units(path):
    """Count actual bearing triangles below the joint, then separate in Y.

    glTF Y is height and -Z is Blender transverse Y. The clear spaces between
    pad assemblies separate their measured triangle-centroid clusters.
    """
    path=Path(path);d=json.loads(path.read_text());binary=path.with_suffix('.bin').read_bytes()
    def array(index):
        a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
        typ={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];n={'SCALAR':1,'VEC3':3}[a['type']]
        return np.ndarray((a['count'],n),dtype=typ,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),
                          strides=(v.get('byteStride',np.dtype(typ).itemsize*n),np.dtype(typ).itemsize))
    node=next(n for n in d['nodes'] if n.get('name')=='BearingStation_0');centers=[];materials=set()
    plan=next(n['extras']['plan'] for n in d['nodes'] if n.get('name','').startswith('Crossing_'))
    for pr in d['meshes'][node['mesh']]['primitives']:
        pos=array(pr['attributes']['POSITION']);tri=pos[array(pr['indices']).ravel().reshape(-1,3)]
        selected=tri[(tri[:,:,1]<plan['deck_z']-1).all(axis=1)]
        if not len(selected):continue
        centers.extend((-selected[:,:,2].mean(axis=1)).tolist());materials.add(pr['material'])
    centers.sort();groups=[]
    for i,value in enumerate(centers):
        if i==0 or value-centers[i-1]>.75:groups.append(0)
        groups[-1]+=1
    assert len(set(groups))==1 and groups[0]<=2000,('Inconsistent bearing assemblies',groups)
    image_ids={d['textures'][t]['source'] for m in materials for t in textures(d['materials'][m])}
    images={}
    for i in image_ids:
        file=path.parent/d['images'][i]['uri'];w,h=Image.open(file).size
        images[hashlib.sha256(file.read_bytes()).hexdigest()]=w*h*4/3/1048576
    return dict(measured_units=len(groups),triangles_per_unit=groups[0],material_states=len(materials),
                shared_image_mib=sum(images.values()))


def main():
    files=sorted(Path('export/pieces').glob('*.gltf'))+[Path(f'export/RiverCrossing-{s}.gltf') for s in (101,202)]
    result={p.stem:measure(p) for p in files}
    for seed in (101,202):
        result[f'RiverCrossing-{seed}']['bearing_unit']=bearing_units(Path(f'export/RiverCrossing-{seed}.gltf'))
        veg=result[f'RiverCrossing-{seed}']['categories']['vegetation']
        assert veg['unique_triangles']<veg['placed_triangles']/5,('Vegetation does not share meshes',seed,veg)
    Path('build/resources.json').write_text(json.dumps(result,indent=2)+'\n')
    print('RIVER_RESOURCES',[(s,result[f'RiverCrossing-{s}']['categories']['vegetation']['mesh_instances'],result[f'RiverCrossing-{s}']['categories']['vegetation']['unique_triangles']) for s in (101,202)])


if __name__=='__main__':main()
