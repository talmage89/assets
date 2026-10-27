"""Resolve the source roof's course/roll addressing into ordinary UV0 charts.

Clip each triangle in its original affine UV domain at course, roll and
shifted-U wrap boundaries. Interpolate position, tint and split normal using
barycentric weights. No runtime math nodes or shader extensions are exported.
"""
import math
import bpy
import bmesh
import numpy as np
from mathutils import Vector


def phase(row,roll):
 # Source shader Math sockets evaluate float32, including the sine argument.
 f=np.float32
 return float(f(f(np.sin(f(f(row)*f(12.9898)+f(roll)*f(78.233))))*f(437.15)))


def clip(poly,axis,bound,positive):
 result=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=a[0][axis]-bound;db=b[0][axis]-bound
  inside_a=da>=0 if positive else da<=0;inside_b=db>=0 if positive else db<=0
  if inside_a:result.append(a)
  if inside_a!=inside_b:
   t=da/(da-db);result.append((a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t))
 return result


def partitions(poly,axis,step):
 lo=min(p[0][axis] for p in poly);hi=max(p[0][axis] for p in poly)
 result=[]
 for cell in range(math.floor(lo/step+1e-7),math.ceil(hi/step-1e-7)):
  p=clip(clip(poly,axis,cell*step,True),axis,(cell+1)*step,False)
  if len(p)>=3:result.append((cell,p))
 return result


def snap(value,step):
 target=round(value/step)*step
 return target if abs(value-target)<2e-7 else value


def resolve(ob,newer,optimize=False):
 me=ob.data
 # Intersections in the source weather grid leave sub-micrometer slivers.
 # Dissolve their zero-length/collinear edges before adding chart cuts;
 # deleting their triangles would leave holes. Surface comparison below
 # and the independent source BVH audit bound this cleanup's effect.
 bm=bmesh.new();bm.from_mesh(me)
 bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges))
 bm.to_mesh(me);bm.free();me.update()
 # New roofs have a uniform causal tint, so their source weather sampling
 # grid carries no information. Dissolve only that redundant planar grid.
 # Tired roofs retain every source weather sample.
 tint=np.array([c.color[:] for c in me.color_attributes['Tint'].data])
 uniform=newer and ob.get('component')=='roof' and np.ptp(tint,axis=0).max()<1e-6
 if uniform:
  bm=bmesh.new();bm.from_mesh(me)
  bmesh.ops.dissolve_limit(bm,angle_limit=1e-5,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit={'MATERIAL','UV','NORMAL'})
  bm.to_mesh(me);bm.free();me.update()
 me.calc_loop_triangles();uv=me.uv_layers.active;colors=me.color_attributes['Tint'];normals=[n.vector.copy() for n in me.corner_normals]
 verts=[];faces=[];uvs=[];tints=[];norm=[];materials=[];source_count=len(me.loop_triangles);source_area=sum(t.area for t in me.loop_triangles);seams=0
 for tri in (me.polygons if uniform else me.loop_triangles):
  ids=list(tri.vertices);lis=list(tri.loop_indices if uniform else tri.loops);count=len(ids);tc=[np.array(uv.data[i].uv,dtype='float64') for i in lis]
  roof=me.materials[tri.material_index].name=='RanchRoof'
  if roof:
   tc=[np.array((snap(a[0],1),snap(a[1],1/17))) for a in tc]
  poly=[(tc[i],np.eye(count,dtype='float64')[i]) for i in range(count)]
  pieces=[]
  if roof:
   detail=optimize and (ob.get('component')=='eave_rake_soffit' or (ob.get('component')=='roof' and tri.normal.z<.4))
   # A 24 mm shingle lip or concealed roof gauge cannot display a new
   # randomized packet every 143 mm. Retain metric/style UVs there, with
   # ordinary atlas-wrap cuts only. Full exposed planes keep every phase.
   for row,p in partitions(poly,1,1 if detail else 1/17):
    for roll,p2 in partitions(p,0,1):
     shift=0 if detail else phase(row,roll)
     shifted=[(np.array((snap(a[0]+shift,1),a[1])),w) for a,w in p2]
     for wrap,p3 in partitions(shifted,0,1):
      pieces.append([(np.array((a[0]-wrap,(a[1]-(row if detail else math.floor((row+.5)/17)))*.5+(.5 if newer else 0))),w) for a,w in p3])
   seams+=len(pieces)-1
  else:pieces=[poly]
  for p in pieces:
   # Remove collinear chart-boundary samples after clipping. The map is
   # affine on every source triangle (uniform on dissolved new-roof ngons).
   changed=True
   while changed and len(p)>3:
    changed=False
    for j in range(len(p)):
     a=p[j-1][0];b=p[j][0];c=p[(j+1)%len(p)][0]
     cross=abs((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))
     if cross<1e-12 and np.dot(b-a,c-b)>=0:
      p.pop(j);changed=True;break
   from mathutils.geometry import tessellate_polygon
   points=[sum((me.vertices[ids[k]].co*w[k] for k in range(count)),Vector()) for _,w in p]
   indices={tuple(v):i for i,v in enumerate(points)}
   for triangle in tessellate_polygon([points]):
    ts=[p[v] if isinstance(v,int) else p[indices[tuple(v)]] for v in triangle]
    xyz=[sum((me.vertices[ids[k]].co*w[k] for k in range(count)),Vector()) for _,w in ts]
    if (xyz[1]-xyz[0]).cross(xyz[2]-xyz[0]).length/2<1e-12:continue
    start=len(verts);verts.extend(xyz);faces.append((start,start+1,start+2));materials.append(tri.material_index)
    for tc,w in ts:
     uvs.append(tc);tints.append(tuple(sum(colors.data[ids[k]].color[c]*w[k] for k in range(count)) for c in range(4)))
     norm.append(sum((normals[lis[k]]*w[k] for k in range(count)),Vector()).normalized())
 mesh=bpy.data.meshes.new(me.name+'_DeliveryCharts');mesh.from_pydata(verts,[],faces);mesh.update()
 for mat in me.materials:mesh.materials.append(mat)
 layer=mesh.uv_layers.new(name='UVMap');attr=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
 for i,value in enumerate(uvs):layer.data[i].uv=value
 for i,value in enumerate(tints):attr.data[i].color=value
 for p,mi in zip(mesh.polygons,materials):p.material_index=mi;p.use_smooth=True
 mesh.normals_split_custom_set(norm);ob.data=mesh
 mesh.calc_loop_triangles()
 texcoords=np.array([v.uv[:] for v in mesh.uv_layers.active.data],dtype='float32')
 triangles=np.array([t.loops[:] for t in mesh.loop_triangles]);tc=texcoords[triangles]
 d=tc[:,1]-tc[:,0];e=tc[:,2]-tc[:,0]
 collapsed=np.any(abs(d[:,0]*e[:,1]-d[:,1]*e[:,0])<2e-14)
 if collapsed:
  # Merge coincident chart cuts while retaining per-loop UVs/hard normals.
  # Dissolve float32 collinear slivers into their neighbors and retriangulate;
  # never delete isolated triangles and leave cracks in the envelope.
  stored=mesh.attributes.new('_ChartNormal',type='FLOAT_VECTOR',domain='CORNER')
  stored.data.foreach_set('vector',np.array(norm,dtype='float32').ravel())
  bm=bmesh.new();bm.from_mesh(mesh)
  doubles=bmesh.ops.find_doubles(bm,verts=list(bm.verts),dist=1e-6)['targetmap']
  compatible={a:b for a,b in doubles.items() if max(abs(tints[a.index][k]-tints[b.index][k]) for k in range(4))<1e-6}
  bmesh.ops.weld_verts(bm,targetmap=compatible)
  bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges))
  bmesh.ops.triangulate(bm,faces=list(bm.faces))
  bm.to_mesh(mesh);bm.free();mesh.update()
  saved=[v.vector.normalized() for v in mesh.attributes['_ChartNormal'].data]
  mesh.normals_split_custom_set(saved);mesh.attributes.remove(mesh.attributes['_ChartNormal'])
 mesh.calc_loop_triangles();delivery_area=sum(t.area for t in mesh.loop_triangles)
 error=abs(delivery_area-source_area)/max(source_area,1e-12)
 assert error<1e-4,('Chart conversion changed surface area',ob.name,error)
 return dict(source_triangles=source_count,delivery_triangles=len(mesh.loop_triangles),split_charts=seams,surface_area_relative_error=error)
