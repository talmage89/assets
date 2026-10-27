"""Independent source look-development for all proof seeds, no Cycles bake."""
import argparse
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from plan import PROOF_SEEDS,generate
from build import build,save
from check_mesh import source_check,delivery_check
from lookdev import prepare
from render import render


def main(a):
    rows=[]
    for seed in PROOF_SEEDS:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        source=Path(f'build/seeds/house-{seed}.blend')
        save(build(generate(seed)),source)
        row=dict(seed=seed,form=source_check(source));row['glb']=delivery_check(source)
        out=Path(f'build/lookdev-seeds/house-{seed}.blend');row['lookdev']=prepare(source,out)
        row['lookdev_surface']=source_check(out)
        if not a.no_render:
            render(argparse.Namespace(source=out,out=Path(f'renders/lookdev-seeds/{seed}'),engine='CYCLES',
                samples=a.samples,width=a.width,shots='hero,back',camera_file=None))
        rows.append(row)
    Path('build/lookdev-seeds/checks.json').write_text(json.dumps(dict(passed=True,rows=rows),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=900);p.add_argument('--samples',type=int,default=32)
    p.add_argument('--no-render',action='store_true');main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
