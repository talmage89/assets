"""Build missing source neighbors on a fresh clone; accepted exports win.

Only generated build files are written. Existing neighbors and all accepted
export images/meshes stay untouched. No bake or portfolio render is invoked.
"""
import argparse
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import generate


def ensure(smoke=None):
    for kind,seed,export,out in (
        ('builder_colonial',27,Path('export/Hearthfield-27.gltf'),Path('build/lookdev.blend')),
        ('ranch',12,Path('export/HearthfieldRanch-12.gltf'),Path('build/ranch/house-12.blend')),
    ):
        if smoke:out=smoke/kind/'source.blend'
        elif export.exists() or out.exists():continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        raw=(smoke if smoke else Path('build/cape/context'))/kind/'form.blend'
        raw.parent.mkdir(parents=True,exist_ok=True)
        save(build(generate(seed,house_type=kind)),raw)
        if kind=='ranch':
            from ranch_lookdev import prepare
        else:
            from lookdev import prepare
        prepare(raw,out)
        assert out.exists() and out.with_suffix('.json').exists()
        print('CAPE_CONTEXT',kind,out)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--smoke',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);ensure(a.smoke)
