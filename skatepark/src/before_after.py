"""Same-camera evidence against the untouched archived checkpoint delivery."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]

def main():
    from render import render,views
    from photo_matches import MATCHES,LIGHT,calibrated_match
    from kit import photo_match
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['before','after'],required=True);p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=24);p.add_argument('--seed',type=int);p.add_argument('--shots',nargs='+');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    before=a.stage=='before';folder=Path('build/before/export/checkpoint' if before else 'export/lookdev')
    for seed in ([a.seed] if a.seed else (101,202,303)):
        manifest=f'build/before/build/park-{seed}.json' if before else f'build/park-{seed}.json'
        parts=json.loads(Path(manifest).read_text())['parts']
        current=json.loads(Path(f'build/park-{seed}.json').read_text())['plan'];shots=views(current)
        chosen=['above','plan']
        if current['bowl']:chosen.append('bowl_plan')
        comparisons={}
        if seed==101:
            chosen+=['bowl','stairs','edge','trees','fence']
            shots['connected_ends']=dict(location=(24,2,5),target=(13,11,1.05),lens=38,aspect=1.5);chosen+=['connected_ends']
            for name,match in MATCHES.items():
                shot=calibrated_match(name)['shot'];shot.update(LIGHT[name]);shot.pop('background',None)
                if before and shot.get('isolate'):
                    shot['isolate']=[root for root in parts if root.startswith('Stairs_5_') or root in ('UpperStreetPlaza','SkatingFlatwork')]
                comparisons[name]=shot
        selected=a.shots or chosen+list(comparisons)
        ordinary=[n for n in selected if n in chosen]
        if ordinary:render(seed,folder,Path('renders/before-after')/a.stage/str(seed),a.width,a.samples,names=ordinary,custom=shots,with_context=False,manifest=manifest)
        # Fresh imports retain the match's feature isolation without letting
        # that visibility state affect the next comparison.
        for name,shot in comparisons.items():
            if name in selected:render(seed,folder,Path('renders/before-after')/a.stage/str(seed),a.width,a.samples,names=[name],custom={name:shot},with_context=False,manifest=manifest)

if __name__=='__main__':main()
