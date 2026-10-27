"""All ranch final views load stock glTF with its delivered shared images."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_render import render

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=12);p.add_argument('--seeds',default='11,12,13,14,15,16');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=48);p.add_argument('--mode',choices=('views','seeds','matches','eevee'),default='views');p.add_argument('--out',type=Path,default=Path('renders/ranch/final'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 source=Path(f'export/HearthfieldRanch-{a.seed}.gltf')
 if a.mode=='views':render(source,a.out,'hero,front,side,rear,back,top,roof,eave,window,entry,chimney,scale',a.width,a.samples)
 elif a.mode=='eevee':render(source,a.out,'hero',a.width,a.samples,'BLENDER_EEVEE')
 elif a.mode=='matches':render(source,a.out,'ranch_summer,ranch_brick_picture,ranch_sun_oblique,ranch_sun_1960',a.width,a.samples,camera_file=Path('build/ranch/cameras.json'))
 else:
  for seed in map(int,a.seeds.split(',')):render(Path(f'export/HearthfieldRanch-{seed}.gltf'),a.out/str(seed),'front,rear,roof',min(a.width,1200),a.samples)
  render(Path('export/HearthfieldRanch-11.gltf'),a.out/'period-11','entry,window',a.width,a.samples)
