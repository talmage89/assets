"""Compare independent checkpoint builds, preserving triangle orientation.

Blender's parallel triangulation can reorder identical bead triangles. All
other accessors and GLB metadata must match exactly; topology is compared as
oriented triangle sets, without tolerances or position quantization.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kit.gltf import GLB


def triangles(array):
    return sorted(min(tuple(np.roll(row, shift)) for shift in range(3))
                  for row in array.reshape(-1, 3))


def compare(reference, repeat):
    left, right = GLB(reference), GLB(repeat)
    assert left.json == right.json, (reference.name, 'metadata differs')
    indices = {p['indices'] for m in left.json['meshes'] for p in m['primitives']}
    reordered = []
    for index in range(len(left.json['accessors'])):
        a, b = left.accessor(index), right.accessor(index)
        if np.array_equal(a, b):
            continue
        assert index in indices, (reference.name, index, 'accessor differs')
        assert triangles(a) == triangles(b), (reference.name, index, 'topology differs')
        reordered.append(index)
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    return dict(passed=True, accessors=len(left.json['accessors']),
                sha256=digest(reference), repeat_sha256=digest(repeat),
                byte_identical=reference.read_bytes() == repeat.read_bytes(),
                identical_vertex_normal_skin_animation_accessors=True,
                identical_oriented_triangle_sets=True,
                reordered_index_accessors=reordered)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='build/determinism.json')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    files = {name: compare(Path('build') / name, Path('build/repeat') / name)
             for name in ('lever.glb', 'cartridge.glb', 'case.glb')}
    Path(args.out).write_text(json.dumps(dict(passed=True, files=files), indent=2))
    print('REPEAT: identical vertices, normals, oriented triangles, skin, sockets and clips')


if __name__ == '__main__':
    main()
