"""Fetch only photographic image tiles; assemble their original pixel grid.

No model/material data. The image pyramid's declared dimensions are recorded
from the dealer's metadata in SOURCES.md. Downloaded images stay in refs/.
"""
from pathlib import Path
from io import BytesIO
import math,urllib.request,concurrent.futures
from PIL import Image
BASE=Path(__file__).resolve().parents[1]/'refs'
SIZES=[(4767,1549),(4623,1866),(1876,4679),(4252,2615),(4359,2390),(2027,4234),(1899,3454),(4047,1858)]
def fetch(i):
 out=BASE/f'plain-{i}.jpg'
 if out.exists():return
 name='6139'+('' if i==0 else '_'+str(i-1))+'.jpg'
 url='https://www.vintagedoubles.com/vd_images/zoomified/'+name
 w,h=SIZES[i];tiers=[(w,h)]
 while max(tiers[-1])>256:tiers.append(tuple(v//2 for v in tiers[-1]))
 tiers.reverse();level=len(tiers)-1
 offset=sum(math.ceil(a/256)*math.ceil(b/256) for a,b in tiers[:-1]);nx=math.ceil(w/256)
 def tile(q):
  x,y=q;group=(offset+y*nx+x)//256
  u=f'{url}/TileGroup{group}/{level}-{x}-{y}.jpg'
  for attempt in range(3):
   try:
    data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()
    return x,y,Image.open(BytesIO(data)).copy()
   except Exception:
    if attempt==2:raise
 im=Image.new('RGB',(w,h))
 with concurrent.futures.ThreadPoolExecutor(12) as pool:
  for x,y,t in pool.map(tile,[(x,y) for y in range(math.ceil(h/256)) for x in range(nx)]):im.paste(t,(x*256,y*256))
 im.save(out,quality=98,subsampling=0);print('Photograph',out.name,im.size,flush=True)
if __name__=='__main__':
 for i in range(8):fetch(i)
