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
 side=[(24,120),(24,98),(24.4,97),(26,95.5),(26,93.5),(24.4,92),(24,91),
       (24,70),(24.4,69),(26,67.5),(26,65.5),(24.4,64),(24,63),(24,59)]
 section=[(-x,z) for x,z in side]+[(-23.6,56),(-22.5,54),(-20,53),(20,53),(22.5,54),(23.6,56)]+list(reversed(side))
 loops=[]
 for y in (-53,-52,-47,-25,0,30,60,90,120,150,180,210,236,240):
  fade=max(0,min(1,(y+52)/9,(218-y)/12))
  loops.append([(math.copysign(24+(abs(x)-24)*fade,x) if abs(x)>24 else x,y,z) for x,z in section])
 o=M.loft('Receiver_Sheet',loops,MAT['paint'],caps=False,closed=False)
 so=o.modifiers.new('Finite visual sheet wall','SOLIDIFY');so.thickness=1.4;so.offset=-1;so.use_even_offset=True;M.apply(o)
 cutbox(o,(21,110,92),(28,185,106),r=2.4)
 cutbox(o,(20,-28,71.7),(30,209,79.3),r=1.8)
 cutbox(o,(-13,125,49),(14,186,58),r=2)
 cutbox(o,(-4,39,49),(4,55,57),r=1)
 cutbox(o,(-30,132,115),(30,208,124),r=.5)
 cut(o,lathe('Safety visual clearance',[(-30,0),(-30,4.6),(30,4.6),(30,0)],axis='X',center=(0,52),raw=True))
 reg(o,r=.25,segments=2)
 # Pressed side rails, seam returns and rivet heads are exterior construction.
 for s in (-1,1):
  # Embossing is in the finite sheet above, including its interior return.
  for i,(y,z) in enumerate([(-44,61),(-46,109),(-37,94),(-29,87),(-23,83),(-18,59),
                           (11,59),(35,60),(86,60),(89,111),(159,110),(204,61),(226,61),(229,111)]):
   a,b=sorted((s*24,s*26.2));lathe(f'Receiver_Rivet_{s}_{i}',[(a,0),(a,2.8),((a+b)/2,3.2),(b,2.6),(b,0)],axis='X',center=(y,z),nseg=12)
  box('Receiver_InnerGuide_'+str(s),(s*17-1,-44,82),(s*17+1,213,85),'steel',r=.15)
  # Rear reinforcement is a folded sheet doubler, with local pin bosses.
  p=[(-51,58),(-39,58),(-39,77),(-25,82),(-27,94),(-40,97),(-40,116),(-51,117)]
  a,b=sorted((s*24.1,s*25.3));profile('Receiver_RearDoubler_'+str(s),M.fillet_polygon(p,1.8,3),a,b,r=.2)
 for y in (89,159):
  p=[(y-17,106),(y-13,115),(y+6,118),(y+16,113),(y+15,106)]
  profile('Receiver_UpperPress_'+str(y),M.fillet_polygon(p,1,2),24.05,25.2,'paint',r=.15)
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
 box('SideWell_FlapRib',(-49,140,76),(-47.8,173,79),'phosphate',r=.5)
 profile('SideWell_ThumbTab',M.fillet_polygon([(161,67),(174,67),(179,72),(175,76),(162,73)],1,3),-51,-48,'phosphate',r=.3)
 box('LinkPort_Rim',(24,188,106),(28,215,119),'phosphate',r=.5)
 cutbox(PARTS[-1],(23,191,108),(30,212,117),r=.8)


def feed():
 # One low cover shell, with a pressed crown and underside visible when open.
 loops=[]
 for y,w,top in [(-56,25,136),(-55,28,140),(-50,30,144),(-43,30,145),(205,30,145),(228,29,141),(237,27,134),(238,25,132)]:
  sec=[(-w,120),(-w,top-7),(-w+2,top-2),(-w+7,top),(w-7,top),(w-2,top-2),(w,top-7),(w,120)]
  loops.append([(x,y,z) for x,z in sec])
 cover=M.loft('FeedCover_Shell',loops,MAT['paint'],caps=False,closed=False)
 so=cover.modifiers.new('Cover wall','SOLIDIFY');so.thickness=1.7;so.offset=-1;so.use_even_offset=True;M.apply(cover)
 cut(cover,lathe('Cover hinge clearway',[(-40,0),(-40,3.6),(40,3.6),(40,0)],axis='X',center=(236,127),raw=True))
 for x in (-32,26):cutbox(cover,(x,-52,123),(x+6,-30,146),r=.7)
 cutbox(cover,(-35,132,118.5),(-20,212,134.5),r=1)
 reg(cover,'FeedCover',r=.35)
 for x in (-17,17):
  profile('FeedCover_PressedBead_'+str(x),M.rounded_rectangle(3.2,212,1.2,4),143.8,146,'paint','FeedCover',axis='Z',r=.2)
  o=PARTS[-1];o.data.transform(Matrix.Translation((x,78,0)))
 lathe('FeedCover_HingePin',[(-34,0),(-34,3.4),(34,3.4),(34,0)],axis='X',center=(236,127),nseg=24)
 for x in (-28,28):
  lathe('FeedCover_HingeSleeve_'+str(x),[(x-4,3.6),(x-4,6.5),(x+4,6.5),(x+4,3.6)],'phosphate','FeedCover',axis='X',center=(236,127),nseg=24,closed=True)
 # Pressed flange returns, short side-wall doublers and underside fasteners.
 for s in (-1,1):
  box('FeedCover_Flange_'+str(s),(s*27-1,-28,124),(s*27+1,127,127),'paint','FeedCover',r=.3)
  p=[(-30,128),(-30,135),(35,139),(104,139),(115,134),(115,128)]
  a,b=sorted((s*29.3,s*30.7));profile('FeedCover_SidePress_'+str(s),M.fillet_polygon(p,1.5,3),a,b,'paint','FeedCover',r=.25)
  for y in (-18,69,116,217):
   lathe('FeedCover_Fastener_'+str(s)+'_'+str(y),[(s*29-.5,0),(s*29-.5,2.1),(s*29+1.5,2.1),(s*29+1.5,0)],'phosphate','FeedCover',axis='X',center=(y,132),nseg=12)
 # Display of the broad curved feed arm, with a rolled section. No operative cam.
 loops=[]
 for y,z in [(-23,138),(-21,138),(8,137.8),(79,137),(137,135),(177,132.8),(207,132),(209,132)]:
  loops.append([(x+7,y,z+dz) for x,dz in M.rounded_rectangle(12,2.4,.7,3)])
 reg(M.loft('FeedCover_UndersideArm',loops,MAT['steel']),'FeedCover')
 for y in (-17,104):
  lathe('FeedCover_ArmRivet_'+str(y),[(135.5,0),(135.5,3),(137.6,3),(137.6,0)],'phosphate','FeedCover',axis='Z',center=(7,y),nseg=16)
 carrier=box('FeedCover_PawlCarrier',(-24,135,130),(24,211,132.5),'phosphate',raw=True)
 for y in (146,179):cutbox(carrier,(-25,y,129),(-7,y+15,134),r=.8)
 reg(carrier,'FeedCover',r=.5)
 for x in (-22,22):
  box('FeedCover_CarrierReturn_'+str(x),(x-1,138,130.5),(x+1,208,132.5),'phosphate','FeedCover',r=.4)
 # Latch and tray are visual seats with no operative locking cam.
 box('CoverLatch_Seat',(-15,-53,121),(15,-48,126),'phosphate',r=.4)
 box('CoverLatch_Tongue',(-13,-53,125.9),(13,-47,129),'phosphate','CoverLatch',r=.4)
 for x in (-31,27):box('CoverLatch_Tab_'+str(x),(x,-51,125),(x+4,-32,137),'phosphate','CoverLatch',r=1)
 tray=box('FeedTray_Pan',(-43,134,115.7),(23,205,117.3),'phosphate','FeedTray',raw=True)
 cutbox(tray,(-5,160,114),(13,190,121),r=2);reg(tray,'FeedTray',r=.3)
 # Turned-down feed lip and the two formed guide walls grow from the pan.
 profile('FeedTray_FeedLip',M.fillet_polygon([(-46,115.3),(-43,117.3),(-35,117.3),(-35,115.7),(-42,115.7),(-45,113.7)],.6,3),138,197,'phosphate','FeedTray',axis='Y',r=.2)
 for y in (136,199):box('FeedTray_Guide_'+str(y),(-46,y,117.3),(23,y+3,121.5 if y==199 else 124),'steel','FeedTray',r=.4)
 box('FeedTray_RoundSeat',(-30,148,117.3),(23,150,119.3),'phosphate','FeedTray',r=.15)
 box('FeedTray_VisualStop',(4.8,145,119),(8,147.4,126),'phosphate','FeedTray',r=.4)
 for y in (149,182):
  profile('FeedPawl_Display_'+str(y),M.fillet_polygon([(-24,135),(-22,138),(-8,138),(-10,135),(-12.8,128.75 if y==149 else 127.25)],1,3),y,y+4,'steel','FeedPawls',axis='Y',r=.35)
 lathe('FeedPawls_Axle',[(150,0),(150,2.2),(195,2.2),(195,0)],'phosphate','FeedPawls',center=(-22,136),nseg=16)
 for y in (151,184):
  box('FeedPawl_BackPlate_'+str(y),(-21,y,131),(-10,y+7,133),'phosphate','FeedPawls',r=.5)
 # Display-only interior owners. No bolt lugs, sear, firing pin, chamber or gas port.
 box('Bolt_Display',(-12,136,89),(12,183,100),'steel','Bolt',r=2)
 # Two inert, rectangular animation witnesses provide a measurable ready seat.
 # They intentionally have none of a working sear's engagement/release geometry.
 box('Bolt_ReadyWitness',(-7,132,86),(7,138,90),'phosphate','Bolt',r=.1)
 box('Sear_VisualWitness',(-18,48,82),(18,52,90),'phosphate',r=.1)
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
 box('RearSight_Base',(-17,-39,143),(17,-3,149),'phosphate','FeedCover',r=1.1)
 for s in (-1,1):
  ear=profile('RearSight_Ear_'+str(s),M.fillet_polygon([(-38,149),(-38,166),(-27,176),(-9,181),(3,179),(7,168),(7,149)],4,6),s*15-.85,s*15+.85,'phosphate','FeedCover',r=0,raw=True)
  cut(ear,lathe('Sight ear window',[(-20,0),(-20,5.6),(20,5.6),(20,0)],axis='X',center=(-14,168),nseg=24,raw=True));reg(ear,'FeedCover',r=.3)
 lathe('RearSight_Aperture', [(-22.5,1.4),(-22.5,4.8),(-20.1,4.8),(-20.1,1.4)],'phosphate','FeedCover',center=(0,SIGHT),nseg=40,closed=True)
 profile('RearSight_Stem',M.fillet_polygon([(-3.5,163),(-3.2,173),(3.2,173),(3.5,163)],.8,3),-22.4,-20.2,'phosphate','FeedCover',axis='Y',r=.25)
 lathe('RearSight_Windage',[(-22,0),(-22,3),(-17,3),(17,3),(22,3),(22,0)],'phosphate','FeedCover',axis='X',center=(-21,159),nseg=20)
 for x in (-7,7):
  lathe('RearSight_ElevationDrum_'+str(x),[(x-3,0),(x-3,5.5),(x+3,5.5),(x+3,0)],'phosphate','FeedCover',axis='X',center=(-21,159),nseg=20)
 for s,y,z in [(-1,-30,159),(1,-5,170)]:
  lathe('RearSight_Dial_'+str(s),[(-24,0),(-24,6.3),(-19,6.3),(-19,0)],'phosphate','FeedCover',axis='X',center=(y,z),nseg=28)
 lathe('RearSight_ForwardAxle',[(-19,0),(-19,2.5),(14,2.5),(14,0)],'phosphate','FeedCover',axis='X',center=(-5,170),nseg=16)
 # A windowed tower with a finite ring and a centered post.
 tower=profile('FrontSight_Tower',M.fillet_polygon([(-10,117),(-8,153),(-5,168),(5,168),(8,153),(10,117)],2,5),529,543,'phosphate',axis='Y',r=0,raw=True)
 cutbox(tower,(-3.5,527,130),(3.5,545,145),r=1.5);reg(tower,r=.5)
 lathe('FrontSight_Hood',[(531,9),(531,11),(542,11),(542,9)],center=(0,SIGHT),nseg=48,closed=True)
 box('FrontSight_Post',(-.8,536,165),(.8,538,176),'phosphate',r=.2)
 # Folded carrying handle sits outboard of the sight ray. Rotation is about +Y.
 lathe('CarryHandle_Sleeve',[(249,11.1),(249,15.5),(265,15.5),(265,11.1)],center=(0,BORE),nseg=32,closed=True,bone='CarryHandle')
 tube('CarryHandle_Arm',[(0,255,121),(20,255,126),(53,255,138),(68,255,145),(68,247,149),(68,164,149)],4.2,'phosphate','CarryHandle',sides=16)
 grip=lathe('CarryHandle_Grip',[(154,0),(154,8),(157,10),(165,9),(171,8.4),(178,9.2),(190,9.2),(197,8.4),(204,9.2),(218,9.2),(225,8.4),(232,9.2),(245,9.5),(250,8),(250,0)],'polymer','CarryHandle',center=(68,149),nseg=32)
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
 # Deep fixed-polymer shell: changing rounded sections and a molded side recess.
 # This photographic version has no folding shoulder rest. Its bone is retained.
 stock=[(-324,39,-22,102),(-323,42,-24,105),(-318,44,-25,106),
  (-305,45,-25,106),(-283,45,-25,105),(-258,44,-25,101),(-239,43,-25,94),
  (-224,42,-24,91),(-216,41,-19,89),(-209,39,-12,88),(-198,36,18,88),
  (-180,33,34,91),(-153,31,41,100),(-124,31,39,111),(-96,33,40,119),
  (-69,36,48,122),(-54,38,53,122),(-52,37,54,121)]
 loops=[]
 for y,w,bot,top in stock:
  mid=(top+bot)/2;h=top-bot
  ring=[]
  for x,dz in M.rounded_rectangle(w,h,min(8,w/4,h/4),5):
   z=mid+dz
   # 1.6-mm side depression with 8-mm soft transitions, generated in the cage.
   mask=math.exp(-((y+273)/43)**8)*math.exp(-((z-35)/44)**8)
   x-=math.copysign(2.2*mask*min(1,abs(x)/(w*.4)),x)
   ring.append((x,y,z))
  loops.append(ring)
 # Inner shell follows the exterior at 3-mm nominal wall, closed at its neck.
 outer=list(loops)
 for ring in reversed(outer):
  y=ring[0][1]
  mid=(max(v[2] for v in ring)+min(v[2] for v in ring))/2
  loops.append([(x-math.copysign(min(3,abs(x)*.25),x),y,z-math.copysign(min(3,abs(z-mid)*.25),z-mid)) for x,y,z in ring])
 stock_ob=M.loft('Stock_Sculpt',loops,MAT['polymer'],caps=False)
 n=len(loops[0]);vs=[tuple(v.co) for v in stock_ob.data.vertices];fs=[tuple(f.vertices) for f in stock_ob.data.polygons]
 fs += [(j,(j+1)%n,(len(loops)-1)*n+(j+1)%n,(len(loops)-1)*n+j) for j in range(n)]
 bpy.data.objects.remove(stock_ob,do_unlink=True)
 sculpt(M.mesh('Stock_Sculpt',vs,fs,MAT['polymer']),3000,2)
 loops=[[(x,y,41+z) for x,z in M.rounded_rectangle(44,134,9,5)] for y in (-330,-329,-324)]
 reg(M.loft('Buttpad',loops,MAT['rubber']),r=.35)
 # A molded seam and butt fasteners remain readable without dense surface noise.
 for z in (-17,91):
  lathe('Buttpad_Screw_'+str(z),[(-329.95,0),(-329.95,2.1),(-329.6,2.1),(-329.6,0)],'phosphate',center=(0,z),nseg=12)
 # Flat-sided, flat-bottom U with a measured 5-mm outside corner radius.
 sections=[]
 def u_section(w,bot,top,r):
  p=[(-w/2,top),(-w/2,bot+r)]
  p += [(-w/2+r+r*math.cos(math.pi+math.pi*j/8),bot+r+r*math.sin(math.pi+math.pi*j/8)) for j in range(1,5)]
  p += [(w/2-r,bot)]
  p += [(w/2-r+r*math.cos(-math.pi/2+math.pi*j/8),bot+r+r*math.sin(-math.pi/2+math.pi*j/8)) for j in range(1,5)]
  p += [(w/2,top)]
  return p
 for y,w,bot,top in [(244,61,42,102),(245,64,40,104),(249,66,39,104),(254,66,39,104),
   (280,66,39,104),(350,65,39,104),(418,64,40,104),(455,63,41,104),
   (481,62,43,103),(486,62,43,103),(488,61,44,102)]:
  outer=u_section(w,bot,top,5);inner=u_section(w-6.4,bot+3.2,top,2)
  sections.append([(x,y,z) for x,z in outer+list(reversed(inner))])
 sculpt(M.loft('Handguard_Sculpt',sections,MAT['polymer']),2400,2)
 # Three longitudinal molded ribs at a 14-mm spacing; broad rectangular section.
 for side in (-1,1):
  for z in (52,66,80):
   loops=[]
   for y,x,up in [(254,32.5,0),(257,33.8,0),(420,32.5,0),(444,32.2,2),(460,31.8,10),(478,31.4,10),(482,30.7,10)]:
    loops.append([(side*(x+dx),y,z+up+dz) for dx,dz in M.rounded_rectangle(2.2,3.2,.7,3)])
   reg(M.loft('Handguard_MoldRib_'+str(side)+'_'+str(z),loops,MAT['polymer']))
 pin('Handguard_Pin',471,90,x=30,r=4)
 # Upper curved heat shield, finite wall, with actual vent openings.
 loops=[]
 for y in (270,271,276,457,465,466):
  loops.append([(24*math.cos(t),y,104+21*math.sin(t)) for t in [math.pi*j/20 for j in range(21)]])
 o=M.loft('HeatShield',loops,MAT['phosphate'],caps=False,closed=False)
 so=o.modifiers.new('Shield gauge','SOLIDIFY');so.thickness=1.0;M.apply(o)
 for y in (277,306,335,364,393,422):cutbox(o,(-13,y,115),(13,y+9,129),r=2)
 reg(o,r=.2)


def bipod():
 yoke=profile('Bipod_Yoke',M.fillet_polygon([(-27,45),(-27,57),(-16,64),(16,64),(27,57),(27,45),(17,45),(13,52),(-13,52),(-17,45)],1.7,4),522,540,'phosphate',axis='Y',r=.5)
 yoke.data.transform(Matrix.Diagonal((.77,1,1,1)))
 lathe('Bipod_Axle',[(-29,0),(-29,4),(29,4),(29,0)],axis='X',center=(531,46),nseg=24)
 for s,label in [(-1,'L'),(1,'R')]:
  b='Bipod'+label;e='BipodExtend'+label;x=s*28
  lathe('Bipod_Hinge_'+label,[(x-4,4.2),(x-4,9),(x+4,9),(x+4,4.2)],bone=b,axis='X',center=(531,46),nseg=28,closed=True)
  # Folded rearward along the handguard, made from a real open channel section.
  sec=[(-6,0),(-6,-9),(-4.5,-9),(-4.5,-1.5),(4.5,-1.5),(4.5,-9),(6,-9),(6,0)]
  loops=[[(x+u,y,z+v) for u,v in sec] for y,z in [(302,38),(305,38),(509,38),(517,40),(522,44)]]
  reg(M.loft('Bipod_Channel_'+label,loops,MAT['phosphate']),'BipodSplay'+label,r=.45)
  # Telescoping display inner, with relief witnesses and a broad stamped foot.
  box('Bipod_Extension_'+label,(x-3.6,276,31),(x+3.6,384,36),'steel',e,r=.5)
  for y in (259,285,311,337):box('Bipod_DetentWitness_'+label+str(y),(x-2,y,35.8),(x+2,y+2.2,36.1),'paint',e,r=.15)
  # Pad lies nearly horizontal in the deployed pose, rather than presenting
  # its broad face vertically. The fixed 18-degree shoe compensates leg splay.
  loops=[]
  for zz,yy in [(16.5,279),(19,277),(36,277),(38.5,279)]:
   loops.append([(x+u,yy+v,zz) for u,v in M.rounded_rectangle(36,1.6,.5,2)])
  foot=reg(M.loft('Bipod_Foot_'+label,loops,MAT['phosphate']),e)
  pivot=Vector((x,278,27.5))
  foot.data.transform(Matrix.Translation(pivot)@Matrix.Rotation(math.radians(-s*18),4,'Z')@Matrix.Translation(-pivot))
  box('Bipod_Detent_'+label,(x-3,301,27.8),(x+3,309,30.8),'phosphate','BipodSplay'+label,r=.6)


def ammo_box():
 # Rounded finite-wall molded bin, actual open mouth and separate lid.
 loops=[]
 for z,w,d in [(-139,111,108),(-138,116,113),(-132,118,115),(-13,126,119),(-9,128,121)]:
  loops.append([(x,y+164,z) for x,y in M.rounded_rectangle(w,d,14,5)])
 o=M.loft('Box_Shell',loops,MAT['polymer'],caps=True)
 inner=[]
 for z,w,d in [(-134,108,105),(-12,119,112),(1,120,113)]:inner.append([(x,y+164,z) for x,y in M.rounded_rectangle(w,d,7,4)])
 cut(o,M.loft('Box cavity',inner,MAT['polymer']))
 cutbox(o,(-70,138,-25),(-43,207,2),r=2)
 reg(o,'Magazine',r=.8)
 # Lid seats on the perimeter with a belt exit on the left edge.
 lid=M.loft('Box_Lid',[[(x,y+164,z) for x,y in M.rounded_rectangle(w,d,12,5)] for z,w,d in [(-9,128,122),(-8,130,124),(-4,130,124),(-3,128,122)]],MAT['polymer'])
 cutbox(lid,(-80,138,-12),(-29,207,2),r=3)
 cut(lid,lathe('Lid hinge clearway',[(98,0),(98,3.4),(230,3.4),(230,0)],center=(64,-7),raw=True))
 reg(lid,'BoxLid',r=1)
 lathe('Box_LidHinge',[(109,0),(109,3),(218,3),(218,0)],'phosphate','Magazine',center=(64,-7),nseg=16)
 for s in (-1,1):
  for y in (119,209):
   box('Box_MoldRib_'+str(s)+'_'+str(y),(s*57-1,y-2,-127),(s*57+1,y+2,-18),'polymer','Magazine',r=.8)
  for z in (-110,-79,-48):
   loops=[]
   for y,x in [(118,57),(121,60),(205,61),(211,57)]:
    loops.append([(s*(x+dx),y,z+dz) for dx,dz in M.rounded_rectangle(2.3,3.4,.8,3)])
   reg(M.loft('Box_EndRib_'+str(s)+'_'+str(z),loops,MAT['polymer']),'Magazine')
 # Exterior spring clip, backing ribs and a hinged-lid catch on the near end.
 profile('Box_AttachmentClip',M.fillet_polygon([(112,-85),(126,-85),(130,-77),(130,-28),(127,-22),(112,-22)],2,4),-64,-61,'phosphate','Magazine',r=.5)
 for y in (108,132):
  box('Box_ClipBacking_'+str(y),(-64,y,-92),(-60,y+2,-25),'polymer','Magazine',r=.7)
 profile('Box_LidCatch',M.fillet_polygon([(111,-23),(111,-8),(121,-8),(121,-14),(117,-14),(117,-23)],1.1,3),-67,-64,'phosphate','BoxLid',r=.3)
 box('Box_Suspension',(-16,141,40),(16,189,48),'polymer','BoxLid',r=2)
 box('Box_LatchSeat',(-20,145,48),(20,185,52),'phosphate',r=.4)
 box('Box_Latch',(-13,145,52),(13,185,54),'phosphate','MagRelease',r=.6)
 for s in (-1,1):box('Box_LidCatch_'+str(s),(s*60-2,209,-19),(s*60+2,222,-9.3),'phosphate','Magazine',r=.8)

 # The photo's narrow end and tall broad flank require a shallower, taller bin.
 # Keep the accepted mouth/world belt path and lid hinge height unchanged.
 for ob in PARTS:
  if not ob.name.startswith('Box_') or ob.name in ('Box_Suspension','Box_Latch','Box_LatchSeat'):continue
  for v in ob.data.vertices:
   v.co.y=164+(v.co.y-164)*.75
   if v.co.z<-9:v.co.z=-9+(v.co.z+9)*1.25
  ob.data.update();ob.update_tag()
 bpy.context.view_layer.update()
 for name in ('Box_Shell','Box_Lid'):
  ob=next(o for o in PARTS if o.name==name)
  cutbox(ob,(-80,138,-27),(-29,207,2),r=2)
