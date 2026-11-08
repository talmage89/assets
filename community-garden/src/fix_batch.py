"""One bounded GPU lock for the eight requested correction comparisons."""
import sys,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from render import render
from look_batch import specimens,ear_detail
import match

p=argparse.ArgumentParser();p.add_argument('--out',default='renders/delivery-pass1');p.add_argument('--samples',type=int,default=48);p.add_argument('--resume',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for seed in (117,229,341):
    names=[n for n in ('hero','turf') if not a.resume or not (Path(a.out)/str(seed)/(n+'.png')).exists()]
    if names:render(seed,Path(a.out)/str(seed),1200,a.samples,names)
species=[sp for sp in ('tomato','squash','bean','corn','marigold') if not a.resume or not (Path(a.out)/'plants'/(sp+'.png')).exists()]
if species:specimens(a.out,1200,a.samples,species)
if not a.resume or not (Path(a.out)/'plants/corn-ear.png').exists():ear_detail(Path(a.out)/'plants',1200,a.samples)
if not Path('build/delivery-before/renders/plants/corn-ear.png').exists():ear_detail('build/delivery-before/renders/plants',1200,a.samples,'build/delivery-before/export/CommunityGardenPieces.gltf')
sys.argv=['match.py','--','--out',str(Path(a.out)/'matches'),'--width','1200','--samples',str(a.samples)];match.main()
