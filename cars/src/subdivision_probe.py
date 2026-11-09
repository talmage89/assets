"""Isolate the cars' subdivision chart from fitting, clipping and reduction.

Run in fresh Blender processes, with -t 4, from the cars directory:
  --prepare suv --out build/chart-probe/input.blend
  --source build/chart-probe/input.blend --out build/chart-probe/run-1.json
Repeat the second command with distinct receipts. Positions and topology stay
exact while native corner UVs can vary. No delivery or texture is read/written.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]
from kit import model


def digest(values):
    return hashlib.sha256(values.tobytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare', choices=('suv', 'hatch'))
    mode.add_argument('--source', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--canonical', action='store_true', help='Also hash the exact mathematical UV lattice; diagnostics only')
    a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
    a.out.parent.mkdir(parents=True, exist_ok=True)
    if a.prepare:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        body = importlib.import_module(a.prepare + '_body')
        original = model.apply

        class Prepared(Exception):
            pass

        def stop_before_final(ob):
            if any(m.name == 'Fair continuous quad sheet' for m in ob.modifiers):
                bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
                raise Prepared
            return original(ob)

        model.apply = stop_before_final
        try:
            body.master(3 if a.prepare == 'suv' else 2)
        except Prepared:
            pass
        finally:
            model.apply = original
        assert a.out.exists(), 'Final subdivision was not reached'
        return

    bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    objects = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.modifiers]
    assert len(objects) == 1 and len(objects[0].modifiers) == 1
    ob = objects[0]
    assert ob.modifiers[0].type == 'SUBSURF'
    model.apply(ob)
    me = ob.data
    vertices = np.empty(len(me.vertices) * 3, dtype=np.float32)
    loops = np.empty(len(me.loops), dtype=np.int32)
    uv = np.empty(len(me.loops) * 2, dtype=np.float32)
    me.vertices.foreach_get('co', vertices)
    me.loops.foreach_get('vertex_index', loops)
    me.uv_layers.active.data.foreach_get('uv', uv)
    report = dict(vertices=len(me.vertices), corners=len(me.loops),
                  positions_sha256=digest(vertices), topology_sha256=digest(loops),
                  native_uv_sha256=digest(uv),
                  max_uv_lattice_drift=float(np.max(np.abs(uv - np.rint(uv * 32) / 32))))
    if a.canonical:
        report['canonical_uv_sha256'] = digest(np.rint(uv * 32) / 32)
    a.out.write_text(json.dumps(report, indent=2) + '\n')
    print('SUBDIVISION_PROBE', json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
