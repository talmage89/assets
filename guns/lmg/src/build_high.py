"""Retained dense molds and manufactured surfaces with immutable finish data."""
import argparse,json,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W
import lookdev
p=argparse.ArgumentParser();p.add_argument('--out',default='build/delivery/high.blend')
p.add_argument('--revision',help='Read this asset’s own historical lookdev from a local git revision')
p.add_argument('--omit',default='');p.add_argument('--wear',type=float,default=1)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/bake-target.blend'))
W.pose(bpy.data.objects['HarrowArmature'],None,0)
with bpy.data.libraries.load(str(BASE/'build/lmg.blend'),link=False) as (src,dst):dst.objects=[n for n in src.objects if n.startswith('HIGH_')]
for dense in dst.objects:
    target=bpy.data.objects.get(dense.get('low_target',''))
    if target:
        target.data=dense.data.copy();target.vertex_groups.clear()
        vg=target.vertex_groups.new(name=target['bone']);vg.add(list(range(len(target.data.vertices))),1,'REPLACE')
    bpy.data.objects.remove(dense,do_unlink=True)
if a.revision:
    import subprocess,types
    source=subprocess.check_output(['git','show',a.revision+':guns/lmg/src/lookdev.py'],cwd=BASE.parents[1],text=True)
    module=types.ModuleType('Historical original Harrow finish');module.__file__=str(BASE/'src/lookdev.py')
    exec(compile(source,module.__file__,'exec'),module.__dict__);lookdev=module
records=lookdev.assign(a.wear,a.omit)
records['lookdev_revision']=a.revision or 'working tree'
out=BASE/a.out;out.parent.mkdir(parents=True,exist_ok=True)
bpy.context.scene['stage']='Original dense finish source; no photographic texture inputs'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
out.with_suffix('.json').write_text(json.dumps(records,indent=2))
