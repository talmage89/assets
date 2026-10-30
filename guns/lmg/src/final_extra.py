"""Baked standalone studio views; shared family renderer, current texture subsets."""
import argparse,subprocess,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];KIT=BASE.parents[1]/'kit'
p=argparse.ArgumentParser();p.add_argument('--width',default='1000');p.add_argument('--samples',default='64');a=p.parse_args()
sys.path.insert(0,str(BASE/'src'))
from final_shots import SHOTS
cameras={}
for name in ('box_loaded','box_empty'):
 shot=dict(SHOTS[name]);target=shot['target'];shot['location']=[t+(v-t)*1.20 for t,v in zip(target,shot['location'])]
 cameras[name]=dict(shot=shot,crop=[0,0,1250,1000])
calibration=BASE/'build/detachable-cameras.json';calibration.write_text(json.dumps(cameras,indent=2))
for name in ('box_loaded','box_empty','cartridge','case','link'):
 subprocess.run([str(KIT/'with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),'--','--source',str(BASE/'export'/(name+'.glb')),'--out',str(BASE/'renders/final/detachables'/name),'--width',a.width,'--samples',a.samples,'--shots',name]+(['--camera-file',str(calibration)] if name in cameras else []),check=True)
