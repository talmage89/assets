"""One GPU-lock acquisition for the complete final presentation.

Validate the exported material patches first, then render the required views.
Every final view imports delivered files; source scenes are comparison-only.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from split_value_render import CASES,render as values
from split_values import measure
from split_final import main as final
from split_street import main as street


def main(a):
    if a.publish:
        from split_deliver import export_house,ROOT
        rows=[export_house(int(s)) for s in a.seeds.split(',')]
        (ROOT/'delivery.json').write_text(json.dumps(dict(rows=rows),indent=2))
        (ROOT/'export.stamp').touch()
    root=Path('renders/split');names=['roof']+[n for n in CASES if n!='roof']
    values(root/'final-values',names,600,a.samples,True)
    result=measure(root/'final-values');assert result['passed'],[(n,r['relative_errors'],r['hue_relative_errors']) for n,r in result['rows'].items() if not r['passed']]
    print('SPLIT_FINAL_PATCHES 17/17 passed',flush=True)
    values(root/'source-values',names,600,a.samples,False);assert measure(root/'source-values')['passed']
    for mode,out in (('main','final'),('seeds','final-seeds'),('matches','final-matches'),('source-matches','source-matches'),('eevee','final-eevee')):
        final(SimpleNamespace(seed=a.seed,seeds=a.seeds,mode=mode,out=root/out,width=a.width,samples=a.samples))
        print('SPLIT_FINAL_GROUP',mode,'complete',flush=True)
    subprocess.run([sys.executable,str(HERE.parents[1]/'kit/photo_match.py'),'compose','--calibration','build/split/cameras-look.json','--renders',str(root/'final-matches'),'--out',str(root/'final-matches')],check=True)
    street(SimpleNamespace(width=a.width,samples=a.samples,layout_only=False))
    (root/'street/.stamp').touch()
    Path('build/split/delivery/final-batch.stamp').touch()
    print('SPLIT_FINAL_BATCH all exported presentation groups complete',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=51);p.add_argument('--seeds',default='51,52,53,54,55,56');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);p.add_argument('--publish',action='store_true');main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
