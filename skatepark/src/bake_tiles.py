"""Locked Cycles bake for the two new shared sets; 4096 to 2048/1024."""
import sys,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.flat_bake import bake
from PIL import Image
import numpy as np
from kit.image_io import read_png,write_png
import shutil
p=argparse.ArgumentParser();p.add_argument('--reuse-trim-bake',action='store_true',help='Recover a completed trim bake after an interrupted filtering step')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for name,coverage,size in [('SkateTrim',4.,2048),('Prefab',4.8768,1024)]:
    source=Path('build/procedural')
    if name=='SkateTrim':
        # Coverage is an independent analytic mask. Bake unassociated RGB,
        # then restore that original mask before coverage-aware filtering.
        source=Path('build/flat-trim-source');source.mkdir(parents=True,exist_ok=True)
        Image.open('build/procedural/T_SkateTrim_BaseColor.png').convert('RGB').save(source/'T_SkateTrim_BaseColor.png')
        for channel in ('ORM','Height'):shutil.copyfile(Path('build/procedural')/f'T_SkateTrim_{channel}.png',source/f'T_SkateTrim_{channel}.png')
    if not (name=='SkateTrim' and a.reuse_trim_bake):
        bake(source,Path('textures/bake'),name,coverage,4096,8,height_distance=.004 if name=='SkateTrim' else .0012)
    if name=='SkateTrim':
        path=Path('textures/bake/T_SkateTrim_BaseColor.png');rgb=np.asarray(Image.open(path).convert('RGB'),dtype=np.float32)/255
        alpha=np.asarray(Image.open('build/procedural/T_SkateTrim_BaseColor.png').getchannel('A'),dtype=np.float32)/255
        write_png(path,np.dstack([rgb,alpha]))
    # The public CLI handles RGB in linear light and alpha as coverage.
    import subprocess
    subprocess.run(['python3','../kit/downsample.py','--source','textures/bake','--out','textures/ship','--asset',name,'--size',str(size)],check=True)
    Path('textures/ship/texture-report.json').replace(Path('textures/ship')/(name+'-texture-report.json'))
Path('textures/ship/.stamp').touch()
