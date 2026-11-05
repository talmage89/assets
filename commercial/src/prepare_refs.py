"""Neutral-balanced inspection copies; original photos never become asset inputs."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageOps
import numpy as np

CASES={'pa-canopy':dict(neutral=(150,1400,250,1450),description='sunlit forecourt concrete at lower left, assumed neutral gray; warm/yellow soffit rejected'),
       'ca-dispenser':dict(neutral=(1050,110,1190,180),description='light store wall behind dispenser, assumed neutral off-white'),
       'tx-store':dict(neutral=(1240,1070,1245,1150),description='exposed aluminum entry jamb, away from lettering and reflected sky; assumed neutral silver'),
       'va-store':dict(neutral=(2025,2228,2228,2329),description='sunlit gray aggregate forecourt between shadow bands, clear of oil; assumed neutral gray; native 3888px coordinates')}

def main():
 rows={}
 for name,case in CASES.items():
  path=Path('refs')/(name+'.jpg');im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');a=np.array(im,dtype=float)/255
  lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  x0,y0,x1,y1=case['neutral'];v=np.median(lin[y0:y1,x0:x1].reshape(-1,3),axis=0);g=v.mean()/v
  balanced=np.clip(lin*g,0,1);srgb=np.where(balanced<=.0031308,balanced*12.92,1.055*balanced**(1/2.4)-.055)
  out=Path('build')/(name+'-neutral.png');Image.fromarray(np.uint8(srgb*255+.5)).save(out)
  rows[name]=dict(**case,gains=g.tolist(),original_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),copy_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),size=im.size,scope='Assumed neutral, preserve mean linear exposure; no inverse albedo claim')
 Path('build/reference-balance.json').write_text(json.dumps(rows,indent=2))
 print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
