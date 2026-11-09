"""Sweep actual imported near LOD surfaces, including the consolidated shell."""
import argparse
import json
import runpy
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod import configuration
from kit.lod_io import digest
from kit.motion import owned, sweep

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='src/lod.json')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
_, family, source, output = configuration(Path(args.config))
manifest = json.loads((output / 'manifest.json').read_text())
config = runpy.run_path(str(Path(__file__).with_name('config.py')))
for spec in config['MOTIONS']:
    spec['allow'] = []
paths = [source] + [output / row['path'] for row in manifest['levels'][1:]
                    if not row.get('proxy') and not row.get('impostor')]
rows = []
for path in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH']
    assert len(meshes) == 4, 'Expected shell, lid and two folding handles'
    assert not any(ob.get('allow_boundary', False) for ob in meshes)
    # LOD_Static retains provenance but does not inherit asset_set. Include
    # every actual surface rather than silently losing the fixed shell.
    for ob in meshes:
        ob['asset_set'] = 'MetalTrashCan'
    counts = []
    for spec in config['MOTIONS']:
        moving = sum(owned(ob, bpy.data.objects[spec['node']]) for ob in meshes)
        assert moving == 1
        counts.append(dict(node=spec['node'], moving=moving, fixed=len(meshes)-moving))
    result = sweep(config)
    result.update(path=str(path.relative_to(ROOT)), sha256=digest(path),
                  mesh_counts=counts, meshes=[ob.name for ob in meshes])
    rows.append(result)
report = dict(passed=all(row['passed'] for row in rows), levels=rows,
              config_sha256=digest(Path(args.config)),
              scope='Sampled physical imported source/near-LOD motion; no bearing exemptions')
(family / 'build/lod-motion.json').write_text(json.dumps(report, indent=2) + '\n')
assert report['passed'], 'Physical LOD motion failed; see build/lod-motion.json'
