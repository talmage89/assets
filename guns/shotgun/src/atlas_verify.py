"""Independent atlas/animation audit, including real imported construction.

Reconstruct named diagnostic parts from actual imported delivery triangles by
rest centroid, rigid owner and vertex agreement. This adds no delivery nodes:
the shipped gun remains one mesh/material. Contacts and clearance then run on
those imported surfaces, separately from affine serialization comparisons.
"""
import sys,json,hashlib,io
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from PIL import Image
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))
from kit import weapon as W,weapon_verify as V,uv,motion
from kit.gltf import GLB
from kit import detachable_verify as DV
from semantics import check
from contacts import measure
from check import geometry,sweep
from interface import CLIPS

def named_reference(arm):
 W.pose(arm,None,0);records=[];templates={};trees={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.parent!=arm or 'bone' not in ob or ob.get('bake_only'):continue
  templates[ob.name]=ob['bone'];ob.data.calc_loop_triangles()
  for face in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
   records.append((ob.name,ob['bone'],points))
 for bone in set(templates.values()):
  selected=[(i,r) for i,r in enumerate(records) if r[1]==bone];tree=KDTree(len(selected))
  for i,row in selected:tree.insert(sum(row[2],Vector())/3,i)
  tree.balance();trees[bone]=tree
 return records,templates,trees

def restore_diagnostics(arm,reference):
 records,templates,trees=reference;W.pose(arm,None,0);mapped={name:[] for name in templates};seen=set();maximum=0.
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
  ob.data.calc_loop_triangles();normals=ob.data.corner_normals
  for triangle in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in triangle.vertices]
   owners=[]
   for i in triangle.vertices:
    group=max(ob.data.vertices[i].groups,key=lambda g:g.weight);owners.append(ob.vertex_groups[group.group].name)
   assert len(set(owners))==1,owners
   bone=owners[0];center=sum(points,Vector())/3
   _,index,distance=trees[bone].find(center);name,_,expected=records[index]
   assert distance<2e-7,(name,distance)
   error=max(min((p-q).length for q in expected) for p in points)
   assert error<2e-7,(name,error);maximum=max(maximum,error)
   assert index not in seen,(name,'duplicate imported triangle');seen.add(index)
   mapped[name].append((points,[ob.matrix_world.to_3x3()@normals[i].vector for i in triangle.loops]))
  bpy.data.objects.remove(ob,do_unlink=True)
 assert len(seen)==len(records),(len(seen),len(records))
 for name,faces in mapped.items():
  vertices=[tuple(p) for points,n in faces for p in points]
  mesh=bpy.data.meshes.new('Imported diagnostic '+name)
  mesh.from_pydata(vertices,[],[(i*3,i*3+1,i*3+2) for i in range(len(faces))]);mesh.update()
  mesh.normals_split_custom_set([tuple(n) for points,normals in faces for n in normals])
  ob=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(ob)
  ob['part_name']=name;ob['asset_set']='Shotgun';W.rigid_bind(ob,arm,templates[name])
 return dict(parts=len(mapped),triangles=len(seen),maximum_vertex_delta_m=maximum,
  scope='actual imported triangles, rigid-owner/centroid and all vertex positions matched one-to-one')

def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'));arm=bpy.data.objects['ShotgunArmature']
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
 u=uv.report(objects,size=2048)
 assert not u['outside_triangles'] and not u['degenerate_uv_triangles']
 assert u['overlap_fraction']<1e-5,u['overlap_fraction']
 assert 1200<u['density_px_m']['50']<5000,u['density_px_m']
 source_states=check(arm);reference=named_reference(arm)
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 expected=V.capture(arm,samples,sockets)
 # Check actual posed source/export surfaces independently at events/endpoints.
 surfaces={};meshes=[o for o in objects if o.parent==arm and 'bone' in o]
 for c,s in CLIPS.items():
  for frame in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,c,frame);surfaces[(c,frame)]=V.surface_points(meshes)
 b=json.loads((BASE/'build/baked/4k/bake-report.json').read_text())
 assert b['size']==4096 and b['samples']>=32
 for channel in ('BaseColor','Roughness','Metallic','AO','MaterialAO','Normal'):
  assert b[channel]['alpha_missed_interior_texels']==0,(channel,b[channel])
 records={}
 for name,limit in [('shotgun',40000),('shell',600),('hull',400)]:
  path=BASE/'export'/(name+'.glb');g=GLB(path)
  tri=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
  assert tri<=limit and len(g.json['materials'])==1 and len(g.json['images'])==3
  assert len(g.json['meshes'])==1
  for mesh in g.json['meshes']:
   for primitive in mesh['primitives']:
    normal=g.accessor(primitive['attributes']['NORMAL'])
    assert np.isfinite(normal).all() and np.max(np.abs(np.linalg.norm(normal,axis=1)-1))<1e-5
  hashes=sorted(hashlib.sha256(g.image(i)).hexdigest() for i in range(3))
  canonical=sorted(hashlib.sha256((BASE/'textures'/('T_Hearth12_'+channel+'.png')).read_bytes()).hexdigest()
                   for channel in ('BaseColor','Normal','ORM'))
  if name=='shotgun':
   assert hashes==canonical,'Gun images differ from current canonical delivery textures'
   subset=None;map_size=2048
  else:
   subset=DV.audit(path,BASE/'textures','Hearth12',BASE/'build/delivery/detachables'/name/'layout.json')
   map_size=subset['size'];assert map_size=={'shell': 1024, 'hull': 512}[name]
  for i in range(3):assert Image.open(io.BytesIO(g.image(i))).size==(map_size,map_size)
  if name=='shotgun':
   assert set(a['name'] for a in g.json['animations'])==set(CLIPS)
   for mesh in g.json['meshes']:
    for p in mesh['primitives']:
     weights=g.accessor(p['attributes']['WEIGHTS_0'])
     assert np.max(np.abs(weights.sum(axis=1)-1))<1e-6
     assert np.all(np.sum(weights>1e-6,axis=1)==1)
  else:assert not g.json.get('skins') and not g.json.get('animations')
  records[name]=dict(triangles=tri,bytes=path.stat().st_size,materials=1,images=3,image_size=map_size,
   image_sha256=hashes,normal_direction=V.normal_direction(g))
  if subset is not None:records[name]['standalone_textures']=subset
  if name!='shotgun':
   alignment=[]
   for mesh in g.json['meshes']:
    for primitive in mesh['primitives']:
     xyz=g.accessor(primitive['attributes']['POSITION']);normal=g.accessor(primitive['attributes']['NORMAL'])
     radius=np.linalg.norm(xyz[:,:2],axis=1)
     # Exact hull base radius excludes brass/head vertices and the folded end.
     selected=(abs(radius-.01005)<2e-7)&(abs(xyz[:,2])>.0104)&(abs(xyz[:,2])<.011)
     alignment.extend(np.sum(normal[selected,:2]*xyz[selected,:2]/radius[selected,None],axis=1).tolist())
   assert alignment and min(alignment)>.9999,(name,'exterior hull normals',alignment)
   records[name]['minimum_outer_hull_radial_normal_alignment']=min(alignment)
 arm=V.import_glb(BASE/'export/shotgun.glb');imported_states=check(arm)
 imported_uv=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH'],size=2048)
 assert not imported_uv['outside_triangles'] and not imported_uv['degenerate_uv_triangles']
 assert imported_uv['overlap_fraction']<1e-5
 affine=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];surface_rows=[]
 for (c,frame),points in surfaces.items():
  W.pose(arm,c,frame);error=V.surface_delta(points,V.surface_points(meshes));assert error<2e-6,(c,frame,error)
  surface_rows.append(dict(clip=c,frame=frame,delta_m=error))
 diagnostic=restore_diagnostics(arm,reference)
 imported_contacts=measure(arm);imported_geometry=geometry(arm);imported_motion=sweep(arm)
 assert imported_motion['passed']
 for name,length in [('shell',.0575),('hull',.0698)]:
  V.import_glb(BASE/'export'/(name+'.glb'));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
  points=np.array(V.surface_points(meshes));lo=points.min(axis=0);hi=points.max(axis=0);size=hi-lo
  assert np.max(np.abs(size-np.array((.0224,length,.0224))))<.0001
  assert abs(lo[1])<1e-6
  records[name]['fresh_import_dimensions_m']=size.tolist()
 result=dict(passed=True,scope='final baked delivery; serialization and independent imported surface construction',
  outputs=records,uv={k:u[k] for k in ('coverage','overlap_pairs','overlap_fraction','degenerate_uv_triangles','outside_triangles','density_px_m')},
  imported_gun_uv={k:imported_uv[k] for k in ('coverage','overlap_pairs','overlap_fraction','degenerate_uv_triangles','outside_triangles','density_px_m')},
  bake_size=b['size'],bake_samples=b['samples'],missed_interior_texels=0,gpu_memory_mib_bc_with_mips=16,
  source_states=source_states,imported_states=imported_states,affine_samples=len(affine),
  maximum_position_delta_m=max(r['position_delta_m'] for r in affine),maximum_linear_delta=max(r['linear_delta'] for r in affine),
  posed_surfaces=surface_rows,imported_diagnostic_reconstruction=diagnostic,
  imported_contacts=imported_contacts,imported_geometry=imported_geometry,imported_motion=imported_motion)
 (BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2))
 print('HEARTH ATLAS VERIFIED',len(affine),'affine/state samples; imported contacts and clearance; canonical gun atlas and two standalone texture sets',flush=True)
if __name__=='__main__':main()
