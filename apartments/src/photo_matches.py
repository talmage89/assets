"""Measured reference-image landmarks for type/form comparisons.

These original buildings are not replicas. Residuals include genuine plan
and rhythm differences, and are reported without pretending survey accuracy.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plans import garden,row
p=garden(304);w,d=p['width'],p['depth'];b=p['base'];fh=p['floor_height'];e=b+2*fh
MATCHES={
 'used-garden':dict(asset='Building-304',photo='refs/garden-2004-balanced.jpg',title='Used 2004 garden apartment / type comparison',crop=(0,0,740,428),
  location=(-17,-26,1.68),target=(0,0,2.7),lens=36,camera_height_m=(1.68,.45),lens_bounds_mm=(25,65),
  landmarks=[dict(world=(-w/2,-d/2,b),pixel=(66,257)),dict(world=(w/2,-d/2,b),pixel=(637,240)),
             dict(world=(-w/2+.14,-d/2+.27,e+.32),pixel=(92,95)),dict(world=(w/2-.14,-d/2+.27,e+.32),pixel=(644,166)),
             dict(world=(-w/2,-d/2,b+fh),pixel=(66,179)),dict(world=(w/2,-d/2,b+fh),pixel=(640,204))]),
 'period-mansard':dict(asset='Building-304',photo='refs/mansard-1978-balanced.jpg',title='1978 mansard and open gallery / type comparison',crop=(0,0,890,365),
  location=(-22,-23,1.65),target=(0,0,2.7),lens=42,camera_height_m=(1.65,.5),lens_bounds_mm=(24,70),
  landmarks=[dict(world=(-w/2,-d/2,b),pixel=(129,271)),dict(world=(w/2,-d/2,b),pixel=(824,246)),
             dict(world=(-w/2+.14,-d/2+.27,e+.32),pixel=(103,54)),dict(world=(w/2-.14,-d/2+.27,e+.32),pixel=(828,112)),
             dict(world=(-w/2,-d/2,b+fh),pixel=(120,163)),dict(world=(w/2,-d/2,b+fh),pixel=(826,181))]),
}
r=row(403);u=r['units'][1];x=u['x'];ww=r['width'];dd=r['depth'];base=r['base']+u['z'];hh=2*r['floor_height']
MATCHES['garage-row']=dict(asset='Row-403',photo='refs/townhouses-balanced.jpg',title='2006 garage townhouse row / type comparison',crop=(170,120,1580,1020),
 location=(-37,-32,1.68),target=(0,0,3.0),lens=38,camera_height_m=(1.68,.5),lens_bounds_mm=(25,70),
 landmarks=[dict(world=(x-ww/2,u['y']-dd/2,base),pixel=(489,885)),dict(world=(x+ww/2,u['y']-dd/2,base),pixel=(737,851)),
            dict(world=(x-ww/2,u['y']-dd/2,base+hh),pixel=(488,439)),dict(world=(x+ww/2,u['y']-dd/2,base+hh),pixel=(737,524)),
            dict(world=(r['units'][2]['x']+ww*.5,r['units'][2]['y']-dd/2,r['base']+r['units'][2]['z']+hh),pixel=(947,535)),
            dict(world=(r['units'][2]['x']+ww*.5,r['units'][2]['y']-dd/2,r['base']+r['units'][2]['z']),pixel=(947,822))])
