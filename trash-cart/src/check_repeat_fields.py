"""Compare actual finalized mesh/UV/normal fields across clean-scene builds."""
import hashlib
import json
import struct
from pathlib import Path

import bpy


def fields(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    result = {}
    for ob in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        if ob.type != 'MESH' or 'asset_set' not in ob:
            continue
        me = ob.data
        me.calc_loop_triangles()
        values = {
            'positions': [tuple(v.co) for v in me.vertices],
            'triangles': [tuple(t.vertices) for t in me.loop_triangles],
            'normals': [tuple(n.vector) for n in me.corner_normals],
            'frame': [tuple(row) for row in ob.matrix_world],
            **{'uv_'+uv.name: [tuple(v.uv) for v in uv.data] for uv in me.uv_layers},
        }
        row = {}
        for name, rows in values.items():
            digest = hashlib.sha256()
            for sample in rows:
                kind = 'I' if name == 'triangles' else 'f'
                digest.update(struct.pack('<'+kind*len(sample), *sample))
            row[name] = digest.hexdigest()
        result[ob.name] = row
    return result


original = fields(Path('build/finalized.blend'))
repeat = fields(Path('build/repeat/finalized.blend'))
assert original == repeat, 'Finalized geometry, UV, normals or frames changed'
result = dict(passed=True, scope='Exact finalized position/index/UV/corner-normal/frame fields',
              parts=original)
Path('build/repeat/finalized-check.json').write_text(json.dumps(result, indent=2)+'\n')
print('Finalized repeat fields match on', len(original), 'meshes')
