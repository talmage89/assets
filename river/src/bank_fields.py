"""Prepare authored bank fields, bake at 4096 and filter the accepted 1024 set.

The height is meter-valued. Cycles derives tangent +Y normals, avoiding image
row/UV handedness ambiguity. No reference image is an input.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
from kit.downsample import filter_pixels


def prepare(base):
    from textures import generate
    work=base/'work';cpu=work/'cpu';source=work/'source';source.mkdir(parents=True,exist_ok=True)
    height=generate(cpu)
    def expand(a):
        return np.asarray(Image.fromarray(a.astype(np.float32)).resize((4096,4096),Image.Resampling.BICUBIC))
    rgb=srgb_to_linear(np.asarray(Image.open(cpu/'T_RiverBank_BaseColor.png').convert('RGB'),dtype=float)/255)
    rgb=np.stack([expand(rgb[:,:,i]) for i in range(3)],axis=2)
    write_png(source/'T_RiverBank_BaseColor.png',linear_to_srgb(np.clip(rgb,0,1)))
    orm=np.asarray(Image.open(cpu/'T_RiverBank_ORM.png'),dtype=float)/255
    write_png(source/'T_RiverBank_ORM.png',np.stack([expand(orm[:,:,i]) for i in range(3)],axis=2))
    write_png(source/'T_RiverBank_Height.png',np.clip(expand((height+.0003)/.006),0,1)[:,:,None],bits=16)
    # Identical deterministic regeneration must not invalidate the GPU bake
    # merely by touching an unchanged field's mtime.
    for folder in ('cpu','source'):
        dest=base/folder;dest.mkdir(exist_ok=True)
        for p in sorted((work/folder).glob('*.png')):
            target=dest/p.name;data=p.read_bytes()
            if not target.exists() or target.read_bytes()!=data:target.write_bytes(data)
    shutil.rmtree(work)


def bake_bank(base,out):
    from kit.flat_bake import bake
    bake(base/'source',out,'RiverBank',2.0,4096,8,height_distance=.006)


def ship(base,baked,out):
    out.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','Normal','ORM'):
        pixels=filter_pixels(read_png(baked/f'T_RiverBank_{channel}.png'),1024,channel)
        write_png(out/f'T_RiverBank_{channel}.png',pixels)
    for name in ('T_RiverPlants_BaseColor.png','T_RiverWater_Normal.png'):
        shutil.copy2(base/'cpu'/name,out/name)


def compare(original,repeated):
    rows=[]
    for p in sorted(original.glob('*.png')):
        a=np.asarray(Image.open(p),dtype=float)/255;b=np.asarray(Image.open(repeated/p.name),dtype=float)/255
        assert a.shape==b.shape
        delta=abs(a-b)*255
        row=dict(image=p.name,maximum_byte_error=float(delta.max()),rms_byte_error=float(np.sqrt((delta*delta).mean())))
        if p.name.startswith(('T_RiverPlants','T_RiverWater')):assert p.read_bytes()==(repeated/p.name).read_bytes()
        assert row['maximum_byte_error']<=1.001 and row['rms_byte_error']<.02,row
        rows.append(row)
    assert len(rows)==5
    Path('build/texture-repeat.json').write_text(json.dumps(dict(passed=True,independent_4096_gpu_bake=True,images=rows),indent=2)+'\n')
    print('BANK_TEXTURE_REPEAT_PASS',rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('prepare','bake','ship','compare'))
    ap.add_argument('--base',type=Path,default=Path('build/bank-fields'));ap.add_argument('--baked',type=Path,default=Path('textures/baked'))
    ap.add_argument('--out',type=Path,default=Path('textures/checkpoint'));ap.add_argument('--repeated',type=Path)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    if a.mode=='prepare':prepare(a.base)
    elif a.mode=='bake':bake_bank(a.base,a.baked)
    elif a.mode=='ship':ship(a.base,a.baked,a.out)
    else:compare(a.out,a.repeated)


if __name__=='__main__':main()
