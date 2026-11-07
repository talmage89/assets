"""One fresh Blender process per view; serial shared lock, bounded image memory."""
import argparse,os,subprocess,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/lookdev'));p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24);p.add_argument('--seeds',default='101,202,303');p.add_argument('--export-root',default='export');p.add_argument('--no-setting',action='store_true');p.add_argument('--resume',action='store_true');p.add_argument('--shots',default='hero,above,clamp-deck,stairs,transfer,slide-entrance,slide-exit,swing-hanger,swing-hollow,arch-swing,swing-seat,bucket-seat,climber,tube-junction,rubber-wear,scale,pieces');a=p.parse_args()
site={'hero','above'};shots=a.shots.split(',');jobs=[(a.seeds.split(',')[0],s) for s in shots if s not in site]+[(seed,s) for seed in a.seeds.split(',') for s in shots if s in site]
folder=Path('build/render-logs');folder.mkdir(exist_ok=True,parents=True)
for seed,shot in jobs:
    output=a.out/(seed if shot in site else '')/(shot+'.png')
    if a.resume and output.exists():continue
    log=folder/f'{a.out.name}-{seed}-{shot}.log'
    cmd=[os.environ.get('BLENDER','src/serial_blender.sh'),'-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--out',str(a.out),'--width',str(a.width),'--samples',str(a.samples),'--seeds',seed,'--shots',shot,'--export-root',a.export_root]
    if a.no_setting:cmd.append('--no-setting')
    with log.open('w') as f:result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    print(seed,shot,result.returncode,flush=True)
    if result.returncode:raise RuntimeError(f'Render interrupted/failed: {log}, exit {result.returncode}; resume keeps completed views')
