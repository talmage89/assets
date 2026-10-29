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
ACTION_STATIONS=[(70,22.0,5,50),(72,22.2,5.2,50.6),(77,22.8,5.5,52),
 (94,24.8,6,55),(104,27.3,7,57.5),(114.5,27.4,7,57.5),(115,27.4,7,57.5)]
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
 # Fence shoulders follow the chamber crowns all the way to the side flats.
 # The central top-strap land is narrow; no full-width flat roof.
 t=max(0,min(1,(y-94)/17));t=t*t*(3-2*t)
 u=max(0,min(1,(y-70)/20));u=u*u*(3-2*u)
 rear=top-8+8*math.sqrt(max(0,1-(x/w)**2))-3*u
 lobe=44+math.sqrt(max(0,14.8**2-(abs(x)-12.6)**2))
 land=top-2.6
 central=math.exp(-(x/6.5)**2)
 fence=lobe*(1-central)+land*central
 return rear*(1-t)+fence*t
def rear_seam(z):
 # A gently bowed forging end; the wood head wraps it after carving.
 return -5.0*math.sin(math.pi*max(0,min(1,(z-3)/38)))
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
 # A Boolean inlet may leave a folded triangular flap attached along one
 # edge. Remove only this bounded, topologically identified remnant; closing
 # its two exposed edges would create a fourth face on the attached edge.
 flaps=[f for f in bm.faces if len(f.verts)==3 and max(e.calc_length() for e in f.edges)<.6
  and sum(e.is_boundary for e in f.edges)==2 and any(len(e.link_faces)==3 for e in f.edges)]
 if flaps:
  bmesh.ops.delete(bm,geom=flaps,context='FACES')
  loose=[v for v in bm.verts if not v.link_faces]
  if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
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
 [h.pop(k,None) for k in ('bone','asset_set','part_name')]
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
 # Continuous forging: radiused lower edge, planar side lands and crown.
 loops=[]
 for y in sorted({a[0] for a in ACTION_STATIONS}|set(range(74,115,2))):
  w,bot,top=action_section(y);pts=[]
  for i in range(65):
   theta=math.pi*i/64;x=-w*math.cos(theta)
   pts.append((x,y,action_roof(x,y)))
  # Elliptical belly transition gives broad radii without rounding the flats.
  shoulder=7.0
  pts += [(w,y,bot+shoulder)]
  for i in range(1,13):
   t=math.pi/2*i/12;pts.append((w-shoulder+shoulder*math.cos(t),y,bot+shoulder-shoulder*math.sin(t)))
  pts += [(-w+shoulder,y,bot)]
  for i in range(1,13):
   t=math.pi/2*i/12;pts.append((-w+shoulder-shoulder*math.sin(t),y,bot+shoulder-shoulder*math.cos(t)))
  fade=max(0,1-(y-70)/20)**2
  loops.append([(x,yy+rear_seam(z)*fade,z) for x,yy,z in pts])
 # The bar continues the same side lands and lower radii. The front plane
 # between the last crown and the first low table loop is the standing breech.
 for y,w,bot,top in [(115.001,27.4,7,30.2),(125,26.3,7,30.2),(145,24,7.5,29),(157,22.6,8,27),(171,21.5,8,26)]:
  pts=[]
  for i in range(65):
   x=-w*math.cos(math.pi*i/64);dx=max(0,abs(x)-(w-4.5))
   z=top-4.5+math.sqrt(max(0,4.5**2-dx**2));pts.append((x,y,z))
  pts.append((w,y,bot+7))
  pts += [(w-7+7*math.cos(math.pi/2*i/12),y,bot+7-7*math.sin(math.pi/2*i/12)) for i in range(1,13)]
  pts.append((-w+7,y,bot))
  pts += [(-w+7-7*math.sin(math.pi/2*i/12),y,bot+7-7*math.cos(math.pi/2*i/12)) for i in range(1,13)]
  loops.append(pts)
 # The rear interface is a curved surface. A planar ngon cannot cap it;
 # use a ruled triangle fan, hidden by the fitted wood, before machining.
 nc=len(loops[0]);vs=[p for loop in loops for p in loop]
 fs=[(j*nc+i,j*nc+(i+1)%nc,(j+1)*nc+(i+1)%nc,(j+1)*nc+i) for j in range(len(loops)-1) for i in range(nc)]
 center=len(vs);vs.append((0,70+rear_seam(27.5),27.5))
 fs += [(center,(i+1)%nc,i) for i in range(nc)]
 fs += [tuple(range((len(loops)-1)*nc,len(loops)*nc))]
 body=M.mesh('Action_Body',vs,fs,MAT['blue'])
 # The knuckle's transverse cheeks belong to the forging, with rolled end
 # shoulders. They retain the accepted circular bearing radius at x=14 mm.
 for side in (-1,1):
  prof=[(6.7,0),(6.7,10.8),(7.9,12),(20.2,12),(21.5,10.7),(21.5,0)]
  prof=[(side*x,r) for x,r in prof]
  cut(body,lathe('Knuckle tool',prof,axis='X',center=(170,19),n=64,raw=True),'UNION')
 cutbox(body,(-6.4,116,-8),(6.4,184,32))
 cut(body,lathe('Hinge bore',[(-27,0),(-27,4.15),(27,4.15),(27,0)],axis='X',center=(170,19),n=50,raw=True))
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
 reg(body,radius=.55);high_copy(body);reduce(body,5400)
 # Flush cross-pin ends: no proud disc or large slotted screw at the hinge.
 lathe('Hinge_Pin',[(-21.5,0),(-21.5,3.85),(-21.25,4.10),(21.25,4.10),(21.5,3.85),(21.5,0)],'dark',axis='X',center=(170,19),n=48)
 for side in (-1,1):
  for y,z,r in [(79,26,2.7),(102,19,2.2)]:screw('Action_CrossPin',side*(action_section(y)[0]-.15),y,z,r)
 # Top strap and lower tang use compound cages, spanning the wood head.
 curved_mesh('Top_Strap',[rounded_loop(y,w,z-1.7,z+1.7,p=3,n=24) for y,w,z in
  [(-27,3.4,18.8),(-26,4,18.9),(-10,5.8,18.8),(9,7,23.2),(28,7.7,32.4),(50,8,42),(72,8.8,50.5)]],
  'blue','Root',level=2,target=950)
 curved_mesh('Trigger_Plate',[rounded_loop(y,w,z-1.4,z+1.4,p=4,n=24) for y,w,z in
  [(-22,3.2,-12),(-20,4,-11.5),(5,6.0,-5.5),(27,9.5,2.5),(48,11,5),(76,9,6.0),(86,6.3,7)]],
  'blue','Root',level=1,target=700)
 # Trigger slots are cut after the plate's compound surface is established.
 plate=PARTS[-1]
 for x,y in [(2.6,64),(-2.6,31)]:cutbox(plate,(x-3.8,y-5,-6),(x+3.8,y+11,9))
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
  ob=M.mesh('Barrel_'+side,vertices,faces,MAT['blue'])
  if sign>0:cutbox(ob,(-30,114,20),(0,240,70))
  else:cutbox(ob,(0,114,20),(30,240,70))
  reg(ob,'Barrels');ob['tube_axis_sign']=sign
 # A solid top rib has a shallow concave matted face; geometry carries its
 # tapered silhouette. Fine matting remains a later normal-bake field.
 loops=[]
 for y,w in [(115,6.4),(116,6.4),(185,5.8),(240,5.3),(500,4.7),(774.8,4.2),(775.4,4.2)]:
  x,r=barrel_shape(y);r-=.015
  t0=math.acos(min(1,(x-.05)/r)) if r>x-.05 else 0
  t1=math.acos((x-w)/r)
  edge=[(x-r*math.cos(t0+(t1-t0)*i/12),y,BORE+r*math.sin(t0+(t1-t0)*i/12)) for i in range(13)]
  z=edge[-1][2]
  top=[(w-2*w*i/16,y,z-.22*math.sin(math.pi*i/16)**2) for i in range(1,17)]
  other=[(-xx,yy,zz) for xx,yy,zz in edge[-2::-1]]
  # Solid valley filler, with an actual soldered-seat curved lower face.
  loops.append(edge+top+other)
 # Identical loop cardinality is required despite the vanishing breech valley.
 assert len({len(p) for p in loops})==1
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
 lathe('Bead_Foot',[(52.1,0),(52.1,1),(53.4,1),(53.4,0)],'brass','Barrels',axis='Z',center=(0,766),n=24)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1.3,location=(0,766,54.7))
 ob=bpy.context.object;ob.name='Front_Bead';ob.data.materials.append(MAT['brass'])
 ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4);reg(ob,'Barrels')

STOCK=[(-299,21.3,-117,-5),(-298.4,21.3,-117,-5),(-294,21.8,-115,-4),
 (-275,22.1,-107,-1),(-245,22.0,-91,4),(-210,21.6,-73,9),(-175,20.9,-54,13),
 (-145,19.9,-40,16),(-122,18.8,-31,18),(-106,17.5,-25,18.7),
 (-88,16.2,-21,18.7),(-65,16.2,-19.5,19.0),(-38,16.0,-20.5,19.2),
 (-15,16.1,-20.5,18.5),(0,16.4,-19,20),(12,17.0,-14,26),(25,17.8,-10,31),
 (45,19.6,-3,41),(60,22.0,3,50),(70,23.0,4,53),(76,23.0,5,53.5)]
def head_section(y,theta):
 yy=max(70,y);w,bot,top=action_section(yy)
 outline=[(-w*math.cos(math.pi*i/64),action_roof(-w*math.cos(math.pi*i/64),yy)-max(0,70-y)*.45) for i in range(65)]
 outline += [(w,bot+7)]
 outline += [(w-7+7*math.cos(math.pi/2*i/12),bot+7-7*math.sin(math.pi/2*i/12)) for i in range(1,13)]
 outline += [(-w+7,bot)]
 outline += [(-w+7-7*math.sin(math.pi/2*i/12),bot+7-7*math.cos(math.pi/2*i/12)) for i in range(1,13)]
 c=Vector((0,(bot+top)/2));d=Vector((math.cos(theta),math.sin(theta)))
 hits=[]
 for aa,bb in zip(outline,outline[1:]+outline[:1]):
  a=Vector(aa)-c;e=Vector(bb)-Vector(aa);den=d.x*e.y-d.y*e.x
  if abs(den)<1e-8:continue
  t=(a.x*e.y-a.y*e.x)/den;u=(a.x*d.y-a.y*d.x)/den
  if t>0 and 0<=u<=1:hits.append(t)
 assert hits
 margin=-.35
 return c+d*(min(hits)+margin)
def wood_loop(y,w,bottom,top,n=40,p=2.25):
 loop=[]
 p=p+(4.5-p)*max(0,min(1,(y-25)/40))
 for i in range(n):
  t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
  x=w*math.copysign(abs(c)**(2/p),c)
  # A narrower comb rolls into full cheeks and an oval wrist, independently
  # of the lengthwise silhouette. Butt pitch fades forward.
  x*=1-.16*max(0,s)**4*(1-max(0,min(1,(y-25)/40)))
  z=(top+bottom)/2+(top-bottom)/2*math.copysign(abs(s)**(2/2.15),s)
  yy=y+.075*(-5-z)*max(0,min(1,(-275-y)/24))
  blend=max(0,min(1,(y-25)/35));blend=blend*blend*(3-2*blend)
  if blend:
   hx,hz=head_section(y,t);x=x*(1-blend)+hx*blend;z=z*(1-blend)+hz*blend
  loop.append((x,yy,z))
 return loop
def wood():
 ob=M.loft('Stock_Walnut',[wood_loop(*r) for r in STOCK],MAT['wood']);subd(ob,2)
 # Tang seats are machined after sculpting so there are no voxel lips.
 for name in ('Top_Strap','Trigger_Plate'):
  src=next(p for p in PARTS if p.name==name);tool=src.copy();tool.data=src.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 body=next(p for p in PARTS if p.name=='Action_Body');tool=body.copy();tool.data=body.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 for x,y in [(2.6,64),(-2.6,31)]:cutbox(ob,(x-4.1,y-9,-9),(x+4.1,y+12,12))
 high_copy(ob);reduce(ob,6700);reg(ob)
 loops=[]
 for y,s in [(-299,1),(-299.5,1.002),(-303.9,1.001),(-304.6,.996)]:
  loops.append(wood_loop(y,21.3*s,-117,-5,n=64))
 reg(M.loft('Butt_Plate',loops,MAT['plate']),radius=.45)
 for z in (-30,-91):
  y=-304.3+.075*(-5-z)
  lathe('Butt_Screw',[(y,0),(y,2),(y+.35,2),(y+.35,0)],'dark',center=(0,z),n=20)
 # Slim forend: unequal end tapers, broad lower palms and two real barrel
 # channels. Its dense source supplies compound curvature for later baking.
 stations=[(181,14.7,12.0,35.5),(182,15.7,12.0,36),
  (189,17.0,12.0,36.5),(211,17.4,12.6,37),(242,16.8,13.5,37),
  (279,15.5,14.7,37),(314,13.8,16.2,36.5),(341,10.8,20,35),
  (351,7.0,25,33.5),(355,2.5,29,32.5),(356,2,29.5,32)]
 ob=M.loft('Forend_Walnut',[rounded_loop(*r,n=48,p=3.5) for r in stations],MAT['wood']);subd(ob,2)
 for side in (-1,1):
  loops=[]
  for y in (178,240,365):
   x,r=barrel_shape(y);loops.append([(side*x+(r+.25)*math.cos(t),y,BORE+(r+.25)*math.sin(t)) for t in [i*math.tau/64 for i in range(64)]])
  cut(ob,M.loft('Channel tool',loops,MAT['wood']))
 # Iron occupies a real pocket in the lower rear wood.
 cutbox(ob,(-7.2,180,10),(7.2,227,18.5))
 cutbox(ob,(-3.7,178,28),(3.7,365,45))
 cut(ob,lathe('Tool',[(-24,0),(-24,12.25),(24,12.25),(24,0)],axis='X',center=(170,19),n=80,raw=True))
 high_copy(ob);reduce(ob,3300);reg(ob,'Forend')
 # Curved iron cups bear on the shared circular knuckle throughout opening.
 for sign in (-1,1):
  a,b=sorted((sign*7.2,sign*17.0))
  arc_solid('Forend_IronCup_'+('R' if sign>0 else 'L'),a,b,12.15,14.3,-50,52,'dark','Forend',n=44)
 curved_mesh('Forend_Iron',[rounded_loop(y,w,bot,top,p=4,n=24) for y,w,bot,top in
  [(180,6.8,12.0,18.3),(188,7,12,18.3),(215,6.5,12.7,18.3),(226,5.7,13,18.3)]],
  'dark','Forend',level=1,target=450)
 # An inset oval latch in the underside, fixed for this presentation.
 latch=curved_mesh('Forend_Latch',[rounded_loop(y,w,z-1.5,z+1.5,p=3,n=20) for y,w,z in
  [(219,2.2,14),(221,4,13.7),(235,5.2,14.0),(250,4.6,14.5),(255,2.8,15.1)]],
  'blue','Forend',level=1,target=400)
 # Recess the inset latch into both source and game wood.
 for woodpart in [ob]+[h for h in HIGH if h.get('low_target')=='Forend_Walnut']:
  tool=latch.copy();tool.data=latch.data.copy();bpy.context.collection.objects.link(tool);cut(woodpart,tool)
 # Latch backing reaches the iron through a short web inside the wood.
 box('Latch_Web',(-3,218,13),(3,225,18),'dark','Forend',radius=.6)

def controls():
 # Guard is a broad thin steel band with radiused lateral edges, swept along
 # the bow. It joins the lower plate at both ends.
 path=M.bezier((10,-9),(13,-25),(44,-32),(72,-32),24)
 path+=M.bezier((72,-32),(90,-34),(100,-28),(100,-14),18)[1:]
 path+=M.bezier((100,-14),(100,-4),(97,3),(94,7),10)[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  p=Vector(path[max(0,i-1)]);q=Vector(path[min(len(path)-1,i+1)]);d=(q-p).normalized();normal=Vector((-d.y,d.x))
  loop=[]
  # Rounded rectangle section across X; a band, never a round rod.
  for x,v in M.rounded_rectangle(8.2,2.3,.6,4):loop.append((x,y+v*normal.x,z+v*normal.y))
  loops.append(loop)
 guard=reg(M.loft('Trigger_Guard',loops,MAT['blue']),radius=.08)
 tang=curved_mesh('Guard_RearTang',[rounded_loop(y,w,z-1.0,z+1.0,p=3,n=20) for y,w,z in
  [(11,4.1,-9),(0,4.0,-16),(-15,4.0,-20.8),
   (-38,3.8,-21.0),(-65,3.4,-20.1),(-82,2.9,-21.4),(-88,1.7,-22.8)]],
  'blue','Root',level=2,target=400)
 for woodpart in [bpy.data.objects['Stock_Walnut']]+[h for h in HIGH if h.get('low_target')=='Stock_Walnut']:
  tool=tang.copy();tool.data=tang.data.copy();bpy.context.collection.objects.link(tool);cut(woodpart,tool)

 for name,x,y,bone in [('Front_Trigger',2.6,64,'Trigger'),('Rear_Trigger',-2.6,31,'TriggerRear')]:
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
 # A swept forging: substantial spindle shank and tilted thumbpiece seated
 # against the strap. Checkering belongs to the later normal map.
 loops=[]
 for y,x,w,z,h in [(97,0,4.6,55.4,1.8),(95,0,4.8,55.5,1.8),
  (89,.3,4.2,54.6,1.8),(81,1.2,3.6,53.2,2.3),
  (73,3.1,5.2,51.6,2.5),(64,6,7.5,49.7,3.0),
  (57,7.7,8.3,48.2,3.4),(53,8.5,7.8,47.7,3.3),
  (50.5,8.7,5.5,46.0,2.6),(50,8.7,4.8,46.0,2.2)]:
  loops.append([(xx+x,yy,zz) for xx,yy,zz in rounded_loop(y,w,z-h,z+h,p=3.0,n=32)])
 ob=M.loft('Top_Lever',loops,MAT['blue']);subd(ob,2)
 for v in ob.data.vertices:v.co.z+=2.15*max(0,min(1,(89-v.co.y)/18))
 high_copy(ob);reduce(ob,1150);reg(ob,'TopLever')
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
 allocations={'Stock_Walnut':4200,'Forend_Walnut':2350,'Action_Body':4800,
  'Barrel_Hook':650,'Breech_Lumps':700,
  'Forend_IronCup_R':500,'Forend_IronCup_L':500,'Trigger_Guard':1100,
  'Butt_Plate':650,'Extractor_Rim_R':350,'Extractor_Rim_L':350,
  'Front_Trigger':650,'Rear_Trigger':650,'Top_Strap':700,'Tang_Safety':450}
 target=allocations.get(ob.name,130 if ob.name.startswith(('Hinge_Head','Action_CrossPin')) else None)
 if target:reduce(ob,target)
 # Collapse can expose a tiny Boolean corner at the lever bore. Repair only
 # isolated sub-half-millimeter triangular boundaries after the final reduction.
 clean(ob,dist=.006)
 tri=ob.modifiers.new('Explicit game triangles','TRIANGULATE');tri.keep_custom_normals=True
 if ob.name=='Front_Bead':tri.quad_method='FIXED'
 M.apply(ob)
 if ob.name=='Front_Bead':
  # BMesh may return the same triangles in a different face order. Packed
  # loop-normal bases depend on that order, so canonicalize this symmetric
  # sphere before writing its analytic normals.
  mesh=ob.data;coordinates=[v.co.copy() for v in mesh.vertices];faces=[]
  for f in mesh.polygons:
   ids=list(f.vertices);i=ids.index(min(ids));faces.append(ids[i:]+ids[:i])
  mesh.clear_geometry();mesh.from_pydata(coordinates,[],sorted(faces));mesh.update();M.smooth(ob,45)
 if ob.name=='Action_Body':
  ob.data.normals_split_custom_set([(0,0,0)]*len(ob.data.loops));M.smooth(ob,42)
  m=ob.modifiers.new('Reseed forged and machined fields','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=40;M.apply(ob)
 normals=[n.vector.copy() for n in ob.data.corner_normals]
 if 'tube_axis_sign' in ob:
  sign=ob['tube_axis_sign']
  for f in ob.data.polygons:
   for j in f.loop_indices:
    p=ob.data.vertices[ob.data.loops[j].vertex_index].co
    if abs(f.normal.x)>.98 and all(abs(v.co.x)<.001 for v in [ob.data.vertices[i] for i in f.vertices]):
     normals[j]=f.normal.copy()
    elif abs(f.normal.y)<.2:
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
   if abs(f.normal.x)>.96 and abs(f.normal.z)<.18 and all(p.y>116 for p in vs):
    for j in f.loop_indices:
     p=ob.data.vertices[ob.data.loops[j].vertex_index].co
     normals[j]=Vector((math.copysign(1,p.x),.045 if p.y<157 else 0,0)).normalized()
   if abs(f.normal.y)<.95 and f.normal.z>.15 and all(70<=p.y<=115 and abs(p.z-action_roof(p.x,p.y))<.65 for p in vs):
    values=[]
    for j in f.loop_indices:
     p=ob.data.vertices[ob.data.loops[j].vertex_index].co
     yy=max(70.01,min(114.99,p.y));w=action_section(yy)[0];xx=max(-w+.03,min(w-.03,p.x))
     dx=(action_roof(xx+.02,yy)-action_roof(xx-.02,yy))/.04
     dy=(action_roof(xx,yy+.02)-action_roof(xx,yy-.02))/.04
     values.append(Vector((-dx,-dy,1)).normalized())
    for j,n in zip(f.loop_indices,values):normals[j]=n
 if ob.name=='Front_Bead':
  for j in range(len(normals)):
   p=ob.data.vertices[ob.data.loops[j].vertex_index].co
   normals[j]=(p-Vector((0,766,54.7))).normalized()
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
 eye.rotation_euler.x=math.atan2(54.7-EYE[2],766-EYE[1])
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
