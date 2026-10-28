"""Relay 9: original scripted visual game prop, authored in millimeters.

Only photographs and exterior published envelopes inform the design. Hidden
surfaces clear visible animation; no functional engineering, firing components,
roller geometry, tolerance model or manufacturing drawings are supplied.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from guns.common.ammo9_visual import cartridge
from clips import build_clips
PARTS=[];HIGH=[];MAT={}
BORE=95.;MUZZLE=400.;BREECH=175.;EYE=148.;CH_Y=301.
HEADS={'Root':(0,0,0),'Bolt':(0,140,95),'ChargingHandle':(0,CH_Y,122),
 'Trigger':(0,59,44),'Selector':(0,3,57),'MagRelease':(0,116,43),'MagCatch':(0,111,51.5),
 'Magazine':(0,143,80),'Follower':(0,145.6,58.8),
 'TopRound':(4.4,128,80),'SecondRound':(-4.4,128,75.3),'ThirdRound':(4.4,129,63.5),
 'ChamberRound':(0,175,95),'RearDrum':(0,.5,133)}
SOCKETS={'Socket_Muzzle':(0,MUZZLE,BORE),'Socket_Foregrip':(-17,265,80),
 'Socket_Butt':(0,-280,50),'Socket_Eye':(0,-65,EYE),'Socket_Ejection':(19,112,108),
 'Socket_MagWell':(0,151,43),'Socket_Magazine':HEADS['Magazine'],
 'Socket_ChargingHandle':(-25,CH_Y,122)}

def material(k,c,metal,rough):
 m=bpy.data.materials.new('CP_'+k);m.use_nodes=True;m.diffuse_color=(*c,1)
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1)
 p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if k in ('polymer','rubber'):p.inputs['Specular IOR Level'].default_value=.28
 return m

def materials():
 for k,c,m,r in [('paint',(.018,.020,.022),.58,.38),('polymer',(.008,.008,.0075),0,.5),
  ('rubber',(.006,.006,.006),0,.7),('steel',(.23,.24,.25),1,.32),
  ('darksteel',(.036,.039,.041),.9,.39),('brass',(.48,.30,.09),1,.3),
  ('copper',(.48,.19,.09),1,.3),('primer',(.35,.32,.25),1,.34),
  ('follower',(.045,.05,.048),0,.5)]:MAT[k]=material(k,c,m,r)

def reg(o,bone='Root',radius=0,segments=3):
 if radius:
  M.bevel(o,radius,segments);wn=o.modifiers.new('Manufactured normals','WEIGHTED_NORMAL');wn.keep_sharp=True
 M.smooth(o,42);M.apply(o);o['asset_set']='SMG';o['bone']=bone;o['part_name']=o.name
 PARTS.append(o);return o

def box(name,lo,hi,mat='paint',bone='Root',radius=.35,segments=3,register=True):
 a,b=Vector(lo),Vector(hi);o=M.box(name,(a+b)/2,b-a,MAT[mat],0);M.apply(o)
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 return reg(o,bone,radius,segments) if register else o

def profile(name,points,lo,hi,mat='paint',bone='Root',axis='X',radius=.25,register=True):
 o=M.profile(name,points,lo,hi,MAT[mat],axis=axis)
 return reg(o,bone,radius) if register else o

def lathe(name,points,mat='paint',bone='Root',axis='Y',center=(0,0),n=48,closed=False,register=True):
 o=M.lathe(name,points,MAT[mat],segments=n,axis=axis,center=center,closed=closed)
 return reg(o,bone) if register else o

def cut(o,tool,operation='DIFFERENCE'):
 tool.data.materials.clear();tool.data.materials.append(o.data.materials[0]);M.boolean(o,tool,operation)
 return o

def cutbox(o,lo,hi):return cut(o,box('tool',lo,hi,register=False))
def rounded(w,h,r,n=6):return M.rounded_rectangle(w,h,r,n)
def reduce(o,target):
 count=sum(len(f.vertices)-2 for f in o.data.polygons)
 if count>target:
  d=o.modifiers.new('Game silhouette budget','DECIMATE');d.ratio=target/count;M.apply(o)
 return o

def subd(o,level):
 s=o.modifiers.new('Compound molding cage','SUBSURF');s.levels=s.render_levels=level;M.apply(o);return o

def sculpt_copy(o,target):
 h=o.copy();h.data=o.data.copy();bpy.context.collection.objects.link(h);h.name='HIGH_'+o.name
 h['bake_only']=True;h['low_target']=o.name;h['bone']='Root';h['asset_set']='SMG'
 HIGH.append(h);reduce(o,target)
 transfer=o.modifiers.new('Dense sculpt normal field','DATA_TRANSFER');transfer.object=h
 transfer.use_loop_data=True;transfer.data_types_loops={'CUSTOM_NORMAL'};transfer.loop_mapping='POLYINTERP_NEAREST';M.apply(o)
 return o

def pin(name,y,z,half=18,r=2.7,bone='Root'):
 for s in (-1,1):
  a,b=sorted((s*(half-.35),s*(half+.35)))
  lathe(name+('_L' if s<0 else '_R'),[(a,0),(a,r-.25),(a+.12,r),(b-.12,r),(b,r-.25),(b,0)],
        'darksteel',bone,axis='X',center=(y,z),n=24)

# A rolled sheet section. The raised rails are continuous deformations of its
# skin; they are not bars stuck onto a box. The return/cavity is separately cut.
def receiver_loop(y,inside=False):
 # Tight sheet bends and broad planar lands; the inside follows the presses.
 fade=max(0,min(1,(y+40)/12,(190-y)/14))
 wall=1.25 if inside else 0
 side=[(15.0,74),(16.4,75.5),(16.4,83.3),(16.8,84.2),
  (16.4+3.5*fade,85.8),(16.4+3.5*fade,89.4),(16.9,90.8),
  (16.4,91.8),(16.4,100.2),(16.9,101.1),(16.4+3.2*fade,102.5),
  (16.4+3.2*fade,106.2),(16.9,107.5),(16.7,109),(16.7,110.5)]
 if inside:side=[(x-wall,z+(1.25 if z<76 else 0)) for x,z in side]
 roof=[((16.7-wall)*math.cos(t),110.5+(20.5-wall)*math.sin(t))
       for t in [math.pi*i/28 for i in range(29)]]
 section=side+roof[1:]+[(-x,z) for x,z in reversed(side[:-1])]
 return [(x,y,z) for x,z in section]

def receiver():
 ys=[-40,-39,-28,176,189,190]
 o=M.loft('Receiver_Shell',[receiver_loop(y) for y in ys],MAT['paint'])
 cut(o,M.loft('Receiver cavity',[receiver_loop(y,True) for y in (-37,-28,176,187)],MAT['paint']))
 port=[(y+112,z+111) for y,z in rounded(44,18,5,8)]
 cut(o,profile('port tool',port,13,24,register=False))
 # Lower magazine throat and open chamber-side visual passage.
 cutbox(o,(-12.0,120,64),(12.0,167,99))
 cut(o,lathe('barrel bore tool',[(172,0),(172,9.3),(195,9.3),(195,0)],center=(0,BORE),n=48,register=False))
 reg(o,radius=.22,segments=1)
 # Welded sheet magazine well, flared only at its folded lower mouth.
 loops=[]
 for z,w,d,yc in [(38,34.0,46.5,148.8),(39.2,33.2,45.8,148.6),(44,31.2,42.5,147.7),(72,29.8,41,144.0),(83,29.5,40,142.6)]:
  loops.append([(x,y+yc,z) for x,y in rounded(w,d,3.0,7)])
 well=M.loft('MagazineWell_Shell',loops,MAT['paint'])
 inner=[]
 for z,yc in [(35,149.4),(44,147.7),(72,144.0),(86,142.28)]:
  inner.append([(x,y+yc,z) for x,y in rounded(27.4,38.3,2.2,7)])
 cut(well,M.loft('well inner tool',inner,MAT['paint']))
 # The catch has a real window in the right wall.
 cutbox(well,(-20,109,46),(-13.7,148,56));cutbox(well,(-18,138,47),(-10.5,148,56));reg(well,radius=.3,segments=2)
 for s in (-1,1):
  # A shallow stamped swage follows the well's sloping sides.
  pad=profile('Well_PressedSwage'+str(s),M.fillet_polygon([(132,48),(163,45),(163,67),(132,70)],3,5),
              13.0,14.1,'paint',register=False)
  for v in pad.data.vertices:v.co.x*=s

  if s<0:cutbox(pad,(-20,109,46),(-13.7,148,56));cutbox(pad,(-18,137.8,47),(-10,148,56))
  reg(pad,radius=.4)
 # Narrow closure seam and intermittent weld spots on the lower flange.
 reg(M.tube('Receiver_FoldSeam',[(0,y,74) for y in (-36,-15,0,50,100,119)],.48,MAT['paint'],sides=6))
 for y in (-47,-12,29,75,111,176):
  for s in (-1,1):
   a,b=sorted((s*17.35,s*17.85))
   lathe('Receiver_SpotWeld',[(a,0),(a,1.35),(b,1.5),(b,0)],'paint',axis='X',center=(y,79.5),n=12)
 pin('Rear_LockingPin',-25,66,18,2.8)
 lathe('Rear_PinShaft',[(-18,0),(-18,2.4),(18,2.4),(18,0)],'darksteel',axis='X',center=(-25,66),n=16)
 pin('Lower_FrontPin',119,56,15.1,2.3)
 # Chamber seat only: a visible ring and an empty bore, not engineered internals.
 lathe('Chamber_Seat',[(175,5.05),(175,10.1),(190,10.1),(190,5.05)],'darksteel',center=(0,BORE),n=40,closed=True)


def barrel_and_tube():
 lathe('Barrel',[(BREECH,5.05),(BREECH,9.1),(190,9.1),(202,8.4),(367,8.1),
  (375,8.1),(375.6,7.7),(398.8,7.7),(400,7.25),(400,5.0),(399.3,4.55),(385,4.5),(195,4.55),(194,5.05)],
  'darksteel',center=(0,BORE),n=40,closed=True)
 # Original shoulder collar, no copied product muzzle interface.
 lathe('Muzzle_Collar',[(369,7.9),(369,10.0),(371,10.8),(374,10.8),(376,9.4),(376,7.9)],
       'paint',center=(0,BORE),n=48,closed=True)
 tube=lathe('Cocking_Tube',[(179,8.3),(179,9.5),(354,9.5),(354,8.3)],center=(0,122),n=64,closed=True,register=False)
 # Slot and raised locking branch are cut through the actual rolled wall.
 cutbox(tube,(-15,214.5,120.1),(-6.0,310,123.9))
 for angle in (8,16,24,32,40):
  tool=box('notch tool',(-17,214.5,120.0),(-6,224.5,124.0),register=False)
  tool.data.transform(Matrix.Translation((0,0,122))@Matrix.Rotation(math.radians(angle),4,'Y')@Matrix.Translation((0,0,-122)))
  cut(tube,tool)
 reg(tube,radius=.22,segments=2)
 lathe('Cocking_FrontCap',[(352.5,0),(352.5,9.25),(355,9.25),(355.7,8.4),(355.7,0)],center=(0,122),n=48)
 # A bridge weld attaches the tube to the receiver at the rear, visibly supported.
 reg(M.tube('Tube_RearWeld',[(8.9*math.cos(t),183,122+8.9*math.sin(t)) for t in [math.tau*i/40 for i in range(41)]],.6,MAT['paint'],sides=6))
 # Internal visual slider and substantial hinged handle. It does not move on fire.
 lathe('Handle_Collar',[(297,0),(297,7.8),(307,7.8),(307,0)],'darksteel','ChargingHandle',center=(0,122),n=32)
 box('Handle_Stem',(-22,298.5,120.5),(-6.3,303.5,123.5),'darksteel','ChargingHandle',radius=.4)
 loops=[]
 for x,w,h in [(-30.5,3,3),(-30,5.7,4.9),(-28.5,6.8,5.5),(-24,6.8,5.5),(-22,5.8,4.8),(-21.5,3.0,3)]:
  loops.append([(x,301+y,122+z) for y,z in rounded(w*2,h*2,min(w,h)*.8,6)])
 grip=M.loft('Handle_Grip',loops,MAT['polymer']);subd(grip,1);reg(grip,'ChargingHandle')
 lathe('Handle_Hinge',[(-22.5,0),(-22.5,1.6),(-21.8,1.6),(-21.8,0)],'darksteel','ChargingHandle',axis='X',center=(301,122),n=20)
 # Bolt's visible surfaces only; hidden roller/fire-control engineering omitted.
 bolt=lathe('Bolt_Body',[(83,0),(83,11.1),(86,12.0),(167,12),(174.7,10.9),(174.7,0)],
  'darksteel','Bolt',center=(0,BORE),n=40,register=False)
 cutbox(bolt,(-13,75,81),(13,176,89.8));reg(bolt,'Bolt',radius=.3)
 # Port cheek with machined edge, and a front face meeting the chamber ring.
 cheek=box('Bolt_PortCheek',(9.2,86,100),(14.3,170,116),'steel','Bolt',radius=1.0,segments=4)
 lathe('Bolt_Face',[(174.7,0),(174.7,10.7),(175,10.7),(175,0)],'steel','Bolt',center=(0,BORE),n=40)
 # Recess representing the visible extractor, rather than a floating wire control.
 profile('Bolt_Extractor',M.fillet_polygon([(157,93),(174.6,93),(174.6,98),(162,99)],1,5),
  9.0,11.6,'darksteel','Bolt',radius=.35)


def sights():
 lathe('Sight_FrontBarrelBand',[(354,8.3),(354,11.7),(366,11.7),(366,8.3)],center=(0,BORE),n=36,closed=True)
 # Welded front tower embraces the barrel and the separate cocking-tube cap.
 base=profile('Sight_FrontTower',M.fillet_polygon([(-10,97),(10,97),(9,124),(5.8,139),(-5.8,139),(-9,124)],2,7),
  354,366,axis='Y',register=False)
 cut(base,lathe('tower barrel tool',[(352,0),(352,8.3),(368,8.3),(368,0)],center=(0,BORE),n=48,register=False))
 cut(base,lathe('tower tube tool',[(352,0),(352,9.7),(361,9.7),(361,0)],center=(0,122),n=48,register=False))
 reg(base,radius=.65,segments=4)
 lathe('Sight_FrontHood',[(359,12.5),(359,14.9),(359.6,15.5),(365.4,15.5),(366,14.9),(366,12.5)],
  center=(0,EYE),n=72,closed=True)
 post=profile('Sight_FrontPost',[(-2.0,133),(-1.4,EYE),(1.4,EYE),(2,133)],361,364,'darksteel',axis='Y',radius=.18)
 for side in (-1,1):
  reg(M.tube('Sight_FrontWeld',[(side*8.1,yy,133.7) for yy in (356,359,363,366)],.65,MAT['paint'],sides=7))
 # Rear saddle welded onto the rolled crown; fine adjusting slots stay geometry
 # for this form checkpoint, and can move to the bake later.
 base=box('Sight_RearSaddle',(-14,-35,127),(14,4,133),'paint',radius=2.0,segments=5)
 cut(base,lathe('saddle crown tool',[(-38,0),(-38,19.9),(6,19.9),(6,0)],center=(0,110.5),n=64,register=False))
 box('Sight_RearBase',(-18.2,-28,131),(18.2,-1,133.5),'darksteel',radius=1.3,segments=4)
 # Closed roof, hollow underside on the bearing. Apertures pierce the skirt;
 # the concealed front exit is relieved so the hood is not occluded by wall two.
 drum=lathe('Sight_RearDrum',[(135,8.8),(135,12.5),(137,13),
  (154.5,11.8),(155.5,11.2),(155.5,0),(153,0),(153,8.4)],
  'paint','RearDrum',axis='Z',center=(0,-14),n=48,closed=True,register=False)
 drum.data.transform(Matrix.Translation((0,-14,133))@Matrix.Rotation(math.radians(16),4,'X')@Matrix.Translation((0,14,-133)))
 cut(drum,lathe('selected aperture tool',[(-37,0),(-37,1.9),(-19,1.9),(-19,0)],center=(0,EYE),n=32,register=False))
 cut(drum,lathe('forward optical exit tool',[(-12,0),(-12,5.0),(8,5.0),(8,0)],center=(0,EYE),n=32,register=False))
 for side,r in [(-1,1.25),(1,1.55)]:
  a,b=sorted((side*6,side*18))
  cut(drum,lathe('side aperture tool',[(a,0),(a,r),(b,r),(b,0)],axis='X',center=(-14,147),n=24,register=False))
 reg(drum,'RearDrum',radius=.15,segments=2)
 drum['detent_degrees']='0,90,180,270';drum['axis_tilt_degrees']=16
 # Split clamp ears with slotted, recessed screw heads, not a plain seat box.
 for side in (-1,1):
  a,b=sorted((side*13.8,side*18.2))
  ear=box('Sight_ClampEar', (a,-27,132),(b,-3,135.8),'darksteel',radius=.65,register=False)
  cutbox(ear,(a-.1,-16,134.6),(b+.1,-15.3,137));reg(ear)
  screw=lathe('Sight_ClampScrew',[(135.7,0),(135.7,2.2),(136.4,2.2),(136.6,1.9),(136.6,0)],
   'steel',axis='Z',center=(side*15.6,-21),n=24,register=False)
  cutbox(screw,(side*15.6-.4,-24,136.1),(side*15.6+.4,-18,138));reg(screw)
 # Clearance for the inclined drum, and a concentric visible bearing sleeve.
 for seatname in ('Sight_RearSaddle','Sight_RearBase'):
  tool=lathe('drum seat tool',[(128,0),(128,13.3),(145,13.3),(145,0)],axis='Z',center=(0,-14),n=48,register=False)
  tool.data.transform(Matrix.Translation((0,-14,133))@Matrix.Rotation(math.radians(16),4,'X')@Matrix.Translation((0,14,-133)))
  cut(bpy.data.objects[seatname],tool)
 bearing=lathe('Sight_RearBearing',[(131,0),(131,8.5),(137.5,8.5),(137.5,0)],'darksteel',axis='Z',center=(0,-14),n=32)
 bearing.data.transform(Matrix.Translation((0,-14,133))@Matrix.Rotation(math.radians(16),4,'X')@Matrix.Translation((0,14,-133)))
 # Low shoulders, protected adjustment screw and visible split seating line.
 pin('Sight_Adjustment',-14,134,13.0,2.0)
 for yy in (-28,-3):
  reg(M.tube('Sight_RearWeld',[(x,yy,130.4) for x in (-10,-5,0,5,10)],.5,MAT['paint'],sides=6))


def super_loop(axis,a,hw,low,high,n=40,power=2.5,center=0):
 loop=[]
 for i in range(n):
  t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
  x=hw*math.copysign(abs(c)**(2/power),c)
  v=(high+low)/2+(high-low)/2*math.copysign(abs(s)**(2/power),s)
  if axis=='Y':loop.append((x,a,v))
  else:loop.append((x,center+v,a))
 return loop


def furniture():
 # Independent width, comb, belly and end support rows: compound stock cage.
 rows=[(-273,19.4,-7,107),(-272.3,19.8,-7,107),(-267,20.1,-6,107.3),
  (-247,20.0,0,107.8),(-218,19.5,14,108.4),(-188,18.1,30,109),
  (-160,16.6,45,109.5),(-136,15.9,57,110.5),(-116,15.5,66,113),
  (-101,15.8,70,117),(-91,16.8,71.6,122),(-82,18,72,129),
  (-73,18.4,72.5,133),(-67,18.4,73,133.4),(-66.2,18.1,73,133.3)]
 rows=[(y+25*max(0,min(1,(y+150)/83.8)),w,b,t) for y,w,b,t in rows]
 stock=M.loft('Stock_Mold',[super_loop('Y',*r,n=40,power=2.55) for r in rows],MAT['polymer']);subd(stock,2)
 M.smooth(stock,60);sculpt_copy(stock,3100);reg(stock)
 padrows=[(-280,19.2,-6.2,106.4),(-279.5,19.8,-7,107),(-278.2,20.0,-7.3,107.3),(-273.5,20.0,-7.3,107.3),(-273,19.6,-7,107)]
 pad=M.loft('Stock_Buttplate',[super_loop('Y',*r,n=40,power=2.55) for r in padrows],MAT['rubber']);subd(pad,1);reg(pad)
 for z in (12,89):lathe('Stock_Screw',[(-280.1,0),(-280.1,2.1),(-279.3,2.1),(-279.3,0)],'darksteel',center=(0,z),n=20)
 # Cast sling inset: a real open slot with a molded surround, not a painted oval.
 sling=box('Stock_SlingSurround',(-21,-247,37),(-18,-211,63),'polymer',radius=4,segments=6,register=False)
 cut(sling,box('sling slot tool',(-23,-229,42),(-16,-223,58),radius=1,register=False));reg(sling,radius=.5)
 for yy in (-240,-217):lathe('Stock_SlingRivet',[(-21.3,0),(-21.3,2),(-20.5,2),(-20.5,0)],'darksteel',axis='X',center=(yy,50),n=20)
 # Slim U section, sculpted nose/rear shoulders, real barrel-clearance channel.
 rows=[(185,16.0,67,111),(185.8,17.7,66.7,111.3),(188,17.7,66.7,111.3),
  (189,16.8,66.8,111),(192,17.3,66.5,111.4),
  (202,17.0,67.0,111),(235,16.5,69,110),(275,16.0,71.5,109),
  (317,15.4,74,108),(341,14.6,75.5,107.3),(348,13.6,77,106.5),(349,13.2,77.3,106.2)]
 def hand_section(y,hw,bottom,top):
  # Oval inner and outer arcs give a full-radius U with actual polymer gauge.
  # The old near-flat flank and circular shallow channel read as a slab.
  cz=95.;rz=cz-bottom;alpha=math.asin((top-cz)/rz)
  start=math.pi-alpha;end=math.tau+alpha
  outer=[(hw*math.cos(t),cz+rz*math.sin(t)) for t in [start+(end-start)*j/40 for j in range(41)]]
  iw=hw-3.2;ir=rz-3.2;beta=math.asin((top-cz)/ir)
  inner=[(iw*math.cos(t),cz+ir*math.sin(t)) for t in [beta-(math.pi+2*beta)*j/40 for j in range(41)]]
  return [(x,y,z) for x,z in outer+inner]
 hand=M.loft('Handguard_Mold',[hand_section(*r) for r in rows],MAT['polymer'],caps=False);subd(hand,2)
 # Cap the concave U only after subdivision: a Catmull-Clark ngon cap would
 # stretch a web across the barrel channel. The end faces are true U sections.
 bm=bmesh.new();bm.from_mesh(hand.data)
 bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(hand.data);bm.free()
 M.bevel(hand,.4,3);M.apply(hand)
 M.smooth(hand,65);sculpt_copy(hand,2700);reg(hand)
 pin('Handguard_Pin',340,90,14.9,2.8)
 # A circular molded pin surround follows the real curved game surface.
 # Author in final furniture coordinates, then compensate for the shared
 # pin shift applied below. The previous surround applied that shift twice.
 from mathutils.bvhtree import BVHTree
 tree=BVHTree.FromObject(hand,bpy.context.evaluated_depsgraph_get())
 for side in (-1,1):
  loops=[];n=32
  for r,lift in [(4.9,-.1),(4.9,.05),(4.65,.20),(3.2,.20),(3.0,.05),(3.0,-.1)]:
   row=[]
   for i in range(n):
    theta=math.tau*i/n;fy=318+r*math.cos(theta);z=90+r*math.sin(theta)
    sy=185+(fy-185)*164/142
    hit=tree.ray_cast(Vector((side*30,sy,z)),Vector((-side,0,0)),40);assert hit[0] is not None
    row.append((hit[0].x+side*lift,fy+22,z))
   loops.append(row)
  vs=[v for row in loops for v in row]
  fs=[(j*n+i,j*n+(i+1)%n,((j+1)%len(loops))*n+(i+1)%n,((j+1)%len(loops))*n+i)
      for j in range(len(loops)) for i in range(n)]
  reg(M.mesh('Handguard_PinSurround',vs,fs,MAT['polymer']))
 # Sleeved feet at each end establish support without hidden dense machinery.
 for y in (193,333):
  lathe('Handguard_Bearing',[(y,8.55),(y,10.5),(y+5,10.5),(y+5,8.55)],
        'darksteel',center=(0,BORE),n=32,closed=True)


def grip_panels(lower):
 # Generated molded panel relief. Fine pebbling exists only in the retained
 # dense source; the low patch carries its silhouette/border for the later bake.
 from mathutils.bvhtree import BVHTree
 from mathutils import noise
 tree=BVHTree.FromObject(lower,bpy.context.evaluated_depsgraph_get())
 outline=rounded(34,68,7,6)
 def make(side,nrings,detail):
  if detail:
   # Uniform physical spacing avoids radial spokes/long straight-edge quads
   # aliasing molding grain into scratches. Only this dense source carries it.
   nu,nz=96,192;vertices=[];faces=[]
   for k in range(nz+1):
    v=-34+68*k/nz;corner=max(0,abs(v)-27)
    span=10+math.sqrt(max(0,49-corner*corner))
    for j in range(nu+1):
     u=-span+2*span*j/nu;z=-15+v;y=.5*z-3+u
     hit=tree.ray_cast(Vector((side*30,y,z)),Vector((-side,0,0)),40);assert hit[0] is not None
     edge=min(1,(span-abs(u))/1.5,(34-abs(v))/1.5)
     relief=.12*noise.noise(Vector((y*.9,z*.9,side*7.1)))
     vertices.append((hit[0].x+side*(.20+relief*edge),y,z))
   for k in range(nz):
    for j in range(nu):
     q=k*(nu+1)+j;faces.append((q,q+1,q+nu+2,q+nu+1))
   border=[*range(nu+1),*[k*(nu+1)+nu for k in range(1,nz+1)],
    *range(nz*(nu+1)+nu-1,nz*(nu+1)-1,-1),*[k*(nu+1) for k in range(nz-1,0,-1)]]
   start=len(vertices)
   for i in border:
    x,y,z=vertices[i];vertices.append((x-side*.15,y,z))
   for j,i in enumerate(border):faces.append((i,border[(j+1)%len(border)],start+(j+1)%len(border),start+j))
   faces.append(tuple(reversed(range(start,start+len(border)))))
   return M.mesh('HIGH_Grip_TexturePanel'+str(side),vertices,faces,MAT['polymer'])
  contour=outline
  vertices=[];faces=[];n=len(contour)
  for k in range(nrings+1):
   radius=max(.001,k/nrings)
   for u,v in contour:
    z=-15+v*radius;y=.5*z-3+u*radius
    hit=tree.ray_cast(Vector((side*30,y,z)),Vector((-side,0,0)),40)
    assert hit[0] is not None,('panel projection',side,y,z)
    bump=0
    lip=.16+.12*math.sin(math.pi*min(1,radius))
    x=hit[0].x+side*(lip+bump*min(1,(1-radius)*12))
    vertices.append((x,y,z))
  for k in range(nrings):
   for j in range(n):faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
  faces.append(tuple(reversed(range(n))))
  # Back follows the same actual surface, closing a thin molded skin.
  start=len(vertices)
  for x,y,z in vertices[-n:]:vertices.append((x-side*.15,y,z))
  for j in range(n):faces.append((nrings*n+j,nrings*n+(j+1)%n,start+(j+1)%n,start+j))
  faces.append(tuple(range(start,start+n)))
  return M.mesh('Grip_TexturePanel'+str(side),vertices,faces,MAT['polymer'])
 for side in (-1,1):
  ob=make(side,3,False);reg(ob)
  hi=make(side,64,True);M.smooth(hi,60);hi['bake_only']=True;hi['low_target']=ob.name;hi['bone']='Root';hi['asset_set']='SMG';HIGH.append(hi)

def selector_marks(lower):
 # Original S / 1 / A legend and short arc, seated by rays on the sculpt.
 from mathutils.bvhtree import BVHTree
 from kit.fonts import find_font
 tree=BVHTree.FromObject(lower,bpy.context.evaluated_depsgraph_get())
 font=bpy.data.fonts.load(find_font('Noto Sans','Regular'))
 for side in (-1,1):
  points=[]
  for i in range(17):
   theta=math.radians(-55+96*i/16);y=3+11.5*math.sin(theta);z=57+11.5*math.cos(theta)
   h=tree.ray_cast(Vector((side*30,y,z)),Vector((-side,0,0)),40);assert h[0] is not None
   points.append((h[0].x+side*.08,y,z))
  reg(M.tube('Selector_MarkedArc'+str(side),points,.12,MAT['follower'],sides=4))
  for text,angle in [('S',34),('1',-8),('A',-49)]:
   theta=math.radians(angle);y=3+15*math.sin(theta);z=57+15*math.cos(theta)
   h=tree.ray_cast(Vector((side*30,y,z)),Vector((-side,0,0)),40);assert h[0] is not None
   curve=bpy.data.curves.new('Mode legend','FONT');curve.body=text;curve.font=font;curve.size=2.7;curve.align_x='CENTER';curve.align_y='CENTER';curve.extrude=.025;curve.resolution_u=1
   ob=bpy.data.objects.new('Selector_Mark_'+text+str(side),curve);bpy.context.collection.objects.link(ob)
   # Local font X follows +/-Y, font Y is +Z, normal faces the selected side.
   ob.matrix_world=Matrix(((0,0,side,h[0].x+side*.05),(side,0,0,y),(0,1,0,z),(0,0,0,1)))
   bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob=bpy.context.object
   ob.data.materials.append(MAT['follower']);M.apply(ob);ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
   bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001)
   bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();reg(ob)


def lower():
 # Supported subdivision sections make a flat-sided molded housing. The
 # sculpt union blends only its grip/guard roots, preserving broad side lands.
 rows=[(-54,14,42,73),(-53.5,15,41,74),(-48,16,40,74),
  (-28,16.6,38.5,74),(0,16.6,38,74),(30,16.2,39,74),
  (70,14.9,40,74),(103,13.5,42,74),(118,13.1,43,74),(120,12.8,44,73.5)]
 loops=[[(x,y,z+(b+t)/2) for x,z in rounded(w*2,t-b,1.35,4)] for y,w,b,t in rows]
 upper=M.loft('Lower_Mold',loops,MAT['polymer']);subd(upper,2)
 def merge(seed):cut(upper,seed,'UNION')
 griprows=[(-56,-24,16,24.5),(-55.3,-24,17.4,26),(-52,-24,18,27),
  (-43,-23,18.1,28),(-28,-14,18.8,28.8),(-10,-4,17.2,26.5),
  (8,7,16.2,24),(22,14,15.8,23),(34,16,16,27),(47,17,15.8,28),(57,14,14.5,26)]
 loops=[]
 for z,yc,hw,hd in griprows:
  loop=[]
  for i in range(48):
   t=math.tau*i/48;c=math.cos(t);sn=math.sin(t)
   x=hw*math.copysign(abs(sn)**(2/2.5),sn)
   yy=hd*math.copysign(abs(c)**(2/(3.0 if c>0 else 2.2)),c)
   x*=1-.07*max(0,c)**4;loop.append((x,yc+yy,z))
  loops.append(loop)
 grip=M.loft('palm seed',loops,MAT['polymer']);subd(grip,2);merge(grip)
 # Flat-faced, radiused rectangular guard section, molded into the housing.
 path=[]
 for args in [((24,40),(25,25),(28,16),(43,9)),((43,9),(58,1),(80,-2),(89,5)),
              ((89,5),(97,16),(100,34),(106,46))]:
  ps=M.bezier(*args,14);path.extend(ps if not path else ps[1:])
 loops=[]
 for i,(y,z) in enumerate(path):
  t=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized();n=Vector((-t.y,t.x))
  loops.append([(x,y+v*n.x,z+v*n.y) for x,v in rounded(16,6.5,1.2,4)])
 merge(M.loft('guard seed',loops,MAT['polymer']))
 rm=upper.modifiers.new('Sculpted continuous lower union','REMESH');rm.mode='VOXEL';rm.voxel_size=.55;rm.use_smooth_shade=True;M.apply(upper)
 sm=upper.modifiers.new('Palm web relaxation','SMOOTH');sm.factor=.40;sm.iterations=3;M.apply(upper)
 # Broad undercut, top seating land, selector hole and actual trigger clearance.
 cutbox(upper,(-25,-70,74),(25,130,95))
 cutbox(upper,(-4.5,47,19),(4.5,78,50))
 cutbox(upper,(-6.3,109,34),(6.3,125,52))
 cut(upper,lathe('paddle axle seat',[(-21,0),(-21,2.9),(21,2.9),(21,0)],axis='X',center=(116,43),n=32,register=False))
 cutbox(upper,(-18,108,46),(-13.7,122,56))
 cut(upper,lathe('button counterbore',[(10.3,0),(10.3,4.5),(21,4.5),(21,0)],axis='X',center=(111,51.5),n=40,register=False))
 cut(upper,lathe('catch rod seat',[(-21,0),(-21,2.2),(21,2.2),(21,0)],axis='X',center=(111,51.5),n=32,register=False))
 cut(upper,lathe('selector seat tool',[(-21,0),(-21,4.5),(21,4.5),(21,0)],axis='X',center=(3,57),n=48,register=False))
 rm=upper.modifiers.new('Rounded finished molded cavities','REMESH');rm.mode='VOXEL';rm.voxel_size=.40;rm.use_smooth_shade=True;M.apply(upper)
 sm=upper.modifiers.new('Finished mold radii','SMOOTH');sm.factor=.32;sm.iterations=2;M.apply(upper)
 M.smooth(upper,48);sculpt_copy(upper,5600);reg(upper)
 grip_panels(upper)
 selector_marks(upper)
 # Trigger is a curved shoe with a broad face, tapering toward its toe.
 front=M.bezier((72,44),(53,32),(52,23),(67,12),16)
 theta=math.atan2(16,11);cy=67-1.8*math.cos(theta);cz=12-1.8*math.sin(theta)
 toe=[(cy+1.8*math.cos(theta-math.pi*i/12),cz+1.8*math.sin(theta-math.pi*i/12)) for i in range(1,13)]
 back=M.bezier(toe[-1],(47,21),(47,32),(57,44),16)
 profile('Trigger_Shoe',front+toe+back[1:],-2.9,2.9,'darksteel','Trigger',radius=.55)
 # Selectors have a stem, flange and a shaped thumb pad seated on the frame.
 for side in (-1,1):
  a,b=sorted((side*16.65,side*18.1))
  lathe('Selector_Hub'+str(side),[(a,0),(a,5.7),(b,5.7),(b,0)],'darksteel','Selector',axis='X',center=(3,57),n=32)
  outline=M.fillet_polygon([(0,54),(6,54),(15,68),(12,73),(7,72)],2,7)
  a,b=sorted((side*17.5,side*20.0))
  lever=profile('Selector_Lever'+str(side),outline,a,b,'polymer','Selector',radius=.8)
  for v in lever.data.vertices:
   v.co.y=3+(v.co.y-3)*1.23;v.co.z=57+(v.co.z-57)*1.23
 lathe('Selector_Shaft',[(-17,0),(-17,3.8),(17,3.8),(17,0)],'darksteel','Selector',axis='X',center=(3,57),n=24)
 # Paddle and catch share their real cross-axis, distinct from the button.
 paddle=M.fillet_polygon([(111,43),(119,43),(123,24),(119,19),(115,20)],1.4,6)
 profile('MagazineRelease_Paddle',paddle,-5.0,5.0,'darksteel','MagRelease',radius=.5)
 lathe('MagazineRelease_Axle',[(-16,0),(-16,2.4),(16,2.4),(16,0)],'darksteel','MagRelease',axis='X',center=(116,43),n=24)
 # This catch tongue seats in the magazine's actual right-side catch window.
 box('MagazineRelease_Catch',(-14.0,138.7,48.5),(-10.8,146.5,54.8),'darksteel','MagCatch',radius=.2)
 # External button is a distinct pad linked visually to the catch stamping.
 lathe('MagazineRelease_Button',[(14.1,0),(14.1,4.1),(16.5,4.1),(17,3.7),(17,0)],
  'paint','MagCatch',axis='X',center=(111,51.5),n=32)
 profile('MagazineRelease_Link',M.fillet_polygon([(109,48),(143,49),(146,53),(141,54),(109,52)],.6,5),
  -15.5,-14.4,'darksteel','MagCatch',radius=.2)
 box('MagazineRelease_Bridge',(-15.6,140,50),(-13.6,144,53),'darksteel','MagCatch',radius=.2)
 lathe('MagazineRelease_Rod',[(-15.4,0),(-15.4,1.7),(15.7,1.7),(15.7,0)],
  'darksteel','MagCatch',axis='X',center=(111,51.5),n=20)



def mag_center(s):return 143+.12*s+.0016*max(0,s-20)**2

def magazine():
 # A curved sheet body, with real inside, rolled corners and integral press ribs.
 loops=[];inner=[]
 stations=[0,1,8,18,30,50,75,100,125,145,156,163,164]
 def section(w,d):
  ring=rounded(w,d,2.8,8);result=[]
  for p,q in zip(ring,ring[1:]+ring[:1]):
   result.append(p)
   if abs(p[0]-q[0])<1e-5 and abs(q[1]-p[1])>10:
    result.extend((p[0],p[1]+(q[1]-p[1])*j/25) for j in range(1,25))
  return result
 def loop(s,inside=False):
  yc=mag_center(s);z=80-s;w=22.7 if s<20 else 24.;d=34.5
  if inside:w-=1.6;d-=1.6
  ring=[]
  for x,y in section(w,d):
   crest=.7*math.exp(-((y-6)/2.1)**2)+.55*math.exp(-((y+8)/2.2)**2)
   fade=max(0,min(1,s/18,(164-s)/12))
   x+=math.copysign(crest*fade*max(0,(abs(x)-7.5)/4),x)
   ring.append((x,yc+y,z))
  return ring
 loops=[loop(s) for s in stations]
 body=M.loft('Magazine_Body',loops,MAT['paint'])
 # A continuous through-cavity with monotone stations; the slid-on floorplate
 # closes the bottom. The earlier folded last station made a false solid.
 cavity=[loop(s,True) for s in [-4,*stations,168]]
 cut(body,M.loft('magazine inner tool',cavity,MAT['paint']))
 cutbox(body,(-15,149,75),(15,180,88))
 cutbox(body,(-15,138.3,48.2),(-10.3,146.9,54.8))
 # Witness holes through the rear spine follow the actual curved surface.
 for s in (36,64,92,120,148):
  y=mag_center(s)-17.25
  cut(body,lathe('witness tool',[(y-3,0),(y-3,1.45),(y+3,1.45),(y+3,0)],center=(0,80-s),n=16,register=False))
 reg(body,'Magazine',radius=.18,segments=2)
 # Formed feed lips curl over staggered top cartridges. Their inner arcs meet
 # the cases at a small photographed visual support gap.
 for side,cx,zz in [(1,4.4,80),(-1,-4.4,75.3)]:
  angles=[math.radians(t) for t in (0,12,24,36,48,60,67)]
  arc=[(cx+side*5.0*math.cos(t),zz+5.0*math.sin(t)) for t in angles]
  outer=[(cx+side*5.65*math.cos(t),zz+5.65*math.sin(t)) for t in angles]
  pts=[(side*11.3,71),(side*11.3,78 if side>0 else 73),*outer,*reversed(arc),(side*10.5,71)]
  profile('Magazine_FeedLip'+str(side),pts,129.0,145.7,'darksteel','Magazine',axis='Y',radius=.10)
 # Thin slid-on floor plate, front toe, curled return and center retaining pad.
 yc=mag_center(165)
 loops=[[(x,y+yc,z) for x,y in rounded(w,d,3,8)] for z,w,d in [(-84.4,25.3,37),(-85.1,25.9,37.6),(-87.8,25.9,37.6),(-88.4,25.1,37.0)]]
 plate=M.loft('Magazine_Floorplate',loops,MAT['darksteel']);reg(plate,'Magazine',radius=.25)
 box('Magazine_PlateRetainer',(-3,yc-4,-88.6),(3,yc+4,-88.2),'paint','Magazine',radius=.12)
 # Three visible staggered rounds, not thirty hidden copies. Follower supports
 # the lowest display round; the rest of the opaque curved body stays empty.
 f=M.loft('Magazine_Follower',[[(x,y+145.6,z) for x,y in rounded(w,29.1,1.8,6)] for z,w in [(56.9,19.6),(57.6,19.2),(58.6,11.8)]],MAT['follower']);reg(f,'Follower',radius=.22)
 for name,bone,xyz,n in [('Magazine_TopRound','TopRound',HEADS['TopRound'],32),
  ('Magazine_SecondRound','SecondRound',HEADS['SecondRound'],28),('Magazine_ThirdRound','ThirdRound',HEADS['ThirdRound'],20),
  ('ChamberRound','ChamberRound',HEADS['ChamberRound'],16)]:cartridge(lathe,name,xyz,bone,sides=n)


def finalize(o):
 # Weld Boolean micro-edges in mm before meters; preserve the dense smooth field.
 normals=o.data.attributes.new('Authored normals','FLOAT_VECTOR','CORNER')
 for r,n in zip(normals.data,o.data.corner_normals):r.vector=n.vector
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0000001)
 bmesh.ops.dissolve_degenerate(bm,dist=.0000001,edges=list(bm.edges));bm.to_mesh(o.data);bm.free()
 ns=[r.vector[:] for r in o.data.attributes['Authored normals'].data]
 o.data.normals_split_custom_set(ns);o.data.attributes.remove(o.data.attributes['Authored normals'])
 tr=o.modifiers.new('Explicit checkpoint triangles','TRIANGULATE');tr.keep_custom_normals=True;M.apply(o)
 if o.name=='Receiver_Shell':
  # The triangulator can expose a duplicate nanometer-wide Boolean triangle
  # at the blind inner end. Weld it only on this steel shell, then retriangulate.
  keep=o.data.attributes.new('Steel corner field','FLOAT_VECTOR','CORNER')
  for r,n in zip(keep.data,o.data.corner_normals):r.vector=n.vector
  bm=bmesh.new();bm.from_mesh(o.data)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002)
  bmesh.ops.dissolve_degenerate(bm,dist=.00002,edges=list(bm.edges))
  boundary=[e for e in bm.edges if e.is_boundary]
  if boundary:
   assert sum(e.calc_length() for e in boundary)<2,'Unexpected receiver opening'
   fill=bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
   bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
  bm.to_mesh(o.data);bm.free()
  o.data.normals_split_custom_set([r.vector[:] for r in o.data.attributes['Steel corner field'].data]);o.data.attributes.remove(o.data.attributes['Steel corner field'])
  tr=o.modifiers.new('Repaired steel triangles','TRIANGULATE');tr.keep_custom_normals=True;M.apply(o)
 ns=[r.vector.copy() for r in o.data.corner_normals]
 drumxf=Matrix.Translation((0,.5,133))@Matrix.Rotation(math.radians(16),4,'X')@Matrix.Translation((0,0,-133))
 for f in o.data.polygons:
  for j in f.loop_indices:
   if ns[j].dot(f.normal)<.05:ns[j]=f.normal.copy()
   if o.name=='Receiver_Shell':
    v=o.data.vertices[o.data.loops[j].vertex_index].co
    q=(v.x/16.7)**2+((v.z-110.5)/20.5)**2
    if v.z>110.4 and .97<q<1.04:
     n=Vector((v.x/16.7**2,0,(v.z-110.5)/20.5**2)).normalized()
     if n.dot(f.normal)>.45:ns[j]=n
   if o.name=='Sight_RearDrum':
    v=drumxf.inverted()@o.data.vertices[o.data.loops[j].vertex_index].co
    r=math.hypot(v.x,v.y)
    if 136.8<v.z<157.2 and abs(r-(13-(v.z-137)*1.1/20))<.20:
     n=drumxf.to_3x3()@Vector((v.x/r,v.y/r,1.1/20)).normalized()
     if n.dot(f.normal)>.45:ns[j]=n
 o.data.transform(Matrix.Scale(.001,4));o.matrix_world=Matrix.Identity(4);o.data.update();o.data.normals_split_custom_set(ns)


def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/smg.blend')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);materials()
 receiver();barrel_and_tube();sights();furniture();lower();magazine()
 # The formed lower magazine follows its arc into a tilted floorplate.
 # Upper feed/catch geometry is unchanged. This removes the horizontal shelf
 # which the photographic side comparison exposed at the curved end.
 for o in PARTS:
  if o.get('bone')!='Magazine':continue
  if o.name=='Magazine_Body':
   for v in o.data.vertices:
    s=80-v.co.z
    if s<=125:continue
    center=mag_center(s);offset=v.co.y-center
    angle=math.atan(.12+.0032*max(0,s-20))*min(1,(s-125)/39)
    v.co.y=center+offset*math.cos(angle);v.co.z+=offset*math.sin(angle)
  elif o.name.startswith(('Magazine_Floorplate','Magazine_PlateRetainer')):
   pivot=Vector((0,mag_center(165),-86.4))
   o.data.transform(Matrix.Translation(pivot)@Matrix.Rotation(math.atan(.12+.0032*144),4,'X')@Matrix.Translation(-pivot))
 # Exterior proportional calibration: 340 mm between sight centers; shorten
 # the slim handguard to the photographed class's roughly 143 mm envelope.
 for o in PARTS:
  if o.name.startswith(('Sight_Front','Cocking_FrontCap')):
   o.data.transform(Matrix.Translation((0,-22,0)))
  if o.name=='Cocking_Tube':
   for v in o.data.vertices:
    if v.co.y>330:v.co.y-=22
  if o.name.startswith(('Sight_Rear','Sight_Adjustment','Sight_Clamp')):
   o.data.transform(Matrix.Translation((0,14.5,0)))
  if o.name=='Handguard_Mold':
   for v in o.data.vertices:v.co.y=185+(v.co.y-185)*142/164
  if o.name.startswith('Handguard_Pin'):o.data.transform(Matrix.Translation((0,-22,0)))
  if o.name.startswith('Handguard_Bearing'):
   # Both supporting sleeves stay inside the shortened polymer ends.
   if min(v.co.y for v in o.data.vertices)>300:o.data.transform(Matrix.Translation((0,-22,0)))
 for h in HIGH:
  if h.get('low_target')=='Handguard_Mold':
   for v in h.data.vertices:v.co.y=185+(v.co.y-185)*142/164
 targets={'Well_PressedSwage-1':300,'Well_PressedSwage1':200,'Magazine_Follower':300,'Bolt_Extractor':230,'Magazine_Body':2600,'Cocking_Tube':1700,
  'Sight_FrontTower':1200,'Barrel':850,'Stock_Buttplate':400,'MagazineWell_Shell':1000,
  'Handle_Grip':550,'Bolt_Body':650,'Magazine_Floorplate':300,'Sight_FrontHood':650,
  'Trigger_Shoe':620,'Muzzle_Collar':240,'Sight_RearSaddle':330,
  'Selector_Lever-1':300,'Selector_Lever1':300,'Tube_RearWeld':250,
  'Stock_SlingSurround':240,'MagazineRelease_Paddle':300,'MagazineRelease_Link':240,
  'Magazine_FeedLip1':330,'Magazine_FeedLip-1':330}
 for o in PARTS:
  if o.name in targets:reduce(o,targets[o.name])
  finalize(o)
 hc=bpy.data.collections.new('High_Sources');bpy.context.scene.collection.children.link(hc)
 for h in HIGH:
  h.data.transform(Matrix.Scale(.001,4))
  for c in list(h.users_collection):c.objects.unlink(h)
  hc.objects.link(h);h.hide_render=True;h.hide_set(True)
 arm=W.armature('SMGArmature',{k:tuple(v*.001 for v in pos) for k,pos in HEADS.items()},
  parents={**{n:'Magazine' for n in ('Follower','TopRound','SecondRound','ThirdRound')}})
 for o in PARTS:W.rigid_bind(o,arm,o['bone'])
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in pos) for k,pos in SOCKETS.items()},
  {'Socket_Magazine':'Magazine','Socket_ChargingHandle':'ChargingHandle'})
 build_clips(arm);W.pose(arm,'Idle',0)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['stage']='Form checkpoint / constant inspection materials / no look-dev'
 sc['maker']='Propane Defense';sc['model']='Relay 9';sc['interface_version']='1.3.0'
 sc['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 bpy.ops.wm.save_as_mainfile(filepath=str(out))
 # Separate named rigid meshes are intentional for the checkpoint contact audit.
 # Final atlas delivery will consolidate through kit.export after form acceptance.
 W.export(out.with_suffix('.glb'),[arm,*PARTS,*sockets])
 counts={o.name:len(o.data.polygons) for o in PARTS}
 report=dict(total=sum(counts.values()),parts=counts,high_sources={h.name:sum(len(f.vertices)-2 for f in h.data.polygons) for h in HIGH},standalones={})
 mp=[o for o in PARTS if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')]
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
  W.pose(arm,clip,0);ob=W.detachable(mp,arm,'Magazine','Magazine')
  W.export(out.parent/('magazine_'+state+'.glb'),[ob],animations=False)
  report['standalones']['magazine_'+state]=sum(len(f.vertices)-2 for f in ob.data.polygons)
  bpy.data.objects.remove(ob,do_unlink=True)
 W.pose(arm,None,0)
 for name,fired,n in [('cartridge',False,32),('case',True,32)]:
  start=len(PARTS);cartridge(lathe,name,(0,0,0),'Root',fired=fired,sides=n);pieces=PARTS[start:]
  for o in pieces:finalize(o)
  ob=W.joined_copy(pieces,name.title());ob.parent=None
  W.export(out.parent/(name+'.glb'),[ob],animations=False)
  report['standalones'][name]=sum(len(f.vertices)-2 for f in ob.data.polygons)
  bpy.data.objects.remove(ob,do_unlink=True)
  for o in pieces:bpy.data.objects.remove(o,do_unlink=True)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2))
 print('SMG TRIANGLES',report['total'],'STANDALONES',report['standalones'],flush=True)
if __name__=='__main__':main()
