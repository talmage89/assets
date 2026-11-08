"""Small serial export-only critique sets under one inherited GPU lease."""
import argparse,os,subprocess,shlex,sys
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--width',default='1200');p.add_argument('--samples',default='20');p.add_argument('--blender',default='blender -t 2');a=p.parse_args()
os.fstat(9)
bp=shlex.split(a.blender)+['-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--']
shared=['--out',a.out,'--width',a.width,'--samples',a.samples]
for seed,shots in [(101,['hero','above_clean','hero_cut']),(101,['pier_girders','bearings','sign_structure']),(202,['hero','above_clean','hero_old'])]:
 subprocess.run(bp+shared+['--seeds',str(seed),'--shots']+shots,check=True,pass_fds=(9,))
for name in ['bearing_2008','traffic_2007','diamond_2002','guide_2008']:
 subprocess.run(bp+['--out',a.out+'/matches','--width',a.width,'--samples',a.samples,'--camera-file','build/cameras.json','--shots',name],check=True,pass_fds=(9,))
