"""Five-seat crossover cabin, with lofted upholstery and cargo under the gate."""
import math,bpy
from mathutils import Vector
from kit import model as G
from detail_helpers import box,tube,loop,print_quad
import suv_spec as S


def build(b):
 def cushion(name,x,y,w,d,z0,z1,mat):
  headrest='headrest' in name
  profile=[(z0,.72),((z0+z1)/2,1),(z1,.78)] if headrest else [(z0,.90),((z0+z1)/2,1),(z1,.94)]
  rows=[[(x+u,y+v,z) for u,v in G.rounded_rectangle(w*scale,d*scale,min(.055,w*.16)*scale,3 if b.high else 2)] for z,scale in profile]
  ob=b.add(G.loft(name,rows,mat),category='interior')
  return G.smooth(ob,80 if headrest else 40)
 for side,x in [('L',-.425),('R',.425)]:
  for dx in [-.15,.15]:box(b,'Seat rail '+side+str(dx),(x+dx,-.16,.47),(.035,.54,.032),b.m['frame'],'interior',radius=0)
  cushion('Front cushion '+side,x,-.17,.48,.53,.50,.64,b.m['cloth'])
  rows=[]
  for z,y,w,d in [(.61,.055,.45,.13),(.81,.095,.48,.15),(1.07,.17,.44,.13),(1.17,.205,.36,.11)]:
   rows.append([(x+u,y+v,z) for u,v in G.rounded_rectangle(w,d,.045,3 if b.high else 2)])
  b.add(G.smooth(G.loft('Front backrest '+side,rows,b.m['cloth'])),category='interior')
  for dx in [-.063,.063]:tube(b,'Headrest stem '+side+str(dx),[(x+dx,.205,1.14),(x+dx,.23,1.26)],.005,b.m['chrome'],'interior',sides=5)
  cushion('Front headrest '+side,x,.23,.245,.13,1.23,1.40,b.m['cloth'])
  for sign in [-1,1]:tube(b,'Bolster seam '+side+str(sign),[(x+sign*.16,yy,zz) for yy,zz in [(-.015,.69),(.015,.82),(.10,1.06)]],.0015,b.m['seat_side'],'interior',sides=4)
 cushion('Rear bench cushion',0,.79,1.34,.48,.55,.67,b.m['cloth'])
 rows=[[(u,y+v,z) for u,v in G.rounded_rectangle(w,d,.045,3 if b.high else 2)] for z,y,w,d in [(.65,1.00,1.34,.12),(.91,1.07,1.32,.14),(1.21,1.14,1.26,.10)]]
 b.add(G.smooth(G.loft('Rear bench back',rows,b.m['cloth'])),category='interior')
 for i,x in enumerate([-.44,0,.44]):
  for dx in [-.05,.05]:tube(b,'Rear headrest stem '+str(i)+str(dx),[(x+dx,1.14,1.19),(x+dx,1.15,1.29)],.005,b.m['chrome'],'interior',sides=5)
  cushion('Rear headrest '+str(i),x,1.15,.22,.115,1.27,1.41,b.m['cloth'])
 profile=[(-1.01,.70),(-1.01,1.025),(-.83,1.07),(-.57,1.045),(-.48,.94),(-.52,.77)]
 b.add(G.profile('Dashboard shell',profile,-.71,.71,b.m['interior'],axis='X',radius=.015,segments=2 if b.high else 1),category='interior')
 box(b,'Center stack',(0,-.485,.88),(.30,.06,.25),b.m['seat_side'],'interior',radius=.025)
 print_quad(b,'Center display',[(.125,-.448,.91),(-.125,-.448,.91),(-.125,-.448,1.035),(.125,-.448,1.035)],b.m['display'],'interior')
 box(b,'Cluster binnacle',(.425,-.59,1.043),(.33,.16,.12),b.m['plastic'],'interior',radius=.025)
 print_quad(b,'Cluster face',[(.57,-.505,1.00),(.28,-.505,1.00),(.28,-.505,1.085),(.57,-.505,1.085)],b.m['cluster'],'interior')
 for x in [-.67,-.20,.20,.67]:
  box(b,'Dash vent '+str(x),(x,-.50,1.00),(.09,.012,.055),b.m['frame'],'interior',radius=.004)
  for z in [.983,1.001,1.019]:box(b,'Vent vane '+str(x)+str(z),(x,-.49,z),(.075,.005,.003),b.m['interior_light'],'interior',radius=0)
 box(b,'Center console',(0,-.06,.63),(.25,.69,.25),b.m['interior'],'interior',radius=.030)
 box(b,'Console arm pad',(0,.12,.77),(.25,.28,.05),b.m['seat_side'],'interior',radius=.021)
 for y in [-.15,-.27]:
  loop(b,'Cup holder '+str(y),(0,y,.76),(1,0,0),(0,1,0),(.043,.043),.005,b.m['frame'],'interior',segments=12,sides=4)
 tube(b,'Shifter',[(.07,-.35,.74),(.07,-.32,.87)],.010,b.m['frame'],'interior',sides=6)
 box(b,'Shifter knob',(.07,-.32,.88),(.045,.055,.045),b.m['seat_side'],'interior',radius=.016)
 c=Vector((.425,-.325,1.00));a=Vector((1,0,0));up=Vector((0,-.42,.907));normal=a.cross(up)
 loop(b,'Steering rim',c,a,up,(.17,.17),.015,b.m['rubber'],'interior',segments=28 if b.high else 20,sides=6)
 tube(b,'Steering column',[c+normal*.02,(.425,-.63,.84)],.026,b.m['plastic'],'interior',sides=8)
 box(b,'Steering airbag',c,(.15,.065,.13),b.m['seat_side'],'interior',radius=.022)
 for angle in [0,math.pi,1.5*math.pi]:tube(b,'Steering spoke '+str(angle),[c+a*.065*math.cos(angle)+up*.065*math.sin(angle),c+a*.15*math.cos(angle)+up*.15*math.sin(angle)],.018,b.m['interior_light'],'interior',sides=4)
 for side,sgn in [('L',-1),('R',1)]:
  for end,ya,yb in [('F',S.DOOR_FRONT,S.DOOR_SPLIT),('R',S.DOOR_SPLIT,S.DOOR_REAR)]:
   parent=bpy.data.objects['Door_'+end+side];y=(ya+yb)/2;w=yb-ya-.16
   # The rear card ends above the wheel arch intrusion, with a curved toe.
   z=.79;h=.50 if end=='F' else .42
   if end=='R':
    # The rear closure wraps the wheel opening; its inner card must do so too.
    bottom,top=z-h/2,z+h/2
    outline=[(ya+.08,bottom),(ya+.08,top),(yb-.08,top)]
    for zz in [top-(top-bottom)*i/12 for i in range(1,13)]:
     dz=(zz-S.HUB_HEIGHT)/(S.ARCH_RADIUS+.04)
     rear=yb-.08 if dz>=1 else min(yb-.08,S.REAR_AXLE-S.ARCH_HALF*max(0,1-abs(dz)**S.ARCH_POWER)**(1/S.ARCH_POWER)-.035)
     outline.append((rear,zz))
   else:outline=[(y+u,z+v) for u,v in G.rounded_rectangle(w,h,.055,2)]
   b.add(G.profile('Door card '+end+side,outline,sgn*.77,sgn*.805,b.m['interior'],axis='X'),parent,'interior')
   # A shaped inner carrier supports the card, with a real wheel-opening notch
   # and 35 mm return depth instead of the form checkpoint's paper-thin door.
   lower=.315;upper=1.155+.018*y;carrier=[(ya+.05,upper),(yb-.05,upper)]
   for zz in [upper-(upper-lower)*i/14 for i in range(1,15)]:
    dz=(zz-S.HUB_HEIGHT)/(S.ARCH_RADIUS+.04)
    limit=yb-.05 if dz>=1 else min(yb-.05,S.REAR_AXLE-S.ARCH_HALF*max(0,1-abs(dz)**S.ARCH_POWER)**(1/S.ARCH_POWER)-.035)
    carrier.append((limit,zz))
   for zz in [lower+(upper-lower)*i/14 for i in range(15)]:
    dz=(zz-S.HUB_HEIGHT)/(S.ARCH_RADIUS+.04)
    limit=ya+.05 if dz>=1 else max(ya+.05,S.FRONT_AXLE+S.ARCH_HALF*max(0,1-abs(dz)**S.ARCH_POWER)**(1/S.ARCH_POWER)+.035)
    carrier.append((limit,zz))
   if (Vector(carrier[0])-Vector(carrier[-1])).length<1e-8:carrier.pop()
   carrier=[p for i,p in enumerate(carrier) if abs((Vector(p)-Vector(carrier[i-1])).cross(Vector(carrier[(i+1)%len(carrier)])-Vector(p)))>1e-10]
   b.add(G.profile('Door inner carrier '+end+side,carrier,sgn*.806,sgn*.841,b.m['seat_side'],axis='X'),parent,'interior')

   box(b,'Door armrest '+end+side,(sgn*.77,y-.015,.95),(.075,w*.57,.065),b.m['seat_side'],'interior',parent,.015)
   box(b,'Inside latch '+end+side,(sgn*.75,y-.20,1.035),(.015,.09,.028),b.m['chrome'],'interior',parent,.005)
   box(b,'Door pocket '+end+side,(sgn*.755,y if end=='F' else ya+.31,.65 if end=='F' else .72),(.065,w*.66 if end=='F' else .39,.075),b.m['plastic'],'interior',parent,.012)
 # Low unibody floor, a separate luggage well and supported privacy cover.
 # Raised rear wheel housings and front footwell setbacks leave tire envelopes.
 outline=[(-.63,-.88),(.63,-.88),(.695,-.65),(.695,.86),(.59,1.22),(-.59,1.22),(-.695,.86),(-.695,-.65)]
 b.add(G.profile('Cabin floor',outline,.4225,.4675,b.m['interior'],axis='Z',radius=.012 if b.high else 0,segments=1),category='interior')
 box(b,'Cargo floor',(0,1.67,.655),(1.29,1.03,.045),b.m['cloth'],'interior',radius=.018 if b.high else 0)
 for s in [-1,1]:
  box(b,'Cargo wheelhouse trim '+str(s),(s*.62,1.57,.81),(.11,.79,.23),b.m['interior'],'interior',radius=.045)
  box(b,'Cargo cover ledge '+str(s),(s*.625,1.61,1.12),(.038,.78,.025),b.m['plastic'],'interior',radius=.005)
 b.add(G.profile('Cargo cover',[(-.64,1.165),(.64,1.165),(.64,1.96),(.60,2.04),(-.60,2.04),(-.64,1.96)],1.121,1.139,b.m['cloth'],axis='Z'),category='interior')
 # Headliner follows the accepted roof crown; one shallow loft rather than a slab.
 rows=[]
 for y,z,w in [(-.22,1.57,.64),(.1,1.635,.66),(1.1,1.63,.66),(1.60,1.59,.63)]:
  rows.append([(-w,y,z-.022),(0,y,z),(w,y,z-.022)])
 ob=G.mesh('Headliner',[p for row in rows for p in row],[(j*3+i,j*3+i+1,(j+1)*3+i+1,(j+1)*3+i) for j in range(3) for i in range(2)],b.m['headliner']);sol=ob.modifiers.new('Headliner thickness','SOLIDIFY');sol.thickness=.008;b.add(ob,category='interior')
 for x in [-.40,.40]:box(b,'Sun visor '+str(x),(x,-.21,1.54),(.33,.15,.025),b.m['headliner'],'interior',radius=.009)
 box(b,'Cab mirror case',(0,-.45,1.43),(.21,.045,.065),b.m['plastic'],'interior',radius=.013)
 box(b,'Cab mirror pane',(0,-.422,1.43),(.19,.004,.045),b.m['mirror'],'interior',radius=.007)

 # The lower gate has a formed inner polymer panel; the upper laminate stays
 # exposed. Rays sample the actual convex gate, then offset toward the cabin.
 from suv_exterior import tree_for
 gate=bpy.data.objects['Liftgate'];skin=tree_for([bpy.data.objects['Liftgate outer']]);rows=[]
 for j in range(4):
  z=.735+.46*j/3;row=[]
  for i in range(9):
   x=-.68+1.36*i/8
   hit=skin.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),3)[0]
   if hit is None:hit=skin.find_nearest(Vector((x,2.25,z)))[0]
   # Offset in vehicle Y even at aperture rims: their lateral normals must
   # never push an interior liner through the exterior plate or lamp.
   row.append(Vector((x,hit.y-.055,z)))
  rows.append(row)
 ob=G.mesh('Liftgate inner trim',[p for row in rows for p in row],[(j*9+i,j*9+i+1,(j+1)*9+i+1,(j+1)*9+i) for j in range(3) for i in range(8)],b.m['interior'])
 solid=ob.modifiers.new('Trim wall','SOLIDIFY');solid.thickness=.003;b.add(ob,gate,'interior')
