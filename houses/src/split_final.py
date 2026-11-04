"""Every final view imports the delivered glTF and canonical shared maps."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from split_render import render
from split_photo_matches import PAIR_SEEDS


def main(a):
    source=lambda seed:Path(f'export/HearthfieldSplit-{seed}.gltf')
    if a.mode=='main':
        render(source(a.seed),a.out,'hero,front,side,rear,back,top,entry,eave,veneer,garage,driveway,tired,scale,peeling,garage_half,garage_open',a.width,a.samples)
        render(source(56),a.out/'bay','bay',a.width,a.samples)
        render(source(55),a.out/'foyer','lower',a.width,a.samples)
    elif a.mode=='eevee':render(source(a.seed),a.out,'hero',a.width,a.samples,engine='BLENDER_EEVEE')
    elif a.mode=='seeds':
        for seed in map(int,a.seeds.split(',')):
            render(source(seed),a.out/str(seed),'front,rear,veneer_face'+(',siding' if seed!=54 else ''),min(a.width,1280),a.samples)
    else:
        for name,seed in PAIR_SEEDS.items():
            render(Path(f'build/split/house-{seed}.blend') if a.mode=='source-matches' else source(seed),a.out,name,a.width,a.samples,Path('build/split/cameras-look.json'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('main','seeds','matches','source-matches','eevee'),default='main');p.add_argument('--seed',type=int,default=51);p.add_argument('--seeds',default='51,52,53,54,55,56');p.add_argument('--out',type=Path,default=Path('renders/split/final'));p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
