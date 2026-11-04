"""Fetch registered inspection images/PDFs and make neutral review crops.

Poppler rasterizes cited PDF photographs only; these images never enter the
model or finish generator. All downloaded material stays under refs/.
"""
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fetch_refs import fetch


def prepare():
    names=['split-period-plans.pdf','split-west-survey.pdf','split-midwest-survey.pdf','split-midwest-summer.jpg','split-ne-summer.jpg','split-pa-split_level_allg_5_1.jpg','split-pa-split_level_10_1.jpg','split-pa-split_entry_2_1.jpg','split-pa-split_entry_1_1.jpg']
    fetch('refs',names);out=Path('build/split/reference-pages');out.mkdir(parents=True,exist_ok=True);rows={}
    for kind,page,box,neutral in [('side',103,(1240,430,2360,985),(700,163,704,213)),('foyer',107,(60,420,1180,978),(670,120,675,250))]:
        prefix=out/kind
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','2400','-jpeg','refs/split-west-survey.pdf',str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        image=Image.open(prefix.with_name(f'{kind}-{page}.jpg')).convert('RGB').crop(box)
        rgb=np.asarray(image)/255;lin=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
        x0,y0,x1,y1=neutral;white=np.median(lin[y0:y1,x0:x1].reshape(-1,3),axis=0);gain=white.mean()/white
        linear=np.clip(lin*gain,0,1);encoded=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
        Image.fromarray(np.uint8(np.clip(encoded*255+.5,0,255))).save(f'refs/split-{kind}-fit.jpg',quality=97)
        rows[kind]=dict(pdf='refs/split-west-survey.pdf',page_one_based=page,pdf_raster_long_edge=2400,crop=box,neutral_roi=neutral,neutral='Painted white upper sash stile' if kind=='side' else 'White entry/screen-wall painted mullion',linear_rgb_gains=gain.tolist(),exposure_changed=False,photographic_date='Leaf-on summer conditions; exact capture date unknown')
    Path('build/split/reference-preparation.json').write_text(json.dumps(rows,indent=2));print('SPLIT_REFS',len(names),'registered sources; two neutral-balanced comparison crops')


if __name__=='__main__':prepare()
