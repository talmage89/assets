"""Actual serialized mesh reuse and per-package shared image allocations."""
import hashlib
import json
from pathlib import Path
from PIL import Image


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
        ids=set().union(*(textures(d['materials'][mi]) for mi in row['materials']))
        for ti in ids:
            image=d['images'][d['textures'][ti]['source']];file=path.parent/image['uri']
            digest=hashlib.sha256(file.read_bytes()).hexdigest();w,h=Image.open(file).size
            info=dict(uri=image['uri'],size=[w,h],png_bytes=file.stat().st_size,bc8_full_mips_mib=w*h*4/3/1048576)
            row['images'][digest]=info;all_images[digest]=info
        row['unique_meshes']=len(row.pop('mesh_indices'));row['material_states']=len(row.pop('materials'))
        row['shared_image_mib']=sum(v['bc8_full_mips_mib'] for v in row['images'].values())
    return dict(categories=categories,unique_images=all_images,shared_image_mib=sum(v['bc8_full_mips_mib'] for v in all_images.values()),
                gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size)


def main():
    files=sorted(Path('export/pieces').glob('*.gltf'))+[Path(f'export/RiverCrossing-{s}.gltf') for s in (101,202)]
    result={p.stem:measure(p) for p in files}
    for seed in (101,202):
        veg=result[f'RiverCrossing-{seed}']['categories']['vegetation']
        assert veg['unique_triangles']<veg['placed_triangles']/5,('Vegetation does not share meshes',seed,veg)
    Path('build/resources.json').write_text(json.dumps(result,indent=2)+'\n')
    print('RIVER_RESOURCES',[(s,result[f'RiverCrossing-{s}']['categories']['vegetation']['mesh_instances'],result[f'RiverCrossing-{s}']['categories']['vegetation']['unique_triangles']) for s in (101,202)])


if __name__=='__main__':main()
