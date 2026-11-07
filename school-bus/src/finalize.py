"""Reuse the car's connected-chart packing and explicit subpixel chart repair."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'cars/src'),str(ROOT)]
from sedan_finalize import main
if __name__=='__main__':main()
