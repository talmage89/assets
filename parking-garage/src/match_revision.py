"""Re-measured structural landmarks, with full native-pixel residuals.

The old Harmon points joined different floor numbers. These measurements
identify the same four ceiling/column stations on two adjacent columns.
"""
import argparse,copy,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import photo_match
from kit.image_io import srgb_to_linear,linear_to_srgb
from matches import definitions
from plan import FLOOR


def definitions_revised():
    d=copy.deepcopy(definitions())
    d['precast']['neutral']=[1210,1800,1280,1900]
    d['precast']['neutral_description']='Bare concrete strip on the column, left of the red sign; assumed neutral cement paste in diffuse shade'
    origin=(d['precast']['landmarks'][0]['world'][0]+d['precast']['landmarks'][1]['world'][0])/2
    for row in d['precast']['landmarks']:row['world'][0]-=origin;row['world'][2]*=.85
    d['precast']['location'][0]-=origin;d['precast']['target'][0]-=origin
    d['precast']['title']='Precast tee, inverted-T and haunch / two flat modular bays / 2014'
    m=d['harmon'];m.update(crop=[1900,550,2900,1650],location=[-56.6304,-27,1.65],target=[-15.6304,-12.8,11],lens=105,
        title='Flat-deck column stack / eight-level, 24-station reference specimen / 2012',landmarks=[])
    for x,pixels in [(-21.9456,[(2314,847),(2318,1036),(2322,1228),(2326,1415)]),(-10.9728,[(2509,965),(2514,1138),(2520,1302),(2524,1468)])]:
        for j,pix in enumerate(pixels):m['landmarks'].append(dict(world=[x,-12.8016-.381,(5-j)*FLOOR-.76],pixel=list(pix)))
    return d


def solve():
    folder=Path('build/lookdev/matches');folder.mkdir(parents=True,exist_ok=True);results={};balance={}
    for name,row in definitions_revised().items():
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');arr=srgb_to_linear(np.asarray(im,dtype=float)/255)
        x0,y0,x1,y1=row['neutral'];median=np.median(arr[y0:y1,x0:x1],axis=(0,1));gain=np.mean(median)/median
        photo=folder/(name+'-balanced.jpg');Image.fromarray(np.rint(np.clip(linear_to_srgb(arr*gain),0,1)*255).astype('uint8')).save(photo,quality=96)
        fit=photo_match.calibrate({**row,'photo':str(photo)});fit.update(seed=row['seed'],gains_linear_rgb=gain.tolist())
        fit['source_form']=f'export/form/comparison-{name}.gltf' if name!='pleasant' else 'export/form/sites/ParkingGarageFormSite-101.gltf'
        assert fit['residual_rms_pixels']<=20,(name,fit['residual_rms_pixels'])
        results[name]=fit;balance[name]=dict(roi=row['neutral'],basis=row['neutral_description'],gain=gain.tolist(),limitation='Approximate neutral balance only; no gray card or exposure recovery.')
        print('REVISED FIT',name,fit['residual_rms_pixels'],flush=True)
    (folder/'calibration.json').write_text(json.dumps(results,indent=2)+'\n');(folder/'balance.json').write_text(json.dumps(balance,indent=2)+'\n')


if __name__=='__main__':solve()
