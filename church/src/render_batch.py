"""One GPU-lock acquisition per serial export review set."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from render import render_file,render_modules,shots


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/look-a'))
    p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=20)
    p.add_argument('--shots',default='hero,above,window,window_dusk');p.add_argument('--matches',action='store_true')
    p.add_argument('--source-matches',action='store_true');p.add_argument('--range',action='store_true');p.add_argument('--full',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.full:a.shots='hero,above,doors,window,window_dusk,tower,wing,sign,scale,age,north_roof';a.matches=True;a.source_matches=True;a.range=True
    for seed in (101,202):
        for name in filter(None,a.shots.split(',')):
            render_file(Path(f'export/ChurchSite-{seed}.gltf'),a.out/str(seed),name,shots(seed)[name],a.width,a.samples,'CYCLES')
    if a.matches:
        for name,data in json.loads(Path('build/matched-cameras.json').read_text()).items():
            spec=dict(data['shot']);spec.update(landmarks_world_m=data['landmarks_world_m'],expected_pixels=data['projected_pixels'],photo_size=[data['crop'][2]-data['crop'][0],data['crop'][3]-data['crop'][1]])
            render_file(Path(data['source']),Path('renders/matches') if a.full else a.out/'matches',name,spec,a.width,a.samples,'CYCLES')
            if a.source_matches:
                render_file(Path(f'build/site-{data["seed"]}.blend'),Path('renders/source-matches') if a.full else a.out/'source-matches',name,spec,a.width,a.samples,'CYCLES')
    if a.range:
        render_file(Path('export/Range.gltf'),a.out,'range',dict(location=(60,-170,90),target=(16,0,6),lens=42,ortho=166,module_studio=True),a.width,a.samples,'CYCLES')
    if a.full:
        render_modules(Path('renders/modules'),720,32,'CYCLES')
        for seed in (101,202):render_file(Path(f'export/ChurchSite-{seed}.gltf'),Path('renders/eevee')/str(seed),'hero',shots(seed)['hero'],a.width,a.samples,'BLENDER_EEVEE')


if __name__=='__main__':main()
