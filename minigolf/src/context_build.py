"""Build absent library context into this family's ignored build directory.

Run separate Blender processes serially; source scripts remain read-only and
all outputs stay in minigolf/build/context. Existing deliveries are preferred.
"""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'minigolf/build/context';OUT.mkdir(parents=True,exist_ok=True)
cases=[('houses','build.py',['--seed','27','--out',str(OUT/'house.blend')],'house.glb'),
 ('houses','build.py',['--seed','41','--type','ranch','--out',str(OUT/'house-ranch.blend')],'house-ranch.glb'),
 ('houses','build.py',['--seed','64','--type','cape','--out',str(OUT/'house-cape.blend')],'house-cape.glb'),
 ('commercial','build.py',['--seeds','101','--out',str(OUT/'station/station-101.blend')],'station/station-101.glb'),
 ('commercial','strip_build.py',['--seeds','201','--out',str(OUT/'strip'),'--no-plants'],'strip/strip-201.glb')]
for family,script,args,target in cases:
 if (OUT/target).exists():continue
 with (OUT/(family+'-'+script+'.log')).open('w') as f:
  # All Blender work is serialized on the shared machine, including models.
  prefix=[str(ROOT/'kit/with_gpu.sh')]
  subprocess.run([*prefix,'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(ROOT/family/'src'/script),'--',*args],cwd=ROOT/family,stdout=f,stderr=subprocess.STDOUT,check=True)
for seed in (811,829):
 target=OUT/f'boxwood-{seed}/variant.glb'
 if target.exists():continue
 with (OUT/f'boxwood-{seed}.log').open('w') as f:
  subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(ROOT/'minigolf/src/context_variant.py'),'--','--seed',str(seed),'--out',str(target)],cwd=ROOT/'minigolf',stdout=f,stderr=subprocess.STDOUT,check=True)
