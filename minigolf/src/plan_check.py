"""Conservative 2D green/border envelopes, independent of routing constants."""
import math
from plan import generate,center,halfwidth,local

def hull(points):
 points=sorted(set(points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 chains=[]
 for order in (points,list(reversed(points))):
  chain=[]
  for p in order:
   while len(chain)>=2 and cross(chain[-2],chain[-1],p)<=0:chain.pop()
   chain.append(p)
  chains.append(chain[:-1])
 return chains[0]+chains[1]

def envelope(h,padding=.29):
 points=[]
 for i in range(31):
  t=i/30;cx,cy=center(h,t)
  for side in (-1,1):points.append(local(h,cx+side*(halfwidth(h,t)+padding),cy)[:2])
 return hull(points)

def overlap(a,b):
 for poly in (a,b):
  for p,q in zip(poly,poly[1:]+poly[:1]):
   axis=(-(q[1]-p[1]),q[0]-p[0]);aa=[x*axis[0]+y*axis[1] for x,y in a];bb=[x*axis[0]+y*axis[1] for x,y in b]
   if max(aa)<=min(bb) or max(bb)<=min(aa):return False
 return True

def strips(h,padding=.17):
 rows=[]
 for j in range(53):
  t=j/52;cx,cy=center(h,t);cy+=(-.08 if j==0 else .08 if j==52 else 0)
  rows.append([local(h,cx+side*(halfwidth(h,t)+padding),cy)[:2] for side in (-1,1)])
 out=[[rows[j][0],rows[j+1][0],rows[j+1][1],rows[j][1]] for j in range(52)]
 if h.get('fixture') in ('castle','windmill'):
  # The broad front gatehouse ends at the buttresses; only the narrow keep
  # continues behind it. These bounds include the scaled caps and masonry.
  cx,cy=center(h,.49)
  shapes=((1.90,-1.05,.90),(.75,.90,1.75)) if h['fixture']=='castle' else ((1.64,-1.05,1.0),)
  for rx,y0,y1 in shapes:
   out.append([local(h,cx+x,cy+y)[:2] for x,y in ((-rx-padding,y0-padding),(rx+padding,y0-padding),(rx+padding,y1+padding),(-rx-padding,y1+padding))])
 return out

def validate(count=250):
 plans=[generate(seed,kind) for seed in range(count) for kind in ('classic','adventure')]+[generate(71,'classic'),generate(92,'adventure')];walk_quads=0;adventure_quads=0;radii=[]
 for p in plans:
  assert p==generate(p['seed'],p['kind'])
  assert [h['number'] for h in p['holes']]==list(range(1,19))
  boxes=[envelope(h) for h in p['holes']]
  for i in range(18):
   for j in range(i+1,18):assert not overlap(boxes[i],boxes[j]),(p['seed'],i+1,j+1)
  if p['kind']=='classic':
   from paths import lane,links,ribbon
   pieces=[strips(h) for h in p['holes']]
   edges=[hull([q for part in group for q in part]) for group in pieces]
   bounds=[(min(q[0] for q in poly),max(q[0] for q in poly),min(q[1] for q in poly),max(q[1] for q in poly)) for poly in edges]
   for line_index,line in enumerate([lane(h) for h in p['holes']]+list(links(p))):
    for segment_index,quad in enumerate(ribbon(line)):
     walk_quads+=1;lo=min(q[0] for q in quad);hi=max(q[0] for q in quad);bottom=min(q[1] for q in quad);top=max(q[1] for q in quad)
     for j,(poly,(x0,x1,y0,y1)) in enumerate(zip(edges,bounds)):
      if x1<lo or x0>hi or y1<bottom or y0>top:continue
      if overlap(quad,poly):assert not any(overlap(quad,part) for part in pieces[j]),('Classic walk crosses green/border',p['seed'],line_index,segment_index,j+1)
  else:
   from paths import adventure_links,ribbon
   for name,line,start,end,span in adventure_links(p):
    adventure_quads+=len(ribbon(line))
    if span:
     for a,b,c in zip(line,line[1:],line[2:]):
      cross=abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
      if cross>1e-12:
       radius=math.dist(a,b)*math.dist(b,c)*math.dist(a,c)/(2*cross);assert radius>1.524,('Framed approach folds inside its width',p['seed'],name,radius);radii.append(radius)
 return dict(seeds=count,kinds_per_seed=2,explicit_proof_plans=2,overlap_count=0,border_padding_m=.29,longitudinal_samples=31,classic_walk_quads_checked=walk_quads,adventure_connection_quads_checked=adventure_quads,minimum_sampled_framed_approach_radius_m=min(radii),walk_border_padding_m=.17,scope='Green/border convex envelopes plus narrow-phase boundary strips against classic walking ribbons and adventure connections, excluding soil berms; a bounded plan-space gate, not full 3D contact or arbitrary parcel packing.')
if __name__=='__main__':print(validate())
