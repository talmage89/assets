"""Carpeted concrete lanes, measured cup voids, real edging and play features."""
import math,random
from geometry import *
from plan import center,halfwidth,level

def playing_mesh(h,parent):
 nx=13;ts=sorted(set([i/52 for i in range(53) if abs(i/52-.88)>.021]+[.859,.901]))
 vs=[];fs=[];row=nx+1
 for t in ts:
  cx,y=center(h,t);w=halfwidth(h,t)
  # Original end shoulders ease the slab's corners.
  ease=1
  for j in range(row):
   x=cx+(2*j/nx-1)*w*ease;vs.append((x,y,level(h,x,t)+.0048))
 ci=next(i for i in range(len(ts)-1) if ts[i]<.88<ts[i+1]);cj=nx//2
 for i in range(len(ts)-1):
  for j in range(nx):
   if i==ci and j==cj:continue
   k=i*row+j;fs.append((k,k+1,k+1+row,k+row))
 # Explicit annular topology: a true circular cup opening, no black disc decal.
 cx,cy=center(h,.88);z=level(h,cx,.88)+.0048
 corners=[ci*row+cj,ci*row+cj+1,(ci+1)*row+cj+1,(ci+1)*row+cj]
 angles=[math.atan2(vs[k][1]-cy,vs[k][0]-cx) for k in corners]
 for i in range(1,4):
  while angles[i]<angles[i-1]:angles[i]+=math.tau
 ringids=[]
 for j in range(4):
  a=angles[j];b=angles[j+1] if j<3 else angles[0]+math.tau
  for k in range(8):
   theta=a+(b-a)*k/8;ringids.append(len(vs));vs.append((cx+.055975*math.cos(theta),cy+.055975*math.sin(theta),z))
 for j in range(4):
  for k in range(8):
   i=j*8+k;fs.append((corners[j],ringids[i],ringids[(i+1)%32]))
  fs.append((corners[j],ringids[((j+1)*8)%32],corners[(j+1)%4]))
 ob=mesh('Carpet playing face',vs,fs,('carpet','carpet2','carpet3')[h['carpet']],parent,False)
 # 4-inch base is a visible perimeter skin; bottom omitted against subgrade.
 boundary=[i*row for i in range(len(ts))]+[(len(ts)-1)*row+j for j in range(1,row)]+[i*row+nx for i in reversed(range(len(ts)-1))]+[j for j in reversed(range(1,nx))]
 top=[vs[k] for k in boundary];verts=[(x,y,z-.0048) for x,y,z in top]+[(x,y,z-.1064) for x,y,z in top];n=len(top)
 mesh('Four inch concrete slab edge',verts,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'concrete',parent,False)
 filltop=[(x,y,z-.1064) for x,y,z in top]
 fillbase=[(x,y,.014) for x,y,z in top]
 own(G.loft('Compacted graded base with planted berm', [fillbase,filltop],M['grass'],caps=False),parent)
 ring('Cup aluminum liner',(cx,cy),.055975,.053975,z-.1016,z,'metal',parent)
 ring('Cup recessed drain floor',(cx,cy),.053975,.010,z-.1016,z-.0996,'black',parent)
 ring('Carpet cut edge',(cx,cy),.05599,.055975,z-.0048,z,'carpet',parent)
 return dict(opening_diameter=.10795,slab_thickness=.1016,cup_center=(cx,cy,z),tee_surface_z=level(h,*[center(h,.08)[0],.08])+.0048)

def border(h,rt):
 rng=random.Random(h['number']+31)
 for side in (-1,1):
  n=25 if h['border']=='rock' else (int(h['length']/.215) if h['border']=='brick' else 14)
  for i in range(n):
   t0=i/n;t1=(i+1)/n
   if min(abs((t0+t1)/2-.08),abs((t0+t1)/2-.88))*h['length']<.44:continue
   x0,y0=center(h,t0);x1,y1=center(h,t1)
   x0+=side*(halfwidth(h,t0)+.08);x1+=side*(halfwidth(h,t1)+.08)
   z0=level(h,x0,t0);z1=level(h,x1,t1)
   if h['border']=='rock':
    rock('Set stone bank',((x0+x1)/2,(y0+y1)/2,(z0+z1)/2-.06),(.34,.40,.28),rt,i+side*39+h['number']*71)
   else:
    mat={'concrete':'concrete','brick':'brick','timber':'wood'}[h['border']]
    height=.1397 if mat=='wood' else (.1016 if mat=='brick' else .1524)
    stock_width=.0889 if mat=='wood' else (.05715 if mat=='brick' else .1524)
    beam('Jointed '+h['border']+' border',(x0,y0,z0+height/2),(x1,y1,z1+height/2),stock_width,height,mat,rt)
    if mat=='wood':
     for x,y,z in ((x0,y0,z0),(x1,y1,z1)):cyl('Countersunk spike',(x,y,z+height-.002),(x,y,z+height+.001),.008,'metal',rt,8)
 # Low tee entrance and cup backstop carry actual crosswise closure.
 for t in (0,1):
  x,y=center(h,t);w=halfwidth(h,t)*(.82 if t in (0,1) else 1)
  box('End curb',(x,y,level(h,x,t)+(.0127 if t==0 else .0762)),(w*2+.30,.15,.0254 if t==0 else .1524),'concrete' if h['border']=='concrete' else 'wood',rt)

def play_feature(h,rt):
 f=h['feature'];x,y=center(h,.48);z=level(h,x,.48)+.006
 if f=='tunnel':
  # Masonry arched opening; .48 m wide and .42 m clear at its crown.
  n=18;vs=[]
  for yy in (y-.50,y+.50):
   for r in (.26,.40):
    vs.extend((x+r*math.cos(i*math.pi/n),yy,z+r*math.sin(i*math.pi/n)) for i in range(n+1))
  stride=n+1;fs=[]
  for i in range(n):
   fs.extend(((i,i+1,2*stride+i+1,2*stride+i),(stride+i,3*stride+i,3*stride+i+1,stride+i+1),(i,stride+i,stride+i+1,i+1),(2*stride+i,2*stride+i+1,3*stride+i+1,3*stride+i)))
  mesh('Tunnel arch with intrados',vs,fs,'brick',rt)
 elif f=='split':
  box('Bank divider',(x,y,z+.14),(.18,1.6,.28),'brick',rt,.018,2)
 elif f=='dogleg':
  for s in (-1,1):box('Offset rebound wall',(x+s*.58,y+s*.8,z+.12),(.75,.18,.24),'wood',rt)
 elif f=='loop':
  # Continuous helical loop has separated entry/exit and supporting steel feet.
  pts=[];n=64
  for i in range(n+1):
   a=-math.pi/2+i*math.tau/n;pts.append((x+(i/n-.5)*.36,y+.58*math.cos(a),z+.58+.58*math.sin(a)))
  loops=[]
  for i,p in enumerate(pts):
   a=-math.pi/2+i*math.tau/n
   loops.append([(p[0]+s*.22,p[1]+d*.012*math.cos(a),p[2]+d*.012*math.sin(a)) for s,d in ((-1,-1),(1,-1),(1,1),(-1,1))])
  own(G.loft('Formed steel loop running track',loops,M['red']),rt)
  for s in (-1,1):
   box('Loop anchor foot',(x+s*.35,y,z+.035),(.24,.50,.07),'metal',rt)
   beam('Loop support',(x+s*.35,y,z+.07),(x+s*.26,y,z+.62),.05,.05,'metal',rt)

def build(h,parent):
 rt=root('Hole_%02d'%h['number'],(*h['origin'],0),h['yaw'],parent,kind='hole');rt['hole_number']=h['number'];rt['feature']=h['feature'];rt['footprint']=json.dumps(h['footprint'])
 audit=playing_mesh(h,rt);border(h,rt);play_feature(h,rt)
 tx,ty=center(h,.08);tz=level(h,tx,.08)+.0048
 # Real 36 × 24 in low rubber mat, recessed start disc, not a giant tee block.
 pad=box('Rubber tee pad',(tx,ty,tz+.0015875),(.9144,.6096,.003175),'rubber',rt,.001,1)
 cutter=cyl('Tee pocket tool',(tx,ty,tz-.02),(tx,ty,tz+.02),.017,'black',rt,24)
 bpy.context.view_layer.update();G.boolean(pad,cutter)
 ring('Tee ball-start recess',(tx,ty),.035,.017,tz+.0032,tz+.004,'black',rt,20)
 sx=tx-halfwidth(h,.08)-.38;station_base=tz-.1298
 box('Tee sign post',(sx,ty,.62+station_base),(.0635,.0635,1.24),'wood',rt)
 box('Tee number sign',(sx,ty-.04,1.24+station_base),(.48,.035,.38),'ivory',rt,.01,2)
 text(rt,str(h['number']),(sx,ty-.059,1.31+station_base),.43,.17)
 text(rt,'PAR '+str(h['par']),(sx,ty-.059,1.14+station_base),.39,.09)
 box('Scorecard shelf',(sx,ty-.15,.98+station_base),(.36,.27,.024),'wood',rt)
 box('Scorecard',(sx,ty-.18,.994+station_base),(.16,.11,.001),'ivory',rt,0)
 text(rt,'SCORE',(sx,ty-.18,.995+station_base),.14,.04,False)
 cyl('Hex pencil',(sx+.10,ty-.24,.997+station_base),(sx+.10,ty-.11,.997+station_base),.0035,'yellow',rt,6)
 cx,cy,cz=audit['cup_center'];flag=root(rt.name+'__Flag',(cx+.20,cy+.15,cz),parent=rt,kind='flag');flag['module']=False;flag['pivot_axis']='Z';flag['range_degrees']=[-30,30]
 cyl('Cup marker pole',(0,0,0),(0,0,.76),.006,'white',flag,8)
 # Soft fabric, 5 × 3 grid, sagging free edge; separate moving marker.
 vs=[(.33*u/4,.016*math.sin(u*1.5+v)*u/4,.73-.18*v/2-.025*math.sin(math.pi*u/4)) for v in range(3) for u in range(5)]
 mesh('Sagging marker flag',vs,[(v*5+u,v*5+u+1,(v+1)*5+u+1,(v+1)*5+u) for v in range(2) for u in range(4)],'yellow',flag,False)
 socket(rt,'Tee',(tx,ty,tz),'tee');socket(rt,'Cup',(cx,cy,cz),'cup')
 rt['footprint_local']=json.dumps([[-2.8,-h['length']/2-1],[2.8,-h['length']/2-1],[2.8,h['length']/2+1],[-2.8,h['length']/2+1]])
 return rt,audit
