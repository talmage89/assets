"""PD Meridian Six: original .357 service revolver visual game asset.

Authored in mm, converted to the family's meter/grip frame. Rounded forging
sections and a subdivided rubber cage give compound form. Only visible prop
construction is modeled; no working lockwork or manufacturing internals.
"""
import argparse,math,sys,json
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import convex_hull_2d
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from guns.common import magnum357
from parameters import *
from clips import build_clips
GENERATOR_HASH=generator_digest()
PARTS=[];MAT={};HIGH={};SEATS={};OUTLINES={}
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
 tool.data.materials.clear();tool.data.materials.append(o.data.materials[0])
 if o.name in ('Frame_Forging','Barrel','Hammer_ThumbSpur'):
  modifier=o.modifiers.new('Manifold visual machining','BOOLEAN');modifier.object=tool
  modifier.operation=operation;modifier.solver='MANIFOLD';M.apply(o)
  bpy.data.objects.remove(tool,do_unlink=True)
 else:M.boolean(o,tool,operation)
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
 # The spine is one tangent-continuous sweep from the hand web into the
 # horizontal topstrap. Stations are samples of that radius, not facets.
 spine=M.bezier((-22,41),(.5,41),(2.5,77.4),(28,77.4),64)
 bottom=[(-22,25),(-12,15),(-3,12),(16,16),(34,20),(56,22.8),
  (78,24),(84,22),(87,22),(91,20.5),(94,25.5),(96,43.0)]
 def height(y,rows):
  for (ya,a),(yb,b) in zip(rows,rows[1:]):
   if ya<=y<=yb:
    t=(y-ya)/(yb-ya);t=t*t*(3-2*t)
    return a+(b-a)*t
  return rows[-1][1]
 stations=[]
 for y in sorted(set([round(-22+1.5*i,4) for i in range(34)]+[28,34,56,78,82,84,87,90,92,94,95,96])):
  if y<28:
   for (ya,a),(yb,b) in zip(spine,spine[1:]):
    if ya<=y<=yb:top=a+(b-a)*(y-ya)/(yb-ya);break
  else:top=77.4 if y<=82 else height(y,[(82,77.4),(90,76.5),(96,72)])
  width=height(y,[(-22,5.2),(-16,8.3),(-8,8.8),(78,8.8),(90,9.7),(96,9.5)])
  stations.append((y,width,height(y,bottom),top))
 loops=[[(x,y,z+(a+b)/2) for x,z in rounded(2*w,b-a,min(3.5,(b-a)*.23),8)] for y,w,a,b in stations]
 o=M.loft('Frame_Forging',loops,MAT['steel'])
 # An uninterrupted large-radius rear contour, not a plate outlined by bevels.
 shield=lathe('tool',[(32.25,0),(32.25,17),(33.0,18.5),(34.4,19),
  (35.5,18.8),(36.7,17),(37.1,14.8),(37.1,0)],center=(0,CY),n=72,register=False)
 cut(o,shield,'UNION')
 # 0.45 mm radial running light around the accepted cylinder envelope.
 window=[(y+59.95,z+48.2) for y,z in rounded(45.7,40.3,.65,6)]
 cut(o,profile('tool',window,-30,30,register=False))
 # Raised recoil boss, filleted out of the shield around the firing bushing.
 boss=lathe('tool',[(33.0,0),(33.0,9.2),(34.7,9.2),(35.8,8.8),
  (36.7,7.8),(37.35,6.4),(37.55,4.7),(37.55,0)],center=(0,BORE),n=48,register=False)
 cut(o,boss,'UNION')
 # Relief for the original ratchet/hub; the surrounding shield is a raised
 # rounded forging, rather than a separate flat disc.
 # The rear ratchet/hub passes sideways out of the shield; leave its
 # real swept release passage in the lower-left shoulder.
 release=[]
 for j in range(17):
  angle=math.radians(-j*5);xx=CRANE[0]+8*math.cos(angle)+28.2*math.sin(angle)
  zz=CRANE[2]-8*math.sin(angle)+28.2*math.cos(angle)
  release.extend(Vector((xx+5.65*math.cos(t),zz+5.65*math.sin(t))) for t in [math.tau*k/32 for k in range(32)])
 release=[tuple(release[i]) for i in convex_hull_2d(release)]
 cut(o,profile('tool',release,34.25,37.8,axis='Y',register=False))
 # The cylinder's center rises 1.1 mm during early swing-out. A left-only
 # underside chamfer clears that arc, while the center/right rail hugs it.
 roof=[(-22,65),(-22,70.9),(0,68.35),(0,65)]
 cut(o,profile('tool',roof,37.1,82.9,axis='Y',register=False))
 # Hammer/trigger slots and front crane heel pocket are visible machining.
 # Close all unused space behind the hammer. This narrow pocket is the
 # swept *body*, rather than a rectangular trough through the backstrap.
 envelope=[]
 for angle in range(0,36,2):
  t=math.radians(angle)
  for y,z in [(4,44),(15,44),(18,65),(18.8,66.2),(18.8,67.8),(18,69),(13.5,73.5),(6.2,73.5),(2.8,66),(0,61)]:
   yy=10+(y-10)*math.cos(t)-(z-48)*math.sin(t)
   zz=48+(y-10)*math.sin(t)+(z-48)*math.cos(t)
   envelope.extend(Vector((yy+dy,zz+dz)) for dy,dz in [(-.3,-.3),(-.3,.3),(.3,.3),(.3,-.3)])
 hull=[tuple(envelope[i]) for i in convex_hull_2d(envelope)]
 cut(o,profile('tool',hull,-4,4,register=False))
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
 # Blend the crane bearing heel into the same forging. The old separately
 # perched support box made a conspicuous step below the barrel shank.
 heel=box('tool',(-11,90,19),(-4,94,34),register=False)
 M.bevel(heel,1.9,5);M.apply(heel);cut(o,heel,'UNION')
 cut(o,lathe('tool',[(89.7,0),(89.7,2.75),(94.5,2.75),(94.5,0)],center=(-8,20),n=24,register=False))
 # Retain the closed pre-bevel machining solid as the rubber molding tool;
 # bevel miter intersections are unsuitable for a subsequent Boolean cutter.
 SEATS['Frame']=o.data.copy()
 # The forging's broad radii are in its loft. Machined pocket lips carry a
 # smaller cutter break so close internal pockets cannot collapse the bevel.
 reg(o,radius=.12,segments=2);reduce(o,5600)
 plate2=[((y-10)*.990+10,(z-40)*.991+40) for y,z in plate]
 profile('Frame_Sideplate',plate2,8.04,8.75,'flat',radius=.24)
 for y,z in [(-5,35),(9,61)]:screw('Sideplate_Screw',8.88,y,z,1.8)
 screw('Sideplate_ScrewFront',8.88,62,25.2,1.3)
 # Small rear strike seat for the hammer, with a visual firing-pin bushing.
 seat=box('Hammer_RestSeat',(-3.5,18.0,65.0),(3.5,19.2,69.0),'steel',register=False)
 cutbox(seat,(-1.6,17.5,65.9),(1.6,19.05,68.1));reg(seat,radius=.10,segments=2)
 lathe('FiringPin_Bushing',[(37.45,1.0),(37.45,2.3),(37.60,2.3),(37.60,1.)],
       'dark',center=(0,BORE),n=24,closed=True)
 lathe('FiringPin',[(36.8,0),(36.8,.7),(37.61,.7),(37.61,0)],'steel',center=(0,BORE),n=16)
 # Photo-scaled flat forged band: 8.4 mm across the gun, 2.8 mm in
 # side elevation, with a .60 mm edge radius. Parallel sides stay flat.
 path=[]
 for controls in [((16,18),(17,8),(17,-6),(29,-7)),((29,-7),(43,-9),(61,-7),(65,4)),
                  ((65,4),(70,17),(66,23),(59,24))]:
  points=M.bezier(*controls,12);path+=points if not path else points[1:]
 loops=[]
 for i,(y,z) in enumerate(path):
  tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized()
  normal=Vector((-tangent.y,tangent.x))
  loops.append([(x,y+v*normal.x,z+v*normal.y) for x,v in rounded(8.4,2.8,.60,3)])
 reg(M.loft('TriggerGuard_ForgedBow',loops,MAT['steel']))
 # Trigger's hidden rear land meets this separate physical frame stop.
 box('Trigger_RestStop',(-3.4,24.9,22.3),(3.4,26.0,24.2),radius=.04,segments=2)
def barrel():
 # A single machined exterior with real side flats, a rib and a narrow
 # barrel/lug transition. Round the outline before making the longitudinal
 # skin; the small edge radii are geometry, not interpolated knife edges.
 a0=math.acos(.34);a1=math.acos(.96)
 shoulder=[(10*math.cos(a0+(a1-a0)*i/24),BORE+10*math.sin(a0+(a1-a0)*i/24)) for i in range(25)]
 lower=M.bezier((9.6,57.0),(9.6,55.9),(9.4,54.6),(8.9,53.6),12)
 half=[(3.4,76.4),*shoulder,(9.6,57.0),*lower[1:],(8.9,53.3),
  (9.5,52.5),(9.5,46.6),(8.5,44.4),(6.2,43.2),(3.9,42.5),(0,42.35)]
 outline=M.fillet_polygon(half+[(-x,z) for x,z in half[-2::-1]],.35,4)
 OUTLINES['Barrel']=outline
 def section(y,inset=0):
  return [(x*(1-inset/12),y,BORE+(z-BORE)*(1-inset/12)) for x,z in outline]
 o=M.loft('Barrel',[section(95.8),section(MUZZLE-.35),section(MUZZLE,.20)],MAT['steel'])
 # Cone joins inside the exterior; the round bore is a separate cutter. This
 # avoids folded polar caps between the rolled lug nose and the bore rim.
 cone=lathe('tool',[(BREECH,0),(BREECH,6.7),(85,7.8),(96.3,9.6),(96.3,0)],n=96,center=(0,BORE),register=False)
 cut(o,cone,'UNION')
 bore=lathe('tool',[(81,0),(81,4.65),(BREECH,4.65),(85,4.52),
  (MUZZLE-.7,4.52),(MUZZLE,5.0),(MUZZLE+1,5.0),(MUZZLE+1,0)],center=(0,BORE),n=96,register=False)
 cut(o,bore)
 # Elliptical quarter-round: 5 mm axial recession over the lug's bottom
 # 10.65 mm. The upper crown remains at the accepted muzzle station.
 nose=[(MUZZLE-5,30),(MUZZLE+2,30),(MUZZLE+2,53),(MUZZLE,53)]
 nose += [(MUZZLE-5+5*math.cos(j*math.pi/48),53-10.65*math.sin(j*math.pi/48)) for j in range(1,25)]
 cut(o,profile('tool',nose,-25,25,register=False))
 # Bore around the rod; the narrow upper-left release is the actual swept
 # passage required by the accepted crane arc, rather than the old open hook.
 cut(o,lathe('tool',[(90,0),(90,2.85),(MUZZLE+1,2.85),(MUZZLE+1,0)],center=(0,CY),n=40,register=False))
 pts=[]
 for j in range(17):
  theta=math.radians(-j*2.5);x=CRANE[0]+8*math.cos(theta)+28.2*math.sin(theta)
  z=CRANE[2]-8*math.sin(theta)+28.2*math.cos(theta)
  pts.append((x,z))
 upper=[(x,z+1.75) for x,z in pts];lower=[(x,z-1.75) for x,z in reversed(pts)]
 cut(o,profile('tool',upper+lower,90,MUZZLE+1,axis='Y',register=False))
 reg(o)
 # Pinned ramp is seated in a milled rib pocket.
 ramp=[(166,76.4),(166,77.4),(176,83.0),(180,83.0),(180,76.4)]
 profile('FrontSight_PinnedRamp',M.fillet_polygon(ramp,.45,5),-1.5,1.5,'dark',radius=.16)
 lathe('FrontSight_Pin',[(-3.4,0),(-3.4,.7),(3.4,.7),(3.4,0)],'dark',axis='X',center=(177,77.5),n=16)
def cylinder():
 star_points=[]
 for j in range(72):
  t=j*math.tau/72;r=10.25+7.45*(.5+.5*math.cos(6*(t-math.pi/3)))**2
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
 lathe('Extractor_Rod',[(REAR-1.2,0),(REAR-1.2,1.5),(182.0,1.5),(182.5,1.3),(182.5,0)],
       'steel','Extractor',center=(0,CY),n=24)
 lathe('Ejector_Tip',[(180,0),(180,1.65),(183.2,1.65),(183.8,1.4),(183.8,0)],
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
 # Muzzle-facing front curve and original hidden stop land/pivot retained.
 # Photo-scaled blade depth is 5.7 mm through the working middle, tapering
 # toward the toe; the old blade was only about 2.8 mm there.
 front=M.bezier((40,21),(33,16),(32,4),(42,-1.3),20)
 toe=M.bezier((42,-1.3),(43,-2.6),(40.9,-3.0),(38.4,-1.9),6)
 back=M.bezier((38.4,-1.9),(26.0,3),(26.0,15),(34.0,21),20)
 pts=[(26,24),(40,24),*front,*toe[1:],*back[1:],(26,22)]
 profile('Trigger_Shoe',pts,-3.5,3.5,'flat','Trigger',radius=.50)
 # Substantial forged body fits an 8 mm slot with .2 mm cheek clearance.
 hammer=M.fillet_polygon([(4,44),(15,44),(18.0,65),(18.0,69),(13.5,73.5),
  (6.2,73.5),(2.8,66),(0,61)],1.2,6)
 profile('Hammer_Body',hammer,-3.8,3.8,'flat','Hammer',radius=.45)
 box('Hammer_Nose',(-1.3,17.25,66.2),(1.3,18.8,67.8),'flat','Hammer',radius=.20,segments=2)
 loops=[]
 for y,z,w,d in [(8,70,3.6,3.3),(3,72,4.1,2.9),(-5,74.5,4.9,2.2),(-12,75.6,4.6,1.7)]:
  loops.append([(x,y,z+dz) for x,dz in rounded(2*w,2*d,.8,4)])
 reg(M.loft('Hammer_ThumbSpur',loops,MAT['flat']),'Hammer')
 # Cut a small original diamond field into the widened thumb face. This
 # is deliberately coarse checkpoint relief; fine pitch transfers by normal.
 spur=PARTS[-1]
 for sign in (-1,1):
  for offset in (-6,-3,0,3,6):
   # Diagonal tool bars across the top, seated in the spur's changing slope.
   vs=[]
   for x in (-5.2,5.2):
    y=-5.6+offset+sign*x*.62
    z=74.5-(y+5)*.19+2.0-(.06 if sign<0 else 0)
    vs.extend([(x,y-.17,z-.23),(x,y+.17,z-.23),(x,y+.17,z+.9),(x,y-.17,z+.9)])
   tool=M.mesh('tool',vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],MAT['flat'])
   cut(spur,tool)
 clean(spur)
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
 # Rubber is a volumetric subdivision cage. The sections vary from a narrow
 # rounded heel, through an egg-shaped palm swell, to a forward-narrowed neck
 # and a high wrap around the rear of the steel backstrap.
 # (height, rear surface, front surface, half width), all mm.
 rows=[(-66.5,-31,-27,1.4),(-66,-40,-17,8),(-64,-48,-5,13.3),
  (-60,-52.5,-1,15.5),(-54,-53.5,1,16.1),(-45,-52.2,3.2,16.6),
  (-35,-48.0,6.0,17.25),(-25,-42.4,9.0,17.7),(-15,-36.2,12.0,17),
  (-5,-31.2,14.4,15.7),(5,-27.0,15.8,14.8),(15,-25.0,15,13.7),
  (25,-24.8,11.2,12),(33,-29.7,6.2,10.5),(38,-27,-2,8.7),
  (42,-22,-8,5.5),(43,-17,-13,1)]
 original=rows;rows=[]
 for a,b in zip(original,original[1:]):
  steps=max(1,round((b[0]-a[0])/2.0))
  for k in range(steps):rows.append(tuple(a[j]+(b[j]-a[j])*k/steps for j in range(4)))
 rows.append(original[-1]);loops=[]
 for z,rear,front,hw in rows:
  center=(rear+front)/2;depth=(front-rear)/2;loop=[]
  for j in range(48):
   t=j*math.tau/48;c=math.cos(t);si=math.sin(t)
   # Broad back and tapered finger face, with the egg bias changing by height.
   bias=.12+.13*math.exp(-((z+20)/25)**2)
   x=hw*si*(1-bias*c)
   yy=center+depth*c
   if c>0:
    crest=sum(3.3*math.exp(-((z-zz)/3.7)**2) for zz in (-12,-32,-51))
    saddle=sum(2.2*math.exp(-((z-zz)/4.1)**2) for zz in (-2,-22,-41))
    yy+=(crest-saddle)*c**4
   # Dome the heel in the longitudinal direction instead of a flat cut.
   heel=3.4*max(0,min(1,(-60-z)/6.5))*c*c
   loop.append((x,yy,z+heel))
  loops.append(loop)
 o=M.loft('Grip_RubberMold',loops,MAT['rubber'])
 sub=o.modifiers.new('Compound service grip subdivision','SUBSURF');sub.levels=2;M.apply(o)
 tool=bpy.data.objects.new('Grip molding tool',SEATS['Frame'].copy());bpy.context.collection.objects.link(tool)
 tool.data.transform(Matrix.Diagonal(Vector((1.015,1.001,1.001,1))))
 cut(o,tool)
 remesh=o.modifiers.new('Finished rubber cavity remesh','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.30;remesh.use_smooth_shade=True;M.apply(o)
 relax=o.modifiers.new('Mold radius relaxation','SMOOTH');relax.factor=.32;relax.iterations=3;M.apply(o);M.smooth(o,70)
 HIGH[o.name]=o.data.copy();reg(o);reduce(o,5400)
 tree=BVHTree.FromPolygons([v.co for v in o.data.vertices],[tuple(f.vertices) for f in o.data.polygons])
 for side in (-1,1):
  # Recessed screw cup and a real slotted screw, supported in the molded flank.
  hit=tree.ray_cast(Vector((side*50,-18,-30)),Vector((-side,0,0)),100)
  assert hit[0] is not None,'Grip screw missed the actual surface'
  x=hit[0].x+side*.18
  lathe('Grip_ScrewCup',[(x-side*.6,1.6),(x-side*.6,3.4),(x,3.4),(x,1.6)],
   'dark',axis='X',center=(-18,-30),n=32,closed=True)
  screw('Grip_Screw',x+side*.12,-18,-30,2.2,'dark')
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
 limits={'Cylinder_Fluted':7700,'Frame_Forging':3700,'Grip_RubberMold':4200,
  'Barrel':2200,'Speedloader_Body':1200,'Speedloader_Release':310,'TriggerGuard_ForgedBow':700,
  'Extractor_Star':750,'Crane_Yoke':850,'Trigger_Shoe':550,'Hammer_Body':500,
  'Frame_Sideplate':400,'Hammer_ThumbSpur':650,'Latch_Thumbpiece':320,
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
 if o.name=='Frame_Forging':
  meridian=[(32.25,17),(33.0,18.5),(34.4,19),(35.5,18.8),(36.7,17),(37.1,14.8)]
  def shield_field(v):
   rr=math.hypot(v.x,v.z-CY)
   for i,((ya,ra),(yb,rb)) in enumerate(zip(meridian,meridian[1:])):
    if ya-.03<=v.y<=yb+.03:
     u=max(0,min(1,(v.y-ya)/(yb-ya)));radius=ra+(rb-ra)*u
     if abs(rr-radius)<.25:
      # Smooth tangents across the turned radius's section stations.
      before=(meridian[max(0,i-1)][1]-rb)/(meridian[max(0,i-1)][0]-yb)
      after=(meridian[min(len(meridian)-1,i+2)][1]-ra)/(meridian[min(len(meridian)-1,i+2)][0]-ya)
      slope=before*(1-u)+after*u
      return Vector((v.x/rr,-slope,(v.z-CY)/rr)).normalized()
   return None
  for f in o.data.polygons:
   vs=[o.data.vertices[i].co for i in f.vertices]
   fields=[shield_field(v) for v in vs]
   if all(n is not None for n in fields) and f.normal.dot(sum(fields,Vector())/3)>.3:
    for j,n in zip(f.loop_indices,fields):normals[j]=n
 if o.name=='Frame_Forging':
  for f in o.data.polygons:
   vs=[o.data.vertices[i].co for i in f.vertices]
   if all(34.20<v.y<37.85 and abs(math.hypot(v.x,v.z-CY)-5.65)<.08 for v in vs):
    for j in f.loop_indices:
     v=o.data.vertices[o.data.loops[j].vertex_index].co
     n=Vector((-v.x,0,CY-v.z)).normalized()
     if n.dot(f.normal)>.5:normals[j]=n
   if abs(f.normal.y)>.9999:
    for j in f.loop_indices:normals[j]=Vector((0,1 if f.normal.y>0 else -1,0))
 if o.name=='Barrel':
  outline=[Vector(p) for p in OUTLINES['Barrel']];fields=[]
  for i,p in enumerate(outline):
   t0=(p-outline[i-1]).normalized();t1=(outline[(i+1)%len(outline)]-p).normalized()
   t=(t0+t1).normalized();fields.append(Vector((-t.y,0,t.x)))
  def outer_field(v):
   point=Vector((v.x,v.z));best=None
   for i,a in enumerate(outline):
    b=outline[(i+1)%len(outline)];ab=b-a
    u=max(0,min(1,(point-a).dot(ab)/ab.length_squared))
    distance=(point-(a+ab*u)).length
    if best is None or distance<best[0]:best=(distance,(fields[i]*(1-u)+fields[(i+1)%len(fields)]*u).normalized())
   return best
  for f in o.data.polygons:
   if abs(f.normal.y)>.15:continue
   values=[outer_field(o.data.vertices[i].co) for i in f.vertices]
   if all(d<.06 and n.dot(f.normal)>.7 for d,n in values):
    for j,(_,n) in zip(f.loop_indices,values):normals[j]=n
 if o.name=='Barrel':
  for f in o.data.polygons:
   c=f.center;u=(c.y-(MUZZLE-5))/5;v=(c.z-53)/10.65
   if c.y>MUZZLE-5.05 and 42.3<c.z<53 and abs(u*u+v*v-1)<.08 and f.normal.y>.25:
    for j in f.loop_indices:
     p=o.data.vertices[o.data.loops[j].vertex_index].co
     normals[j]=Vector((0,(p.y-(MUZZLE-5))/25,(p.z-53)/(10.65**2))).normalized()
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
