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
 import json
 return _adventure_links(json.dumps(p['holes'],sort_keys=True,separators=(',',':')))

@functools.lru_cache(maxsize=512)
def _adventure_links(key):
 """Connected routes outside inflated construction envelopes, no ring circuit.

 Cubic headland turns are preferred. An eight-neighbor plan-space search
 handles the two cross-course connections, then removes unnecessary stations.
 Each accepted ribbon is checked against the actual boundary strips.
 """
 import json,heapq
 from PIL import Image,ImageDraw
 from plan_check import strips,overlap,hull
 holes=json.loads(key);obstacles=[q for h in holes for q in strips(h)];boxes=[(min(q[0] for q in poly),max(q[0] for q in poly),min(q[1] for q in poly),max(q[1] for q in poly)) for poly in obstacles]
 def clear(line,width=1.524):
  for quad in ribbon(line,width):
   lo,hi=min(q[0] for q in quad),max(q[0] for q in quad);bottom,top=min(q[1] for q in quad),max(q[1] for q in quad)
   if lo<-23.8 or hi>23.8 or bottom<-12.8 or top>27.6:return False
   for poly,(x0,x1,y0,y1) in zip(obstacles,boxes):
    if x1<lo or x0>hi or y1<bottom or y0>top:continue
    if overlap(quad,poly):return False
  return True
 step=.35;x0,y0=-23.0,-12.0;nx,ny=132,112
 image=Image.new('1',(nx,ny));draw=ImageDraw.Draw(image)
 for h in holes:
  for quad in strips(h,1.17):draw.polygon([((x-x0)/step,(y-y0)/step) for x,y in quad],fill=1)
  for t,direction in ((0,-1),(1,1)):
   cx,cy=center(h,t);w=halfwidth(h,t)+1.15
   cap=[local(h,cx+x,cy+y)[:2] for x,y in ((-w,0),(w,0),(w,direction*1.15),(-w,direction*1.15))]
   draw.polygon([((x-x0)/step,(y-y0)/step) for x,y in cap],fill=1)
 def grid(q):return (round((q[0]-x0)/step),round((q[1]-y0)/step))
 def point(q):return (x0+q[0]*step,y0+q[1]*step)
 def route(a,d):
  start,goal=grid(a),grid(d);opened=[(0,start)];cost={start:0};came={};seen=set()
  while opened:
   _,q=heapq.heappop(opened)
   if q in seen:continue
   seen.add(q)
   if q==goal:break
   for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
    n=q[0]+dx,q[1]+dy
    if not(0<=n[0]<nx and 0<=n[1]<ny) or (image.getpixel(n) and n not in (start,goal)):continue
    c=cost[q]+math.hypot(dx,dy)
    if c<cost.get(n,1e20):cost[n]=c;came[n]=q;heapq.heappush(opened,(c+math.dist(n,goal),n))
  if goal not in came:raise ValueError(('No adventure walking route',a,d))
  path=[goal]
  while path[-1]!=start:path.append(came[path[-1]])
  line=[a]+[point(q) for q in reversed(path[1:-1])]+[d]
  simplified=[line[0]];i=0
  while i<len(line)-1:
   j=len(line)-1
   while j>i+1 and not clear([line[i],line[j]],1.9):j-=1
   simplified.append(line[j]);i=j

  # Smooth each corner only when the actual finite-width ribbon stays clear.
  dense=[]
  for i,q in enumerate(simplified):
   if i==0 or i==len(simplified)-1:dense.append(q);continue
   prev,nxt=simplified[i-1],simplified[i+1];radius=min(.85,math.dist(prev,q)*.26,math.dist(q,nxt)*.26)
   a1=tuple(q[k]+(prev[k]-q[k])*radius/math.dist(prev,q) for k in (0,1));b1=tuple(q[k]+(nxt[k]-q[k])*radius/math.dist(nxt,q) for k in (0,1))
   bend=curve(a1,q,q,b1,7)
   if clear([prev]+bend+[nxt]):dense.extend(bend)
   else:dense.append(q)
  if not clear(dense):
   bad=[(i,j) for i,quad in enumerate(ribbon(dense)) for j,h in enumerate(holes) if any(overlap(quad,poly) for poly in strips(h))]
   raise ValueError(('Adventure route ribbon clearance',a,d,bad[:8],[(dense[i],dense[i+1],j+1) for i,j in bad[:2]]))
  return dense
 out=[]
 for prev,nxt in zip(holes,holes[1:]):
  a,d=lane(prev)[-1],lane(nxt)[0];fa,fb=forward(prev),forward(nxt);line=None
  for handle in (1.2,2.4,3.5,5,7):
   trial=curve(a,tuple(a[k]+fa[k]*handle for k in (0,1)),tuple(d[k]-fb[k]*handle for k in (0,1)),d,25)
   if clear(trial):line=trial;break
  if line is None:line=route(a,d)
  # Connections follow terraced fill. Actual stream spans retain framed decks.
  out.append((f'Winding adventure link {prev["number"]} to {nxt["number"]}',line,(prev['number'],1),(nxt['number'],0),False))
 return out

def quarry_ledge():
 """Public stair return to the grade-backed central viewing ledge."""
 return [(5.9,10.5,2.45),(5.35,12.3,2.35),(3.9,14.1,2.05),(1.2,15.3,1.62),(-1.7,15.4,1.521)]
