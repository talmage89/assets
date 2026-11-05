"""Neutral-balanced inspection copies. References never enter asset materials."""
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image


def prepare():
    out=Path('build/strip/references');out.mkdir(parents=True,exist_ok=True);records={}
    # Extract the brochure's own JPEG losslessly, never its page graphics,
    # site plan or tenant logos. It remains a reference-only inspection input.
    subprocess.run(['pdfimages','-f','1','-l','1','-j','refs/strip-sterling.pdf',str(out/'sterling')],check=True)
    cases={
        'commerce':dict(roi=(965,2524,1260,2559),neutral='White minivan hatch paint, excluding plate, badge, glazing and lamps; nominal neutral paint, not a gray card.'),
        'sunnyvale':dict(roi=(1000,2254,1286,2277),neutral='Sunlit gray public sidewalk, away from the yellow road paint and planting; assumed neutral concrete.'),
        'sterling':dict(roi=(450,258,464,260),neutral='White painted lower fascia trim beside the left pavilion, excluding the teal field and glazing; assumed neutral paint. Tiny JPEG ROI, not a gray card.'),
    }
    for name,row in cases.items():
        source=out/'sterling-000.jpg' if name=='sterling' else Path(f'refs/strip-{name}.jpg')
        im=Image.open(source).convert('RGB');a=np.asarray(im,dtype=float)/255
        linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
        x0,y0,x1,y1=row['roi'];neutral=np.median(linear[y0:y1,x0:x1],axis=(0,1));gains=neutral.mean()/neutral
        balanced=np.clip(linear*gains,0,1);encoded=np.where(balanced<=.0031308,balanced*12.92,1.055*balanced**(1/2.4)-.055)
        path=out/f'{name}-neutral.png';Image.fromarray(np.round(encoded*255).astype('uint8')).save(path)
        records[name]=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),balanced=str(path),roi_native_px=row['roi'],neutral=row['neutral'],linear_RGB_gains=gains.tolist(),scope='Remove an assumed photographic cast only; not reflectance, exposure or construction-date calibration.')
        if name=='sterling':records[name].update(pdf='refs/strip-sterling.pdf',pdf_sha256=hashlib.sha256(Path('refs/strip-sterling.pdf').read_bytes()).hexdigest(),page=1)
    (out/'balance.json').write_text(json.dumps(records,indent=2)+'\n')


if __name__=='__main__':prepare()
