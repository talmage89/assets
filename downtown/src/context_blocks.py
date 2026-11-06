"""Build alternate-seed opposing blocks in ignored presentation data only."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build_block
from plan import PROOF,opposite_seed
for seed,region in PROOF:build_block(opposite_seed(seed,region),region,context=True)
