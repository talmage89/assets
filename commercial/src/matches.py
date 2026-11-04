import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import render
from kit.photo_match import verify
from photo_matches import PAIR_SEEDS,LIGHTING
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=32);a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 verify('build/cameras.json')
 for name,seed in PAIR_SEEDS.items():
  cameras=json.loads(Path('build/cameras.json').read_text());cameras[name]['shot'].update(LIGHTING[name]);path=Path('build/camera-'+name+'.json');path.write_text(json.dumps({name:cameras[name]}))
  render(Path(f'build/station-{seed}.glb'),Path('renders/matches'),[name],a.width,a.samples,path)
