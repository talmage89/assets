"""Serial Blender processes, one GPU-lock acquisition around each render set."""
import argparse,subprocess,sys
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('--width',default='1280');ap.add_argument('--samples',default='40');ap.add_argument('--out',default='renders/final');ap.add_argument('--seeds',default='117,228,339');ap.add_argument('--photographs',action='store_true');ap.add_argument('--shots',default='hero,above,table,counter,awning,chair,scale,site,retained,front,side,back,top,use,wear,door,eevee');a=ap.parse_args()
for seed in map(int,a.seeds.split(',')):
    subprocess.run(['blender','-b','-t','1','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--out',a.out,'--seeds',str(seed),'--width',a.width,'--samples',a.samples,'--shots',a.shots],check=True)
if a.out=='renders/final' and '228' in a.seeds.split(','):
    subprocess.run([sys.executable,'src/render_rail.py','--lock-held','--width',a.width,'--samples',a.samples],check=True)
if a.photographs:
    for folder,options in [('renders/final-matches',[]),('renders/final-source-matches',['--source-finish'])]:
        subprocess.run(['blender','-b','-t','1','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--matches','build/photo-calibration.json','--out',folder,'--width',a.width,'--samples',a.samples]+options,check=True)
