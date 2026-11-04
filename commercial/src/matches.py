import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import render
from kit.photo_match import verify
from photo_matches import PAIR_SEEDS,LIGHTING
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--width',type=int,default=1400);a.add_argument('--samples',type=int,default=40);a.add_argument('--calibration',type=Path,default=Path('build/look-cameras.json'));a.add_argument('--out',type=Path,default=Path('renders/look-matches'));a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 verify(a.calibration)
 for name,seed in PAIR_SEEDS.items():
  cameras=json.loads(a.calibration.read_text());cameras[name]['shot'].update(LIGHTING[name]);path=Path('build/camera-'+name+'.json');path.write_text(json.dumps({name:cameras[name]}))
  render(Path(f'export/CommercialGas-{seed}.gltf'),a.out,[name],a.width,a.samples,path)
