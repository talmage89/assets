"""Original 4K physical fields -> kit GPU flat bakes -> mixed-size PBR delivery.

No reference pixels enter this module. Each house uses the same fifteen PNGs.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from textures import SETS,fields
from kit.image_io import write_png,linear_to_srgb


def source(size):
    folder=Path('build/procedural');folder.mkdir(parents=True,exist_ok=True);report={}
    for role,(ship,coverage) in SETS.items():
        color,h,ao,rough,metal=fields(role,size,coverage)
        # Signed original meter heights are encoded to a normalized 16-bit field.
        lo=float(h.min());distance=max(.00001,float(h.max())-lo)
        dx=(np.roll(h,-1,axis=1)-np.roll(h,1,axis=1))/(2*coverage/size)
        dy=(np.roll(h,-1,axis=0)-np.roll(h,1,axis=0))/(2*coverage/size)
        normal=np.stack([-dx,dy,np.ones_like(h)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
        for channel,array in dict(BaseColor=linear_to_srgb(color),ORM=np.stack([ao,rough,metal],axis=-1),
                                  Normal=normal*.5+.5,Height=((h-lo)/distance)[:,:,None]).items():
            write_png(folder/f'T_House{role}_{channel}.png',array,bits=16 if channel in ('Normal','Height') else 8)
        report[role]=dict(height_distance_m=distance,height_offset_m=lo,coverage_m=coverage,size=size,ship_size=ship)
        print('ORIGINAL_FIELDS',role,report[role],flush=True)
    (folder/'fields.json').write_text(json.dumps(report,indent=2))


def filtered(source,out):
    out.mkdir(parents=True,exist_ok=True)
    for role,(size,coverage) in SETS.items():
        subprocess.run([sys.executable,str(HERE.parents[1]/'kit/downsample.py'),'--source',str(source),
            '--out',str(out),'--asset','House'+role,'--size',str(size)],check=True)


def bake(size,samples):
    from kit.flat_bake import bake as flat_bake
    fields=json.loads(Path('build/procedural/fields.json').read_text())
    for role,row in fields.items():
        flat_bake(Path('build/procedural'),Path('textures/bake'),'House'+role,row['coverage_m'],size,samples,row['height_distance_m'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('source','bake','filter-source','filter-ship'))
    p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=8)
    # Blender and ordinary Python both supported for their appropriate stages.
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:];a=p.parse_args(args)
    if a.stage=='source':source(a.size)
    elif a.stage=='bake':bake(a.size,a.samples)
    elif a.stage=='filter-source':filtered(Path('build/procedural'),Path('textures/source'))
    else:filtered(Path('textures/bake'),Path('textures/ship'))
