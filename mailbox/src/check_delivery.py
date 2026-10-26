"""Physical motion of the imported GLB, distinct from serialization comparisons."""
import argparse,sys,json,runpy
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.motion import sweep
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.source).resolve()))
cfg=runpy.run_path(str(Path(__file__).with_name('config.py')))
# All three exported rigid meshes are tested. No source-part allow-list is used.
for spec in cfg['MOTIONS']:spec['allow']=[]
r=sweep(cfg);r['source']=a.source;r['scope']='sampled physical imported-GLB motion, not export/source equality';Path(a.out).write_text(json.dumps(r,indent=2));assert r['passed']
