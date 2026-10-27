"""Bake the accepted native procedural fields at 4096, without reseeding them.

Native 512/1024 manufacturing fields are interpolated to 4K in their channel
spaces. This preserves the accepted fired-unit palette and roof packet table;
it does not claim newly authored 4K detail. Cycles evaluates physical relief.
"""
import argparse,json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
from ranch_fields import brick,roof,trim_orm
ROOT=Path('build/ranch/delivery')


def expand(a,size):
 # Periodic bilinear interpolation, with texel centers preserved at the seam.
 q=(np.arange(size)+.5)*a.shape[0]/size-.5;i=np.floor(q).astype(int);f=(q-i).astype('float32')
 b=a[i%len(a)]*(1-f[:,None,None])+a[(i+1)%len(a)]*f[:,None,None]
 return b[:,i%len(a)]*(1-f[None,:,None])+b[:,(i+1)%len(a)]*f[None,:,None]


def source(size):
 rows={};native=ROOT/'native';out=ROOT/'procedural';out.mkdir(parents=True,exist_ok=True)
 for kind in ('red','red_brown','buff','tan'):
  folder=native/kind;brick(folder,kind);rows['RanchBrick_'+kind]=(folder,'RanchBrick',512)
 folder=native/'roof';roof(folder);rows['RanchRoof']=(folder,'RanchRoof',1024)
 manifest={}
 for name,(folder,original,ship) in rows.items():
  meta=json.loads((folder/f'{original}-height.json').read_text())
  for channel in ('BaseColor','Normal','ORM','Height'):
   a=read_png(folder/f'T_{original}_{channel}.png')
   if a.ndim==2:a=a[:,:,None]
   if channel=='BaseColor':a=srgb_to_linear(a)
   a=expand(a,size)
   if channel=='BaseColor':a=linear_to_srgb(a)
   write_png(out/f'T_{name}_{channel}.png',np.ascontiguousarray(a),bits=16 if channel in ('Height','Normal') else 8)
  manifest[name]=dict(**meta,ship_size=ship)
 (ROOT/'fields.json').write_text(json.dumps(manifest,indent=2))
 print('RANCH_ORIGINAL_FIELDS',len(manifest),size,flush=True)


def bake(size,samples):
 from kit.flat_bake import bake as flat
 for name,row in json.loads((ROOT/'fields.json').read_text()).items():
  flat(ROOT/'procedural',Path('textures/ranch-bake'),name,row['coverage_m'][0],size,samples,row['height_distance_m'])


def filtered():
 out=Path('textures/ranch-ship');out.mkdir(parents=True,exist_ok=True)
 for name,row in json.loads((ROOT/'fields.json').read_text()).items():
  subprocess.run([sys.executable,str(HERE.parents[1]/'kit/downsample.py'),'--source','textures/ranch-bake','--out',str(out),'--asset',name,'--size',str(row['ship_size'])],check=True)
 # ORM-only trim adjustment is derived from the already baked shared trim.
 trim_orm(out,Path('textures/ship/T_HouseTrim_ORM.png'))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=('source','bake','filter'));p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=8)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 if a.stage=='source':source(a.size)
 elif a.stage=='bake':bake(a.size,a.samples)
 else:filtered()
