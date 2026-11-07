"""Build absent library context into this family's ignored build directory.

Run separate Blender processes serially; source scripts remain read-only and
all outputs stay in minigolf/build/context. Existing deliveries are preferred.
"""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'minigolf/build/context';OUT.mkdir(parents=True,exist_ok=True)
cases=[('houses','build.py',['--seed','27','--out',str(OUT/'house.blend')],'house.glb'),
 ('commercial','build.py',['--seeds','101','--out',str(OUT/'station/station-101.blend')],'station/station-101.glb'),
 ('commercial','strip_build.py',['--seeds','201','--out',str(OUT/'strip'),'--no-plants'],'strip/strip-201.glb')]
for family,script,args,target in cases:
 if (OUT/target).exists():continue
 with (OUT/(family+'-'+script+'.log')).open('w') as f:
  subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(ROOT/family/'src'/script),'--',*args],cwd=ROOT/family,stdout=f,stderr=subprocess.STDOUT,check=True)
