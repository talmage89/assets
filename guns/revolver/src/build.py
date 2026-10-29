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
from mathutils.geometry import convex_hull_2d,barycentric_transform
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import model as M,weapon as W
from guns.common import magnum357
from parameters import *
from clips import build_clips
GENERATOR_HASH=generator_digest()
PARTS=[];MAT={};HIGH={};SEATS={};OUTLINES={};SKIN_FIELDS={}
def skin_field(name,loops):
 # Retain the analytic loft's smooth normals across Boolean machining and
 # reduction. A nearest triangle is only used on the original outer skin;
 # pocket walls, bore and planar end faces keep their independent fields.
 nr=len(loops);nc=len(loops[0]);points=[Vector(p) for row in loops for p in row]
 normals=[];faces=[]
 for j in range(nr):
  for i in range(nc):
   across=Vector(loops[j][(i+1)%nc])-Vector(loops[j][(i-1)%nc])
   along=Vector(loops[min(j+1,nr-1)][i])-Vector(loops[max(j-1,0)][i])
   normals.append(across.cross(along).normalized())
 for j in range(nr-1):
  for i in range(nc):
   a=j*nc+i;b=j*nc+(i+1)%nc;c=b+nc;d=a+nc
   faces.extend([(a,b,c),(a,c,d)])
 SKIN_FIELDS[name]=(BVHTree.FromPolygons(points,faces,all_triangles=True),points,faces,normals)
def clean(o,dist=.001):
 # Exact Boolean intersections can leave coincident seam vertices and
 # microscopic edges. Clean in mm, before their scale defeats decimation.
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=dist)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=dist)
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
    internal=(any((34<v.co.y<50 and 19<v.co.z<31 and abs(v.co.x)<6.5) or (81<v.co.y<95 and v.co.z<30)
      or (v.co.y<22 and v.co.z>42 and abs(v.co.x)<4.3) for v in e.verts)
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
 if o.name in ('Frame_Forging','GripMoldingEnvelope','Barrel','Hammer_Body','Hammer_ThumbSpur','Latch_Thumbpiece'):
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
  m=o.modifiers.new('Silhouette triangle budget','DECIMATE');m.ratio=target/n
  group=None
  if o.name=='Frame_Forging':
   # Preserve the accepted rolled recoil shield while the revised upper
   # crown uses its share of the same frame budget. Remove this temporary
   # modeling group before the unchanged rigid binding.
   group=o.vertex_groups.new(name='Accepted shield retention')
   ids=[v.index for v in o.data.vertices if 35.25<v.co.y<37.85 and abs(v.co.x)>8.9]
   if ids:group.add(ids,1,'REPLACE')
   m.vertex_group=group.name;m.invert_vertex_group=True;m.vertex_group_factor=1
  group_name=group.name if group else None
  M.apply(o)
  if group_name:
   current=o.vertex_groups.get(group_name)
   if current:o.vertex_groups.remove(current)
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
def checked_pad(name,rows,across,mat,bone,axis='Z',relief=.085):
 # Original fine pyramids on a curved pad, integrated into its closed mesh.
 # rows=(length station, half width, upper surface, lower surface).
 # Four triangles per tooth avoid thousands of tiny Boolean cutter seams.
 verts=[];faces=[];nr=len(rows);nc=across+1
 def point(u,v,h):return (u,v,h) if axis=='Z' else (h,u,v)
 for y,w,top,bottom in rows:
  for i in range(nc):
   u=-1+2*i/across;verts.append(point(w*u,y,top-.22*abs(u)**6))
 for j in range(nr-1):
  for i in range(across):
   ids=[j*nc+i,j*nc+i+1,(j+1)*nc+i+1,(j+1)*nc+i]
   center=sum((Vector(verts[k]) for k in ids),Vector())/4
   center[2 if axis=='Z' else 0]+=relief if axis=='Z' else -relief
   k=len(verts);verts.append(tuple(center))
   faces.extend((ids[t],ids[(t+1)%4],k) for t in range(4))
 base=len(verts)
 for y,w,top,bottom in rows:verts.extend([point(-w,y,bottom),point(w,y,bottom)])
 for j in range(nr-1):
  a=j*nc;b=(j+1)*nc;c=base+2*j;d=c+2
  faces.extend([(a,b,d,c),(a+across,c+1,d+1,b+across),(c,d,d+1,c+1)])
 faces.append(tuple([*range(nc-1,-1,-1),base,base+1]))
 faces.append(tuple([*( (nr-1)*nc+i for i in range(nc)),base+2*nr-1,base+2*nr-2]))
 return reg(M.mesh(name,verts,faces,MAT[mat]),bone)
def hammer_sections():
 return [(18.05,3.25,67.5,65.2),(17.8,3.68,68.0,62.2),
  (16.8,3.78,68.4,54.5),(15.3,3.78,68.6,46.0),
  (14,3.78,68.8,44.2),(10,3.78,69.1,44.2),
  (6,3.78,69.7,46.0),(4,3.75,70.25,52.5),
  (2,3.75,71.0,60.6),(0,4.0,71.8,63.8),
  (-2,4.55,72.8,66.0),(-4,5.0,73.5,67.3),
  (-6,5.05,74.0,68.15),(-7.5,4.8,74.1,68.55),
  (-8.5,4.3,73.9,68.8),(-9.0,2.7,73.5,69.5)]
def sculpted_hammer():
 # One subdivision cage: broad crescent cheeks flow through a thick thumb
 # tongue. Fine checkering belongs to the bake, not silhouette triangles.
 rows=hammer_sections()
 loops=[]
 for y,w,top,bottom in rows:
  mid=(top+bottom)/2;h=(top-bottom)/2
  loop=[]
  for i in range(24):
   t=i*math.tau/24;c=math.cos(t);s=math.sin(t)
   loop.append((w*math.copysign(abs(c)**.48,c),y,
    mid+h*math.copysign(abs(s)**.72,s)))
  loops.append(loop)
 ob=M.loft('Hammer_Body',loops,MAT['flat'])
 sub=ob.modifiers.new('Sculpted crescent cheek continuity','SUBSURF');sub.levels=2;M.apply(ob)
 M.smooth(ob,180);HIGH[ob.name]=ob.data.copy()
 reg(ob,'Hammer');reduce(ob,1250)
 return ob
def frame():
 # Forging volume varies in all three axes: broad recoil shoulder, lower
 # belly, neck and front collar. Machining leaves planar cheek lands.
 # The spine is one tangent-continuous sweep from the hand web into the
 # horizontal topstrap. Stations are samples of that radius, not facets.
 spine=M.bezier((-22,41),(.5,41),(2.5,77.4),(28,77.4),64)
 bottom=[(-22,25),(-12,15),(-3,12),(16,16),(34,20),(50,21.8),
  (56,21.4),(60,20.4),(64,18.8),(67,17.8),(69,17.8),(73,17.8),
  (78,17.8),(82,17.2),(86,16.4),(89,16.5),(92,19.0),(94,25.5),(96,43.0)]
 def height(y,rows):
  for (ya,a),(yb,b) in zip(rows,rows[1:]):
   if ya<=y<=yb:
    t=(y-ya)/(yb-ya);t=t*t*(3-2*t)
    return a+(b-a)*t
  return rows[-1][1]
 stations=[]
 def flow(y,rows):
  slopes=[(b-a)/(yb-ya) for (ya,a),(yb,b) in zip(rows,rows[1:])]
  tangents=[slopes[0]]+[0 if a*b<=0 else 2*a*b/(a+b) for a,b in zip(slopes,slopes[1:])]+[slopes[-1]]
  for i,((ya,a),(yb,b)) in enumerate(zip(rows,rows[1:])):
   if ya<=y<=yb:
    t=(y-ya)/(yb-ya);d=yb-ya
    return (2*t**3-3*t*t+1)*a+(t**3-2*t*t+t)*d*tangents[i]+(-2*t**3+3*t*t)*b+(t**3-t*t)*d*tangents[i+1]
  return rows[-1][1]
 for y in sorted(set([round(-22+1.5*i,4) for i in range(79)]+[28,34,56,64,67,69,73,78,82,84,87,90,92,94,95,96])):
  if y<28:
   for (ya,a),(yb,b) in zip(spine,spine[1:]):
    if ya<=y<=yb:top=a+(b-a)*(y-ya)/(yb-ya);break
  else:top=77.4 if y<=82 else height(y,[(82,77.4),(90,76.5),(96,72)])
  width=height(y,[(-22,5.2),(-16,8.3),(-8,8.8),(78,8.8),(85,10.8),(90,10.8),(96,9.5)])
  stations.append((y,width,flow(y,bottom) if y>=34 else height(y,bottom),top))
 loops=[]
 for y,w,a,b in stations:
  # Separate top and lower radii: the rear spine has a small, even round,
  # while the belly retains the broad forging radius around the crane.
  points=[]
  for sx,sz,start in [(1,1,0),(-1,1,90),(-1,-1,180),(1,-1,270)]:
   r=min(1.25 if sz>0 else 3.5,(b-a)*.23)
   for i in range(7):
    t=math.radians(start+90*i/6)
    points.append((sx*(w-r)+r*math.cos(t),y,(b if sz>0 else a)-sz*r+r*math.sin(t)))
   if sx==1 and sz==1:
    # Resolve the transverse crown behind the sight instead of spanning
    # its whole width with one flat face. The longitudinal spine stays put.
    points.extend((w-r-2*(w-r)*j/12,y,b) for j in range(1,12))
  crown=max(0,min(1,(28-y)/14));crown=crown*crown*(3-2*crown)
  upper=max(0,min(1,(b-61)/9));crown*=upper*upper*(3-2*upper)
  points=[(x,yy,z-3.0*crown*(x/w)**2*max(0,min(1,(z-(b-8))/8))**2)
   for x,yy,z in points]
  loops.append(points)
 skin_field('Frame_Forging',loops)
 o=M.loft('Frame_Forging',loops,MAT['steel'])
 # An uninterrupted large-radius rear contour, not a plate outlined by bevels.
 shield=lathe('tool',[(35.5,0),(35.5,17.6),(35.8,18.6),(36.3,19.25),
  (37.35,19.25),(37.65,18.95),(37.65,0)],center=(0,CY),n=72,register=False)
 cut(o,shield,'UNION')
 # A closed molding envelope excludes lockwork slots from the rubber seat.
 # Keep the accepted rubber molding envelope independent of these upper
 # frame edits. Its original round-three sections are rebuilt below.
 old_stations=[]
 old_bottom=[(-22,25),(-12,15),(-3,12),(16,16),(34,20),(56,22.8),(78,24),(84,22),(87,22),(91,20.5),(94,25.5),(96,43)]
 for y in sorted(set([round(-22+1.5*i,4) for i in range(34)]+[28,34,56,78,82,84,87,90,92,94,95,96])):
  top=next((za+(zb-za)*(y-ya)/(yb-ya) for (ya,za),(yb,zb) in zip(spine,spine[1:]) if ya<=y<=yb),77.4 if y<=82 else height(y,[(82,77.4),(90,76.5),(96,72)]))
  width=height(y,[(-22,5.2),(-16,8.3),(-8,8.8),(78,8.8),(90,9.7),(96,9.5)])
  low=height(y,old_bottom)
  old_stations.append([(x,y,z+(low+top)/2) for x,z in rounded(2*width,top-low,min(3.5,(top-low)*.23),8)])
 mold=M.loft('GripMoldingEnvelope',old_stations,MAT['steel'])
 old_shield=lathe('tool',[(32.25,0),(32.25,17),(33,18.5),(34.4,19),(35.5,18.8),(36.7,17),(37.1,14.8),(37.1,0)],center=(0,CY),n=72,register=False)
 cut(mold,old_shield,'UNION');SEATS['Grip']=mold.data.copy();bpy.data.objects.remove(mold,do_unlink=True)
 # 0.45 mm radial running light around the accepted cylinder envelope.
 window=[(y+60.225,z+48.2) for y,z in rounded(45.15,40.3,.65,6)]
 tool=profile('tool',window,-30,30,register=False)
 # Closely wrapped upper shoulders follow the cylinder's radial envelope.
 # The floor stays at its accepted level for the leftward swing.
 roof_limit=[(-30,-50),(30,-50),(30,48.2)]
 roof_limit += [(20.15*math.cos(t),48.2+20.15*math.sin(t)) for t in [math.pi*i/64 for i in range(65)]]
 roof_limit.append((-30,48.2))
 cut(tool,profile('tool',roof_limit,30,90,axis='Y',register=False),'INTERSECT');cut(o,tool)
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
 cut(o,profile('tool',release,35.52,37.8,axis='Y',register=False))
 # The cylinder's center rises 1.1 mm during early swing-out. A left-only
 # underside chamfer clears that arc, while the center/right rail hugs it.
 roof=[(-22,65),(-22,70.9),(0,68.35),(0,65)]
 cut(o,profile('tool',roof,37.1,82.9,axis='Y',register=False))
 # A shallow tapered sight mortise gives the leaf a seated front tongue.
 groove=M.loft('tool',[[(x,y,z+78.6) for x,z in rounded(w,2.9,.25,3)]
  for y,w in [(31,12.1),(36,11.3),(47,9.7),(59,7.5),(65.5,6.1)]],MAT['steel'])
 cut(o,groove)
 # Hammer/trigger slots and front crane heel pocket are visible machining.
 # Close all unused space behind the hammer. This narrow pocket is the
 # swept *body*, rather than a rectangular trough through the backstrap.
 rows=hammer_sections()
 outline=[(y,top) for y,w,top,bottom in rows]+[(y,bottom) for y,w,top,bottom in reversed(rows)]
 # Include the accepted strike nose in this single section cutter. Separate
 # overlapping coplanar nose cutters leave microscopic nonmanifold seams.
 outline[0]=(19.10,68.10);outline[-1]=(19.10,65.90)
 area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1]))
 outline=M.offset_profile(outline,-.28 if area>0 else .28)
 # Resolve the concave swept section before cutting the forging. Repeated
 # overlapping Boolean cuts spent the frame budget on invisible sawteeth.
 # A convex hull, however, removes the unoccupied backstrap under the tongue.
 sweeps=[]
 for angle in range(0,36,1):
  t=math.radians(angle)
  section=[(10+(y-10)*math.cos(t)-(z-48)*math.sin(t),
   48+(y-10)*math.sin(t)+(z-48)*math.cos(t)) for y,z in outline]
  sweeps.append(section)
 stations=sorted(set(round(y,6) for section in sweeps for y,z in section))
 lo,hi=stations[0],stations[-1]
 stations=sorted(set(stations+[lo+(hi-lo)*j/math.ceil((hi-lo)/.20) for j in range(math.ceil((hi-lo)/.20)+1)]))
 lower=[];upper=[]
 for y in stations:
  hits=[]
  for section in sweeps:
   for (ya,za),(yb,zb) in zip(section,section[1:]+section[:1]):
    if abs(yb-ya)>1e-8 and min(ya,yb)-1e-6<=y<=max(ya,yb)+1e-6:
     hits.append(za+(zb-za)*(y-ya)/(yb-ya))
  if hits:lower.append((y,min(hits)-.04));upper.append((y,max(hits)+.04))
 def simplify(points,tolerance=.025):
  if len(points)<3:return points
  a,b=Vector(points[0]),Vector(points[-1]);ab=b-a
  distances=[(Vector(p)-a-ab*max(0,min(1,(Vector(p)-a).dot(ab)/ab.length_squared))).length for p in points[1:-1]]
  i=max(range(len(distances)),key=distances.__getitem__)+1
  if distances[i-1]<=tolerance:return [points[0],points[-1]]
  return simplify(points[:i+1],tolerance)[:-1]+simplify(points[i:],tolerance)
 swept=simplify(upper)+list(reversed(simplify(lower)))
 cut(o,profile('tool',swept,-4,4,register=False))
 cutbox(o,(-4.1,26,12),(4.1,44,26))
 cutbox(o,(-22,82.6,12),(6.5,90.0,54.7))
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
 # The plate is a patch of the same forging skin. Its curved lower edge must
 # follow that skin, instead of standing proud as a constant-thickness slab.
 plate_skin=bpy.data.objects.new('Frame_Sideplate',o.data.copy());bpy.context.collection.objects.link(plate_skin)
 area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(plate,plate[1:]+plate[:1]))
 plate2=M.offset_profile(plate,.10 if area>0 else -.10)
 cut(plate_skin,profile('tool',plate2,7.55,12,register=False),'INTERSECT')
 for v in plate_skin.data.vertices:v.co.x-=.025
 cut(o,profile('tool',plate,7.50,12,register=False))
 # Blend the crane bearing heel into the same forging. The old separately
 # perched support box made a conspicuous step below the barrel shank.
 cut(o,lathe('tool',[(89.7,0),(89.7,2.75),(94.5,2.75),(94.5,0)],center=(-8,20),n=24,register=False))
 # Retain the closed pre-bevel machining solid as the rubber molding tool;
 # bevel miter intersections are unsuitable for a subsequent Boolean cutter.
 SEATS['Frame']=o.data.copy()
 # The forging's broad radii are in its loft. Machined pocket lips carry a
 # smaller cutter break so close internal pockets cannot collapse the bevel.
 reg(o,radius=.12,segments=2);reduce(o,5600)
 plate_skin.data.materials.clear();plate_skin.data.materials.append(MAT['steel'])
 reg(plate_skin,radius=.045,segments=2)
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
 a0=math.acos(.55);a1=math.acos(.96)
 shoulder=[(10*math.cos(a0+(a1-a0)*i/24),BORE+10*math.sin(a0+(a1-a0)*i/24)) for i in range(25)]
 # The lower web is tangent to the barrel flat, then rolls through a broad
 # elliptical underside. No inset rail, crease or chamfered bottom shelf.
 lower=M.bezier((9.6,57.0),(9.6,54.0),(8.2,53.5),(8.2,50.2),16)
 bottom=[(8.2*math.cos(t),50.2-7.85*math.sin(t))
  for t in [j*math.pi/48 for j in range(1,25)]]
 # Tangent rib root: a 1.5 mm concave radius, rather than a plank on a tube.
 rib=M.bezier((3.4,76.4),(3.4,70.6),(3.9,70.4),shoulder[0],16)
 half=[*rib,*shoulder[1:],(9.6,57.0),*lower[1:],*bottom]
 perimeter=half+[(-x,z) for x,z in half[-2::-1]]
 outline=M.fillet_polygon(perimeter,[1.15 if z<53 else .35 for x,z in perimeter],5)
 OUTLINES['Barrel']=outline
 loops=[[(x,y,z) for x,z in outline] for y in (95.8,MUZZLE-8)]
 # The end is a rolled surface in both directions. Deep quarter-elliptic
 # rounds on the lug meet the small accepted barrel/crown lip continuously.
 # Each section is authored explicitly; there is no cut-and-warp cap shelf.
 for j in range(9):
  t=j*math.pi/16;row=[]
  for x,z in outline:
   u=max(0,min(1,(57-z)/5));u=u*u*(3-2*u)
   axial=.8+6.2*u;inset=(.55+3.0*u)*(1-math.cos(t))
   center=BORE*(1-u)+CY*u
   row.append((x*(1-inset/12),MUZZLE-axial+axial*math.sin(t),center+(z-center)*(1-inset/12)))
  loops.append(row)
 skin_field('Barrel',loops)
 o=M.loft('Barrel',loops,MAT['steel'])
 # Cone joins inside the exterior; the round bore is a separate cutter. This
 # avoids folded polar caps between the rolled lug nose and the bore rim.
 cone=lathe('tool',[(BREECH,0),(BREECH,6.7),(85,7.8),(96.3,9.6),(96.3,0)],n=96,center=(0,BORE),register=False)
 cut(o,cone,'UNION')
 # Recessed crown: a clean annular floor behind a rounded protective lip.
 bore=lathe('tool',[(81,0),(81,4.65),(BREECH,4.65),(85,4.52),
  (MUZZLE-1.7,4.52),(MUZZLE-1.45,4.8),(MUZZLE-1.45,7.45),
  (MUZZLE-1.2,7.7),(MUZZLE-.35,7.7),(MUZZLE,7.95),
  (MUZZLE+1,7.95),(MUZZLE+1,0)],center=(0,BORE),n=96,register=False)
 cut(o,bore)
 # Bore around the rod; the narrow upper-left release is the actual swept
 # passage required by the accepted crane arc, rather than the old open hook.
 cut(o,lathe('tool',[(90,0),(90,3.15),(178.0,3.15),(179.5,3.45),
  (MUZZLE+1,3.45),(MUZZLE+1,0)],center=(0,CY),n=48,register=False))
 pts=[]
 for j in range(17):
  theta=math.radians(-j*2.5);x=CRANE[0]+8*math.cos(theta)+28.2*math.sin(theta)
  z=CRANE[2]-8*math.sin(theta)+28.2*math.cos(theta)
  pts.append((x,z))
 upper=[(x,z+3.15) for x,z in pts];lower=[(x,z-3.15) for x,z in reversed(pts)]
 cut(o,profile('tool',upper+lower,90,MUZZLE+1,axis='Y',register=False))
 upper=[(x,z+3.45) for x,z in pts];lower=[(x,z-3.45) for x,z in reversed(pts)]
 cut(o,profile('tool',upper+lower,178.0,MUZZLE+1,axis='Y',register=False))
 reg(o)
 # Pinned ramp is seated in a milled rib pocket.
 ramp=[(163.5,76.15),*M.bezier((163.5,76.5),(168,76.8),(174,82.4),(176,83),12),
  (180,83),(180,76.15)]
 front=profile('FrontSight_PinnedRamp',M.fillet_polygon(ramp,.35,5),-1.5,1.5,'dark',register=False)
 for v in front.data.vertices:
  v.co.x*=1+1.9/1.5*max(0,min(1,(79-v.co.z)/2.6))
 reg(front,radius=.20)
 lathe('FrontSight_Pin',[(-2.65,0),(-2.65,.7),(2.65,.7),(2.65,0)],'dark',axis='X',center=(177,77.5),n=16)
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
 # Keep the accepted concealed journals and axial endpoints. Only the
 # exposed forward shaft grows; it still passes through the original yoke.
 lathe('Extractor_Rod',[(REAR-1.2,0),(REAR-1.2,1.5),(111.0,1.5),
  (112.0,2.6),(112.7,2.9),(182.0,2.9),(182.5,2.7),(182.5,0)],
       'steel','Extractor',center=(0,CY),n=24)
 lathe('Ejector_Tip',[(180,0),(180,3.0),(180.3,3.2),(183.2,3.2),(183.8,2.8),(183.8,0)],
       'steel','Extractor',center=(0,CY),n=32)
 for i in range(6):
  t=i*math.tau/6
  pts=[(r*math.cos(a),CY+r*math.sin(a)) for r,a in
       [(2.8,t),(5.3,t+.06),(5.3,t+.42),(3.1,t+.73)]]
  profile('Extractor_Ratchet'+str(i),pts,REAR-2.3,REAR-1.4,'dark','Extractor',axis='Y',radius=.12)
def crane_controls():
 # Forged yoke has two bored bosses and an offset web, in the front plane.
 # The dark hanging rectangle in the old side view was the yoke's lower
 # web, not an extra accessory. Round its pivot boss and taper the web.
 outline=M.fillet_polygon([(-11.3,20),(-10.4,17.1),(-7.1,16.9),(-4.9,19.2),
  (4.6,43),(4.6,50),(1,53),(-4,51),(-8.2,29)],2.1,8)
 o=profile('Crane_Yoke',outline,83.0,88.8,'steel','Crane',axis='Y',register=False)
 cut(o,lathe('tool',[(82,0),(82,3.0),(90,3.0),(90,0)],center=(0,CY),n=32,register=False))
 cut(o,lathe('tool',[(82,0),(82,2.7),(90,2.7),(90,0)],center=(-8,20),n=24,register=False))
 cut(o,lathe('tool',[(82,0),(82,9.85),(90,9.85),(90,0)],center=(0,BORE),n=48,register=False))
 reg(o,'Crane',.85,4)
 lathe('Crane_UpperBearing',[(82.8,1.75),(82.8,4.4),(84.0,4.4),(84.0,1.75)],
  'steel','Crane',center=(0,CY),n=32,closed=True)
 lathe('Crane_Axle',[(70,1.75),(70,3.0),(84,3.0),(84,1.75)],'steel','Crane',center=(0,CY),n=32,closed=True)
 lathe('Crane_Pivot',[(81,0),(81,2.6),(91,2.6),(91,0)],'dark','Root',center=(-8,20),n=24)
 box('Crane_ClosedSeat',(-9.7,88.8,19),(-6.3,90,24),radius=.10)
 # A thumb dish swells out from its recessed stem. Fine teeth occupy the
 # forward pad; the screw sits on a clear radiused land at its rear.
 rows=[]
 for j in range(13):
  z=49+j*.65;t=j/12
  width=2.5+3.5*math.sin(math.pi*t)**.65
  rows.append((z,width,-12.0-.7*math.sin(math.pi*t),-9.0))
 o=checked_pad('Latch_Thumbpiece',rows,12,'steel','Latch',axis='X',relief=.10)
 for v in o.data.vertices:v.co.y+=23
 for v in o.data.vertices:
  if v.co.x< -11:
   distance=math.hypot(v.co.y-19.7,v.co.z-53.2)
   blend=max(0,min(1,(2.7-distance)/.7));blend=blend*blend*(3-2*blend)
   v.co.x=v.co.x*(1-blend)-12.48*blend
 screw('Latch_Screw',-12.45,19.7,53.2,1.5,bone='Latch')
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
 sculpted_hammer()
 box('Hammer_Nose',(-1.3,17.25,66.2),(1.3,18.8,67.8),'flat','Hammer',radius=.20,segments=2)
 screw('Hammer_PivotHead',8.9,10,48,1.55)
 # Leaf, hinge and adjustment housing visibly sit on the topstrap's recess.
 loops=[]
 for y,w,bottom,top in [(30,5.8,77.20,80.1),(35,5.5,77.20,80.0),
  (46,4.7,77.20,79.4),(58,3.6,77.20,78.7),(65,2.8,77.20,78.3)]:
  loops.append([(x,y,z+(bottom+top)/2) for x,z in rounded(w*2,top-bottom,.40,4)])
 reg(M.loft('RearSight_Leaf',loops,MAT['dark']))
 blade=[(-7.4,78.7),(-7.4,82.3),(-6.7,83),(-2,83),(-2,80.1),
  (2,80.1),(2,83),(6.7,83),(7.4,82.3),(7.4,78.7)]
 base=profile('RearSight_NotchBody',M.fillet_polygon(blade,.16,3),27.4,28.55,'dark',axis='Y',register=False)
 housing=M.loft('tool',[[(x,y,z+center) for x,z in rounded(w,depth,.55,4)]
  for y,w,depth,center in [(28.3,14.2,3.6,80.0),(30.0,14.0,3.3,79.95),(33.5,11.5,2.0,79.4)]],MAT['dark'])
 cutbox(housing,(-2.0,26,80.05),(2.0,35,85));cut(base,housing,'UNION')
 reg(base,radius=.12,segments=2)
 # Elevation screw is sunk into the leaf, windage screw sits transversely.
 elev=lathe('RearSight_ElevationScrew',[(79.5,0),(79.5,1.7),(80.2,1.7),(80.2,0)],'dark',axis='Z',center=(0,45),n=24,register=False)
 cutbox(elev,(-2,44.7,80.0),(2,45.3,81));reg(elev,radius=.05,segments=2)
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
 remesh=o.modifiers.new('Finished rubber cavity remesh','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.30;remesh.use_smooth_shade=True;M.apply(o)
 relax=o.modifiers.new('Mold radius relaxation','SMOOTH');relax.factor=.32;relax.iterations=3;M.apply(o);M.smooth(o,70)
 # Cut after the surface relaxation. Voxelizing an already cut lip produced
 # the torn, stair-stepped seam seen at the prior checkpoint.
 tool=bpy.data.objects.new('Grip molding tool',SEATS['Grip'].copy());bpy.context.collection.objects.link(tool)
 tool.data.transform(Matrix.Diagonal(Vector((1.020,1.003,1.003,1))))
 cut(o,tool)
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
 limits={'Cylinder_Fluted':7700,'Frame_Forging':3500,'Grip_RubberMold':4200,
  'Barrel':2500,'Speedloader_Body':1200,'Speedloader_Release':310,'TriggerGuard_ForgedBow':700,
  'Extractor_Star':750,'Crane_Yoke':850,'Trigger_Shoe':550,'Hammer_Body':1950,
  'Frame_Sideplate':320,'Hammer_ThumbSpur':1450,'Latch_Thumbpiece':680,
  'RearSight_Leaf':250,'RearSight_NotchBody':400,'Crane_PivotSupport':180}
 limit=limits.get(o.name,144 if 'Screw' in o.name or 'PivotHead' in o.name else 210)
 if o.name.startswith(('Live','Case','LoaderRound','InsertRound')):limit=1000
 reduce(o,limit)
 if o.name=='Barrel':clean(o,dist=.004)
 tri=o.modifiers.new('Budget triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(o)
 if o.name in ('Speedloader_Body','Barrel','Cylinder_Fluted','Frame_Forging','Frame_Sideplate','Extractor_Star','Latch_Thumbpiece','RearSight_NotchBody'):
  # Reseed the machining fields after QEM, rather than interpolating obsolete
  # Boolean corner normals into wavy cap and pocket highlights.
  o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));M.smooth(o,42)
  wn=o.modifiers.new('Final machined surface normals','WEIGHTED_NORMAL');wn.keep_sharp=True;wn.weight=50;M.apply(o)
 normals=[n.vector.copy() for n in o.data.corner_normals]
 if o.name in ('Frame_Forging','Frame_Sideplate','Speedloader_Body','Speedloader_Release','Extractor_Star'):
  axis=0 if o.name.startswith('Frame_') else 1
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
  meridian=[(35.5,17.6),(35.8,18.6),(36.3,19.25),(37.35,19.25),(37.65,18.95)]
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
 if o.name in SKIN_FIELDS:
  tree,points,triangles,field=SKIN_FIELDS[o.name]
  for f in o.data.polygons:
   if o.name=='Frame_Forging':
    if not (f.center.y<28 and f.center.z>40):continue
    nearest=tree.find_nearest(f.center)
    if nearest[0] is None or nearest[3]>.15:continue
   for j in f.loop_indices:
    v=o.data.vertices[o.data.loops[j].vertex_index].co
    p,_,index,distance=tree.find_nearest(v)
    if p is None or distance>(.20 if o.name=='Frame_Forging' else .035):continue
    ids=triangles[index]
    n=barycentric_transform(p,*[points[k] for k in ids],*[field[k] for k in ids]).normalized()
    if n.dot(f.normal)>.70:normals[j]=n
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
 # Fine teeth need their individual facet normals: smoothing all four sides
 # of a sub-millimeter pyramid averages them back into an invisible roof.
 if o.name=='Latch_Thumbpiece':
  for f in o.data.polygons:
   if f.normal.x<-.25:
    for j in f.loop_indices:normals[j]=f.normal.copy()
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
 # Dense molded/sculpted sources are retained together for the isolated bake.
 saved={}
 for name,data in HIGH.items():
  data.transform(Matrix.Scale(.001,4));ob=bpy.data.objects[name];saved[name]=ob.data;ob.data=data
  ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(data.vertices))),1,'REPLACE')
 bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'))
 for name,data in saved.items():
  ob=bpy.data.objects[name];ob.data=data
  ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(data.vertices))),1,'REPLACE')
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
