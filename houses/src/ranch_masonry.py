"""Brick returns, rowlock sills and gauged steel angles; no extra material."""
import math

COURSE=.2032/3
BRICK_FACE=.072
FRAME_FACE=-.0254


def brick_extent(b,o):
 block=next(v for v in b.plan['blocks'] if v.name==o['block'])
 if b.plan['spec']['cladding'][block.name][o['face']]!='veneer':return None
 return block.floor+1.016-.07 if b.plan['spec']['wall_mix']=='wainscot' else block.plate-.03


def opening_masonry(b):
 for o in b.openings:
  top=brick_extent(b,o)
  if top is None or top<o['z']:continue
  block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,l=b.frame(block,o['face'])
  u,z,w,h=(o[k] for k in ('u','z','w','h'))
  me=b.mesh(o['id']+'_Masonry',component='opening_masonry',opening_id=o['id'],block=block.name,face=o['face'])
  # The shell's gauged hole already exposes the 3.8 in brick jamb returns.
  # Rowlock units have their long axis into the wall; joints are individual.
  if o['kind']=='window':
   width=w+.1524;count=math.ceil(width/COURSE);step=width/count
   for j in range(count):
    lo=u-width/2+j*step+.004;hi=lo+step-.008
    me.prism([xf((lo,-.081,z-.004)),xf((hi,-.081,z-.004)),xf((hi,.1222,z-.035)),xf((lo,.1222,z-.035))],(0,0,-1),.0889,'Veneer')
  if z+h<=top+.001:
   # 4 mm steel angle: horizontal bearing shelf and vertical back leg.
   color=(.085,.090,.075)
   me.box((u,.021,z+h+.008),(w+.3048,.112,.004),'Trim',color,r=0,xf=xf)
   me.box((u,-.033,z+h+.045),(w+.3048,.004,.075),'Trim',color,r=0,xf=xf)
  me.finish()
