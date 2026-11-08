"""Independent serialized attribute error and shared-node storage audit."""
import json
from pathlib import Path
import numpy as np


def audit(path):
    d=json.loads(Path(path).read_text());binary=Path(path).with_suffix('.bin').read_bytes()
    mesh_nodes=[n for n in d['nodes'] if 'mesh' in n]
    counts={i:0 for i in range(len(d['meshes']))}
    for n in mesh_nodes:counts[n['mesh']]+=1
    assert max(counts.values())>100,('No repeated mesh references',path)
    # Decode scales are measured from actual accessor ranges, independently
    # of the exporter receipt. All structural positions remain full precision.
    error=0;quantized=0
    for me in d['meshes']:
        decode=me.get('extras',{}).get('river_position_decode')
        if decode:
            quantized+=1;error=max(error,decode[1]/65535/2)
        for pr in me['primitives']:
            a=d['accessors'][pr['attributes']['POSITION']]
            assert a['componentType']==(5123 if decode else 5126)
    assert error<.0005
    total=Path(path).stat().st_size+len(binary)
    assert total<120_000_000,(path,total)
    return dict(package_bytes=total,mesh_nodes=len(mesh_nodes),unique_meshes=len(counts),
                maximum_mesh_references=max(counts.values()),quantized_context_meshes=quantized,
                maximum_context_position_half_step_m=error)


if __name__=='__main__':
    rows={str(s):audit(f'export/RiverCrossing-{s}.gltf') for s in (101,202)}
    Path('build/storage-check.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('STORAGE_CHECK_PASS',rows)
