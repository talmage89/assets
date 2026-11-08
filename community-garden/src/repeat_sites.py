"""CPU-only repeat of the exported native-neighborhood scene assembly."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import neighborhood
from render import context,CONTEXT_SHA256
from plan import SEEDS

for seed in SEEDS:
    # Invalidate only the package receipt, so the actual packaging path rebuilds
    # all scene data and metadata instead of comparing an untouched receipt.
    Path(f'build/context/site-{seed}.json').unlink(missing_ok=True)
    neighborhood.prepare(seed,REPO,CONTEXT_SHA256,context)

