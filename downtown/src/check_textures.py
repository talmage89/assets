"""Independent delivered PNG dimensions, canonical bytes, normals and charts."""
import json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png
files=list(Path('export/textures').glob('*.png'));expected={p.name for p in Path('textures/ship').glob('*.png')}|{'T_DowntownSigns_BaseColor.png'}
assert {p.name for p in files}==expected,(len(files),expected)
rows=[]
for p in files:
 im=Image.open(p);size=im.size[0];assert im.size==(size,size)
 assert size==(1024 if 'MineralRoof' in p.name or 'Interior' in p.name else 2048)
 origin=(Path('build/signs') if 'Signs' in p.name else Path('textures/ship'))/p.name
 assert p.read_bytes()==origin.read_bytes()
 error=None
 if 'Normal' in p.name:
  a=np.asarray(im).astype(float)/255*2-1;error=float(abs(np.linalg.norm(a,axis=2)-1).max());assert error<.015,(p,error)
 rows.append(dict(image=p.name,size=size,bytes=p.stat().st_size,normal_length_error=error))
allocation=sum(Image.open(p).size[0]**2*4/3 for p in files)/2**20
assert abs(allocation-42-2/3)<.001
Path('build/texture-check.json').write_text(json.dumps(dict(passed=True,images=rows,bc_8bpp_mips_MiB=allocation,scope='Shipped sizes, exact canonical bytes, normalized normals; compression is an engine allocation estimate'),indent=2)+'\n')
print('TEXTURES PASS',len(rows),allocation,'MiB compressed with mips')
