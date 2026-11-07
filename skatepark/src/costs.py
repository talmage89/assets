"""Runtime allocation receipt from serialized parks, with placed primitive draws."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image


def inspect(path):
    d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes()
    meshes=d['meshes'];nodes=[n for n in d['nodes'] if 'mesh' in n]
    parents={c:i for i,n in enumerate(d['nodes']) for c in n.get('children',[])}
    own_draws={'Skate_Trim_Burnish':0,'Skate_ConcreteWall':0}
    for i,n in enumerate(d['nodes']):
        if 'mesh' not in n:continue
        rt=i
        while rt in parents:rt=parents[rt]
        if d['nodes'][rt].get('extras',{}).get('module_kind')!='skating':continue
        for prim in meshes[n['mesh']]['primitives']:
            material=d['materials'][prim['material']]['name']
            if material in own_draws:own_draws[material]+=1
    images={str((path.parent/r['uri']).resolve()):(path.parent/r['uri']).resolve() for r in d.get('images',[])}
    return dict(gltf_bytes=path.stat().st_size,bin_bytes=len(binary),gltf_bin_bytes=path.stat().st_size+len(binary),
                unique_geometry_triangles=sum(d['accessors'][p['indices']]['count']//3 for m in meshes for p in m['primitives']),
                placed_triangles=sum(d['accessors'][p['indices']]['count']//3 for n in nodes for p in meshes[n['mesh']]['primitives']),
                material_states=len(d['materials']),wear_blend_placed_draws=own_draws['Skate_Trim_Burnish'],formed_wall_placed_draws=own_draws['Skate_ConcreteWall'],unique_mesh_primitives=sum(len(m['primitives']) for m in meshes),
                placed_primitive_draws=sum(len(meshes[n['mesh']]['primitives']) for n in nodes),
                image_files=len(images),shared_image_bytes=sum(p.stat().st_size for p in images.values()),
                compressed_full_mip_MiB=sum(Image.open(p).width*Image.open(p).height*4/3 for p in images.values())/1048576)


def main():
    out={}
    for seed in (101,202,303):
        row=inspect(Path(f'export/final/Park_{seed}.gltf'));info=json.loads(Path(f'build/park-{seed}.json').read_text())
        row['skating_triangles']=info['skating_triangles'];row['placed_wear']=info['placed_wear']
        baseline=Path('../build/skatepark-gate-before/export/final')/f'Park_{seed}.gltf'
        if baseline.exists():
            before=inspect(baseline)
            # The ignored viewing archive rebases image URIs. Recover the
            # original JSON bytes in memory and verify their original receipt,
            # so archive-only URI length never inflates the baseline cost.
            doc=json.loads(baseline.read_text());images=json.loads(baseline.with_suffix('.images.json').read_text())
            for image,original in zip(doc['images'],images):image['uri']=original['uri']
            raw=(json.dumps(doc,separators=(',',':'))+'\n').encode()
            receipt=json.loads((baseline.parents[2]/f'build/park-{seed}.json').read_text())['delivery']
            assert hashlib.sha256(raw+baseline.with_suffix('.bin').read_bytes()).hexdigest()==receipt['sha256']
            before['gltf_bytes']=len(raw);before['gltf_bin_bytes']=len(raw)+before['bin_bytes']
            row['baseline_geometry_sha256']=receipt['sha256']
            row['change_from_ed8953f']={k:row[k]-before[k] for k in ('gltf_bin_bytes','bin_bytes','placed_triangles','material_states','unique_mesh_primitives','placed_primitive_draws','wear_blend_placed_draws','formed_wall_placed_draws','compressed_full_mip_MiB')}
        out[str(seed)]=row
    Path('build/costs.json').write_text(json.dumps(out,indent=2));print(json.dumps({s:{k:v for k,v in r.items() if k!='placed_wear'} for s,r in out.items()},indent=2))
if __name__=='__main__':main()
