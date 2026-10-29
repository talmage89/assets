"""Check that diagnostic naming preserves the untouched GLB's appearance."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from final_review import sheet
BASE=Path(__file__).resolve().parents[1];out=BASE/'renders/final'
current=hashlib.sha256((BASE/'export/ak.glb').read_bytes()).hexdigest()
assert hashlib.sha256((BASE/'build/ak_raw.glb').read_bytes()).hexdigest()==current
metadata=json.loads((out/'raw-check/shots.json').read_text());rows={};pictures=[]
for name in ('hero','grip_detail','gas_muzzle','rear_sight'):
    assert metadata[name]['sha256']==current
    a=np.asarray(Image.open(out/'beauty'/(name+'.png')).convert('RGBA')).astype(float)
    b=np.asarray(Image.open(out/'raw-check'/(name+'.png')).convert('RGBA')).astype(float)
    valid=(a[:,:,3]>250)|(b[:,:,3]>250);diff=np.abs(a[:,:,:3]-b[:,:,:3]);values=diff[valid]
    row=dict(mean_absolute_rgb=float(values.mean()),p99_absolute_rgb=float(np.percentile(values,99)),max_absolute_rgb=float(values.max()),foreground_pixels=int(valid.sum()))
    assert row['mean_absolute_rgb']<1 and row['p99_absolute_rgb']<5,(name,row)
    rows[name]=row
    Image.fromarray(np.uint8(np.clip(diff*8,0,255))).save(out/'raw-check'/(name+'-difference.png'))
    pictures.extend([(name+' / untouched import',out/'raw-check'/(name+'.png')),(name+' / naming diagnostic',out/'beauty'/(name+'.png')),(name+' / absolute RGB difference x8',out/'raw-check'/(name+'-difference.png'))])
sheet(out/'raw-check/comparison.jpg',pictures,3,(600,540))
(BASE/'build/raw-appearance.json').write_text(json.dumps(dict(passed=True,sha256=current,comparisons=rows,scope='Same GLB, cameras, studio and Cycles settings; untouched import versus attributed imported triangles. Foreground 8-bit RGB, not source-scene parity.'),indent=2))
print('RAW IMPORT APPEARANCE',rows)
