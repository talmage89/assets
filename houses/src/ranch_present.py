"""Requested checkpoint views, six distinct sources, and same-scale types."""
import argparse
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_render import render

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=12);p.add_argument('--seeds',default='11,12,13,14,15,16');p.add_argument('--out',type=Path,default=Path('renders/ranch/checkpoint'));p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=48)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(f'build/ranch/house-{a.seed}.blend')
 render(source,a.out,'hero,back,roof,eave,window,entry,chimney,scale',a.width,a.samples)
 for seed in map(int,a.seeds.split(',')):render(Path(f'build/ranch/house-{seed}.blend'),a.out/'seeds'/str(seed),'front,rear,roof',min(1200,a.width),a.samples)

 render(Path('build/ranch/house-11.blend'),a.out/'period-11','entry,window',a.width,a.samples)
