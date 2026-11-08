"""Trim the course's grade-backed route slabs at real common junctions.

Lane centerlines and routing stay fixed. At overlapping approaches the earlier
slab owns the joint; the later slab meets its surface and is trimmed at its edge.
Spanning decks and tee/cup flights retain their explicit bearing construction.
"""
import math
from collections import Counter
import bpy,bmesh
from mathutils import Vector
from kit import model as G

def cross(a,b,c):return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x)
def area(poly):return abs(sum(a.x*b.y-a.y*b.x for a,b in zip(poly,poly[1:]+poly[:1])))/2

def half(poly,a,b,inside=True):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  dp,dq=cross(a,b,p),cross(a,b,q);ip=dp>=-1e-9 if inside else dp<=1e-9;iq=dq>=-1e-9 if inside else dq<=1e-9
  if ip:out.append(p.copy())
  if ip!=iq:
   t=dp/(dp-dq);out.append(p+(q-p)*t)
 return out

def difference(poly,cut):
 common=poly
 for a,b in zip(cut,cut[1:]+cut[:1]):
  common=half(common,a,b)
  if len(common)<3:return [poly]
 if area(common)<1e-8:return [poly]
 inside=poly;outside=[]
 for a,b in zip(cut,cut[1:]+cut[:1]):
  part=half(inside,a,b,False)
  if len(part)>2 and area(part)>1e-9:outside.append(part)
  inside=half(inside,a,b)
  if len(inside)<3:return outside
 return outside

def nearest(poly,q):
 if all(cross(a,b,q)>=-1e-7 for a,b in zip(poly,poly[1:]+poly[:1])):return 0.,q
 best=(1e10,None)
 for a,b in zip(poly,poly[1:]+poly[:1]):
  d=Vector((b.x-a.x,b.y-a.y,0));p=Vector((q.x,q.y,0));aa=Vector((a.x,a.y,0));t=max(0,min(1,(p-aa).dot(d)/max(1e-12,d.length_squared)));hit=aa+d*t;distance=(p-hit).length
  if distance<best[0]:best=(distance,hit)
 return best

def plane(poly,q):
 a,b,c=poly;n=(b-a).cross(c-a)
 return a.z-(n.x*(q.x-a.x)+n.y*(q.y-a.y))/n.z

def bounds(poly):return (min(q.x for q in poly),max(q.x for q in poly),min(q.y for q in poly),max(q.y for q in poly))
def near(a,b,margin=0):return not(a[1]+margin<b[0] or a[0]-margin>b[1] or a[3]+margin<b[2] or a[2]-margin>b[3])

def conform(vs,faces):
 """Share every projected T vertex; triangulate convex fragments in XY.

 A 3D ngon triangulator may discard a collinear XY vertex whose Z changed
 during grading. A centre fan preserves the graded boundary on both sides.
 """
 used=sorted({i for f in faces for i in f});grid={};cell=.25
 for i in used:grid.setdefault((math.floor(vs[i].x/cell),math.floor(vs[i].y/cell)),[]).append(i)
 out=[]
 for face in faces:
  boundary=[]
  for a,b in zip(face,face[1:]+face[:1]):
   qa,qb=vs[a],vs[b];dx,dy=qb.x-qa.x,qb.y-qa.y;length2=dx*dx+dy*dy;points=[(0.,a)]
   if length2>1e-12:
    lo,hi=min(qa.x,qb.x)-1e-5,max(qa.x,qb.x)+1e-5;bottom,top=min(qa.y,qb.y)-1e-5,max(qa.y,qb.y)+1e-5
    candidates={i for x in range(math.floor(lo/cell),math.floor(hi/cell)+1) for y in range(math.floor(bottom/cell),math.floor(top/cell)+1) for i in grid.get((x,y),())}
    for i in sorted(candidates):
     if i in (a,b):continue
     q=vs[i];t=((q.x-qa.x)*dx+(q.y-qa.y)*dy)/length2
     if 1e-6<t<1-1e-6 and abs(dx*(q.y-qa.y)-dy*(q.x-qa.x))/math.sqrt(length2)<1e-5:points.append((t,i))
   for t,i in sorted(points):
    if not boundary or (vs[i].xy-vs[boundary[-1]].xy).length>1e-5:boundary.append(i)
  if len(boundary)>2 and (vs[boundary[0]].xy-vs[boundary[-1]].xy).length<1e-5:boundary.pop()
  if len(boundary)<3:continue
  if len(boundary)==3:out.append(tuple(boundary));continue
  center=sum((vs[i] for i in boundary),Vector())/len(boundary);k=len(vs);vs.append(center)
  out.extend((k,a,b) for a,b in zip(boundary,boundary[1:]+boundary[:1]) if abs(cross(center,vs[a],vs[b]))>1e-10)
 return vs,out

def fixture():
 square=[Vector(q) for q in ((0,0,0),(1,0,0),(1,1,0),(0,1,0))]
 outside=[Vector(q) for q in ((2,0,0),(3,0,0),(2,1,0))]
 assert len(difference(square,outside))==1 and abs(area(difference(square,outside)[0])-1)<1e-8
 half_square=[Vector(q) for q in ((0,0,0),(1,0,0),(0,1,0))]
 assert abs(sum(area(q) for q in difference(square,half_square))-.5)<1e-8
 covering=[Vector(q) for q in ((-2,-2,0),(4,-2,0),(-2,4,0))]
 assert not difference(square,covering)

def resolve(rt,materials,grade):
 fixture()
 walks=[o for o in rt.children if o.type=='MESH' and o.get('walk_rows')]
 walks.sort(key=lambda o:(0 if o.name.startswith('Curving lane-side') else 1 if 'route connection' in o.name or 'adventure link' in o.name else 2,o.name))
 prior=[];grid={};report=[];cell=2.5
 def cells(box,margin=0):
  return ((x,y) for x in range(math.floor((box[0]-margin)/cell),math.floor((box[1]+margin)/cell)+1) for y in range(math.floor((box[2]-margin)/cell),math.floor((box[3]+margin)/cell)+1))
 def query(box):
  indices=sorted({i for key in cells(box) for i in grid.get(key,())})
  return [prior[i] for i in indices if near(box,prior[i][1])]
 for ob in walks:
  for end in (0,1):
   n=ob['walk_rows'];indices=(0,1) if end==0 else (2*n-2,2*n-1)
   ob['join_probe_'+str(end)]=[value for k in indices for value in ob.data.vertices[k].co]
  ob.data.calc_loop_triangles();vs=[v.co.copy() for v in ob.data.vertices];source=[[vs[k].copy() for k in t.vertices] for t in ob.data.loop_triangles]
  for tri in source:
   if cross(*tri)<0:tri.reverse()
  pieces=[];adjust={};cuts=0
  for tri in source:
   fragments=[tri];tb=bounds(tri)
   for cut,box in query(tb):
    if not near(tb,box):continue
    common=tri
    for a,b in zip(cut,cut[1:]+cut[:1]):
     common=half(common,a,b)
     if len(common)<3:break
    if len(common)<3 or area(common)<1e-8:continue
    adjust[id(cut)]=cut;cuts+=1
    fragments=[part for poly in fragments for part in difference(poly,cut)]
    if not fragments:break
   pieces.extend(fragments)
  if cuts:
   # Blend only within 0.9m of an actual overlap, giving one common grade at
   # the butt joint rather than an upper slab passing through a lower one.
   cached={};adjusted=[(cut,bounds(cut)) for cut in adjust.values()];local_grid={}
   for i,(cut,box) in enumerate(adjusted):
    for key in cells(box,.9):local_grid.setdefault(key,[]).append(i)
   def height(q):
    key=tuple(round(v,7) for v in q)
    if key in cached:return cached[key].copy()
    best=(.9,None,None)
    for i in local_grid.get((math.floor(q.x/cell),math.floor(q.y/cell)),()):
     cut,box=adjusted[i]
     if not near((q.x,q.x,q.y,q.y),box,.9):continue
     distance,hit=nearest(cut,q)
     if distance<best[0]:best=(distance,cut,hit)
    if best[1] is None:cached[key]=q.copy();return q.copy()
    distance,cut,hit=best;weight=(1-distance/.9)**2;v=q.copy();v.z=q.z*(1-weight)+plane(cut,hit)*weight;cached[key]=v.copy();return v
   vs=[height(q) for q in vs];lookup={tuple(round(v,6) for v in q):i for i,q in enumerate(vs)};faces=[]
   for poly in pieces:
    indices=[]
    for q in poly:
     q=height(q);key=tuple(round(v,6) for v in q)
     if key not in lookup:lookup[key]=len(vs);vs.append(q)
     index=lookup[key]
     if not indices or indices[-1]!=index:indices.append(index)
    if indices and indices[0]==indices[-1]:indices.pop()
    if len(set(indices))>2:faces.append(tuple(indices))
   vs,faces=conform(vs,faces)
   temp=G.mesh('Joined route surface tool',vs,faces,materials['concrete']);old=ob.data;ob.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
   if old.users==0:bpy.data.meshes.remove(old)
   bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update()
   bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-10],context='FACES')
   bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0]);bm.to_mesh(ob.data);bm.free();ob.data.update()
   for support in list(rt.children):
    if support.get('support_for')==ob.name:bpy.data.objects.remove(support,do_unlink=True)
   vs=[v.co.copy() for v in ob.data.vertices];faces=[tuple(f.vertices) for f in ob.data.polygons]
   # Rebuild the grade backing at the trimmed boundary; no old fill can
   # protrude through a lowered approach.
   counts=Counter(tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1]));edges=[e for e,n in counts.items() if n==1];sv=[];sf=[]
   for a,b in edges:
    qa,qb=vs[a],vs[b]
    if (qa.xy-qb.xy).length<.00002:continue
    k=len(sv);sv.extend(((qa.x,qa.y,qa.z-.10),(qb.x,qb.y,qb.z-.10),(qb.x,qb.y,min(qb.z-.12,.015+grade(qb.y)-.08)),(qa.x,qa.y,min(qa.z-.12,.015+grade(qa.y)-.08))));sf.append((k,k+1,k+2,k+3))
   if sf:
    support=G.mesh('Compacted support below joined walk',sv,sf,materials['soil']);support.parent=rt;support['solid']=False;support['walk_cleanup']=True
  G.smooth(ob,30)
  bm=bmesh.new();bm.from_mesh(ob.data)
  for edge in bm.edges:
   if edge.is_boundary:edge.smooth=False
  bm.to_mesh(ob.data);bm.free();ob.data.update()
  ob.data.calc_loop_triangles()
  for t in ob.data.loop_triangles:
   tri=[ob.data.vertices[k].co.copy() for k in t.vertices]
   if cross(*tri)<0:tri.reverse()
   box=bounds(tri);index=len(prior);prior.append((tri,box))
   for key in cells(box):grid.setdefault(key,[]).append(index)
  report.append(dict(walk=ob.name,overlapping_triangle_pairs_trimmed=cuts,retained_top_triangles=len(ob.data.loop_triangles)))
  if cuts:print('WALK JOIN',ob.name,cuts,'overlaps',len(ob.data.loop_triangles),'triangles',flush=True)
 rt['walk_trim_report']=__import__('json').dumps(report)
