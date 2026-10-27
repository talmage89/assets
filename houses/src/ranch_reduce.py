"""Remove redundant planar samples inside ordinary UV charts.

Chart seams and hard normals remain split. Boundary vertices may disappear
only when collinear. A linear color fit bounds local interpolation changes;
weather comparisons against the accepted export measure the accumulated error.
"""
import bpy,bmesh
import numpy as np
from mathutils import Vector


def reduce(ob,meta,tolerance=.035,passes=12):
 comp=ob.get('component')
 if comp not in ('roof','eave_rake_soffit','ridge') and not (comp=='wall' and ob.get('face') in ('back','left','right')):return None
 me=ob.data;me.calc_loop_triangles();before=len(me.loop_triangles)
 vertices=[];colors=[];coords=[];normals=[];faces=[];materials=[];lookup={};old=me.color_attributes['Tint'];uv=me.uv_layers.active
 for tri in me.loop_triangles:
  face=[]
  for li in tri.loops:
   vi=me.loops[li].vertex_index;p=me.vertices[vi].co;c=old.data[vi].color;tc=uv.data[li].uv;n=me.corner_normals[li].vector
   key=tuple(round(float(x),6) for x in (*p,*tc,*n,*c))
   if key not in lookup:
    lookup[key]=len(vertices);vertices.append(tuple(p));colors.append(tuple(c));coords.append(tuple(tc));normals.append(tuple(n))
   face.append(lookup[key])
  if len(set(face))==3:faces.append(face);materials.append(tri.material_index)
 mesh=bpy.data.meshes.new(me.name+'_Reduced');mesh.from_pydata(vertices,[],faces);mesh.update()
 for mat in me.materials:mesh.materials.append(mat)
 attr=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
 tex=mesh.attributes.new('_MetricUV',type='FLOAT_VECTOR',domain='POINT');normal=mesh.attributes.new('_PlaneNormal',type='FLOAT_VECTOR',domain='POINT')
 for i in range(len(vertices)):
  attr.data[i].color=colors[i];tex.data[i].vector=(*coords[i],0);normal.data[i].vector=normals[i]
 for p,mi in zip(mesh.polygons,materials):p.material_index=mi
 bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update()
 tint=bm.verts.layers.float_color['Tint'];uvlayer=bm.verts.layers.float_vector['_MetricUV'];nlayer=bm.verts.layers.float_vector['_PlaneNormal']
 removed=0;max_residual=0
 for iteration in range(passes):
  bm.normal_update();chosen=[];busy=set()
  for v in list(bm.verts):
   if v in busy or not v.is_valid or (not v.is_manifold and not v.is_boundary):continue
   fs=list(v.link_faces)
   if not fs:continue
   n=fs[0].normal
   if any(len(f.verts)!=3 or f.normal.dot(n)<.999999 or f.material_index!=fs[0].material_index for f in fs):continue
   if comp=='wall' and ((ob.matrix_world@v.co).z<meta['blocks'][0]['floor']+.60 or max(abs(n.x),abs(n.y))<.9):continue
   ring={w for f in fs for w in f.verts if w!=v}
   if len(ring)<2 or len(ring)>12:continue
   if v.is_boundary:
    ends=[e.other_vert(v) for e in v.link_edges if e.is_boundary]
    if len(ends)!=2:continue
    a,b=ends[0].co-v.co,ends[1].co-v.co
    if a.dot(b)>=0 or a.cross(b).length>1e-6*(a.length+b.length):continue
   vertices2=[v]+sorted(ring,key=lambda w:tuple(w.co))
   if max(abs((w.co-v.co).dot(n)) for w in ring)>1e-6:continue
   axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis]
   points=np.array([[1.,w.co[axes[0]]-v.co[axes[0]],w.co[axes[1]]-v.co[axes[1]]] for w in vertices2])
   values=np.array([tuple(w[tint]) for w in vertices2]);texcoords=np.array([tuple(w[uvlayer]) for w in vertices2])
   residual=float(abs(points@np.linalg.lstsq(points,values,rcond=None)[0]-values).max())
   if residual>tolerance/2:continue
   if float(abs(points@np.linalg.lstsq(points,texcoords,rcond=None)[0]-texcoords).max())>1e-6:continue
   chosen.append(v);busy.update(vertices2);max_residual=max(max_residual,residual)
  if not chosen:break
  bmesh.ops.dissolve_verts(bm,verts=chosen,use_face_split=False,use_boundary_tear=False)
  bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3],ngon_method='EAR_CLIP')
  removed+=len(chosen)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 bmesh.ops.triangulate(bm,faces=list(bm.faces))
 bm.to_mesh(mesh);bm.free();mesh.update()
 layer=mesh.uv_layers.new(name='UVMap');ns=[]
 for loop in mesh.loops:
  layer.data[loop.index].uv=mesh.attributes['_MetricUV'].data[loop.vertex_index].vector[:2]
  ns.append(mesh.attributes['_PlaneNormal'].data[loop.vertex_index].vector.normalized())
 for p in mesh.polygons:p.use_smooth=True
 mesh.normals_split_custom_set(ns)
 for name in ('_MetricUV','_PlaneNormal'):mesh.attributes.remove(mesh.attributes[name])
 ob.data=mesh;mesh.calc_loop_triangles()
 return dict(before=before,after=len(mesh.loop_triangles),removed_weather_vertices=removed,max_local_affine_residual=max_residual,tolerance=tolerance,passes=passes)
