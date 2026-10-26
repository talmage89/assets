"""Numerical reproducibility gate for two rebuilt delivery sets (RGB byte units)."""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image


def compare(reference,candidate,max_delta=2,rmse_limit=.02):
    rows=[]
    for path in sorted(Path(reference).glob('T_*.png')):
        other=Path(candidate)/path.name
        a=np.asarray(Image.open(path).convert('RGB'),dtype=np.int16);b=np.asarray(Image.open(other).convert('RGB'),dtype=np.int16)
        if a.shape!=b.shape:raise ValueError('Texture dimensions differ: '+path.name)
        delta=np.abs(a-b);maximum=int(delta.max());rmse=float(np.sqrt(np.mean(delta.astype(np.float64)**2)))
        rows.append(dict(file=path.name,max_byte_delta=maximum,rmse_bytes=rmse,changed_channels=int(np.count_nonzero(delta)),passed=maximum<=max_delta and rmse<=rmse_limit))
    if not rows:raise ValueError('No delivery textures to compare')
    return dict(passed=all(r['passed'] for r in rows),max_byte_delta_limit=max_delta,rmse_byte_limit=rmse_limit,textures=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--reference',required=True);p.add_argument('--candidate',required=True);p.add_argument('--out',required=True)
    p.add_argument('--max-byte-delta',type=int,default=2);p.add_argument('--rmse-byte-limit',type=float,default=.02)
    a=p.parse_args();result=compare(a.reference,a.candidate,a.max_byte_delta,a.rmse_byte_limit)
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(1)
