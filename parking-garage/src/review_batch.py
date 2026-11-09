"""One GPU-lock acquisition for a complete review set, no modeling here."""
import argparse,runpy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent


def run(script,args):
    sys.argv=[str(HERE/script),'--',*args];runpy.run_path(str(HERE/script),run_name='__main__')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',default='lookdev');p.add_argument('--pass-name',default='look-pass1');p.add_argument('--width',default='1200');p.add_argument('--samples',default='24');p.add_argument('--source-pairs',action='store_true');p.add_argument('--baselines',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.baselines:
        shots='retained_hero,retained_aisle,tower,above,entry,ramp_turn,top_deck'
        originals=[Path(f'renders/before/checkpoint/{s}/{n}.png') for s in (101,202) for n in ('hero','aisle','tower','above','entry','ramp_turn','top_deck')]
        if not all(p.exists() for p in originals):run('lookdev_render.py',['--stage','baseline','--out','renders/before/checkpoint','--shots',shots,'--width','1200','--samples','24'])
        run('lookdev_render.py',['--stage','baseline','--out','renders/before/open-lift','--shots','tower_open','--width',a.width,'--samples',a.samples])
    common=['--stage',a.stage,'--width',a.width,'--samples',a.samples]
    run('lookdev_render.py',[*common,'--out','renders/'+a.pass_name,'--shots','hero,retained_hero,above,aisle,retained_aisle,tee_detail,ramp_turn,tower,tower_landing,tower_open,entry,top_deck,plan_path'])
    run('match_render.py',[*common,'--out','renders/'+a.pass_name+'-matches'])
    if a.source_pairs:run('match_render.py',[*common,'--out','renders/'+a.pass_name+'-source-matches','--source-finish'])
