"""Recover the approved local form checkpoint for reproducible fixed views.

Only our own committed source at 0b013bb is executed. Sibling asset deliveries
are read-only symlinks; all rebuilt geometry and images stay under build/.
"""
import argparse,io,subprocess,tarfile,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def main():
    a=argparse.ArgumentParser();a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a=a.parse_args()
    saved=Path('build/before-lookdev/renders/checkpoint')
    if all((saved/str(seed)/'hero.png').exists() for seed in (117,228,339)):return
    stage=Path('build/baseline-source').resolve();stage.mkdir(parents=True,exist_ok=True)
    payload=subprocess.check_output(['git','archive','0b013bb','coffee-shop'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(payload)) as archive:archive.extractall(stage,filter='data')
    for name in ('kit','downtown','commercial','patio-set','street-furniture','ground','trees','cars'):
        dst=stage/name
        if not dst.exists():dst.symlink_to(ROOT/name,target_is_directory=True)
    work=stage/'coffee-shop';(work/'build').mkdir(exist_ok=True)
    jobs=[]
    for kind in ('downtown','strip','pad'):jobs.append(['blender','-b','--factory-startup','--python-exit-code','1','--python','src/hosts.py','--','--kind',kind,'--out','build/hosts/'+kind+'.glb'])
    jobs.append(['blender','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/coffee.blend'])
    jobs.append([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--out','renders/checkpoint','--width',str(a.width),'--samples',str(a.samples),'--shots','hero,above,table,counter,awning'])
    with Path('build/baseline.log').open('w') as log:
        for cmd in jobs:subprocess.run(cmd,cwd=work,stdout=log,stderr=subprocess.STDOUT,check=True)
    saved.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(work/'renders/checkpoint',saved,dirs_exist_ok=True)

if __name__=='__main__':main()
