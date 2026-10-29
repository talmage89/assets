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
def source(o,low=None):
 """Retain an authored detail source without adding it to the game mesh."""
 o['bake_only']=True;o['low_target']=low or o.name.removeprefix('HIGH_')
 HIGH.append(o);return o
def ribbon(name,path,width,gauge,mat='blue',bone='Root',edge=.15):
 """Flat broad faces with only the thin sheared edges rounded."""
 loops=[]
 for i,(y,z) in enumerate(path):
  tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized()
  normal=Vector((-tangent.y,tangent.x))
  loops.append([(x,y+v*normal.x,z+v*normal.y) for x,v in rounded(width,gauge,edge,2)])
 return reg(M.loft(name,loops,MAT[mat]),bone)
def soften_forging(ob,voxel=.45):
 """Original smooth union with regular surface spacing before machined cuts."""
 remesh=ob.modifiers.new('Continuous forged surface','REMESH');remesh.mode='VOXEL'
 remesh.voxel_size=voxel;remesh.use_smooth_shade=True;M.apply(ob)
 smooth=ob.modifiers.new('Soft forged shoulder transitions','SMOOTH');smooth.factor=.55;smooth.iterations=3;M.apply(ob)
 return ob
def rivet(n,y,z,side,r=2.4):
 a=side*17.55;b=side*19
 p=[(min(a,b),0),(min(a,b),r*.78),((a+b)/2,r),(max(a,b),r*.78),(max(a,b),0)]
 return lathe(n,p,axis='X',center=(y,z),nseg=12)
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
 ys=sorted({-35,-34,-30,-25,-20,175,180,190,*[k+d for k in (-5,75,150) for d in (-7,-5,-3,-1.5,0,1.5,3,5,7)]})
 def rib(y):
  return 1.5*sum(math.exp(-((y-k)/3.2)**4) for k in (-5,75,150))
 loops=[]
 for y in ys:
  bump=rib(y);arch=[]
  for i in range(33):
   t=math.pi*i/32
   # A flatter crown and rolled shoulders, with ribs pressed through the roof.
   arch.append(((18.3+bump)*math.copysign(abs(math.cos(t))**.82,math.cos(t)),y,86+(27+bump)*math.sin(t)**.72))
  # Outer and inner profile enclose the bent sheet, open underneath.
  arch += [((17.5+bump)*math.copysign(abs(math.cos(math.pi*i/32))**.82,math.cos(math.pi*i/32)),y,86+(26.2+bump)*math.sin(math.pi*i/32)**.72) for i in range(32,-1,-1)]
  loops.append(arch)
 o=M.loft('TopCover_Pressed',loops,MAT['paint'])
 # Carrier/handle opening on the right. The roof stays above the visible port.
 cutbox(o,(9,45,76),(26,191,98),r=4)
 cutbox(o,(-6,-39,91),(6,-29,101),r=1)
 reg(o,radius=.16,segments=1);reduce(o,3500)
 # The return cap seats inside the sheet. Its edge must not share the outer
 # roof surface: coincident triangles previously caused bright seam flecks.
 cap=[(17.6*math.copysign(abs(math.cos(math.pi*i/32))**.82,math.cos(math.pi*i/32)),86+26.3*math.sin(math.pi*i/32)**.72) for i in range(33)]
 rear=profile('TopCover_RearCap',cap,-35.2,-34.3,'paint',axis='Y',r=.15,register=False)
 cutbox(rear,(-6,-37,91),(6,-32,101),r=.7);reg(rear,radius=.12)
 # Folded rear return surrounds the button opening; a sheet lip, not a seam.
 lip=profile('TopCover_ButtonLip',M.fillet_polygon([(-7,90),(7,90),(7,102),(-7,102)],1.6,5),-35.8,-34.8,'paint',axis='Y',r=.15,register=False)
 cutbox(lip,(-5.9,-37,91.2),(5.9,-33,100.5),r=1);reg(lip,radius=.12)
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
 rows=[(-79,-18,11.4,15.5),(-78,-18,14.1,17.5),(-74,-18,14.4,18),
  (-60,-16,14.7,19.0),(-45,-11,15.1,20.5),(-30,-6,15.5,20.8),
  (-12,-3,15.4,18.2),(-3,-4,14.5,14.5),
  (12,-8,13.5,15),(20,-8,14.4,17),(34,-8,15.4,18),(38,-8,15.7,18),(39,-8,15.2,17)]
 loops=[]
 for z,y,hw,hd in rows:
  loops.append([(hw*math.copysign(abs(math.cos(a))**.34,math.cos(a)),
    y+hd*math.copysign(abs(math.sin(a))**.62,math.sin(a)),z) for a in [math.tau*i/40 for i in range(40)]])
 sculpt(M.loft('PistolGrip_Sculpt',loops,MAT['grip']),2300)
 # Low, wide molded ridges follow the actual compound skin, rather than
 # floating circular wires. The dense source supplies every supporting ray.
 from mathutils.bvhtree import BVHTree
 high=next(o for o in HIGH if o.name=='HIGH_PistolGrip_Sculpt')
 high.data.calc_loop_triangles();tree=BVHTree.FromPolygons([v.co for v in high.data.vertices],[t.vertices for t in high.data.loop_triangles],all_triangles=True)
 for z0,y,hw,hd in rows[3:8]:
  for sign in (-1,1):
   loops=[]
   for dz in (-1.4,-1,-.5,0,.5,1,1.4):
    ring=[]
    for x in (-9,-8,-5,0,5,8,9):
     hit=tree.ray_cast(Vector((x,sign*100,z0+dz)),Vector((0,-sign,0)),200)
     assert hit[0] is not None
     height=.32*max(0,1-(dz/1.4)**2)*max(0,1-(abs(x)/9)**6)
     ring.append((x,hit[0].y+sign*height,z0+dz))
    loops.append(ring)
   ob=M.loft('HIGH_GripStrap',loops,MAT['grip'],caps=False,closed=False)
   if sum(f.normal.y for f in ob.data.polygons)*sign<0:
    for f in ob.data.polygons:f.flip()
   M.smooth(ob,80);source(ob,'PistolGrip_Sculpt')
 screw('Grip_HeelScrew',(0,-18,-79),'Z',3)

def guard_controls():
 # Broad stamped strip, not a wire loop; 12 mm across, flat blade thickness.
 path=[]
 for q in [((3,40),(6,32),(5,14),(15,8)),((15,8),(25,2),(58,2),(71,7)),
           ((71,7),(74,12),(73,29),(73,40))]:
  pts=M.bezier(*q,12);path.extend(pts if not path else pts[1:])
 ribbon('TriggerGuard_Stamping',path,13,1.65,edge=.16)
 box('Guard_RearFlange',(-7,-4,40),(7,8,42),'blue',r=.3)
 box('Guard_FrontFlange',(-7,68,40),(7,80,42),'blue',r=.3)
 section=M.fillet_polygon([(-9,76),(-9,91),(9,91),(9,76),(7.5,76),(7.5,89.5),(-7.5,89.5),(-7.5,76)],.45,3)
 housing=M.loft('Release_Housing',[[(x,y,z) for x,y in section] for z in (21,42)],MAT['blue'])
 cutbox(housing,(-5.3,88,32.5),(5.3,93,37),r=.25)
 cut(housing,lathe('Oversize visual pin relief',[(-12,0),(-12,2.8),(12,2.8),(12,0)],axis='X',center=(84,33),register=False))
 reg(housing,radius=.2)
 # Concave finger face faces +Y. The rounded toe curls toward the muzzle.
 face=M.bezier((33,42),(26,35),(25,28),(31,23),16)
 toe=M.bezier((31,23),(34,21),(34,20),(30,20),6)
 back=M.bezier(toe[-1],(22,24),(22,35),(28,42),16)
 profile('Trigger_Shoe',face+toe[1:]+back[1:],-2.6,2.6,'blue','Trigger',r=.45)
 lathe('Trigger_VisualPin',[(-16,0),(-16,2.5),(16,2.5),(16,0)],'blue','Trigger',axis='X',center=(29,45),nseg=20)
 # Hidden hammer/sear has no render mesh. The retained Hammer transform still
 # carries the accepted clip timing; an inventory check proves zero visibility.
 # Paddle has broad folded face, axle and radiused lower end.
 paddle=M.bezier((84,35),(85,19),(91,10),(98,9),16)
 ribbon('MagRelease_Paddle',paddle,13.5,1.4,bone='MagRelease',edge=.2)
 lathe('MagRelease_Axle',[(-11,0),(-11,2.5),(11,2.5),(11,0)],'blue','MagRelease',axis='X',center=(84,33),nseg=20)
 box('MagRelease_VisualCatch',(-5,88,33.5),(5,98,36),'blue','MagCatch',r=.2)
 # Selector is a thin pressed fan-shaped plate, with turned edge and broad tab.
 shape=M.fillet_polygon([(-4,62),(-7,70),(-2,77),(8,79),(34,81),(54,96),(71,98),(152,99),(160.5,97),(160.5,83),(83,77),(32,66),(7,60)],1.5,5)
 profile('Selector_Lever',shape,20.5,21.9,'paint','Selector',r=.45)
 lathe('Selector_Hub',[(17.6,0),(17.6,6),(21.8,6),(23,5.5),(23,0)],'blue','Selector',axis='X',center=(5,69),nseg=28)
 tab=[]
 for x,y,z in [(20.5,146,88),(22,149,87),(24,152,86.5),(26,154,86.5)]:
  tab.append([(x,y+u,z+v) for u,v in rounded(7,8,1,3)])
 reg(M.loft('Selector_ThumbFold',tab,MAT['blue']),'Selector')
 lathe('Selector_HubRim',[(21.8,5),(21.8,7.4),(22.5,7.7),(23.1,7.4),(23.1,5)],'blue','Selector',axis='X',center=(5,69),nseg=28,closed=True)
 # Original three detent witness marks, exterior only.
 for angle in (0,-10,-15):
  theta=math.radians(angle);y=5+143*math.cos(theta)-16*math.sin(theta);z=69+143*math.sin(theta)+16*math.cos(theta)
  rivet('Selector_Detent_'+str(angle),y,z,1,r=1.1)
 lathe('Selector_Dimple',[(18.9,0),(18.9,1.1),(20.4,1.6),(21.9,1.8),(22.3,0)],'blue','Selector',axis='X',center=(148,85),nseg=16)

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
 # Hidden bolt lugs/sear geometry is intentionally absent; its transform is
 # retained for the interface. The visible carrier closes against a real face.
 lathe('Carrier_SeatingFace',[(166,0),(166,4),(185,4),(185,0)],'blue','BoltCarrier',center=(0,102.5),nseg=24)
 stop=box('Front_InsertUpperShoulder',(-9,185,91),(9,194,106.5),'blue',r=1,register=False)
 cut(stop,lathe('Piston visual passage',[(182,0),(182,5),(197,5),(197,0)],center=(0,107),register=False));reg(stop,radius=.3)

def sights():
 # The forged rear saddle changes section in all three axes. Its sloping
 # shoulders merge into a barrel collar; the leaf floats above a spring pocket.
 loops=[]
 for z,w,d,y in [(84,27,48,216),(86,30,53,216),(92,31,59,216),
                 (98,29,63,219),(109,26,65,220),(117,23,65,220),
                 (120,22,64,220),(121,21,62,220)]:
  loops.append([(x,y+v,z) for x,v in rounded(w,d,4,5)])
 base=M.loft('Sight_RearBlock',loops,MAT['blue'])
 soften_forging(base,.5)
 cutbox(base,(-7.8,189,115),(7.8,248,128),r=1.8)
 for z,r in [(107,7.5),(85,8.2)]:
  cut(base,lathe('Inert animation clearance',[(180,0),(180,r),(258,r),(258,0)],center=(0,z),register=False))
 M.bevel(base,.35,2);M.apply(base);sculpt(base,1100,level=0)
 # Long leaf, shallow central stiffening channel and front hinge cheeks.
 leaf=profile('Sight_TangentLeaf',M.fillet_polygon([(188,121),(248,119.5),(251,121),(251,123),(188,124)],.55,4),-6.7,6.7,'blue',r=.3,register=False)
 cutbox(leaf,(-.8,192,123),( .8,247,125),r=.3);reg(leaf,radius=.1)
 notch=profile('Sight_RearNotch',M.fillet_polygon([(-9,123),(-9,127.3),(-7,128),(-1.5,128),(-1.5,125),(1.5,125),(1.5,128),(7,128),(9,127.3),(9,123)],.25,3),187.7,190,'blue',axis='Y',r=.2)
 # Cylindrical release buttons nest in a thin slider saddle around the leaf.
 slider=profile('Sight_SliderBridge',M.fillet_polygon([(-8.4,120),(-8.4,125),(8.4,125),(8.4,120),(6.8,120),(6.8,123.5),(-6.8,123.5),(-6.8,120)],.45,4),201,207,'blue',axis='Y',r=.15)
 for side in (-1,1):
  a,b=sorted((side*8.2,side*14.2))
  button=lathe('Sight_SliderButton'+str(side),[(a,0),(a,3.0),(a+.35,3.6),(b-.35,3.6),(b,3.1),(b,0)],'blue',axis='X',center=(204,122.5),nseg=24)
  # The button's small grooves belong in the source normal, not extra rings.
  for dy in (-1.5,0,1.5):
   x=side*14.15
   detail=box('HIGH_ButtonGroove',(min(x,x+side*.15),203.8+dy,120),(max(x,x+side*.15),204.1+dy,125),'blue',register=False,r=0)
   source(detail,button.name)
 lathe('Sight_RearPivot',[(-12.5,0),(-12.5,2.1),(-10,2.4),(10,2.4),(12.5,2.1),(12.5,0)],'blue',axis='X',center=(248,121),nseg=24)
 spring=M.bezier((193,116.0),(204,117.8),(225,120),(245,117.8),20)
 ribbon('Sight_LeafSpring',spring,9,.8,edge=.12)
 # Etched graduation bars: high only, projected to the original leaf below.
 for y in range(212,247,4):
  for side in (-1,1):
   z=124-(y-188)/63
   ob=box('HIGH_Graduation',(2.5 if side>0 else -6,y,z-.08),(6 if side>0 else -2.5,y+.35,z+.08),'blue',register=False,r=0)
   source(ob,'Sight_TangentLeaf')
 from kit.fonts import find_font
 font=bpy.data.fonts.load(find_font('Noto Sans','Regular'))
 for i,y in enumerate(range(213,247,7)):
  for x in (-3.6,3.6):
   curve=bpy.data.curves.new('Original tangent numeral','FONT');curve.body=str(1+i*2);curve.size=2.4
   curve.font=font;curve.align_x='CENTER';curve.extrude=.055;curve.resolution_u=3
   ob=bpy.data.objects.new('HIGH_SightNumeral',curve);bpy.context.collection.objects.link(ob)
   ob.location=(x,y,124-(y-188)/63+.03)
   bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH')
   ob=bpy.context.object;ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
   source(ob,'Sight_TangentLeaf');ob.select_set(False)
 # Front collar and tower are a single rounded forging. Each Z station changes
 # depth and width rather than extruding a side silhouette.
 loops=[]
 for z,w,d,y in [(84,21,23,552),(88,22,23,552),(94,20,22,552),
                 (100,17,18,552),(109,15,15,552),(116,17.8,14,552),
                 (120,18.5,13,552),(122,18,12,552)]:
  loops.append([(x,y+v,z) for x,v in rounded(w,d,min(3.7,w/4),5)])
 tower=M.loft('Sight_FrontTower',loops,MAT['blue'])
 collar=lathe('Front collar union',[(543,0),(543,10),(545,11.7),(558,11.7),(562,10),(562,0)],'blue',center=(0,BORE),nseg=40,register=False)
 M.boolean(tower,collar,'UNION')
 soften_forging(tower,.4)
 cut(tower,lathe('Barrel exterior clearance',[(540,0),(540,7.3),(565,7.3),(565,0)],'blue',center=(0,BORE),nseg=40,register=False))
 cutbox(tower,(-14,548,95),(14,556,106),r=2.8)
 M.bevel(tower,.35,2);M.apply(tower);sculpt(tower,1200,level=0)
 # Open protective ears: the upper arc is genuinely absent, with rounded ends.
 loops=[]
 for i in range(57):
  a=math.radians(140+260*i/56)
  loops.append([(r*math.cos(a),y,128+r*math.sin(a)) for r,y in [(9.3,548),(11.2,548),(11.8,549),(11.8,555),(11.2,556),(9.3,556)]])
 reg(M.loft('Sight_FrontHood',loops,MAT['blue']),radius=.25)
 # Decorative thread witness rings carry no operative thread pitch/fit model.
 lathe('Sight_FrontPost',[(117,0),(117,1.8),(120,1.8),(122,1.35),(127.7,.8),(128,.7),(128,0)],'blue',axis='Z',center=(0,552),nseg=20)
 for z in (122.1,123,123.9):
  lathe('Sight_PostThreadWitness',[(z,1.15),(z,1.55),(z+.3,1.55),(z+.3,1.15)],'blue',axis='Z',center=(0,552),nseg=20,closed=True)
 drum=lathe('Sight_WindageDrum',[(-11,0),(-11,4.1),(-10.3,4.7),(10.3,4.7),(11,4.1),(11,0)],'blue',axis='X',center=(552,117),nseg=28,register=False)
 cutbox(drum,(-12,546,120.5),(12,558,124));cutbox(drum,(-12,546,110),(12,558,113.5));reg(drum,radius=.2)
 # Supported rod seat and a rounded lug below the collar, joined by a saddle.
 seat=profile('Sight_RodSeat',M.fillet_polygon([(-7,69),(-6,75),(6,75),(7,69),(5,62),(-5,62)],1.2,4),547,559,'blue',axis='Y',r=.5,register=False)
 cut(seat,lathe('Rod seat clearance',[(544,0),(544,2.9),(562,2.9),(562,0)],'blue',center=(0,66),nseg=20,register=False));reg(seat,radius=.3)

def receiver_sources():
 """Fine exterior pin, spring-end and stamping detail for normal projection."""
 for side in (-1,1):
  for y,z in [(41,59),(74,61)]:
   # Heads are on the exterior sheet; their fine recesses are bake sources.
   a,b=sorted((side*17.35,side*18.15))
   ob=lathe('HIGH_TriggerPin',[(a,0),(a,2.1),(b,2.4),(b,0)],'paint',axis='X',center=(y,z),nseg=32,register=False)
   source(ob,'Receiver_Sheet')
  for y in (43,75):
   pts=[(side*17.8,y-3,57.2),(side*17.95,y,57.5),(side*17.8,y+3.5,59.7)]
   source(M.tube('HIGH_RetainingEnd',pts,.35,MAT['paint'],sides=12),'Receiver_Sheet')
  # A shallow oval stamped shoulder sharpens the existing guide-dimple mouth.
  loops=[]
  for x,w,h in [(side*17.45,26,10),(side*17.85,24,8),(side*17.45,21.7,6.6)]:
   loops.append([(x,143+y,57+z) for y,z in rounded(w,h,3,10)])
  source(M.loft('HIGH_DimpleShoulder',loops,MAT['paint'],caps=False),'Receiver_Sheet')

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
 lug=profile('Magazine_FrontLug',M.fillet_polygon([(162,62),(164,62),(166,65),(166,69),(162,70),(161.5,67)],.6,4),-5,5,'blue','Magazine',r=.2,register=False)
 nose=lathe('Rounded visual hook nose',[(-5,0),(-5,2.2),(5,2.2),(5,0)],'blue',axis='X',center=(166,67),nseg=24,register=False)
 M.boolean(lug,nose,'UNION');reg(lug,'Magazine',radius=.15)
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

def visible_seating():
 # A visible open cradle joins the receiver walls. Its round contact land
 # follows the authored rock pivot; no operable retention mechanism is modeled.
 outer=[(166+4.3*math.cos(t),67+4.3*math.sin(t)) for t in [math.radians(90*i/18) for i in range(19)]]
 inner=[(166+2.2*math.cos(t),67+2.2*math.sin(t)) for t in [math.radians(90-90*i/18) for i in range(19)]]
 lip=profile('Receiver_FrontLugSlot',outer+inner,-5.8,5.8,'blue',r=.12,register=False)
 cutbox(lip,(-1.2,164,61),(1.2,172,74),r=.15);reg(lip)
 for side in (-1,1):
  a,b=sorted((side*5.6,side*17.5))
  profile('Receiver_FrontLugBridge'+str(side),M.fillet_polygon([(169,63),(175,63),(177,76),(171,76)],.8,4),a,b,'blue',r=.3)

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
