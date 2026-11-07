"""One locked checkpoint batch for heroes, dusk and balanced-photo comparisons."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import render_file
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/focus'));p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=32)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for stem,shots in (('Complex-301',['hero','dusk']),('Row-403',['hero'])):
 render_file(Path('export')/(stem+'.gltf'),a.out/stem,a.width,a.samples,shots)
for key,row in json.loads(Path('build/matched-cameras.json').read_text()).items():
 render_file(Path('export')/(row['asset']+'.gltf'),a.out/'matches',a.width,a.samples,cameras={key:row['shot']})
