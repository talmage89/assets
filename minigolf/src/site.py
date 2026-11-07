"""Course site construction, water containment and serviceable public fixtures."""
import math,random
from geometry import *
from fixtures import roof
from plan import center,halfwidth,level,local,water_level
import landscape
import paths

GRADING=False
def grade(y):return .065*max(0,y+7) if GRADING else 0

def water_airside(ob,axis=2,sign=1):
 # The kit closes/reorients general mesh normals. An open water skin needs
 # an explicit air-facing side after that operation, even below world Z=0.
 bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
 bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal[axis]*sign<0])
 bm.to_mesh(ob.data);bm.free();ob.data.update();return ob

def mulch_skin(ob):
 # Course bed construction is split at its two-metre atlas repeat so its
 # chip scale survives across the whole parcel without another texture set.
 tile=2.;atlas_repeat_cells(ob.data,tile,(0,1));ob['mulch_uv_m']=tile
 return ob

def walk(rt,name,points,width=1.524,z=.065,span=False):
 if span:
  # Additional stations retain contact through tight grade transitions.
  points=[q for a,b in zip(points,points[1:]) for q in (a,tuple((x+y)/2 for x,y in zip(a,b)))]+[points[-1]]
  rt=root('WalkSpan',parent=rt,kind='walk_span')
 vs=[]
 for i,p in enumerate(points):
  a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)]);d=Vector((b.x-a.x,b.y-a.y)).normalized();n=Vector((-d.y,d.x))
  for side in (-1,1):vs.append((p[0]+side*n.x*width/2,p[1]+side*n.y*width/2,(p[2] if len(p)>2 else z+(grade(p[1]) if z>=0 else 0))))
 ob=mesh(name,vs,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(points)-1)],'concrete',rt,False)
 ob['walking_surface']=True
 if z>=0:
  bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0]);bm.to_mesh(ob.data);bm.free();ob.data.update()
  mod=ob.modifiers.new('Walk slab gauge','SOLIDIFY');mod.thickness=.10;mod.offset=-1
  if not span:ob['buried_walk_bottom']=True
  if span:
   # An explicit vertical-gauge deck gives each graded flange a real seat.
   # Unlike an offset shell, its end bearing surfaces stay above the supports.
   ob.modifiers.remove(mod);n=len(vs);boundary=list(range(0,n,2))+list(reversed(range(1,n,2)))
   topfaces=[tuple(f.vertices) for f in ob.data.polygons]
   data=G.mesh('Crossing walk solid deck',vs+[(x,y,zz-.10) for x,y,zz in vs],topfaces+[tuple(k+n for k in reversed(f)) for f in topfaces]+[(a,b,b+n,a+n) for a,b in zip(boundary,boundary[1:]+boundary[:1])],M['concrete'])
   old=ob.data;ob.data=data.data;bpy.data.objects.remove(data,do_unlink=True);bpy.data.meshes.remove(old)
   seats={}
   for side in (-1,1):
    sections=[]
    for i in range(len(points)):
     a=Vector(vs[2*i]);b=Vector(vs[2*i+1]);normal=(b-a).normalized();q=(a+b)/2+normal*side*(width/2-.20)
     tops=[q+normal*dx-Vector((0,0,.10)) for dx in (-.05,.05)]
     sections.append([tuple(tops[0]-Vector((0,0,.14))),tuple(tops[1]-Vector((0,0,.14))),tuple(tops[1]),tuple(tops[0])])
     seats[(side,i)]=(q,min(v.z for v in tops)-.14,normal)
    own(G.loft('Continuous crossing-walk girder',sections,M['wood']),rt)
    for index in (round((len(points)-1)*.28),round((len(points)-1)*.72)):
     q,top,normal=seats[(side,index)]
     box('Crossing-walk intermediate pier',(q.x,q.y,(top-.57)/2),(.35,.50,top+.57),'rocklight',rt,.012)
   for i in (0,len(points)-1):
    q=(Vector(vs[2*i])+Vector(vs[2*i+1]))/2;top=min(seats[(side,i)][1] for side in (-1,1))-.012;bottom=min(.015+grade(q.y),top-.18)
    support=box('Crossing-walk abutment',(q.x,q.y,(bottom+top)/2),(.40,width,max(.02,top-bottom)),'rocklight',rt,.008)
    direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);support.rotation_euler.z=math.atan2(direction.y,direction.x)
    for side in (-1,1):
     qq,zz,normal=seats[(side,i)];pad=box('Crossing-walk abutment bearing',(qq.x,qq.y,(top+zz)/2),(.30,.16,zz-top),'rubber',rt)
     pad.rotation_euler.z=support.rotation_euler.z
   for i in range(0,len(points),6):
    q=Vector(vs[2*i+1]);box('Outer span guard post',(q.x,q.y,q.z+.5335),(.07,.07,1.067),'wood',rt)
   rail=[tuple(Vector(vs[2*i+1])+Vector((0,0,1.067))) for i in range(len(points))]
   tube('Continuous span handrail',rail,.022,'wood',rt,8)
  else:
   # Raised paving is seated on compacted fill, not a floating 100mm sheet.
   upper=[v.co-v.normal*.10 for v in ob.data.vertices]
   if any(q.z>.015+grade(q.y)+.015 for q in upper):
    n=len(upper);lower=[(q.x,q.y,min(q.z-.015,.015+grade(q.y)-.08)) for q in upper]
    boundary=list(range(0,n,2))+list(reversed(range(1,n,2)))
    mesh('Compacted support below raised walk',list(map(tuple,upper))+lower,[(a,b,b+n,a+n) for a,b in zip(boundary,boundary[1:]+boundary[:1])],'soil',rt,False)
 return ob

def footbridge(rt,p=(0,-7.1,0)):
 sub=root('StreamFootbridge',p,parent=rt,kind='footbridge')
 for y in (-.65,.65):
  box('2x6 continuous joist',(0,y,.1361),(3.6,.0381,.1397),'wood',sub)
 for i in range(24):box('Bridge deck board',(-1.725+i*.15,0,.225),(.143,1.68,.0381),'wood',sub)
 for y in (-.81,.81):
  for x in (-1.70,0,1.70):
   box('Bridge guard post',(x,y,.7775),(.0889,.0889,1.067),'wood',sub)
   for z in (.38,.95):cyl('Galvanized carriage bolt',(x,y-.05,z),(x,y+.05,z),.010,'metal',sub,8)
  for z in (.67,1.292):beam('42 inch guard rail',(-1.75,y,z),(1.75,y,z),.0381,.0889,'wood',sub)
  for x in (-1.26,-.84,-.42,.42,.84,1.26):box('Guard baluster',(x,y,.76),(.0381,.0381,.95),'wood',sub)
 for x in (-1.9,1.9):box('Bridge concrete abutment',(x,0,-.066875),(.28,1.9,.26625),'concrete',sub)
 socket(sub,'DeckCenter',(0,0,.244),'footbridge')
 return sub

def pond_loops(adv):
 # Shared cut/liner outlines. Adventure's southern arc opens into a real
 # channel: one polygon, not an oval wall with a stream laid across it.
 cx,cy=0,5;rx,ry=(3.6,7.0) if adv else (1.1,2.7);loops=[]
 for k,(factor,width,z) in enumerate(((1.15,1.0,None),(1.02,.65,-.08),(.80,.50,-.57))):
  if not adv:
   xy=[(rx*factor*math.cos(i*math.tau/64),cy+ry*factor*math.sin(i*math.tau/64)) for i in range(64)]
  else:
   delta=math.asin(width/(rx*factor));start=1.5*math.pi+delta;end=1.5*math.pi-delta+math.tau
   xy=[(rx*factor*math.cos(start+(end-start)*i/56),cy+ry*factor*math.sin(start+(end-start)*i/56)) for i in range(57)]
   centers=[(.08,-3.5),(.10,-4),(-.20,-6),(0,-7.3)]
   xy += [(x-width,y) for x,y in centers]
   xy += [(width*math.cos(math.pi+j*math.pi/8),-7.3+.35*math.sin(math.pi+j*math.pi/8)) for j in range(1,9)]
   xy += [(x+width,y) for x,y in reversed(centers[:-1])]
  loop=[]
  for i,(x,y) in enumerate(xy):
   x*=1+.12*math.sin(y*.85)+.07*math.sin(y*1.95)
   y+=.30*math.sin(x*1.7+y*.65)
   zz=.015+grade(y) if k==0 else z
   if adv and k==2 and i>=57:zz=-.31
   loop.append((x if adv else x-1.7,y,zz))
  loops.append(loop)
 return loops

def froth(rt,p,size,seed):
 # Millimetre-scale entrained bubbles have no square lattice or large opaque
 # islands. Tiny irregular triangles resolve as glints at the player camera.
 rng=random.Random(seed);x,y,z=p;w,d=size;vs=[];fs=[]
 for i in range(80):
  angle=rng.random()*math.tau;radius=math.sqrt(rng.random());cx=x+w*.5*radius*math.cos(angle);cy=y+d*.5*radius*math.sin(angle)
  r=rng.uniform(.0015,.0055);turn=rng.random()*math.tau;k=len(vs)
  vs.extend((cx+r*math.cos(turn+j*math.tau/3),cy+r*math.sin(turn+j*math.tau/3),z+.0006*rng.random()) for j in range(3));fs.append((k,k+1,k+2))
 return water_airside(mesh('Broken receiving-pool froth',vs,fs,'foam',rt,False))

def basin(rt,adv):
 water=root('WaterSystem',parent=rt,kind='water_system')
 cx,cy=0,5;rx,ry=(3.6,7.0) if adv else (1.1,2.7);n=64;loops=pond_loops(adv)
 own(G.loft('Protected continuous EPDM basin and channel',loops,M['liner'],caps=False),water)
 # Cast shoreline shelf shields the EPDM from feet and sunlight. The liner
 # remains continuous underneath; only the lowest folded toe is exposed.
 stone_loops=[[(x*.995,cy+(y-cy)*.995,z+.006) for x,y,z in loop] for loop in loops[:2]]
 own(G.loft('Carved shoreline shelves',stone_loops,M['rocklight'],caps=False),water)
 mesh('Pond liner floor',loops[-1],[tuple(range(len(loops[-1])))],'liner',water,False)
 surface=[]
 for mid,floor in zip(loops[1],loops[2]):
  t=(water_level(mid[1])-mid[2])/(floor[2]-mid[2]);surface.append((mid[0]*(1-t)+floor[0]*t,mid[1]*(1-t)+floor[1]*t))
 def clip(poly,y,above):
  out=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   ia=(a[1]>=y) if above else (a[1]<=y);ib=(b[1]>=y) if above else (b[1]<=y)
   if ia:out.append(a)
   if ia!=ib:
    t=(y-a[1])/(b[1]-a[1]);out.append((a[0]+t*(b[0]-a[0]),y))
  return out
 stations=sorted(set([q[1] for q in surface]+[-5.83,-5.53,-3.23,-2.93]));wet_vs=[];wet_fs=[]
 for lo,hi in zip(stations,stations[1:]):
  poly=clip(clip(surface,lo,True),hi,False)
  clean=[]
  for q in poly:
   if not clean or math.dist(q,clean[-1])>1e-7:clean.append(q)
  if len(clean)>2 and math.dist(clean[0],clean[-1])<1e-7:clean.pop()
  if len(clean)>3:clean=[q for i,q in enumerate(clean) if abs((q[0]-clean[i-1][0])*(clean[(i+1)%len(clean)][1]-q[1])-(q[1]-clean[i-1][1])*(clean[(i+1)%len(clean)][0]-q[0]))>1e-10]
  if len(clean)<3:continue
  area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(clean,clean[1:]+clean[:1])))/2
  if area<1e-9:continue
  first=len(wet_vs);wet_vs.extend((x,y,water_level(y)) for x,y in clean);wet_fs.append(tuple(range(first,len(wet_vs))))
 water_airside(mesh('Continuous pond and stream water',wet_vs,wet_fs,'water',water,False))
 rim=[(x,y,z-.10) for x,y,z in loops[0]]
 rockwall('Continuous mortared pond coping',rim,.48,.27,water,517,closed=True)
 for i in range(0,len(rim),7):
  x,y,z=rim[i];rock('Embedded irregular fieldstone',(x,y,z-.08),(.75+.15*math.sin(i),.58,.38),water,118+i,'rocklight')
 for i in range(5):
  a=i*2.4;ball('Lost pond ball',((0 if adv else -1.7)+.9*math.sin(a),cy+.7*i,-.54865),.02135,'white' if i%2 else 'yellow',water)
 if adv:
  # One continuous stratified mountain, with three independent spill shelves.
  mountain=rock('Quarry mountain',(3.5,11.1,-.10),(7.0,6.8,3.1),water,290,'rocklight')
  cutter=box('Recessed fall channel tool',(2.0,8.1,1.6),(2.40,4.75,3.8),'black',water,0)
  bpy.context.view_layer.update();G.boolean(mountain,cutter)
  # The public stair and ledge are carved into the faux-rock shell; the
  # mountain must not protrude through their walking surfaces.
  from plan_check import hull
  ledge=hull([q for quad in paths.ribbon([(5.85,10.30),(6.3,12.2),(7.08,14.20)],1.70) for q in quad])
  cutter=own(G.profile('Quarry ledge clearance tool',ledge,2.35,5,M['black'],axis='Z'),water)
  bpy.context.view_layer.update();G.boolean(mountain,cutter)
  floor=[]
  for j in range(10):
   z=.95+(j+1)*.15-.04
   floor.extend(((6.93+j*.34+.012,z),(6.93+(j+1)*.34+.012,z)))
  profile=floor+[(floor[-1][0],5),(floor[0][0],5)]
  cutter=own(G.profile('Quarry stair clearance tool',profile,5.04,6.76,M['black'],axis='X'),water)
  bpy.context.view_layer.update();G.boolean(mountain,cutter)
  rock('Fractured fall west cheek',(.62,10.2,-.06),(1.10,2.1,2.45),water,300,'rocklight')
  rock('Fractured fall east cheek',(3.40,10.3,-.05),(1.35,2.6,2.80),water,302,'rocklight')
  rock('Western terraced outcrop',(-5.0,14.6,.4),(3.8,5.0,2.4),water,294,'rocklight')
  # A continuous stepped stone body supports the spill shelves. The old
  # hollow recess left separate shelf plates hanging in an empty channel.
  levels=[(-.30,8.50,2.30),(.69,8.76,2.30),(.735,9.23,2.05),(1.60,9.43,1.95),(1.645,9.84,1.63),(2.45,10.01,1.52),(2.49,10.08,1.52)]
  backing=[]
  for z,front,width in levels:
   backing.append([(2-width/2,front+.035,z),(2-width*.22,front-.014,z+.006),(2+width*.24,front+.009,z-.004),(2+width/2,front+.028,z),(2+width/2+.13,10.91,z),(2-width/2-.12,10.91,z)])
  body=own(G.smooth(G.loft('Continuous cast waterfall stair body',backing,M['rocklight']),38),water);body['rock_seed']=329
  for j,(yy,zz,width) in enumerate(((10.20,2.48,1.15),(9.60,1.63,1.55),(8.95,.72,1.9))):
   box('Recessed spill lip',(2.0,yy-.17,zz),(width,.025,.012),'metal',water,.002,1)
   # Cast ledge with an undercut toe and a broad forward crown covers the
   # weir body. Only its thin front lip remains visible beneath the flow.
   top=[(2-width/2-.40,yy-.17),(2-width/2,yy-.175),(2+width/2,yy-.175),(2+width/2+.40,yy-.13),(2+width/2+.48,yy+.58),(2-width/2-.46,yy+.65)]
   lower=[(x, y+(.19 if k<4 else 0),zz-.24-.014*math.sin(k*2+j)) for k,(x,y) in enumerate(top)]
   crown=[(x,y,zz-.010+.004*math.sin(k*3+j)) for k,(x,y) in enumerate(top)]
   shelf=own(G.smooth(G.loft('Undercut cast spill ledge',[lower,crown],M['rocklight']),40),water);shelf['rock_seed']=330+j
   pool=[(2-width/2+.02,yy-.173,zz+.013),(2+width/2-.02,yy-.173,zz+.013),(2+width/2-.02,yy+.46,zz+.013),(2-width/2+.02,yy+.46,zz+.013)]
   water_airside(mesh('Receiving spill pool',pool,[(0,1,2,3)],'fallwater',water,False))
   drop=zz-(1.63,.72,-.17)[j]
   # One continuous closed liquid film, with nonparallel travelling
   # wrinkles. Regular separated bands looked like a radiator grille.
   vs=[];fs=[];nx,ny=24,8;phase=j*2.13
   def flow_point(q,t):
    warp=(.004*math.sin(q*53+t*11+phase)+.0025*math.sin(q*121-t*17+phase*.7)+.0014*math.sin(q*231+t*31))*(.2+.8*t)
    return (2+(q-.5)*width,yy-.18-.30*math.sin(t*math.pi/2)+warp,zz-drop*t+.0025*math.sin(q*83+t*31+phase)*t)
   for v in range(ny+1):
    for u in range(nx+1):vs.append(flow_point(u/nx,v/ny))
   for v in range(ny):
    for u in range(nx):
     k=v*(nx+1)+u;fs.append((k,k+1,k+nx+2,k+nx+1))
   flow=G.smooth(water_airside(mesh('Aerated water cascading sheet',vs,fs,'fallwater',water,False),1,-1),70);flow['flow_sheet']=True
   film=flow.modifiers.new('Liquid film exit interface','SOLIDIFY');film.thickness=.0015;film.offset=-1
   rng=random.Random(912+j)
   for fragment in range(72):
    q=rng.uniform(.015,.985);start=rng.uniform(.10,.95);end=min(.995,start+rng.uniform(.008,.045));strip=[]
    half=rng.uniform(.00035,.0012)
    for t in (start,end):
     xx,yyflow,zzflow=flow_point(q,t)
     for dx in (-half,half):strip.append((xx+dx,yyflow-.002,zzflow))
    water_airside(mesh('Entrained cascade foam streak',strip,[(0,1,3,2)],'foam',water,False),1,-1)
   for i in range(6):
    a=i*2.1;froth(water,(2+width*.36*math.sin(a),yy-.48+.15*math.cos(a),zz-drop+.012),(.40,.23),710+j*17+i)
  # The continuous basin above already contains the protected stream.
  footbridge(rt)
  for j,yy in enumerate((-3.0,-5.6)):
   upstream=water_level(yy+.22)
   rockwall('Stream bedrock riffle',[(-.70,yy,upstream-.035),(-.25,yy+.12,upstream-.065),(.2,yy-.1,upstream-.065),(.68,yy+.05,upstream-.035)],.32,.025,water,850+j,'rock')
   for k in range(5):
    froth(water,(-.52+k*.26,yy-.22,water_level(yy-.22)+.005),(.22,.31),880+k)
  # Gravity deposits collect at sheltered bends rather than across the pool.
  rng=random.Random(531)
  for j in range(24):
   x=rng.gauss(-2.45 if j%2 else -2.75,.17);y=rng.gauss(5.5 if j%2 else 6.15,.26);angle=rng.random()*math.tau;size=rng.uniform(.7,1.2)
   points=[(x+size*(u*math.cos(angle)-v*math.sin(angle)),y+size*(u*math.sin(angle)+v*math.cos(angle)),-.165+.001*rng.random()) for u,v in ((-.025,0),(0,.045),(.025,0),(0,-.045))]
   water_airside(mesh('Sheltered water-edge fallen leaf',points,[(0,1,2,3)],'leaf',water,False))
  # Return pipe follows the buried bank; only service ends are exposed.
  tube('63 mm return service pipe',[(4.1,8.8,.05),(4.1,9.5,.05),(3.9,10.5,1.90),(3.1,10.5,2.48),(2.0,10.30,2.48)],.0315,'black',water,10)
  box('Pump service vault',(4.9,8.8,grade(8.8)-.09),(.75,.85,.24),'concrete',water)
  box('Pump service lid',(4.9,8.8,grade(8.8)+.0425),(.78,.88,.025),'metal',water)
  box('Screened intake',(2.9,6.7,-.22),(.38,.38,.11),'black',water)
  tube('Intake bank connection',[(3.05,6.7,-.22),(3.5,6.7,-.22)],.0315,'black',water,10)
  for i in range(7):box('Intake screen bar',(2.75+i*.05,6.7,-.156),(.012,.35,.015),'metal',water)
 socket(water,'Pump',(4.9,8.8,.25),'water_pump');socket(water,'WaterLevel',(0 if adv else -1.7,5,-.17),'water_level')
 return water

def planted_bed(rt,spec):
 points=landscape.outline(spec);surface=[(x,y,.023+grade(y)) for x,y in points]
 mulch_skin(mesh(spec['name']+' mulch',surface,[tuple(range(len(surface)))],'soil',rt,False))
 edging=[]
 for i,(x,y) in enumerate(points):
  a=Vector(points[i-1]);b=Vector(points[(i+1)%len(points)]);d=(b-a).normalized();normal=Vector((-d.y,d.x));z=.023+grade(y)
  edging.append([(x+normal.x*dx,y+normal.y*dx,z+dz) for dx,dz in ((-.0015,-.04),(.0015,-.04),(.0015,.025),(-.0015,.025))])
 own(G.loft(spec['name']+' formed edging',edging+[edging[0]],M['black'],caps=False),rt)

def clubhouse(p,rt):
 x,y=p['clubhouse'];sub=root('Clubhouse',(x,y,.06),parent=rt,kind='clubhouse');w,d=6.8,4.6
 box('Hut slab',(0,.6,.06),(w+.4,d+1.6,.12),'concrete',sub)
 # Open counter faces course +Y. Actual framed walls, recess, inside floor.
 box('Back wall',(0,-d/2,1.35),(w,.14,2.7),'ivory',sub)
 for s in (-1,1):box('Side wall',(s*w/2,0,1.35),(.14,d,2.7),'ivory',sub)
 box('Counter sill wall',(0,d/2,.50),(4.3,.14,1.0),'wood',sub)
 box('Counter header',(0,d/2,2.46),(w,.17,.48),'wood',sub)
 for x in (-3.1,-2.2,2.2,3.1):box('Counter jamb',(x,d/2,1.70),(.14,.17,1.4),'wood',sub)
 box('Fixed service-board plywood wall',(-2.775,d/2,1.16),(1.11,.14,2.32),'ivory',sub,0)
 box('Entry outer wall return',(3.25,d/2,1.16),(.30,.14,2.32),'ivory',sub,0)
 box('Entry strike-side casing',(3.044,d/2-.04,1.15),(.07,.14,2.10),'wood',sub,0)
 box('Entry frame head',(2.65,d/2-.04,2.205),(.76,.14,.04),'wood',sub,0)
 box('Open service counter',(0,d/2+.14,1.03),(4.4,.65,.075),'red',sub,.018,2)
 box('Sheltered counter ceiling',(0,0,2.66),(w,d,.10),'wood',sub)
 box('Counter fluorescent housing',(0,1.25,2.58),(1.25,.18,.055),'metal',sub)
 for yy in (1.20,1.30):box('Service counter lamp',(0,yy,2.542),(1.14,.026,.026),'white',sub,.006,2)
 socket(sub,'CounterLight',(0,1.25,2.52),'service_counter_light')
 roof(sub,'Hut pitched roof',w+.65,d+.9,2.73,1.1)
 # Small operating entry in the side bay, physical hinge at jamb.
 door=root('Clubhouse__Door',(2.29,d/2-.04,.13),parent=sub);door['module']=False;door['pivot_axis']='Z';door['range_degrees']=[-90,0]
 box('Entry leaf',(.369,0,1.025),(.690,.045,2.05),'red',door)
 cyl('Entry pull',(.63,-.05,.90),(.63,-.05,1.14),.012,'metal',door)
 for z in (.40,1.70):
  box('Fixed hinge strap',(2.24,d/2-.04,z+.075),(.10,.025,.010),'metal',sub)
  cyl('Fixed hinge pin',(2.29,d/2-.04,z+.08),(2.29,d/2-.04,z+.18),.008,'metal',sub,12)
  ring('Moving hinge barrel',(0,0),.015,.009,z-.04,z+.04,'metal',door,12)
  box('Moving hinge strap',(.054,0,z),(.082,.020,.065),'metal',door)
 # Counter-facing signs are flipped so their fronts face +Y.
 sign=root('Clubhouse sign',(0,d/2+.47,3.04),180,sub);sign['module']=False
 text(sign,p['name'].upper(),(0,0,0),3.5,.27)
 # Actual interior stock sits on a supported worktop behind the opening.
 box('Inner worktop',(0,1.55,1.0),(4.4,1.50,.06),'wood',sub,0)
 for x in (-1.8,1.8):
  box('Counter rear support',(x,.86,.545),(.10,.10,.85),'wood',sub,0)
 # Actual interior stock visible through the opening.
 for x in (-1.55,0,1.55):
  box('Ball tray plywood floor',(x,1.25,1.035),(.40,.30,.010),'navy',sub,0)
  for side in (-1,1):box('Ball tray plywood side',(x+side*.197,1.25,1.085),(.006,.30,.09),'navy',sub,0)
  box('Ball tray plywood back',(x,1.103,1.085),(.388,.006,.09),'navy',sub,0)
  box('Ball tray lowered front',(x,1.397,1.0525),(.388,.006,.025),'navy',sub,0)
  for i in range(8):
   ball('Counter ball',(x-.105+(i%4)*.07,1.21+(i//4)*.08,1.06135),.02135,('yellow','red','white')[i%3],sub,sides=8,rings=4)
 box('Rear stock shelf',(0,-2.05,1.4),(5.5,.38,.06),'wood',sub,0)
 box('Putter rack lower',(0,2.85,.22),(3.8,.32,.05),'wood',sub,0)
 box('Putter rack upper',(0,2.85,.91),(3.8,.23,.10),'wood',sub,0)
 for x in (-1.8,1.8):box('Rack upright',(x,2.85,.50),(.10,.12,.76),'wood',sub,0)
 for i in range(16):
  x=-1.72+i*.23;length=.63+(i%4)*.10
  cyl('Racked putter shaft',(x,2.85,.288),(x,2.85,.30+length),.005,'metal',sub,6)
  cyl('Putter grip',(x,2.85,.30+length-.15),(x,2.85,.30+length),.011,'black',sub,6)
  box('Putter blade',(x+.025,2.85,.2675),(.10,.035,.045),'red',sub,0)
 # Painted lap siding, separate corner casings and open framed windows.
 for j in range(18):
  z=.22+j*.135
  box('Rear clapboard',(0,-d/2-.084,z),(w,.025,.14),'ivory',sub,0)
  for side in (-1,1):
   box('Side clapboard',(side*(w/2+.084),0,z),(.025,d,.14),'ivory',sub,0)
 for side in (-1,1):
  for yy in (-d/2,d/2):box('Corner casing',(side*(w/2+.10),yy,1.40),(.055,.16,2.65),'white',sub)
 # Side windows: cut both wall and siding rather than lay glass on a wall.
 for side in (-1,1):
  wall=next(o for o in sub.children if o.name.startswith('Side wall') and o.location.x*side>0)
  cutter=box('Window opening tool',(side*w/2,-.50,1.63),(.55,1.35,.94),'black',sub,0)
  bpy.context.view_layer.update();G.boolean(wall,cutter)
  for ob in list(sub.children):
   if ob.name.startswith('Side clapboard') and ob.location.x*side>0 and 1.13<ob.location.z<2.13:
    bpy.data.objects.remove(ob,do_unlink=True)
  box('Side window glazing',(side*(w/2+.04),-.50,1.63),(.006,1.32,.90),'glass',sub,0)
  for yy in (-1.22,.22):box('Window casing',(side*(w/2+.08),yy,1.63),(.08,.14,1.10),'white',sub)
  for zz in (1.11,2.15):box('Window head and sill',(side*(w/2+.08),-.50,zz),(.11,1.52,.16),'white',sub)
  box('Window center mullion',(side*(w/2+.07),-.50,1.63),(.06,.045,.96),'white',sub)
 # Two captured channels let the operating sash slide behind the fixed pane.
 sash=root('Clubhouse__ServiceSash',(0,d/2-.245,1.6995),parent=sub);sash['module']=False;sash['slide_axis']='X';sash['range_m']=[-2.04,0]
 fixed_sash=root('ServiceFixedSash',(0,d/2-.18,1.6995),parent=sub);fixed_sash['module']=False
 for xx,frame in ((-1.02,fixed_sash),(1.02,sash)):
  box('Service sash glazing',(xx,0,.0),(2.00,.006,1.19),'glass',frame,0)
  for edge in (-.99,.99):box('Sash stile',(xx+edge,.025,0),(.035,.045,1.20),'white',frame)
  for zz in (-.60,.60):box('Sash rail',(xx,.025,zz),(2.02,.045,.035),'white',frame)
  for xg in (-.70,.70):box('Sash nylon glide',(xx+xg,.025,-.62375),(.030,.025,.0125),'black',frame,0)
 box('Sash rear timber saddle',(0,2.0775,1.04875),(4.30,.075,.0375),'wood',sub,0)
 box('Sash lower channel base',(0,2.12,1.0685),(4.30,.16,.002),'metal',sub,0)
 box('Sash upper channel base',(0,2.12,2.3315),(4.30,.16,.004),'metal',sub,0)
 for zz in (1.0845,2.3145):
  for yy in (2.04,2.115,2.185):box('Sash channel guide',(0,yy,zz),(4.30,.003,.030),'metal',sub,0)
 box('Sash meeting cover',(0,2.145,1.6995),(.045,.045,1.235),'white',sub)
 for xx in (-2.08,2.08):box('Service side jamb',(xx,2.12,1.6995),(.10,.20,1.26),'white',sub)
 # Canvas awning sags between four rafter supports.
 for stripe in range(16):
  vs=[]
  for j in range(7):
   q=j/6
   for xx in (stripe/16,(stripe+1)/16):vs.append((-2.5+5*xx,d/2+.04+q*1.12,2.52-.38*q-.055*math.sin(q*math.pi)))
  cloth=mesh('Striped service awning',vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(6)],'clothred' if stripe%2 else 'clothivory',sub,False)
  gauge=cloth.modifiers.new('Awning fabric gauge','SOLIDIFY');gauge.thickness=.002;gauge.offset=-.5
  box('Awning valance',(-2.5+(stripe+.5)*5/16,d/2+1.16,2.045),(5/16,.022,.19),'clothred' if stripe%2 else 'clothivory',sub,0)
 for xx in (-2.45,2.45):beam('Awning knee brace',(xx,d/2,1.85),(xx,d/2+1.10,2.14),.028,.028,'metal',sub)
 beam('Awning wall ledger',(-2.5,d/2+.04,2.50),(2.5,d/2+.04,2.50),.038,.038,'metal',sub)
 beam('Awning front bar',(-2.5,d/2+1.16,2.12),(2.5,d/2+1.16,2.12),.032,.032,'metal',sub)
 for xx in (-2.45,-1.22,0,1.22,2.45):
  tube('Awning rafter',[(xx,d/2+.04+j/6*1.12,2.50-.38*j/6-.055*math.sin(j/6*math.pi)) for j in range(7)],.016,'metal',sub,8)

 board=root('Service boards',(0,d/2+.0825,0),180,sub);board['module']=False
 # Both boards occupy the fixed left wall; none bridges the operating door.
 for zz in (1.68,.94):box('Menu backing',(2.85,0,zz),(.64,.025,.64),'navy',board,.008)
 for j,word in enumerate(('18 HOLES  $5','CHILDREN  $3','REPLAY  $2','OPEN 10 - 10')):text(board,word,(2.85,-.02,1.89-j*.14),.58,.11)
 for j,word in enumerate(('COLD DRINKS','SODA  $1','ICE CREAM $2','PLEASE RETURN')):text(board,word,(2.85,-.02,1.15-j*.14),.58,.11)
 label=root('Restroom door label',(.369,.027,1.38),180,door);label['module']=False
 text(label,'RESTROOM',(0,0,0),.58,.11)
 box('Service porch light',(2.45,d/2+.12,2.35),(.20,.14,.20),'yellow',sub,.014)
 socket(sub,'Counter',(0,d/2+.5,1.03),'service_counter');socket(sub,'Entry',(2.65,d/2+.6,.12),'entry')
 return sub

def bench(rt,p,yaw=0):
 sub=root('CourseBench',p,yaw,rt,kind='bench')
 box('Bench anchored concrete pad',(0,0,-.0825),(2.0,.85,.165),'concrete',sub,.005,1)
 for x in (-.56,.56):
  for y in (-.21,.21):box('Bench leg',(x,y,.23),(.075,.075,.46),'navy',sub,0)
  beam('Bench back support',(x,.20,.20),(x,.31,.87),.055,.055,'navy',sub,edge_radius=0)
 for y in (-.21,-.07,.07,.21):box('Bench seat board',(0,y,.47),(1.65,.125,.035),'wood',sub,0)
 for z in (.64,.80):box('Bench back board',(0,.30,z),(1.65,.035,.135),'wood',sub,0)
 return sub

def light(rt,p):
 sub=root('CourseLight',p,parent=rt,kind='light')
 box('Light footing',(0,0,.09),(.32,.32,.18),'concrete',sub,0)
 cyl('Course steel pole',(0,0,.18),(0,0,4.7),.0445,'navy',sub,12)
 for s in (-1,1):
  beam('Floodlight bracket',(0,0,4.60),(s*.31,0,4.65),.028,.028,'metal',sub,edge_radius=0)
  box('Floodlight cast housing',(s*.31,0,4.7),(.27,.19,.20),'navy',sub,.018,1)
  box('Floodlight lens',(s*.31,-.099,4.69),(.23,.014,.15),'white',sub,.005,1)
 socket(sub,'Emitter',(0,0,4.65),'light_emitter');return sub

def build(p,parent):
 global GRADING
 GRADING=p['water']
 W,D=p['lot'];rt=root('Site',parent=parent,kind='site')
 # Boolean the exact same original rim polygon out of the graded ground.
 # Retain only its terrain skin: buried walls/bottom are construction helpers.
 xs=(-W/2,-25,25,W/2) if p['water'] else (-W/2,W/2)
 ys=(-D/2,-7,28.5,D/2) if p['water'] else (-D/2,-7,D/2)
 # Bare outer embankments taper the raised course back to adjoining grade.
 # Every green, planted bed, bench and fence lies inside the full-grade core.
 top=[(x,y,.015+(grade(y) if not p['water'] or abs(x)<W/2 and y<D/2 else 0)) for y in ys for x in xs];n=len(top);verts=top+[(x,y,-2) for x,y,z in top]
 faces=[]
 nx,ny=len(xs),len(ys)
 for i in range(len(ys)-1):
  for k in range(nx-1):
   j=nx*i+k;face=(j,j+1,j+1+nx,j+nx);faces.extend((face,tuple(v+n for v in reversed(face))))
 boundary=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+j for j in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
 faces.extend((a,a+n,b+n,b) for a,b in zip(boundary,boundary[1:]+boundary[:1]))
 terrain=mesh('Site planted grade',verts,faces,'grass',rt)
 cutter=own(G.profile('Basin excavation tool',[(x,y) for x,y,z in pond_loops(p['water'])[0]],-3,3,M['grass'],axis='Z'),rt)
 bpy.context.view_layer.update();G.boolean(terrain,cutter)
 bm=bmesh.new();bm.from_mesh(terrain.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z<.5],context='FACES');bm.to_mesh(terrain.data);bm.free();terrain.data.update()
 # A common landscaped enclosure sits inside lawn perimeter buffers. Its
 # pond excavation shares the liner outline, so neither layer blocks water.
 if p['water']:
  outline=[(22.6*math.cos(j*math.tau/64)+.65*math.sin(j*3*math.tau/64),7+20.0*math.sin(j*math.tau/64)+.35*math.cos(j*4*math.tau/64)) for j in range(64)]
 else:outline=paths.court(p)
 bed=own(G.profile('Shared mulched landscape bed',outline,-1,.020,M['soil'],axis='Z'),rt)
 for v in bed.data.vertices:v.co.z+=grade(v.co.y)
 cutter=own(G.profile('Bed pond opening',[(x,y) for x,y,z in pond_loops(p['water'])[0]],-3,5,M['grass'],axis='Z'),rt)
 bpy.context.view_layer.update();G.boolean(bed,cutter)
 bm=bmesh.new();bm.from_mesh(bed.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z<.5],context='FACES');bm.to_mesh(bed.data);bm.free();bed.data.update()
 mulch_skin(bed)
 edging=[]
 for i,(x,y) in enumerate(outline):
  a=Vector(outline[i-1]);b=Vector(outline[(i+1)%len(outline)]);d=(b-a).normalized();normal=Vector((-d.y,d.x));z=.020+grade(y)
  edging.append([(x+normal.x*dx,y+normal.y*dx,z+dz) for dx,dz in ((-.0015,-.045),(.0015,-.045),(.0015,.025),(-.0015,.025))])
 own(G.loft('Formed steel mulch-bed edging',edging+[edging[0]],M['black'],caps=False),rt)
 for spec in landscape.beds(p):planted_bed(rt,spec)
 # Continuous shared beds replace individual lawn plots. Curved edge paths
 # follow each playing lane, with short crossovers only at the headlands.
 for h in p['holes']:
  # Walks follow the lane's broad alignment, not its tightly rounded tips.
  points=[]
  for i in range(27):
   t=i/26;cx,cy=center(h,t);side=paths.side(h)
   q=local(h,cx+side*paths.offset(h,t),cy,level(h,cx,t)-.055)
   if not h.get('crossing'):q=(q[0],q[1],.065+grade(q[1]))
   points.append(q)
  walk(rt,'Curving lane-side walk',points,1.524,span=bool(h.get('crossing')))
  for tag,t in (('tee',.08),('cup',.88)):
   cx,cy=center(h,t);side=paths.side(h);edge=local(h,cx+side*(halfwidth(h,t)+.02),cy,level(h,cx,t)+.0048)
   outer=local(h,cx+side*paths.offset(h,t),cy,level(h,cx,t)-.055)
   if not h.get('crossing'):outer=(outer[0],outer[1],.065+grade(outer[1]))
   walk(rt,'Open '+tag+' landing',[outer,edge],.78)
 if p['water']:
  pts=[]
  for j in range(97):
   a=j*math.tau/96;x=17.25*math.cos(a);y=7+14.85*math.sin(a);pts.append((x,y,.065+grade(y)))
  walk(rt,'Continuous inner circuit',pts,1.524)
  for name,line,start,end,span in paths.adventure_links(p):
   def extra(station):
    if station is None:return 0
    number,t=station;h=p['holes'][number-1];cx,cy=center(h,t);q=paths.lane(h)[0 if t==0 else -1]
    return (level(h,cx,t)-.055-(.065+grade(q[1]))) if h.get('crossing') else 0
   ea,eb=extra(start),extra(end);distances=[0]
   for a,b in zip(line,line[1:]):distances.append(distances[-1]+math.dist(a,b))
   route=[]
   for (x,y),distance in zip(line,distances):
    t=distance/distances[-1];blend=t*t*(3-2*t);route.append((x,y,.065+grade(y)+ea*(1-blend)+eb*blend))
   walk(rt,name,route,1.524,span=span)
 else:
  for line in paths.links(p):walk(rt,'Winding classic route connection',[(x,y,.065) for x,y in line],1.524)
 walk(rt,'Entrance path',[(0,p['clubhouse'][1]+2.3,.065),(0,-10.6 if p['water'] else -12,.065)],1.8)
 if p['water']:
  walk(rt,'Footbridge west landing',[(-5.0,-7.1,.065+grade(-7.1)),(-1.8,-7.1,.244)],1.524)
  walk(rt,'Footbridge east landing',[(1.8,-7.1,.244),(5.0,-7.1,.065+grade(-7.1))],1.524)
 if p['water']:
  for j in range(10):
   y=7.1+j*.34;top=.95+(j+1)*.15
   tread=box('Quarry stair tread',(5.9,y,top/2),(1.45,.34,top),'rocklight',rt,.008);tread['walking_surface']=True
  walk(rt,'Upper quarry ledge',[(5.9,10.5,2.45),(6.3,12.2,2.45),(7.0,14.0,2.45)],1.524)
  for side in (-1,1):
   beam('Quarry stair handrail',(5.9+side*.70,7.05,2.02),(5.9+side*.70,10.35,3.52),.038,.038,'wood',rt)
   for j in (0,4,9):
    y=7.1+j*.34;top=.95+(j+1)*.15;box('Quarry guard post',(5.9+side*.70,y,top+.48),(.07,.07,.96),'wood',rt)
 basin(rt,p['water']);clubhouse(p,rt)
 # A real parking row and two-way aisle enter off the road, separate from play.
 front=-D/2;py=front+6.4008
 box('Parking paved court',(4,py,.018),(W-10,12.8016,.035),'asphalt',rt,0)
 # 18 ft stalls behind a full 24 ft two-way aisle. The hut occupies the
 # middle three positions; the driving aisle remains clear in front of it.
 for x in [(-W/2+9+i*2.7432) for i in range(int((W-10)/2.7432)+1)]:
  if abs(x)<4.4:continue
  box('Parking stall stripe',(x,front+10.0584,.039),(.09,5.4864,.001),'white',rt,0)
 walk(rt,'Parking head walk',[(-W/2+9,front+13.5636),(W/2-1,front+13.5636)],1.524,.065)
 for x in p['driveways']:
  socket(rt,'Driveway_%d'%int(x*100),(x,front,0),'driveway')
 # Nailed-face treated three-rail fence; exact endpoints and shared corner
 # posts avoid dangling last rails or doubled members outside the parcel.
 left,right,fy,back=p['fence_bounds'];seen=set()
 def fence_run(a,b,outward):
  length=math.dist(a,b);n=math.ceil(length/2.4384)
  stations=[(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n) for i in range(n+1)]
  for x,y in stations:
   key=(round(x,5),round(y,5))
   if key not in seen:box('Fence post',(x,y,.59+grade(y)),(.0889,.0889,1.18),'wood',rt,0);seen.add(key)
  for (x0,y0),(x1,y1) in zip(stations,stations[1:]):
   for z in (.30,.65,.99):
    if abs(x1-x0)<1e-6:
     dy=y1-y0;dz=grade(y1)-grade(y0)
     ob=box('Supported fence rail',((x0+x1)/2+outward*.0635,(y0+y1)/2,z+(grade(y0)+grade(y1))/2),(.0381,math.hypot(dy,dz),.0889),'wood',rt,0);ob.rotation_euler.x=math.atan2(dz,dy)
    else:box('Supported fence rail',((x0+x1)/2,(y0+y1)/2+outward*.0635,z+grade(y0)),(abs(x1-x0),.0381,.0889),'wood',rt,0)
 fence_run((left,fy),(left,back),-1);fence_run((right,fy),(right,back),1)
 fence_run((left,back),(right,back),1)
 fence_run((left,fy),(-5,fy),-1);fence_run((5,fy),(right,fy),-1)
 bench_x=23.2 if p['water'] else W/2-2
 for pos in (((-5,-12,.065) if p['water'] else (-2.5,-10,.065)),(5.5,22,.065),(-bench_x,6,.065),(bench_x,6,.065)):bench(rt,(pos[0],pos[1],pos[2]+grade(pos[1])),180 if pos[1]>0 else 0)
 lamp_x=22.9 if p['water'] else W/2-2
 light_positions=[(-lamp_x,-12,0),(-lamp_x,21,0),(lamp_x,-12,0),(lamp_x,21,0)]
 light_positions+=([(5,0,0),(-14,-4,0),(14,1,0),(-10,17,0),(11,18,0)] if p['water'] else [(-1.7,-5.4,0),(-1.7,14.8,0),(-W/2+2,5,0),(W/2-2,5,0),(-1.7,9.8,0)])
 for pos in light_positions:light(rt,(pos[0],pos[1],grade(pos[1])))
 # Internally lit roadside pylon with a real steel column and cabinet returns.
 sign=root('RoadSign',(-W/2+4,-D/2+2,0),parent=rt,kind='sign')
 box('Pylon concrete plinth',(0,0,.22),(1.2,.85,.44),'concrete',sign,.025)
 box('Pylon steel column',(0,0,2.8),(.35,.28,5.6),'navy',sign,.014)
 box('Lit sign cabinet',(0,0,5.2),(5.0,.42,1.8),'navy',sign,.05,2)
 box('Opal sign face',(0,-.222,5.2),(4.82,.025,1.61),'ivory',sign,.012)
 text(sign,'@pylon:'+p['name'],(0,-.240,5.2),4.82,1.61)
 for x in (-.42,.42):
  box('Sign service foot',(x,0,.47),(.14,.50,.05),'metal',sign)
  for y in (-.17,.17):cyl('Pylon anchor bolt',(x,y,.47),(x,y,.53),.015,'metal',sign,8)
 rear=root('Pylon reverse face',(0,.24,5.2),180,sign);rear['module']=False
 box('Opal sign face',(0,.016,0),(4.82,.025,1.61),'ivory',rear,.012)
 text(rear,'@pylon:'+p['name'],(0,0,0),4.82,1.61)
 socket(sign,'Light',(0,-.23,5.2),'sign_emitter')
 return rt
