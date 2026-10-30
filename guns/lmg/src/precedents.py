"""Read existing accepted GLBs only; render in this asset's neutral studio."""
import argparse,subprocess,sys,os,tarfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];KIT=BASE.parents[1]/'kit'
p=argparse.ArgumentParser();p.add_argument('--width',default='1600');p.add_argument('--samples',default='64');a=p.parse_args()
for name in ('ak','smg'):
 source=BASE.parent/name/'export'/(name+'.glb')
 if not source.exists():
  # A fresh clone need not carry another gun's ignored build outputs. Stage
  # accepted main's scripts inside THIS asset's build; never write in the
  # other gun folders or worktrees.
  staging=BASE/'build/precedent-root';staging.mkdir(parents=True,exist_ok=True)
  archive=BASE/'build/precedent-main.tar'
  if not (staging/'kit').exists():
   with archive.open('wb') as stream:subprocess.run(['git','archive','--format=tar','main','kit','guns/common','guns/ak','guns/smg'],cwd=BASE.parents[1],stdout=stream,check=True)
   with tarfile.open(archive) as stream:stream.extractall(staging,filter='data')
  subprocess.run(['make','-C',str(staging/'guns'/name),'export'],check=True)
  source=staging/'guns'/name/'export'/(name+'.glb')
 subprocess.run([str(KIT/'with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),'--','--source',str(source),'--out',str(BASE/'renders/final/precedents'/name),'--width',a.width,'--samples',a.samples,'--shots',name+'_hero'],check=True)
