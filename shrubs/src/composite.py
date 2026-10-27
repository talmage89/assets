"""Composite only original analytic cards into the 4096 Cycles wood bake."""
import argparse,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png,write_png
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
for channel in ('BaseColor','Normal','ORM'):
    name=f'T_Shrubs_{channel}.png';source=read_png(a.source/name);bake=read_png(a.out/name)
    if isinstance(source,tuple):source=source[0]
    if isinstance(bake,tuple):bake=bake[0]
    if channel=='BaseColor':
        bake=np.dstack([bake[:,:,:3],np.ones(bake.shape[:2],np.float32)])
    h,w=bake.shape[:2];mask=np.ones((h,w),bool);mask[:h//2,:w//4]=False
    bake[mask]=source[mask];write_png(a.out/name,bake,bits=16 if channel=='Normal' else 8)
