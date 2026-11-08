"""Preserve analytic coverage beside GPU-baked RGB, without touching RGB."""
import argparse,sys
from pathlib import Path
from PIL import Image
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png


def pack(source,out):
    source=Path(source);out=Path(out);name='T_Manufactured_BaseColor.png'
    rgb=Image.open(out/name).convert('RGB');coverage=Image.open(source/'T_Manufactured_Coverage.png').convert('L')
    assert rgb.size==coverage.size
    write_png(out/name,np.dstack((np.asarray(rgb,dtype=float)/255,np.asarray(coverage,dtype=float)/255)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();pack(a.source,a.out)
