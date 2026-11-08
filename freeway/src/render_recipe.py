"""Pure render dependency fingerprint shared by the runner and verifier."""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def digest():
 paths=[HERE/'render.py',HERE/'foliage_adapter.py',HERE/'source_compare.py',ROOT/'kit/foliage.py',ROOT/'trees/src/leaf_material.py']
 return hashlib.sha256(b'\0'.join(p.read_bytes() for p in paths)).hexdigest()
