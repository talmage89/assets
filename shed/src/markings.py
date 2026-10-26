"""No printed branding; required pipeline entry point."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float);a=p.parse_args();Path(a.out).mkdir(parents=True,exist_ok=True)
