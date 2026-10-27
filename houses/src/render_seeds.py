"""Consistent-size Cycles portraits of independently exported seeded houses."""
import argparse
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from render import render
from sweep import SEEDS

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=760);p.add_argument('--samples',type=int,default=24)
    p.add_argument('--lookdev',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    for seed in SEEDS:
        render(argparse.Namespace(source=Path(f'build/lookdev-seeds/house-{seed}.blend' if a.lookdev else f'build/seeds/house-{seed}.glb'),
            out=Path(f'renders/lookdev-seeds/{seed}' if a.lookdev else f'renders/seeds/{seed}'),
            engine='CYCLES',samples=a.samples,width=a.width,shots='hero,back' if a.lookdev else 'hero',camera_file=None))
