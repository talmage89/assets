"""Linear-light color, vector-normal and RMS roughness box filtering."""
import argparse
import json
from pathlib import Path
import numpy as np
try:
    from .image_io import read_png,write_png,srgb_to_linear,linear_to_srgb
except ImportError:
    from image_io import read_png,write_png,srgb_to_linear,linear_to_srgb


def filter_pixels(pixels,size,channel,alpha_mode='coverage'):
    """Filter a PBR field; colors are encoded sRGB and data channels linear.

    Alpha can be straight cutout coverage or an independent data field.
    Base/coat normals use normalized vector averages. Green is perceptual
    roughness in both ORM and Clearcoat, so it uses an RMS average.
    """
    array=np.asarray(pixels).copy();h,w,c=array.shape
    if not isinstance(size,int) or size<=0 or h%size or w%size or size>min(h,w):
        raise ValueError('Downsampling requires an integer reduction ratio')
    if alpha_mode not in ('coverage','independent'):raise ValueError('Unknown alpha filtering mode')
    fh,fw=h//size,w//size;fallback=None
    color=channel in ('BaseColor','Emission');normal=channel in ('Normal','CoatNormal')
    rough=channel in ('ORM','Clearcoat')
    if not (color or normal or rough or channel=='Transmission'):raise ValueError('Unknown PBR field')
    coverage=channel=='BaseColor' and c==4 and alpha_mode=='coverage'
    if color:
        array[:,:,:3]=srgb_to_linear(array[:,:,:3])
        if coverage:
            fallback=array[:,:,:3].reshape(size,fh,size,fw,3).mean(axis=(1,3))
            array[:,:,:3]*=array[:,:,3:4]
    elif normal:array=array*2-1
    elif rough:array[:,:,1]**=2
    array=array.reshape(size,fh,size,fw,c).mean(axis=(1,3))
    if color:
        if coverage:
            alpha=array[:,:,3:4]
            array[:,:,:3]=np.where(alpha>1e-8,array[:,:,:3]/np.maximum(alpha,1e-8),fallback)
        array[:,:,:3]=linear_to_srgb(array[:,:,:3])
    elif normal:
        length=np.linalg.norm(array,axis=2,keepdims=True)
        array/=np.maximum(length,1e-8);array[length[:,:,0]<1e-8]=(0,0,1)
        array=array*.5+.5
    elif rough:array[:,:,1]=np.sqrt(array[:,:,1])
    return array


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--alpha-mode',choices=('coverage','independent'),default='coverage',
                   help='Premultiply cutout coverage, or filter a non-coverage data mask independently')
    p.add_argument('--asset',required=True);p.add_argument('--size',type=int,default=2048);a=p.parse_args()
    source=Path(a.source);out=Path(a.out);report={}
    for channel in ('BaseColor','Normal','ORM'):
        array=filter_pixels(read_png(source/f'T_{a.asset}_{channel}.png'),a.size,channel,a.alpha_mode)
        path=out/f'T_{a.asset}_{channel}.png';write_png(path,array)
        report[channel]=dict(size=[a.size,a.size],bytes=path.stat().st_size)
        print('DOWNSAMPLED',channel,report[channel])
    (out/'texture-report.json').write_text(json.dumps(report,indent=2))


if __name__=='__main__':main()
