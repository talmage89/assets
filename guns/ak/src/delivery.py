"""Attribute actual imported triangles to named source parts for visual audit.

This does not substitute source surfaces for the import. Every imported vertex,
corner normal, UV and material is retained. A one-to-one rigid-owner/centroid
match independently bounds the attribution error before contact checks run.
"""
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.kdtree import KDTree
from kit import weapon as W

def references(path):
 with bpy.data.libraries.load(str(path),link=False) as (src,dst):
  dst.objects=[name for name in src.objects if name not in ('Case_Proof','Cartridge_Proof') and not name.startswith('HIGH_')]
 records=[];templates={};trees={}
 for ob in dst.objects:
  if ob.type!='MESH' or not ob.get('bone') or not ob.get('asset_set'):continue
  name=ob.get('part_name',ob.name.split('.')[0]);templates[name]=dict(bone=ob['bone'])
  ob.data.calc_loop_triangles()
  for tri in ob.data.loop_triangles:
   records.append((name,ob['bone'],[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]))
 for bone in {r['bone'] for r in templates.values()}:
  selected=[(i,r) for i,r in enumerate(records) if r[1]==bone];tree=KDTree(len(selected))
  for i,row in selected:tree.insert(sum(row[2],Vector())/3,i)
  tree.balance();trees[bone]=tree
 for ob in dst.objects:bpy.data.objects.remove(ob,do_unlink=True)
 return records,templates,trees

def split_imported(scene,source):
 arm=next(o for o in scene.objects if o.type=='ARMATURE');W.pose(arm,None,0)
 reference=references(source);records,templates,trees=reference
 mapped={name:[] for name in templates};seen=set();maximum=0
 for ob in [o for o in scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]:
  ob.data.calc_loop_triangles();normals=ob.data.corner_normals;layer=ob.data.uv_layers.active
  for tri in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
   owners=[ob.vertex_groups[max(ob.data.vertices[i].groups,key=lambda g:g.weight).group].name for i in tri.vertices]
   assert len(set(owners))==1
   _,index,distance=trees[owners[0]].find(sum(points,Vector())/3);name,_,expected=records[index]
   error=max(min((p-q).length for q in expected) for p in points)
   assert distance<2e-7 and error<2e-7,(name,distance,error)
   assert index not in seen;seen.add(index);maximum=max(maximum,error)
   mapped[name].append((points,[ob.matrix_world.to_3x3()@normals[i].vector for i in tri.loops],[layer.data[i].uv.copy() for i in tri.loops],ob.data.materials[ob.data.polygons[tri.polygon_index].material_index]))
  bpy.data.objects.remove(ob,do_unlink=True)
 assert len(seen)==len(records),(len(seen),len(records))
 for name,faces in mapped.items():
  mesh=bpy.data.meshes.new('Imported '+name);mesh.from_pydata([p for ps,*_ in faces for p in ps],[],[(3*i,3*i+1,3*i+2) for i in range(len(faces))]);mesh.update()
  # glTF's imported Normal Map node names UVMap explicitly. Preserve that
  # name so its tangent basis remains valid after diagnostic separation.
  mesh.normals_split_custom_set([n for _,ns,*_ in faces for n in ns]);uv=mesh.uv_layers.new(name='UVMap')
  for row,coord in zip(uv.data,[c for _,_,coords,_ in faces for c in coords]):row.uv=coord
  mats=list(dict.fromkeys(r[3] for r in faces))
  for m in mats:mesh.materials.append(m)
  for f,row in zip(mesh.polygons,faces):f.material_index=mats.index(row[3]);f.use_smooth=True
  attr=mesh.attributes.new('SavedNormal','FLOAT_VECTOR','CORNER');attr.data.foreach_set('vector',[a for r in mesh.corner_normals for a in r.vector])
  bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bm.to_mesh(mesh);bm.free()
  mesh.normals_split_custom_set([r.vector[:] for r in mesh.attributes['SavedNormal'].data]);mesh.attributes.remove(mesh.attributes['SavedNormal'])
  ob=bpy.data.objects.new(name,mesh);scene.collection.objects.link(ob);ob['part_name']=name;ob['asset_set']='R39';W.rigid_bind(ob,arm,templates[name]['bone'])
 return dict(parts=len(mapped),triangles=len(seen),maximum_vertex_delta_m=maximum,scope='actual imported triangles with original UVs/normals/materials; matched one-to-one to source names')
