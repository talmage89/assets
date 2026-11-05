"""Resample the quarter roll in physical shoulder-aligned coordinates.

Keep every patch boundary vertex and edge. Replace only interior chords with
regular rows sampled on our accepted evaluated parent. This resolves reflected
normal interpolation with fewer triangles. High retains the dense original.
"""
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from hatch_reference_surface import field


def apply(b):
 if b.high:return
 for name in ['Rear quarter_L','Rear quarter_R']:
  ob=bpy.data.objects[name];me=ob.data;sign=-1 if name.endswith('L') else 1
  old=me.attributes.new('held normals','FLOAT_VECTOR','CORNER')
  for row,n in zip(old.data,me.corner_normals):row.vector=n.vector
  bm=bmesh.new();bm.from_mesh(me);role=bm.faces.layers.int['hatch_outer_skin'];before=len(bm.faces);bm.verts.index_update()
  selected=[]
  for f in bm.faces:
   p=ob.matrix_world@f.calc_center_median();t=p.z-(.891+.012*p.y)
   if f[role] and abs(p.x)>.83 and 1.10<p.y<1.91 and abs(t)<.033:selected.append(f)
  region=set(selected);boundary=[e for f in selected for e in f.edges if sum(q in region for q in e.link_faces)==1];boundary=list(dict.fromkeys(boundary));verts=sorted({v for e in boundary for v in e.verts},key=lambda v:v.index);lookup={v:i for i,v in enumerate(verts)}
  ps=[ob.matrix_world@v.co for v in verts];uv=[Vector((p.y,p.z-(.891+.012*p.y))) for p in ps];edges=[tuple(lookup[v] for v in e.verts) for e in boundary]
  def inside(q):
   n=0
   for a,c in edges:
    a,c=uv[a],uv[c]
    if (a.y>q.y)!=(c.y>q.y) and q.x<(c.x-a.x)*(q.y-a.y)/(c.y-a.y)+a.x:n+=1
   return n%2==1
  def distance(q):
   ds=[]
   for a,c in edges:
    a,c=uv[a],uv[c];d=c-a;t=max(0,min(1,(q-a).dot(d)/d.length_squared));ds.append((q-a-d*t).length)
   return min(ds)
  for i in range(40):
   y=1.10+i*.021
   for t in [-.030,-.022,-.014,-.007,0,.007,.014,.022,.030]:
    q=Vector((y,t))
    if inside(q) and distance(q)>.002:uv.append(q)
  coords,_,faces,original,*_=delaunay_2d_cdt(uv,edges,[],0,1e-8)
  faces=[f for f in faces if inside(sum((coords[i] for i in f),Vector((0,0)))/len(f))]
  material=selected[0].material_index;needed={i for f in faces for i in f};newverts={}
  for i in sorted(needed):
   oldids=[j for j in original[i] if j<len(verts)]
   if oldids:
    if len(oldids)>1:raise ValueError('Merged held boundary')
    newverts[i]=verts[oldids[0]]
   else:
    y,t=coords[i];z=.891+.012*y+t;hit=field()((sign*2,y,z),(-sign,0,0))
    if hit is None:raise ValueError('Patch ray miss')
    newverts[i]=bm.verts.new(ob.matrix_world.inverted()@hit[0])
  bmesh.ops.delete(bm,geom=selected,context='FACES_ONLY')
  for f in faces:
   vs=[newverts[i] for i in f];ps=[ob.matrix_world@v.co for v in vs];n=(ps[1]-ps[0]).cross(ps[2]-ps[0]);p=sum(ps,Vector())/3
   if n.dot(field().nearest_normal(p))<0:vs.reverse()
   nf=bm.faces.new(vs);nf[role]=1;nf.smooth=True;nf.material_index=material
  bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
  bm.normal_update();
  for edge in boundary:
   if not edge.is_valid or len(edge.link_faces)!=2:raise ValueError('Shoulder patch did not retain a conforming boundary')
  ob['shoulder_patch_held_boundary_vertices']=len(verts);ob['shoulder_patch_removed_faces']=len(selected);ob['shoulder_patch_new_faces']=len(faces);print('H120_SHOULDER_PATCH',name,'old selected',len(selected),'new',len(faces),'before',before,'after',len(bm.faces),flush=True);bm.to_mesh(me);bm.free()
  old=me.attributes['held normals'];role=me.attributes['hatch_outer_skin'];nm=ob.matrix_world.to_3x3().transposed();normals=[]
  for f in me.polygons:
   for li in f.loop_indices:
    p=ob.matrix_world@me.vertices[me.loops[li].vertex_index].co
    normals.append(nm@field().nearest_normal(p) if role.data[f.index].value else old.data[li].vector.copy())
  me.normals_split_custom_set(normals);me.attributes.remove(old)
