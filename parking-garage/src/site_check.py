"""External-resource and instancing audit; geometry rays live in check.py."""
import hashlib
import json
from pathlib import Path


def main():
    rows=[];canonical={}
    for seed in (101,202):
        path=Path(f'export/sites/ParkingGarageSite-{seed}.gltf');doc=json.loads(path.read_text())
        for b in doc['buffers']:
            f=path.parent/b['uri'];assert f.stat().st_size==b['byteLength']
        images=[]
        for im in doc.get('images',[]):
            assert 'uri' in im and not im['uri'].startswith('data:')
            f=(path.parent/im['uri']).resolve();assert f.is_file(),f
            h=hashlib.sha256(f.read_bytes()).hexdigest()
            assert canonical.setdefault(h,str(f))==str(f),('Duplicate image copies',f)
            images.append(dict(uri=im['uri'],sha256=h,bytes=f.stat().st_size))
        garage=json.loads(Path(f'build/garage-{seed}.json').read_text())
        actors=json.loads(Path(f'build/actors-{seed}.json').read_text())
        meshes=[sum(doc['accessors'][p['indices']]['count']//3 for p in m['primitives']) for m in doc['meshes']]
        expanded=sum(meshes[n['mesh']] for n in doc['nodes'] if 'mesh' in n)
        assert expanded==garage['garage_triangles']+actors['context_triangles'],(seed,expanded)
        sockets=sum(n.get('extras',{}).get('socket_kind')=='parked_car' for n in doc['nodes'])
        assert sockets==len(garage['stalls'])
        counts={category:sum(a['category']==category for a in actors['actors']) for category in ('garage','surface court','street')}
        rows.append(dict(seed=seed,images=images,expanded_triangles=expanded,unique_mesh_triangles=sum(meshes),
            car_counts=counts,car_triangles=actors['actor_triangles'],static_context_triangles=actors['context_triangles']-actors['actor_triangles'],
            stall_sockets=sockets,gltf_bytes=path.stat().st_size,bin_bytes=sum(b['byteLength'] for b in doc['buffers']),materials=len(doc['materials'])))
    Path('build/site-check.json').write_text(json.dumps(dict(sites=rows,canonical_images=len(canonical),passed=True),indent=2)+'\n')
    print('SITE RESOURCE PASS',[(r['seed'],r['unique_mesh_triangles'],r['car_counts']) for r in rows],flush=True)


if __name__=='__main__':main()
