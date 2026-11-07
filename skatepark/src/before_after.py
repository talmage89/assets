"""Same-camera evidence against the untouched archived checkpoint delivery."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]

def main():
    from render import render,views
    from photo_matches import MATCHES,LIGHT,calibrated_match
    from kit import photo_match
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['before','after'],required=True);p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=24);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    before=a.stage=='before';folder=Path('build/before/export/checkpoint' if before else 'export/lookdev')
    for seed in (101,202,303):
        current=json.loads(Path(f'build/park-{seed}.json').read_text())['plan'];shots=views(current)
        chosen=['above','plan']
        if current['bowl']:chosen.append('bowl_plan')
        if seed==101:
            chosen+=['bowl','stairs','edge','trees','fence']
            shots['connected_ends']=dict(location=(20,8,3.8),target=(9,14,1.5),lens=38,aspect=1.5);chosen+=['connected_ends']
            for name,match in MATCHES.items():
                shot=calibrated_match(name)['shot'];shot.update(LIGHT[name]);shot.pop('background',None)
                # The full scene shows precisely which geometry changed under
                # the new, frozen calibrated camera.
                shot.pop('isolate',None);shots[name]=shot;chosen.append(name)
        manifest=f'build/before/build/park-{seed}.json' if before else f'build/park-{seed}.json'
        render(seed,folder,Path('renders/before-after')/a.stage/str(seed),a.width,a.samples,names=chosen,custom=shots,with_context=False,manifest=manifest)

if __name__=='__main__':main()
