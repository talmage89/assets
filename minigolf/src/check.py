"""Independent checkpoint gates: raw glTF, fresh surfaces, sockets and motion.

Does not claim final UV/texture bake certification. Swatch UV reuse is intended.
"""
import hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kit.gltf import GLB
from kit.motion import surface,penetration
from plan import generate
from plan_check import validate
from preserve import check as preserve

class External(GLB):
 def __init__(self,path):
  self.json=json.loads(path.read_text());self.binary=(path.parent/self.json['buffers'][0]['uri']).read_bytes();self.parents={c:i for i,n in enumerate(self.json['nodes']) for c in n.get('children',[])}

def tree(obs):
 vs=[];fs=[]
 for ob in obs:
  ob.data.calc_loop_triangles();offset=len(vs);vs.extend(ob.matrix_world@v.co for v in ob.data.vertices);fs.extend(tuple(offset+k for k in t.vertices) for t in ob.data.loop_triangles)
 return BVHTree.FromPolygons(vs,fs,all_triangles=True)

def check():
 rows=[];used_images={}
 for seed in (71,92):
  path=Path(f'export/Minigolf-{seed}.gltf');g=External(path);meta=json.loads(path.with_suffix('.json').read_text());counts=0
  for mesh in g.json['meshes']:
   for prim in mesh['primitives']:
    indices=g.accessor(prim['indices']).ravel();positions=g.accessor(prim['attributes']['POSITION']);normals=g.accessor(prim['attributes']['NORMAL']);uv=g.accessor(prim['attributes']['TEXCOORD_0']);counts+=len(indices)//3
    assert np.all(np.isfinite(positions)) and np.all(np.isfinite(uv))
    assert np.max(np.abs(np.linalg.norm(normals,axis=1)-1))<1e-4
    faces=positions[indices.reshape(-1,3)];areas=np.linalg.norm(np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]),axis=1)/2
    assert np.min(areas)>1e-12,('Degenerate triangles',seed,np.min(areas))
  assert counts==meta['triangles']
  assert all(2000<=v<=8000 for v in meta['holes'].values()),meta['holes']
  assert all(v<=15000 for v in meta['fixtures'].values())
  assert meta['materials']<=10
  for im in g.json['images']:
   f=(path.parent/im['uri']).resolve();assert f.is_file();digest=hashlib.sha256(f.read_bytes()).hexdigest();assert str(f) not in used_images or used_images[str(f)]==digest;used_images[str(f)]=digest
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
  hole_roots=[o for o in bpy.context.scene.objects if o.get('module_kind')=='hole'];assert len(hole_roots)==18
  cup_measure=[]
  for rt in hole_roots:
   sockets={o.get('socket_kind'):o for o in rt.children if o.get('socket_kind') in ('cup','tee')};assert set(sockets)=={'cup','tee'}
   q=sockets['cup'].matrix_world.translation;h=meta['plan']['holes'][rt['hole_number']-1]
   assert (q-Vector(h['cup'])).length<.00002,('Cup serialization',rt.name)
   assert (sockets['tee'].matrix_world.translation-Vector(h['tee'])).length<.00002,('Tee serialization',rt.name)
   obs=[o for o in rt.children if o.type=='MESH'];bvh=tree(obs)
   # Down rays test a real opening and adjacent supported carpet. Rim samples
   # lie outside aluminum, not on a symbolic constant-radius disk.
   hit=bvh.ray_cast(q+Vector((.021,0,.10)),Vector((0,0,-1)),1)
   assert hit[0] is not None and q.z-hit[0].z>.085,('Cup blocked',rt.name,q,hit)
   lip=[]
   for a in range(8):
    v=q+Vector((.063*math.cos(a*math.tau/8),.063*math.sin(a*math.tau/8),.10));r=bvh.ray_cast(v,Vector((0,0,-1)),1);assert r[0] is not None
    lip.append(r[0].z-q.z)
   assert max(abs(v) for v in lip)<.006,('Carpet-to-cup discontinuity',rt.name,lip)
   # Geometry-based horizontal aperture measurement from inside the cup.
   spans=[]
   for d in (Vector((1,0,0)),Vector((0,1,0))):
    origin=q-Vector((0,0,.04));a=bvh.ray_cast(origin,d,.20);b=bvh.ray_cast(origin,-d,.20);assert a[0] is not None and b[0] is not None;spans.append((a[0]-b[0]).length)
   assert max(abs(s-.10795) for s in spans)<.001,spans
   aperture_recess=[]
   for i in range(24):
    a=i*math.tau/24;v=q+Vector((.049*math.cos(a),.049*math.sin(a),.10));r=bvh.ray_cast(v,Vector((0,0,-1)),1);assert r[0] is not None;depth=q.z-r[0].z;assert depth>.085,('Carpet occludes cup aperture',rt.name,i,depth);aperture_recess.append(depth)
   cup_measure.append(dict(aperture_minimum_recess_m=min(aperture_recess),hole=rt.name,opening_xy_m=spans,center_recess_m=q.z-hit[0].z,lip_offsets_m=lip))
  motion=[]
  for rotor in [o for o in bpy.context.scene.objects if o.get('module_kind')=='moving rotor']:
   # Swept vertices against actual fixed fixture BVH; shaft/hub intended bearing
   # removed from the obstruction set by using the axial separation certificate.
   body=[o for o in rotor.parent.children if o.type=='MESH'];moving=[o for o in rotor.children_recursive if o.type=='MESH'];inv=rotor.parent.matrix_world.inverted()
   # Real bored hub leaves the 35 mm shaft inside a 37.5 mm bore.
   # Kit collision measures all fixed/moving triangle surfaces at each pose.
   fixed=[surface(o) for o in body];floor=tree([o for o in rotor.parent.parent.children if o.type=='MESH']);minimum_floor_gap=1e9;low=1e9;maximum_penetration=0.0;matrix=rotor.rotation_euler.copy()
   for deg in range(0,361,5):
    rotor.rotation_euler.y=math.radians(deg);bpy.context.view_layer.update()
    worldpoints=[o.matrix_world@v.co for o in moving for v in o.data.vertices];lowest=min(worldpoints,key=lambda q:q.z);low=min(low,(inv@lowest).z)
    hit=floor.ray_cast(lowest+Vector((0,0,.5)),Vector((0,0,-1)),2)
    if hit[0] is not None:minimum_floor_gap=min(minimum_floor_gap,lowest.z-hit[0].z)
    for ob in moving:
     current=surface(ob)
     for other in fixed:
      depth,_=penetration(current,other,.00025);maximum_penetration=max(maximum_penetration,depth)
   rotor.rotation_euler=matrix;bpy.context.view_layer.update()
   assert low>=.002,low
   assert minimum_floor_gap>.001,minimum_floor_gap
   assert maximum_penetration<.00025,('Rotor collision',maximum_penetration)
   motion.append(dict(node=rotor.name,sample_step_degrees=5,minimum_swept_height_in_fixture_m=low,maximum_fixed_surface_penetration_m=maximum_penetration,minimum_sampled_carpet_gap_m=minimum_floor_gap,scope='kit.motion surface/solid-parity measurement; bored hub and fixed shaft included; sampled, not a continuous guarantee'))
  for node in [o for o in bpy.context.scene.objects if o.get('slide_axis') or ('Clubhouse__Door' in o.name and o.type=='EMPTY')]:
   moving=[o for o in node.children_recursive if o.type=='MESH'];fixed=[surface(o) for o in node.parent.children if o.type=='MESH'];slide=node.get('slide_axis');rot=node.rotation_euler.copy();loc=node.location.copy();depthmax=0.0
   for step in range(21):
    if slide:node.location['XYZ'.index(slide)]=loc['XYZ'.index(slide)]+float(node['range_m'][1])*step/20
    else:node.rotation_euler.z=math.radians(node['range_degrees'][0]*step/20)
    bpy.context.view_layer.update()
    for ob in moving:
     current=surface(ob)
     for other in fixed:
      depth,_=penetration(current,other,.00025);depthmax=max(depthmax,depth)
   node.rotation_euler=rot;node.location=loc;bpy.context.view_layer.update()
   assert depthmax<.00025,('Moving leaf collision',node.name,depthmax)
   motion.append(dict(node=node.name,maximum_fixed_surface_penetration_m=depthmax,samples=21,kind='translation' if slide else 'hinged leaf'))
  # Site swatches retain precise semantic cells, so the actual imported
  # asphalt and stall polygons can be measured after static consolidation.
  import geometry as F
  site=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='site');site_meshes=[o for o in site.children if o.type=='MESH']
  def palette_vertices(key):
   from textures import RECTS
   u0,v0,u1,v1=RECTS[key];points=[]
   for ob in site_meshes:
    uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
     mat=ob.data.materials[poly.material_index].name
     direct=mat.startswith(key.capitalize()) or mat.startswith('Quick_'+key)
     tiled=mat.startswith('Minigolf') and all(u0<uv.data[li].uv.x<u1 and v0<uv.data[li].uv.y<v1 for li in poly.loop_indices)
     if direct or tiled:points.extend(ob.matrix_world@ob.data.vertices[k].co for k in poly.vertices)
   return points
  asphalt=palette_vertices('asphalt');stripes=palette_vertices('white');assert asphalt and stripes
  front=min(q.y for q in asphalt);aisle=min(q.y for q in stripes)-front;stall_depth=max(q.y for q in stripes)-min(q.y for q in stripes)
  assert abs(aisle-7.3152)<.00002 and abs(stall_depth-5.4864)<.00002,(aisle,stall_depth)
  # An upward-extruded walk would end above the neighboring carpet.
  concrete=palette_vertices('concrete');assert concrete
  parking=dict(aisle_clear_depth_m=aisle,stall_depth_m=stall_depth,court_width_m=max(q.x for q in asphalt)-min(q.x for q in asphalt),court_depth_m=max(q.y for q in asphalt)-front)
  # Actual water/terrain surfaces prove the pond's open connection into its
  # channel; a separately valid oval and strip could still have a wall between.
  waterroot=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='water_system');water_tree=tree([o for o in waterroot.children if o.type=='MESH']);site_tree=tree(site_meshes);water_proof=[]
  if meta['kind']=='adventure':
   for y in (-6.8,-4,-3,0,5):
    origin=Vector((0,y,2));hit=water_tree.ray_cast(origin,Vector((0,0,-1)),4);assert hit[0] is not None and abs(hit[0].z+.17)<.00002,('Water connection',y,hit)
    terrain_hit=site_tree.ray_cast(origin,Vector((0,0,-1)),4);assert terrain_hit[0] is None,('Terrain blocks water',y,terrain_hit)
    water_proof.append(list(hit[0]))
  walk_x,walk_y,walk_z=(17.25,7,.975) if meta['kind']=='adventure' else (-19,-10.6,.065)
  hit=site_tree.ray_cast(Vector((walk_x,walk_y,4)),Vector((0,0,-1)),6);assert hit[0] is not None and abs(hit[0].z-walk_z)<.015,('Walk top',hit,walk_z)
  walk_proof=dict(measured_top_m=list(hit[0]),nominal_top_z_m=walk_z)
  bridge_proof=[]
  for rt in [o for o in bpy.context.scene.objects if o.get('module_kind')=='footbridge']:
   bvh=tree([o for o in rt.children if o.type=='MESH']);probes=[]
   for x in (-1.77,1.77):
    for y in (-.65,.65):
     # Top hit proves deck presence. Joist support was measured separately
     # before consolidation, where construction faces remain identifiable.
     q=rt.matrix_world@Vector((x,y,1.0));hit=bvh.ray_cast(q,Vector((0,0,-1)),2);assert hit[0] is not None
     probes.append(list(hit[0]))
   bridge_proof.append(dict(root=rt.name,deck_top_probes_m=probes))
  rows.append(dict(seed=seed,passed=True,triangles=counts,cups=cup_measure,motion=motion,materials=meta['materials'],kind=meta['kind'],bridge=bridge_proof,parking=parking,continuous_water_probes_m=water_proof,walk_top=walk_proof))
 # Pure generator determinism and distinct seeded dimensions/order.
 for seed in range(250):
  a=generate(seed);assert a==generate(seed);assert [h['number'] for h in a['holes']]==list(range(1,19));assert len({h['feature'] for h in a['holes']})>=5
 assert generate(71,'classic')['lot']!=generate(92,'adventure')['lot']
 plan_proof=validate()
 out=dict(passed=True,plan_envelopes=plan_proof,rows=rows,shared_external_images=used_images,generator_seeds_checked=250,scope=__doc__)
 Path('build/check.json').write_text(json.dumps(out,indent=2));preserve();print('MINIGOLF CHECK PASS',[(r['kind'],r['triangles']) for r in rows])
if __name__=='__main__':check()
