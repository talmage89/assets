"""Source-only Cycles gate. No UV, bake or delivery publication is invoked."""
import argparse,json,sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from split_render import render
from split_photo_matches import PAIR_SEEDS


def run(a):
    root=Path('renders/split/lookdev/checkpoint')
    if a.group=='main':
        source=Path('build/split/house-51.blend')
        render(source,root,'hero,back,side,entry,eave,veneer,garage,tired,driveway,scale',a.width,a.samples)
        for seed in range(51,57):
            source=Path(f'build/split/house-{seed}.blend');out=root/'seeds'/str(seed)
            render(source,out,'front,rear,veneer_face'+(',siding' if seed!=54 else ''),min(a.width,1280),a.samples)
        render(Path('build/split/house-55.blend'),root/'details'/'55','lower',a.width,a.samples)
        render(Path('build/split/house-56.blend'),root/'details'/'56','bay',a.width,a.samples)
        render(Path('build/split/house-54.blend'),root/'details'/'54','garage',a.width,a.samples)
        render(Path('build/split/house-51.blend'),root/'comparison','types',2400,a.samples,types=True)
    elif a.group=='pairs':
        for clay in (True,False):
            for name,seed in PAIR_SEEDS.items():
                render(Path(f'build/split/house-{seed}.blend'),root/('clay' if clay else 'look'),name,a.width,a.samples,Path('build/split/cameras-look.json'),clay=clay)
    else:
        from split_value_render import CASES,render as values
        values(root/'values',list(CASES),600,a.samples)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--group',choices=('main','pairs','values'),required=True);p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run(a)
