"""Maple compatibility wrapper; unchanged horizontal framing defaults."""
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_frame import frame
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();frame(a.source,a.out)
