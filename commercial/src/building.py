"""Reusable one-story retail envelope: bays, storefront, coping and services.

A strip mall can call retail_shell repeatedly for tenant bays or pass a wider
BuildingSpec. Fuel equipment and corner-site choices do not enter this module.
"""
import math
from geometry import *


def wall_with_openings(name,width,height,openings,parent,y=0,thickness=.2032,mat='Wall'):
 """Disjoint solids around real rectangular holes, including depth returns."""
 xs=sorted(set([-width/2,width/2]+[x+s*w/2 for x,w,z,h in openings for s in (-1,1)]))
 for a,b in zip(xs,xs[1:]):
  if b-a<1e-6:continue
  mid=(a+b)/2;holes=sorted((z,z+h) for x,w,z,h in openings if x-w/2<mid<x+w/2)
  cursor=0
  for lo,hi in holes+[(height,height)]:
   if lo>cursor:box(name+' pier',(mid,y,cursor+(lo-cursor)/2),(b-a,thickness,lo-cursor),mat,parent,.003)
   cursor=max(cursor,hi)


def glazed_leaf(name,x,y,z,w,h,parent,open_sign=1):
 # Outward hinge at jamb; separate fixed frame has 6 mm fit clearances.
 direction=-1 if name.endswith('_Right') else 1
 pivot=hinge(name,(x-direction*w/2,y-.09,z),parent,(-100,0) if direction>0 else (0,100))
 frame(name+' aluminum',direction*w/2,0,h/2,w-.012,h-.008,'Trim',pivot,.055,.047)
 panel(name+' glass',direction*w/2,.003,h/2,w-.12,h-.13,'Glass',pivot,.006)
 for v in (.72,1.16):
  cylinder(name+' pull mounts',(direction*(w-.14),-.035,v),(direction*(w-.14),-.09,v),.012,'Metal',pivot,10)
 cylinder(name+' pull',(direction*(w-.14),-.09,.72),(direction*(w-.14),-.09,1.16),.012,'Metal',pivot,10)
 box(name+' bottom kick',(direction*w/2,-.029,.14),(w-.13,.009,.19),'Metal',pivot,.002)
 for zz in (.18,1.05,1.92):cylinder(name+' hinge',(0,0,zz),(0,0,zz+.09),.012,'Metal',pivot,10)
 socket(name+'__Hand',(direction*(w-.14),-.09,1.0),pivot,'door_handle')
 return pivot


def storefront(name,x,y,width,parent,door=False):
 bottom=.27;head=2.75;transom=2.20
 if door:
  for xx in (-.4572,.4572):glazed_leaf(name+('_Left' if xx<0 else '_Right'),x+xx,y-.008,.158,.9144,2.03,parent,1)
  for side in (-1,1):box(name+' entry jamb',(x+side*(width-.055)/2,y,1.4512),(.055,.12,2.5976),'Trim',parent,.002)
  box(name+' entry head',(x,y,head-.0275),(width-.11,.12,.055),'Trim',parent,.002)
  box(name+' door header',(x,y,2.22),(width,.12,.07),'Trim',parent,.002)
  panel(name+' transom',x,y,2.475,width-.12,.43,'Glass',parent,.006)
  return
 frame(name+' frame',x,y,(bottom+head)/2,width,head-bottom,'Trim',parent,.055,.12)
 box(name+' crossbar',(x,y,transom),(width-.10,.105,.042),'Trim',parent,.002)
 panel(name+' lower glass',x,y,bottom+(transom-bottom)/2,width-.12,transom-bottom-.07,'Glass',parent,.006)
 panel(name+' upper glass',x,y,(head+transom)/2,width-.12,head-transom-.07,'Glass',parent,.006)
 # Deep window bay: floor, ceiling, interior partition and separate small shelves.
 box(name+' ceiling',(x,y+.9,2.92),(width,1.8,.06),'White',parent,0)
 box(name+' interior floor',(x,y+1.1,.141),(width,2.2,.04),'Concrete',parent,0)
 box(name+' interior back',(x,y+2.2,1.55),(width,.06,2.8),'Inside',parent,0)
 for zz in (.65,1.05,1.45):
  box(name+' shelf',(x,y+1.65,zz),(width*.78,.42,.035),'Trim',parent,.001)
  for i in range(5):box(name+' stock',(x-width*.32+i*width*.16,y+1.67,zz+.12),(.11,.12,.20),'Accent' if i%2 else 'White',parent,.002)


def rooftop_unit(name,p,parent,size=(2.0,1.3,1.2)):
 x,y,z=p;w,d,h=size
 box(name+' curb',(x,y,z+.12),(w-.15,d-.15,.24),'Trim',parent,.008)
 box(name+' shell',(x,y,z+.24+h/2),(w,d,h),'Metal',parent,.018,2)
 box(name+' folded cap',(x,y,z+.25+h),(w+.06,d+.06,.055),'White',parent,.008)
 # Open louvered condenser side, backed by a dark plenum, not pasted stripes.
 panel(name+' plenum',x,y-d/2-.003,z+.24+h*.5,w-.15,h-.20,'Black',parent)
 for i in range(12):box(name+' louver',(x,y-d/2-.026,z+.36+i*(h-.28)/12),(w-.16,.056,.022),'Metal',parent,.002)
 for xx in (-w*.26,w*.26):
  cylinder(name+' fan dark',(x+xx,y,z+.27+h),(x+xx,y,z+.285+h),.34,'Black',parent,24)
  for j in range(7):
   # Bar grille, silhouette only; finer mesh belongs in trim normals.
   yy=(j-3)*.085;half=math.sqrt(max(.001,.33**2-yy**2))
   cylinder(name+' grille',(x+xx-half,y+yy,z+.30+h),(x+xx+half,y+yy,z+.30+h),.007,'Metal',parent,6)
 box(name+' disconnect',(x+w/2+.04,y,z+.6),(.07,.28,.38),'Trim',parent,.004)
 tube(name+' conduit',[(x+w/2+.08,y,z+.5),(x+w/2+.15,y,z+.28),(x+w/2+.26,y,z+.05)],.016,'Metal',parent,8)


def retail_shell(spec,brand):
 b=spec;w,d=b['width'],b['depth'];fy=-d/2
 r=root('Store',(b['center_x'],b['front']+d/2,0),kind='Store')
 # Every wall has actual thickness; the floor edge and membrane are distinct.
 box('Store slab edge',(0,0,.0762),(w,d,.1524),'Concrete',r,.01)
 # Door and windows occupy an actual common storefront hole, with masonry piers.
 sw=w-4.0;entryw=1.98
 wall_with_openings('Front',w,b['parapet'],[(0,sw,.20,2.68)],r,fy+.1016)
 for side in (-1,1):box('Side wall',(side*(w/2-.1016),0,b['parapet']/2),(.2032,d-.2032,b['parapet']),'Wall',r,.004)
 # Back service door cut, built in a rotated local wall frame.
 back=root('Store_BackWall',(0,d/2-.1016,0),180,parent=r,kind='Store')
 drains=[(xx,.312,b['roof']+.005,.17) for xx in (-w*.35,w*.35)]
 wall_with_openings('Rear',w,b['parapet'],[(w*.28,1.016,.1524,2.134),*drains],back)
 dp=hinge('ServiceDoor',(w*.28-.495,-.13,.158),back,(-100,0))
 box('Steel service leaf',(.495,0,1.055),(.984,.045,2.10),'Trim',dp,.004)
 box('Service panic bar',(.50,-.06,1.04),(.68,.035,.035),'Metal',dp,.003)
 # Storefront rhythmic 5 ft bays around a central paired entry.
 span=(sw-entryw)/2;nb=max(2,round(span/1.524));bay=span/nb
 for side in (-1,1):
  for i in range(nb):
   x=side*(entryw/2+(i+.5)*bay)
   storefront('Storefront',x,fy-.025,bay,r)
   if i in (0,nb-1):
    panel('Fictional window poster',x,fy+.012,1.52,min(.58,bay*.55),.74,'Accent',r,.004)
    text('Poster offer','FRESH\nCOFFEE' if i==0 else 'DAILY\nGOODS',(x,fy-.002,1.52),.095,'Light',r)
 storefront('Entry',0,fy-.045,entryw,r,True)
 # Shallow foyer, with full-width threshold and door clearance, no fake solid hole.
 box('Threshold',(0,fy-.02,.1524),(2.02,.25,.016),'Metal',r,.002)
 box('Foyer floor',(0,fy+1.4,.136),(entryw,2.8,.034),'Concrete',r,0)
 box('Foyer rear',(0,fy+3,1.55),(entryw,.08,2.8),'Inside',r,0)
 for xx in (-1.02,1.02):box('Foyer cheek',(xx,fy+1.5,1.55),(.08,3,2.8),'Inside',r,0)
 # Integral sign band and masonry soldier/control courses; no applied wall boxes.
 for zz in (2.96,4.12):box('Facade belt',(0,fy-.12,zz),(w,.075,.13),'Concrete',r,.004)
 brand_sign('Store brand',(0,fy-.10,3.55),min(7.4,w*.42),.83,brand,r)
 text('Store descriptor','FOOD  •  COFFEE  •  EVERYDAY',(0,fy-.159,2.96),.115,'Trim',r)
 # Parapet rises above the real roof; return and folded coping protect both skins.
 roof=b['roof'];box('Roof membrane',(0,0,roof),(w-.40,d-.40,.045),'Roof',r,0)
 for yy in (-d/2+.1016,d/2-.1016):
  box('Coping horizontal',(0,yy,b['parapet']+.018),(w+.085,.30,.036),'Trim',r,.003)
  for off in (-.142,.142):box('Coping folded hem',(0,yy+off,b['parapet']-.025),(w+.085,.016,.065),'Trim',r,.002)
 for xx in (-w/2+.1016,w/2-.1016):
  box('Coping horizontal',(xx,0,b['parapet']+.018),(.30,d-.14,.036),'Trim',r,.003)
  for off in (-.142,.142):box('Coping folded hem',(xx+off,0,b['parapet']-.025),(.016,d-.14,.065),'Trim',r,.002)
 # Roof drainage on the rear: scupper boxes through parapet with supported pipes.
 for xx in (-w*.35,w*.35):
  for side in (-1,1):box('Scupper sleeve jamb',(xx+side*.15,d/2-.07,roof+.09),(.012,.36,.17),'Metal',r,.001)
  for zz in (.011,.169):box('Scupper sleeve sill',(xx,d/2-.07,roof+zz),(.288,.36,.012),'Metal',r,.001)
  def section(width,depth,z):return [(xx+x,d/2+.15+y,z) for x,y in ((-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2))]
  loops=[section(.12,.10,roof-.25),section(.35,.25,roof-.01),section(.33,.23,roof-.01),section(.10,.08,roof-.25)]
  own(G.ring_loft('Open conductor hopper',loops,M['Metal']),r)
  loops=[section(.10,.08,.16),section(.10,.08,roof-.25),section(.09,.07,roof-.25),section(.09,.07,.16)]
  own(G.ring_loft('Hollow downpipe',loops,M['Metal']),r)
  for zz in (.50,2.0,3.4):
   box('Downpipe strap front',(xx,d/2+.195,zz),(.12,.010,.025),'Trim',r,.001)
   for side in (-1,1):
    box('Downpipe strap return',(xx+side*.055,d/2+.10,zz),(.010,.19,.025),'Trim',r,.001)
    box('Downpipe wall anchor',(xx+side*.055,d/2+.005,zz),(.025,.012,.06),'Trim',r,.001)
  box('Splash block',(xx,d/2+.43,.04),(.35,.70,.08),'Concrete',r,.015)
 for i in (-1,1):rooftop_unit('Roof unit',(i*w*.23,1,roof+.0225),r)
 # Roof vent boots and a pipe above their roof-mounted seals.
 for xx in (-.7,.7):
  cylinder('Vent boot',(xx,2.4,roof+.02),(xx,2.4,roof+.10),.18,'Black',r,16)
  cylinder('Plumbing vent',(xx,2.4,roof+.08),(xx,2.4,roof+.62),.055,'Metal',r,14)
 # Meter and switchgear: wall-mounted, with conduit physically joining the boxes.
 xx=w/2+.05
 box('Electric cabinet',(xx,1.8,1.2),(.18,1.0,1.4),'Metal',r,.008)
 for yy in (1.52,2.05):
  cylinder('Meter housing',(xx+.10,yy,1.8),(xx+.18,yy,1.8),.14,'Metal',r,20)
  cylinder('Conduit',(xx,yy,.08),(xx,yy,.62),.025,'Metal',r,10)
 box('Service disconnect',(xx,2.65,1.3),(.16,.34,.60),'Trim',r,.004)
 if b['cooler']:
  box('Walk-in cooler insulated box',(w/2+1.25,d*.19,1.6),(2.50,3.7,3.10),'White',r,.025)
  for yy in (-1.5,-.5,.5,1.5):box('Cooler panel seam',(w/2+2.505,d*.19+yy,1.6),(.012,.012,3.0),'Metal',r,0)
  box('Cooler folded roof',(w/2+1.25,d*.19,3.18),(2.58,3.78,.055),'Metal',r,.005)
  rooftop_unit('Cooler condenser',(w/2+1.25,d*.19,3.2),r,(1.1,.75,.65))
 socket('Socket_StoreEntry',(0,fy-.17,.1524),r,'pedestrian_entry')
 socket('Socket_StoreWalk',(0,fy,0),r,'retail_frontage_grade')
 return r
