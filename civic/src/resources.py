"""Count real exported accessor bytes per reusable module, excluding images."""
import json,struct
from pathlib import Path


def module_costs():
    d=json.loads(Path('export/CivicPieces.gltf').read_text());rows=[]
    authored={m['name']:m for m in json.loads(Path('build/modules.json').read_text())['modules']}
    for root in d['scenes'][d.get('scene',0)]['nodes']:
        node=d['nodes'][root];name=node['name'].removeprefix('Module_')
        if name not in authored:continue
        stack=[root];accessors=set();triangles=0
        while stack:
            n=d['nodes'][stack.pop()];stack.extend(n.get('children',[]))
            if 'mesh' not in n:continue
            for p in d['meshes'][n['mesh']]['primitives']:
                triangles+=d['accessors'][p['indices']]['count']//3
                accessors.add(p['indices']);accessors.update(p['attributes'].values())
        views={d['accessors'][i]['bufferView'] for i in accessors}
        row=authored[name];assert triangles==row['triangles'],name
        rows.append(dict(module=name,triangles=triangles,accessor_bytes=sum(d['bufferViews'][i]['byteLength'] for i in views),
            materials=row['materials'],shared_image_mib=row['image_gpu_mib']))
    assert len(rows)==len(authored)
    result=dict(modules=rows,scope='Actual unique bufferView byte lengths used by each exported module subtree; shared JSON/container overhead and resident PNGs excluded')
    Path('build/module-costs.json').write_text(json.dumps(result,indent=2)+'\n')
    return rows


def package_costs():
    rows=[]
    for path in sorted(Path('export').glob('*.gltf')):
        d=json.loads(path.read_text());groups={}
        def walk(index,category='static'):
            n=d['nodes'][index];category=n.get('extras',{}).get('category',category)
            category='vegetation' if category=='vegetation' else 'static'
            g=groups.setdefault(category,dict(triangles=0,views=set()))
            if 'mesh' in n:
                for p in d['meshes'][n['mesh']]['primitives']:
                    g['triangles']+=d['accessors'][p['indices']]['count']//3
                    for i in [p['indices'],*p['attributes'].values()]:g['views'].add(d['accessors'][i]['bufferView'])
            for child in n.get('children',[]):walk(child,category)
        for root in d['scenes'][d.get('scene',0)]['nodes']:walk(root)
        costs={k:dict(placed_triangles=g['triangles'],unique_accessor_bytes=sum(d['bufferViews'][i]['byteLength'] for i in g['views'])) for k,g in groups.items()}
        rows.append(dict(package=path.stem,gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,categories=costs))
    actors=[]
    for name in ('AlderS240','AlderC150'):
        path=Path('../cars/export')/(name+'.glb');payload=path.read_bytes()
        length=struct.unpack_from('<I',payload,12)[0];d=json.loads(payload[20:20+length]);views=set()
        for m in d['meshes']:
            for p in m['primitives']:
                for i in [p['indices'],*p['attributes'].values()]:views.add(d['accessors'][i]['bufferView'])
        actors.append(dict(model=name,native_glb_bytes=path.stat().st_size,unique_accessor_bytes=sum(d['bufferViews'][i]['byteLength'] for i in views)))
    result=dict(packages=rows,native_car_sources=actors,scope='Accessor bytes count shared geometry once per category; placed triangles count instances. Native car file bytes include embedded textures, shared across actors; fictional police roof upfits remain presentation geometry.')
    Path('build/package-costs.json').write_text(json.dumps(result,indent=2)+'\n')
    return rows,actors
