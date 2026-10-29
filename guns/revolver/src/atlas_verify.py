"""Canonical atlas, states, posed surfaces and actual imported-part audit.

Every imported triangle is matched by rigid owner, centroid and all vertices;
reconstructed diagnostic parts are evidence from the delivery, not a source copy.
"""
import sys,json,hashlib,io
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from PIL import Image
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V,uv
from kit.gltf import GLB
from kit import detachable_verify as DV
from interface import CLIPS
from semantics import check
def named_reference(arm):
 W.pose(arm,None,0);records=[];templates={};trees={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.parent!=arm or 'bone' not in ob or ob.get('bake_only'):continue
  templates[ob.name]=dict(bone=ob['bone'],allow_boundary=ob.get('allow_boundary',False));ob.data.calc_loop_triangles()
  for face in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
   records.append((ob.name,ob['bone'],points))
 for bone in {r['bone'] for r in templates.values()}:
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
  ob['part_name']=name;ob['asset_set']='Revolver';ob['allow_boundary']=templates[name]['allow_boundary']
  # Restore indexed vertices for the independent manifold-solid audit. Corner
  # normals remain face-corner data, including discontinuous hard edges.
  attr=mesh.attributes.new('SavedNormal','FLOAT_VECTOR','CORNER')
  attr.data.foreach_set('vector',[a for r in mesh.corner_normals for a in r.vector])
  bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bm.to_mesh(mesh);bm.free()
  mesh.normals_split_custom_set([r.vector[:] for r in mesh.attributes['SavedNormal'].data]);mesh.attributes.remove(mesh.attributes['SavedNormal'])
  W.rigid_bind(ob,arm,templates[name]['bone'])
 return dict(parts=len(mapped),triangles=len(seen),maximum_vertex_delta_m=maximum,
  scope='actual imported triangles, rigid-owner/centroid and all vertex positions matched one-to-one')


def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 arm=bpy.data.objects['RevolverArmature']
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
 u=uv.report(objects,size=2048)
 assert not u['outside_triangles'] and not u['degenerate_uv_triangles'] and u['overlap_fraction']<1e-5
 assert 2000<u['density_px_m']['50']<6500
 source_states=check(arm);reference=named_reference(arm)
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 expected=V.capture(arm,samples,[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')])
 surfaces={}
 for c,s in CLIPS.items():
  for frame in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,c,frame);surfaces[(c,frame)]=V.surface_points(objects)
 spawns={}
 for name,bone,owners,clip,frame in [
  ('cartridge','Live0',['Live0'],'Idle',0),
  ('case','Case0',['Case0'],'IdleAfter6',0),
  ('speedloader_loaded','LoaderGuide',['LoaderBody','LoaderRelease',*['LoaderRound'+str(i) for i in range(6)]],'Reload',142)]:
  W.pose(arm,clip,frame)
  spawns[name]=(V.surface_points([o for o in objects if o['bone'] in owners]),arm.matrix_world@arm.pose.bones[bone].matrix)
 b=json.loads((BASE/'build/baked/4k/bake-report.json').read_text())
 assert b['size']==4096 and b['samples']>=32
 for channel in ('BaseColor','Roughness','Metallic','AO','MaterialAO','Normal'):
  assert b[channel]['alpha_missed_interior_texels']==0,(channel,b[channel])
 canonical=sorted(hashlib.sha256((BASE/'textures'/('T_MeridianSix_'+c+'.png')).read_bytes()).hexdigest() for c in ('BaseColor','Normal','ORM'))
 records={}
 for name,limit in [('revolver',40000),('cartridge',600),('case',500),('speedloader_loaded',5500)]:
  path=BASE/'export'/(name+'.glb');g=GLB(path)
  triangles=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
  assert triangles<=limit and len(g.json['materials'])==1 and len(g.json['images'])==3
  hashes=sorted(hashlib.sha256(g.image(i)).hexdigest() for i in range(3))
  if name=='revolver':
   assert hashes==canonical
   subset=None;map_size=2048
  else:
   subset=DV.audit(path,BASE/'textures','MeridianSix',BASE/'build/delivery/detachables'/name/'layout.json',gun=BASE/'export/revolver.glb')
   subset['mip_bleed']=DV.mip_bleed(path,BASE/'textures','MeridianSix',BASE/'build/delivery/detachables'/name/'layout.json',gun=BASE/'export/revolver.glb')
   map_size=subset['size'];assert map_size=={'cartridge': 512, 'case': 512, 'speedloader_loaded': 1024}[name]
  for i in range(3):assert Image.open(io.BytesIO(g.image(i))).size==(map_size,map_size)
  if name=='revolver':
   assert {a['name'] for a in g.json['animations']}==set(CLIPS)
   for animation in g.json['animations']:
    times=[g.accessor(s['input']).reshape(-1) for s in animation['samplers']]
    lo=min(float(t.min()) for t in times);hi=max(float(t.max()) for t in times)
    assert abs(lo)<1e-7 and abs(hi-CLIPS[animation['name']]['frames']/60)<3e-7
   assert len(g.json['skins'])==1
  else:assert not g.json.get('animations') and not g.json.get('skins')
  records[name]=dict(triangles=triangles,bytes=path.stat().st_size,materials=1,images=3,image_size=map_size,image_sha256=hashes,normal_direction=V.normal_direction(g))
  if subset is not None:records[name]['standalone_textures']=subset
 arm=V.import_glb(BASE/'export/revolver.glb');imported_states=check(arm)
 imported_uv=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH'],size=2048)
 assert not imported_uv['outside_triangles'] and not imported_uv['degenerate_uv_triangles'] and imported_uv['overlap_fraction']<1e-5
 affine=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];surface_rows=[]
 for (c,frame),points in surfaces.items():
  W.pose(arm,c,frame);error=V.surface_delta(points,V.surface_points(meshes));assert error<2e-6,(c,frame,error)
  surface_rows.append(dict(clip=c,frame=frame,delta_m=error))
 diagnostic=restore_diagnostics(arm,reference)
 bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/imported-parts.blend'))
 for name in ('cartridge','case','speedloader_loaded'):
  V.import_glb(BASE/'export'/(name+'.glb'));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
  points=V.surface_points(meshes);lo=np.min(points,axis=0);hi=np.max(points,axis=0)
  records[name]['fresh_import_dimensions_m']=(hi-lo).tolist()
  target,spawn=spawns[name]
  error=V.surface_delta(target,[tuple(spawn@Vector(v)) for v in points]);assert error<2e-6,(name,error)
  records[name]['posed_spawn_delta_m']=error
  if name=='cartridge':assert abs((hi-lo)[1]-.04020)<3e-5
  if name=='case':assert abs((hi-lo)[1]-.03280)<5e-5
 keys=('coverage','outside_triangles','degenerate_uv_triangles','overlap_pairs','overlap_fraction','density_px_m')
 result=dict(passed=True,outputs=records,uv={k:u[k] for k in keys},imported_uv={k:imported_uv[k] for k in keys},
  source_states=source_states,imported_states=imported_states,
  bake_size=b['size'],bake_samples=b['samples'],missed_interior_texels=0,
  affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),
  maximum_linear_delta=max(r['linear_delta'] for r in affine),posed_surfaces=surface_rows,
  imported_diagnostic_reconstruction=diagnostic,gpu_memory_mib_bc_with_mips=16)
 (BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2))
 print('MERIDIAN ATLAS VERIFIED',len(affine),'poses;',diagnostic)
if __name__=='__main__':main()
