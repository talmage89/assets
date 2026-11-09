"""Concrete-balanced photo controls and display-value evidence, never textures."""
import json
import argparse
from pathlib import Path
import numpy as np
from PIL import Image


def main(folder=Path('renders/checkpoint')):
    out=Path('build/value-controls');out.mkdir(parents=True,exist_ok=True);photos={}
    for name,file,box in (
        ('urban','Raisinriver.jpg',(260,466,350,477)),
        ('bank-bridge','CO_SH_8_bridge_over_Bear_Creek,_Morrison,_CO.jpg',(1500,480,1580,510))):
        im=Image.open(Path('refs')/file).convert('RGB');a=np.asarray(im,dtype=float)/255
        patch=np.asarray(im.crop(box),dtype=float)/255;med=np.median(patch.reshape(-1,3),axis=0)
        gain=np.exp(np.log(med).mean())/med;balanced=np.clip(a*gain,0,1)
        Image.fromarray(np.uint8(balanced*255)).save(out/(name+'.png'))
        photos[name]=dict(photo=file,assumed_neutral='sunlit bridge concrete',neutral_xyxy=box,
            neutral_rgb=med.tolist(),gains=gain.tolist())
    frames=[]
    for seed in (101,202):
        p=folder/str(seed)/'hero.png';a=np.asarray(Image.open(p).convert('RGB'),dtype=float)/255
        y=a@np.array([.2126,.7152,.0722]);h,w=y.shape
        roi=a[round(h*.420):round(h*.437),round(w*.43):round(w*.59)]
        frames.append(dict(seed=seed,path=str(p),display_luminance_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),
            near_clipped_pixel_fraction=float((a.max(axis=2)>.985).mean()),fascia_sample_median_rgb=np.median(roi.reshape(-1,3),axis=0).tolist()))
    Path('build/value-check.json').write_text(json.dumps(dict(photos=photos,heroes=frames),indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--folder',type=Path,default=Path('renders/checkpoint'))
    main(ap.parse_args().folder)
