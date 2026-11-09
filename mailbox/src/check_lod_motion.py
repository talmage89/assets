"""Validate closed reduced doors, animated flags and the original interaction hold."""
import argparse
import copy
import json
import runpy
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document, digest
from kit.motion import owned, sweep

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='src/lod.json')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
cfg, family, source, output = configuration(Path(args.config))
manifest = json.loads((output/'manifest.json').read_text())
assert Document(source).dependencies() == manifest['baseline']
motions = runpy.run_path(str(Path(__file__).with_name('config.py')))['MOTIONS']
paths = [source]+[output/row['path'] for row in manifest['levels'][1:]]
rows = []
for level, path in enumerate(paths):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH']
    assert len(meshes) == 3
    assert not any(ob.get('allow_boundary', False) for ob in meshes)
    for ob in meshes:
        ob['asset_set'] = 'Mailbox'
    specs = copy.deepcopy(motions)
    for spec in specs:
        spec['allow'] = []
        assert sum(owned(ob, bpy.data.objects[spec['node']]) for ob in meshes) == 1
        if level and spec['node'] == 'Door':
            spec['range'] = [0, 0]
    result = sweep(dict(MOTIONS=specs))
    root = bpy.data.objects['Mailbox']
    before = [ob.matrix_world@v.co for ob in meshes for v in ob.data.vertices]
    rest = root.matrix_world.copy()
    root.matrix_world = Matrix.Translation(Vector((1, 0, 0)))@rest
    bpy.context.view_layer.update()
    after = [ob.matrix_world@v.co for ob in meshes for v in ob.data.vertices]
    error = max((b-a-Vector((1, 0, 0))).length for a, b in zip(before, after))
    assert error < 1e-6, 'All static and moving meshes must follow the placement root'
    root.matrix_world = rest
    result.update(level=level, path=str(path.relative_to(ROOT)), sha256=digest(path),
                  placement_error_m=error, meshes=[ob.name for ob in meshes],
                  moving_meshes_per_motion=1, fixed_meshes_per_motion=2)
    rows.append(result)
report = dict(passed=all(r['passed'] for r in rows), levels=rows,
    config_sha256=digest(Path(args.config)), script_sha256=digest(Path(__file__)),
    policy='Hold LOD0 whenever Door differs from rest; Flag may animate at every level',
    scope='Actual imported surfaces; sampled permitted poses; no contact exemptions')
(family/'build/lod-motion.json').write_text(json.dumps(report, indent=2)+'\n')
assert report['passed'], 'See build/lod-motion.json'
