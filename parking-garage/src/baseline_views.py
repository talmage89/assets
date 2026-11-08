"""Freeze original exported-site cameras before adding taller core details."""
import json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from render import shots

if __name__=='__main__':
    results={}
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/sites/ParkingGarageSite-{seed}.gltf').resolve()));bpy.context.view_layer.update()
        p=json.loads(Path(f'build/garage-{seed}.json').read_text());results[str(seed)]=shots(p)
    Path('build/lookdev/baseline-cameras.json').write_text(json.dumps(results,indent=2)+'\n')
