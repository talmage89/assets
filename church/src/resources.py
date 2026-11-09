"""Per-package and per-actor resident resources from actual external glTF."""
import hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from PIL import Image


def measure(path):
    d=json.loads(path.read_text());ns=d['nodes'];parents={c:i for i,n in enumerate(ns) for c in n.get('children',[])}
    triangles=Counter();materials=defaultdict(set);mesh_ids=defaultdict(set)
    for i,n in enumerate(ns):
        if 'mesh' not in n:continue
        j=i;actor='church'
        while True:
            if 'actor_kind' in ns[j].get('extras',{}):actor=ns[j]['extras']['actor_kind'];break
            if j not in parents:break
            j=parents[j]
        mesh_ids[actor].add(n['mesh'])
        for pr in d['meshes'][n['mesh']]['primitives']:
            triangles[actor]+=d['accessors'][pr['indices']]['count']//3
            if 'material' in pr:materials[actor].add(pr['material'])
    def image_refs(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k.endswith('Texture') and isinstance(v,dict) and 'index' in v:
                    yield d['textures'][v['index']]['source']
                else:yield from image_refs(v)
        elif isinstance(value,list):
            for v in value:yield from image_refs(v)
    images={}
    for i,im in enumerate(d.get('images',[])):
        p=(path.parent/im['uri']).resolve();w,h=Image.open(p).size
        images[i]=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),uri=im['uri'],size=[w,h],bytes=p.stat().st_size,mib=w*h*4/3/1024**2)
    actors={};groups={}
    for actor in triangles:
        used={ii for mi in materials[actor] for ii in image_refs(d['materials'][mi])}
        unique={images[ii]['sha256']:images[ii] for ii in used}
        groups[actor]=unique
        accessors={ai for mi in mesh_ids[actor] for pr in d['meshes'][mi]['primitives']
                   for ai in [pr['indices'],*pr['attributes'].values()]}
        views={d['accessors'][ai]['bufferView'] for ai in accessors}
        geometry_bytes=sum(d['bufferViews'][i]['byteLength'] for i in views)
        actors[actor]=dict(triangles=triangles[actor],materials=len(materials[actor]),meshes=len(mesh_ids[actor]),
                          geometry_bytes=geometry_bytes,image_bytes=sum(v['bytes'] for v in unique.values()),
                          texture_mib=sum(v['mib'] for v in unique.values()))
    unique={v['sha256']:v for v in images.values()}
    static_images={h:v for actor,group in groups.items() if actor in ('church','site','town') for h,v in group.items()}
    static=dict(triangles=sum(n for actor,n in triangles.items() if actor in ('church','site','town')),texture_mib=sum(v['mib'] for v in static_images.values()))
    return dict(triangles=sum(triangles.values()),static_without_cars_plants=static,actors=actors,texture_mib=sum(v['mib'] for v in unique.values()),image_bytes=sum(v['bytes'] for v in unique.values()),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=list(unique.values()))


def main():
    rows={str(p):measure(p) for p in sorted(Path('export').rglob('*.gltf'))}
    Path('build/resources.json').write_text(json.dumps(rows,indent=2))
    lines=['# Measured checkpoint resources','','Full-mip block-compressed estimate: 8 bits/pixel/image. Shared images counted once per row. Actor memory overlaps; do not add actor rows. Cars include native household-driveway cars. Vegetation includes native trees/shrubs and the new clipped sward.','','| Package / actor | Triangles | Resident images, MiB | glTF + BIN bytes |','| --- | ---: | ---: | ---: |']
    for name,row in rows.items():
        lines.append(f'| {name} | {row["triangles"]:,} | {row["texture_mib"]:.2f} | {row["gltf_bytes"]+row["bin_bytes"]:,} |')
        if 'ChurchSite' in name:
            static=row['static_without_cars_plants'];lines.append(f'| ↳ budgeted static union | {static["triangles"]:,} | {static["texture_mib"]:.2f} | shared |')
            for actor,value in row['actors'].items():lines.append(f'| ↳ {actor} | {value["triangles"]:,} | {value["texture_mib"]:.2f} | {value["geometry_bytes"]:,} geometry only |')
    Path('build/resources.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
