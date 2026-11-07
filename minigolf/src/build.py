"""Build both seeded construction checkpoints and external-image glTFs."""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
import geometry as F
import holes,fixtures,site as builtin_site
# Python preloads stdlib site. Load our family module by an unambiguous name.
import importlib.util
spec=importlib.util.spec_from_file_location('course_site',HERE/'site.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
from plan import generate,center,level
from preserve import check as preserve

def triangles(ob):
 ob.data.calc_loop_triangles();return len(ob.data.loop_triangles)

def source_measure(roots):
 bpy.context.view_layer.update();rows={}
 for course,p in roots:
  holes_data={};fixture_data={}
  for rt in course.children_recursive:
   if rt.get('module_kind')=='hole':
    carpet=next(o for o in rt.children if o.name.startswith('Carpet playing face'))
    cup=next(o for o in rt.children if o.name.startswith('Cup aluminum liner'))
    pad=next(o for o in rt.children if o.name.startswith('Rubber tee pad'))
    c=bpy.data.objects[rt.name+'__Cup'].location
    pts=[v.co for v in cup.data.vertices]
    radii=[math.hypot(v.x-c.x,v.y-c.y) for v in pts]
    zs=[v.z for v in pts]
    low=min(radii);diameter=2*low
    assert abs(diameter-.10795)<1e-5,(rt.name,diameter)
    # Actual mesh boundaries and actual pad vertices, independent of constructor constants.
    width=max(v.co.x for v in pad.data.vertices)-min(v.co.x for v in pad.data.vertices)
    # box() stores dimensions in mesh and center in its local object transform.
    assert abs(width-.9144)<1e-5
    slab=next(o for o in rt.children if o.name.startswith('Four inch concrete slab edge'));n=len(slab.data.vertices)//2;gauge=[slab.data.vertices[i].co.z-slab.data.vertices[i+n].co.z for i in range(n)];assert max(abs(v-.1016) for v in gauge)<1e-5
    holes_data[rt.name]=dict(slab_thickness_range_m=[min(gauge),max(gauge)],cup_inner_diameter_m=diameter,cup_depth_m=max(zs)-min(zs),tee_mat_width_m=width,
      carpet_vertices=len(carpet.data.vertices),carpet_bounds_m=[[min(v.co[k] for v in carpet.data.vertices) for k in range(3)],[max(v.co[k] for v in carpet.data.vertices) for k in range(3)]])
   if rt.get('fixture_kind'):
    points=[o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
    fixture_data[rt.name]=dict(kind=rt['fixture_kind'],bounds_m=[[min(v[k] for v in points) for k in range(3)],[max(v[k] for v in points) for k in range(3)]])
  bridges=[]
  for bridge in [o for o in course.children_recursive if o.get('module_kind')=='footbridge']:
   joists=[o for o in bridge.children if o.name.startswith('2x6 continuous joist')];decks=[o for o in bridge.children if o.name.startswith('Bridge deck board')];abut=[o for o in bridge.children if o.name.startswith('Bridge concrete abutment')]
   def zbound(obs,op):return op((o.matrix_local@v.co).z for o in obs for v in o.data.vertices)
   seat=zbound(decks,min)-zbound(joists,max);support=zbound(joists,min)-zbound(abut,max);assert abs(seat)<1e-5 and abs(support)<1e-5,(seat,support)
   bridges.append(dict(root=bridge.name,deck_to_joist_gap_m=seat,joist_to_abutment_gap_m=support))
  from mathutils.bvhtree import BVHTree
  def bvh(obs,top_only=False):
   vs=[];fs=[];dg=bpy.context.evaluated_depsgraph_get()
   for ob in obs:
    data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg);data.calc_loop_triangles();off=len(vs);vs.extend(ob.matrix_world@v.co for v in data.vertices);fs.extend(tuple(off+k for k in t.vertices) for t in data.loop_triangles if not top_only or t.normal.z>.5);bpy.data.meshes.remove(data)
   return BVHTree.FromPolygons(vs,fs,all_triangles=True)
  ground_parts=[o for o in course.children_recursive if o.type=='MESH' and o.name.startswith(('Site planted grade','Shared mulched landscape bed'))]
  ground=bvh(ground_parts,True);ground_gaps=[]
  for playing in [o for o in course.children_recursive if o.type=='MESH' and o.name.startswith('Carpet playing face')]:
   for face in playing.data.polygons:
    q=playing.matrix_world@face.center;hit=ground.ray_cast(Vector((q.x,q.y,10)),Vector((0,0,-1)),20)
    if hit[0] is not None:
     gap=q.z-hit[0].z;assert gap>.03,('Landscape covers actual playing carpet',playing.name,list(q),list(hit[0]),gap);ground_gaps.append(gap)
  obstacle_checks=[]
  rocks=[o for o in course.children_recursive if o.type=='MESH' and o.name.startswith(('Quarry mountain','Quarry terraced','Quarry upper','Western terraced outcrop','Fractured fall','Carved terrace'))]
  surfaces=[o for o in course.children_recursive if o.type=='MESH' and (o.get('walking_surface') or o.name.startswith('Carpet playing face'))]
  surface_trees={o:bvh([o],True) for o in surfaces}
  for rock in rocks:
   tree=bvh([rock])
   for ob,surface in surface_trees.items():
    hits=tree.overlap(surface);assert not hits,('Quarry obstructs actual playing/walking surface',rock.name,ob.name,len(hits))
   obstacle_checks.append(dict(rock=rock.name,surfaces_checked=len(surfaces),triangle_intersection_pairs=0,scope='Evaluated source rock surfaces against actual top triangles, within this course only; separate from plan-space envelopes'))
  crossing_contacts=[]
  for owner in [o for o in course.children_recursive if o.get('module_kind') in ('hole','walk_span')]:
   girders=[o for o in owner.children if o.name.startswith(('Continuous bridge-slab girder','Continuous crossing-walk girder'))]
   if not girders:continue
   skin=[o for o in owner.children if o.name.startswith('Bridge slab underside') or o.get('walking_surface')]
   support=[o for o in owner.children if o.name.startswith(('Stream-crossing abutment','Bridge elastomer bearing','Crossing-walk abutment'))]
   underside=bvh(skin);seats=bvh(support);gaps=[];bearing=[]
   for girder in girders:
    for face in girder.data.polygons:
     if face.normal.z>.8:
      q=girder.matrix_world@face.center;hit=underside.find_nearest(q);gaps.append(hit[3])
    for station in (list(girder.data.vertices)[:4],list(girder.data.vertices)[-4:]):
     lowest=sorted(station,key=lambda v:v.co.z)[:2]
     for vertex in lowest:bearing.append(seats.find_nearest(girder.matrix_world@vertex.co)[3])
   assert gaps and max(gaps)<.003,(owner.name,'girder skin',max(gaps))
   assert bearing and max(bearing)<.003,(owner.name,'girder bearing',max(bearing))
   crossing_contacts.append(dict(root=owner.name,top_surface_max_gap_m=max(gaps),abutment_bearing_max_gap_m=max(bearing),top_samples=len(gaps),bearing_samples=len(bearing),scope='Nearest distances between evaluated source surfaces and actual girder top/bearing points; separate from export serialization'))
  bench_contacts=[]
  for bench in [o for o in course.children_recursive if o.get('module_kind')=='bench']:
   pad=next(o for o in bench.children if o.name.startswith('Bench anchored concrete pad'));seat=bvh([pad]);gaps=[]
   for leg in [o for o in bench.children if o.name.startswith('Bench leg')]:
    points=[leg.matrix_world@v.co for v in leg.data.vertices];z=min(v.z for v in points)
    gaps.extend(seat.find_nearest(q)[3] for q in points if q.z<z+1e-6)
   assert gaps and max(gaps)<1e-5,(bench.name,max(gaps));bench_contacts.append(dict(root=bench.name,leg_to_pad_max_gap_m=max(gaps),samples=len(gaps)))
  counter_contacts=[]
  for hut in [o for o in course.children_recursive if o.get('module_kind')=='clubhouse']:
   floors=[o for o in hut.children if o.name.startswith('Ball tray plywood floor')];stock=[o for o in hut.children if o.name.startswith('Counter ball')];floor_tree=bvh(floors);stock_gaps=[]
   def vertical_gap(tree,q,direction):
    start=q-Vector((0,0,direction*.01));hit=tree.ray_cast(start,Vector((0,0,direction)),.03)
    assert hit[0] is not None,('Missing bearing surface',hut.name,list(q));return abs(q.z-hit[0].z)
   for ball in stock:
    points=[ball.matrix_world@v.co for v in ball.data.vertices];bottom=min(points,key=lambda q:q.z);stock_gaps.append(vertical_gap(floor_tree,bottom,-1))
   base=next(o for o in hut.children if o.name.startswith('Sash lower channel base'));base_tree=bvh([base]);glide_gaps=[];rail_gaps=[]
   for glide in [o for o in hut.children_recursive if o.name.startswith('Sash nylon glide')]:
    points=[glide.matrix_world@v.co for v in glide.data.vertices];lo=min(q.z for q in points);hi=max(q.z for q in points);rail_tree=bvh([o for o in glide.parent.children if o.name.startswith('Sash rail')])
    glide_gaps.extend(vertical_gap(base_tree,q,-1) for q in points if q.z<lo+1e-6);rail_gaps.extend(vertical_gap(rail_tree,q,1) for q in points if q.z>hi-1e-6)
   assert stock_gaps and max(stock_gaps)<1e-5,(hut.name,'Floating counter stock',max(stock_gaps))
   assert glide_gaps and max(glide_gaps)<1e-5 and max(rail_gaps)<1e-5,(hut.name,'Sash support',max(glide_gaps),max(rail_gaps))
   counter_contacts.append(dict(root=hut.name,stock_balls=len(stock),ball_to_tray_max_gap_m=max(stock_gaps),glide_to_track_max_gap_m=max(glide_gaps),glide_to_sash_max_gap_m=max(rail_gaps),scope='Vertical rays onto actual evaluated support faces at stock/glide extremal vertices; measures seating without tangential nearest-point roundoff'))
  flow_normals=[]
  for flow in [o for o in course.children_recursive if o.get('flow_sheet')]:
   ys=[(flow.matrix_world.to_3x3().inverted().transposed()@f.normal).y for f in flow.data.polygons]
   assert max(ys)<-.5,('Spill sheet faces upstream, risking inside-water refraction',flow.name,min(ys),max(ys))
   flow_normals.append(dict(sheet=flow.name,world_y_normal_range=[min(ys),max(ys)],scope='Actual source face normals point into downstream air'))
  pool_normals=[]
  for pool in [o for o in course.children_recursive if o.type=='MESH' and o.name.startswith(('Continuous pond and stream water','Receiving spill pool'))]:
   zs=[(pool.matrix_world.to_3x3().inverted().transposed()@f.normal).z for f in pool.data.polygons]
   assert min(zs)>.5,('Pool skin points into water instead of air',pool.name,min(zs));pool_normals.append(dict(surface=pool.name,world_z_normal_range=[min(zs),max(zs)]))
  posts=[o for o in course.children_recursive if o.type=='MESH' and o.name.startswith('Fence post')]
  centers=[o.matrix_world@(sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)) for o in posts]
  fence=[min(v.x for v in centers),max(v.x for v in centers),min(v.y for v in centers),max(v.y for v in centers)]
  for owner in [o for o in course.children_recursive if o.get('module_kind')=='hole']:
   carpet=next(o for o in owner.children if o.name.startswith('Carpet playing face'))
   points=[carpet.matrix_world@v.co for v in carpet.data.vertices]
   assert all(fence[0]<q.x<fence[1] and fence[2]<q.y<fence[3] for q in points),('Playing face outside actual fence',owner.name)
  rows[str(p['seed'])]=dict(landscape_to_carpet_minimum_gap_m=min(ground_gaps),holes=holes_data,fixtures=fixture_data,bridge_contacts=bridges,crossing_contacts=crossing_contacts,bench_contacts=bench_contacts,counter_contacts=counter_contacts,quarry_obstacle_checks=obstacle_checks,spill_sheet_normals=flow_normals,pool_airside_normals=pool_normals,fence_post_centerline_bounds_m=fence,fenced_play_enclosure_m2=(fence[1]-fence[0])*(fence[3]-fence[2]),fence_measure_scope='Extrema of actual source post-mesh centroids; rectangular paid-play enclosure, excluding hut and parking; all playing-face vertices lie inside')
 Path('build/source-construction.json').write_text(json.dumps(rows,indent=2))

def build(args):
 if args.resume_form:
  preserve();bpy.ops.wm.open_mainfile(filepath=str(Path('build/source-form.blend').resolve()));roots=[]
  for seed,kind in ((args.classic_seed,'classic'),(args.adventure_seed,'adventure')):roots.append((bpy.data.objects['Course_'+str(seed)],generate(seed,kind)))
  F.M.update({name:bpy.data.materials['Quick_'+name] for name in F.COLORS});F.FONT=F.find_font('DejaVu Sans','Bold')
  for ob in bpy.context.scene.objects:
   key=ob.get('graphic')
   if not key or key in F.PRINTS:continue
   F.PRINTS[key]=len(F.PRINTS)
   F.PRINT_LAYOUTS[key]=(key,1) if key.startswith('@pylon:') else (key.rsplit('|',1)[0],float(key.rsplit('|',1)[1]))
 else:
  preserve();bpy.ops.wm.read_factory_settings(use_empty=True);F.setup();roots=[]
  for seed,kind in ((args.classic_seed,'classic'),(args.adventure_seed,'adventure')):
   p=generate(seed,kind);course=F.root('Course_'+str(seed),kind='course');course['seed']=seed;course['course_kind']=kind
   for h in p['holes']:
    rt,audit=holes.build(h,course)
    if h['fixture']:
     x,y=center(h,.49);z=level(h,x,.49)+.005
     fixtures.build(h['fixture'],(x,y,z),0,rt,'Fixture_%02d_%s'%(h['number'],h['fixture']))
   S.build(p,course);roots.append((course,p));print('MODELED',kind,flush=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/source-form.blend').resolve()))
 print('MEASURING CONSTRUCTION',flush=True)
 source_measure(roots)
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and any(m.name=='Walk slab gauge' for m in ob.modifiers):assert min(p.normal.z for p in ob.data.polygons)>0,'Downward walk top: '+ob.name
 bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/source-form.blend').resolve()))
 print('FINALIZING',flush=True)
 F.finalize()
 # Set scale and retain authoring metadata as glTF extras.
 scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
 bpy.context.view_layer.update()
 manifest=[]
 for course,p in roots:
  owned=list(course.children_recursive);meshes=[o for o in owned if o.type=='MESH'];counts={}
  for o in meshes:
   owner=o.parent
   while owner and not (owner.get('module') or owner.get('fixture_kind')):owner=owner.parent
   name=owner.name if owner else 'Unowned';counts[name]=counts.get(name,0)+triangles(o)
  hole_counts={}
  for rt in owned:
   if rt.get('module_kind')=='hole':
    hole_counts[rt.name]=sum(triangles(o) for o in rt.children_recursive if o.type=='MESH' and not any(a.get('fixture_kind') for a in ancestors(o,rt)))
  fixture_counts={rt.name:sum(triangles(o) for o in rt.children_recursive if o.type=='MESH') for rt in owned if rt.get('fixture_kind')}
  bpy.ops.object.select_all(action='DESELECT');course.select_set(True)
  for ob in owned:ob.select_set(True)
  Path('build/embedded').mkdir(parents=True,exist_ok=True)
  path=Path('export')/f'Minigolf-{p["seed"]}.gltf';path.parent.mkdir(parents=True,exist_ok=True)
  bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False,export_texture_dir='textures')
  bpy.ops.export_scene.gltf(filepath=str((Path('build/embedded')/path.with_suffix('.glb').name).resolve()),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False)
  from tangents import repair
  repairs={ext:repair(path.with_suffix(ext) if ext=='.gltf' else Path('build/embedded')/path.with_suffix(ext).name) for ext in ('.gltf','.glb')}
  from external import share
  share(path)
  Path('build',f'tangent-repair-{p["seed"]}.json').write_text(json.dumps(repairs,indent=2))
  doc=json.loads(path.read_text());images=[dict(uri=im['uri'],bytes=(path.parent/im['uri']).stat().st_size) for im in doc.get('images',[])]
  row=dict(seed=p['seed'],kind=p['kind'],plan=p,triangles=sum(triangles(o) for o in meshes),holes=hole_counts,fixtures=fixture_counts,modules=counts,materials=len(doc['materials']),meshes=len(doc['meshes']),primitives=sum(len(m['primitives']) for m in doc['meshes']),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images)
  manifest.append(row);path.with_suffix('.json').write_text(json.dumps(row,indent=2))
  print('COURSE',p['kind'],row['triangles'],'triangles; holes',min(hole_counts.values()),max(hole_counts.values()),'fixtures',fixture_counts,flush=True)
 from pieces import export as export_pieces
 export_pieces(roots)
 # Exporter's image directory is transient; every URI now names its canonical source.
 import shutil
 shutil.rmtree('export/textures',ignore_errors=True)
 for old in Path('export').glob('*.glb'):old.unlink()
 Path('build/manifest.json').write_text(json.dumps(manifest,indent=2))
 out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
 preserve()

def ancestors(ob,stop):
 p=ob.parent
 while p and p!=stop:yield p;p=p.parent

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/course.blend');p.add_argument('--resume-form',action='store_true');p.add_argument('--classic-seed',type=int,default=71);p.add_argument('--adventure-seed',type=int,default=92);args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None);build(args)
