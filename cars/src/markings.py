"""No markings at the body-form gate. The family pipeline reserves this entry."""
import argparse
from pathlib import Path
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float);a=p.parse_args();Path(a.out).mkdir(parents=True,exist_ok=True)
