"""Gauged K gutters, off-corner bottom outlets and rounded rectangular offsets."""
import math
from mathutils import Vector


def rounded(points,r=.065):
 pts=list(map(Vector,points));out=[pts[0]]
 for a,p,c in zip(pts,pts[1:],pts[2:]):
  d=min(r,(p-a).length*.3,(c-p).length*.3);u=p+(a-p).normalized()*d;v=p+(c-p).normalized()*d
  out.append(u)
  for j in range(1,6):
   t=j/5;out.append((1-t)**2*u+2*t*(1-t)*p+t*t*v)
 out.append(pts[-1]);return out


def section(me,points,wide,width=.0762,depth=.0508):
 pts=list(map(Vector,points));wide=Vector(wide).normalized();vs=[]
 for i,p in enumerate(pts):
  tangent=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
  u=(wide-tangent*wide.dot(tangent)).normalized();v=tangent.cross(u).normalized()
  vs.extend(p+u*sx*width/2+v*sy*depth/2 for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1)))
 me.geom(vs,[(j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k) for j in range(len(pts)-1) for k in range(4)])
 return vs[-4:]


def drain(b,me,a,c,n,block,index):
 if block.name=='Porch':return  # Small stoop roof has a drip hem; no pipes on its columns.
 a,c=Vector(a),Vector(c);normal=Vector((*n,0));along=(c-a).normalized()
 choices=[]
 for end,other in ((a,c),(c,a)):
  # The outlet is 11 in along the gutter, away from the miter itself.
  foot=end+(other-end).normalized()*min(.2794,(other-end).length*.3)
  pipe=foot-normal*(block.overhang-.125)
  if abs(n[0])>.5:pipe.y=max(block.y0+.15,min(block.y1-.15,pipe.y))
  else:pipe.x=max(block.x0+.15,min(block.x1-.15,pipe.x))
  valid=not any(v is not block and v.contains(pipe.x,pipe.y,.012) for v in b.plan['blocks'])
  # Pick a solid pier against the union of all opening intervals; a
  # sequential clamp can move out of one window and into its neighbor.
  axis=0 if abs(n[1])>.5 else 1;intervals=[]
  for opening in b.openings:
   owner=next(v for v in b.plan['blocks'] if v.name==opening['block'])
   face={'front':(0,-1),'back':(0,1),'left':(-1,0),'right':(1,0)}[opening['face']]
   if tuple(n)!=face:continue
   plane=owner.y0 if n==(0,-1) else owner.y1 if n==(0,1) else owner.x0 if n==(-1,0) else owner.x1
   support_plane=block.y0 if n==(0,-1) else block.y1 if n==(0,1) else block.x0 if n==(-1,0) else block.x1
   if abs(plane-support_plane)>.02:continue
   origin=owner.x0 if axis==0 else owner.y0;middle=origin+opening['u']
   margin=(opening['w'] if opening['shutters'] else opening['w']/2)+.19
   intervals.append((middle-margin,middle+margin))
  lo=block.x0+.15 if axis==0 else block.y0+.15;hi=block.x1-.15 if axis==0 else block.y1-.15
  candidates=[pipe[axis],lo,hi]+[v for a0,c0 in intervals for v in (a0-.005,c0+.005)]
  options=[v for v in candidates if lo<=v<=hi and not any(a0<v<c0 for a0,c0 in intervals)]
  if options:pipe[axis]=min(options,key=lambda v:abs(v-pipe[axis]));foot[axis]=pipe[axis]
  else:valid=False
  choices.append((valid,end,foot,pipe))
 valid,end,foot,pipe=max(choices,key=lambda x:(x[0],abs(x[1].x)))
 if not valid:raise ValueError('Blocked ranch drain '+block.name)
 # Continuous 1 mm K-gutter skin. Ends extend to the geometric miter,
 # without a collector box or any pipe through the corner.
 profile=[(.006,0),(.006,-.126),(.081,-.126),(.121,-.077),(.137,-.047),(.137,0),(.136,0),(.136,-.047),(.120,-.077),(.080,-.125),(.007,-.125),(.007,0)]
 verts=[]
 for p in (a,c):
  z=-.055+.0025*((p-foot).length-(end-foot).length)
  for u,dz in profile:
   v=p+normal*u+Vector((0,0,z+dz))
   if abs(n[1])>.5:
    if abs(p.x-(block.x0-block.overhang))<1e-5:v.x-=u
    if abs(p.x-(block.x1+block.overhang))<1e-5:v.x+=u
   else:
    if abs(p.y-(block.y0-block.overhang))<1e-5:v.y-=u
    if abs(p.y-(block.y1+block.overhang))<1e-5:v.y+=u
   verts.append(v)
 nn=len(profile);me.geom(verts,[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)])
 # Adjoining eaves can share one pipe near a wall corner; other run drains
 # around the open gutter miter to the first bottom outlet.
 reuse=next((v for v in b.drains if v['block']==block.name and math.dist(v['centerline'][3][:2],pipe[:2])<.55),None)
 if reuse:
  b.drains.append({**reuse,'gutter':[list(a),list(c)],'normal':n,'shared_column_outlet':True});return
 start=foot+normal*.060+Vector((0,0,-.183))
 walltop=Vector((pipe.x,pipe.y,start.z-block.overhang-.13));finish=Vector((pipe.x,pipe.y,.24))
 outlet=finish+normal*.30+Vector((0,0,-.12))
 controls=[start,start+Vector((0,0,-.09)),walltop+Vector((0,0,.10)),walltop,finish,finish+normal*.12+Vector((0,0,-.09)),outlet]
 rim=section(me,rounded(controls),along)
 center=sum(rim,Vector())/4;me.geom([center+(p-center)*.90-normal*.012 for p in rim],[(0,1,2,3)],color=(.025,.027,.024))
 # A short collar is entirely below the gutter's bottom.
 section(me,[start,start+Vector((0,0,-.045))],along,.082,.057)
 for z in (.72,1.65,2.45):
  if z>=walltop.z-.08:continue
  p=Vector((pipe.x,pipe.y,z));me.beam(p-along*.047,p+along*.047,.014,.015,r=.001)
  me.beam(p-along*.047,p-along*.047-normal*.14,.014,.015,r=.001)
  me.beam(p+along*.047,p+along*.047-normal*.14,.014,.015,r=.001)
 splash=b.mesh(f'{block.name}_Splash_{index}',component='splash_block');mid=outlet+normal*.12;mid.z=.0225
 splash.box(mid,(.31,.60,.045) if abs(n[1])>.5 else (.60,.31,.045),'Concrete',r=.009);splash.finish()
 b.drains.append(dict(block=block.name,gutter=[list(a),list(c)],normal=n,fall=.0025,
  centerline=[list(p) for p in controls],outlet=list(outlet),bottom_outlet=list(start),sampled_path=[list(p) for p in rounded(controls)]))
