"""Corner hardscape and 24 ft commercial interfaces on the ground grid.

The adjacent road/walk is context, constructed with ground's published profile
and pitches. A wide entrance is not a scaled residential curb cut: its level
central run is extended, preserving the 5 ft transition and apron run.
"""
import math, random
from geometry import *
from plan import FT
from ground_adapter import PROFILE,FLOW,CURB_TOP,STRIP,CORNER_ANGLES,TRANSITION,depression,cut_top,walk_z


def strip(name,a,b,width,mat,parent,z=.002):
 ax,ay=a;bx,by=b;dx,dy=bx-ax,by-ay;length=math.hypot(dx,dy)
 if length<1e-6:return
 nx,ny=-dy/length*width/2,dx/length*width/2
 return mesh(name,[(ax+nx,ay+ny,z),(ax-nx,ay-ny,z),(bx-nx,by-ny,z),(bx+nx,by+ny,z)],[(0,1,2,3)],mat,parent,False)


def flat(name,rect,mat,parent,z=0):
 x0,x1,y0,y1=rect;return mesh(name,[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],[(0,1,2,3)],mat,parent,False)


def curb_run(name,points,parent):
 # Path at face, left points toward lot. Gauge/back remains 6 inches.
 vs=[];fs=[]
 profile=PROFILE
 for i,(x,y,z) in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];dx,dy=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dy);nx,ny=-dy/le,dx/le
  for u,v in profile:
   factor=(z-FLOW)/.1524
   zz=FLOW+v*(factor if u>=-.01 else 1)
   vs.append((x+nx*u,y+ny*u,zz))
 for i in range(len(points)-1):
  for j in range(len(profile)-1):a=i*len(profile)+j;fs.append((a,a+len(profile),a+1+len(profile),a+1))
 return mesh(name,vs,fs,'Concrete',parent,False)


def street_edge(edge,p,parent):
 W,D=p['lot'];south=edge=='south';length=W if south else D
 origin=(0,-D/2) if south else (-W/2,0)
 def xy(u,v):return (u,origin[1]+v) if south else (origin[0]+v,-u)
 drive=next(d for d in p['driveways'] if d['edge']==edge)
 dc=drive['center'][0] if south else -drive['center'][1];width=drive['width'];half=width/2;wing=1.524
 start=-length/2+1.2192 if south else -length/2
 end=length/2 if south else length/2-1.2192
 transitions=[dc+s for s in TRANSITION(width+2*wing,width)]
 us=sorted(set([start,end]+transitions))
 # The public walk keeps ground's true 1% crossfall and exact strip widths.
 for a,b in zip(us,us[1:]):
  vs=[]
  for u,v in ((a,-1.3716),(b,-1.3716),(b,.1524),(a,.1524)):
   x,y=xy(u,v);vs.append((x,y,walk_z(v)))
  mesh('Public sidewalk',vs,[(0,1,2,3)],'Concrete',parent,False)
 # Uncut planting lies outside the entrance's entire wing envelope.
 for a,b in ((start,dc-half-wing),(dc+half+wing,end)):
  if b<=a:continue
  mesh('Public planting',[(x,y,CURB_TOP+.009) for x,y in [xy(a,-3.2004),xy(b,-3.2004),xy(b,-1.3716),xy(a,-1.3716)]],[(0,1,2,3)],'Green',parent,False)
 # Keep the native curved pan/nose. Depress only the native upright/back
 # profile, never the gutter: lowering the whole section would open a road gap.
 stations=[(u,cut_top(u-dc,width)) for u in us]
 curb_run('Commercial native curb',[( *xy(u,-3.3528),height) for u,height in stations],parent)
 # Fan apron, same native six-foot run and five-foot transition wings.
 xs=(0,.6096,STRIP-.0254,STRIP-.0127,STRIP)
 base=TRANSITION(width+2*wing,width);verts=[];faces=[]
 for x in xs:
  t=x/STRIP;hh=half+wing*(1-t)
  for s in base:
   u=dc+s/(half+wing)*hh
   z0=cut_top(u-dc,width);z=z0+(CURB_TOP-z0)*t
   xx,yy=xy(u,-3.2004+x);verts.append((xx,yy,z))
 n=len(base)
 for j in range(len(xs)-1):
  for i in range(n-1):q=j*n+i;faces.append((q,q+1,q+1+n,q+n))
 mesh('Commercial tapered apron',verts,faces,'Concrete',parent,False)
 # Grass triangles outside the fan meet its actual edge grade, rather than
 # covering the depressed pour with a flat planting rectangle.
 for side in (-1,1):
  verts=[]
  for x in xs:
   t=x/STRIP;inner=half+wing*(1-t);outer=half+wing
   for u in (dc+side*inner,dc+side*outer):
    z0=cut_top(u-dc,width);z=z0+(CURB_TOP-z0)*t+.002
    xx,yy=xy(u,-3.2004+x);verts.append((xx,yy,z))
  # The first pair is one shared apex; weld/dissolve it in finalization.
  mesh('Tapered turf wing',verts,[(2*i,2*i+1,2*i+3,2*i+2) if side>0 else (2*i+2,2*i+3,2*i+1,2*i) for i in range(4)],'Green',parent,False)
 for u in [j*1.524-length/2 for j in range(int(length/1.524)+1)]:
  if not start<=u<=end or abs(u-dc)<half:continue
  a=xy(u,-1.3716);b=xy(u,.1524);du=(.003,0) if south else (0,.003)
  # A narrow score surface follows the walk's slope.
  mesh('Walk score',[(a[0]-du[0],a[1]-du[1],walk_z(-1.3716)+.001),(a[0]+du[0],a[1]+du[1],walk_z(-1.3716)+.001),(b[0]+du[0],b[1]+du[1],.001),(b[0]-du[0],b[1]-du[1],.001)],[(0,1,2,3)],'Trim',parent,False)
 return xy


def site(p):
 W,D=p['lot'];b=p['building'];r=root('SitePaving',kind='SitePaving')
 # Visible ground skins, no invisible buried faces.
 cx,cy=-W/2+1.2192,-D/2+1.2192
 poly=[(cx,-D/2+.1524),(W/2,-D/2+.1524),(W/2,D/2),(-W/2+.1524,D/2),(-W/2+.1524,cy)]
 poly += [(cx+1.0668*math.cos(math.radians(a)),cy+1.0668*math.sin(math.radians(a))) for a in CORNER_ANGLES[1:]]
 mesh('Lot asphalt',[(x,y,0) for x,y in poly],[tuple(range(len(poly)))],'Asphalt',r,False)
 for ri,ro,mat in ((1.0668,2.5908,'Concrete'),(2.5908,4.4196,'Green')):
  verts=[(cx+rr*math.cos(math.radians(a)),cy+rr*math.sin(math.radians(a)),(.01524*(4.572-rr-.1524-1.8288)/1.524+CURB_TOP) if mat=='Concrete' else CURB_TOP+.009) for a in CORNER_ANGLES for rr in (ri,ro)]
  mesh('Corner '+mat,verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(24)],mat,r,False)
 curb_run('Corner curb return',[(cx+4.572*math.cos(math.radians(a)),cy+4.572*math.sin(math.radians(a)),CURB_TOP) for a in CORNER_ANGLES],r)
 # Concrete fueling pad is fitted to canopy, with a perimeter beyond islands.
 c=p['canopy'];pad=root('FuelPad',(c['center'][0],c['center'][1],.01),c['angle'],'SitePaving',r)
 flat('Fuel apron',(-c['width']/2-1,c['width']/2+1,-c['depth']/2-.8,c['depth']/2+.8),'Concrete',pad)
 for x in [(-c['width']/2+i*3.048) for i in range(int(c['width']/3.048)+1)]:strip('Fuel slab joint',(x,-c['depth']/2-.8),(x,c['depth']/2+.8),.009,'Trim',pad,.001)
 for y in (-3.048,0,3.048):strip('Fuel slab joint',(-c['width']/2-1,y),(c['width']/2+1,y),.009,'Trim',pad,.001)
 # A 12-ft walk contains a 6-ft 1:12 run plus a 6-ft level top landing.
 front=b['front'];walkback=front-p['walk'];bx=b['center_x'];bw=b['width']
 box('Store front walk',(bx,front-p['walk']/2,.0762),(bw+1.1,p['walk'],.1524),'Concrete',r,.015)
 # Ramp and landing stay wholly inside the walk, clear of the level stall aisle.
 # Top walk cells are cut at this gap rather than hidden by a pasted ramp.
 # Its final exact opening is constructed below by replacing the broad walk box.
 old=bpy.data.objects['Store front walk'];bpy.data.objects.remove(old,do_unlink=True)
 access_x=p['access']['center_x'];access_w=p['access']['width']
 x0=bx-(bw+1.1)/2;x1=bx+(bw+1.1)/2;ax0=access_x-access_w/2;ax1=access_x+access_w/2
 for lo,hi in ((x0,ax0),(ax1,x1)):
  box('Walk raised pour',((lo+hi)/2,front-p['walk']/2,.0762),(hi-lo,p['walk'],.1524),'Concrete',r,.012)
 ramp_end=walkback+p['access']['run']
 verts=[(ax0,walkback,0),(ax1,walkback,0),(ax1,ramp_end,.1524),(ax0,ramp_end,.1524)]
 mesh('Accessible walk ramp',verts,[(0,1,2,3)],'Concrete',r,False)
 flat('Accessible level landing',(ax0,ax1,ramp_end,front),'Concrete',r,.1524)
 # Parking row on street face, near-front wheel stops keep overhang off the walk.
 rear=walkback;pf=p['parking_front'];stall_w=9*FT
 start=bx-bw/2+.15
 for i in range(p['stalls']):
  xx=start+i*stall_w
  # Reserve central accessible stall + aisle rather than draw overlapping stripes.
  if xx+stall_w>access_x-2.1 and xx<access_x+1.0:continue
  strip('Faded parking stripe',(xx,pf),(xx,rear-.1),.10,'White',r)
  box('Wheel stop',(xx+stall_w/2,rear-.45,.065),(1.65,.17,.13),'Concrete',r,.035,2)
 # Accessible vehicle space and fully hatched aisle with a clear link to ramp.
 van_right=ax0;van_left=van_right-3.3528
 for xx in (van_left,van_right,ax1):strip('Accessible stall boundary',(xx,pf),(xx,rear),.10,'White',r)
 for yy in [pf+.3+j*.50 for j in range(int((rear-pf-.5)/.5))]:strip('Access aisle hatching',(ax0+.07,yy),(ax1-.07,yy+.38),.065,'White',r)
 # Accessible pictogram uses analytic wheelchair strokes and a disk, no copied font icon.
 icon=root('AccessiblePaint',((van_left+van_right)/2,pf+2.6,.004),kind='SitePaving',parent=r)
 pts=[(.39*math.cos(math.radians(45+i*300/15)),.39*math.sin(math.radians(45+i*300/15))) for i in range(16)]
 for a,bb in zip(pts,pts[1:]):strip('Wheelchair wheel',a,bb,.065,'White',icon,0)
 for a,bb in [((-.05,.10),(-.05,.58)),((-.05,.10),(.40,.10)),((.4,.10),(.53,-.18))]:strip('Wheelchair person',a,bb,.07,'White',icon,0)
 cylinder('Wheelchair head',(-.05,.74,-.001),(-.05,.74,.002),.105,'White',icon,16)
 # Sign is behind walk's edge and outside access aisle.
 sg=root('AccessibleSign',(van_left+.15,rear-.20,0),kind='AccessibleSign')
 cylinder('Accessible sign post',(0,0,.02),(0,0,2.12),.025,'Metal',sg,10)
 panel('Accessible sign',0,-.025,1.90,.40,.57,'White',sg,.02)
 panel('Accessible blue pictogram',0,-.038,1.93,.30,.29,'Blue',sg,.005)
 wheelchair_sign(sg,0,-.047,1.92,.24)
 text('Accessible sign message','RESERVED',(0,-.044,2.12),.048,'Green',sg)
 text('Accessible sign message','VAN ACCESSIBLE',(0,-.044,1.67),.032,'Green',sg)
 # Low shrubs on rear and side property lines; original loose leaf masses.
 # Continuous beds, with actual low curb edging, replace isolated soil pads.
 rear_start=-W/2+5.5
 flat('East landscape strip',(W/2-1.4,W/2,-D/2+1,D/2),'Soil',r,.012)
 flat('Rear landscape strip',(rear_start,W/2-1.4,D/2-1.4,D/2),'Soil',r,.012)
 box('East planting curb',(W/2-1.4,.5,.0375),(.10,D-1,.075),'Concrete',r,.008)
 box('Rear planting curb',((rear_start+W/2-1.4)/2,D/2-1.4,.0375),(W/2-1.4-rear_start,.10,.075),'Concrete',r,.008)
 box('Landscape strip end',(rear_start,D/2-.7,.0375),(.10,1.4,.075),'Concrete',r,.008)
 rng=random.Random(p['seed'])
 for axis in ('rear','east'):
  for i in range(12):
   xx=-W/2+2+i*(W-4)/11 if axis=='rear' else W/2-.65
   yy=D/2-.65 if axis=='rear' else -D/2+2+i*(D-4)/11
   # Avoid cooler/service yard region, leaving room behind the shell.
   if axis=='rear' and (abs(xx-bx)<bw/2+1 or xx<rear_start+.3):continue
   for j in range(4):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(xx+rng.uniform(-.28,.28),yy+rng.uniform(-.28,.28),.38+rng.uniform(-.1,.1)))
    ob=bpy.context.object;ob.name='Low shrub form';ob.scale=(.40,.35,.30);ob.data.materials.append(M['Green']);own(ob,r)
 # Tank pad at southeast edge, reachable from entrance without crossing footpath.
 tank=root('TankPad',(W/2-4.2,-D/2+6.0,0),kind='TankPad')
 flat('Tank service pad',(-2.3,2.3,-2.0,2.0),'Concrete',tank,.006)
 for i,(mat,label) in enumerate((('White','REG'),('Blue','PLUS'),('Red','PREM'),('Orange','VAPOR'))):
  xx=(i-1.5)*.95;cylinder('Fill cover frame',(xx,0,.007),(xx,0,.021),.245,'Trim',tank,24)
  if i in (1,2):cylinder('Ethanol extender white border',(xx,0,.021),(xx,0,.026),.232,'White',tank,24)
  cylinder('Color coded fill cover',(xx,0,.021),(xx,0,.026),.219,mat,tank,24)
  if i<3:
   box('Unleaded cross',(xx,0,.027),(.29,.055,.003),'Black' if i==0 else 'White',tank,0)
   box('Unleaded cross',(xx,0,.027),(.055,.29,.003),'Black' if i==0 else 'White',tank,0)
 for xx in (-1.6,1.6):
  cylinder('Monitoring cover',(xx,1.1,.007),(xx,1.1,.024),.12,'White',tank,16)
  mesh('Monitoring black triangle',[(xx-.07,1.06,.025),(xx+.07,1.06,.025),(xx,1.18,.025)],[(0,1,2)],'Black',tank,False)
 # Three separate protected 12 ft tank vents along the east property boundary.
 vt=root('TankVents',(W/2-1.1,1.0,0),kind='TankVents')
 for i in range(3):
  yy=i*.35
  cylinder('Vent pipe',(0,yy,0),(0,yy,12*FT),.030,'Metal',vt,12)
  cylinder('Vent cap',(0,yy,12*FT),(0,yy,12*FT+.10),.055,'Trim',vt,12)
 for zz in (.6,2.1):box('Vent support',(0,.35,zz),(.13,1.0,.05),'Trim',vt,.002)
 for edge in ('south','west'):street_edge(edge,p,r)
 for drive in p['driveways']:
  south=drive['edge']=='south';dc=drive['center'][0] if south else drive['center'][1]
  angle=90 if south else 0
  def port(v,z):return (dc,-D/2+v,z) if south else (-W/2+v,dc,z)
  socket('Socket_Drive_'+drive['edge'],port(.1524,0),r,'private_paving_24ft',angle)
  socket('Socket_GroundCurb_'+drive['edge'],port(-3.3528,FLOW),r,'ground_curb_flowline',angle)
  socket('Socket_GroundApron_'+drive['edge'],port(-3.2004,FLOW),r,'ground_apron_origin',angle)
  socket('Socket_GroundWalk_'+drive['edge'],port(-1.3716,FLOW),r,'ground_sidewalk_origin',angle)

 return r


def context_roads(p):
 W,D=p['lot'];r=root('PresentationRoads',kind='CONTEXT')
 # One union surface avoids coincident road skins and self-shadow squares.
 # This flat presentation roadway is separate from the station export.
 bounds=[(-W/2-15,W/2+30,-D/2-11.0,-D/2-3.80),
         (-W/2-11.0,-W/2-3.80,-D/2-30,D/2+30),
         (-W/2-20,-W/2+1.2192,-D/2-20,-D/2+1.2192)]
 xs=sorted({v for a,b,c,d in bounds for v in (a,b)});ys=sorted({v for a,b,c,d in bounds for v in (c,d)})
 verts=[(x,y,FLOW+.00635) for y in ys for x in xs];faces=[];n=len(xs)
 for j,(c,d) in enumerate(zip(ys,ys[1:])):
  for i,(a,b) in enumerate(zip(xs,xs[1:])):
   if any(x0<(a+b)/2<x1 and y0<(c+d)/2<y1 for x0,x1,y0,y1 in bounds):
    q=j*n+i;faces.append((q,q+1,q+n+1,q+n))
 mesh('Presentation roadway',verts,faces,'Asphalt',r,False)
 # Procedural distant surroundings have subdued grass, avoiding a false blue horizon.
 flat('Distant grade',(-2000,2000,-2000,2000),'Green',r,FLOW-.025)
 return r
