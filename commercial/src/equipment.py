"""Reusable fueling, storage and forecourt equipment; all geometry original."""
import math
from geometry import *

FUEL_PRICES=(3.459,3.759,4.059)


def bollard(name,p,parent=None,color='Yellow',height=1.067):
 r=root(name,p,kind='Bollard',parent=parent);r['reusable_module']=True
 cylinder('Pipe bollard',(0,0,.015),(0,0,height),.084,color,r,16)
 # Welded closed domed cap, no open pipe mouth.
 loops=[]
 for j in range(4):
  a=j*math.pi/6;rr=.084*math.cos(a);zz=height+.084*math.sin(a)
  if rr<1e-5:rr=.001
  loops.append([(rr*math.cos(i*math.tau/16),rr*math.sin(i*math.tau/16),zz) for i in range(16)])
 own(G.smooth(G.loft('Bollard domed cap',loops,M[color])),r)
 cylinder('Ground collar',(0,0,0),(0,0,.028),.108,'Concrete',r,16)
 return r


def trash(name,p,yaw=0):
 r=root(name,p,yaw,'TrashWasher')
 rounded_slab('Molded trash cabinet',(0,0,0),.52,.48,.83,.055,'Trim',r)
 rim=[[(x,y,z) for x,y in G.rounded_rectangle(w,d,rr,4)] for w,d,rr,z in ((.56,.52,.06,.83),(.56,.52,.06,.94),(.38,.34,.04,.94),(.38,.34,.04,.83))]
 own(G.ring_loft('Trash opening rim',rim,M['Black']),r)
 # Dark top opening surrounded by a molded rim, offset hood held at the back.
 box('Trash opening',(0,-.035,.835),(.36,.30,.014),'Black',r,.04,3)
 box('Hood',(0,.12,1.0),(.53,.22,.10),'Trim',r,.04,3)
 box('Washer bucket support',(.34,.06,.54),(.20,.31,.035),'Metal',r,.003)
 bucket=[[(x+.34,y+.06,z) for x,y in G.rounded_rectangle(w,d,rr,4)] for w,d,rr,z in ((.21,.31,.035,.54),(.21,.31,.035,.79),(.185,.285,.025,.79),(.185,.285,.025,.55))]
 own(G.ring_loft('Open washer bucket',bucket,M['Black']),r)
 box('Washer bucket bottom',(.34,.06,.546),(.185,.285,.012),'Black',r,.01)
 box('Washer water',(.34,.06,.72),(.16,.26,.008),'Inside',r,0)
 cylinder('Squeegee handle',(.34,.04,.63),(.34,.04,1.03),.009,'Metal',r,8)
 box('Squeegee blade',(.34,.04,1.04),(.20,.025,.035),'Rubber',r,.004)
 box('Towel dispenser',(0,-.252,.67),(.29,.10,.21),'White',r,.012,2)
 box('Paper towel',(.005,-.31,.53),(.15,.006,.14),'White',r,.001)
 return r


def nozzle(name,p,parent,back=False):
 r=root(name,p,180 if back else 0,'Dispenser',parent)
 r['static_root']=False;r['detachable']=True;r['rest_state']='holstered'
 # Compound cast envelope: changing transverse breadth and center at each section.
 loops=[]
 for z,cx,wx,dy in [(-.18,-.035,.028,.027),(-.12,-.02,.042,.037),(.02,.025,.054,.047),(.10,.055,.062,.048),(.16,.065,.048,.035),(.19,.06,.033,.027)]:
  loops.append([(cx+wx*math.cos(i*math.tau/16),dy*math.sin(i*math.tau/16),z) for i in range(16)])
 own(G.smooth(G.loft('Cast nozzle body',loops,M['Metal'])),r)
 # Rubber hand warmer follows a sculpted grip section rather than a flat profile.
 loops=[]
 for z,cx,wx,dy in [(-.15,-.028,.036,.037),(-.10,-.015,.047,.041),(-.015,.015,.052,.044),(.065,.045,.055,.045)]:
  loops.append([(cx+wx*math.cos(i*math.tau/16),dy*math.sin(i*math.tau/16),z) for i in range(16)])
 own(G.smooth(G.loft('Nozzle handwarmer',loops,M['Black'])),r)
 guard=[(-.07,-.005,-.15),(-.14,-.005,-.12),(-.16,-.005,.04),(-.13,-.005,.12),(-.04,-.005,.13)]
 pts=[]
 for i in range(len(guard)-1):
  a,b=Vector(guard[i]),Vector(guard[i+1]);pts.extend(tuple(a.lerp(b,t/3)) for t in range(3))
 pts.append(guard[-1]);tube('Trigger guard',pts,.012,'Metal',r,8)
 beam('Trigger',(-.10,-.005,-.10),(-.08,-.005,.08),.013,.018,'Trim',r)
 pts=G.bezier((.06,0,.18),(.05,0,.27),(-.01,0,.30),(-.08,0,.34),10)
 tube('Curved unleaded spout',pts,.0105,'Metal',r,10)
 cylinder('Hose swivel',(-.035,0,-.18),(-.035,0,-.255),.021,'Metal',r,12)
 socket(name+'__Hand',(.004,-.007,-.045),r,'nozzle_grip')
 return r


def dispenser(name,p,yaw,brand,index=1):
 r=root(name,p,yaw,'Dispenser')
 r['make']='Cairn Metering';r['model']='M3';r['grades']='87 / 89 / 93, separate products; one hose per face'
 # 44 in class body, formed lower hydraulic cabinet, independent top/electronics.
 box('Dispenser plinth',(0,0,.055),(1.07,.61,.11),'Trim',r,.015,2)
 box('Hydraulic cabinet',(0,0,.57),(1.04,.56,1.0),'White',r,.026,1)
 for s in (-1,1):
  yy=s*.29
  panel('Hydraulic access panel',0,yy,.56,.965,.90,'Primary',r,.015)
  cylinder('Panel lock',(0,yy,.93),(0,yy+s*.014,.93),.018,'Metal',r,10)
 box('Electronics enclosure',(0,0,1.56),(1.10,.62,1.06),'Trim',r,.045,2)
 box('Dispenser crown',(0,0,2.15),(1.19,.67,.18),'Primary',r,.024,1)
 for s in (-1,1):
  # UI local frame: +180 for the back; common analytic construction.
  f=root(name+('_front' if s<0 else '_rear'),(0,s*.322,0),0 if s<0 else 180,'Dispenser',r)
  panel('Face insert',0,-.003,1.57,.93,.93,'White',f,.016)
  panel('Sale and volume display',.08,-.016,1.91,.61,.23,'Black',f)
  volume=7.234
  text('Sale digits',f'{FUEL_PRICES[0]*volume:.2f}',(.16,-.024,1.955),.074,'Lamp',f)
  text('Volume digits',f'{volume:.3f}',(.16,-.024,1.87),.064,'Lamp',f)
  text('Sale labels','$\nGAL',(-.18,-.024,1.91),.044,'White',f)
  panel('Payment screen',-.045,-.024,1.58,.35,.25,'Black',f,.025)
  text('Screen instruction','PAY AT PUMP',(-.045,-.041,1.60),.033,'Lamp',f)
  text('Screen instruction','INSERT CARD',(-.045,-.041,1.54),.028,'Lamp',f)
  panel('Reader bezel',.30,-.035,1.56,.17,.24,'Trim',f,.036)
  panel('Card slot',.30,-.057,1.62,.13,.025,'Black',f,.01)
  panel('Receipt slot',.29,-.052,1.40,.14,.021,'Black',f,.012)
  for row in range(3):
   for col in range(3):box('Keypad',(.26+col*.031,-.062,1.54-row*.032),(.023,.009,.022),'Metal',f,0)
  for i,grade in enumerate(('87','89','93')):
   x=-.25+i*.25
   panel('Grade button',x,-.03,1.20,.19,.145,'Yellow',f,.025)
   text('Grade number',grade,(x,-.047,1.20),.078,'Black',f)
   box('Grade unit-price lens',(x,-.03,1.34),(.20,.010,.065),'Black',f,0)
   text('Grade unit price',f'{FUEL_PRICES[i]:.3f}',(x,-.037,1.34),.032,'Lamp',f)
  text('Dispenser number',str(index),(0,-.015,2.15),.13,'Light',f)
  # A real holster has a dark opening and a retaining lip.
  panel('Nozzle holster',-.49,-.06,1.29,.18,.36,'Black',f,.10)
  panel('Holster lip',-.49,-.125,1.12,.18,.055,'Trim',f,.024)
  panel('Spout docking pocket',-.57,-.11,1.61,.12,.12,'Black',f,.07)
  noz=nozzle(name+('_NozzleA' if s<0 else '_NozzleB'),(-.49,-.14,1.27),f)
  # Curb hose: 30 mm OD. A gravity loop clears the island, with metal breakaway.
  pts=G.bezier((-.57,-.06,2.10),(-.74,-.10,1.94),(-1.01,-.14,.57),(-.94,-.15,.46),20)
  pts+=G.bezier((-.94,-.15,.46),(-.81,-.16,.21),(-.57,-.14,.62),(-.525,-.14,1.015),28)[1:]
  hose=tube('30 mm curb hose',pts,.015,'Rubber',f,8);hose['hose_radius_m']=.015
  hose['centerline_m']=[v for p in pts for v in p]
  cylinder('Breakaway coupling',(-.57,-.06,2.10),(-.57,-.06,2.01),.027,'Metal',f,12)
  # Stored slack hose, without the former unsupported wire/reel proxy.
  # The crown bulkhead and nozzle swivel support the two ends.
  panel('Safety plate',.16,.016,.77,.42,.22,'White',f,.012)
  ring=[(-.005+.044*math.cos(i*math.tau/24),.005,.77+.044*math.sin(i*math.tau/24)) for i in range(25)]
  tube('No smoking red ring',ring,.004,'Red',f,6)
  tube('No smoking red slash',[(-.036,.004,.739),(.026,.004,.801)],.004,'Red',f,6)
  box('Cigarette pictogram',(-.005,.005,.76),(.045,.004,.009),'Black',f,0)
  text('Safety instructions','NO SMOKING\nSTOP ENGINE',(.19,.008,.77),.035,'Red',f)
  text('Fictional dispenser maker','CAIRN  M3',(.15,.020,.28),.041,'White',f)
  mark('Fuel brand mark',(-.25,.020,.49),.15,brand,f)
  text('Fuel brand name',brand['name'],(.12,.020,.49),.060,'Light',f)
 return r


def canopy(spec,brand):
 c=spec;r=root('Canopy',(c['center'][0],c['center'][1],0),c['angle'],'Canopy')
 w,d,clear,fascia=c['width'],c['depth'],c['clear'],c['fascia']
 # Fascia is a hollow band around soffit + membrane, not a thick solid slab.
 lights=[((i-(c['count']-1)/2)*c['pitch']+side*2.2,yy) for i in range(c['count']) for side in (-1,1) for yy in (-d/2+2.0,d/2-2.0)]
 xs=sorted(set([-w/2,w/2]+[x+u for x,y in lights for u in (-.275,.275)]))
 ys=sorted(set([-d/2,d/2]+[y+v for x,y in lights for v in (-.275,.275)]))
 for xa,xb in zip(xs,xs[1:]):
  for ya,yb in zip(ys,ys[1:]):
   mx,my=(xa+xb)/2,(ya+yb)/2
   if any(abs(mx-x)<.275 and abs(my-y)<.275 for x,y in lights):continue
   ob=G.plane_uv('Soffit cladding',[(xa,ya,clear),(xa,yb,clear),(xb,yb,clear),(xb,ya,clear)],M['White']);own(ob,r,False)
 box('Canopy membrane',(0,0,clear+fascia-.055),(w-.12,d-.12,.055),'Roof',r,0)
 for yy in (-d/2,d/2):
  box('Fascia vertical',(0,yy,clear+fascia/2),(w,.10,fascia),'Primary',r,.008)
  box('Fascia lower reveal',(0,yy-.006,clear+.08),(w,.122,.09),'Accent',r,.002)
  box('Top coping',(0,yy,clear+fascia+.018),(w+.08,.18,.04),'Trim',r,.002)
 for xx in (-w/2,w/2):
  box('Fascia end',(xx,0,clear+fascia/2),(.10,d-.12,fascia),'Primary',r,.008)
  box('Fascia end lower reveal',(xx,0,clear+.08),(.122,d,.09),'Accent',r,.002)
  box('Top coping',(xx,0,clear+fascia+.018),(.18,d,.04),'Trim',r,.002)
 for side in (-1,1):
  f=root('CanopySign', (0,side*(d/2+.06),clear+fascia*.54),0 if side<0 else 180,'Canopy',r)
  # Luminous mark and letters stand 28 mm off their aluminum fascia face.
  mark('Canopy logo',(-3.20,-.02,0),.64,brand,f)
  text('Canopy lettering',brand['name'],(.45,.008,0),.47,'Light',f)
  text('Clearance marking','CLEARANCE 14 ft 6 in',(w*.38,.008,-fascia*.27),.095,'White',f)
 # Soffit seams are construction panels, fine corrugation is a future normal.
 for j in range(round(d/.61)):
  yy=-d/2+j*.61
  box('Soffit seam',(0,yy,clear-.001),(w-.12,.013,.002),'Metal',r,0)
 for i in range(c['count']):
  x=(i-(c['count']-1)/2)*c['pitch'];island=root('Island_'+str(i+1),(x,0,0),kind='Canopy',parent=r)
  rounded_slab('Raised curb island',(0,0,.01),c['island'][0],c['island'][1],c['island'][2],.40,'Concrete',island)
  box('Column base plate',(0,.92,.19),(.52,.52,.055),'Metal',island,.008)
  box('Square canopy column',(0,.92,(clear+.20)/2),(c['column'],c['column'],clear-.20),'White',island,.009,2)
  # Brake-formed four-piece painted aluminum wrap with folded base skirt,
  # a gasketed vertical closure and the brand's narrow identity band.
  box('Column base skirt',(0,.92,.30),(.40,.40,.20),'Trim',island,.008)
  box('Column skirt drip',(0,.92,.407),(.425,.425,.025),'Metal',island,.003)
  box('Column brand band',(0,.92,1.48),(.3636,.3636,.24),'Primary',island,.003)
  box('Column band reveal',(0,.92,1.35),(.365,.365,.025),'Accent',island,.001)
  box('Column closure seam',(.1785,.92,2.42),(.002,.009,3.86),'Trim',island,0)
  for xx in (-.20,.20):
   for yy in (.72,1.12):cylinder('Column anchor',(xx,yy,.215),(xx,yy,.245),.022,'Metal',island,6)
  # Downpipe sits on the column face, with straps touching it.
  box('Canopy drain',(0,1.14,(clear+.25)/2),(.076,.05,clear-.25),'Metal',island,.004)
  for z in (.4,1.8,3.4):box('Drain strap',(0,1.12,z),(.13,.18,.022),'Trim',island,.002)
  tube('Column U guard',[(-.40,.45,.17),(-.40,.45,.90),(-.34,.45,.97),(.34,.45,.97),(.40,.45,.90),(.40,.45,.17)],.057,'Yellow',island,12)
  for yy in (-2.15,2.15):
   # Protection remains a separately reusable small prop.
   bollard('IslandBollard_'+str(i+1)+'_'+str(yy),(x,yy,.1624),r,height=.92)
  for side in (-1,1):
   for yy in (-d/2+2.0,d/2-2.0):
    xx=x+side*2.2
    box('Recessed luminaire frame',(xx,yy,clear+.018),(.55,.55,.036),'Trim',r,.003)
    box('Flush luminaire lens',(xx,yy,clear+.005),(.47,.47,.010),'Lamp',r,.003)
  # Pump and washer are independent module roots, located through canopy frame.
 return r


def price_sign(kind,p,brand):
 r=root('PriceSign',p,0,'PriceSign');pylon=kind=='pylon'
 base=2.3 if pylon else .42;w=2.9 if pylon else 3.6;h=3.0 if pylon else 2.8
 box('Sign foundation',(0,0,.12),(w+.34,.80,.24),'Concrete',r,.025)
 if pylon:
  for xx in (-.75,.75):box('Pylon steel upright',(xx,0,base/2),( .24,.28,base),'Trim',r,.008)
 else:
  box('Monument masonry base',(0,0,.29),(w,.68,.58),'Wall',r,.008)
  box('Monument masonry cap',(0,0,.59),(w+.12,.80,.09),'Concrete',r,.012)
  for xx in (-w/2+.13,w/2-.13):box('Monument masonry end pier',(xx,0,.36),(.26,.73,.60),'Wall',r,.005)
 box('Price cabinet',(0,0,base+h/2),(w,.42,h),'Trim',r,.025,2)
 for side in (-1,1):
  for xx in (-w/2+.035,w/2-.035):box('Sign extruded jamb',(xx,side*.23,base+h/2),(.075,.055,h+.04),'Metal',r,.006)
  for zz in (base+.015,base+h-.015):box('Sign extruded rail',(0,side*.23,zz),(w-.08,.055,.075),'Metal',r,.006)
 for s in (-1,1):
  f=root('PriceFace',(0,s*.225,base),0 if s<0 else 180,'PriceSign',r)
  panel('Price display face',0,0,h/2,w-.10,h-.10,'Black',f,.020)
  brand_sign('Price brand',(0,-.025,h-.51),w-.10,.88,brand,f)
  for i,(grade,price) in enumerate(zip(('REGULAR','PLUS','PREMIUM'),FUEL_PRICES)):
   z=h-1.17-i*.53
   text('Price grade',grade,(-w*.43,-.012,z),.14,'White',f,'LEFT')
   led_digits('LED price',f'{price:.3f}',(w*.22,-.014,z),.34,f)
  text('Price legal','CASH / CREDIT  •  PER GALLON',(0,-.012,.30),.062,'White',f)
 return r


def ice(p):
 r=root('IceMerchandiser',p,kind='IceMerchandiser')
 box('Ice insulated back',(0,.39,.95),(1.70,.08,1.90),'White',r,.015,2)
 for xx in (-.81,.81):box('Ice insulated side',(xx,0,.95),(.08,.78,1.90),'White',r,.012,2)
 for zz in (.08,1.84):box('Ice insulated return',(0,0,zz),(1.60,.78,.10),'White',r,.012,2)
 # Cabinet is covered by door leaves. Inset dark gaps describe insulation returns.
 frame('Ice gasket',0,-.433,.91,1.59,1.42,'Black',r,.025,.02)
 for side in (-1,1):
  x=side*.40;pv=hinge('IceDoor_'+str(side),(x-.37,-.46,.24),r,(-100,0))
  box('Insulated ice door',(.37,0,.66),(.735,.060,1.31),'White',pv,.012,2)
  cylinder('Ice handle',(.64,-.08,.48),(.64,-.08,.87),.013,'Metal',pv,10)
  text('Ice door graphic','ICE',(.37,-.035,.79),.20,'Blue',pv)
 box('Ice compressor housing',(0,0,1.98),(1.74,.88,.16),'White',r,.015)
 panel('Ice vent',0,-.451,1.99,1.42,.10,'Black',r,.014)
 for i in range(16):box('Ice vent fin',(-.68+i*.09,-.464,1.99),(.016,.016,.09),'Metal',r,.001)
 return r


def tank(name,p,parent):
 x,y,z=p;profile=[(0,z),(.12,z),(.15,z+.035),(.153,z+.10),(.153,z+.32),(.14,z+.37),(.06,z+.41),(.015,z+.425)]
 ob=G.lathe(name,[(zz,rr) for rr,zz in profile],M['White'],segments=12,center=(x,y));own(G.smooth(ob),parent)
 cylinder('Cylinder valve',(x,y,z+.42),(x,y,z+.465),.018,'Metal',parent,8)
 # Open protective collar represented by a partial bent strip.
 pts=[(x+.082*math.cos(math.radians(30+i*300/12)),y+.082*math.sin(math.radians(30+i*300/12)),z+.46) for i in range(13)]
 tube('Cylinder collar',pts,.012,'White',parent,6)


def propane(p):
 r=root('PropaneCage',p,kind='PropaneCage')
 for zz in (.08,.78,1.53):box('Cage shelf',(0,0,zz),(1.85,.78,.035),'Metal',r,.002)
 for xx in (-.94,.94):
  for yy in (-.41,.41):box('Cage angle frame',(xx,yy,.83),(.036,.036,1.66),'White',r,.002)
 for zz in (.12,1.53):
  for yy in (-.41,.41):box('Cage edge rail',(0,yy,zz),(1.90,.034,.034),'White',r,.002)
 # Back and side welded wire, actual open grid at form gate.
 for x in [i*.15-.90 for i in range(13)]:box('Cage back wire',(x,.405,.83),(.008,.008,1.4),'Metal',r,0)
 for z in [i*.15+.18 for i in range(9)]:box('Cage back wire',(0,.405,z),(1.8,.008,.008),'Metal',r,0)
 for xx in (-.94,.94):
  for yy in (-.27,-.12,.03,.18,.33):box('Cage side wire',(xx,yy,.83),(.008,.008,1.4),'Metal',r,0)
 for side in (-1,1):
  pv=hinge('PropaneDoor_'+str(side),(-.92+(.94 if side>0 else 0),-.49,.12),r,(-100,0))
  frame('Cage gate',.45,0,.70,.91,1.40,'White',pv,.03,.032)
  for x in [i*.15+.075 for i in range(6)]:box('Gate wire',(x,0,.70),(.008,.008,1.34),'Metal',pv,0)
  for z in [i*.15+.05 for i in range(9)]:box('Gate wire',(.45,0,z),(.88,.008,.008),'Metal',pv,0)
  panel('Cage hazard',.45,-.025,1.05,.44,.36,'White',pv,.012)
  text('Cage warning','PROPANE\nFLAMMABLE',(.45,-.034,1.05),.052,'Red',pv)
 for zz in (.0975,.7975):
  for xx in (-.66,-.22,.22,.66):tank('Original 20lb cylinder',(xx,0,zz),r)
 text('Cage header','CYLINDER EXCHANGE',(0,-.45,1.64),.10,'White',r)
 return r


def air(p):
 r=root('AirWater',p,kind='AirWater')
 box('Air machine concrete pad',(0,0,.06),(.85,.85,.12),'Concrete',r,.025)
 box('Air pedestal',(0,0,.53),(.30,.30,.94),'Trim',r,.012)
 box('Air coin cabinet',(0,0,1.23),(.57,.44,.58),'Primary',r,.035,2)
 panel('Air controls',0,-.231,1.25,.45,.42,'White',r,.02)
 text('Air water label','AIR / WATER',(0,-.247,1.35),.065,'Black',r)
 panel('Air coin slot',.13,-.25,1.19,.055,.014,'Black',r)
 panel('Air pressure display',-.08,-.25,1.20,.15,.08,'Black',r)
 pts=[]
 for i in range(90):
  t=i/89;angle=t*math.tau*4+math.pi/2
  pts.append((.20+.19*math.cos(angle),-.27-.035*t,.67+.19*math.sin(angle)-.10*t))
 lead=G.bezier((.24,-.22,1.0),(.38,-.26,.88),(.30,-.27,.86),pts[0],8)
 tube('Air supply hose',lead,.008,'Black',r,6)
 tube('Air hose hook',[(.20,-.18,1.0),(.20,-.30,.89),(.20,-.30,.81),(.20,-.22,.81)],.012,'Metal',r,8)
 tube('Slack coiled air hose',pts,.008,'Black',r,6)
 cylinder('Air chuck',pts[-1],(.19,-.34,.66),.012,'Metal',r,8)
 cylinder('Water faucet',(-.20,-.22,1.07),(-.20,-.34,1.07),.014,'Metal',r,8)
 return r


def lightpole(name,p):
 r=root(name,p,kind='LightPole')
 cylinder('Light foundation',(0,0,0),(0,0,.65),.20,'Concrete',r,16)
 box('Pole shoe',(0,0,.68),(.31,.31,.06),'Metal',r,.006)
 box('Parking light pole',(0,0,3.68),(.13,.13,6.0),'Trim',r,.005)
 beam('Luminaire arm',(0,0,6.48),(.65,0,6.48),.075,.075,'Trim',r)
 box('Full cutoff head',(.68,0,6.47),(.62,.35,.15),'Trim',r,.03,2)
 box('Light lens',(.68,0,6.389),(.51,.27,.012),'Lamp',r,.005)
 return r


def dumpster_enclosure(p):
 r=root('DumpsterEnclosure',p,kind='DumpsterEnclosure')
 box('Yard concrete',(0,0,.06),(4.5,3.6,.12),'Concrete',r,.02)
 box('Yard rear',(0,1.65,1.15),(4.4,.2032,2.1),'Wall',r,.008)
 for xx in (-2.1,2.1):box('Yard side',(xx,0,1.15),(.2032,3.4,2.1),'Wall',r,.008)
 for side in (-1,1):
  pv=hinge('DumpsterGate_'+str(side),(side*1.96,-1.78,.12),r,(-110,0) if side<0 else (0,110))
  direction=-side;box('Gate steel frame',(direction*.97,0,.98),(1.93,.07,1.96),'Trim',pv,.006)
  for i in range(17):box('Gate slat',(direction*(.07+i*.111),-.05,.98),(.093,.022,1.88),'Primary',pv,.001)
 # Roll-off style commercial dumpster, no wheels required for its skid feet.
 box('Dumpster bottom',(0,.1,.22),(2.7,1.65,.14),'Trim',r,.02)
 loops=[]
 for zz,ww,dd in ((.28,2.65,1.60),(1.50,2.9,1.83)):
  loops.append([(-ww/2,.10-dd/2,zz),(ww/2,.10-dd/2,zz),(ww/2,.10+dd/2,zz),(-ww/2,.10+dd/2,zz)])
 for zz,ww,dd in ((1.50,2.888,1.818),(.28,2.638,1.588)):
  loops.append([(-ww/2,.10-dd/2,zz),(ww/2,.10-dd/2,zz),(ww/2,.10+dd/2,zz),(-ww/2,.10+dd/2,zz)])
 own(G.ring_loft('Dumpster welded open shell',loops,M['Trim']),r)
 for side in (-1,1):
  pv=root('DumpsterLid_'+str(side),(side*.73,1.03,1.54),kind='DumpsterEnclosure',parent=r)
  pv['static_root']=False;pv['pivot_axis']='X';pv['range_degrees']=(-105,0)
  box('Molded dumpster lid',(0,-.92,0),(1.42,1.83,.075),'Black',pv,.04,2)
  for i in (-.44,0,.44):box('Dumpster lid rib',(i,-.92,.045),(.045,1.50,.04),'Black',pv,.012)
 return r
