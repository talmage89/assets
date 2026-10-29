"""Covey 26: original visual game geometry, authored in millimeters.

No photograph is read here. Visible construction is modeled for animation;
hidden firing parts and working mechanical fits are intentionally absent.
Wood and thumb controls use changing three-dimensional subdivision cages.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from guns.common.shell12_visual import shell,bridge
from parameters import *
from clips import build_clips

PARTS=[];HIGH=[];MAT={}
ACTION_STATIONS=[(36,16.6,3,44),(37,16.8,3,44.5),(43,17.5,3.5,46),
 (57,19.8,4,49),(77,22.4,4.8,52.5),(94,24.5,6,55),
 (104,26,7,57.5),(114.5,26.1,7,57.7),(115,26.1,7,57.7)]
def action_section(y):
 i=next((i for i in range(len(ACTION_STATIONS)-1) if y<=ACTION_STATIONS[i+1][0]),len(ACTION_STATIONS)-2)
 a,b=ACTION_STATIONS[i:i+2];h=b[0]-a[0];t=max(0,min(1,(y-a[0])/h));values=[]
 for k in (1,2,3):
  def slope(j):
   if j==0:return (ACTION_STATIONS[1][k]-ACTION_STATIONS[0][k])/(ACTION_STATIONS[1][0]-ACTION_STATIONS[0][0])
   if j==len(ACTION_STATIONS)-1:return (ACTION_STATIONS[j][k]-ACTION_STATIONS[j-1][k])/(ACTION_STATIONS[j][0]-ACTION_STATIONS[j-1][0])
   l=(ACTION_STATIONS[j][k]-ACTION_STATIONS[j-1][k])/(ACTION_STATIONS[j][0]-ACTION_STATIONS[j-1][0]);r=(ACTION_STATIONS[j+1][k]-ACTION_STATIONS[j][k])/(ACTION_STATIONS[j+1][0]-ACTION_STATIONS[j][0])
   return 2*l*r/(l+r) if l*r>0 else 0
  m,n=slope(i),slope(i+1)
  values.append((2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*h*m+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*h*n)
 return values
def action_roof(x,y):
 w,_,top=action_section(y)
 arch=math.sqrt(max(.000001,1-(x/w)**2));blend=max(0,min(1,(y-76)/28));blend=blend*blend*(3-2*blend)
 lobe=44+math.sqrt(max(0,13.7**2-(abs(x)-12.6)**2));land=top-3.8
 # A small central strap land joins the rounded fences without a knife valley.
 lobe=.5*(lobe+land+math.sqrt((lobe-land)**2+.30**2))
 # A soft minimum rolls the fence into its top land. A literal min leaves a
 # moving crease across decimated triangles, visible as a sawtooth highlight.
 crown=.5*(top+lobe-math.sqrt((top-lobe)**2+.8**2))
 return (top-7+7*arch)*(1-blend)+crown*blend
def materials():
 for name,color,metal,rough in [('blue',(.014,.016,.019),.85,.39),
  ('wood',(.065,.025,.010),0,.46),('plate',(.016,.015,.013),0,.56),
  ('steel',(.25,.26,.27),1,.34),('dark',(.045,.047,.050),1,.40),
  ('brass',(.48,.30,.085),1,.28),('hull',(.30,.018,.009),0,.36),
  ('primer',(.34,.32,.26),1,.35),('mouth',(.015,.007,.004),0,.77)]:
  mat=bpy.data.materials.new('CP_'+name);mat.use_nodes=True;mat.diffuse_color=(*color,1)
  bs=mat.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*color,1)
  bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;MAT[name]=mat
def clean(ob,dist=.00003):
 bm=bmesh.new();bm.from_mesh(ob.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=dist)
 bmesh.ops.dissolve_degenerate(bm,dist=dist,edges=list(bm.edges))
 boundary=[e for e in bm.edges if e.is_boundary]
 if boundary and len(boundary)==3 and max(e.calc_length() for e in boundary)<.5:
  bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
def reg(ob,bone='Root',radius=0,segments=3):
 if radius:M.bevel(ob,radius,segments)
 M.apply(ob);clean(ob);M.smooth(ob,45)
 ob['bone']=bone;ob['asset_set']='SXS';ob['part_name']=ob.name;PARTS.append(ob);return ob
def box(name,lo,hi,mat='blue',bone='Root',radius=.3,raw=False):
 a,b=Vector(lo),Vector(hi);ob=M.box(name,(a+b)/2,b-a,MAT[mat],0);M.apply(ob)
 ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
 return ob if raw else reg(ob,bone,radius)
def lathe(name,pts,mat='blue',bone='Root',axis='Y',center=(0,0),n=48,closed=False,raw=False):
 ob=M.lathe(name,pts,MAT[mat],segments=n,axis=axis,center=center,closed=closed)
 return ob if raw else reg(ob,bone)
def profile(name,pts,lo,hi,mat='blue',bone='Root',axis='X',radius=.3,raw=False):
 ob=M.profile(name,pts,lo,hi,MAT[mat],axis=axis)
 return ob if raw else reg(ob,bone,radius)
def cut(ob,tool,operation='DIFFERENCE'):
 tool.data.materials.clear();tool.data.materials.append(ob.data.materials[0]);M.boolean(ob,tool,operation);return ob
def cutbox(ob,lo,hi):return cut(ob,box('Tool',lo,hi,raw=True))
def subd(ob,level):
 m=ob.modifiers.new('Sculpted compound cage','SUBSURF');m.levels=level;m.render_levels=level;M.apply(ob);return ob
def reduce(ob,target):
 count=sum(len(f.vertices)-2 for f in ob.data.polygons)
 if count>target:
  m=ob.modifiers.new('Game silhouette allocation','DECIMATE');m.ratio=target/count;M.apply(ob)
 return ob
def high_copy(ob):
 h=ob.copy();h.data=ob.data.copy();bpy.context.collection.objects.link(h);h.name='HIGH_'+ob.name
 h['bake_only']=True;h['low_target']=ob.name;h['source_method']='three-dimensional subdivision cage'
 HIGH.append(h);return h
def curved_mesh(name,loops,mat,bone,*,level=0,target=None,high=False):
 ob=M.loft(name,loops,MAT[mat]);subd(ob,level) if level else None
 if high:high_copy(ob)
 if target:reduce(ob,target)
 return reg(ob,bone)
def rounded_loop(y,w,bottom,top,p=3.2,n=48):
 return [(w*math.copysign(abs(math.cos(t))**(2/p),math.cos(t)),y,
  (top+bottom)/2+(top-bottom)/2*math.copysign(abs(math.sin(t))**(2/p),math.sin(t))) for t in [i*math.tau/n for i in range(n)]]
def arc_solid(name,x0,x1,r0,r1,a0,a1,mat='dark',bone='Root',n=48):
 # Annular machined section, centered on the common hinge axis.
 pts=[]
 for r,seq in [(r1,range(n+1)),(r0,range(n,-1,-1))]:
  for i in seq:
   t=math.radians(a0+(a1-a0)*i/n);pts.append((HINGE[1]+r*math.cos(t),HINGE[2]+r*math.sin(t)))
 return profile(name,pts,x0,x1,mat,bone,radius=.08)
def screw(name,x,y,z,r=2.4,axis='X',bone='Root',mat='dark'):
 pts=[(-.6,0),(-.6,r*.84),(-.3,r),(.15,r),(.3,r*.88),(.3,0)]
 if axis=='X':pts=[(a*(1 if x>=0 else -1)+x,rr) for a,rr in pts];center=(y,z)
 elif axis=='Z':pts=[(a+z,rr) for a,rr in pts];center=(x,y)
 else:pts=[(a+y,rr) for a,rr in pts];center=(x,z)
 ob=lathe(name,pts,mat,bone,axis,center,n=24)
 if axis=='X':
  a,b=sorted((x-.1*(1 if x>=0 else -1),x+.5*(1 if x>=0 else -1)));cutbox(ob,(a,y-r-.1,z-.28),(b,y+r+.1,z+.28))
 elif axis=='Z':cutbox(ob,(x-.28,y-r-.1,z-.1),(x+.28,y+r+.1,z+.5))
 return ob

def action():
 # One rounded forged body with changing width/height and two rounded fences.
 loops=[]
 for y in sorted({a[0] for a in ACTION_STATIONS}|set(range(38,115,2))):
  w,bot,top=action_section(y)
  # Long side lands, a radiused belly and lobed roof. Top tangency flows into
  # the barrel fences, rather than two round caps perched on a rectangular box.
  pts=[]
  for i in range(65):
   x=-w+2*w*i/64
   z=action_roof(x,y)
   pts.append((x,y,z))
  pts += [(w,y,bot+4),(w-1.2,y,bot+1.2),(w-4,y,bot),(-w+4,y,bot),(-w+1.2,y,bot+1.2),(-w,y,bot+4)]
  loops.append(pts)
 body=M.loft('Action_Body',loops,MAT['blue'])
 roof_tag=body.data.attributes.new('SXS_Roof','INT','FACE')
 nc=len(loops[0]);surface_faces=(len(loops)-1)*nc
 for f in body.data.polygons:roof_tag.data[f.index].value=int(f.index<surface_faces and f.index%nc<64)
 # The open water table is a shallow continuation with a real central floor
 # slot. It is not a solid rectangular block beneath the barrels.
 bed=M.loft('Table raw',[[(x,y,z+(bot+top)/2) for x,z in M.rounded_rectangle(w*2,top-bot,2.8,8)] for y,w,bot,top in
  [(113,26.0,7,30.2),(125,25.8,7,30.2),(145,25.1,7,29.5),(156,24.2,7.5,26),(169,22.5,9,24)]],MAT['blue'])
 cut(body,bed,'UNION')
 cutbox(body,(-6.4,116,-8),(6.4,178,32))
 # Two pin bushings, recessed in the standing breech. Their dark centers are
 # visible representations only; no firing-pin geometry or working bores.
 for side,x in [('R',12.6),('L',-12.6)]:
  tool=lathe('Tool',[(113.9,0),(113.9,3.5),(116,3.5),(116,0)],center=(x,BORE),n=32,raw=True)
  cut(body,tool)
  lathe('Bushing_'+side,[(114,1),(114,3.35),(114.95,3.35),(114.95,1)],'steel',center=(x,BORE),n=32,closed=True)
  lathe('PinFace_'+side,[(114.6,0),(114.6,.8),(114.85,.8),(114.85,0)],'dark',center=(x,BORE),n=16)
 # Genuine passage for the visual locking shoe beneath the two lug bites.
 cutbox(body,(-4.4,98,10),(4.4,146,15.1))
 cut(body,lathe('Tool',[(48.9,0),(48.9,4.25),(59,4.25),(59,0)],axis='Z',center=(0,94),n=48,raw=True))
 # Trigger plate wells are relieved through the underside.
 cutbox(body,(-7.4,39,-5),(7.4,78,11))
 reg(body,radius=.65);reduce(body,4300)
 # Hinge pin is continuous; the two knuckle cheeks leave the hook visible.
 lathe('Hinge_Pin',[(-23,0),(-23,4.10),(23,4.10),(23,0)],'steel',axis='X',center=(170,19),n=48)
 for side in (-1,1):
  a,b=sorted((side*6.7,side*23))
  lathe('Knuckle_'+('R' if side>0 else 'L'),[(a,4.15),(a,12),(b,12),(b,4.15)],'blue',axis='X',center=(170,19),n=32,closed=True)
  screw('Hinge_Head',side*23,170,19,3.2)
 for side in (-1,1):
  for y,z,r in [(55,26,2.7),(88,19,2.2)]:screw('Action_CrossPin',side*(action_section(y)[0]-.15),y,z,r)
 # Top strap and lower tang use compound cages, spanning the wood head.
 curved_mesh('Top_Strap',[rounded_loop(y,w,z-1.7,z+1.7,p=3,n=24) for y,w,z in
  [(-27,3.4,18.8),(-26,4,18.9),(-10,5.8,18.8),(9,7,23.2),(28,8,38.4),(43,9.2,46)]],
  'blue','Root',level=2,target=950)
 curved_mesh('Trigger_Plate',[rounded_loop(y,w,z-1.4,z+1.4,p=4,n=24) for y,w,z in
  [(-22,3.2,-12),(-20,4,-11.5),(5,6.0,-5.5),(27,9.5,2.5),(48,11,5),(76,9,6.0),(86,6.3,7)]],
  'blue','Root',level=1,target=700)
 # Trigger slots are cut after the plate's compound surface is established.
 plate=PARTS[-1]
 for x,y in [(2.6,64),(-2.6,43)]:cutbox(plate,(x-3.8,y-5,-6),(x+3.8,y+11,9))
 # Distinct shoe translates out of the bites before the opening swing.
 box('Locking_Shoe',(-4,124,10.4),(4,129.9,11.8),'steel','LockBolt',radius=.10)
 box('Locking_Shoe_Upper',(-4,130,13.2),(4,141.9,14.6),'steel','LockBolt',radius=.10)
 # Unseen lockwork is omitted; this bridge only makes the visible bite contact.

def barrel_shape(y):
 t=(y-BREECH)/(MUZZLE-BREECH)
 x=12.6-1.7*t
 if y<185:r=13.35-.5*(y-BREECH)/70
 elif y<240:r=12.85-1.65*(y-185)/55
 else:r=11.2-.6*(y-240)/(MUZZLE-240)
 return x,r
def barrels():
 for side,sign in [('R',1),('L',-1)]:
  specs=[]
  # Continuous tube walls, thicker at the chamber and a small rolled muzzle.
  outer=[(115,13.35),(116,13.35),(155,13.1),(185,12.85),(212,12.0),(240,11.2),
   (500,10.91),(740,10.64),(774.8,10.6),(775.4,10.35)]
  inner=[(775.4,9.55),(775.0,9.25),(235,9.25),(185,10.2),(116.8,10.2),(116.8,11.3),(115,11.3)]
  rings=[];vertices=[]
  for y,r in outer+inner:
   x=sign*barrel_shape(y)[0];ring=[]
   sides=64 if y>774 or y<118 else 48
   for i in range(sides):
    t=math.tau*i/sides;ring.append(len(vertices));vertices.append((x+r*math.cos(t),y,BORE+r*math.sin(t)))
   rings.append(ring)
  faces=[f for a,b in zip(rings,rings[1:]+rings[:1]) for f in bridge(a,b)]
  ob=reg(M.mesh('Barrel_'+side,vertices,faces,MAT['blue']),'Barrels');ob['tube_axis_sign']=sign
 # A solid top rib has a shallow concave matted face; geometry carries its
 # tapered silhouette. Fine matting remains a later normal-bake field.
 loops=[]
 for y,w,z in [(115,4.4,58.2),(116,4.4,58.2),(185,4.0,58.0),(240,3.7,57.6),
  (500,3.2,57.2),(774.8,2.8,57.0),(775.4,2.8,57.0)]:
  lower=BORE+barrel_shape(y)[1]*.58
  pts=[(-w,y,lower),(-w,y,z-.35),(-w+.4,y,z),(-w*.5,y,z-.18),(0,y,z-.25),
   (w*.5,y,z-.18),(w-.4,y,z),(w,y,z-.35),(w,y,lower)]
  loops.append(pts)
 reg(M.loft('Solid_TopRib',loops,MAT['blue']),'Barrels')
 lower_loops=[]
 for y,w in [(118,3.5),(185,3.0),(240,2.4),(500,2.2),(775.1,2.1)]:
  x,r=barrel_shape(y);bottom=BORE-r+.15
  top=BORE-math.sqrt(max(0,r*r-(x-w)**2))+.28
  lower_loops.append([(xx,y,zz+(bottom+top)/2) for xx,zz in M.rounded_rectangle(w*2,top-bottom,.28,3)])
 reg(M.loft('Bottom_Rib',lower_loops,MAT['blue']),'Barrels')
 # Monobloc's lower bridge and visible stepped lumps. Bites are real pockets.
 lump=profile('Breech_Lumps',M.fillet_polygon([(119,30.8),(153,30.8),(164,27),(164,15),
  (144,7),(121,7)],1.2,4),-5.3,5.3,'dark','Barrels',radius=.25,raw=True)
 cutbox(lump,(-5.8,118,10.1),(5.8,130.1,12.1))
 cutbox(lump,(-5.8,118,12.9),(5.8,142.1,14.9))
 cutbox(lump,(-2.5,114,29.1),(2.5,155,33.4))
 reg(lump,'Barrels',radius=.18)
 arc_solid('Barrel_Hook',-5.3,5.3,4.30,8.6,44,318,'dark','Barrels',n=64)
 box('Hook_Web',(-5.3,155,25),(5.3,170,31.0),'dark','Barrels',radius=.5)
 # Continuous double-lobe extractor; two crescent pads bear on the shell rims.
 pads=[]
 for side,x in [('R',12.6),('L',-12.6)]:
  pts=[]
  for r,seq in [(11.18,range(25)),(10.2,range(24,-1,-1))]:
   for i in seq:
    t=math.radians(204+132*i/24);pts.append((x+r*math.cos(t),BORE+r*math.sin(t)))
  pad=profile('Extractor_Rim_'+side,pts,116.4,118.5,'steel','Extractor',axis='Y',radius=.04)
  for v in pad.data.vertices:
   if v.co.y<116.5:
    r=math.hypot(v.co.x-x,v.co.z-BORE);v.co.y+=max(0,(11.2-r)*.4/1.1)+.04
  pads.append(pad)
 box('Extractor_Bridge',(-3.4,116.4,31.0),(3.4,118.5,33.6),'steel','Extractor',radius=.10)
 box('Extractor_Stem',(-2.2,118,29.5),(2.2,154,33.0),'dark','Extractor',radius=.25)
 # Stem channel and pads' actual relief keep the extractor out of barrel steel.
 for ob in [o for o in PARTS if o.name in ('Barrel_R','Barrel_L')]:
  sign=ob['tube_axis_sign'];pad=next(p for p in pads if p.name.endswith('R' if sign>0 else 'L'))
  tool=pad.copy();tool.data=pad.data.copy();bpy.context.collection.objects.link(tool)
  for v in tool.data.vertices:
   xx=v.co.x-sign*12.6;zz=v.co.z-BORE;rr=math.hypot(xx,zz)
   if rr<10.5:
    v.co.x=sign*12.6+xx*9.8/rr;v.co.z=BORE+zz*9.8/rr
   if v.co.y>117:v.co.y=119
   else:v.co.y=114.9
  cut(ob,tool)
 rib=next(o for o in PARTS if o.name=='Bottom_Rib');cutbox(rib,(-2.5,114,29.0),(2.5,155,33.4))
 cutbox(rib,(-3.7,114,29),(3.7,119,34))
 # Brass bead is a round object on a seated foot, not an emissive dot.
 lathe('Bead_Foot',[(56.8,0),(56.8,1),(58.5,1),(58.5,0)],'brass','Barrels',axis='Z',center=(0,766),n=24)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1.3,location=(0,766,59.8))
 ob=bpy.context.object;ob.name='Front_Bead';ob.data.materials.append(MAT['brass'])
 ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4);reg(ob,'Barrels')

STOCK=[(-299,21.3,-117,-5),(-298.4,21.3,-117,-5),(-294,21.8,-115,-4),
 (-275,22.1,-107,-1),(-245,22.0,-91,4),(-210,21.6,-73,9),(-175,20.9,-54,14),
 (-145,19.9,-40,18),(-122,18.8,-31,20),(-106,17.5,-25,20.7),
 (-88,16.2,-21,20.7),(-65,15.2,-18.5,20.2),(-38,14.4,-17.7,19.2),
 (-15,14.5,-17.2,18),(0,15,-17,18),(12,15.8,-12,24),(25,16.3,-4,35),
 (35.5,16.55,3,44),(36.5,16.55,3,44),(37,16.55,3,44)]
def wood_loop(y,w,bottom,top,n=40,p=2.25):
 loop=[]
 for i in range(n):
  t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
  x=w*math.copysign(abs(c)**(2/p),c)
  # A narrower comb rolls into full cheeks and an oval wrist, independently
  # of the lengthwise silhouette. Butt pitch fades forward.
  x*=1-.16*max(0,s)**4
  z=(top+bottom)/2+(top-bottom)/2*math.copysign(abs(s)**(2/2.15),s)
  yy=y+.075*(-5-z)*max(0,min(1,(-275-y)/24))
  loop.append((x,yy,z))
 return loop
def wood():
 ob=M.loft('Stock_Walnut',[wood_loop(*r) for r in STOCK],MAT['wood']);subd(ob,2)
 # Tang seats are machined after sculpting so there are no voxel lips.
 for name in ('Top_Strap','Trigger_Plate'):
  src=next(p for p in PARTS if p.name==name);tool=src.copy();tool.data=src.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 body=next(p for p in PARTS if p.name=='Action_Body');tool=body.copy();tool.data=body.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 h=high_copy(ob);subd(h,1);reduce(ob,6700);reg(ob)
 loops=[]
 for y,s in [(-299,1),(-299.5,1.002),(-303.9,1.001),(-304.6,.996)]:
  loops.append(wood_loop(y,21.3*s,-117,-5,n=64))
 reg(M.loft('Butt_Plate',loops,MAT['plate']),radius=.45)
 for z in (-30,-91):
  y=-304.3+.075*(-5-z)
  lathe('Butt_Screw',[(y,0),(y,2),(y+.35,2),(y+.35,0)],'dark',center=(0,z),n=20)
 # Slim forend: unequal end tapers, broad lower palms and two real barrel
 # channels. Its dense source supplies compound curvature for later baking.
 stations=[(181,17.1,3,31),(182,18.8,3,32.4),(189,20.7,2,34),
  (211,21.1,3,34.4),(242,20.5,4,34.7),(279,19.1,5,34.9),
  (314,17.3,7,34.6),(341,14.5,10,33.4),(355,10.0,16,30.3),
  (360,6.5,21,28),(361,6.2,21.5,27.6)]
 ob=M.loft('Forend_Walnut',[wood_loop(*r,n=40,p=2.7) for r in stations],MAT['wood']);subd(ob,2)
 for side in (-1,1):
  loops=[]
  for y in (178,240,365):
   x,r=barrel_shape(y);loops.append([(side*x+(r+.25)*math.cos(t),y,BORE+(r+.25)*math.sin(t)) for t in [i*math.tau/64 for i in range(64)]])
  cut(ob,M.loft('Channel tool',loops,MAT['wood']))
 # Iron occupies a real pocket in the lower rear wood.
 cutbox(ob,(-7.2,180,-1),(7.2,227,11.5))
 cutbox(ob,(-3.1,178,29),(3.1,365,36))
 cut(ob,lathe('Tool',[(-24,0),(-24,12.25),(24,12.25),(24,0)],axis='X',center=(170,19),n=80,raw=True))
 high_copy(ob);reduce(ob,3300);reg(ob,'Forend')
 # Curved iron cups bear on the shared circular knuckle throughout opening.
 for sign in (-1,1):
  a,b=sorted((sign*7.2,sign*21.5))
  arc_solid('Forend_IronCup_'+('R' if sign>0 else 'L'),a,b,12.15,14.3,-50,52,'dark','Forend',n=44)
 curved_mesh('Forend_Iron',[rounded_loop(y,w,bot,top,p=4,n=24) for y,w,bot,top in
  [(180,6.8,3,11.3),(188,7,3,11.3),(215,6.5,3.5,11.3),(226,5.7,4,11.3)]],
  'dark','Forend',level=1,target=450)
 # An inset oval latch in the underside, fixed for this presentation.
 latch=curved_mesh('Forend_Latch',[rounded_loop(y,w,z-1.5,z+1.5,p=3,n=20) for y,w,z in
  [(219,2.2,4.6),(221,4,4.2),(235,5.2,4.5),(250,4.6,5.0),(255,2.8,5.6)]],
  'blue','Forend',level=1,target=400)
 # Recess the inset latch into both source and game wood.
 for woodpart in [ob]+[h for h in HIGH if h.get('low_target')=='Forend_Walnut']:
  tool=latch.copy();tool.data=latch.data.copy();bpy.context.collection.objects.link(tool);cut(woodpart,tool)
 # Latch backing reaches the iron through a short web inside the wood.
 box('Latch_Web',(-3,218,3),(3,225,9),'dark','Forend',radius=.6)

def controls():
 # Guard is a broad thin steel band with radiused lateral edges, swept along
 # the bow. It joins the lower plate at both ends.
 path=M.bezier((14,-1),(14,-37),(49,-35),(75,-29),24)
 path+=M.bezier((75,-29),(94,-25),(95,-3),(82,4),20)[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  p=Vector(path[max(0,i-1)]);q=Vector(path[min(len(path)-1,i+1)]);d=(q-p).normalized();normal=Vector((-d.y,d.x))
  loop=[]
  # Rounded rectangle section across X; a band, never a round rod.
  for x,v in M.rounded_rectangle(9.4,2.5,.6,4):loop.append((x,y+v*normal.x,z+v*normal.y))
  loops.append(loop)
 reg(M.loft('Trigger_Guard',loops,MAT['blue']),radius=.08)
 for name,x,y,bone in [('Front_Trigger',2.6,64,'Trigger'),('Rear_Trigger',-2.6,43,'TriggerRear')]:
  pts=[(y-3,7),(y+7.0,7),(y+7,3)]
  pts+=M.bezier((y+7,3),(y-1,-4),(y,-16),(y+7.1,-23),14)[1:]
  pts+=M.bezier((y+7.1,-23),(y+7.8,-24.4),(y+6,-24.7),(y+4.6,-23),5)[1:]
  pts+=M.bezier((y+4.6,-23),(y-4,-15),(y-4,-4),(y+2,3),12)[1:]
  pts += [(y-3,4)]
  # Broad at its root, narrower near the forward toe, with a rounded face.
  ob=M.profile(name,pts,x-2.7,x+2.7,MAT['blue'],axis='X')
  for v in ob.data.vertices:
   s=max(0,min(1,(4-v.co.z)/28));v.co.x=x+(v.co.x-x)*(1-.24*s)
  reg(ob,bone,radius=.55,segments=3)
 # Sculpted top lever: thick root, swept neck, flattened curved thumb paddle.
 loops=[]
 for y,x,w,z,h in [(96,0,4.7,53,2),(94,0,4.8,53.8,2),(89,-.2,4.3,54.2,1.8),
  (81,-1.2,3.4,54.7,1.8),(73,-1.8,6.2,55.0,1.8),(63,-1.1,8.4,55.2,1.7),
  (56,0,7.5,55.0,1.5),(53,0,5.1,54.8,1.0),(52.5,0,4.7,54.8,.8)]:
  loops.append([(xx+x,yy,zz) for xx,yy,zz in rounded_loop(y,w,z-h,z+h,p=2.8,n=24)])
 ob=M.loft('Top_Lever',loops,MAT['blue']);subd(ob,2)
 for v in ob.data.vertices:v.co.z+=2.5
 high_copy(ob);reduce(ob,800);reg(ob,'TopLever')
 lathe('Top_LeverSpindle',[(49.2,0),(49.2,4.1),(56,4.1),(56,0)],'dark','TopLever',axis='Z',center=(0,94),n=32)
 # Safety follows the inclined strap, with a broad low thumb land and real
 # guide block below. State-only automatic actuation is in the interface.
 loops=[]
 for y,w,z,h in [(-2,2.6,30.5,1),(-1.5,3.2,30.7,1.3),(4,4.1,33.1,1.5),
  (11,4.2,35.5,1.5),(15.5,3.1,37.1,1.2),(16,2.6,37.2,1)]:
  loops.append(rounded_loop(y,w,z-h-10,z+h-10,p=3,n=24))
 ob=M.loft('Tang_Safety',loops,MAT['blue']);subd(ob,2);high_copy(ob);reduce(ob,600);reg(ob,'Safety')
 box('Safety_Guide',(-2.3,0,17),(2.3,10,23),'dark','Safety',radius=.3)
 # Cut the safety's entire guide and 5 mm visual detent travel into the strap.
 strap=next(o for o in PARTS if o.name=='Top_Strap')
 # Cut a continuous visual thumb-pad inlet in the strap and stock, with a
 # small radial separation. No allowed-pair collision skips hide the seat.
 pad=next(o for o in PARTS if o.name=='Tang_Safety')
 stock=next(o for o in PARTS if o.name=='Stock_Walnut')
 for target in [strap,stock]+[h for h in HIGH if h.get('low_target')=='Stock_Walnut']:
  outline=[(x,y+4.5) for x,y in M.rounded_rectangle(9.1,28,3.8,8)]
  cut(target,profile('Safety inlet',outline,16.6,39,axis='Z',raw=True))
 # Two recessed machined rails close the broad inlet below the thumb pad.
 # The narrow guide runs between them; the remaining visible slot has depth.
 for sign in (-1,1):
  loops=[]
  for y,z in [(-8.5,19.15),(-6,19.73),(0,21.12),(8,22.47),(17.8,25.5)]:
   z-=1.0;x=sign*3.475;loops.append([(x-.875,y,z-1.5),(x+.875,y,z-1.5),(x+.875,y,z),(x-.875,y,z)])
  reg(M.loft('Safety_Track_'+('R' if sign>0 else 'L'),loops,MAT['dark']))
 floor=[(x,y+4.45) for x,y in M.rounded_rectangle(8.9,27.3,3.8,5)]
 profile('Safety_TrackFloor',floor,16.55,16.85,'dark',axis='Z',radius=0)

def ammunition():
 for name,base in [('LiveR',(12.6,BREECH,BORE)),('LiveL',(-12.6,BREECH,BORE)),
  ('HullR',(12.6,BREECH,BORE)),('HullL',(-12.6,BREECH,BORE)),
  ('InsertR',(12.6,BREECH,BORE)),('InsertL',(-12.6,BREECH,BORE))]:
  ob=shell(name,MAT,base=base,fired=name.startswith('Hull'));reg(ob,name)

def finalize(ob):
 clean(ob)
 if not len(ob.data.vertices):raise AssertionError('Empty manufactured part: '+ob.name)
 # Only silhouette-scale detail survives in the game mesh. In particular,
 # annular-section edge bevels must not consume thousands of hidden triangles.
 allocations={'Stock_Walnut':5200,'Forend_Walnut':2350,'Action_Body':3000,
  'Barrel_Hook':650,
  'Forend_IronCup_R':500,'Forend_IronCup_L':500,'Trigger_Guard':1100,
  'Butt_Plate':650,'Extractor_Rim_R':350,'Extractor_Rim_L':350,
  'Front_Trigger':650,'Rear_Trigger':650,'Top_Strap':700,'Tang_Safety':450}
 target=allocations.get(ob.name,130 if ob.name.startswith(('Hinge_Head','Action_CrossPin')) else None)
 if target:reduce(ob,target)
 # Collapse can expose a tiny Boolean corner at the lever bore. Repair only
 # isolated sub-half-millimeter triangular boundaries after the final reduction.
 clean(ob,dist=.0001)
 tri=ob.modifiers.new('Explicit game triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(ob)
 if ob.name=='Action_Body':
  ob.data.normals_split_custom_set([(0,0,0)]*len(ob.data.loops));M.smooth(ob,42)
  m=ob.modifiers.new('Reseed forged and machined fields','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=40;M.apply(ob)
 normals=[n.vector.copy() for n in ob.data.corner_normals]
 if 'tube_axis_sign' in ob:
  sign=ob['tube_axis_sign']
  for f in ob.data.polygons:
   for j in f.loop_indices:
    p=ob.data.vertices[ob.data.loops[j].vertex_index].co
    if abs(f.normal.y)<.2:
     x=sign*barrel_shape(p.y)[0];nn=Vector((p.x-x,0,p.z-BORE)).normalized()
     normals[j]=nn if nn.dot(f.normal)>0 else -nn
    elif abs(f.normal.y)>.995:normals[j]=Vector((0,math.copysign(1,f.normal.y),0))
 if ob.name=='Action_Body':
  # Preserve the long forging flats and standing-breech plane.
  for f in ob.data.polygons:
   vs=[ob.data.vertices[i].co for i in f.vertices]
   if abs(f.normal.y)>.998:
    for j in f.loop_indices:normals[j]=f.normal.copy()
   if abs(f.normal.x)>.85 and abs(f.normal.z)<.25 and all(36<=p.y<=115 and abs(abs(p.x)-action_section(p.y)[0])<.25 for p in vs):
    for j in f.loop_indices:
     p=ob.data.vertices[ob.data.loops[j].vertex_index].co;dw=(action_section(p.y+.02)[0]-action_section(p.y-.02)[0])/.04
     normals[j]=Vector((math.copysign(1,p.x),-dw,0)).normalized()
   roof_tag=ob.data.attributes.get('SXS_Roof')
   if roof_tag and roof_tag.data[f.index].value and abs(f.normal.y)<.95 and f.normal.z>.01:
    values=[]
    for j in f.loop_indices:
     p=ob.data.vertices[ob.data.loops[j].vertex_index].co
     yy=max(36.01,min(114.99,p.y));w=action_section(yy)[0];xx=max(-w+.03,min(w-.03,p.x))
     dx=(action_roof(xx+.02,yy)-action_roof(xx-.02,yy))/.04
     dy=(action_roof(xx,yy+.02)-action_roof(xx,yy-.02))/.04
     values.append(Vector((-dx,-dy,1)).normalized())
    for j,n in zip(f.loop_indices,values):normals[j]=n
 if ob.get('ammo_visual'):
  x,_,z=HEADS[ob['bone']]
  for f in ob.data.polygons:
   for j in f.loop_indices:
    p=ob.data.vertices[ob.data.loops[j].vertex_index].co
    if abs(f.normal.y)>.995:normals[j]=Vector((0,math.copysign(1,f.normal.y),0))
    elif abs(f.normal.y)<.12:
     nn=Vector((p.x-x,0,p.z-z)).normalized();normals[j]=nn if nn.dot(f.normal)>0 else -nn
 for f in ob.data.polygons:
  for j in f.loop_indices:
   if normals[j].dot(f.normal)<.03:normals[j]=f.normal.copy()
 ob.data.transform(Matrix.Scale(.001,4));ob.data.update();ob.data.normals_split_custom_set(normals)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/sxs.blend')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);materials()
 action();barrels();wood();controls();ammunition()
 for ob in PARTS:finalize(ob)
 highcollection=bpy.data.collections.new('High_Sources');bpy.context.scene.collection.children.link(highcollection)
 for ob in HIGH:
  ob.data.transform(Matrix.Scale(.001,4))
  for c in list(ob.users_collection):c.objects.unlink(ob)
  highcollection.objects.link(ob);ob.hide_render=True;ob.hide_set(True)
 arm=W.armature('SXSArmature',{k:tuple(v*.001 for v in p) for k,p in HEADS.items()},parents=PARENTS)
 for ob in PARTS:W.rigid_bind(ob,arm,ob['bone'])
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in p) for k,p in SOCKETS.items()},RIDING)
 # The optical frame follows the bead from the cheek-weld eye height. It is
 # a slight downward sightline; the rig and all other sockets keep +Y/+Z.
 eye=next(o for o in sockets if o.name=='Socket_Eye')
 eye.rotation_euler.x=math.atan2(59.8-EYE[2],766-EYE[1])
 arm['generator_sha256']=generator_digest();build_clips(arm);W.pose(arm,'Idle',0)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['stage']='Form checkpoint, unbaked constant inspection materials'
 sc['maker']='Propane Defense';sc['model']='Covey 26';sc['interface_version']='1.7.0'
 bpy.ops.wm.save_as_mainfile(filepath=str(out));W.export(out.with_suffix('.glb'),[arm]+PARTS+sockets)
 counts={ob.name:len(ob.data.polygons) for ob in PARTS}
 report=dict(total=sum(counts.values()),parts=counts,standalones={})
 for name,fired in [('shell',False),('hull',True)]:
  ob=shell('LiveShell' if not fired else 'FiredHull',MAT,fired=fired)
  tri=ob.modifiers.new('Explicit triangles','TRIANGULATE');M.apply(ob);ob.data.transform(Matrix.Scale(.001,4))
  W.export(out.parent/(name+'.glb'),[ob],animations=False)
  report['standalones'][name]=len(ob.data.polygons);bpy.data.objects.remove(ob,do_unlink=True)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2));print('SXS TRIANGLES',report['total'],report['standalones'],flush=True)
if __name__=='__main__':main()
