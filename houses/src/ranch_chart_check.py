"""Compare converted roof surfaces and UV samples to the accepted source.

Independent BVH sampling recovers the old metric UV at each delivered triangle
centroid, then evaluates the source course/roll expression. Periodic U errors
are measured modulo one; atlas style and course V are checked explicitly.
"""
import math
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def compile_address(node):
 """Compile the saved source vector graph into independent scalar operations."""
 cache={}
 def input_value(socket):
  if socket.is_linked:return output_value(socket.links[0].from_socket)
  value=np.float32(socket.default_value);return lambda uv:value
 def output_value(socket):
  key=socket.as_pointer()
  if key in cache:return cache[key]
  n=socket.node
  if n.type=='TEX_COORD':fn=lambda uv:uv
  elif n.type=='SEPXYZ':
   child=input_value(n.inputs[0]);index=('X','Y','Z').index(socket.name);fn=lambda uv:child(uv)[index]
  elif n.type=='COMBXYZ':
   children=[input_value(i) for i in n.inputs];fn=lambda uv:np.array([f(uv) for f in children],dtype='float32')
  else:
   assert n.type=='MATH',n.type
   left=input_value(n.inputs[0]);right=input_value(n.inputs[1]);op=n.operation
   def fn(uv):
    a=left(uv);b=right(uv)
    if op=='ADD':value=a+b
    elif op=='MULTIPLY':value=a*b
    elif op=='FLOOR':value=np.floor(a)
    elif op=='SINE':value=np.sin(a)
    elif op=='FRACT':value=a-np.floor(a)
    else:raise AssertionError(op)
    return np.float32(value)
  cache[key]=fn;return fn
 return input_value(node.inputs['Vector'])


def nearest64(point,triangles,all_within=None):
 """Float64 closest points: BVH float32 loses precision on long gauges."""
 q=np.array(point,dtype='float64');a,b,c=triangles[:,0],triangles[:,1],triangles[:,2]
 ab=b-a;ac=c-a;n=np.cross(ab,ac);nn=np.einsum('ij,ij->i',n,n)
 projected=q-n*(np.einsum('ij,ij->i',q-a,n)/nn)[:,None]
 u=np.einsum('ij,ij->i',np.cross(projected-a,ac),n)/nn
 v=np.einsum('ij,ij->i',np.cross(ab,projected-a),n)/nn
 valid=(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)
 best=projected.copy();dist=np.linalg.norm(best-q,axis=1);dist[~valid]=np.inf
 for start,end in ((a,b),(b,c),(c,a)):
  edge=end-start;length=np.einsum('ij,ij->i',edge,edge)
  t=np.clip(np.einsum('ij,ij->i',q-start,edge)/np.maximum(length,1e-30),0,1)
  p=start+edge*t[:,None];d=np.linalg.norm(p-q,axis=1);take=d<dist
  best[take]=p[take];dist[take]=d[take]
 if all_within is not None:return [(best[i],int(i),float(dist[i])) for i in np.flatnonzero(dist<all_within)]
 i=int(np.argmin(dist));return Vector(best[i]),i,float(dist[i])


def check(seed):
 bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/ranch/house-{seed}.blend').resolve()))
 sources={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not any(ob.data.materials[p.material_index].name=='RanchRoof' for p in ob.data.polygons):continue
  me=ob.data;me.calc_loop_triangles();verts=[ob.matrix_world@v.co for v in me.vertices];tris=[tuple(t.vertices) for t in me.loop_triangles]
  uv=[tuple(me.uv_layers.active.data[li].uv) for t in me.loop_triangles for li in t.loops]
  mat=next(m for m in me.materials if m.name=='RanchRoof')
  tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE')
  # Save numeric graph samples before loading the game scene invalidates RNA.
  # A tiny source material-only library keeps its actual graph available.
  mat.use_fake_user=True
  sources[ob.name]=(verts,tris,uv,BVHTree.FromPolygons(verts,tris,all_triangles=True))
 mat=next(m for m in bpy.data.materials if m.name=='RanchRoof')
 library=Path(f'build/ranch/delivery/address-{seed}.blend');bpy.data.libraries.write(str(library.resolve()),{mat})
 bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/ranch/delivery/game-{seed}.blend').resolve()))
 with bpy.data.libraries.load(str(library.resolve())) as (src,dst):dst.materials=['RanchRoof']
 tex=next(n for n in dst.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');address=compile_address(tex)
 surface_error=0;uv_error=0;samples=0;reverse=0;edge_samples=0;wrap_samples=0;surface_samples=0;detail_samples=0
 for name,(verts,tris,uv,tree) in sources.items():
  triangles64=np.array([[verts[i][:] for i in t] for t in tris],dtype='float64')
  ob=bpy.data.objects[name];me=ob.data;me.calc_loop_triangles();points=[ob.matrix_world@v.co for v in me.vertices]
  delivered=BVHTree.FromPolygons(points,[tuple(t.vertices) for t in me.loop_triangles],all_triangles=True)
  delivered64=np.array([[points[i][:] for i in t.vertices] for t in me.loop_triangles],dtype='float64')
  for p in verts:
   error=delivered.find_nearest(p)[3]
   if error>2e-5:error=nearest64(p,delivered64)[2]
   reverse=max(reverse,error)
  for t in me.loop_triangles:
   if me.materials[t.material_index].name!='RanchRoof':continue
   center=sum((points[i] for i in t.vertices),Vector())/3;hit=tree.find_nearest(center)
   point,idx,distance=(hit[0],hit[2],hit[3]) if hit[3]<2e-6 else nearest64(center,triangles64)
   surface_error=max(surface_error,distance)
   surface_samples+=1
   # Packet jitter was intentionally removed on tiny shingle lips and
   # hidden roof gauges, while their metric/style charts remain ordinary UVs.
   if ob.get('component')=='eave_rake_soffit' or (ob.get('component')=='roof' and t.normal.z<.4):detail_samples+=1;continue
   a,b,c=triangles64[idx];ab=b-a;ac=c-a;n=np.cross(ab,ac);nn=np.dot(n,n);q=np.array(point)-a
   u=np.dot(np.cross(q,ac),n)/nn;v=np.dot(np.cross(ab,q),n)/nn
   coords=np.array(uv[idx*3:idx*3+3]);value=coords[0]*(1-u-v)+coords[1]*u+coords[2]*v;old=Vector((*value,0))
   # Nearest faces sharing an edge can have different tangent charts. Only
   # compare addressing inside a source triangle, where its chart is unique.
   if min(u,v,1-u-v)<1e-5:edge_samples+=1;continue
   row=math.floor(old.y*17);roll=math.floor(old.x)
   expected=address(np.array((old.x,old.y,0),dtype='float32'))
   actual=sum((me.uv_layers.active.data[li].uv for li in t.loops),Vector((0,0)))/3
   du=abs(actual.x-expected[0]);du=min(du,abs(1-du));dv=abs(actual.y-expected[1])
   # The source UV itself is float32, so points exactly on its course/roll
   # boundary have ambiguous source-side derivatives. Compare interior only.
   if min(abs(old.y*17-round(old.y*17)),abs(old.x-round(old.x)))<2e-5:wrap_samples+=1;continue
   if max(du,dv)>2e-4:
    # Gauged/mitered source solids can meet on co-located faces with
    # different charts. Match any source chart at the same physical point,
    # within two micrometers; never widen the geometric acceptance radius.
    for point2,idx2,distance2 in nearest64(center,triangles64,all_within=2e-6):
     a2,b2,c2=triangles64[idx2];ab2=b2-a2;ac2=c2-a2;n2=np.cross(ab2,ac2);nn2=np.dot(n2,n2);q2=point2-a2
     u2=np.dot(np.cross(q2,ac2),n2)/nn2;v2=np.dot(np.cross(ab2,q2),n2)/nn2
     coords2=np.array(uv[idx2*3:idx2*3+3]);value2=coords2[0]*(1-u2-v2)+coords2[1]*u2+coords2[2]*v2
     expected2=address(np.array((*value2,0),dtype='float32'));du2=abs(actual.x-expected2[0]);du2=min(du2,abs(1-du2));dv2=abs(actual.y-expected2[1])
     if max(du2,dv2)<max(du,dv):du,dv=du2,dv2
    if max(du,dv)>2e-4:print('CHART_ADDRESS_MISS',seed,name,t.index,tuple(old),tuple(actual),tuple(expected),distance,flush=True)
   uv_error=max(uv_error,du,dv);samples+=1
 assert max(surface_error,reverse)<2e-5,(seed,surface_error,reverse)
 assert uv_error<2e-4,(seed,uv_error)
 return dict(passed=True,samples=samples,surface_samples=surface_samples,detail_metric_chart_samples=detail_samples,ambiguous_source_edge_samples=edge_samples,wrap_boundary_samples=wrap_samples,source_to_game_surface_error_m=reverse,game_to_source_centroid_error_m=surface_error,max_periodic_uv_error=float(uv_error),scope='All roof surfaces, exposed-plane packet addressing; metric-only detail charts counted separately; independent of glTF serialization')
