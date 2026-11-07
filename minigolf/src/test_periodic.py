"""Independent pixel sampling at the protected two-metre repeat boundaries."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
from textures import RECTS

def check():
 rows=[];digests={}
 for channel in ('BaseColor','Height','ORM'):
  path=Path('build/procedural')/f'T_Minigolf_{channel}.png'
  digests[channel]=hashlib.sha256(path.read_bytes()).hexdigest()
  with Image.open(path) as image:
   n=image.width
   for key in ('soil','rock','rocklight','wetrock'):
    u,v,U,V=RECTS[key];a=np.asarray(image.crop((round(u*n),round((1-V)*n),round(U*n),round((1-v)*n))),dtype=float)
    if a.ndim==2:a=a[:,:,None]
    pad=round(8*n/2048);h,w=a.shape[:2]
    # Texture sampling on the boundary averages the two adjacent texel centers.
    left=(a[pad:-pad,pad-1]+a[pad:-pad,pad])/2;right=(a[pad:-pad,w-pad-1]+a[pad:-pad,w-pad])/2
    top=(a[pad-1,pad:-pad]+a[pad,pad:-pad])/2;bottom=(a[h-pad-1,pad:-pad]+a[h-pad,pad:-pad])/2
    error=float(max(np.max(abs(left-right)),np.max(abs(top-bottom))))
    assert error<=1.01,(channel,key,error,'Protected repeat has a value seam')
    rows.append(dict(channel=channel,role=key,max_boundary_error_code_values=error,source_bits=16 if channel=='Height' else 8))
 report=dict(passed=True,source_size=n,protected_delivery_guard_texels=8,measurements=rows,source_sha256=digests,scope='Original source-field value continuity at actual protected UV boundaries; baked filtering and normal response are judged separately')
 Path('build/periodic-field-check.json').write_text(json.dumps(report,indent=2));print('PERIODIC FIELD CHECK PASS',len(rows),'map/role boundaries')

if __name__=='__main__':check()
