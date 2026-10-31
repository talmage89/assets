"""Audit the unchanged GLB without diagnostic per-part separation."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
BASE=Path(__file__).resolve().parents[1];KIT=BASE.parents[1]/'kit'
p=argparse.ArgumentParser();p.add_argument('--samples',default='64');a=p.parse_args()
source=BASE/'export/lmg.glb';copy=BASE/'build/lmg_raw.glb';shutil.copyfile(source,copy)
assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(copy.read_bytes()).hexdigest()
out=BASE/'renders/final/raw-check'
subprocess.run([str(KIT/'with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),'--','--source',str(copy),'--out',str(out),'--width','1600','--samples',a.samples,'--shots','hero,handguard,barrel_handle,belt'],check=True)
records={}
for name in ('hero','handguard','barrel_handle','belt'):
 aa=np.asarray(Image.open(BASE/'renders/final/beauty'/(name+'.png')).convert('RGB'),float)
 bb=np.asarray(Image.open(out/(name+'.png')).convert('RGB'),float);delta=abs(aa-bb)
 mask=np.any(abs(aa-aa[0,0])>2,axis=2)
 records[name]=dict(mean_absolute_rgb=float(delta[mask].mean()),rmse=float(np.sqrt((delta[mask]**2).mean())),maximum_rgb=float(delta[mask].max()),pixels_over_4=int(np.any(delta>4,axis=2)[mask].sum()))
(out/'raw-comparison.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),comparisons=records),indent=2))
print('RAW GLB COMPARISON',records,flush=True)
