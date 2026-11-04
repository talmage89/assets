"""All requested source look-dev views, with shared procedural daylight."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from cape_render import render


def main(root,width,samples):
    render(Path('build/cape/house-36.blend'),root,'hero,back,roof,dormer,eave,entry,scale,foundation,peeling',width,samples)
    for seed in range(31,37):
        render(Path(f'build/cape/house-{seed}.blend'),root/'seeds'/str(seed),'front,rear,siding'+(',hero,connector' if seed in (32,35) else '')+(',tired' if seed==32 else ''),min(width,1400),samples)
    render(Path('build/cape/house-36.blend'),root/'comparison','types',1800,samples,types=True)
    render(Path('build/cape/authored-lookdev.blend'),root/'painted_cedar','siding',min(width,1400),samples)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/cape/lookdev/checkpoint'));p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(a.out,a.width,a.samples)
