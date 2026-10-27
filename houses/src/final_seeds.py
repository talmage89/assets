"""Independent delivered glTF portraits; same relative image URIs for each."""
import argparse
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from render import render
from plan import PROOF_SEEDS
p=argparse.ArgumentParser();p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)))
p.add_argument('--samples',type=int,default=48);p.add_argument('--width',type=int,default=900)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for seed in dict.fromkeys(map(int,a.seeds.split(','))):
    render(argparse.Namespace(source=Path(f'export/Hearthfield-{seed}.gltf'),out=Path(f'renders/final-seeds/{seed}'),
        width=a.width,samples=a.samples,engine='CYCLES',shots='hero,back',camera_file=None))
