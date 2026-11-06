"""Conservative 2D green/border envelopes, independent of routing constants."""
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

def envelope(h):
 points=[]
 for i in range(31):
  t=i/30;cx,cy=center(h,t)
  for side in (-1,1):points.append(local(h,cx+side*(halfwidth(h,t)+.29),cy)[:2])
 return hull(points)

def overlap(a,b):
 for poly in (a,b):
  for p,q in zip(poly,poly[1:]+poly[:1]):
   axis=(-(q[1]-p[1]),q[0]-p[0]);aa=[x*axis[0]+y*axis[1] for x,y in a];bb=[x*axis[0]+y*axis[1] for x,y in b]
   if max(aa)<=min(bb) or max(bb)<=min(aa):return False
 return True

def validate(count=250):
 plans=[generate(seed) for seed in range(count)]+[generate(71,'classic'),generate(92,'adventure')]
 for p in plans:
  assert p==generate(p['seed'],p['kind'])
  assert [h['number'] for h in p['holes']]==list(range(1,19))
  boxes=[envelope(h) for h in p['holes']]
  for i in range(18):
   for j in range(i+1,18):assert not overlap(boxes[i],boxes[j]),(p['seed'],i+1,j+1)
 return dict(seeds=count,explicit_proof_plans=2,overlap_count=0,border_padding_m=.29,longitudinal_samples=31,scope='Convex plan envelopes of sampled authored greens plus border allowance; proves bounded lane separation, not full 3D contact or arbitrary parcel packing.')
if __name__=='__main__':print(validate())
