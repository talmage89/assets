"""Course site construction, water containment and serviceable public fixtures."""
import math,random
from geometry import *
from fixtures import roof
from plan import center,halfwidth,level,local

GRADING=False
def grade(y):return .025*max(0,y+9) if GRADING else 0

def walk(rt,name,points,width=1.524,z=.065):
 vs=[]
 for i,p in enumerate(points):
  a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)]);d=(b-a).normalized();n=Vector((-d.y,d.x))
  for side in (-1,1):vs.append((p[0]+side*n.x*width/2,p[1]+side*n.y*width/2,(p[2] if len(p)>2 else z+(grade(p[1]) if z>=0 else 0))))
 return mesh(name,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)],'concrete',rt,False)

def footbridge(rt,p=(0,-4,0)):
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

def basin(rt,adv):
 water=root('WaterSystem',parent=rt,kind='water_system')
 cx,cy=(0,5) if adv else (0,5);rx,ry=(3.6,7.0) if adv else (1.1,2.7);n=64
 loops=[]
 for z,f in ((.035,1.15),(-.08,1.02),(-.57,.80)):
  loops.append([(cx+rx*f*(1+.035*math.sin(i*2.7))*math.cos(i*math.tau/n),cy+ry*f*(1+.025*math.sin(i*3.1))*math.sin(i*math.tau/n),z) for i in range(n)])
 own(G.loft('Folded protected EPDM basin',loops,M['liner'],caps=False),water)
 mesh('Pond liner floor',loops[-1],[tuple(range(n))],'liner',water,False)
 edge=loops[1];mesh('Pond still water',[(x*.97,cy+(y-cy)*.97,-.17) for x,y,z in edge],[tuple(range(n))],'water',water,False)
 for i in range(n):
  a=i*math.tau/n;x=cx+rx*1.09*math.cos(a);y=cy+ry*1.08*math.sin(a)
  rock('Restrained pond-edge coping',(x,y,-.13),(.70,.75,.43),water,100+i,'rocklight')
  if i%8==0:
   # Wet exposed liner folds, with a visibly restrained upper edge beneath rock.
   tube('Liner bank fold',[(x*.99,cy+(y-cy)*.99,-.06),(x*.95,cy+(y-cy)*.95,-.32),(x*.90,cy+(y-cy)*.90,-.54)],.012,'liner',water)
 for i in range(5):
  a=i*2.4;ball('Lost pond ball',(.9*math.sin(a),cy+.7*i,-.54865),.02135,'white' if i%2 else 'yellow',water)
 if adv:
  # Waterfall is a supported ledged shotcrete mass on the pond's east bank.
  for i,(p,size) in enumerate((((3.0,9.8,-.10),(2.8,3.4,1.2)),((3.2,10.8,.65),(2.3,2.2,.70)),((2.5,9.2,.28),(1.6,1.5,.45)))):
   rock('Sculpted shotcrete outcrop',p,size,water,290+i)
  box('Waterfall stainless spill lip',(2.05,9.15,.88),(1.30,.19,.025),'metal',water,.003,2)
  # Flow cross-section curls over lip and breaks in width; no rigid blue wall.
  vs=[];fs=[]
  for j in range(9):
   t=j/8
   for i in range(15):
    u=i/14;vs.append((1.4+u*1.30,9.12-.25*math.sin(t*math.pi/2),.89-1.05*t+.035*math.sin(u*43+t*5)*t))
  for j in range(8):
   for i in range(14):k=j*15+i;fs.append((k,k+1,k+16,k+15))
  mesh('Falling water curtain',vs,fs,'water',water,False)
  for i in range(10):
   a=i*.71;rock('Water impact foam',(2.03+.70*math.sin(a),8.82+.18*math.cos(a),-.16),(.26,.14,.025),water,710+i,'foam')
  # Stream from lower pond, bank protection continuing under the human bridge.
  points=[(0,5-ry),(0,-2.7),(.10,-4),(-.20,-6.0),(0,-7.1)]
  walk(water,'Stream liner',points,1.65,-.31);walk(water,'Stream flow',points,1.1,-.165)
  for ob in water.children:
   if ob.name.startswith('Stream liner'):ob.data.materials.clear();ob.data.materials.append(M['liner'])
   if ob.name.startswith('Stream flow'):ob.data.materials.clear();ob.data.materials.append(M['water'])
  for y in (-2.3,-3,-4,-5,-6.0,-6.8):
   for x in (-.82,.82):rock('Stream bank stone',(x,y,-.15),(.5,.65,.37),water,int((y+9)*100+x*30))
  footbridge(rt)
  # Return pipe follows the buried bank; only service ends are exposed.
  tube('63 mm return service pipe',[(4.1,8.8,.05),(4.1,9.5,.05),(3.9,10.5,.66),(3.1,10.5,.85)],.0315,'black',water,10)
  box('Pump service vault',(4.9,8.8,.12),(.75,.85,.24),'concrete',water)
  box('Pump service lid',(4.9,8.8,.25),(.78,.88,.025),'metal',water)
  box('Screened intake',(2.9,6.7,-.22),(.38,.38,.11),'black',water)
  for i in range(7):box('Intake screen bar',(2.75+i*.05,6.7,-.156),(.012,.35,.015),'metal',water)
 socket(water,'Pump',(4.9,8.8,.25),'water_pump');socket(water,'WaterLevel',(0,5,-.17),'water_level')
 return water

def clubhouse(p,rt):
 x,y=p['clubhouse'];sub=root('Clubhouse',(x,y,.06),parent=rt,kind='clubhouse');w,d=6.8,4.6
 box('Hut slab',(0,0,.06),(w+.4,d+.4,.12),'concrete',sub)
 # Open counter faces course +Y. Actual framed walls, recess, inside floor.
 box('Back wall',(0,-d/2,1.35),(w,.14,2.7),'ivory',sub)
 for s in (-1,1):box('Side wall',(s*w/2,0,1.35),(.14,d,2.7),'ivory',sub)
 box('Counter sill wall',(0,d/2,.50),(4.3,.14,1.0),'wood',sub)
 box('Counter header',(0,d/2,2.46),(w,.17,.48),'wood',sub)
 for x in (-3.1,-2.2,2.2,3.1):box('Counter jamb',(x,d/2,1.70),(.14,.17,1.4),'wood',sub)
 box('Open service counter',(0,d/2+.14,1.03),(4.4,.65,.075),'red',sub,.018,2)
 box('Sheltered counter ceiling',(0,0,2.66),(w,d,.10),'wood',sub)
 roof(sub,'Hut pitched roof',w+.65,d+.9,2.73,1.1)
 # Small operating entry in the side bay, physical hinge at jamb.
 door=root('Clubhouse__Door',(2.29,d/2-.04,.13),parent=sub);door['module']=False;door['pivot_axis']='Z';door['range_degrees']=[-100,0]
 box('Entry leaf',(.369,0,1.025),(.690,.045,2.05),'red',door)
 cyl('Entry pull',(.63,-.05,.90),(.63,-.05,1.14),.012,'metal',door)
 for z in (.40,1.70):
  box('Fixed hinge strap',(2.24,d/2-.04,z+.075),(.10,.025,.010),'metal',sub)
  cyl('Fixed hinge pin',(2.29,d/2-.04,z+.08),(2.29,d/2-.04,z+.18),.008,'metal',sub,12)
  ring('Moving hinge barrel',(0,0),.015,.009,z-.04,z+.04,'metal',door,12)
  box('Moving hinge strap',(.054,0,z),(.082,.020,.065),'metal',door)
 # Counter-facing signs are flipped so their fronts face +Y.
 sign=root('Clubhouse sign',(0,d/2+.11,2.44),180,sub);sign['module']=False
 text(sign,p['name'].upper(),(0,0,0),3.5,.27)
 # Actual interior stock visible through the opening.
 for x in (-1.55,0,1.55):
  box('Ball sorting tray',(x,1.25,1.09),(.68,.48,.12),'navy',sub)
  for i in range(8):
   ball('Counter ball',(x-.23+(i%4)*.15,1.15+(i//4)*.15,1.17),.02135,('yellow','red','white')[i%3],sub)
 box('Rear stock shelf',(0,-1.8,1.4),(5.5,.38,.06),'wood',sub)
 box('Putter rack lower',(0,2.85,.25),(3.8,.32,.12),'wood',sub)
 box('Putter rack upper',(0,2.85,.91),(3.8,.23,.10),'wood',sub)
 for i in range(16):
  x=-1.72+i*.23;length=.63+(i%4)*.10
  cyl('Racked putter shaft',(x,2.85,.30),(x,2.85,.30+length),.005,'metal',sub,8)
  cyl('Putter grip',(x,2.85,.30+length-.15),(x,2.85,.30+length),.011,'black',sub,8)
  box('Putter blade',(x+.025,2.85,.27),(.10,.035,.045),'red',sub)
 socket(sub,'Counter',(0,d/2+.5,1.03),'service_counter');socket(sub,'Entry',(2.65,d/2+.6,.12),'entry')
 return sub

def bench(rt,p,yaw=0):
 sub=root('CourseBench',p,yaw,rt,kind='bench')
 for x in (-.56,.56):
  for y in (-.21,.21):box('Bench leg',(x,y,.23),(.075,.075,.46),'navy',sub)
  beam('Bench back support',(x,.20,.20),(x,.31,.87),.055,.055,'navy',sub)
 for y in (-.21,-.07,.07,.21):box('Bench seat board',(0,y,.47),(1.65,.125,.035),'wood',sub)
 for z in (.64,.80):box('Bench back board',(0,.30,z),(1.65,.035,.135),'wood',sub)
 return sub

def light(rt,p):
 sub=root('CourseLight',p,parent=rt,kind='light')
 box('Light footing',(0,0,.09),(.32,.32,.18),'concrete',sub)
 cyl('Course steel pole',(0,0,.18),(0,0,4.7),.0445,'navy',sub,12)
 for s in (-1,1):
  beam('Floodlight bracket',(0,0,4.60),(s*.31,0,4.65),.028,.028,'metal',sub)
  box('Floodlight cast housing',(s*.31,0,4.7),(.27,.19,.20),'navy',sub,.018,2)
  box('Floodlight lens',(s*.31,-.099,4.69),(.23,.014,.15),'white',sub,.005,2)
 socket(sub,'Emitter',(0,0,4.65),'light_emitter');return sub

def build(p,parent):
 global GRADING
 GRADING=p['water']
 W,D=p['lot'];rt=root('Site',parent=parent,kind='site')
 # Grade skin with a real basin/stream opening. Carpeted holes sit above it.
 xs=sorted(set([-W/2,W/2,-4.5,4.5,-1,1]));ys=sorted(set([-D/2,D/2,-7.5,-2,12.9]))
 vs=[];fs=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   if p['water'] and ((-4.5<(a+b)/2<4.5 and -2<(c+d)/2<12.9) or (-1<(a+b)/2<1 and -7.5<(c+d)/2<-2)):continue
   # Both kinds have ponds; classic cut is generated separately below.
   if not p['water'] and -4.5<(a+b)/2<4.5 and -2<(c+d)/2<12.9:continue
   k=len(vs);vs.extend(((a,c,.015+grade(c)),(b,c,.015+grade(c)),(b,d,.015+grade(d)),(a,d,.015+grade(d))));fs.append((k,k+1,k+2,k+3))
 mesh('Site planted grade',vs,fs,'grass',rt,False)
 # Fill around the precise pond edge down to basin rim; ellipse skirt avoids
 # visible rectangular excavation corners in overhead and close views.
 rx,ry=(3.6,7) if p['water'] else (1.1,2.7);n=64;loops=[]
 for mode in (0,1):
  loop=[]
  for i in range(n):
   a=i*math.tau/n;x=math.cos(a);y=math.sin(a)
   if mode==0:
    factor=min(4.5/max(abs(x),1e-9),(7.9 if y>0 else 7.0)/max(abs(y),1e-9));xx=x*factor;yy=y*factor+5
   else:xx=x*rx*1.15;yy=5+y*ry*1.15
   loop.append((xx,yy,.015+grade(yy) if mode==0 else .032))
  loops.append(loop)
 own(G.loft('Pond planted bank',loops,M['grass'],caps=False),rt)
 # Paved serpentine route outside each playing envelope, continuous headlands.
 xs=(-26.4,-19.4,-12.4,5.6,12.6,19.6) if p['water'] else (-21.4,-14.4,-7.4,.6,7.6,14.6)
 for x in xs:walk(rt,'Connected side walk',[(x,y) for y in (-12,-9,0,11,22)],1.524)
 for y in (-12,22):walk(rt,'Connecting headland',[(-W/2+1.4,y),(W/2-1.4,y)],1.524)
 for h in p['holes']:
  # Short approach from tee to its nearest route, plus separate exit from cup.
  for tag in ('tee','cup'):
   q=h[tag];x=min(xs,key=lambda x:abs(x-q[0]));walk(rt,'Hole %d %s approach'%(h['number'],tag),[(x,q[1],.070+grade(q[1])),(q[0],q[1],q[2])],1.0)
 # Central entrance route to both lobes, using the human bridge at the stream.
 walk(rt,'Entrance path',[(0,p['clubhouse'][1]+2.3),(0,-12)],1.8)
 for x in (-5.5,5.5):walk(rt,'Water-side promenade',[(x,y) for y in (-12,-9,0,11,22)],1.524)
 if p['water']:walk(rt,'Footbridge west landing',[(-5.5,-4,.065),(-1.8,-4,.244)],1.524);walk(rt,'Footbridge east landing',[(1.8,-4,.244),(5.5,-4,.065)],1.524)
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
 fy=-13.5;seen=set()
 def fence_run(a,b,outward):
  length=math.dist(a,b);n=math.ceil(length/2.4384)
  stations=[(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n) for i in range(n+1)]
  for x,y in stations:
   key=(round(x,5),round(y,5))
   if key not in seen:box('Fence post',(x,y,.59+grade(y)),(.0889,.0889,1.18),'wood',rt);seen.add(key)
  for (x0,y0),(x1,y1) in zip(stations,stations[1:]):
   for z in (.30,.65,.99):
    if abs(x1-x0)<1e-6:
     dy=y1-y0;dz=grade(y1)-grade(y0)
     ob=box('Supported fence rail',((x0+x1)/2+outward*.0635,(y0+y1)/2,z+(grade(y0)+grade(y1))/2),(.0381,math.hypot(dy,dz),.0889),'wood',rt);ob.rotation_euler.x=math.atan2(dz,dy)
    else:box('Supported fence rail',((x0+x1)/2,(y0+y1)/2+outward*.0635,z+grade(y0)),(abs(x1-x0),.0381,.0889),'wood',rt)
 left,right=-W/2+.65,W/2-.65;back=D/2-.65
 fence_run((left,fy),(left,back),-1);fence_run((right,fy),(right,back),1)
 fence_run((left,back),(right,back),1)
 fence_run((left,fy),(-5,fy),-1);fence_run((5,fy),(right,fy),-1)
 for pos in ((-5,-12,.065),(5.5,22,.065),(-W/2+2,6,.065),(W/2-2,6,.065)):bench(rt,(pos[0],pos[1],pos[2]+grade(pos[1])),180 if pos[1]>0 else 0)
 for pos in ((-W/2+2,-12,0),(-W/2+2,21,0),(W/2-2,-12,0),(W/2-2,21,0),(5,0,0)):light(rt,(pos[0],pos[1],grade(pos[1])))
 # Fictional road sign on two steel supports; readable course, never real branding.
 sign=root('RoadSign',(-W/2+4,-D/2+2,0),parent=rt,kind='sign')
 for x in (-1.3,1.3):box('Road sign post',(x,0,2.0),(.10,.10,4.0),'navy',sign)
 box('Road sign cabinet',(0,0,3.5),(4.4,.22,1.25),'red' if p['kind']=='classic' else 'navy',sign,.04,2)
 text(sign,p['name'].upper(),(0,-.12,3.76),4.10,.43);text(sign,'18 HOLES  •  MINI GOLF',(0,-.12,3.22),4.0,.25)
 return rt
