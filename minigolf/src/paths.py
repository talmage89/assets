"""Original connected classic-course route and its compact paved outline."""
import math,functools
from plan import center,halfwidth,local

def offset(h,t):
 base=max(halfwidth(h,j/52) for j in range(53))+1.05
 clearance={'castle':3.30,'windmill':2.85}.get(h.get('fixture'),base);spread=.40 if h.get('fixture') in ('castle','windmill') else .32
 return base+max(0,clearance-base)*math.exp(-((t-.49)/spread)**4)
def side(h):
 # The upper inner lanes pass outside the quarry formations.
 return 1 if h.get('organic') and h['number'] in (13,14,16,17) else -1
def lane(h,n=27):
 return [local(h,center(h,t)[0]+side(h)*offset(h,t),center(h,t)[1])[:2] for t in (j/(n-1) for j in range(n))]
def forward(h):
 a=math.radians(h['yaw']);return (-math.sin(a),math.cos(a))
def curve(a,b,c,d,n=25):
 return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in (0,1)) for t in (j/(n-1) for j in range(n))]
def links(p):
 key=tuple((h['number'],*h['origin'],h['yaw'],h['length'],h['width'],h['bend'],h['organic'],h['fixture']) for h in p['holes'])
 return _links(key)

@functools.lru_cache(maxsize=512)
def _links(key):
 from plan_check import strips,overlap
 holes=[dict(number=q[0],origin=q[1:3],yaw=q[3],length=q[4],width=q[5],bend=q[6],organic=q[7],fixture=q[8]) for q in key];out=[]
 obstacles=[part for h in holes for part in strips(h)];grid={};boxes=[]
 for i,poly in enumerate(obstacles):
  box=(min(q[0] for q in poly),max(q[0] for q in poly),min(q[1] for q in poly),max(q[1] for q in poly));boxes.append(box)
  for x in range(math.floor(box[0]/2),math.floor(box[1]/2)+1):
   for y in range(math.floor(box[2]/2),math.floor(box[3]/2)+1):grid.setdefault((x,y),[]).append(i)
 def clear(line):
  for quad in ribbon(line):
   if any(not(-23.4<q[0]<23.4 and -13<q[1]<27) for q in quad):return False
   lo,hi=min(q[0] for q in quad),max(q[0] for q in quad);bottom,top=min(q[1] for q in quad),max(q[1] for q in quad);near=set()
   for x in range(math.floor(lo/2),math.floor(hi/2)+1):
    for y in range(math.floor(bottom/2),math.floor(top/2)+1):near.update(grid.get((x,y),()))
   for i in near:
    x0,x1,y0,y1=boxes[i]
    if x1<lo or x0>hi or y1<bottom or y0>top:continue
    if overlap(quad,obstacles[i]):return False
  return True
 def choose(candidates,label):
  for line in candidates:
   if clear(line):return tuple(line)
  raise ValueError('No clear bounded classic route: '+label)
 for prev,nxt in zip(holes,holes[1:]):
  a=lane(prev)[-1];d=lane(nxt)[0];fa,fb=forward(prev),forward(nxt);opposed=sum(fa[k]*fb[k] for k in (0,1))<0;candidates=[]
  for handle in ((2.4,3.2,4,5,6) if opposed else (.9,1.3,2,2.8,3.5)):
   candidates.append(curve(a,tuple(a[k]+fa[k]*handle for k in (0,1)),tuple(d[k]-fb[k]*handle for k in (0,1)),d))
  if not opposed:
   oa=(-fa[1],fa[0]);ob=(-fb[1],fb[0]);travel=((d[0]-a[0])/max(.01,math.dist(a,d)),(d[1]-a[1])/max(.01,math.dist(a,d)))
   # A long neighboring green can occupy the forward tangent's extension.
   # Turn outward early, then return along the next green's outside bank.
   for bow in (.6,1,1.5,2,2.5,3):
    candidates.append(curve(a,tuple(a[k]+fa[k]*.25+oa[k]*bow for k in (0,1)),tuple(d[k]-fb[k]*.25+ob[k]*bow for k in (0,1)),d))
   for bow in (.6,1.0,1.5,2,2.5):
    mid=tuple((a[k]+d[k])/2+(oa[k]+ob[k])*bow/2 for k in (0,1));span=math.dist(a,d)*.22
    left=curve(a,tuple(a[k]+fa[k]*.8 for k in (0,1)),tuple(mid[k]-travel[k]*span for k in (0,1)),mid,13)
    right=curve(mid,tuple(mid[k]+travel[k]*span for k in (0,1)),tuple(d[k]-fb[k]*.8 for k in (0,1)),d,13)
    candidates.append(left[:-1]+right)
  out.append(choose(candidates,str(prev['number'])+' to '+str(nxt['number'])))
 entry=(0,-12);d=lane(holes[0])[0];fd=forward(holes[0]);out.append(choose((curve(entry,(-2,-12),tuple(d[k]-fd[k]*handle for k in (0,1)),d) for handle in (4.5,5,5.5,6)),'entry'))
 a=lane(holes[-1])[-1];fa=forward(holes[-1]);out.append(choose((curve(a,tuple(a[k]+fa[k]*handle for k in (0,1)),(2,-12),entry) for handle in (4.5,5,5.5,6)),'exit'))
 return tuple(out)
def ribbon(points,width=1.524):
 vs=[]
 for i,p in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
  for side in (-1,1):vs.append((p[0]-side*dy/length*width/2,p[1]+side*dx/length*width/2))
 return [[vs[2*i],vs[2*i+2],vs[2*i+3],vs[2*i+1]] for i in range(len(points)-1)]
def court(p):
 from plan_check import hull
 points=[]
 for h in p['holes']:
  for j in range(17):
   t=j/16;cx,cy=center(h,t)
   for side in (-1,1):points.append(local(h,cx+side*(halfwidth(h,t)+.45),cy)[:2])
 for line in [lane(h) for h in p['holes']]+list(links(p)):
  for quad in ribbon(line,2.05):points.extend(quad)
 return hull(points)

def adventure_links(p):
 """Connected inner sequence, with framed approaches to the upper crossing.

 The outer twelve lanes already share the circuit. The upper lane branches
 join that circuit at both ends, rather than stopping in planted beds.
 Each tuple is (label, XY stations, start hole/t, end hole/t, framed deck).
 """
 from plan_check import strips,overlap
 h={q['number']:q for q in p['holes']};out=[];obstacles=[]
 for hole in h.values():
  for poly in strips(hole):obstacles.append((poly,(min(q[0] for q in poly),max(q[0] for q in poly),min(q[1] for q in poly),max(q[1] for q in poly))))
 def clear(line):
  for quad in ribbon(line):
   lo,hi=min(q[0] for q in quad),max(q[0] for q in quad);bottom,top=min(q[1] for q in quad),max(q[1] for q in quad)
   for poly,(x0,x1,y0,y1) in obstacles:
    if x1<lo or x0>hi or y1<bottom or y0>top:continue
    if overlap(quad,poly):return False
  return True
 def add(label,a,b,c,d,start,end,span=False):
  for scale in (1,1.5,2,3,.7,4):
   line=curve(a,tuple(a[k]+(b[k]-a[k])*scale for k in (0,1)),tuple(d[k]+(c[k]-d[k])*scale for k in (0,1)),d,17)
   if clear(line):out.append((label,line,start,end,span));return
  raise ValueError(('Adventure connection crosses a green',p['seed'],label))
 a=lane(h[13])[0];y=7+14.85*math.sqrt(max(0,1-(a[0]/17.25)**2));d=(a[0],y)
 add('Northwest circuit branch',d,(d[0],d[1]-.3),(a[0],a[1]+.3),a,None,(13,0))
 for na,nb in ((13,14),(14,15),(15,16),(16,17)):
  a=lane(h[na])[-1];d=lane(h[nb])[0]
  if na in (13,16):
   fa,fb=forward(h[na]),forward(h[nb]);b=tuple(a[k]+fa[k]*.6 for k in (0,1));c=tuple(d[k]-fb[k]*.6 for k in (0,1))
  else:
   fa,fb=forward(h[na]),forward(h[nb]);b=tuple(a[k]+fa[k]*1.4 for k in (0,1));c=tuple(d[k]-fb[k]*1.4 for k in (0,1))
  add(f'Inner course link {na} to {nb}',a,b,c,d,(na,1),(nb,0))
 a=lane(h[17])[-1];d=(a[0],7+14.85*math.sqrt(max(0,1-(a[0]/17.25)**2)))
 add('Northeast circuit branch',a,(a[0],a[1]+.3),(d[0],d[1]-.3),d,(17,1),None)
 # These rising decks branch clear of the greens and are supported over the
 # sloping stream bank; neither is a floating paving skin.
 for sign,station,label in ((-1,0,'west'),(1,1,'east')):
  a=lane(h[15])[0 if station==0 else -1];d=lane(h[18])[-1 if station==0 else 0]
  add('Upper crossing '+label+' bank approach',a,(sign*4.6,a[1]+1.5),(sign*4.6,d[1]-1.5),d,(15,station),(18,1-station),True)
 for name,line,*_ in out:assert clear(line),('Adventure walking ribbon crosses green/border',p['seed'],name)
 return out
