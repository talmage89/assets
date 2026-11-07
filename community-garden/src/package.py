"""Build and freshly re-import the three scene packages without using a GPU."""
import sys,argparse,json
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import neighborhood,geometry as Q
from render import RECIPE_SHA256,context
from plan import SEEDS

p=argparse.ArgumentParser();p.add_argument('--seeds',type=int,nargs='+',default=list(SEEDS));a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for seed in a.seeds:
    scene,receipt=neighborhood.prepare(seed,REPO,RECIPE_SHA256,context)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(scene.resolve()))
    measured=sum(Q.count(o) for o in bpy.context.scene.objects if not o.parent)
    assert measured==json.loads(receipt.read_text())['triangles'],'Scene import count differs'
    print('SCENE PACKAGE VERIFIED',seed,measured,flush=True)
