"""One serial GPU-lock batch for the original shared manufacture sets."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.flat_bake import bake
from kit.image_io import read_png,write_png
import numpy as np
from textures import SETS
for name,spec in SETS.items():
 bake(Path('textures/source'),Path('textures/bake'),name,spec['coverage'],4096,8,spec['height'])
 if name=='FreewayMaintenance':
  p=Path('textures/bake')/f'T_{name}_BaseColor.png';rgb=read_png(p);alpha=read_png(Path('textures/source')/f'T_{name}_Alpha.png')[:,:,0];write_png(p,np.dstack([rgb,alpha]),bits=8)
