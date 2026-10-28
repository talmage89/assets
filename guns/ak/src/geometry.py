"""Original exterior visual prop, authored in mm; never a fabrication model.

Changing subdivision cages supply compound furniture. Stamped surfaces have
finite gauge. Hidden action/fire-control shapes are inert animation proxies.
Only exterior envelope and photographs inform these artistic approximations.
"""
import math
import bpy,bmesh
from mathutils import Matrix,Vector
from kit import model as M
from guns.common.ammo762_visual import cartridge
PARTS=[];HIGH=[];MAT={}
BORE=85.;SIGHT=128.;MUZZLE=595.

def palette():
 for k,c,m,r in [('paint',(.010,.010,.010),0,.43),('blue',(.017,.018,.019),.75,.36),
  ('steel',(.24,.25,.26),1,.32),('wood',(.18,.047,.016),0,.35),
  ('grip',(.069,.023,.014),0,.47),('case',(.075,.085,.043),.7,.38),
  ('copper',(.42,.18,.075),1,.31),('dark',(.009,.009,.009),.5,.5)]:
  mat=bpy.data.materials.new('Inspection_'+k);mat.use_nodes=True
  mat.diffuse_color=(*c,1);bs=mat.node_tree.nodes['Principled BSDF']
  bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Metallic'].default_value=m
  bs.inputs['Roughness'].default_value=r;MAT[k]=mat

def reg(o,bone='Root',radius=0,segments=2):
 if radius:
  M.bevel(o,radius,segments)
  wn=o.modifiers.new('Area-weighted manufactured flats','WEIGHTED_NORMAL');wn.keep_sharp=True
 M.smooth(o,48);M.apply(o)
 o['asset_set']='R39';o['bone']=bone;o['part_name']=o.name;PARTS.append(o)
 return o
def box(n,lo,hi,mat='paint',bone='Root',r=.4,register=True):
 a,b=Vector(lo),Vector(hi);o=M.box(n,(a+b)/2,b-a,MAT[mat],0)
 bpy.context.view_layer.update()
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 return reg(o,bone,r) if register else o
def lathe(name,p,mat='paint',bone='Root',axis='Y',center=(0,0),nseg=32,closed=False,register=True,**kw):
 count=kw.get('n',nseg)
 o=M.lathe(name,p,MAT[mat],segments=count,axis=axis,center=center,closed=closed)
 return reg(o,bone) if register else o
def profile(n,p,a,b,mat='paint',bone='Root',axis='X',r=.35,register=True):
 o=M.profile(n,p,a,b,MAT[mat],axis=axis)
 return reg(o,bone,r) if register else o
def cut(o,t):M.boolean(o,t);return o
def cutbox(o,a,b,r=0):
 t=box('Cutting tool',a,b,r=r,register=False)
 if r:M.bevel(t,r,3);M.apply(t)
 return cut(o,t)
def rounded(w,h,r,n=4):return M.rounded_rectangle(w,h,r,n)
def reduce(o,target):
 count=sum(len(f.vertices)-2 for f in o.data.polygons)
 if count>target:
  d=o.modifiers.new('Silhouette allocation','DECIMATE');d.ratio=target/count;M.apply(o)
 return o
def sculpt(o,target,level=2):
 s=o.modifiers.new('Supported compound cage','SUBSURF');s.levels=s.render_levels=level;M.apply(o)
 M.smooth(o,70);M.apply(o)
 high=o.copy();high.data=o.data.copy();bpy.context.collection.objects.link(high)
 high.name='HIGH_'+o.name;high['low_target']=o.name;high['bake_only']=True;HIGH.append(high)
 reduce(o,target)
 d=o.modifiers.new('Retained sculpt normals','DATA_TRANSFER');d.object=high
 d.use_loop_data=True;d.data_types_loops={'CUSTOM_NORMAL'};d.loop_mapping='POLYINTERP_NEAREST';M.apply(o)
 if 'Handguard' in o.name:
  # Thin U skins must not borrow opposing cavity normals at the rim.
  o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops))
 return reg(o)
def rivet(n,y,z,side,r=2.4):
 a=side*17.55;b=side*19
 p=[(min(a,b),0),(min(a,b),r*.78),((a+b)/2,r),(max(a,b),r*.78),(max(a,b),0)]
 return lathe(n,p,axis='X',center=(y,z),nseg=16)
def screw(n,position,axis='Z',r=3):
 x,y,z=position
 center=(y,z) if axis=='X' else ((x,z) if axis=='Y' else (x,y))
 h=position['XYZ'.index(axis)]
 o=lathe(n,[(h-.6,0),(h-.6,r),(h,r),(h+.3,r-.3),(h+.3,0)],'blue',axis=axis,center=center,nseg=20)
 # Screw slot is a shallow machined recess, not a black floating decal.
 if axis=='Z':cutbox(o,(x-2.1,y-.35,z),(x+2.1,y+.35,z+1))
 return o

def receiver():
 # An open U section with rounded lower bends and finite wall gauge.
 side=[(17.5,z) for z in (53,55,57,59,61,63,68,76,86)]
 section=[(-x,z) for x,z in reversed(side)]+[(-17.1,51.6),(-16,50.4),(-14.5,50),
  (14.5,50),(16,50.4),(17.1,51.6)]+side
 loops=[]
 for y in (-35,-25,-12,0,40,80,94,100,110,124,128,132,134,138,143,148,152,156,160,164,170,178,190,205,220):
  loops.append([(x-math.copysign(1.8*math.exp(-((y-143)/12)**4-((z-57)/5.5)**4),x),y,z) for x,z in section])
 o=M.loft('Receiver_Sheet',loops,MAT['paint'],caps=False,closed=False)
 so=o.modifiers.new('One millimeter visual sheet gauge','SOLIDIFY');so.thickness=1;so.offset=-1;so.use_even_offset=True;M.apply(o)
 cutbox(o,(-15,94,35),(15,184,62),r=2)
 cutbox(o,(-4.5,35,45),(4.5,63,58),r=1.3)
 reg(o)
 for side in (-1,1):
  for i,(y,z) in enumerate([(193,76),(210,76),(181,51),(-22,75),(-22,50),(3,59)]):
   rivet('Receiver_Rivet'+str(side)+'_'+str(i),y,z,side)
 # Visible inserts are exterior seating envelopes. No locking recesses/cam track.
 back=box('Rear_Insert',(-16.2,-35,42),(16.2,-21,88),'blue',r=1.2)
 front=box('Front_Insert',(-16.1,185,42),(16.1,220,91),'blue',r=1.2,register=False)
 cut(front,lathe('Visual passage',[(182,0),(182,11),(224,11),(224,0)],center=(0,BORE),register=False))
 reg(front,radius=.5)
 for side in (-1,1):
  box('Carrier_VisualRail'+str(side),(side*12 if side>0 else -15,-18,77),(15 if side>0 else -12,185,79),'steel',r=.2)
 # Reinforced rear stock tongue and supported cover latch.
 box('Stock_Tang',(-6,-71,78),(6,-22,81),'blue',r=.7)
 screw('Tang_Screw',(0,-58,81.2))
 latch=box('Cover_RetainingButton',(-5.5,-38,92),(5.5,-26,100),'blue',r=1)

def cover():
 # Continuous pressed ribs follow the entire vaulted sheet, not stuck-on wires.
 ys=sorted({-35,-34,-30,-25,-20,175,180,190,*[k+d for k in (-5,75,150) for d in (-6,-3,-1,0,1,3,6)]})
 def rib(y):
  return .6*sum(math.exp(-((y-k)/2.2)**4) for k in (-5,75,150))
 loops=[]
 for y in ys:
  bump=rib(y);arch=[]
  for i in range(33):
   t=math.pi*i/32
   arch.append(((18.3+bump)*math.cos(t),y,86+(27+bump)*math.sin(t)))
  # Outer and inner profile enclose the bent sheet, open underneath.
  arch += [((17.5+bump)*math.cos(math.pi*i/32),y,86+(26.2+bump)*math.sin(math.pi*i/32)) for i in range(32,-1,-1)]
  loops.append(arch)
 o=M.loft('TopCover_Pressed',loops,MAT['paint'])
 # Carrier/handle opening on the right. The roof stays above the visible port.
 cutbox(o,(9,45,76),(26,191,98),r=4)
 cutbox(o,(-6,-39,91),(6,-29,101),r=1)
 reg(o,radius=.16,segments=1);reduce(o,3500)
 cap=[(18.3*math.cos(math.pi*i/32),86+27*math.sin(math.pi*i/32)) for i in range(33)]
 rear=profile('TopCover_RearCap',cap,-35.2,-34.3,'paint',axis='Y',r=.15,register=False)
 cutbox(rear,(-6,-37,91),(6,-32,101),r=.7);reg(rear,radius=.12)
 # Longitudinal rolled shoulders have real sections rather than thin rods.
 for side in (-1,1):
  y1=45 if side==1 else -30
  p=[(side*18.6,85),(side*18.6,88),(side*18.0,89),(side*17.8,88),(side*17.8,85)]
  reg(M.loft('Cover_Return'+str(side),[[(x,y,z) for x,z in p] for y in (-30,y1 if y1>-30 else 190)],MAT['paint']))

def furniture():
 # Stock: changing oval/superelliptic sections; rounded comb and fuller toe.
 rows=[(-282,16,-12,82),(-281,17.3,-13,83),(-277,18,-13,84),
  (-250,18.3,-10,85),(-210,18.4,1,85),(-170,17.6,14,84),
  (-135,16.2,25,85),(-108,14.8,32,85),(-88,14.4,35,86),
  (-62,15.7,39,85),(-39,16.3,41,88),(-35.2,16.3,41,88),(-34.5,15.9,42,87)]
 loops=[]
 for y,hw,b,t in rows:
  loop=[]
  for i in range(40):
   a=math.tau*i/40;c,s=math.cos(a),math.sin(a)
   x=hw*math.copysign(abs(c)**.67,c)
   z=(b+t)/2+(t-b)/2*math.copysign(abs(s)**.77,s)
   loop.append((x,y,z))
  loops.append(loop)
 sculpt(M.loft('Stock_Sculpt',loops,MAT['wood']),3200)
 # Buttplate repeats the actual compound end section with rounded rolled rim.
 loops=[]
 for y,w,h in [(-285,32.5,93),(-284.5,35.8,97),(-282.4,35.8,97),(-281.6,33.8,95)]:
  loops.append([(x,y,z+35) for x,z in rounded(w,h,8,6)])
 reg(M.loft('Buttplate',loops,MAT['blue']),radius=.5)
 # Trap seam and flap shown on rear surface.
 profile('Buttplate_Trap',[(x,z+35) for x,z in rounded(15,35,6,6)],-285.4,-285,'blue',axis='Y',r=.15)
 for z in (0,70):screw('Butt_Screw',(0,-285.5,z),'Y',2.5)
 # Sling eye is a formed strip, seated beneath the toe.
 loop=[(-6,-249,-5),(-7,-254,-13),(-5,-260,-17),(5,-260,-17),(7,-254,-13),(6,-249,-5)]
 reg(M.tube('Stock_SlingEye',loop,1.3,MAT['blue'],sides=8))
 # Handguards use supported subdivision U sections, with an internal barrel channel.
 for name,ys,width,bottom,top,upper,target in [
  ('LowerHandguard',[220,221,225,239,265,300,332,355,363,364],22.3,39,84,False,2600),
  ('UpperHandguard',[245,246,249,258,280,310,334,345,346],17.7,91,120,True,1800)]:
  loops=[]
  for y in ys:
   u=(y-ys[0])/(ys[-1]-ys[0]);hw=width*(1-.08*u)+(0 if upper else 1.2*math.sin(math.pi*u))
   # Oval sections curve all the way round. End support rings retain a broad rim.
   zc=(bottom+top)/2;rh=(top-bottom)/2
   ring=[]
   if upper:
    # Top half-ring over the gas tube, with finite flat-ish lower lands.
    for i in range(33):
     a=math.pi*i/32;ring.append((hw*math.cos(a),y,bottom+(top-bottom)*math.sin(a)))
    for i in range(32,-1,-1):
     a=math.pi*i/32;ring.append(((hw-3.2)*math.cos(a),y,bottom+2+(top-bottom-5.2)*math.sin(a)))
   else:
    for i in range(41):
     a=math.pi+math.pi*i/40
     depth=top-bottom-8*u+3*math.exp(-((u-.15)/.18)**2)
     ring.append((hw*math.cos(a),y,top+depth*math.sin(a)))
    for i in range(40,-1,-1):
     a=math.pi+math.pi*i/40
     depth=top-bottom-8*u+3*math.exp(-((u-.15)/.18)**2)
     ring.append(((hw-4.2)*math.cos(a),y,top-1+(depth-5.2)*math.sin(a)))
   loops.append(ring)
  ob=M.loft(name+'_Sculpt',loops,MAT['wood'],caps=False)
  s=ob.modifiers.new('Continuous carved section cage','SUBSURF');s.levels=s.render_levels=2;M.apply(ob)
  bm=bmesh.new();bm.from_mesh(ob.data)
  bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
  # Dense source retained before game reduction.
  sculpt(ob,target,level=0)
 # Molded grip with nonparallel faces, palm swell, round heel and neck.
 rows=[(-79,-18,12,16),(-78,-18,14.8,18),(-74,-18,15.6,19),
  (-60,-15,16.2,18.8),(-30,-6,16.4,18.5),(-3,-3,15.2,14),
  (20,-6,14.4,16),(34,-8,15.4,18),(38,-8,15.7,18),(39,-8,15.2,17)]
 loops=[]
 for z,y,hw,hd in rows:
  loops.append([(hw*math.copysign(abs(math.cos(a))**.65,math.cos(a)),
    y+hd*math.copysign(abs(math.sin(a))**.70,math.sin(a)),z) for a in [math.tau*i/40 for i in range(40)]])
 sculpt(M.loft('PistolGrip_Sculpt',loops,MAT['grip']),2300)
 screw('Grip_HeelScrew',(0,-18,-79),'Z',3)

def guard_controls():
 # Broad stamped strip, not a wire loop; 12 mm across, flat blade thickness.
 path=[]
 for q in [((3,40),(6,32),(5,14),(15,8)),((15,8),(25,2),(58,2),(71,7)),
           ((71,7),(74,12),(73,29),(73,40))]:
  pts=M.bezier(*q,12);path.extend(pts if not path else pts[1:])
 loops=[]
 for i,(y,z) in enumerate(path):
  d=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized();normal=Vector((-d.y,d.x))
  loops.append([(x,y+v*normal.x,z+v*normal.y) for x,v in rounded(12,1.8,.6,3)])
 reduce(reg(M.loft('TriggerGuard_Stamping',loops,MAT['blue'])),800)
 box('Guard_RearFlange',(-7,-4,40),(7,8,42),'blue',r=.3)
 box('Guard_FrontFlange',(-7,68,40),(7,80,42),'blue',r=.3)
 housing=box('Release_Housing',(-9,76,20),(9,91,42),'blue',r=1,register=False)
 cutbox(housing,(-6.7,74,17),(6.7,94,41),r=.8)
 cut(housing,lathe('Oversize visual pin relief',[(-12,0),(-12,2.8),(12,2.8),(12,0)],axis='X',center=(84,33),register=False))
 reg(housing,radius=.5)
 # Concave finger face faces +Y. The rounded toe curls toward the muzzle.
 face=M.bezier((33,42),(22,30),(24,20),(45,12),16)
 toe=M.bezier((45,12),(48,10),(48,8),(44,8.3),6)
 back=M.bezier(toe[-1],(17,16),(17,30),(23,42),16)
 profile('Trigger_Shoe',face+toe[1:]+back[1:],-3,3,'blue','Trigger',r=.65)
 lathe('Trigger_VisualPin',[(-16,0),(-16,2.5),(16,2.5),(16,0)],'blue','Trigger',axis='X',center=(29,45),nseg=20)
 # Simplified hammer and support shoe are animation silhouettes, no sear geometry.
 profile('Hammer_Visual',M.fillet_polygon([(52,50),(46,69),(54,77),(63,75),(64,61)],2.5,6),-4,4,'blue','Hammer',r=1)
 lathe('Hammer_VisualPin',[(-15,0),(-15,2.4),(15,2.4),(15,0)],'blue','Hammer',axis='X',center=(55,52),nseg=20)
 # Paddle has broad folded face, axle and radiused lower end.
 profile('MagRelease_Paddle',M.fillet_polygon([(80,35),(88,35),(92,6),(88,1),(83,2)],1.4,5),-6,6,'blue','MagRelease',r=.5)
 lathe('MagRelease_Axle',[(-11,0),(-11,2.5),(11,2.5),(11,0)],'blue','MagRelease',axis='X',center=(84,33),nseg=20)
 box('MagRelease_VisualCatch',(-5,88,33.5),(5,98,36),'blue','MagCatch',r=.2)
 # Selector is a thin pressed fan-shaped plate, with turned edge and broad tab.
 shape=M.fillet_polygon([(-7,73),(0,78),(17,78),(106,99),(112,97),(108,92),(20,62),(4,61)],1.2,5)
 profile('Selector_Lever',shape,18.1,19.5,'paint','Selector',r=.45)
 lathe('Selector_Hub',[(17.6,0),(17.6,6),(20,6),(20.5,5),(20.5,0)],'blue','Selector',axis='X',center=(5,69),nseg=28)
 profile('Selector_ThumbFold',M.fillet_polygon([(95,95),(111,98),(112,94),(97,91)],.8,4),19,23,'blue','Selector',r=.5)
 # Original three detent witness marks, exterior only.
 for angle in (0,-16,-26):
  theta=math.radians(angle);y=5+96*math.cos(theta);z=69+96*math.sin(theta)+25*math.cos(theta)
  box('Selector_Detent_'+str(angle),(17.55,y-2,z-.45),(18,y+2,z+.45),'steel',r=.15)

def action_barrel():
 # No barrel chamber/rifling or functional bolt lock. The muzzle has a short
 # dark visual recess; the buried rear barrel is a solid silhouette.
 barrel=lathe('Barrel',[(170,0),(170,11),(220,11),(235,9.8),(355,8.4),(440,7.7),
  (550,7.2),(584,7.2),(585,6.7),(585,4),(577,4),(577,0)],'blue',center=(0,BORE),nseg=40,register=False)
 cut(barrel,lathe('Oversize inert display cavity',[(165,0),(165,8),(232,8),(232,0)],center=(0,BORE),register=False))
 reg(barrel)
 # Gas tube and lower retainers; original rounded machined seating envelopes.
 lathe('GasTube',[(221,8),(221,9.8),(345,9.8),(351,8.5),(351,8)],'blue',center=(0,107),closed=True,nseg=32)
 for y in (221,363):
  loops=[[(x,yy,z+66) for x,z in rounded(w,h,6,5)] for yy,w,h in [(y-2,43,53),(y,44,54),(y+2,43,53)]]
  ob=M.loft('Handguard_Retainer'+str(y),loops,MAT['blue'])
  cutbox(ob,(-18,y-4,43),(18,y+4,91),r=5);reg(ob,radius=.5)
 # Gas block neck leans at about 45 degrees; holes are cosmetic vents.
 lathe('GasBlock_BarrelBand',[(431,7.8),(431,12),(435,13),(445,13),(450,10),(450,7.8)],'blue',center=(0,BORE),closed=True,nseg=32)
 block=profile('GasBlock_Neck',M.fillet_polygon([(429,86),(451,87),(430,115),(411,116),(414,108)],3,6),-9,9,'blue',r=1.2)
 lathe('GasBlock_TubeSeat',[(345,8),(345,10),(416,10),(423,9),(423,8)],'blue',center=(0,107),closed=True,nseg=32)
 for side in (-1,1):
  for y in (383,401):
   a,b=sorted((side*8.6,side*10.4))
   lathe('Gas_Vent'+str(side)+str(y),[(a,0),(a,1.1),(b,1.1),(b,0)],'dark',axis='X',center=(y,107),nseg=12)
 box('Bayonet_Lug',(-7,439,62),(7,452,73),'blue',r=1)
 cutbox(PARTS[-1],(-2.6,437,60),(2.6,454,67),r=.8)
 # Cleaning rod is supported at two bands, slight tip shoulder.
 lathe('CleaningRod',[(229,0),(229,2),(548,2),(550,2.8),(558,2.8),(558,0)],'blue',center=(0,66),nseg=16)
 # Slanted muzzle sleeve; cut-plane affects both inner and outer forward rings.
 loops=[]
 for station,r in [(570,7.5),(570,10),(573,10),(588,10),(588,7.8),(572,7.8)]:
  loops.append([(r*math.cos(a),station+(7*math.sin(a)+2*math.cos(a) if station==588 else 0),BORE+r*math.sin(a))
                 for a in [math.tau*i/40 for i in range(40)]])
 reg(M.loft('Muzzle_SlantBrake',loops+[loops[0]],MAT['blue'],caps=False))
 # Visible carrier, piston and handle are independent rigid animation owners.
 lathe('Carrier_Body',[(92,0),(92,7.5),(99,8),(164,8),(168,7),(168,0)],'blue','BoltCarrier',center=(0,99.5),nseg=32)
 box('Carrier_PortCheek',(8,80,89),(16.2,168,97),'blue','BoltCarrier',r=1.7)
 lathe('Carrier_Piston',[(174,0),(174,4),(353,4),(357,7),(368,7),(368,0)],'steel','BoltCarrier',center=(0,107),nseg=24)
 # One forged, rounded handle silhouette with a broad finger-contact pad.
 rows=[]
 for x,y,w,h in [(14.8,164,3,3),(18,165,5,4),(24,165,7,4),(30,164,9,4),(34,163,7,3.5)]:
  rows.append([(x,y+yy,91+zz) for yy,zz in rounded(w,h,1.5,4)])
 reg(M.loft('ChargingHandle',rows,MAT['blue']),'ChargingHandle',radius=.3)
 lathe('Bolt_Visual',[(138,0),(138,6.0),(169,6.0),(169,0)],'steel','Bolt',center=(0,BORE),nseg=24)

def sights():
 # Rounded rear saddle, tangent leaf, broad adjustment slider and actual notch.
 base=profile('Sight_RearBlock',M.fillet_polygon([(190,86),(191,105),(200,119),(225,119),(232,106),(231,85)],3,6),-14,14,'blue',r=1)
 cutbox(base,(-10,192,108),(10,228,124),r=2)
 for z,r in [(107,7.5),(85,8.2)]:
  cut(base,lathe('Inert animation clearance',[(185,0),(185,r),(236,r),(236,0)],center=(0,z),register=False))
 leaf=box('Sight_TangentLeaf',(-7,188,121),(7,229,124),'blue',r=.7)
 notch=box('Sight_RearNotch',(-7,188,122),(7,192,128),'blue',r=.5,register=False)
 cutbox(notch,(-1.5,186,125),(1.5,194,132),r=.3)
 reg(notch,radius=.15)
 for side in (-1,1):
  a,b=sorted((side*7,side*11.5))
  box('Sight_SliderEar'+str(side),(a,208,118),(b,216,126),'blue',r=.8)
 box('Sight_SliderBridge',(-7,208,124),(7,216,126),'blue',r=.5)
 for y in range(194,228,4):
  for side in (-1,1):box('Sight_Graduation',(side*2.2 if side>0 else -6.3,y,124),(6.3 if side>0 else -2.2,y+.45,124.2),'steel',r=.05)
 lathe('Sight_RearPivot',[(-16,0),(-16,2.3),(16,2.3),(16,0)],'blue',axis='X',center=(227,120),nseg=24)
 # Front band and cast tower, with a weight-relief window and rounded roots.
 lathe('Sight_FrontBand',[(545,7.4),(545,11),(551,12),(559,11),(560,7.4)],'blue',center=(0,BORE),closed=True,nseg=40)
 tower=profile('Sight_FrontTower',M.fillet_polygon([(544,84),(560,84),(557,124),(548,125)],2,6),-9,9,'blue',r=1.2,register=False)
 cutbox(tower,(-12,548,94),(12,555,106),r=2.4);reg(tower,radius=.7)
 # Hood is a protective ring with a short mounting skirt, finite rounded rim.
 lathe('Sight_FrontHood',[(547,9),(547,11.5),(549,12),(555,12),(557,11.5),(557,9)],'blue',center=(0,128),closed=True,nseg=56)
 # Narrow post rises to the shared 128-mm line inside the hood.
 box('Sight_FrontPost',(-.8,550,117),(.8,553,128),'blue',r=.15)
 lathe('Sight_WindageDrum',[(-10,0),(-10,4.3),(10,4.3),(10,0)],'blue',axis='X',center=(552,117),nseg=28)

def mag_path(s):
 # Large exterior curvature, progressively rotating sections and floorplate.
 angle=math.atan(.0033*s+.000009*s*s)
 y=132+(.00165*s*s+.000003*s*s*s);z=70-s
 return y,70-.87*s,angle

def magazine():
 stations=[0,1,5,12,25,45,65,90,115,140,160,177,185,187]
 def ring(s,inside=False):
  y,z,a=mag_path(s);w=26-(1.6 if inside else 0);d=63-(1.6 if inside else 0)
  # Densify flat flanks so the integral longitudinal ribs have curved shoulders.
  sec=rounded(w,d,3.0,5);points=[]
  for p,q in zip(sec,sec[1:]+sec[:1]):
   points.append(p)
   if abs(p[0]-q[0])<1e-5 and abs(p[1]-q[1])>20:
    points.extend((p[0],p[1]+(q[1]-p[1])*k/32) for k in range(1,32))
  result=[]
  for x,v in points:
   crest=sum(1.15*math.exp(-((v-c)/1.5)**4) for c in (-22,-11,0,11,22))
   fade=max(0,min(1,(s-8)/10,(182-s)/9))
   x+=math.copysign(crest*fade*max(0,(abs(x)-8)/5),x)
   result.append((x,y+v*math.cos(a),z+v*math.sin(a)))
  return result
 body=M.loft('Magazine_Sheet',[ring(s) for s in stations],MAT['paint'])
 cut(body,M.loft('Magazine cavity',[ring(s,True) for s in [-3,*stations,191]],MAT['paint']))
 cutbox(body,(-17,147,65),(17,180,83),r=2)
 reg(body,'Magazine',radius=.17,segments=1);reduce(body,3100)
 # Raised spine is folded from finite strip stock and follows the actual arc.
 for side in (-1,1):
  points=[]
  for s in stations:
   y,z,a=mag_path(s);v=side*31.8;points.append((0,y+v*math.cos(a),z+v*math.sin(a)))
  reg(M.tube('Magazine_FoldSpine'+str(side),points,.8,MAT['blue'],sides=6),'Magazine')
 y,z,a=mag_path(188)
 loops=[]
 for off,w,d in [(1,28.7,66),(.2,29,66.5),(-2,29,66.5),(-2.5,28,65.5)]:
  loops.append([(x,y+v*math.cos(a)-off*math.sin(a),z+v*math.sin(a)+off*math.cos(a)) for x,v in rounded(w,d,3.3,5)])
 reg(M.loft('Magazine_Floorplate',loops,MAT['blue']),'Magazine',radius=.25)
 box('Magazine_FrontLug',(-5,162,64),(5,171,70),'blue','Magazine',r=.7)
 box('Magazine_RearCatch',(-5,94,36),(5,103,41),'blue','Magazine',r=.4)
 # Curled lips visibly reach over the two staggered display rounds.
 for side,x,z in [(1,5.15,70),(-1,-5.15,64.4)]:
  pts=[]
  for r,angles in [(5.9,range(0,67,6)),(5.4,range(66,-1,-6))]:
   pts.extend((x+side*r*math.cos(math.radians(t)),z+r*math.sin(math.radians(t))) for t in angles)
  profile('Magazine_FeedLip'+str(side),pts,108,132,'blue','Magazine',axis='Y',r=.1)
 for name,xyz,segments in [('TopRound',(5.15,103,70),32),('SecondRound',(-5.15,103,64.4),24),('ThirdRound',(5.15,104,58.8),16)]:
  cartridge(lathe,'Magazine_'+name,xyz,name,sides=segments)
 box('Magazine_Follower',(-10,106,50),(10,153,53.3),'blue','Follower',r=1)
 cartridge(lathe,'ChamberRound',(0,170,BORE),'ChamberRound',sides=12)
 cartridge(lathe,'EjectedCase',(0,126,BORE),'EjectedCase',fired=True,sides=16)

def hand_normals(ob):
 """Analytic oval normals avoid opposing inner-skin transfer at the U rim."""
 upper='Upper' in ob.name;w=17.7 if upper else 22.3
 start,end=(245,346) if upper else (220,364)
 zc,rh=(91,29) if upper else (84,45)
 inset=3.2 if upper else 4.2;izc=93 if upper else 83;irh=rh-5.2
 normals=[]
 for f in ob.data.polygons:
  for j in f.loop_indices:
   v=ob.data.vertices[ob.data.loops[j].vertex_index].co
   u=(v.y-start)/(end-start);hw=w*(1-.08*u)+(0 if upper else 1.2*math.sin(math.pi*u))
   local_rh=rh if upper else rh-8*u+3*math.exp(-((u-.15)/.18)**2)
   local_irh=local_rh-5.2
   if abs(f.normal.y)>.8:n=f.normal.copy()
   else:
    outer=abs((v.x/hw)**2+((v.z-zc)/local_rh)**2-1)
    inner=abs((v.x/(hw-inset))**2+((v.z-izc)/local_irh)**2-1)
    h,c,r,sign=(hw,zc,local_rh,1) if outer<inner else (hw-inset,izc,local_irh,-1)
    n=Vector((v.x/h**2, v.x*v.x/h**3*(w*.08/(end-start)),(v.z-c)/r**2)).normalized()*sign
    if n.dot(f.normal)<.08:n=f.normal.copy()
   normals.append(n)
 ob.data.normals_split_custom_set(normals)
