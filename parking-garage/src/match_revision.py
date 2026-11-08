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
    for row in d['precast']['landmarks']:row['world'][2]*=.85
    d['precast']['title']='Precast haunch / identical bearing height, deeper lower apex / 2014'
    m=d['harmon'];m.update(crop=[1980,600,2750,1620],location=[-42,-27,1.65],target=[-1,-12.8,8],lens=105,
        title='Flat-deck adjacent column stack / five-level generator specimen / 2012',landmarks=[])
    for x,pixels in [(-7.3152,[(2314,847),(2318,1036),(2322,1228),(2326,1415)]),(3.6576,[(2509,965),(2514,1138),(2520,1302),(2524,1468)])]:
        for j,pix in enumerate(pixels):m['landmarks'].append(dict(world=[x,-12.8016-.381,(4-j)*FLOOR-.76],pixel=list(pix)))
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
