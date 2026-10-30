"""Original exterior visual meshes, in millimeters. Not fabrication geometry.

Surfaces are artistic envelopes. Hidden firing, locking and sear geometry is
absent. Molded furniture retains subdivision sources for a later normal bake.
"""
import math
import bpy,bmesh
from mathutils import Matrix,Vector
from kit import model as M
PARTS=[];HIGH=[];MAT={}
BORE=105.;SIGHT=176.;MUZZLE=710.

def palette():
 for k,c,metal,rough in [('paint',(.006,.006,.006),0,.43),('phosphate',(.026,.026,.025),.65,.55),
  ('steel',(.16,.16,.15),.9,.4),('polymer',(.012,.012,.011),0,.58),
  ('rubber',(.006,.006,.006),0,.78),('brass',(.42,.27,.085),.9,.34),
  ('copper',(.39,.15,.065),.9,.34),('marks',(.38,.39,.36),0,.65)]:
  m=bpy.data.materials.new('Inspection_'+k);m.use_nodes=True;m.diffuse_color=(*c,1)
  p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1)
  p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
  p.inputs['Specular IOR Level'].default_value=.3;MAT[k]=m

def freeze(o):
 M.apply(o);bpy.context.view_layer.update();o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4);return o

def reg(o,bone='Root',r=0,segments=2):
 freeze(o)
 if r:
  M.bevel(o,r,segments);m=o.modifiers.new('Manufactured planes','WEIGHTED_NORMAL');m.keep_sharp=True
 M.smooth(o,48);M.apply(o);o['bone']=bone;o['asset_set']='LMG';o['part_name']=o.name;PARTS.append(o);return o

def box(n,a,b,mat='paint',bone='Root',r=.4,raw=False):
 a,b=Vector(a),Vector(b);o=M.box(n,(a+b)/2,b-a,MAT[mat],0);freeze(o)
 return o if raw else reg(o,bone,r)

def lathe(n,p,mat='phosphate',bone='Root',axis='Y',center=(0,0),nseg=32,closed=False,raw=False,**kw):
 o=M.lathe(n,p,MAT[mat],segments=kw.get('n',nseg),axis=axis,center=center,closed=closed)
 return o if raw else reg(o,bone)

def profile(n,p,lo,hi,mat='paint',bone='Root',axis='X',r=.4,raw=False):
 o=M.profile(n,p,lo,hi,MAT[mat],axis=axis);return o if raw else reg(o,bone,r)

def cut(o,t):
 t.data.materials.clear();t.data.materials.append(o.data.materials[0]);M.boolean(o,t);return o

def cutbox(o,a,b,r=1):
 t=box('tool',a,b,raw=True)
 if r:M.bevel(t,r,3);freeze(t)
 return cut(o,t)

def tube(n,path,r,mat='phosphate',bone='Root',sides=12):return reg(M.tube(n,path,r,MAT[mat],sides=sides),bone)

def reduce(o,target):
 count=sum(len(f.vertices)-2 for f in o.data.polygons)
 if count>target:
  d=o.modifiers.new('Silhouette allocation','DECIMATE');d.ratio=target/count;M.apply(o)
 return o

def sculpt(o,target,level=2,bone='Root'):
 s=o.modifiers.new('Supported compound molding cage','SUBSURF');s.levels=s.render_levels=level;M.apply(o)
 M.smooth(o,75);freeze(o)
 h=o.copy();h.data=o.data.copy();h.name='HIGH_'+o.name;h['low_target']=o.name;h['bake_only']=True
 bpy.context.collection.objects.link(h);HIGH.append(h);reduce(o,target)
 d=o.modifiers.new('Dense mold normals','DATA_TRANSFER');d.object=h;d.use_loop_data=True
 d.data_types_loops={'CUSTOM_NORMAL'};d.loop_mapping='POLYINTERP_NEAREST';M.apply(o)
 return reg(o,bone)

def pin(n,y,z,x=25,r=3,bone='Root'):
 for s in (-1,1):
  a,b=sorted((s*(x-.3),s*(x+1.3)))
  lathe(n+('_L' if s<0 else '_R'),[(a,0),(a,r*.8),(a+.2,r),(b-.2,r),(b,r*.8),(b,0)],
   'phosphate',bone,axis='X',center=(y,z),nseg=16)

def receiver():
 # Finite folded U, two tight lower bends and broad sheet lands.
 section=[(-24,120),(-24,59),(-23.6,56),(-22.5,54),(-20,53),(20,53),(22.5,54),(23.6,56),(24,59),(24,120)]
 loops=[]
 for y in (-53,-52,-47,-25,0,30,60,90,120,150,180,210,236,240):
  loops.append([(x,y,z) for x,z in section])
 o=M.loft('Receiver_Sheet',loops,MAT['paint'],caps=False,closed=False)
 so=o.modifiers.new('Finite visual sheet wall','SOLIDIFY');so.thickness=1.4;so.offset=-1;so.use_even_offset=True;M.apply(o)
 cutbox(o,(21,110,76),(28,185,106),r=2.4)
 cutbox(o,(-13,125,49),(14,186,58),r=2)
 cutbox(o,(-4,39,49),(4,55,57),r=1)
 cutbox(o,(-30,132,115),(30,208,124),r=.5)
 cut(o,lathe('Safety visual clearance',[(-30,0),(-30,4.6),(30,4.6),(30,0)],axis='X',center=(0,52),raw=True))
 reg(o,r=.25,segments=2)
 # Pressed side rails, seam returns and rivet heads are exterior construction.
 for s in (-1,1):
  for z in (66,94):
   section=[(s*24.0,z-3),(s*26,z-1),(s*26,z+1),(s*24,z+3)]
   if s<0:section.reverse()
   rail=M.loft('Receiver_PressedRail_'+str(s)+'_'+str(z),[[(x,y,zz) for x,zz in section] for y in (-43,-40,105)],MAT['paint'],caps=False,closed=False)
   so=rail.modifiers.new('Sheet emboss return','SOLIDIFY');so.thickness=.6;M.apply(rail);reg(rail)
  for i,(y,z) in enumerate([(-43,62),(-43,111),(-20,59),(12,59),(202,61),(226,61),(215,113),(232,109),(87,72),(87,111)]):
   a,b=sorted((s*24,s*26.2));lathe(f'Receiver_Rivet_{s}_{i}',[(a,0),(a,3.1),((a+b)/2,3.3),(b,2.7),(b,0)],axis='X',center=(y,z),nseg=12)
  box('Receiver_InnerGuide_'+str(s),(s*17-1,-44,82),(s*17+1,213,85),'steel',r=.15)
 # End caps seat on sheet; no internal locking pockets or chamber.
 box('Receiver_RearCap',(-23,-56,54),(23,-50,121),'phosphate',r=1)
 cap=box('Receiver_FrontCollar',(-23,215,55),(23,241,121),'phosphate',raw=True)
 cut(cap,lathe('Visual barrel passage',[(210,0),(210,17),(247,17),(247,0)],center=(0,105),raw=True));reg(cap,r=.8)
 guide=box('ChargingGuide', (25,-42,70),(31,221,77),'phosphate',r=.8)
 cutbox(guide,(27,-45,71.5),(34,224,80),r=0)
 # Broad pressed handle, with a finger opening, rather than a ball on a wire.
 handle=profile('ChargingHandle_Paddle',M.fillet_polygon([(172,75),(201,75),(206,80),(205,90),(196,94),(175,87)],2.3,5),28,51,'phosphate','ChargingHandle',r=0,raw=True)
 cutbox(handle,(37,177,78),(55,199,87),r=2.5);reg(handle,'ChargingHandle',r=.7)
 box('ChargingHandle_Shoe',(27.5,182,72),(30.5,205,75),'steel','ChargingHandle',r=.8)
 # Side well is an exterior closed dust flap, deliberately inactive.
 well=profile('SideWell_Housing',M.fillet_polygon([(130,64),(180,64),(180,99),(137,99)],3,4),-47,-24,'paint',raw=True)
 cutbox(well,(-49,138,70),(-26,175,94),r=1);reg(well,r=.5)
 profile('SideWell_DustCover',M.fillet_polygon([(136,69),(177,69),(177,95),(136,95)],2.5,4),-48,-46,'phosphate',r=.2)
 lathe('SideWell_Hinge',[(134,0),(134,2.5),(178,2.5),(178,0)],axis='Y',center=(-48,97),nseg=16)
 box('LinkPort_Rim',(24,188,106),(28,215,119),'phosphate',r=.5)
 cutbox(PARTS[-1],(23,191,108),(30,212,117),r=.8)


def feed():
 # One low cover shell, with a pressed crown and underside visible when open.
 loops=[]
 for y,w,top in [(-56,25,136),(-55,28,140),(-50,30,144),(-43,30,145),(205,30,145),(228,29,141),(237,27,134),(238,25,132)]:
  sec=[(-w,124),(-w,top-7),(-w+2,top-2),(-w+7,top),(w-7,top),(w-2,top-2),(w,top-7),(w,124)]
  loops.append([(x,y,z) for x,z in sec])
 cover=M.loft('FeedCover_Shell',loops,MAT['paint'],caps=False,closed=False)
 so=cover.modifiers.new('Cover wall','SOLIDIFY');so.thickness=1.7;so.offset=-1;so.use_even_offset=True;M.apply(cover)
 cut(cover,lathe('Cover hinge clearway',[(-40,0),(-40,3.6),(40,3.6),(40,0)],axis='X',center=(236,127),raw=True))
 for x in (-32,26):cutbox(cover,(x,-52,123),(x+6,-30,146),r=.7)
 cutbox(cover,(-34,140,121),(-22,205,134),r=1)
 reg(cover,'FeedCover',r=.35)
 for x in (-17,17):
  profile('FeedCover_PressedBead_'+str(x),M.rounded_rectangle(3.2,212,1.2,4),143.8,146,'paint','FeedCover',axis='Z',r=.2)
  o=PARTS[-1];o.data.transform(Matrix.Translation((x,78,0)))
 lathe('FeedCover_HingePin',[(-34,0),(-34,3.4),(34,3.4),(34,0)],axis='X',center=(236,127),nseg=24)
 for x in (-28,28):
  lathe('FeedCover_HingeSleeve_'+str(x),[(x-4,3.6),(x-4,6.5),(x+4,6.5),(x+4,3.6)],'phosphate','FeedCover',axis='X',center=(236,127),nseg=24,closed=True)
 # Latch and tray are visual seats with no operative locking cam.
 box('CoverLatch_Seat',(-15,-53,121),(15,-48,126),'phosphate',r=.4)
 box('CoverLatch_Tongue',(-13,-53,125.9),(13,-47,129),'phosphate','CoverLatch',r=.4)
 for x in (-31,27):box('CoverLatch_Tab_'+str(x),(x,-51,125),(x+4,-32,137),'phosphate','CoverLatch',r=1)
 tray=box('FeedTray_Pan',(-31,134,115.5),(23,205,118),'phosphate','FeedTray',raw=True)
 cutbox(tray,(-6,147,114),(16,196,121),r=2);reg(tray,'FeedTray',r=.45)
 for y in (136,199):box('FeedTray_Guide_'+str(y),(-46,y,118),(23,y+3,121.5 if y==199 else 124),'steel','FeedTray',r=.4)
 box('FeedTray_RoundSeat',(-30,148,118),(23,150,119.3),'phosphate','FeedTray',r=.15)
 box('FeedTray_VisualStop',(4.8,145,119),(8,147.4,126),'phosphate','FeedTray',r=.4)
 for y in (149,182):
  profile('FeedPawl_Display_'+str(y),M.fillet_polygon([(-24,135),(-22,138),(-8,138),(-10,135),(-12.8,128.75 if y==149 else 127.25)],1,3),y,y+4,'steel','FeedPawls',axis='Y',r=.35)
 lathe('FeedPawls_Axle',[(150,0),(150,2.2),(195,2.2),(195,0)],'phosphate','FeedPawls',center=(-22,136),nseg=16)
 # Display-only interior owners. No bolt lugs, sear, firing pin, chamber or gas port.
 box('Bolt_Display',(-12,136,89),(12,183,100),'steel','Bolt',r=2)
 lathe('OperatingRod_Display',[(98,0),(98,4),(207,4),(207,0)],'phosphate','OperatingRod',center=(0,70),nseg=20)


def sights_barrel():
 lathe('Barrel_Exterior',[(205,0),(205,16.4),(225,16.4),(232,12),(248,11),(510,10),(529,10),(544,8.6),(666,7.6),(670,7.6),(670,4),(661,4),(661,0)],center=(0,BORE),nseg=48)
 for name,a,b,r in [('BarrelSeat',236,248,17),('BarrelCollar',521,546,15)]:
  lathe(name,[(a,10.05),(a,r),(a+1,r+.5),(b-1,r+.5),(b,r),(b,10.05)],center=(0,BORE),nseg=40,closed=True)
 lathe('GasTube',[(236,0),(236,11),(510,11),(516,13),(534,13),(534,0)],center=(0,68),nseg=40)
 # Continuous rounded diagonal web joins the collars, rather than two blocks.
 neck=profile('GasBlock_Web',M.fillet_polygon([(523,57),(545,58),(549,111),(537,120),(525,114)],3,6),-12,12,'phosphate',r=1.2)
 lathe('GasRegulator',[(536,0),(536,10),(549,10),(552,8),(556,8),(557,0)],center=(0,68),nseg=32)
 for i in range(6):
  t=math.tau*i/6;tube('Regulator_Grip_'+str(i),[(9*math.cos(t),546,68+9*math.sin(t)),(9*math.cos(t),551,68+9*math.sin(t))],1.2,sides=6)
 flash=lathe('FlashHider',[(669,7),(669,10),(677,10),(684,10.8),(703,12),(709,13),(710,12.5),(710,9),(704,8.5),(677,7)],center=(0,BORE),nseg=48,closed=True,raw=True)
 for i in range(5):
  t=math.tau*i/5;tool=box('slot',(-2.1,684,111),(2.1,703,122),raw=True)
  tool.data.transform(Matrix.Translation((0,0,BORE))@Matrix.Rotation(t,4,'Y')@Matrix.Translation((0,0,-BORE)))
  cut(flash,tool)
 reg(flash)
 # Rear aperture on rounded ears and a flat adjustable base.
 box('RearSight_Base',(-20,-38,143),(20,-3,150),'phosphate','FeedCover',r=1.4)
 for s in (-1,1):
  ear=profile('RearSight_Ear_'+str(s),M.fillet_polygon([(-36,149),(-35,169),(-28,179),(-13,179),(-5,167),(-5,149)],3,6),s*15-2,s*15+2,'phosphate','FeedCover',r=.7)
 lathe('RearSight_Aperture', [(-22.5,5),(-22.5,10),(-19.5,10),(-19.5,5)],'phosphate','FeedCover',center=(0,SIGHT),nseg=48,closed=True)
 lathe('RearSight_Windage',[(-26,0),(-26,6.2),(-20,6.2),(20,6.2),(26,6.2),(26,0)],'phosphate','FeedCover',axis='X',center=(-21,157),nseg=24)
 for s in (-1,1):
  lathe('RearSight_Dial_'+str(s),[(s*26-2,0),(s*26-2,8),(s*26+2,8),(s*26+2,0)],'phosphate','FeedCover',axis='X',center=(-21,157),nseg=32)
 # A windowed tower with a finite ring and a centered post.
 tower=profile('FrontSight_Tower',M.fillet_polygon([(-10,117),(-8,153),(-5,168),(5,168),(8,153),(10,117)],2,5),529,543,'phosphate',axis='Y',r=0,raw=True)
 cutbox(tower,(-3.5,527,130),(3.5,545,145),r=1.5);reg(tower,r=.5)
 lathe('FrontSight_Hood',[(531,9),(531,11),(542,11),(542,9)],center=(0,SIGHT),nseg=48,closed=True)
 box('FrontSight_Post',(-.8,536,165),(.8,538,176),'phosphate',r=.2)
 # Folded carrying handle sits outboard of the sight ray. Rotation is about +Y.
 lathe('CarryHandle_Sleeve',[(249,11.1),(249,15.5),(265,15.5),(265,11.1)],center=(0,BORE),nseg=32,closed=True,bone='CarryHandle')
 tube('CarryHandle_Arm',[(0,255,121),(17,255,126),(36,255,139),(44,255,145),(44,247,149),(44,164,149)],4.2,'phosphate','CarryHandle',sides=16)
 grip=lathe('CarryHandle_Grip',[(154,0),(154,8),(157,10),(165,9),(171,8.4),(178,9.2),(190,9.2),(197,8.4),(204,9.2),(218,9.2),(225,8.4),(232,9.2),(245,9.5),(250,8),(250,0)],'polymer','CarryHandle',center=(44,149),nseg=32)
 # Exterior quick-change latch, broad stamped thumb pad.
 latch=profile('BarrelLatch',M.fillet_polygon([(225,121),(246,121),(252,130),(244,136),(226,131)],2,4),-45,-38,'phosphate','BarrelLatch',r=.5)
 cut(latch,lathe('Latch pivot bore',[(-48,0),(-48,3.2),(-35,3.2),(-35,0)],axis='X',center=(235,124),raw=True))
 lathe('BarrelLatch_Pin_L',[(-44,0),(-44,3),(-38,3),(-38,0)],axis='X',center=(235,124),nseg=16)


def furniture():
 # Changing superellipse loops give changing width, depth and curved straps.
 loops=[]
 for z,y,w,d in [(-71,-28,34,43),(-70,-28,38,47),(-66,-27,38,47),(-53,-23,35,43),(-35,-17,36,41),(-10,-9,35,39),(16,-1,32,38),(36,4,30,37),(43,5,29,35),(45,5,27,33)]:
  ring=[]
  for j in range(24):
   t=math.tau*j/24;c,s=math.cos(t),math.sin(t)
   ring.append((w/2*math.copysign(abs(c)**.72,c),y+d/2*math.copysign(abs(s)**.78,s),z))
  loops.append(ring)
 sculpt(M.loft('PistolGrip_Sculpt',loops,MAT['polymer']),2400,2)
 # Shallow molded horizontal finger ribs taper naturally around the front strap.
 for z in (-57,-49,-41,-33,-25,-17):
  y=-9+(z+10)*.30
  path=[(-15,y+16,z),(-10,y+20,z+.4),(0,y+21,z+.6),(10,y+20,z+.4),(15,y+16,z)]
  tube('Grip_MoldRib_'+str(z),path,.75,'polymer',sides=6)
 housing=box('TriggerHousing',(-21,-35,44),(21,91,54),'paint',r=1.2)
 cutbox(housing,(-4,39,40),(4,54,57),r=1)
 cut(housing,lathe('Safety recess',[(-30,0),(-30,4.6),(30,4.6),(30,0)],axis='X',center=(0,52),raw=True))
 pin('TriggerHousing_Pin',-26,49,x=22,r=3.5);pin('TriggerHousing_Pin',83,49,x=22,r=3.5)
 # Broad flat guard band follows a curved bow, not a round rod.
 path=M.bezier((11,46),(10,18),(14,10),(35,10),12)+M.bezier((35,10),(65,9),(79,15),(78,46),14)[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  a=Vector(path[max(0,i-1)]);b=Vector(path[min(len(path)-1,i+1)]);t=(b-a).normalized();n=Vector((-t.y,t.x))
  loops.append([(x,y+v*n.x,z+v*n.y) for x,v in M.rounded_rectangle(12,3.4,.7,3)])
 reg(M.loft('TriggerGuard_Band',loops,MAT['paint']),r=0)
 # Concave muzzle-facing front and toe curling +Y, broad radiused blade.
 path=M.bezier((47,48),(42,41),(39,28),(49,22),20)
 loops=[]
 for i,(y,z) in enumerate(path):
  # Broad blade with a round section edge and a finite, blunt toe.
  w=4.8-.8*(i/(len(path)-1))**4
  loops.append([(x,y+dy,z) for x,dy in M.rounded_rectangle(w,2.4,.65,3)])
 reg(M.loft('Trigger_Blade',loops,MAT['phosphate']),'Trigger')
 lathe('Safety_Button',[(-24,0),(-24,4.3),(-21,4.3),(21,4.3),(25,4.3),(25,0)],'phosphate','Safety',axis='X',center=(0,52),nseg=24)
 # Smooth stock cage with a flowing comb and deeper heel, no extruded side cutout.
 loops=[]
 for y,w,bot,top in [(-324,39,-15,109),(-323,42,-18,112),(-317,43,-19,113),(-300,44,-17,114),(-266,44,-12,116),(-231,42,-2,117),(-209,39,18,111),(-188,34,38,103),(-160,30,51,104),(-125,29,56,112),(-95,31,56,121),(-66,35,55,123),(-53,38,54,122),(-52,37,55,121)]:
  h=top-bot;mid=(top+bot)/2
  loops.append([(w/2*math.copysign(abs(math.cos(t))**.74,math.cos(t)),y,mid+h/2*math.copysign(abs(math.sin(t))**.82,math.sin(t))) for t in [math.tau*j/24 for j in range(24)]])
 sculpt(M.loft('Stock_Sculpt',loops,MAT['polymer']),3600,2)
 # Butt plate fits the changing section of the stock instead of floating.
 loops=[[(x,y,47+z) for x,z in M.rounded_rectangle(44,134,15,5)] for y in (-330,-329,-324)]
 reg(M.loft('Buttpad',loops,MAT['rubber']),r=.4)
 tube('ShoulderRest_Bow',[(-24.9,-321,109),(-24,-319,119),(-24,-270,124),(-19,-259,124),(19,-259,124),(24,-270,124),(24,-319,119),(24.9,-321,109)],2.6,'phosphate','ShoulderRest',sides=12)
 for s in (-1,1):
  lathe('ShoulderRest_Pivot_'+str(s),[(s*20-2,0),(s*20-2,4),(s*20+2,4),(s*20+2,0)],axis='X',center=(-321,109),nseg=16)
 # Sculpted U handguard, continuous outer and inner surfaces, open at its top.
 sections=[]
 for y,w,bot,top in [(244,60,42,102),(246,64,39,104),(252,66,38,104),(281,66,38,104),(350,64,39,104),(416,62,41,104),(453,60,47,103),(478,56,61,102),(486,53,64,101),(488,51,65,100)]:
  outer=[];inner=[]
  for j in range(21):
   t=math.pi+math.pi*j/20
   outer.append((w/2*math.cos(t),y,top+(top-bot)*math.sin(t)))
   inner.append(((w/2-3.3)*math.cos(t),y,top+(top-bot-3.3)*math.sin(t)))
  sections.append(outer+list(reversed(inner)))
 sculpt(M.loft('Handguard_Sculpt',sections,MAT['polymer']),2900,2)
 pin('Handguard_Pin',471,90,x=28,r=4)
 # Upper curved heat shield, finite wall, with actual vent openings.
 loops=[]
 for y in (270,271,276,457,465,466):
  loops.append([(24*math.cos(t),y,104+21*math.sin(t)) for t in [math.pi*j/20 for j in range(21)]])
 o=M.loft('HeatShield',loops,MAT['phosphate'],caps=False,closed=False)
 so=o.modifiers.new('Shield gauge','SOLIDIFY');so.thickness=1.0;M.apply(o)
 for y in (277,306,335,364,393,422):cutbox(o,(-13,y,115),(13,y+9,129),r=2)
 reg(o,r=.2)


def bipod():
 box('Bipod_Yoke',(-22,520,44),(22,542,55),'phosphate',r=2)
 lathe('Bipod_Axle',[(-29,0),(-29,4),(29,4),(29,0)],axis='X',center=(531,46),nseg=24)
 for s,label in [(-1,'L'),(1,'R')]:
  b='Bipod'+label;e='BipodExtend'+label;x=s*28
  lathe('Bipod_Hinge_'+label,[(x-4,4.2),(x-4,9),(x+4,9),(x+4,4.2)],bone=b,axis='X',center=(531,46),nseg=28,closed=True)
  # Folded rearward along the handguard, made from a real open channel section.
  sec=[(-6,0),(-6,-9),(-4.5,-9),(-4.5,-1.5),(4.5,-1.5),(4.5,-9),(6,-9),(6,0)]
  loops=[[(x+u,y,44+v) for u,v in sec] for y in (302,305,519,522)]
  reg(M.loft('Bipod_Channel_'+label,loops,MAT['phosphate']),'BipodSplay'+label,r=.45)
  # Telescoping display inner, with relief witnesses and a broad stamped foot.
  box('Bipod_Extension_'+label,(x-3.6,231,37),(x+3.6,384,42),'steel',e,r=.5)
  for y in (259,285,311,337):box('Bipod_DetentWitness_'+label+str(y),(x-2,y,41.8),(x+2,y+2.2,42.1),'paint',e,r=.15)
  profile('Bipod_Foot_'+label,M.fillet_polygon([(225,36),(244,36),(247,40),(242,43),(227,40)],1.2,4),x-13,x+13,'phosphate',e,r=.5)
  box('Bipod_Detent_'+label,(x-3,301,33.8),(x+3,309,36.8),'phosphate','BipodSplay'+label,r=.6)


def ammo_box():
 # Rounded finite-wall molded bin, actual open mouth and separate lid.
 loops=[]
 for z,w,d in [(-139,111,108),(-138,116,113),(-132,118,115),(-13,126,119),(-9,128,121)]:
  loops.append([(x,y+164,z) for x,y in M.rounded_rectangle(w,d,9,4)])
 o=M.loft('Box_Shell',loops,MAT['polymer'],caps=True)
 inner=[]
 for z,w,d in [(-134,108,105),(-12,119,112),(1,120,113)]:inner.append([(x,y+164,z) for x,y in M.rounded_rectangle(w,d,7,4)])
 cut(o,M.loft('Box cavity',inner,MAT['polymer']))
 cutbox(o,(-70,138,-25),(-43,207,2),r=2)
 reg(o,'Magazine',r=.8)
 # Lid seats on the perimeter with a belt exit on the left edge.
 lid=box('Box_Lid',(-65,102,-9),(65,226,-3),'polymer','BoxLid',raw=True)
 cutbox(lid,(-80,138,-12),(-29,207,2),r=3)
 cutbox(lid,(-22,137,-12),(22,193,2),r=2)
 cut(lid,lathe('Lid hinge clearway',[(98,0),(98,3.4),(230,3.4),(230,0)],center=(64,-7),raw=True))
 reg(lid,'BoxLid',r=1)
 lathe('Box_LidHinge',[(109,0),(109,3),(218,3),(218,0)],'phosphate','Magazine',center=(64,-7),nseg=16)
 for s in (-1,1):
  for y in (119,209):
   box('Box_MoldRib_'+str(s)+'_'+str(y),(s*57-1,y-2,-127),(s*57+1,y+2,-18),'polymer','Magazine',r=.8)
 box('Box_Suspension',(-16,141,40),(16,189,48),'polymer','Magazine',r=2)
 box('Box_LatchSeat',(-20,145,48),(20,185,52),'phosphate',r=.4)
 box('Box_Latch',(-13,145,52),(13,185,54),'phosphate','MagRelease',r=.6)
 for s in (-1,1):box('Box_LidCatch_'+str(s),(s*60-2,209,-19),(s*60+2,222,-9.3),'phosphate','Magazine',r=.8)
