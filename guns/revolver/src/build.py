"""PD Meridian Six: original .357 service revolver visual game asset.

Authored in mm, converted to the family's meter/grip frame. Rounded forging
sections and a subdivided rubber cage give compound form. Only visible prop
construction is modeled; no working lockwork or manufacturing internals.
"""
import argparse,math,sys,json
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from guns.common import magnum357
from parameters import *
from clips import build_clips
GENERATOR_HASH=generator_digest()
PARTS=[];MAT={};HIGH={};SEATS={}
def clean(o):
 # Exact Boolean intersections can leave coincident seam vertices and
 # microscopic edges. Clean in mm, before their scale defeats decimation.
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.001)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free();o.data.update()
def materials():
 for key,c,metal,r in [('steel',(.33,.34,.35),1,.34),('flat',(.38,.39,.40),1,.28),
  ('rubber',(.008,.007,.006),0,.64),('dark',(.012,.013,.014),.8,.4),
  ('brass',(.48,.29,.08),1,.29),('copper',(.45,.17,.065),1,.32),
  ('primer',(.38,.37,.32),1,.33),('lead',(.065,.067,.070),.75,.48),
  ('loader',(.020,.023,.025),0,.45)]:
  m=bpy.data.materials.new('CP_'+key);m.use_nodes=True;m.diffuse_color=(*c,1)
  b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*c,1)
  b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=r
  MAT[key]=m
def reg(ob,bone='Root',radius=0,segments=3):
 clean(ob)
 if radius:
  M.bevel(ob,radius,segments)
  if ob.name in ('Frame_Forging','Cylinder_Fluted'):
   # Weight only resolved cutter edges. Microscopic Boolean intersections
   # otherwise clamp the entire modifier to zero or make overlapping miters.
   bm=bmesh.new();bm.from_mesh(ob.data)
   weights=bm.edges.layers.float.new('bevel_weight_edge')
   for e in bm.edges:
    clear=min(q.calc_length() for v in e.verts for q in v.link_edges)
    internal=(any(34<v.co.y<50 and 19<v.co.z<31 and abs(v.co.x)<6.5 for v in e.verts)
      if ob.name=='Frame_Forging' else any(v.co.y<41.5 for v in e.verts))
    e[weights]=1.0 if not internal and clear>.45 and e.calc_face_angle(0)>math.radians(25) else 0.0
   bm.to_mesh(ob.data);bm.free()
   ob.modifiers[-1].limit_method='WEIGHT'
   ob.modifiers[-1].use_clamp_overlap=False
  w=ob.modifiers.new('Machined flat normals','WEIGHTED_NORMAL');w.keep_sharp=True;w.weight=30
 M.smooth(ob,45);M.apply(ob)
 ob['bone']=bone;ob['asset_set']='Revolver';ob['part_name']=ob.name;PARTS.append(ob);return ob
def box(name,lo,hi,mat='steel',bone='Root',radius=.3,segments=3,register=True):
 a,b=Vector(lo),Vector(hi);o=M.box(name,(a+b)/2,b-a,MAT[mat],0);M.apply(o)
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 return reg(o,bone,radius,segments) if register else o
def profile(name,pts,lo,hi,mat='steel',bone='Root',axis='X',radius=.3,register=True):
 o=M.profile(name,pts,lo,hi,MAT[mat],axis=axis)
 return reg(o,bone,radius) if register else o
def lathe(name,pts,mat='steel',bone='Root',axis='Y',center=(0,0),n=48,closed=False,register=True):
 o=M.lathe(name,pts,MAT[mat],n,axis=axis,center=center,closed=closed)
 return reg(o,bone) if register else o
def cut(o,tool,operation='DIFFERENCE'):
 tool.data.materials.clear();tool.data.materials.append(o.data.materials[0]);M.boolean(o,tool,operation)
 for f in o.data.polygons:f.material_index=0
 return o
def cutbox(o,lo,hi):return cut(o,box('tool',lo,hi,register=False))
def reduce(o,target):
 n=sum(len(f.vertices)-2 for f in o.data.polygons)
 if n>target:
  m=o.modifiers.new('Silhouette triangle budget','DECIMATE');m.ratio=target/n;M.apply(o)
 return o
def rounded(w,h,r,n=6):return M.rounded_rectangle(w,h,r,n)
def sphere(name,center,size,mat='steel',bone='Root',register=True):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1)
 o=bpy.context.object;o.name=name
 o.data.transform(Matrix.Translation(Vector(center))@Matrix.Diagonal(Vector((*size,1))))
 o.data.materials.append(MAT[mat]);return reg(o,bone) if register else o
def screw(name,x,y,z,r=2.1,mat='steel',bone='Root'):
 sign=1 if x>0 else -1
 lo,hi=sorted((x-sign*.65,x+sign*.1))
 o=lathe(name,[(lo,0),(lo,r*.92),(hi-.08*sign,r),(hi,r*.92),(hi,0)],mat,bone,axis='X',center=(y,z),n=24,register=False)
 a,b=sorted((x-sign*.20,x+sign*.4));cutbox(o,(a,y-r-.1,z-.30),(b,y+r+.1,z+.30))
 return reg(o,bone,.10,2)
def frame():
 # Forging volume varies in all three axes: broad recoil shoulder, lower
 # belly, neck and front collar. Machining leaves planar cheek lands.
 stations=[(-22,5.2,25,41),(-19,7.3,21,42),(-12,8.5,15,44),
  (-3,8.7,12,49),(5,8.8,13,56),(11,8.8,14.5,65),
  (16,8.8,16,73),(22,8.8,17,77.4),
  (34,8.8,20,77.4),(56,8.8,22.8,77.4),(78,8.8,24,77.4),
  (85,9.5,22,77),(93,9.7,24,75),(96,9.5,40,72)]
 loops=[[(x,y,z+(a+b)/2) for x,z in rounded(2*w,b-a,min(3.0,(b-a)*.2),6)] for y,w,a,b in stations]
 o=M.loft('Frame_Forging',loops,MAT['steel'])
 # An uninterrupted large-radius rear contour, not a plate outlined by bevels.
 shield=lathe('tool',[(32,0),(32,18.4),(34.6,19.0),(35.0,18.7),(35,0)],center=(0,CY),n=72,register=False)
 cut(o,shield,'UNION')
 window=[(y+58.95,z+48.2) for y,z in rounded(47.4,42.0,1.1,6)]
 cut(o,profile('tool',window,-30,30,register=False))
 # Hammer/trigger slots and front crane heel pocket are visible machining.
 cutbox(o,(-4.2,-3,40),(4.2,19,81))
 cutbox(o,(-4.1,26,12),(4.1,44,26))
 cutbox(o,(-22,82.6,18),(6.5,90.0,54.7))
 cutbox(o,(-28,81,CY-3.8),(3.5,98,CY+3.8))
 cut(o,lathe('tool',[(80,0),(80,5.2),(100,5.2),(100,0)],center=(0,BORE),n=48,register=False))
 # Cylinder stop's slot and the center latch pin's actual receiver bore.
 cutbox(o,(-1.8,41.9,20),(1.8,49.0,30.0))
 cutbox(o,(3.7,35.2,20),(5.8,48.0,27.0))
 cutbox(o,(-1.9,42.0,20.1),(5.9,45.2,27.1))
 cut(o,lathe('tool',[(25,0),(25,2.8),(38,2.8),(38,0)],center=(0,CY),n=24,register=False))
 # Sideplate fits into a shallow seat, with an even narrow reveal.
 plate=M.fillet_polygon([(-11,30),(-8,45),(1,51),(9,65),(26,64),
  (33.8,34),(33.8,27.0),(78,27.0),(78,24.7),(57,23.7),(45,23.8),(25,21),(6,17)],
  [2.5,2.5,2.5,2.5,2.5,1.0,.7,.5,.5,.7,.7,1.8,2.5],6)
 cut(o,profile('tool',plate,8.0,12,register=False))
 # Retain the closed pre-bevel machining solid as the rubber molding tool;
 # bevel miter intersections are unsuitable for a subsequent Boolean cutter.
 SEATS['Frame']=o.data.copy()
 # The forging's broad radii are in its loft. Machined pocket lips carry a
 # smaller cutter break so close internal pockets cannot collapse the bevel.
 reg(o,radius=.16,segments=3);reduce(o,5700)
 box('Crane_PivotSupport',(-12,90,19),(-4,94,34),radius=1.0)
 plate2=[((y-10)*.990+10,(z-40)*.991+40) for y,z in plate]
 profile('Frame_Sideplate',plate2,8.04,8.75,'flat',radius=.24)
 for y,z in [(-5,35),(9,61)]:screw('Sideplate_Screw',8.88,y,z,1.8)
 screw('Sideplate_ScrewFront',8.88,62,25.2,1.3)
 # Small rear strike seat for the hammer, with a visual firing-pin bushing.
 box('Hammer_RestSeat',(-3.5,18.0,65.0),(3.5,19.2,69.0),'steel',radius=.12)
 lathe('FiringPin_Bushing',[(34.9,1.0),(34.9,2.3),(35.12,2.3),(35.12,1.)],
       'dark',center=(0,BORE),n=24,closed=True)
 lathe('FiringPin',[(33,0),(33,.7),(35.13,.7),(35.13,0)],'steel',center=(0,BORE),n=16)
 # Guard is swept with a real oval bar section and broad heel blends.
 path=[]
 for controls in [((16,18),(17,8),(17,-6),(29,-7)),((29,-7),(43,-9),(61,-7),(65,4)),
                  ((65,4),(70,17),(66,23),(59,24))]:
  points=M.bezier(*controls,20);path+=points if not path else points[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized()
  normal=Vector((-tangent.y,tangent.x))
  loops.append([(5.0*math.cos(t),y+2.3*math.sin(t)*normal.x,z+2.3*math.sin(t)*normal.y)
    for t in [math.tau*j/16 for j in range(16)]])
 reg(M.loft('TriggerGuard_ForgedBow',loops,MAT['steel']))
 # Trigger's hidden rear land meets this separate physical frame stop.
 box('Trigger_RestStop',(-3.4,24.9,22.3),(3.4,26.0,24.2),radius=.04,segments=2)
def barrel():
 # One analytic bored skin, including the rib and full round underlug. This
 # replaces overlapping cylindrical Boolean unions and their broken seams.
 r=10.;lug=5.7;d=BORE-CY
 # Common tangents join the barrel and lower shroud. A union of two circles
 # leaves a pinched waist and a folded polar cap when the lower radius shrinks.
 a=math.atan2(math.sqrt(r*r-3.4**2),3.4);b=math.asin((lug-r)/d)
 def arc(cx,cz,rr,lo,hi,n):
  return [(cx+rr*math.cos(lo+(hi-lo)*j/n),cz+rr*math.sin(lo+(hi-lo)*j/n)) for j in range(n+1)]
 outline=[(3.4,76.4),*arc(0,BORE,r,a,b,24),
  *arc(0,CY,lug,b,-math.pi-b,48),
  *arc(0,BORE,r,-math.pi-b,-math.pi-a,24),(-3.4,76.4)]
 # Keep the bore round through the long straight tangent/rib transitions.
 # Their endpoint-only polar correspondence otherwise leaves 50-degree chords.
 original=outline;outline=[]
 for va,vb in zip(original,original[1:]+original[:1]):
  span=(math.atan2(va[1]-BORE,va[0])-math.atan2(vb[1]-BORE,vb[0]))%math.tau
  steps=max(1,math.ceil(span/math.radians(3))) if span>math.radians(6) else 1
  outline.extend([(va[0]+(vb[0]-va[0])*k/steps,va[1]+(vb[1]-va[1])*k/steps) for k in range(steps)])
 angles=[math.atan2(z-BORE,x) for x,z in outline]
 def circle(y,rr):return [(rr*math.cos(t),y,BORE+rr*math.sin(t)) for t in angles]
 def section(y,inset=0):
  return [(x*(1-inset/12),y,BORE+(z-BORE)*(1-inset/12)) for x,z in outline]
 loops=[circle(BREECH,6.7),circle(85,7.8),circle(96,10),section(96),
  section(MUZZLE-.55),section(MUZZLE,.35),circle(MUZZLE,5.0),
  circle(MUZZLE-.7,4.52),circle(85,4.52),circle(BREECH,4.65)]
 o=M.ring_loft('Barrel',loops,MAT['steel']);clean(o)
 # One open-left, round-root milling cutter produces the shroud relief.
 pts=[(-22,CY-3.8),(0,CY-3.8),*arc(0,CY,3.8,-math.pi/2,math.pi/2,24)[1:],(-22,CY+3.8)]
 cut(o,profile('tool',pts,91,151,axis='Y',register=False))
 reg(o,radius=.22,segments=2)
 # Pinned ramp is seated in a milled rib pocket.
 ramp=[(166,76.4),(166,77.4),(176,83.0),(180,83.0),(180,76.4)]
 profile('FrontSight_PinnedRamp',M.fillet_polygon(ramp,.45,5),-1.5,1.5,'dark',radius=.16)
 lathe('FrontSight_Pin',[(-3.4,0),(-3.4,.7),(3.4,.7),(3.4,0)],'dark',axis='X',center=(177,77.5),n=16)
def cylinder():
 star_points=[]
 for j in range(72):
  t=j*math.tau/72;r=6.8+3.6*(.5+.5*math.cos(6*(t-math.pi/3)))**2
  star_points.append((r*math.cos(t),CY+r*math.sin(t)))
 o=lathe('Cylinder_Fluted',[(REAR,3.2),(REAR,19.25),(REAR+.55,RADIUS),
  (FRONT-.55,RADIUS),(FRONT,19.25),(FRONT,3.2)],bone='Cylinder',center=(0,CY),n=96,closed=True,register=False)
 for i in range(6):
  x,y,z=chamber(i)
  # Exterior visual chamber and rim counterbore. No functional throat design.
  cut(o,lathe('tool',[(REAR-2,0),(REAR-2,5.8),(REAR,5.8),(REAR+.15,5.65),(REAR+1.4,5.65),(REAR+1.4,4.90),
   (FRONT-1.0,4.90),(FRONT,4.55),(FRONT+1,4.55),(FRONT+1,0)],center=(x,z),n=32,register=False))
  # A swept round-ended cutter leaves continuous spherical end blends.
  fx,fz=flute_axis(i);rr=FLUTE_RADIUS
  cutter=[(FLUTE_START,0)]
  for j in range(1,9):
   a=-math.pi/2+j*math.pi/16
   cutter.append((FLUTE_START+rr+rr*math.sin(a),rr*math.cos(a)))
  cutter.append((FLUTE_END-rr,rr))
  for j in range(1,9):
   a=j*math.pi/16
   cutter.append((FLUTE_END-rr+rr*math.sin(a),0 if j==8 else rr*math.cos(a)))
  flute=lathe('tool',cutter,center=(fx,fz),n=32,register=False)
  cut(o,flute)
  # A rectangular stop recess with a shallow approach cut, around each station.
  tool=box('tool',(-1.6,42.0,CY-RADIUS-1),(1.6,48.0,CY-RADIUS+1.4),register=False)
  xf=Matrix.Translation(Vector((0,0,CY)))@Matrix.Rotation(i*math.tau/6,4,'Y')@Matrix.Translation(Vector((0,0,-CY)))
  tool.data.transform(xf);cut(o,tool)
  tool=profile('tool',[(-4.8,CY-RADIUS-.2),(-1.4,CY-RADIUS-.2),
    (-1.4,CY-RADIUS+.9),(-4.8,CY-RADIUS+.10)],42.0,48.0,axis='Y',register=False)
  tool.data.transform(xf);cut(o,tool)
 seat=[(x*1.012,CY+(z-CY)*1.012) for x,z in star_points]
 cut(o,profile('tool',seat,REAR-.2,REAR+2.95,axis='Y',register=False))
 reg(o,'Cylinder',.16,segments=2);reduce(o,9300)
 # Star has genuine scalloped arms around the rims. Its seat is a separate
 # shallow web on the rear face; six open sectors preserve chamber visibility.
 star=profile('Extractor_Star',star_points,REAR+1.4,REAR+2.8,'steel','Extractor',axis='Y',register=False)
 for i in range(6):
  x,_,z=chamber(i)
  cut(star,lathe('tool',[(37,0),(37,5.1),(42,5.1),(42,0)],center=(x,z),n=32,register=False))
 cut(star,lathe('tool',[(35,0),(35,1.75),(42,1.75),(42,0)],center=(0,CY),n=24,register=False))
 reg(star,'Extractor',.10,2)
 lathe('Extractor_LatchHub',[(35.65,1.75),(35.65,3.1),(39.6,3.1),(39.6,1.75)],
       'steel','Extractor',center=(0,CY),n=32,closed=True)
 lathe('Extractor_Rod',[(REAR-1.2,0),(REAR-1.2,1.5),(145,1.5),(146,1.3),(146,0)],
       'steel','Extractor',center=(0,CY),n=24)
 lathe('Ejector_Tip',[(142,0),(142,2.3),(147,2.3),(148,2.0),(148,0)],
       'steel','Extractor',center=(0,CY),n=32)
 for i in range(6):
  t=i*math.tau/6
  pts=[(r*math.cos(a),CY+r*math.sin(a)) for r,a in
       [(2.8,t),(5.3,t+.06),(5.3,t+.42),(3.1,t+.73)]]
  profile('Extractor_Ratchet'+str(i),pts,REAR-2.3,REAR-1.4,'dark','Extractor',axis='Y',radius=.12)
def crane_controls():
 # Forged yoke has two bored bosses and an offset web, in the front plane.
 outline=M.fillet_polygon([(-12,17),(-3,16),(5,43),(5,50),(1,53),(-4,51),(-9,30)],2.2,8)
 o=profile('Crane_Yoke',outline,83.0,88.8,'steel','Crane',axis='Y',register=False)
 cut(o,lathe('tool',[(82,0),(82,3.0),(90,3.0),(90,0)],center=(0,CY),n=32,register=False))
 cut(o,lathe('tool',[(82,0),(82,2.7),(90,2.7),(90,0)],center=(-8,20),n=24,register=False))
 cut(o,lathe('tool',[(82,0),(82,9.85),(90,9.85),(90,0)],center=(0,BORE),n=48,register=False))
 reg(o,'Crane',.45,3)
 lathe('Crane_UpperBearing',[(82.8,1.75),(82.8,4.4),(84.0,4.4),(84.0,1.75)],
  'steel','Crane',center=(0,CY),n=32,closed=True)
 lathe('Crane_Axle',[(70,1.75),(70,3.0),(84,3.0),(84,1.75)],'steel','Crane',center=(0,CY),n=32,closed=True)
 lathe('Crane_Pivot',[(81,0),(81,2.6),(91,2.6),(91,0)],'dark','Root',center=(-8,20),n=24)
 box('Crane_ClosedSeat',(-9.7,88.8,19),(-6.3,90,24),radius=.10)
 # The thumb latch has a broad machined pad, tapered sides, recessed center.
 pts=M.fillet_polygon([(16,49),(16,56.5),(25,58),(30,55),(28,49)],1.6,6)
 o=profile('Latch_Thumbpiece',pts,-11.7,-8.9,'steel','Latch',register=False)
 for v in o.data.vertices:
  if v.co.x< -10:v.co.x-=.55*math.sin((v.co.y-16)/14*math.pi)
 reg(o,'Latch',.35,3)
 screw('Latch_Screw',-12.1,23.3,53.2,1.5,bone='Latch')
 lathe('Latch_CenterPin',[(31,0),(31,1.6),(35.55,1.6),(35.55,2.6),
  (35.65,2.6),(35.65,1.6),(36.55,1.6),(36.55,0)],'dark','LatchPin',center=(0,CY),n=24)
 # Bolt stop with a wide head and an offset rocker on a supported pin.
 box('CylinderStop',(-1.35,42.3,24.5),(1.35,45.7,29.85),'dark','CylinderStop',radius=.12,segments=2)
 lever=box('CylinderStop_SideLever',(3.9,37,23.2),(5.5,44.5,25.5),'dark','CylinderStop',register=False)
 cut(lever,lathe('tool',[(3.7,0),(3.7,1.36),(5.7,1.36),(5.7,0)],axis='X',center=(37,24),n=16,register=False))
 reg(lever,'CylinderStop',.15,2)
 box('CylinderStop_Bridge',(-1.0,42.4,24.5),(5.4,44.5,26.0),'dark','CylinderStop',radius=.15,segments=2)
 lathe('CylinderStop_Bearing',[(3.9,.85),(3.9,1.35),(5.5,1.35),(5.5,.85)],
  'dark','CylinderStop',axis='X',center=(37,24),n=16,closed=True)
 lathe('CylinderStop_Pin',[(3.7,0),(3.7,.75),(6.2,.75),(6.2,0)],
  'steel','Root',axis='X',center=(37,24),n=12)
def lockwork_sights():
 front=M.bezier((40,21),(33,16),(32,4),(42,-1.3),18)
 toe=M.bezier((42,-1.3),(43,-2.6),(40.9,-3.0),(39.5,-1.9),5)
 back=M.bezier((39.5,-1.9),(29,3),(29,15),(36.6,21),18)
 pts=[(26,24),(40,24),*front,*toe[1:],*back[1:],(26,22)]
 profile('Trigger_Shoe',pts,-3.5,3.5,'flat','Trigger',radius=.50)
 # Hammer forged stem and a widened swept thumb spur, each section changes.
 hammer=M.fillet_polygon([(4,44),(15,44),(18.0,65),(18.0,69),(13,73),
  (8,73),(5,65),(0,61)],1.2,6)
 profile('Hammer_Body',hammer,-3.65,3.65,'flat','Hammer',radius=.55)
 loops=[]
 for y,z,w,d in [(8,70,3.3,1.8),(3,73.5,4.0,2.0),(-5,76.2,4.8,1.7),(-12,77.0,4.4,1.3)]:
  loops.append([(x,y,z+dz) for x,dz in rounded(2*w,2*d,1.0,5)])
 reg(M.loft('Hammer_ThumbSpur',loops,MAT['flat']),'Hammer',.16,2)
 # Coarse divisions show the checkpoint's thumb surface; fine checkering bakes later.
 for y in (-10,-8,-6,-4,-2):
  z=76.8+(y+10)*-.2
  box('Hammer_SpurRidge',(-3.8,y-.22,z),(3.8,y+.22,z+.45),'dark','Hammer',radius=.10,segments=2)
 screw('Hammer_PivotHead',8.9,10,48,1.55)
 # Leaf, hinge and adjustment housing visibly sit on the topstrap's recess.
 box('RearSight_Leaf',(-4.2,30,77.4),(4.2,66,79.7),'dark',radius=.40)
 base=box('RearSight_NotchBody',(-7.4,27.4,78.4),(7.4,31.8,83.0),'dark',register=False)
 cutbox(base,(-2.0,26,80.0),(2.0,33,85));reg(base,radius=.15,segments=2)
 # Elevation screw is sunk into the leaf, windage screw sits transversely.
 lathe('RearSight_ElevationScrew',[(79.5,0),(79.5,1.7),(80.2,1.7),(80.2,0)],'dark',axis='Z',center=(0,45),n=24)
 screw('RearSight_WindageScrew',7.5,29.6,80.6,1.45,'dark')
 lathe('RearSight_Hinge',[(-4.4,0),(-4.4,.8),(4.4,.8),(4.4,0)],'steel',axis='X',center=(62,78),n=20)
def grips():
 # A genuine 3D subdivision cage: changing horizontal sections, palm swell,
 # curved backstrap and finger grooves. No side outline is extruded.
 rows=[(-60.5,-29.8,11.8,20.3),(-59.3,-29.8,14.8,23.3),(-58.6,-29.5,16.0,24.4),
  (-56,-28.7,16.4,24.6),(-49,-25,16.5,25.0),(-40,-21,16.9,25.3),
  (-30,-16.4,17.0,25.0),(-20,-12.4,16.5,24.2),(-10,-8.5,15.8,22.5),
  (0,-5.8,15.0,21.4),(9,-5,14.1,20),(18,-6,12.8,18),
  (27,-10,11.5,15.6),(35,-13,9.5,12),(38,-14,7.7,9.5)]
 # More cage stations resolve the finger saddles instead of smoothing them away.
 original=rows;rows=[]
 for a,b in zip(original,original[1:]):
  steps=max(1,round((b[0]-a[0])/2.5))
  for k in range(steps):rows.append(tuple(a[j]+(b[j]-a[j])*k/steps for j in range(4)))
 rows.append(original[-1]);loops=[]
 for z,y,hw,hd in rows:
  loop=[]
  for j in range(40):
   t=j*math.tau/40;c=math.cos(t);s=math.sin(t)
   x=hw*math.copysign(abs(s)**(2/2.4),s)
   yy=y+hd*math.copysign(abs(c)**(2/2.4),c)
   if c>0:
    # Three support crests, blended around the front shoulder.
    relief=sum(4.8*math.exp(-((z-zz)/3.5)**2) for zz in (-12,-31,-49))
    yy+=relief*c**5
   loop.append((x,yy,z*1.1 if z<0 else z))
  loops.append(loop)
 o=M.loft('Grip_RubberMold',loops,MAT['rubber'])
 sub=o.modifiers.new('Compound service grip subdivision','SUBSURF');sub.levels=2;M.apply(o)
 # Molded tang saddle; cut actual seat to clear the forging above the hand.
 tool=bpy.data.objects.new('Grip molding tool',SEATS['Frame'].copy());bpy.context.collection.objects.link(tool)
 tool.data.transform(Matrix.Diagonal(Vector((1.015,1.001,1.001,1))))
 cut(o,tool)
 remesh=o.modifiers.new('Finished rubber cavity remesh','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.30;remesh.use_smooth_shade=True;M.apply(o)
 relax=o.modifiers.new('Mold radius relaxation','SMOOTH');relax.factor=.32;relax.iterations=3;M.apply(o);M.smooth(o,70)
 HIGH[o.name]=o.data.copy();reg(o);reduce(o,5400)
 for side in (-1,1):
  # Recessed screw cup and a real slotted screw, supported in the molded flank.
  x=side*16.85
  lathe('Grip_ScrewCup',[(x-side*.6,1.6),(x-side*.6,3.4),(x,3.4),(x,1.6)],
   'dark',axis='X',center=(-18,-30),n=32,closed=True)
  screw('Grip_Screw',side*16.95,-18,-30,2.2,'dark')
def ammunition():
 for prefix,fired in [('Live',False),('Case',True),('LoaderRound',False)]:
  for i in range(6):
   for o in magnum357.build(prefix+str(i),chamber(i),MAT,fired=fired,segments=16):reg(o,prefix+str(i))
 for o in magnum357.build('InsertRound',chamber(0),MAT,segments=16):reg(o,'InsertRound')
 # Original six-pocket speedloader with a central push release, scalloped skirt.
 o=lathe('Speedloader_Body',[(26,0),(26,17.3),(27,18.7),(33.8,18.7),(35.1,17.7),(35.1,0)],
  'loader','LoaderBody',center=(0,CY),n=72,register=False)
 for i in range(6):
  x,_,z=chamber(i)
  cut(o,lathe('tool',[(25,0),(25,5.7),(36,5.7),(36,0)],center=(x,z),n=24,register=False))
 cut(o,lathe('tool',[(25,0),(25,3.2),(37,3.2),(37,0)],center=(0,CY),n=24,register=False))
 reg(o,'LoaderBody',.35,2);reduce(o,1500)
 lathe('Speedloader_Release',[(15,0),(15,6.0),(16,6.7),(22,6.7),(23,5.3),(23,3.0),(30,3.0),(30,0)],
  'dark','LoaderRelease',center=(0,CY),n=36)
 for i in range(6):
  x,_,z=chamber(i)
  lathe('Speedloader_RimClip'+str(i),[(34.7,3.5),(34.7,4.1),(38.0,4.1),(38.0,3.5)],
   'steel','LoaderBody',center=(x,z),n=16,closed=True)
def finalize(o):
 tri=o.modifiers.new('Final triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(o)
 clean(o)
 # Budget actual finalized triangles; Boolean cap tessellation can cost more
 # than a pre-triangulation ngon count. Fine hardware relief belongs in bake.
 limits={'Cylinder_Fluted':7700,'Frame_Forging':2600,'Grip_RubberMold':4000,
  'Barrel':2800,'Speedloader_Body':1200,'Speedloader_Release':310,'TriggerGuard_ForgedBow':850,
  'Extractor_Star':650,'Crane_Yoke':850,'Trigger_Shoe':550,'Hammer_Body':400,
  'Frame_Sideplate':400,'Hammer_ThumbSpur':300,'Latch_Thumbpiece':320,
  'RearSight_Leaf':180,'RearSight_NotchBody':260,'Crane_PivotSupport':180}
 limit=limits.get(o.name,144 if 'Screw' in o.name or 'PivotHead' in o.name else 210)
 if o.name.startswith(('Live','Case','LoaderRound','InsertRound')):limit=1000
 reduce(o,limit)
 tri=o.modifiers.new('Budget triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(o)
 if o.name in ('Speedloader_Body','Barrel','Cylinder_Fluted','Frame_Forging'):
  # Reseed the machining fields after QEM, rather than interpolating obsolete
  # Boolean corner normals into wavy cap and pocket highlights.
  o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));M.smooth(o,42)
  wn=o.modifiers.new('Final machined surface normals','WEIGHTED_NORMAL');wn.keep_sharp=True;wn.weight=50;M.apply(o)
 normals=[n.vector.copy() for n in o.data.corner_normals]
 if o.name in ('Frame_Forging','Speedloader_Body','Speedloader_Release'):
  axis=0 if o.name=='Frame_Forging' else 1
  planar={}
  for f in o.data.polygons:
   xs=[o.data.vertices[i].co[axis] for i in f.vertices]
   if abs(f.normal[axis])>.999 and max(xs)-min(xs)<.03:
    fixed=Vector((0,0,0));fixed[axis]=1 if f.normal[axis]>0 else -1
    for i in f.vertices:planar[i]=fixed.copy()
  for f in o.data.polygons:
   for j in f.loop_indices:
    fixed=planar.get(o.data.loops[j].vertex_index)
    if fixed is not None and f.normal.dot(fixed)>.7:normals[j]=fixed.copy()
 if o.name in ('Cylinder_Fluted','Barrel'):
  for f in o.data.polygons:
   if abs(f.normal.y)>.9999:
    for j in f.loop_indices:normals[j]=Vector((0,1 if f.normal.y>0 else -1,0))
   elif o.name=='Cylinder_Fluted':
    vs=[o.data.vertices[i].co for i in f.vertices]
    radial=Vector((f.center.x,0,f.center.z-CY)).normalized()
    if all(abs(math.hypot(v.x,v.z-CY)-RADIUS)<.025 for v in vs) and f.normal.dot(radial)>.95:
     for j in f.loop_indices:
      v=o.data.vertices[o.data.loops[j].vertex_index].co
      normals[j]=Vector((v.x,0,v.z-CY)).normalized()
    else:
     for i in range(6):
      fx,fz=flute_axis(i)
      def cutter_normal(v):
       yy=min(max(v.y,FLUTE_START+FLUTE_RADIUS),FLUTE_END-FLUTE_RADIUS)
       return Vector((fx,yy,fz))-v
      if all(abs(cutter_normal(v).length-FLUTE_RADIUS)<.13 for v in vs) and f.normal.dot(cutter_normal(f.center).normalized())>.7:
       for j in f.loop_indices:
        normals[j]=cutter_normal(o.data.vertices[o.data.loops[j].vertex_index].co).normalized()
       break
 for f in o.data.polygons:
  for j in f.loop_indices:
   if normals[j].dot(f.normal)<.03:normals[j]=f.normal.copy()
 o.data.normals_split_custom_set(normals)
 o.data.transform(Matrix.Scale(.001,4));o.matrix_world=Matrix.Identity(4);o.data.update()
 # Meter-space float storage can reverse a microscopic Boolean cap's normal
 # relative to its former mm-space field. Judge the actual shipping triangles.
 normals=[n.vector.copy() for n in o.data.corner_normals]
 for f in o.data.polygons:
  for j in f.loop_indices:
   if normals[j].dot(f.normal)<.10:normals[j]=f.normal.copy()
 o.data.normals_split_custom_set(normals)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/revolver.blend')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);materials()
 frame();barrel();cylinder();crane_controls();lockwork_sights();grips();ammunition()
 for o in PARTS:
  finalize(o)
  assert len(o.data.polygons)>0,('Empty generated part',o.name)
 arm=W.armature('RevolverArmature',{n:tuple(v*.001 for v in pos) for n,pos in HEADS.items()},PARENTS)
 for o in PARTS:W.rigid_bind(o,arm,o['bone'])
 sockets=W.sockets(arm,{n:tuple(v*.001 for v in pos) for n,pos in SOCKETS.items()},RIDING)
 build_clips(arm)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['stage']='FORM CHECKPOINT: quick unbaked materials, no final texture claim'
 sc['generator_sha256']=arm['generator_sha256']=GENERATOR_HASH
 bpy.ops.wm.save_as_mainfile(filepath=str(out))
 # Checkpoint retains original named parts to audit actual imported contacts.
 W.export(out.with_suffix('.glb'),[arm,*PARTS,*sockets])
 # Dense grip is retained for the later isolated high-to-low bake.
 for name,data in HIGH.items():
  data.transform(Matrix.Scale(.001,4));ob=bpy.data.objects[name];old=ob.data;ob.data=data
  ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(data.vertices))),1,'REPLACE')
  bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'));ob.data=old
  ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(old.vertices))),1,'REPLACE')
 # Standalones use the same rigid-bone extraction as family delivery.
 W.pose(arm,'Idle',0)
 for name,bone in [('cartridge','Live0'),('case','Case0')]:
  if name=='case':W.pose(arm,'IdleAfter6',0)
  item=W.detachable([o for o in PARTS if o['bone']==bone],arm,bone,name)
  W.export(out.parent/(name+'.glb'),[item],False);bpy.data.objects.remove(item,do_unlink=True)
 W.pose(arm,'Reload',142)
 item=W.detachable([o for o in PARTS if o['bone'] in ('LoaderBody','LoaderRelease') or o['bone'].startswith('LoaderRound')],arm,'LoaderGuide','LoadedSpeedloader')
 W.export(out.parent/'speedloader_loaded.glb',[item],False);bpy.data.objects.remove(item,do_unlink=True)
 counts={o.name:len(o.data.polygons) for o in PARTS};total=sum(counts.values())
 (out.parent/'triangles.json').write_text(json.dumps(dict(total=total,parts=counts),indent=2))
 print('REVOLVER TRIANGLES',total,flush=True)
if __name__=='__main__':main()
