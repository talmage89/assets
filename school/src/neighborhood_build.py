"""Local presentation-only adapters. Original library scripts stay read-only."""
import argparse,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('kind',choices=('houses','utility'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--house-type',default='builder_colonial');ap.add_argument('--seed',type=int,default=27);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
a.out.parent.mkdir(parents=True,exist_ok=True)
sys.path[:0]=[str(ROOT/a.kind/'src'),str(ROOT)]
bpy.ops.wm.read_factory_settings(use_empty=True)
if a.kind=='houses':
    from build import build
    from plan import load
    b=build(load(a.seed,None,a.house_type))
    bpy.ops.export_scene.gltf(filepath=str(a.out.resolve()),export_format='GLB',export_extras=True,export_animations=False)
else:
    import surfaces
    # Uniform context finishes on the native pole geometry. No source shader
    # is silently exported as if baked, and no canonical utility map changes.
    surfaces.material=lambda:None;surfaces.uv_object=lambda *args,**kw:None
    from build import parts
    parts(a.out.with_suffix('.blend'))
