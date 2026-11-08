"""Small serial Cycles sets for the three native-resolution look critiques."""
import argparse,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from render import render
p=argparse.ArgumentParser();p.add_argument('--out',default='renders/look-pass1');p.add_argument('--width',type=int,default=1100);p.add_argument('--samples',type=int,default=20);p.add_argument('--matches',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for seed,names in [(101,['hero','terminal','pier_girders','sign_structure']),(202,['hero','above'])]:
 render(f'export/Freeway-{seed}.gltf',Path(a.out)/str(seed),a.width,a.samples,'CYCLES',names=names,seed=seed)
if a.matches:
 for name,row in json.loads(Path('build/cameras.json').read_text()).items():
  render(row['source'],Path(a.out)/'matches',a.width,a.samples,'CYCLES',custom={name:row['shot']})
