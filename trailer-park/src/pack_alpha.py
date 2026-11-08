"""Preserve analytic coverage beside GPU-baked RGB, without touching RGB."""
import argparse
from pathlib import Path
from PIL import Image


def pack(source,out):
    source=Path(source);out=Path(out);name='T_Manufactured_BaseColor.png'
    rgb=Image.open(out/name).convert('RGB');coverage=Image.open(source/'T_Manufactured_Coverage.png').convert('L')
    assert rgb.size==coverage.size
    Image.merge('RGBA',(*rgb.split(),coverage)).save(out/name)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();pack(a.source,a.out)
