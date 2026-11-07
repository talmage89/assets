"""Course site construction, water containment and serviceable public fixtures."""
import math,random
from geometry import *
from fixtures import roof
from plan import center,halfwidth,level,local

GRADING=False
def grade(y):return .065*max(0,y+7) if GRADING else 0

def walk(rt,name,points,width=1.524,z=.065):
 vs=[]
 for i,p in enumerate(points):
  a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)]);d=(b-a).normalized();n=Vector((-d.y,d.x))
  for side in (-1,1):vs.append((p[0]+side*n.x*width/2,p[1]+side*n.y*width/2,(p[2] if len(p)>2 else z+(grade(p[1]) if z>=0 else 0))))
 ob=mesh(name,vs,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(points)-1)],'concrete',rt,False)
 if z>=0:
  bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0]);bm.to_mesh(ob.data);bm.free();ob.data.update()
  mod=ob.modifiers.new('Walk slab gauge','SOLIDIFY');mod.thickness=.10;mod.offset=-1
 return ob

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
   loop.append((x,y,zz))
  loops.append(loop)
 return loops

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
  t=(-.17-mid[2])/(floor[2]-mid[2]);surface.append((mid[0]*(1-t)+floor[0]*t,mid[1]*(1-t)+floor[1]*t,-.17))
 mesh('Continuous pond and stream water',surface,[tuple(range(len(surface)))],'water',water,False)
 rim=[(x,y,z-.10) for x,y,z in loops[0]]
 rockwall('Continuous mortared pond coping',rim,.48,.27,water,517,closed=True)
 for i in range(0,len(rim),7):
  x,y,z=rim[i];rock('Embedded irregular fieldstone',(x,y,z-.08),(.75+.15*math.sin(i),.58,.38),water,118+i,'rocklight')
 for i in range(5):
  a=i*2.4;ball('Lost pond ball',(.9*math.sin(a),cy+.7*i,-.54865),.02135,'white' if i%2 else 'yellow',water)
 if adv:
  # One continuous stratified mountain, with three independent spill shelves.
  mountain=rock('Quarry mountain',(3.5,11.1,-.10),(7.0,6.8,3.1),water,290,'rocklight')
  cutter=box('Recessed fall channel tool',(2.0,8.1,1.6),(2.40,4.75,3.8),'black',water,0)
  bpy.context.view_layer.update();G.boolean(mountain,cutter)
  rock('Fractured fall west cheek',(.62,10.2,-.06),(1.10,2.1,2.45),water,300,'rocklight')
  rock('Fractured fall east cheek',(3.40,10.3,-.05),(1.35,2.6,2.80),water,302,'rocklight')
  rock('Western terraced outcrop',(-5.0,14.6,.4),(3.8,5.0,2.4),water,294,'rocklight')
  for j,(yy,zz,width) in enumerate(((10.20,2.48,1.15),(9.60,1.63,1.55),(8.95,.72,1.9))):
   box('Recessed spill lip',(2.0,yy,zz),(width,.36,.025),'metal',water,.004,1)
   rock('Overhanging spill shelf',(2.0,yy+.40,zz-.22),(width+1.1,.85,.26),water,330+j,'rocklight')
   vs=[];fs=[]
   for v in range(9):
    t=v/8
    for u in range(17):
     q=u/16;vs.append((2+(q-.5)*width,yy-.18-.30*math.sin(t*math.pi/2),zz-.88*t+.02*math.sin(q*46+t*7)*t))
   for v in range(8):
    for u in range(16):k=v*17+u;fs.append((k,k+1,k+18,k+17))
   mesh('Aerated water cascading sheet',vs,fs,'water',water,False)
   for i in range(6):
    a=i*2.1;rock('Splash plume',(2+width*.36*math.sin(a),yy-.48+.15*math.cos(a),zz-.87),(.40,.23,.035),water,710+i,'foam')
  # The continuous basin above already contains the protected stream.
  footbridge(rt)
  for j,yy in enumerate((-3.0,-5.6)):
   rockwall('Stream bedrock riffle',[(-.70,yy,-.22),(-.25,yy+.12,-.20),(.2,yy-.1,-.21),(.68,yy+.05,-.22)],.32,.075,water,850+j,'rock')
   for k in range(5):
    rock('Riffle aeration',(-.52+k*.26,yy-.22,-.158),(.22,.31,.018),water,880+k,'foam')
  # Gravity deposits collect at sheltered bends rather than across the pool.
  for j in range(24):
   a=j*2.4;x=-2.3+.45*math.sin(a);y=5.4+.9*math.cos(a)
   mesh('Water-edge fallen leaf',[(x-.025,y,-.165),(x,y+.045,-.161),(x+.025,y,-.165),(x,y-.045,-.166)],[(0,1,2,3)],'leaf',water,False)
  # Return pipe follows the buried bank; only service ends are exposed.
  tube('63 mm return service pipe',[(4.1,8.8,.05),(4.1,9.5,.05),(3.9,10.5,1.90),(3.1,10.5,2.48),(2.0,10.30,2.48)],.0315,'black',water,10)
  box('Pump service vault',(4.9,8.8,grade(8.8)-.09),(.75,.85,.24),'concrete',water)
  box('Pump service lid',(4.9,8.8,grade(8.8)+.0425),(.78,.88,.025),'metal',water)
  box('Screened intake',(2.9,6.7,-.22),(.38,.38,.11),'black',water)
  tube('Intake bank connection',[(3.05,6.7,-.22),(3.5,6.7,-.22)],.0315,'black',water,10)
  for i in range(7):box('Intake screen bar',(2.75+i*.05,6.7,-.156),(.012,.35,.015),'metal',water)
 socket(water,'Pump',(4.9,8.8,.25),'water_pump');socket(water,'WaterLevel',(0,5,-.17),'water_level')
 return water

def clubhouse(p,rt):
 x,y=p['clubhouse'];sub=root('Clubhouse',(x,y,.06),parent=rt,kind='clubhouse');w,d=6.8,4.6
 box('Hut slab',(0,.6,.06),(w+.4,d+1.6,.12),'concrete',sub)
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
 door=root('Clubhouse__Door',(2.29,d/2-.04,.13),parent=sub);door['module']=False;door['pivot_axis']='Z';door['range_degrees']=[-90,0]
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
 # Actual interior stock sits on a supported worktop behind the opening.
 box('Inner worktop',(0,1.55,1.0),(4.4,1.50,.06),'wood',sub)
 for x in (-1.8,1.8):
  box('Counter rear support',(x,.86,.545),(.10,.10,.85),'wood',sub)
 # Actual interior stock visible through the opening.
 for x in (-1.55,0,1.55):
  box('Ball sorting tray',(x,1.25,1.09),(.68,.48,.12),'navy',sub)
  for i in range(8):
   ball('Counter ball',(x-.23+(i%4)*.15,1.15+(i//4)*.15,1.17),.02135,('yellow','red','white')[i%3],sub)
 box('Rear stock shelf',(0,-2.05,1.4),(5.5,.38,.06),'wood',sub)
 box('Putter rack lower',(0,2.85,.22),(3.8,.32,.05),'wood',sub)
 box('Putter rack upper',(0,2.85,.91),(3.8,.23,.10),'wood',sub)
 for x in (-1.8,1.8):box('Rack upright',(x,2.85,.50),(.10,.12,.76),'wood',sub)
 for i in range(16):
  x=-1.72+i*.23;length=.63+(i%4)*.10
  cyl('Racked putter shaft',(x,2.85,.288),(x,2.85,.30+length),.005,'metal',sub,8)
  cyl('Putter grip',(x,2.85,.30+length-.15),(x,2.85,.30+length),.011,'black',sub,8)
  box('Putter blade',(x+.025,2.85,.2675),(.10,.035,.045),'red',sub)
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
  box('Side window glazing',(side*(w/2+.04),-.50,1.63),(.016,1.32,.90),'glass',sub,0)
  for yy in (-1.22,.22):box('Window casing',(side*(w/2+.12),yy,1.63),(.08,.09,1.10),'white',sub)
  for zz in (1.11,2.15):box('Window head and sill',(side*(w/2+.12),-.50,zz),(.11,1.52,.09),'white',sub)
  box('Window center mullion',(side*(w/2+.14),-.50,1.63),(.06,.045,.96),'white',sub)
 # Sliding service sash stows above the open counter. Its own track/pivot
 # records a real translational range without filling the operating opening.
 sash=root('Clubhouse__ServiceSash',(0,d/2-.18,1.86),parent=sub);sash['module']=False;sash['slide_axis']='X';sash['range_m']=[0,.82]
 for xx in (-1.02,1.02):
  box('Service sash glazing',(xx,0,.0),(1.92,.018,.55),'glass',sash,0)
  for edge in (-.99,.99):box('Sash stile',(xx+edge,.025,0),(.035,.045,.61),'white',sash)
  for zz in (-.30,.30):box('Sash rail',(xx,.025,zz),(2.02,.045,.035),'white',sash)
 for zz in (1.49,2.22):box('Sliding sash track',(0,d/2-.09,zz),(4.30,.03,.045),'metal',sub)
 # Canvas awning sags between four rafter supports.
 for stripe in range(16):
  vs=[]
  for j in range(7):
   q=j/6
   for xx in (stripe/16,(stripe+1)/16):vs.append((-2.5+5*xx,d/2+.04+q*1.12,2.52-.38*q-.055*math.sin(q*math.pi)))
  mesh('Striped service awning',vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(6)],'red' if stripe%2 else 'ivory',sub,False)
  box('Awning valance',(-2.5+(stripe+.5)*5/16,d/2+1.16,2.045),(5/16,.022,.19),'red' if stripe%2 else 'ivory',sub,0)
 for xx in (-2.45,2.45):beam('Awning knee brace',(xx,d/2,1.85),(xx,d/2+1.10,2.14),.028,.028,'metal',sub)
 board=root('Service boards',(0,d/2+.13,0),180,sub);board['module']=False
 for xx in (-2.70,2.70):box('Menu backing',(xx,0,1.62),(.64,.025,1.1),'navy',board,.008)
 for j,word in enumerate(('18 HOLES  $5','CHILDREN  $3','REPLAY  $2','OPEN 10 - 10')):text(board,word,(-2.70,-.02,1.95-j*.19),.58,.11)
 for j,word in enumerate(('COLD DRINKS','SODA  $1','ICE CREAM $2','PLEASE RETURN')):text(board,word,(2.70,-.02,1.95-j*.19),.58,.11)
 text(board,'RESTROOM',(-2.70,-.02,.86),.58,.11)
 box('Service porch light',(2.45,d/2+.12,2.35),(.20,.14,.20),'yellow',sub,.014)
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
 # Boolean the exact same original rim polygon out of the graded ground.
 # Retain only its terrain skin: buried walls/bottom are construction helpers.
 ys=sorted(set((-D/2,-7,D/2)));top=[(x,y,.015+grade(y)) for y in ys for x in (-W/2,W/2)];n=len(top);verts=top+[(x,y,z-1.5) for x,y,z in top]
 faces=[]
 for i in range(len(ys)-1):
  j=2*i;faces.extend(((j,j+1,j+3,j+2),(n+j+2,n+j+3,n+j+1,n+j)))
 boundary=[0,1,3,5,4,2]
 faces.extend((boundary[i],boundary[(i+1)%6],n+boundary[(i+1)%6],n+boundary[i]) for i in range(6))
 terrain=mesh('Site planted grade',verts,faces,'grass',rt)
 cutter=own(G.profile('Basin excavation tool',[(x,y) for x,y,z in pond_loops(p['water'])[0]],-3,3,M['grass'],axis='Z'),rt)
 bpy.context.view_layer.update();G.boolean(terrain,cutter)
 bm=bmesh.new();bm.from_mesh(terrain.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z<.5],context='FACES');bm.to_mesh(terrain.data);bm.free();terrain.data.update()
 # A common landscaped enclosure sits inside lawn perimeter buffers. Its
 # pond excavation shares the liner outline, so neither layer blocks water.
 if p['water']:
  outline=[(22.6*math.cos(j*math.tau/64)+.65*math.sin(j*3*math.tau/64),7+20.0*math.sin(j*math.tau/64)+.35*math.cos(j*4*math.tau/64)) for j in range(64)]
 else:outline=[(-21,-11.8),(18.7,-11.8),(19.7,20.8),(-21.8,20.8)]
 bed=own(G.profile('Shared mulched landscape bed' if p['water'] else 'Classic shared concrete court',outline,-1,.020,M['soil' if p['water'] else 'concrete'],axis='Z'),rt)
 for v in bed.data.vertices:v.co.z+=grade(v.co.y)
 cutter=own(G.profile('Bed pond opening',[(x,y) for x,y,z in pond_loops(p['water'])[0]],-3,5,M['grass'],axis='Z'),rt)
 bpy.context.view_layer.update();G.boolean(bed,cutter)
 bm=bmesh.new();bm.from_mesh(bed.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z<.5],context='FACES');bm.to_mesh(bed.data);bm.free();bed.data.update()
 # Continuous shared beds replace individual lawn plots. Curved edge paths
 # follow each playing lane, with short crossovers only at the headlands.
 for h in p['holes']:
  points=[]
  for i in range(27):
   t=i/26;cx,cy=center(h,t);side=-1
   q=local(h,cx+side*(halfwidth(h,t)+1.05),cy,level(h,cx,t)-.055)
   points.append(q)
  walk(rt,'Curving lane-side walk',points,1.524)
  for tag,t in (('tee',.08),('cup',.88)):
   cx,cy=center(h,t);edge=local(h,cx-halfwidth(h,t)-.02,cy,level(h,cx,t)+.0048)
   outer=local(h,cx-halfwidth(h,t)-1.05,cy,level(h,cx,t)-.055)
   walk(rt,'Open '+tag+' landing',[outer,edge],.78)
 if p['water']:
  pts=[]
  for j in range(97):
   a=j*math.tau/96;x=17.25*math.cos(a);y=7+14.85*math.sin(a);pts.append((x,y,.065+grade(y)))
  walk(rt,'Continuous inner circuit',pts,1.524)
 else:
  for y in (-10.6,20.6):
   pts=[(-19+i*1.2,y+.36*math.sin(i*.7),.065) for i in range(31)]
   walk(rt,'Shared paved headland',pts,1.524)
 walk(rt,'Entrance path',[(0,p['clubhouse'][1]+2.3,.065),(0,-10.6,.065)],1.8)
 if p['water']:
  walk(rt,'Footbridge west landing',[(-5.0,-4,.065+grade(-4)),(-1.8,-4,.244)],1.524)
  walk(rt,'Footbridge east landing',[(1.8,-4,.244),(5.0,-4,.065+grade(-4))],1.524)
 if p['water']:
  for j in range(10):
   y=7.1+j*.34;top=.95+(j+1)*.15
   box('Quarry stair tread',(5.9,y,top/2),(1.45,.345,top),'rocklight',rt,.008)
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
 for pos in ((-W/2+2,-12,0),(-W/2+2,21,0),(W/2-2,-12,0),(W/2-2,21,0),(5,0,0),(-14,-4,0),(14,1,0),(-10,17,0),(11,18,0)):light(rt,(pos[0],pos[1],grade(pos[1])))
 # Internally lit roadside pylon with a real steel column and cabinet returns.
 sign=root('RoadSign',(-W/2+4,-D/2+2,0),parent=rt,kind='sign')
 box('Pylon concrete plinth',(0,0,.22),(1.2,.85,.44),'concrete',sign,.025)
 box('Pylon steel column',(0,0,2.8),(.35,.28,5.6),'navy',sign,.014)
 box('Lit sign cabinet',(0,0,5.2),(5.0,.42,1.8),'navy',sign,.05,2)
 box('Opal sign face',(0,-.222,5.2),(4.82,.025,1.61),'ivory',sign,.012)
 text(sign,p['name'].upper(),(.33,-.240,5.57),3.7,.48)
 text(sign,'@creek',(-2.02,-.240,5.57),.48,.48)
 text(sign,'MINIATURE GOLF',(0,-.240,5.02),4.3,.30)
 text(sign,'18 HOLES   •   OPEN LATE',(0,-.240,4.66),4.3,.20)
 for x in (-.42,.42):
  box('Sign service foot',(x,0,.47),(.14,.50,.05),'metal',sign)
  for y in (-.17,.17):cyl('Pylon anchor bolt',(x,y,.47),(x,y,.53),.015,'metal',sign,8)
 rear=root('Pylon reverse face',(0,.24,5.2),180,sign);rear['module']=False
 box('Opal sign face',(0,.016,0),(4.82,.025,1.61),'ivory',rear,.012)
 text(rear,p['name'].upper(),(.33,0,.37),3.7,.48)
 text(rear,'@creek',(-2.02,0,.37),.48,.48)
 text(rear,'MINIATURE GOLF',(0,0,-.18),4.3,.30)
 text(rear,'18 HOLES   •   OPEN LATE',(0,0,-.54),4.3,.20)
 socket(sign,'Light',(0,-.23,5.2),'sign_emitter')
 return rt
