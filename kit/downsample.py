"""Filter BaseColor in linear light; filter normals as vectors and renormalize."""
import argparse,json
from pathlib import Path
import numpy as np
from image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
p.add_argument('--alpha-mode',choices=('coverage','independent'),default='coverage',
               help='Premultiply cutout coverage, or filter a non-coverage data mask independently')
p.add_argument('--asset',required=True);p.add_argument('--size',type=int,default=2048);a=p.parse_args()
source=Path(a.source);out=Path(a.out);report={}
for channel in ('BaseColor','Normal','ORM'):
    array=read_png(source/f'T_{a.asset}_{channel}.png');h,w,_=array.shape
    if h%a.size or w%a.size:raise ValueError('Downsampling requires an integer ratio')
    factor=h//a.size
    if channel=='BaseColor':
        rgb=srgb_to_linear(array[:,:,:3]);fallback=None
        if array.shape[2]==4 and a.alpha_mode=='coverage':
            # Coverage is linear. Filter premultiplied albedo to avoid colored
            # transparent margins contaminating retained leaf/thread texels.
            fallback=rgb.reshape(a.size,factor,a.size,factor,3).mean(axis=(1,3))
            array=np.dstack([rgb*array[:,:,3:4],array[:,:,3]])
        else:array=np.dstack([rgb,array[:,:,3]]) if array.shape[2]==4 else rgb
    elif channel=='Normal':array=array*2-1
    elif channel=='ORM':array[:,:,1]**=2
    array=array.reshape(a.size,factor,a.size,factor,array.shape[2]).mean(axis=(1,3))
    if channel=='BaseColor':
        if array.shape[2]==4 and a.alpha_mode=='coverage':
            alpha=array[:,:,3:4]
            rgb=np.where(alpha>1e-8,array[:,:,:3]/np.maximum(alpha,1e-8),fallback)
            array=np.dstack([linear_to_srgb(rgb),alpha])
        else:array[:,:,:3]=linear_to_srgb(array[:,:,:3])
    elif channel=='Normal':
        lengths=np.linalg.norm(array,axis=2,keepdims=True);array/=np.maximum(lengths,1e-8)
        array=array*.5+.5
    elif channel=='ORM':array[:,:,1]=np.sqrt(array[:,:,1])
    path=out/f'T_{a.asset}_{channel}.png';write_png(path,array)
    report[channel]=dict(size=[a.size,a.size],bytes=path.stat().st_size)
    print('DOWNSAMPLED',channel,report[channel])
(out/'texture-report.json').write_text(json.dumps(report,indent=2))
