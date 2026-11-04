"""Inspection-only photo normalization and Midwest survey crop; never textures."""
from pathlib import Path
import json
import subprocess
from PIL import Image,ImageOps
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import srgb_to_linear,linear_to_srgb


def prepare():
    root=Path('refs');rows={}
    # Neutral white-painted casing, with original color/luminance retained in
    # the report. Correct chromatic white balance only, not exposure or palette.
    for name,patch in [('cape-northeast-spring',(706,486,714,615)),('cape-midatl-leaf',(574,405,580,535)),('cape-ne-summer',(0,0,1,1))]:
        im=ImageOps.exif_transpose(Image.open(root/(name+'.jpg'))).convert('RGB');im.thumbnail((1200,1200))
        rgb=np.asarray(im)/255.;linear=srgb_to_linear(rgb)
        if name=='cape-ne-summer':
            patch=(656,345,665,384) # Entry's white-painted door stile, below lintel.
        x0,y0,x1,y1=patch;neutral=np.median(linear[y0:y1,x0:x1],axis=(0,1));gain=np.mean(neutral)/neutral
        corrected=np.clip(linear_to_srgb(linear*gain),0,1);Image.fromarray(np.uint8(np.rint(corrected*255))).save(root/(name+'-fit.jpg'),quality=97)
        rows[name]=dict(neutral='white-painted exterior casing/door stile',patch_1200px=patch,linear_median=neutral.tolist(),rgb_gain=gain.tolist(),operation='chromatic neutrality preserving mean linear RGB; no exposure fit')
    subprocess.run(['pdftoppm','-f','114','-l','114','-scale-to','1600','-jpeg',str(root/'cape-midwest-survey.pdf'),str(root/'cape-midwest')],check=True)
    Image.open(root/'cape-midwest-114.jpg').crop((342,495,895,838)).save(root/'cape-midwest-elongated.jpg',quality=97)
    subprocess.run(['pdftoppm','-f','230','-l','230','-scale-to','1600','-jpeg',str(root/'cape-midwest-survey.pdf'),str(root/'cape-midwest-postwar')],check=True)
    Image.open(root/'cape-midwest-postwar-230.jpg').crop((367,419,869,763)).save(root/'cape-midwest-summer.jpg',quality=97)
    Path('build/cape').mkdir(parents=True,exist_ok=True);Path('build/cape/photo-neutral.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':prepare()
