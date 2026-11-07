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
  rows[str(p['seed'])]=dict(holes=holes_data,fixtures=fixture_data,bridge_contacts=bridges)
 Path('build/source-construction.json').write_text(json.dumps(rows,indent=2))

def build(args):
 preserve();bpy.ops.wm.read_factory_settings(use_empty=True);F.setup();roots=[]
 for seed,kind in ((args.classic_seed,'classic'),(args.adventure_seed,'adventure')):
  p=generate(seed,kind);course=F.root('Course_'+str(seed),kind='course');course['seed']=seed;course['course_kind']=kind
  for h in p['holes']:
   rt,audit=holes.build(h,course)
   if h['fixture']:
    x,y=center(h,.49);z=level(h,x,.49)+.005
    fixtures.build(h['fixture'],(x,y,z),0,rt,'Fixture_%02d_%s'%(h['number'],h['fixture']))
  S.build(p,course);roots.append((course,p))
 source_measure(roots)
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and any(m.name=='Walk slab gauge' for m in ob.modifiers):assert min(p.normal.z for p in ob.data.polygons)>0,'Downward walk top: '+ob.name
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
  path=Path('export')/f'Minigolf-{p["seed"]}.gltf';path.parent.mkdir(parents=True,exist_ok=True)
  bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',use_selection=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_tangents=False,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False,export_texture_dir='textures')
  doc=json.loads(path.read_text());images=[dict(uri=im['uri'],bytes=(path.parent/im['uri']).stat().st_size) for im in doc.get('images',[])]
  row=dict(seed=p['seed'],kind=p['kind'],plan=p,triangles=sum(triangles(o) for o in meshes),holes=hole_counts,fixtures=fixture_counts,modules=counts,materials=len(doc['materials']),meshes=len(doc['meshes']),primitives=sum(len(m['primitives']) for m in doc['meshes']),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images)
  manifest.append(row);path.with_suffix('.json').write_text(json.dumps(row,indent=2))
  print('COURSE',p['kind'],row['triangles'],'triangles; holes',min(hole_counts.values()),max(hole_counts.values()),'fixtures',fixture_counts,flush=True)
 Path('build/manifest.json').write_text(json.dumps(manifest,indent=2))
 out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
 preserve()

def ancestors(ob,stop):
 p=ob.parent
 while p and p!=stop:yield p;p=p.parent

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/course.blend');p.add_argument('--classic-seed',type=int,default=71);p.add_argument('--adventure-seed',type=int,default=92);args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None);build(args)
