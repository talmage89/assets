"""Baked standalone studio views; shared family renderer, current texture subsets."""
import argparse,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];KIT=BASE.parents[1]/'kit'
p=argparse.ArgumentParser();p.add_argument('--width',default='1000');p.add_argument('--samples',default='64');a=p.parse_args()
subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/detachable_cameras.py')],check=True)
calibration=BASE/'build/detachable-cameras.json'
for name in ('box_loaded','box_empty','cartridge','case','link'):
 subprocess.run([str(KIT/'with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),'--','--source',str(BASE/'export'/(name+'.glb')),'--out',str(BASE/'renders/final/detachables'/name),'--width',a.width,'--samples',a.samples,'--shots',name]+['--camera-file',str(calibration)],check=True)
