"""CPU-only repeat of the exported native-neighborhood scene assembly."""
import sys,json
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import neighborhood
from render import context
from plan import SEEDS

for seed in SEEDS:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path(f'export/final/Garden_{seed}.gltf').resolve()))
    p=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan'];context(p)
    neighborhood.export(f'export/final/Site_{seed}.gltf',REPO)

