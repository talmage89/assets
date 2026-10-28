"""Freeze a review pass made only from the current exported atlas asset."""
import argparse,json,hashlib,subprocess,sys,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from final_review import sheet
p=argparse.ArgumentParser();p.add_argument('--pass',dest='name',required=True);a=p.parse_args()
out=BASE/'renders/review'/a.name;out.mkdir(parents=True,exist_ok=True)
cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/details.py'),'--','--source',str(BASE/'export/bolt.glb'),'--out',str(out/'views'),'--width','1200','--samples','32','--shots','hero,optic,wrist,bolt_open,grip,deployed,rear_cocked,aimed,crown,receiver_markings,forend_wear','--camera-file',str(BASE/'build/cameras.json')]
with (out/'render.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,cwd=BASE)
cmd[cmd.index('--out')+1]=str(out/'photos');cmd[cmd.index('--shots')+1]='right_photo,profile_right,left_photo,open_photo,wrist_photo,used_open'
with (out/'photos.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,cwd=BASE)
subprocess.run([sys.executable,str(BASE/'src/compose_pairs.py'),'--calibration',str(BASE/'build/cameras.json'),'--renders',str(out/'photos'),'--out',str(out/'pairs')],check=True,cwd=BASE)
sheet([(n,out/'views'/(n+'.png')) for n in ('hero','optic','wrist','bolt_open','grip','deployed','rear_cocked','aimed','crown','receiver_markings','forend_wear')],out/'contact-sheet.jpg',columns=3,width=1800,height=430)
for f in ('lookdev.py','final_shots.py','config.py','details.py','value_review.py'):shutil.copy2(BASE/'src'/f,out/f)
(out/'identity.json').write_text(json.dumps(dict(glb_sha256=hashlib.sha256((BASE/'export/bolt.glb').read_bytes()).hexdigest(),maps={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'textures').glob('*.png')}),indent=2))
print(out/'contact-sheet.jpg')
