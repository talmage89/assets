"""PD Hearth 12: original visual game geometry, authored in millimeters.

Reference pixels are never read. Internal parts describe visible poses only;
the scene is neither a functioning mechanism nor a manufacturing model.
Wood is a subdivided three-dimensional cage, retained as a high bake source.
"""
import argparse, json, math, sys, hashlib
from pathlib import Path
import bpy, bmesh
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M, weapon as W
from clips import build_clips
from feed import PITCH,BONES
def source_hash():
 return hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('build.py','clips.py','feed.py','interface.py'))).hexdigest()
GENERATOR_HASH=source_hash()

PARTS=[]; HIGH=[]; MAT={}
GRIP=Vector((0,-55,16))
BORE=65.; TUBE=29.; BREECH=186.1; MUZZLE=656.; PAD=-322.
HEADS={'Root':(0,-50,0),'Forend':(0,375,29),'Bolt':(0,116,65),
 'BoltLock':(0,150,69),'Carrier':(0,30,20),'CarrierShell':(0,104,29),
 'CarrierGuide':(0,104,29),'FiredGuide':(0,BREECH,BORE),'FiredHull':(0,BREECH,BORE),
 'TubeFeedGuide':(0,200,29),
 'Trigger':(0,29,12),'Safety':(0,1,8),'ActionRelease':(-12.8,45,13),
 'ShellStopL':(-12.5,185,29),'ShellStopR':(12.5,185,29),
 'Follower':(0,200+4*PITCH,29),'ChamberShell':(0,BREECH,BORE),
 'InsertShell':(0,130,29),'ShellGuide':(0,130,29),'Magazine':(0,200,29),
 **{'Tube'+str(i+1):(0,200+i*PITCH,29) for i in range(4)}}
SOCKETS={'Socket_Muzzle':(0,MUZZLE,BORE),'Socket_Foregrip':(-19,373,7),
 'Socket_Butt':(0,PAD+.11*57,-37),'Socket_Eye':(0,-80,80.6),
 'Socket_Ejection':(18,117,63),'Socket_MagWell':(0,107,14),
 'Socket_Magazine':HEADS['Magazine'],'Socket_SupportHand':(-19,373,7),
 'Socket_Shell':HEADS['InsertShell']}
def P(p):return tuple((Vector(p)-GRIP)*.001)
def material(name,color,metal,rough):
 m=bpy.data.materials.new('CP_'+name);m.use_nodes=True;m.diffuse_color=(*color,1)
 b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*color,1)
 b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough
 return m
def materials():
 for k,c,m,r in [('blue',(.012,.014,.016),.8,.36),('wood',(.05,.018,.006),0,.48),
  ('rubber',(.007,.006,.005),0,.68),('steel',(.23,.235,.24),1,.28),
  ('dark',(.035,.035,.033),.9,.38),('brass',(.48,.30,.085),1,.28),
  ('hull',(.30,.018,.009),0,.36),('primer',(.34,.32,.26),1,.35),
  ('mouth',(.015,.007,.004),0,.77),('follower',(.25,.065,.012),0,.48)]:MAT[k]=material(k,c,m,r)
def reg(ob,bone='Root',radius=0,segments=3):
 if radius:
  M.bevel(ob,radius,segments);n=ob.modifiers.new('Area normals','WEIGHTED_NORMAL');n.keep_sharp=True
 M.smooth(ob,42);M.apply(ob);ob['bone']=bone;ob['asset_set']='Shotgun';ob['part_name']=ob.name;PARTS.append(ob)
 return ob
def box(name,lo,hi,mat='blue',bone='Root',radius=.35,segments=3,register=True):
 a,b=Vector(lo),Vector(hi);o=M.box(name,(a+b)/2,b-a,MAT[mat],0);M.apply(o)
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 return reg(o,bone,radius,segments) if register else o
def profile(name,pts,lo,hi,mat='blue',bone='Root',axis='X',radius=.35,register=True):
 o=M.profile(name,pts,lo,hi,MAT[mat],axis=axis)
 return reg(o,bone,radius) if register else o
def lathe(name,points,mat='blue',bone='Root',axis='Y',center=(0,0),n=48,closed=False,register=True):
 o=M.lathe(name,points,MAT[mat],segments=n,axis=axis,center=center,closed=closed)
 return reg(o,bone) if register else o
def cut(ob,tool,operation='DIFFERENCE'):
 tool.data.materials.clear();tool.data.materials.append(ob.data.materials[0]);M.boolean(ob,tool,operation)
 return ob
def cutbox(ob,lo,hi):return cut(ob,box('tool',lo,hi,register=False))
def subd(ob,level):
 m=ob.modifiers.new('Carved compound surface','SUBSURF');m.levels=level;m.render_levels=level;M.apply(ob)
 return ob
def high_copy(ob,bone='Root'):
 h=ob.copy();h.data=ob.data.copy();bpy.context.collection.objects.link(h);h.name='HIGH_'+ob.name
 h['bake_only']=True;h['low_target']=ob.name;h['asset_set']='Shotgun';h['bone']=bone;HIGH.append(h);return h
def reduce(ob,target):
 n=sum(len(f.vertices)-2 for f in ob.data.polygons)
 if n>target:
  mod=ob.modifiers.new('Silhouette budget','DECIMATE');mod.ratio=target/n;M.apply(ob)
 return ob

RECEIVER=[(-18,17.1,18,66),(-14,17.4,17.7,69),(-5,17.75,17.2,74),
 (8,17.75,16.8,77.6),(24,17.75,16.7,79.4),(42,17.75,16.9,80),
 (83,17.75,17.3,80),(125,17.75,18.1,80),(165,17.75,19.7,80),
 (182,17.65,20.8,79.8),(191,17.2,21.7,78.8),(195,16.7,22,78)]
def receiver_shape(y):
 """Monotone Hermite profile and derivatives for continuous machined shading."""
 i=next((i for i in range(len(RECEIVER)-1) if y<=RECEIVER[i+1][0]),len(RECEIVER)-2)
 a,b=RECEIVER[i:i+2];h=b[0]-a[0];t=max(0,min(1,(y-a[0])/h));values=[];derivatives=[]
 for k in (1,2,3):
  def slope(j):
   if j==0:return (RECEIVER[1][k]-RECEIVER[0][k])/(RECEIVER[1][0]-RECEIVER[0][0])
   if j==len(RECEIVER)-1:return (RECEIVER[j][k]-RECEIVER[j-1][k])/(RECEIVER[j][0]-RECEIVER[j-1][0])
   l=(RECEIVER[j][k]-RECEIVER[j-1][k])/(RECEIVER[j][0]-RECEIVER[j-1][0]);r=(RECEIVER[j+1][k]-RECEIVER[j][k])/(RECEIVER[j+1][0]-RECEIVER[j][0])
   return 2*l*r/(l+r) if l*r>0 else 0
  m,n=slope(i),slope(i+1)
  values.append((2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*h*m+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*h*n)
  derivatives.append(((6*t*t-6*t)*a[k]+(3*t*t-4*t+1)*h*m+(-6*t*t+6*t)*b[k]+(3*t*t-2*t)*h*n)/h)
 return values,derivatives
def receiver_section(y,w,bottom,top,inside=False):
 spring=top-14.75;rr=12.25 if inside else 14.75
 if inside:w-=3.75;bottom+=1.1
 section=[(-w,bottom+2)]
 section += [(w*math.cos(math.pi-i*math.pi/32),spring+rr*math.sin(math.pi-i*math.pi/32)) for i in range(33)]
 section += [(w,bottom+2),(w-1.6,bottom),(-w+1.6,bottom)]
 return [(x,y,z) for x,z in section]
def receiver():
 # The crown rolls into the stock head; the lower machining rises toward the
 # barrel seat. Independently loft the inner roof so the roll cannot be cut off.
 ys=[a[0]+(b[0]-a[0])*i/3 for a,b in zip(RECEIVER,RECEIVER[1:]) for i in range(3)]+[195]
 loops=[receiver_section(y,*receiver_shape(y)[0]) for y in ys]
 o=M.loft('Receiver',loops,MAT['blue'])
 inner=[receiver_section(y,*receiver_shape(y)[0],True) for y in [-13.7]+[y for y in ys if -13.7<y<=182]+[187]]
 cut(o,M.loft('tool',inner,MAT['blue']))
 cutbox(o,(-7.4,149,73.5),(7.4,178,78.2))
 for s in (-1,1):
  a,b=sorted((s*10,s*15.7));cutbox(o,(a,168,23),(b,200,35))
  a,b=sorted((s*11.5,s*14.2));cutbox(o,(a,180,41.5),(b,200,45.5))
 cut(o,lathe('tool',[(-15,0),(-15,2.9),(15,2.9),(15,0)],axis='X',center=(30,20),n=24,register=False))
 port=[(y+132,z+63) for y,z in M.rounded_rectangle(100,24,11.5,12)]
 cut(o,profile('tool',port,9,25,register=False))
 loading=[(x,y+104) for x,y in M.rounded_rectangle(27.0,112,4.5,8)]
 cut(o,profile('tool',loading,10,33,axis='Z',register=False))
 # A continuous feed throat clears the raised receiver floor all the way from
 # the loading opening into the tube; there is no solid web in the shell path.
 for y,z,r in [(180,BORE,12.85),(152,TUBE,12.65)]:
  cut(o,lathe('tool',[(y,0),(y,r),(200,r),(200,0)],center=(0,z),n=64,register=False))
 # Internal ramp clearance for the inclined hull before it reaches the bore.
 cutbox(o,(-11.4,143,40),(11.4,184,65))
 reg(o,radius=.65,segments=3)
 # Preserve the crown: unconstrained QEM collapse can move a Boolean bevel
 # junction millimeters off this shallow roof. Dissolve only coplanar faces.
 planar=o.modifiers.new('Coplanar machining faces','DECIMATE');planar.decimate_type='DISSOLVE';planar.angle_limit=math.radians(.12);M.apply(o)
 o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));M.smooth(o,42)
 wn=o.modifiers.new('Continuous roof and flat sides','WEIGHTED_NORMAL');wn.keep_sharp=True;M.apply(o)
 for y in (8,69):
  # Two actual receiver cross-pin seats and slightly recessed heads.
  for side in (-1,1):
   a,b=sorted((side*17.55,side*17.85))
   lathe('Receiver_Pin',[(a,0),(a,2.35),(b,2.35),(b,0)],'dark',axis='X',center=(y,29),n=24)
 # A visible seat for the rising visual locking block. Its contacting underside
 # is audited separately from serialization and unwanted penetration.
 box('Barrel_LockSeat',(-7.1,160,77.8),(7.1,177,79),'dark',radius=.15)
 # Barrel extension, with bore through it, remains visible in the open port.
 lathe('Barrel_Extension',[(186.1,10.35),(186.1,12.55),(194,12.55),(194,10.35)],
       'dark',center=(0,BORE),n=32,closed=True)
 ext=PARTS[-1]
 cut(ext,lathe('tool',[(184,0),(184,11.35),(188,11.35),(188,0)],center=(0,BORE),n=48,register=False))
 cutbox(ext,(10.2,185.8,63),(12.8,189,67))

def barrel_tube():
 # Cylinder bore, chamber-side visual counterbore, rolled crown highlight.
 points=[(BREECH,12.45),(226,12.45),(248,11.8),(649,11.25),(655.5,11.25),
  (656,10.9),(656,9.65),(655.4,9.25),(270,9.25),(256.4,10.2),(189.2,10.2),(189.2,11.35),(BREECH,11.35)]
 # Keep 96 sides at the visible muzzle. Half-density hidden bore rings pay for
 # the receiver's preserved crown without reducing its silhouette resolution.
 shell_surface('Barrel',[(a,r,96 if i<=6 else 48) for i,(a,r) in enumerate(points)]+[(points[0][0],points[0][1],96)],(0,0,BORE),'blue','Root')
 cutbox(PARTS[-1],(10.2,185.8,63),(12.8,189,67))
 tube=lathe('Magazine_Tube',[(190,11.5),(190,12.5),(534,12.5),(534,11.5)],center=(0,TUBE),n=64,closed=True)
 for s in (-1,1):
  a,b=sorted((s*10,s*16))
  cutbox(tube,(a,189,23.5),(b,205 if s>0 else 200,34.5))
 # The welded barrel lug wraps the tube; the cap bears against its front face.
 lathe('Barrel_Ring',[(524,12.65),(524,15.8),(534,15.8),(534,12.65)],center=(0,TUBE),n=64,closed=True)
 box('Ring_Bridge',(-6.5,525,43),(6.5,533,54),'blue',radius=2,segments=4)
 cap=lathe('Magazine_Cap',[(534,0),(534,14),(534.7,14.5),(535.2,14.6),
  (542.5,14.6),(543.2,14.4),(545,12.8),(545,0)],center=(0,TUBE),n=64)
 # A radial field makes original scallops without microscopic Boolean slivers.
 for v in cap.data.vertices:
  r=math.hypot(v.co.x,v.co.z-TUBE)
  if 534.7<=v.co.y<=543.2 and r>14.3:
   t=math.atan2(v.co.z-TUBE,v.co.x);rr=r-.55*(.5+.5*math.cos(16*t))**2
   v.co.x*=rr/r;v.co.z=TUBE+(v.co.z-TUBE)*rr/r
 cap.data.normals_split_custom_set([(0,0,0)]*len(cap.data.loops));M.smooth(cap,50)
 # Brass bead is a sphere on a short shouldered foot, rather than a flat dot.
 lathe('Bead_Foot',[(76.0,0),(76.0,1.25),(79.4,1.25),(79.4,0)],'brass',axis='Z',center=(0,645),n=32)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=1.65,location=(0,645,80.6))
 o=bpy.context.object;o.name='Bead';o.data.materials.append(MAT['brass']);o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4);reg(o)
 for name,y,z,axis in [('Sling_Front',547,29,'Y'),('Sling_Rear',-252,-85,'Z')]:
  if axis=='Y':
   lathe(name+'_Stem',[(545,0),(545,2),(551,2),(551,0)],'dark',center=(0,z),n=16)
   pts=[(x,zz+z) for x,zz in M.rounded_rectangle(7.5,7.5,2.0,4)]
   o=profile(name+'_Eye',pts,549,551,'dark',axis='Y',register=False)
   cut(o,lathe('tool',[(548,0),(548,2.05),(552,2.05),(552,0)],center=(0,z),n=20,register=False));reg(o,radius=.2);reduce(o,220)
  else:
   lathe(name+'_Stem',[(-89,0),(-89,2),(-82,2),(-82,0)],'dark',axis='Z',center=(0,y),n=16)
   o=profile(name+'_Eye',[(yy+y,zz-90) for yy,zz in M.rounded_rectangle(7,7,2,4)],-1.2,1.2,'dark',register=False)
   cut(o,lathe('tool',[(-3,0),(-3,1.9),(3,1.9),(3,0)],axis='X',center=(y,-90),n=16,register=False));reg(o,radius=.2);reduce(o,220)

# Y / half width / bottom / top. Independent horizontal and vertical curvature
# creates the narrow wrist, cheek roll and thick butt. This is not a side extrusion.
STOCK=[(-298,21.8,-102,20),(-297.3,21.9,-102,20),(-291.4,22.2,-99,21.1),
 (-270,22.5,-91,23.7),(-245,22.3,-80,26.2),(-210,21.7,-62,29.7),
 (-175,20.8,-47,33.2),(-145,19.8,-34.5,36),(-125,18.8,-28.5,37.6),
 (-113,18,-28.7,38.3),(-104,17.5,-32.5,38.6),(-97,17.1,-37,38.4),
 (-94,17,-38.6,37.7),(-91,16.9,-39.3,37.6),(-80,16.2,-41.7,37.7),
 (-77,16,-41.4,38),(-74,15.9,-35,38.7),(-68,15.9,-16,40.5),
 (-60,15.9,0,42.6),(-55,16,1,45),(-42,16.3,8,52),
 (-30,16.7,14,59.5),(-21,17.1,17.6,65),(-18.3,17.1,18,66),(-18,17.1,18,66)]
def stock_loop(y,hw,bottom,top,n=32):
 loop=[]
 for i in range(n):
  t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
  # Elliptical comb rolls away from cheek; the belly has slightly fuller cheeks.
  power=2.3 if s<0 else 2.0
  x=hw*math.copysign(abs(c)**(2/power),c)
  z=(top+bottom)/2+(top-bottom)/2*math.copysign(abs(s)**(2/power),s)
  x*=1-.10*max(0,s)**4
  # The pitched butt is a plane, including its toe; fade the pitch forward.
  yy=y+.11*(20-z)*max(0,min(1,(-270-y)/28))
  loop.append((x,yy,z))
 return loop
def furniture():
 stock=M.loft('Stock',[stock_loop(*r) for r in STOCK],MAT['wood']);subd(stock,2)
 # Carve a small oblique end flat into the semi-pistol grip, then ease its
 # perimeter. It is a real cap plane across the volume, not a side-view kink.
 cut(stock,profile('tool',[(-100,-70),(-73,-70),(-73,-41.26),(-100,-35.32)],-30,30,register=False))
 M.bevel(stock,.45,3);M.apply(stock)
 M.smooth(stock,42)
 h=high_copy(stock);h['source_method']='subdivision cage, changing compound sections'
 # Retain source and reduce only the game copy, preserving the smooth normal field.
 reduce(stock,7000)
 stock.data.normals_split_custom_set([(0,0,0)]*len(stock.data.loops));reg(stock)
 # Pad follows the carved butt section, with a rounded shoulder and concave back.
 loops=[]
 for y,s in [(-298,1),(-298.7,1.006),(-300.4,1.012),(-319.8,1.012),(-322,1)]:
  loop=stock_loop(y,21.8*s,-102,20,48)
  loops.append([(x,yy,z) for x,yy,z in loop])
 pad=M.loft('Recoil_Pad',loops,MAT['rubber']);reg(pad,radius=.65,segments=3)
 for z in (-9,-77):
  yy=-321.5+.11*(20-z)
  lathe('Pad_Screw', [(yy,0),(yy,2.1),(yy+.5,2.1),(yy+.5,0)],'dark',center=(0,z),n=16)
 # Sculpted forend cage with tapered ends, broad palms and shallow paired flutes.
 stations=[(296,17.8,20),(296.7,18.4,20.7),(300,19.7,22.4),(306,20,23)]
 for y in range(312,501,8):
  for yy in (y,y+3):
   stations.extend([(yy-.8,20,23),(yy-.2,19.45,22.45),(yy+.2,19.45,22.45),(yy+.8,20,23)])
 stations.extend([(505,19.8,22.6),(510,18,20.5),(514.5,15.4,17),(516,15.1,16.7)])
 stations.sort()
 loops=[]
 for y,w,h in stations:
  loop=[]
  for i in range(32):
   c=math.cos(i*math.tau/32);s=math.sin(i*math.tau/32)
   loop.append((w*math.copysign(abs(c)**(2/3.2),c),y,29+h*math.copysign(abs(s)**(2/2.4),s)))
  loops.append(loop)
 wood=M.loft('Forend_Wood',loops,MAT['wood']);subd(wood,1)
 for yy,zz,rr in [(290,TUBE,14.1),(290,BORE,14.5)]:
  cut(wood,lathe('tool',[(yy,0),(yy,rr),(525,rr),(525,0)],center=(0,zz),n=64,register=False))
 M.smooth(wood,42)
 h=high_copy(wood,'Forend');subd(h,1);h['source_method']='subdivided radial cage with compound tapers and paired grooves'
 # Mill the bar and interceptor inlets after sculpting both surfaces.
 # Subdividing these narrow cavities rounded away their planar end walls.
 for target in (wood,h):
  for s in (-1,1):
   a,b=sorted((s*11.8,s*13.8));cutbox(target,(a,290,41.7),(b,322,45.3))
  cutbox(target,(9.9,290,23),(16.4,305,35.5));M.smooth(target,42)
 reduce(wood,7600);reg(wood,'Forend')
 # Continuous hollow action sleeve with bearing rings. The wood has a real bore.
 lathe('Forend_Sleeve',[(299,12.65),(299,14),(513,14),(513,12.65)],'dark','Forend',center=(0,TUBE),n=48,closed=True)
 cutbox(PARTS[-1],(9.9,298,23),(16.4,305,35.5))
 for y in (315,456):
  lathe('Forend_Bearing',[(y,12.58),(y,12.65),(y+6,12.65),(y+6,12.58)],'steel','Forend',center=(0,TUBE),n=48,closed=True)
 # Two action bars are supported by the sleeve and enter the receiver channels.
 for sign in (-1,1):
  x=sign*12.8
  box('Action_Bar', (x-.7,112,42),(x+.7,321,45),'steel','Forend',radius=.3)
 # A supported visual slide block joins both bars to the bolt's underside.
 # Its upper land and the actual bolt bearing face are independently audited.
 block=[(-13.5,44.8),(-13.5,47.5),(-8,47.5),(-8,55.25),
        (8,55.25),(8,47.5),(13.5,47.5),(13.5,44.8)]
 slide=profile('Action_SlideBlock',block,155,173,'steel','Forend',axis='Y',register=False)
 cutbox(slide,(-10.8,154,42),(10.8,174,52));reg(slide,'Forend',radius=.25)

def trigger():
 # A broad 6 mm blade: +Y-facing hollow, convex grip-side back and forward toe.
 # The hidden rear land rests on the existing plate slot's Y=23 end wall.
 front=[(23,15),(34.5,15),(34.5,13)]
 front+=M.bezier((34.5,13),(27,7),(29,-2),(37.8,-8.0),10)[1:]
 toe=M.bezier((37.8,-8.0),(38.5,-9.0),(37.0,-9.2),(35.2,-8.0),4)[1:]
 back=M.bezier((35.2,-8.0),(25.5,-2),(25.8,6),(29.8,11.5),8)[1:]+[(23,13.0)]
 shoe=profile('Trigger_Shoe',front+toe+back,-3,3,'blue','Trigger',register=False)
 reg(shoe,'Trigger',radius=.55,segments=2)

def controls():
 # Cast bow: a swept elliptical bar, continuously curved in section and in
 # side elevation. Its ends join the plate, rather than hanging as a bracket.
 plate=box('Trigger_Plate',(-12,-7,12),(12,81,20),'dark',register=False)
 loops=[]
 for i in range(49):
  t=math.pi*i/48;y=29+34*math.cos(t);z=14-27*math.sin(t)
  transverse=Vector((0,-27*math.cos(t),34*math.sin(t))).normalized()
  loops.append([tuple(Vector((5.3*math.cos(a*math.tau/12),y,z))+transverse*(2.2*math.sin(a*math.tau/12))) for a in range(12)])
 cut(plate,M.loft('raw_guard',loops,MAT['dark']),'UNION')
 cutbox(plate,(-4,23,1),(4,47,22))
 cutbox(plate,(-12,27,16),(12,83,25))
 cut(plate,lathe('tool',[(-16,0),(-16,3.8),(16,3.8),(16,0)],axis='X',center=(1,8),n=32,register=False))
 reg(plate,radius=.65,segments=3);reduce(plate,1700)
 trigger()
 lathe('Safety_Crossbolt',[(-10,0),(-10,3.5),(-7,3.5),(-7,2.6),(8,2.6),(8,3.5),(10,3.5),(10,0)],
       'dark','Safety',axis='X',center=(1,8),n=32)
 # A raised index ridge can be recognized in silhouette without lettering.
 box('Safety_Index',(-10.3,.3,6.8),(-9.9,1.7,9.2),'steel','Safety',radius=.12)
 lever=M.fillet_polygon([(44,13),(57,13),(57,6),(50,2),(43,3)],1.3,5)
 profile('ActionRelease_Lever',lever,-13.5,-12.1,'dark','ActionRelease',radius=.4)

def mechanism():
 # The rear block ends ahead of the receiver's rolled tail at full stroke.
 # Its bearing land, face, lock and all animation pivots retain their positions.
 body=profile('Bolt_Body',[(x,z+65) for x,z in M.rounded_rectangle(20.8,19.5,4.5,8)],112,184,'dark','Bolt',axis='Y',register=False)
 cutbox(body,(-7.5,149,68),(7.5,178,80))
 cutbox(body,(-12,80,54),(12,151,66));reg(body,'Bolt',radius=.35)
 face=profile('Bolt_Face',[(x,z+65) for x,z in M.rounded_rectangle(20.6,20,6,8)],184,BREECH,'steel','Bolt',axis='Y',radius=.35)
 # The port-side cheek closes the lower battery view while the carrier has
 # clearance in the central underside pocket. Its upper web joins the bolt.
 cheek=profile('Bolt_PortCheek',[(94,51.5),(176,51.5),(176,70.5),(120,70.5),(110,68.5),(94,65)],10.9,12.25,'steel','Bolt',register=False)
 cut(cheek,box('raw cheek web',(9.5,120,68.5),(12.25,176,70.5),'dark',register=False),'UNION')
 reg(cheek,'Bolt',radius=.35)
 # Visible extractor on the right; no detailed hidden fire-control engineering.
 profile('Bolt_Extractor',M.fillet_polygon([(172,59),(185.9,59),(186.1,62),(181,67),(173,67)],.8,4),
  10.7,12.2,'steel','Bolt',radius=.25)
 box('Extractor_ClawArm',(12,183,64),(12.6,187.7,66),'steel','Bolt',radius=0)
 box('Extractor_Claw',(10.95,187.5,64),(12.6,187.7,66),'steel','Bolt',radius=0)
 box('Ejector_Spring',(-14.2,74,63.5),(-11.4,96,66.5),'dark',radius=0)
 box('Ejector_Shoulder',(-11.4,95,64),(-10.5,96,66),'steel',radius=0)
 box('Bolt_Lock',(-6.9,160.5,74), (6.9,176.5,77.8),'steel','BoltLock',radius=.18)
 # Stamped carrier: concave bed and real turned-up sides, not a flat floating plate.
 inner=[(x,29-math.sqrt(11.2**2-x*x)) for x in (-10.4,-9.7,-7,-4,0,4,7,9.7,10.4)]
 section=inner+[(x,z-.9) for x,z in reversed(inner)]
 carrier=M.loft('Carrier_Tray',[[(x,y,z) for x,z in section] for y in (54,55,137,138)],MAT['steel'])
 cutbox(carrier,(-2.7,70,14),(2.7,126,24));reg(carrier,'Carrier',radius=.3)
 for side in (-1,1):
  x0,x1=sorted((side*10,side*11.8))
  ob=profile('Carrier_Arm',M.fillet_polygon([(29,19),(56,19),(60,24),(32,23)],1,4),x0,x1,'steel','Carrier',register=False)
  cut(ob,lathe('tool',[(-14,0),(-14,2.8),(14,2.8),(14,0)],axis='X',center=(30,20),n=24,register=False));reg(ob,'Carrier',radius=.2)
 lathe('Carrier_Pivot',[(-13.5,0),(-13.5,2.7),(13.5,2.7),(13.5,0)],'dark',axis='X',center=(30,20),n=24)
 # Retaining tips bear on the rim's rear face, below its upper quadrant.
 for side,bone in [(-1,'ShellStopL'),(1,'ShellStopR')]:
  x0,x1=sorted((side*11.2,side*13.1))
  end=203.3 if side>0 else 199.9
  profile('ShellStop_Arm_'+bone,[(170,24),(end,24),(end,34),(end-7.9,34),(170,29)],x0,x1,'dark',bone,radius=.2)
  x0,x1=sorted((side*(10.3 if side>0 else 9.3),side*(11.8 if side>0 else 11.2)))
  rear=203.4 if side>0 else 200
  box('ShellStop_Tip_'+bone,(x0,rear-1.2,26.5),(x1,rear,31.5),'steel',bone,radius=.08)
 y=200+4*PITCH
 lathe('Magazine_Follower',[(y,0),(y,10.9),(y+7,10.9),(y+7,0)],'follower','Follower',center=(0,TUBE),n=24)
 for i in range(4):shell('TubeShell'+str(i+1),(0,200+i*PITCH,TUBE),'Tube'+str(i+1),n=16,hidden=True)
 shell('ChamberShell',(0,BREECH,BORE),'ChamberShell',n=16)
 shell('CarrierShell',(0,104,29),'CarrierShell',n=16)
 shell('InsertShell',(0,130,29),'InsertShell',n=16)
 shell('FiredHull',(0,BREECH,BORE),'FiredHull',fired=True,n=28)

def bridge(a,b):
 """Join different ring counts without spending hidden subdivision rings."""
 if len(a)==1:return [(a[0],b[(j+1)%len(b)],b[j]) for j in range(len(b))]
 if len(b)==1:return [(a[i],a[(i+1)%len(a)],b[0]) for i in range(len(a))]
 faces=[];i=j=0;n,m=len(a),len(b)
 while i<n or j<m:
  an=(i+1)/n;bn=(j+1)/m
  if abs(an-bn)<1e-9:
   faces.append((a[i%n],b[j%m],b[(j+1)%m],a[(i+1)%n]));i+=1;j+=1
  elif an<bn:faces.append((a[i%n],b[j%m],a[(i+1)%n]));i+=1
  else:faces.append((a[i%n],b[j%m],b[(j+1)%m]));j+=1
 return faces
def shell_surface(name,specs,base,mat,bone,warp=None,cap_last=False):
 x,y,z=base;vertices=[];rings=[]
 for k,(a,r,n) in enumerate(specs):
  ring=[]
  for i in range(n if r else 1):
   t=i*math.tau/n;offset=warp(k,t) if warp else 0
   ring.append(len(vertices));vertices.append((x+r*math.cos(t),y+a+offset,z+r*math.sin(t)))
  rings.append(ring)
 faces=[f for a,b in zip(rings,rings[1:]) for f in bridge(a,b)]
 if cap_last:faces.append(tuple(reversed(rings[-1])))
 ob=reg(M.mesh(name,vertices,faces,MAT[mat]),bone);ob['shell_surface']=True;ob['shell_axis']=(x,z)
 return ob
def shell(name,base,bone='Root',fired=False,n=32,hidden=False):
 # Exterior gets 28/32 sides. Sparse primer/inner rings and absent hidden
 # backing disks pay for them; the rim still has its actual turned step.
 n=28 if fired else n;pn=12 if fired else (8 if hidden else 16)
 shell_surface(name+'_Head',[(0,2.7,pn),(0,11.2,n),(1.4,11.2,n),(1.8,10.1,n),(10.5,10.1,n)],base,'brass',bone)
 primer=[(.12,0,pn),(.12,2.7,pn),(0,2.7,pn)]
 if fired:primer=[(.75,0,pn),(.15,.65,pn),(.12,2.7,pn)]
 shell_surface(name+'_Primer',primer,base,'primer',bone)
 if fired:
  # Spend the mouth's budget on both visible lips; only the deep base is coarse.
  ob=shell_surface(name+'_Hull',[(10.5,10.05,n),(69.8,10.12,n),(69.8,9.55,n),(10.5,9.35,6)],base,'hull',bone,
   lambda k,t: -.18*(.5+.5*math.cos(6*t)) if k in (1,2) else 0,cap_last=True)
  ob.data.materials.append(MAT['mouth'])
  for f in ob.data.polygons:
   if f.center.y>base[1]+68:f.material_index=1
 else:
  shell_surface(name+'_Hull',[(10.5,10.05,n),(57.5,9.8,n),(57.5,9.3,n)],base,'hull',bone)
  # Six folds sink toward a small genuine center opening. Smooth compound
  # petals replace the old triangles meeting at a single flat center vertex.
  cn=12 if hidden else 24
  ob=shell_surface(name+'_Crimp',[(57.25,9.3,cn),(56.95,7.3,cn),(56.35,4.8,cn),(55.7,.65,cn),(55.1,.6,8 if hidden else 16)],base,'hull',bone,
   lambda k,t: .35*math.cos(6*t) if k==1 else .6*math.cos(6*t) if k==2 else .14*math.cos(6*t) if k==3 else 0)
  ob['fold_surface']=True;M.smooth(ob,85)

def finalize(ob):
 # Repair degenerate Boolean edges before explicit final triangulation.
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001)
 bmesh.ops.dissolve_degenerate(bm,dist=.0001,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 tri=ob.modifiers.new('Explicit game triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(ob)
 normals=[n.vector.copy() for n in ob.data.corner_normals]
 for f in ob.data.polygons:
  if ob.name=='Receiver':
   for j in f.loop_indices:normals[j]=f.normal.copy()
  for j in f.loop_indices:
   if normals[j].dot(f.normal)<.03:normals[j]=f.normal.copy()
   # Booleans and reduction must not bend an optically flat machined side.
   if ob.name=='Receiver' and abs(f.normal.x)>.995:
    for j in f.loop_indices:normals[j]=Vector((math.copysign(1,f.normal.x),0,0))
  if ob.name=='Receiver' and abs(f.normal.y)<.92:
   for j in f.loop_indices:
    p=ob.data.vertices[ob.data.loops[j].vertex_index].co
    (aa,_,top),(da,_,dt)=receiver_shape(p.y);hh=14.75;spring=top-hh
    q=(p.x/aa)**2+((p.z-spring)/hh)**2
    # Clamped Boolean bevels can put a shared roof corner just outside the
    # ideal ellipse. Keep its radial shading continuous across the triangle
    # fan; inward port walls still fail the outward normal test below.
    if p.z>=spring-.05 and .90<q<1.13:
     ny=-(p.x*p.x*da/aa**3+(p.z-spring)*dt/hh**2)
     n=Vector((p.x/aa**2,ny,(p.z-spring)/hh**2)).normalized()
     if n.dot(f.normal)>.3:normals[j]=n
  if ob.name=='Bead':
   for j in f.loop_indices:
    p=ob.data.vertices[ob.data.loops[j].vertex_index].co
    normals[j]=(p-Vector((0,645,80.6))).normalized()
  if ob.get('shell_surface') and not ob.get('fold_surface'):
   x,z=ob['shell_axis']
   if abs(f.normal.y)<.12:
    for j in f.loop_indices:
     p=ob.data.vertices[ob.data.loops[j].vertex_index].co
     n=Vector((p.x-x,0,p.z-z)).normalized()
     normals[j]=n if n.dot(f.normal)>0 else -n
   elif abs(f.normal.y)>.995:
    for j in f.loop_indices:normals[j]=Vector((0,math.copysign(1,f.normal.y),0))
 ob.data.transform(Matrix.Scale(.001,4)@Matrix.Translation(-GRIP));ob.matrix_world=Matrix.Identity(4)
 # Encode custom normals in the final meter-space loop bases. Encoding first
 # and then changing float precision can flip skinny Boolean-face corners.
 ob.data.update();ob.data.normals_split_custom_set(normals)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/shotgun.blend');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);materials()
 receiver();barrel_tube();furniture();controls();mechanism()
 for ob in PARTS:finalize(ob)
 highcollection=bpy.data.collections.new('High_Sources');bpy.context.scene.collection.children.link(highcollection)
 for h in HIGH:
  h.data.transform(Matrix.Scale(.001,4)@Matrix.Translation(-GRIP))
  for c in list(h.users_collection):c.objects.unlink(h)
  highcollection.objects.link(h);h.hide_render=True;h.hide_set(True)
 parents={'BoltLock':'Bolt','CarrierShell':'CarrierGuide','FiredHull':'FiredGuide','InsertShell':'ShellGuide',**{'Tube'+str(i):'TubeFeedGuide' for i in range(1,5)}}
 arm=W.armature('ShotgunArmature',{k:P(v) for k,v in HEADS.items()},parents=parents)
 for o in PARTS:W.rigid_bind(o,arm,o['bone'])
 sockets=W.sockets(arm,{k:P(v) for k,v in SOCKETS.items()},
  {'Socket_Magazine':'Magazine','Socket_SupportHand':'Forend','Socket_Shell':'ShellGuide'})
 build_clips(arm);W.pose(arm,'Idle',0)
 scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
 scene['stage']='Form checkpoint, constant inspection materials, no look-dev or baked delivery'
 scene['maker']='Propane Defense';scene['model']='Hearth 12';scene['interface_version']='1.1.0'
 scene['generator_sha256']=GENERATOR_HASH
 bpy.ops.wm.save_as_mainfile(filepath=str(out))
 # Separate checkpoint meshes preserve independent named surface tests after
 # import. Final atlas export will consolidate; these are temporary draw calls.
 from guns.common.feed_sampling import export as feed_export
 feed_export(out.with_suffix('.glb'),[arm]+PARTS+sockets,BONES)
 counts={o.name:len(o.data.polygons) for o in PARTS}
 report={'total':sum(counts.values()),'parts':counts,'high_sources':{h.name:sum(len(f.vertices)-2 for f in h.data.polygons) for h in HIGH},'standalones':{}}
 old=list(PARTS)
 for name,fired,n in [('shell',False,32),('hull',True,28)]:
  start=len(PARTS);shell(name,(0,0,0),'Root',fired,n);parts=PARTS[start:]
  # Standalone origin is the center of its head, +Y toward the mouth.
  for o in parts:
   finalize(o);o.data.transform(Matrix.Translation(GRIP*.001))
  joined=W.joined_copy(parts,'LoadedShell' if not fired else 'FiredHull');joined.parent=None
  W.export(out.parent/(name+'.glb'),[joined],animations=False)
  report['standalones'][name]=sum(len(f.vertices) for f in joined.data.polygons)//3
  bpy.data.objects.remove(joined,do_unlink=True)
  for o in parts:bpy.data.objects.remove(o,do_unlink=True)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2))
 print('SHOTGUN TRIANGLES',report['total'],'STANDALONES',report['standalones'],flush=True)
if __name__=='__main__':main()
