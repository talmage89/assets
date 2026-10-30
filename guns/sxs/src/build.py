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
def smoothstep(v):
 v=max(0,min(1,v));return v*v*(3-2*v)
# Exterior visual form, in mm. Photo-scale estimates are in refs/SOURCES.md.
ACTION_HALF_WIDTH=25.95
BOTTOM_RADIUS=8.0
FENCE_RADIUS=13.35
FENCE_ROLL=18.5
SLOT_WIDTH=6.0
HEAD_TOP=49.72
HEAD_CENTER_FLOOR=55.59
HEAD_SIDE_RADIUS=6.0
HEAD_INNER_OFFSET=.68

def action_section(y):
 """One ground side plane from the stock head through the hinge cheeks."""
 if y<=115:
  return (ACTION_HALF_WIDTH,5-5*smoothstep((y-70)/45),47.2+.12*(y-94))
 if y<170:
  return (ACTION_HALF_WIDTH,7*smoothstep((y-115)/55),30.2)
 return (ACTION_HALF_WIDTH,19-math.sqrt(max(0,144-(y-170)**2)),19+math.sqrt(max(0,144-(y-170)**2)))
def head_base_6(x,y):
 """Z55.59 center, 8 mm center half-width, R6 side, Y85–94 return."""
 xx=abs(x)
 if y<=85:z=47.2+.12*(y-94)
 elif y<94:
  t=(y-85)/9
  z=(2*t**3-3*t*t+1)*46.12+(t**3-2*t*t+t)*1.08+(-2*t**3+3*t*t)*HEAD_TOP
 else:z=HEAD_TOP
 z+=(HEAD_CENTER_FLOOR-HEAD_TOP)*(1-smoothstep(xx/8))*smoothstep((y-85)/9)
 r=HEAD_SIDE_RADIUS;u=max(0,min(1,(xx-(ACTION_HALF_WIDTH-r))/r))
 return z-r*(1-math.sqrt(max(0,1-u*u)))

def front_arc_8(x,d):
 """R13.35 concentric front, L18.5 crown curvature, 1 mm join distance."""
 xx=abs(x);base=head_base_6(x,115-d);radius=FENCE_RADIUS*math.sqrt(max(0,1-(d/FENCE_ROLL)**2))
 dx=xx-barrel_shape(115-d)[0];arc=BORE+math.sqrt(max(0,radius*radius-dx*dx))
 lo=max(base,arc if abs(dx)<radius else base);hi=max(base,BORE+radius)+1
 for _ in range(25):
  mid=(lo+hi)*.5;a=mid-base;b=math.hypot(dx,mid-BORE)-radius
  h=max(0,1-abs(a-b));f=min(a,b)-h**3/6
  if f>0:hi=mid
  else:lo=mid
 return (lo+hi)*.5

_HEAD_PROFILES={}
def action_roof(x,y):
 """Front 8 mm circles; monotone degree-5 return ending at 18.5 mm on bore.

 Rear endpoint shifts .68 mm per transverse mm inward. The last three
 Bezier controls are zero, so height, slope and curvature reach the head
 together. Positive ordered controls prevent secondary rear folds.
 """
 d=max(0,115-y);base=head_base_6(x,y)
 if d<=8:return front_arc_8(x,d)
 key=round(abs(x),6)
 if key not in _HEAD_PROFILES:
  length=FENCE_ROLL+HEAD_INNER_OFFSET*(12.6-abs(x))-8
  e=.02;z=front_arc_8(x,8);background=head_base_6(x,107)
  a=max(0,z-background);slope=(front_arc_8(x,8+e)-front_arc_8(x,8-e))/(2*e)
  curvature=(front_arc_8(x,8+e)-2*z+front_arc_8(x,8-e))/e**2
  c1=max(0,min(a,a+slope*length/5))
  c2=max(0,min(c1,a+2*slope*length/5+curvature*length**2/20))
  _HEAD_PROFILES[key]=(length,a,c1,c2)
 length,a,c1,c2=_HEAD_PROFILES[key];t=max(0,min(1,(d-8)/length));u=1-t
 return base+a*u**5+5*c1*t*u**4+10*c2*t*t*u**3

def upper_normals(ob,normals=None):
 """Differentiate the Z55.59/R6/degree-5 field; retain the flat breech face."""
 normals=normals or [n.vector.copy() for n in ob.data.corner_normals]
 for face in ob.data.polygons:
  if face.normal.z<.01:continue
  for i in face.loop_indices:
   p=ob.data.vertices[ob.data.loops[i].vertex_index].co
   if not 70.01<p.y<114.99 or abs(p.z-action_roof(p.x,p.y))>.10:continue
   if abs(p.x)>ACTION_HALF_WIDTH-.015:n=Vector((math.copysign(1,p.x),0,0))
   else:
    e=.003
    dx=(action_roof(p.x+e,p.y)-action_roof(p.x-e,p.y))/(2*e)
    dy=(action_roof(p.x,p.y+e)-action_roof(p.x,p.y-e))/(2*e)
    n=Vector((-dx,-dy,1)).normalized()
   if n.dot(face.normal)>.4:normals[i]=n
 return normals
def lower_loop(y,w,bot,r):
 """Shared transverse skin: plate and bar use exactly the same lower arris."""
 pts=[(w,y,bot+r)]
 pts += [(w-r+r*math.cos(math.pi/2*i/10),y,bot+r-r*math.sin(math.pi/2*i/10)) for i in range(1,11)]
 pts += [(-w+r,y,bot)]
 pts += [(-w+r-r*math.sin(math.pi/2*i/10),y,bot+r-r*math.cos(math.pi/2*i/10)) for i in range(1,11)]
 return pts
def lower_normals(ob,normals=None):
 """Continuous forged lower skin across the independent plate joint.

 A planar end cap at that joint must not pull the outer roll's normals.
 Evaluate the original 8 mm arris and rising belly, in modeling millimeters.
 """
 normals=normals or [n.vector.copy() for n in ob.data.corner_normals]
 for face in ob.data.polygons:
  if face.normal.z>-.12:continue
  for i in face.loop_indices:
   p=ob.data.vertices[ob.data.loops[i].vertex_index].co
   if not 70.01<p.y<169.9:continue
   w,bot,_=action_section(p.y);dx=max(0,abs(p.x)-(w-BOTTOM_RADIUS))
   if dx>BOTTOM_RADIUS:continue
   cos=math.sqrt(max(0,1-(dx/BOTTOM_RADIUS)**2))
   z=bot+BOTTOM_RADIUS*(1-cos)
   if abs(p.z-z)>.08:continue
   t=max(0,min(1,(p.y-70)/45 if p.y<=115 else (p.y-115)/55))
   slope=(-5/45 if p.y<=115 else 7/55)*6*t*(1-t)
   n=Vector((math.copysign(dx/BOTTOM_RADIUS,p.x),slope*cos,-cos)).normalized()
   if n.dot(face.normal)>.85:normals[i]=n
 return normals
def rear_seam(z,x=0):
 # Forward wood fingers beside the central strap; a shorter upper head
 # whose rear seam returns gently around the narrow root of the strap.
 return (15+10*smoothstep((abs(x)-8)/12))*smoothstep((z-15)/15)
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
 boundary=set(e for e in bm.edges if e.is_boundary)
 while boundary:
  group={boundary.pop()};queue=list(group)
  while queue:
   e=queue.pop()
   for v in e.verts:
    for adjacent in v.link_edges:
     if adjacent in boundary:
      boundary.remove(adjacent);group.add(adjacent);queue.append(adjacent)
  if len(group)==3 and max(e.calc_length() for e in group)<.8:
   edge=max(group,key=lambda e:e.calc_length());a,c=[v.co.copy() for v in edge.verts]
   middle=next(v for e in group for v in e.verts if v not in edge.verts)
   t=(middle.co-a).dot(c-a)/(c-a).length_squared
   if 0<t<1 and (middle.co-(a+(c-a)*t)).length<.006:
    # Close a sub-.8 mm Boolean T-junction on the planar breech by
    # splitting its long edge at the existing third point, not by
    # manufacturing a zero-area triangle across three collinear points.
    from bmesh.utils import edge_split
    _,vertex=edge_split(edge,edge.verts[0],t);vertex.co=middle.co.copy()
    bmesh.ops.remove_doubles(bm,verts=[vertex,middle],dist=.006)
   else:bmesh.ops.holes_fill(bm,edges=list(group),sides=3)
 for _ in range(64):
  edges=[e for e in bm.edges if e.is_boundary and e.calc_length()<(1.2 if ob.name in ('Action_Body','HIGH_Action_Body') else .8)
   and (ob.name in ('Action_Body','HIGH_Action_Body') or all(abs(v.co.y-115)<.01 for v in e.verts))]
  vertices={v for e in edges for v in e.verts};repair=None
  for e in edges:
   a,c=[v.co.copy() for v in e.verts];delta=c-a
   if delta.length_squared<1e-12:continue
   for v in vertices-set(e.verts):
    t=(v.co-a).dot(delta)/delta.length_squared
    if .001<t<.999 and (v.co-(a+delta*t)).length<.006:
     repair=e,v,t;break
   if repair:break
  if not repair:break
  e,v,t=repair
  from bmesh.utils import edge_split
  _,new=edge_split(e,e.verts[0],t);new.co=v.co.copy()
  bmesh.ops.remove_doubles(bm,verts=[new,v],dist=.006)
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
  canonical_surface(ob)
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
 # A single closed ruled forging. The ground faces are explicit planes and
 # the fences use circular transverse sections and a short axial roll. The knuckle continues the same
 # skin; there is no overlapping cylinder/disc to stand proud of the lands.
 loops=[]
 ys=[70+i*.5 for i in range(91)]
 xs=lambda w,y:sorted([w*math.sin(-math.pi/2+math.pi*i/96) for i in range(97)]+[-barrel_shape(y)[0],barrel_shape(y)[0]])
 for y in ys:
  w,bot,top=action_section(y);pts=[]
  for x in xs(w,y):
   z=action_roof(x,y)
   yy=y+rear_seam(z,x)*max(0,1-(y-70)/30)
   # Evaluate the plane at the actual station to retain a perfectly ground
   # shoulder after shortening the head beside the top strap.
   if abs(abs(x)-w)<.001 or abs(abs(x)-(w-4))<.001:
    x+=math.copysign(action_section(yy)[0]-w,x)
   z=action_roof(x,yy)
   pts.append((x,yy,z))
  pts += lower_loop(y,w,bot,BOTTOM_RADIUS)
  loops.append(pts)
 # Standing breech is the planar step to the low water table. Small edge
 # radii are retained in the dense source for the later normal-map transfer.
 for y in [115.001,116,122,130,140,148,154,160,166,170]+[170+12*math.sin(math.pi/2*i/16) for i in range(1,16)]+[181.99]:
  w,bot,top=action_section(y)
  if y<170:top=30.2+.8*smoothstep((y-150)/20)
  r=min(4,(top-bot)/3)
  rb=min(BOTTOM_RADIUS,(top-bot)*.48)
  pts=[]
  for x in xs(w,y):
   dx=max(0,abs(x)-(w-r))
   z=top-r+math.sqrt(max(0,r*r-dx*dx));pts.append((x,y,z))
  pts += lower_loop(y,w,bot,rb)
  loops.append(pts)
 nc=len(loops[0]);vs=[p for loop in loops for p in loop]
 fs=[(j*nc+i,j*nc+(i+1)%nc,(j+1)*nc+(i+1)%nc,(j+1)*nc+i) for j in range(len(loops)-1) for i in range(nc)]
 center=len(vs);vs.append((0,78,27.5));fs += [(center,(i+1)%nc,i) for i in range(nc)]
 fs += [tuple(range((len(loops)-1)*nc,len(loops)*nc))]
 body=M.mesh('Action_Body',vs,fs,MAT['blue']);clean(body)
 # The narrow visual lug passage opens on the table; its bottom remains
 # closed by the forging so the underside shows the smooth neck in the photo.
 cutbox(body,(-6.4,116,6.3),(6.4,184,33))
 cut(body,lathe('Hinge bore',[(-28,0),(-28,4.15),(28,4.15),(28,0)],axis='X',center=(170,19),n=50,raw=True))
 for side,x in [('R',12.6),('L',-12.6)]:
  cut(body,lathe('Tool',[(113.9,0),(113.9,3.5),(116,3.5),(116,0)],center=(x,BORE),n=32,raw=True))
  lathe('Bushing_'+side,[(114,1),(114,3.35),(114.95,3.35),(114.95,1)],'steel',center=(x,BORE),n=32,closed=True)
  lathe('PinFace_'+side,[(114.6,0),(114.6,.8),(114.85,.8),(114.85,0)],'dark',center=(x,BORE),n=16)
 cutbox(body,(-4.4,98,10),(4.4,146,15.1))
 cut(body,lathe('Tool',[(44,0),(44,4.35),(56,4.35),(56,0)],axis='Z',center=(0,94),n=48,raw=True))
 cutbox(body,(-7.4,39,-5),(7.4,78,11))
 reg(body,radius=.18,segments=2)
 # Condition coincident constructive seams before archiving or reduction;
 # the same 6 micrometer weld is used on the final game surface below.
 clean(body,dist=.006);canonical_surface(body)
 lathe('Hinge_Pin',[(-25.95,0),(-25.95,4.04),(-25.80,4.10),(25.80,4.10),(25.95,4.04),(25.95,0)],'blue',axis='X',center=(170,19),n=48)
 for side in (-1,1):
  for y,z,r in [(79,14,2.7),(102,19,2.2)]:screw('Action_CrossPin',side*(action_section(y)[0]-.15),y,z,r)
 # The strap alone continues behind the short upper body. Its slope also
 # seats the new low tapered lever through the complete 25-degree swing.
 curved_mesh('Top_Strap',[rounded_loop(y,w,z-1.1,z+1.1,p=5,n=24) for y,w,z in
  [(-27,3.4,18.8),(-26,4,18.9),(-10,5.8,18.8),(9,7,23.2),(28,7.7,31.0),(50,8,38.5),(72,8.8,43.4),(94,8.8,46.1)]],
  'blue','Root',level=2,target=950)
 strap=PARTS[-1]
 cut(strap,lathe('Spindle seat',[(44,0),(44,4.35),(56,4.35),(56,0)],axis='Z',center=(0,94),n=48,raw=True))
 # The trigger plate's forward lower skin is identical to the forging's.
 # Seat it before archiving the action source: the only exterior break is
 # a 0.10 mm joint. Its forward seam curves back toward the outer sides.
 loops=[]
 specs=[(-22,3.2,-13.4),(-20,4,-12.9),(5,6,-6.9),(27,9.5,1.1),
  (48,16,3.6),(60,22,4.3),(70,ACTION_HALF_WIDTH,5),
  *[(y,ACTION_HALF_WIDTH,None) for y in (70.8,74,80,86,90,92,96,99,100,102,103)]]
 for y,w,bot in specs:
  if bot is None:bot=action_section(y)[1]
  r=min(BOTTOM_RADIUS,w*.7,1.2+6.8*smoothstep((y-27)/43))
  pts=[(-w,y,bot+r+.6),(w,y,bot+r+.6)]+lower_loop(y,w,bot,r)
  if y>=80:
   shift=lambda x:4*(abs(x)/w)**4*smoothstep((y-80)/23)
   pts=[(x,y-shift(x),action_section(y-shift(x))[1]+z-bot) for x,_,z in pts]
  loops.append(pts)
 plate=M.loft('Trigger_Plate',loops,MAT['blue']);clean(plate)
 seat=plate.copy();seat.data=plate.data.copy();bpy.context.collection.objects.link(seat)
 for i,v in enumerate(seat.data.vertices):
  v.co.x*=1.002;v.co.y+=.10
  v.co.z+=.10 if i%len(loops[0])<2 else -2.0
 cut(body,seat)
 # Keep the archive synchronized after cutting the real plate seat.
 clean(body,dist=.006);canonical_surface(body)
 body.data.normals_split_custom_set(upper_normals(body,lower_normals(body)));high_copy(body)
 HIGH[-1]['source_method']='Single field: Z55.59 center, R6 side, degree-5 rear return, R13.35/L18.5 front crowns'
 # Keep the head dense until the recess and its R0.60 lip are cut;
 # one final reduction avoids Boolean cuts through a sparse rim.
 for x,y in [(2.6,64),(-2.6,31)]:
  outline=[(xx+x,yy+y+3) for xx,yy in M.rounded_rectangle(SLOT_WIDTH,16,.9,6)]
  cut(plate,profile('Blade slot',outline,-8,18,axis='Z',raw=True))
 reg(plate)
 plate.data.normals_split_custom_set(lower_normals(plate))
 high_copy(plate)
 box('Locking_Shoe',(-4,124,10.4),(4,129.9,11.8),'steel','LockBolt',radius=.10)
 box('Locking_Shoe_Upper',(-4,130,13.2),(4,141.9,14.6),'steel','LockBolt',radius=.10)

def lever_recess_R590():
 """R5.90 fore wall around R5.60 boss; Y94–78 Bezier flare for 25° swing.

 One closed cutter avoids the tangent intersection of a cylinder and a
 separate swept hull. Its floor is Z48 at the boss, falling .22 mm/mm
 rearward. The R0.60 upper lip is cut after this single Boolean.
 """
 r=5.9
 outline=[(r*math.cos(t),94+r*math.sin(t)) for t in [math.pi*i/64 for i in range(65)]]
 outline+=M.bezier((-r,94),(-r,90),(-7,85),(-8.5,82),18)[1:]
 outline+=[(15,78)]
 outline+=M.bezier((15,78),(10,83),(r,90),(r,94),24)[1:-1]
 # Construct the R0.60 circular lip in each perimeter-normal plane,
 # tangent to the actual head roof. A C1 Y88–92 taper joins the strap.
 profiles=[]
 for i,(x,y) in enumerate(outline):
  tangent=Vector(outline[(i+1)%len(outline)])-Vector(outline[i-1])
  n=Vector((tangent.y,-tangent.x)).normalized()
  radius=.60*smoothstep((y-88)/4)
  radius=max(.0001,radius)
  roof=lambda distance:action_roof(x+n.x*distance,y+n.y*distance)
  derivative=lambda distance:(roof(distance+.003)-roof(distance-.003))/.006
  lo=0;hi=radius*2
  for _ in range(22):
   distance=(lo+hi)*.5;q=derivative(distance)
   if distance-radius+radius*q/math.sqrt(1+q*q)>0:hi=distance
   else:lo=distance
  distance=(lo+hi)*.5;q=derivative(distance)
  zc=roof(distance)-radius/math.sqrt(1+q*q)
  end=math.atan2(1,-q)
  arc=[]
  for j in range(13):
   angle=math.pi+(end-math.pi)*j/12
   offset=radius*(1+math.cos(angle))
   arc.append((x+n.x*offset,y+n.y*offset,zc+radius*math.sin(angle)))
  profiles.append([(x,y,48+.22*min(0,y-94)),*arc,(arc[-1][0],arc[-1][1],65)])
 loops=[list(row) for row in zip(*profiles)]
 template=M.loft('Recess R5.90 lip R0.60',loops,MAT['blue']);clean(template)
 for name in ('Action_Body','HIGH_Action_Body'):
  tool=template.copy();tool.data=template.data.copy();bpy.context.collection.objects.link(tool)
  target=bpy.data.objects[name];cut(target,tool);clean(target,dist=.006)
 bpy.data.objects.remove(template,do_unlink=True)

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
 def rib_center(y,w):
  x,r=barrel_shape(y);return BORE+math.sqrt((r-.015)**2-(x-w)**2)-.22
 rib_rear=rib_center(115,6.4);rib_front=rib_center(775.4,4.2)
 loops=[]
 for y,w in [(115,6.4),(116,6.4),(185,5.8),(240,5.3),(500,4.7),(774.8,4.2),(775.4,4.2)]:
  x,r=barrel_shape(y);r-=.015
  t0=math.acos(min(1,(x-.05)/r)) if r>x-.05 else 0
  t1=math.acos((x-w)/r)
  edge=[(x-r*math.cos(t0+(t1-t0)*i/12),y,BORE+r*math.sin(t0+(t1-t0)*i/12)) for i in range(13)]
  z=rib_rear+(rib_front-rib_rear)*(y-115)/660.4+.22
  top=[(w-2*w*i/16,y,z-.22*math.sin(math.pi*i/16)**2) for i in range(1,17)]
  other=[(-xx,yy,zz) for xx,yy,zz in edge[-2::-1]]
  # Solid valley filler, with an actual soldered-seat curved lower face.
  loops.append(edge+[(w,y,z)]+top+[(-w,y,edge[-1][2])]+other)
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
 w,bot,top=action_section(max(70,y));t=theta;c=math.cos(t);sn=math.sin(t)
 x=(w-.35)*math.copysign(abs(c)**(2/4.5),c)
 z=(bot+top)/2+(top-bot)/2*math.copysign(abs(sn)**(2/3.2),sn)
 z=min(z,47.2+.12*(y-94)-.82*max(0,abs(x)-6.5)-.2)
 return x,z
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
   hx,hz=head_section(y,t)
   # The seam warps the cage station forward. Match its section at that
   # actual station rather than retaining the narrower unwarped head.
   for _ in range(3):hx,hz=head_section(y+rear_seam(hz,hx)*smoothstep((y-25)/45),t)
   x=x*(1-blend)+hx*blend;z=z*(1-blend)+hz*blend
  yy+=rear_seam(z,x)*smoothstep((y-25)/45)
  loop.append((x,yy,z))
 return loop
def wood():
 ob=M.loft('Stock_Walnut',[wood_loop(*r) for r in STOCK],MAT['wood']);subd(ob,2)
 # Tang seats are machined after sculpting so there are no voxel lips.
 for name in ('Top_Strap','Trigger_Plate'):
  src=next(p for p in PARTS if p.name==name);tool=src.copy();tool.data=src.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 body=next(p for p in PARTS if p.name=='Action_Body');tool=body.copy();tool.data=body.data.copy();bpy.context.collection.objects.link(tool);cut(ob,tool)
 for x,y in [(2.6,64),(-2.6,31)]:cutbox(ob,(x-3.3,y-9,-9),(x+3.3,y+12,12))
 # A small clearance at the front of the head's well removes the unsupported
 # wood feather that an exactly matching metal-well rim would otherwise leave.
 cutbox(ob,(-7.6,76.5,8.5),(7.6,79,12))
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
 stations=[(181.5,15.7,12.0,36.2),(181.8,15.7,12.0,36.2),
  (184,17.2,12.0,36.2),(189,17.2,12.0,36.2),(211,17.2,12.6,36.2),
  (242,16.4,14.8,36.2),(279,15.35,17.3,36.2),(314,14.3,19.6,36.2),
  (340,13.53,21.43,36.2),(341,13.5,21.5,36.2),(342,13.4,22.25,36.2),(351,12.5,29.0,36.2),(354.2,11.5,32.3,36.2),
  (354.5,11.5,32.3,36.2)]
 loops=[]
 for y,w,bot,top in stations:
  loops.append([(x,y,z+(bot+top)/2) for x,z in M.rounded_rectangle(w*2,top-bot,min(1.6,(top-bot)/3),6)])
 ob=M.loft('Forend_Walnut',loops,MAT['wood']);subd(ob,2)
 bounds=[(min(v.co[k] for v in ob.data.vertices),max(v.co[k] for v in ob.data.vertices)) for k in range(3)]
 for v in ob.data.vertices:
  for k,(lo,hi,target_lo,size) in enumerate([(bounds[0][0],bounds[0][1],-17.2,34.4),(bounds[1][0],bounds[1][1],181.5,173),(bounds[2][0],bounds[2][1],12,24.2)]):
   v.co[k]=target_lo+(v.co[k]-lo)*size/(hi-lo)
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
 path+=M.bezier((100,-14),(98,-2),(88,7),(74,7),10)[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  p=Vector(path[max(0,i-1)]);q=Vector(path[min(len(path)-1,i+1)]);d=(q-p).normalized();normal=Vector((-d.y,d.x))
  loop=[]
  # Rounded rectangle section across X; a band, never a round rod.
  for x,v in M.rounded_rectangle(12.4*(.64+.36*smoothstep((y-13)/25)),1.65,.22,3):loop.append((x,y+v*normal.x,z+v*normal.y))
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
 # Measured from top/side plain dealer photographs (see SOURCES): narrow
 # tapered tail lies just above the strap. Pivot and accepted travel unchanged.
 loops=[]
 for y,x,w,z,h in [(99,0,3.0,49.0,1.15),(98,0,4.1,49,1.15),
  (94,0,4.5,48.9,1.15),(89,0,3.6,48.2,1.1),(83,0,2.8,47.0,1.0),
  (72,.1,2.4,44.9,.95),(58,.3,2.7,42.1,.95),(44,.6,3.5,39.0,1.0),
  (30,.6,3.8,33.1,1.0),(22,.6,2.9,29.2,.85),(20.5,.6,1.5,28.6,.7)]:
  loops.append([(xx+x,yy,zz) for xx,yy,zz in rounded_loop(y,w,z-h,z+h,p=4.5,n=32)])
 ob=M.loft('Top_Lever',loops,MAT['blue']);subd(ob,2)
 for v in ob.data.vertices:v.co.z+=1.2
 high_copy(ob);reduce(ob,1300);reg(ob,'TopLever')
 # The accepted lever tail had a 0.062 mm visual overlap at Y21. The
 # new strict separation audit requires a real 0.20 mm local wood seat.
 for angle in range(7):
  for target in (bpy.data.objects['Stock_Walnut'],bpy.data.objects['HIGH_Stock_Walnut'],bpy.data.objects['Top_Strap']):
   if angle>3 and target.name!='Top_Strap':continue
   tool=ob.copy();tool.data=ob.data.copy();bpy.context.collection.objects.link(tool)
   for v in tool.data.vertices:v.co+=v.normal*.20
   pivot=Vector((0,94,0));rot=Matrix.Rotation(math.radians(angle),3,'Z')
   for v in tool.data.vertices:v.co=rot@(v.co-pivot)+pivot
   cut(target,tool);clean(target,dist=.006)
 lathe('Top_LeverSpindle',[(45.5,0),(45.5,4.1),(48.25,4.1),(48.35,5.6),(50.0,5.6),(50.3,5.3),(50.3,0)],'dark','TopLever',axis='Z',center=(0,94),n=48)
 lever_recess_R590()
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

def canonical_surface(ob):
 """Stable corner bases for deterministic sculpt-normal transfer.

 Boolean/decimation can enumerate equivalent faces in different orders.
 Blender packs custom normals in a corner basis: canonical source and target
 ordering makes that basis and nearest-face ties reproducible. Coordinates
 are snapped to a 1 micrometer modeling grid before reduction, preventing
 submicrometer Boolean roundoff from changing equal-cost collapse choices.
 """
 old=ob.data;coords=[tuple(round(x,3) for x in v.co) for v in old.vertices]
 ordered=sorted(set(coords));indices={p:i for i,p in enumerate(ordered)};mapping={i:indices[p] for i,p in enumerate(coords)};faces=[]
 for f in old.polygons:
  ids=[mapping[i] for i in f.vertices];ids=[v for i,v in enumerate(ids) if v!=ids[i-1]]
  if len(set(ids))<3:continue
  k=ids.index(min(ids));faces.append(ids[k:]+ids[:k])
 me=bpy.data.meshes.new(old.name+'_ordered');me.from_pydata(ordered,[],sorted(faces));me.update()
 for mat in old.materials:me.materials.append(mat)
 ob.data=me
 if old.users==0:bpy.data.meshes.remove(old)
 M.smooth(ob,42)

def finalize(ob):
 clean(ob)
 if not len(ob.data.vertices):raise AssertionError('Empty manufactured part: '+ob.name)
 # Only silhouette-scale detail survives in the game mesh. In particular,
 # annular-section edge bevels must not consume thousands of hidden triangles.
 allocations={'Stock_Walnut':4200,'Forend_Walnut':2350,'Action_Body':7750,
  'Barrel_Hook':650,'Breech_Lumps':700,
  'Forend_IronCup_R':500,'Forend_IronCup_L':500,'Trigger_Guard':1100,
  'Butt_Plate':650,'Extractor_Rim_R':350,'Extractor_Rim_L':350,
  'Front_Trigger':650,'Rear_Trigger':650,'Top_Strap':1100,'Tang_Safety':450}
 target=allocations.get(ob.name,130 if ob.name.startswith(('Hinge_Head','Action_CrossPin')) else None)
 if target:reduce(ob,target)
 # Collapse can expose a tiny Boolean corner at the lever bore. Repair only
 # isolated sub-half-millimeter triangular boundaries after the final reduction.
 clean(ob,dist=.006)
 if ob.name in ('Action_Body','Stock_Walnut','Forend_Walnut'):canonical_surface(ob)
 tri=ob.modifiers.new('Explicit game triangles','TRIANGULATE');tri.keep_custom_normals=True
 if ob.name=='Front_Bead':tri.quad_method='FIXED'
 M.apply(ob)
 if ob.name=='Action_Body':clean(ob,dist=.006)
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
 if ob.name in ('Stock_Walnut','Forend_Walnut','Action_Body'):
  high=next(h for h in HIGH if h.get('low_target')==ob.name)
  canonical_surface(ob);canonical_surface(high)
  if ob.name=='Action_Body':high.data.normals_split_custom_set(upper_normals(high,lower_normals(high)))
  if ob.name=='Forend_Walnut':
   # The routed latch intersects the broad lower land. Its wall must not
   # pull the exterior's normals into a star around the cut. Preserve the
   # dense source's measured land normals on those nearly planar polygons;
   # retain smooth normals on the carved corners and the slanted nose.
   hn=[n.vector.copy() for n in high.data.corner_normals]
   for f in high.data.polygons:
    vs=[high.data.vertices[i].co for i in f.vertices]
    if f.normal.z<-.985 and all(198<p.y<335 and p.z<26 for p in vs):
     for j in f.loop_indices:hn[j]=f.normal.copy()
   high.data.normals_split_custom_set(hn)
  m=ob.modifiers.new('Original carved surface normals','DATA_TRANSFER');m.object=high
  m.use_loop_data=True;m.data_types_loops={'CUSTOM_NORMAL'};m.loop_mapping='POLYINTERP_NEAREST'
  m.use_max_distance=True;m.max_distance=.8;M.apply(ob)
 normals=[n.vector.copy() for n in ob.data.corner_normals]
 if ob.name=='Forend_Walnut':
  for f in ob.data.polygons:
   if f.normal.z<-.985 and 205<f.center.y<275 and f.center.z<24:
    # Nearest-face projection at an inlet boundary can choose the routed
    # wall even when the target corner belongs to the exterior land.
    for j in f.loop_indices:normals[j]=f.normal.copy()
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
  for f in ob.data.polygons:
   vs=[ob.data.vertices[i].co for i in f.vertices]
   if abs(f.normal.y)>.999:
    for j in f.loop_indices:normals[j]=f.normal.copy()
   elif all(70<=p.y<=115 and abs(abs(p.x)-action_section(p.y)[0])<.015 for p in vs):
    expected=Vector((math.copysign(1,sum(p.x for p in vs)),0,0)).normalized()
    for j in f.loop_indices:normals[j]=expected
   elif all(114.99<=p.y<=170.001 and abs(abs(p.x)-action_section(p.y)[0])<.015 for p in vs):
    expected=Vector((math.copysign(1,sum(p.x for p in vs)),0,0)).normalized()
    for j in f.loop_indices:normals[j]=expected
 if ob.name in ('Action_Body','Trigger_Plate'):normals=lower_normals(ob,normals)
 if ob.name=='Action_Body':normals=upper_normals(ob,normals)
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
 rib=bpy.data.objects['Solid_TopRib']
 coin_y=(BREECH+200)*.001
 hit,point,_,_=rib.ray_cast(Vector((0,coin_y,.09)),Vector((0,0,-1)))
 assert hit,'Coin station absent from actual rib'
 coin_top=point.z+.00315
 eye_z=.0547+(coin_top-.0547)*(.766-EYE[1]*.001)/(.766-coin_y)
 eye_mm=(0,EYE[1],eye_z*1000)
 socket_specs=dict(SOCKETS,Socket_Eye=eye_mm)
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in p) for k,p in socket_specs.items()},RIDING)
 eye=next(o for o in sockets if o.name=='Socket_Eye')
 eye.rotation_euler.x=math.atan2(.0547-eye_z,.766-EYE[1]*.001)
 arm['eye_fit_rule']='CPSA 2005 handbook p4-2: bead center clears round pound 200 mm ahead of breech'
 arm['coin_rib_surface_m']=point.z;arm['coin_thickness_m']=.00315
 arm['generator_sha256']=generator_digest();build_clips(arm);W.pose(arm,'Idle',0)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['stage']='Form checkpoint, unbaked constant inspection materials'
 sc['maker']='Propane Defense';sc['model']='Covey 26';sc['interface_version']='1.7.0'
 bpy.ops.wm.save_as_mainfile(filepath=str(out));W.export(out.with_suffix('.glb'),[arm]+PARTS+sockets)
 counts={ob.name:sum(len(f.vertices)-2 for f in ob.data.polygons) for ob in PARTS}
 report=dict(total=sum(counts.values()),parts=counts,standalones={})
 for name,fired in [('shell',False),('hull',True)]:
  ob=shell('LiveShell' if not fired else 'FiredHull',MAT,fired=fired)
  tri=ob.modifiers.new('Explicit triangles','TRIANGULATE');M.apply(ob);ob.data.transform(Matrix.Scale(.001,4))
  W.export(out.parent/(name+'.glb'),[ob],animations=False)
  report['standalones'][name]=len(ob.data.polygons);bpy.data.objects.remove(ob,do_unlink=True)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2));print('SXS TRIANGLES',report['total'],report['standalones'],flush=True)
if __name__=='__main__':main()
