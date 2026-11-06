"""Neutral-balance reference copies for comparison, then use kit camera fitting."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate
from photo_matches import MATCHES
out=Path('renders/reference-neutral');out.mkdir(parents=True,exist_ok=True);result={};balances={}
for name,row in MATCHES.items():
    photo=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');pixels=np.asarray(photo,dtype=float)
    patch=np.asarray(photo.crop(row['neutral']),dtype=float);rgb=np.median(patch,axis=(0,1));gains=np.mean(rgb)/rgb
    balanced=np.clip(pixels*gains,0,255).astype('uint8');dest=out/(name+'.jpg');Image.fromarray(balanced).save(dest,quality=97)
    definition={**row,'photo':str(dest)};fit=calibrate(definition);fit['presentation']=row['presentation'];result[name]=fit
    balances[name]=dict(neutral_patch=row['neutral'],assumption='Concrete is approximately neutral; uncertainty from aggregate and ambient light retained',median_rgb_before=rgb.tolist(),gains=gains.tolist(),median_rgb_after=np.median(balanced[row['neutral'][1]:row['neutral'][3],row['neutral'][0]:row['neutral'][2]],axis=(0,1)).tolist())
    print(name,'lens',fit['shot']['lens'],'RMS px',fit['residual_rms_pixels'])
Path('build/cameras.json').write_text(json.dumps(result,indent=2));Path('build/photo-balance.json').write_text(json.dumps(balances,indent=2))
