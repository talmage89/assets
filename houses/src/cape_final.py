"""Final Cape views import only the delivered glTF and canonical shared maps."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from cape_render import render

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=36);p.add_argument('--seeds',default='31,32,33,34,35,36');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=48);p.add_argument('--mode',choices=('views','seeds','matches','source-matches','eevee'),default='views');p.add_argument('--out',type=Path,default=Path('renders/cape/final'));p.add_argument('--shots');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=Path(f'export/HearthfieldCape-{a.seed}.gltf')
    if a.mode=='views':render(source,a.out,a.shots or 'hero,front,side,rear,back,top,roof,dormer,eave,entry,chimney,scale,foundation,concrete,peeling',a.width,a.samples)
    elif a.mode=='eevee':render(source,a.out,'hero',a.width,a.samples,engine='BLENDER_EEVEE')
    elif a.mode in ('matches','source-matches'):
        for seed,name in ((36,'cape_dormers'),(33,'cape_plain')):render(Path(f'build/cape/house-{seed}.blend' if a.mode=='source-matches' else f'export/HearthfieldCape-{seed}.gltf'),a.out,name,a.width,a.samples,camera_file=Path('build/cape/cameras.json'))
    else:
        for seed in map(int,a.seeds.split(',')):
            render(Path(f'export/HearthfieldCape-{seed}.gltf'),a.out/str(seed),'front,rear,siding'+(',hero,connector' if seed in (32,35) else '')+(',tired' if seed==32 else ''),min(a.width,1400),a.samples)
