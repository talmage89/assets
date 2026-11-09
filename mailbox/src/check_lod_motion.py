"""Physical LOD door/flag sweeps, including the consolidated fixed shell."""
import json
import runpy
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod_io import digest
from kit.motion import owned, sweep


def run():
    config = runpy.run_path(str(Path(__file__).with_name('config.py')))
    for spec in config['MOTIONS']:
        spec['allow'] = []
    rows = []
    for level in (1, 2):
        source = Path(f'export/lod/Mailbox_LOD{level}.gltf')
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        assert len(meshes) == 3, 'Expected fixed shell, door and flag'
        # Consolidation retains provenance but does not copy asset_set onto
        # LOD_Static. Include every imported mesh in this physical audit.
        for ob in meshes:
            ob['asset_set'] = 'Mailbox'
        for spec in config['MOTIONS']:
            pivot = bpy.data.objects[spec['node']]
            assert sum(owned(ob, pivot) for ob in meshes) == 1
        result = sweep(config)
        result.update(level=level, source_sha256=digest(source),
                      meshes=[ob.name for ob in meshes],
                      fixed_meshes_per_motion=2,
                      scope='Actual imported LOD surfaces; sampled physical motion')
        rows.append(result)
    report = dict(passed=all(r['passed'] for r in rows), levels=rows)
    Path('build/lod-motion.json').write_text(json.dumps(report, indent=2) + '\n')
    assert report['passed'], 'LOD moving surfaces interfere; see build/lod-motion.json'


if __name__ == '__main__':
    run()
