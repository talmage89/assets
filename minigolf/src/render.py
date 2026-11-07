"""Final judgments from freshly imported external-image glTF deliveries."""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
from kit.gpu import enable
import context
from plan import local,center,level,halfwidth,water_level
from external import bundle
from render_batch import recipe_hash

def world(sun=(.8,.2,.60),energy=3.4,sky_strength=.18):
 sc=bpy.context.scene;w=bpy.data.worlds.new('Procedural sky');w.use_nodes=True;sc.world=w
 nt=w.node_tree;b=nt.nodes['Background'];sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.atan2(sun[2],math.hypot(*sun[:2]));sky.sun_rotation=math.atan2(sun[1],sun[0]);sky.sun_disc=False;sky.altitude=.2;nt.links.new(sky.outputs[0],b.inputs['Color']);b.inputs['Strength'].default_value=sky_strength
 d=bpy.data.lights.new('Raking sun','SUN');d.energy=energy;d.angle=math.radians(1.2);ob=bpy.data.objects.new('Raking sun',d);sc.collection.objects.link(ob);ob.rotation_euler=Vector((-sun[0],-sun[1],-sun[2])).to_track_quat('-Z','Y').to_euler()

def camera(shot):
 sc=bpy.context.scene;d=bpy.data.cameras.new('Checkpoint camera');o=bpy.data.objects.new('Checkpoint camera',d);sc.collection.objects.link(o);sc.camera=o
 o.location=shot['location'];o.rotation_euler=(Vector(shot['target'])-o.location).to_track_quat('-Z','Y').to_euler();d.lens=shot.get('lens',40);d.sensor_width=36;d.sensor_fit='HORIZONTAL';d.shift_y=shot.get('shift_y',0);d.shift_x=shot.get('shift_x',0)
 if shot.get('roll'):o.rotation_euler.rotate_axis('Z',shot['roll'])
 if 'ortho' in shot:d.type='ORTHO';d.ortho_scale=shot['ortho']
 return o

def views(p):
 W,D=p['lot'];adv=p['kind']=='adventure';bank_h=next(q for q in p['holes'] if q['feature']=='ramp');h=p['holes'][0];tee=h['tee'];cup=h['cup'];fx=next(q for q in p['holes'] if q['fixture']=='windmill');fcx,fcy=center(fx,.49);fcz=level(fx,fcx,.49)+.005;c=local(fx,fcx,fcy,fcz)
 def relative(pt,dx,dy,dz):return (pt[0]+dx,pt[1]+dy,pt[2]+dz)
 def fixture_view(kind):
  hh=next(q for q in p['holes'] if q['fixture']==kind);xx,yy=center(hh,.49);zz=level(hh,xx,.49)+.005
  return dict(location=local(hh,xx-4,yy-(13 if kind=='castle' else 10),zz+1.65),target=local(hh,xx,yy,zz+(2.6 if kind=='castle' else 2.2)),lens=42,aspect=1.5)

 return {
 'front':dict(location=(0,-D*1.5,D*.30),target=(0,0,1),ortho=W*1.14,lens=45,aspect=1.5),
 'side':dict(location=(W*1.5,0,D*.30),target=(0,0,1),ortho=D*1.14,lens=45,aspect=1.5),
 'back':dict(location=(0,D*1.5,D*.30),target=(0,0,1),ortho=W*1.14,lens=45,aspect=1.5),
 'top':dict(location=(0,-2,90),target=(0,-2,0),ortho=max(W,D)*1.08,lens=45,aspect=1.05),
 'ground':dict(location=(7.5,-12.5,1.65) if adv else (-15,-14,1.65),target=(0,9,1.65) if adv else (-4,9,1.65),lens=40,aspect=1.8,shift_y=-.035),
 'above':dict(location=(-58,-66,71) if adv else (-45,-55,61),target=(0,-2,0),lens=43,aspect=1.5),
 'hero':dict(location=(0,-7.1,1.894) if adv else (-6,12.5,1.665),target=(3,10.5,2.0) if adv else (0,2,1.2),lens=35 if adv else 40,aspect=1.6,shift_y=0 if adv else -.04,**(dict(sun=(-.65,-.65,.40)) if adv else {})),
 'tee':dict(location=relative(tee,-2.1,-2.7,1.85),target=relative(tee,-.65,.0,.65),lens=46,aspect=1.45),
 'cup':dict(location=relative(cup,-.38,-.42,.40),target=relative(cup,0,0,.015),lens=55,aspect=1.35),
 'border':dict(location=relative(tee,-2.1,.45,.56),target=relative(tee,-1.0,.75,.05),lens=55,aspect=1.55),
 'waterfall':dict(location=(-.5,7.2,3.25),target=(2.0,9.65,1.35),lens=32,aspect=1.25,sun=(-.65,-.65,.48)),
 'pond':dict(location=(-7,-4,13.5),target=(0,3,0),lens=32,aspect=1.2,sun=(-.65,-.65,1.4),sky_strength=.24),
 'fixture':dict(location=local(fx,fcx-3.5,fcy-8.5,fcz+1.65),target=relative(c,0,0,1.65),lens=48,aspect=1.35,human=local(fx,fcx-halfwidth(fx,.49)-1.05,fcy,fcz-.13)),
 'lighthouse':fixture_view('lighthouse'),
 'castle':fixture_view('castle'),
 'bank':dict(location=relative(bank_h['tee'],-3,-2,1.2),target=relative(bank_h['cup'],0,0,-.12),lens=42,aspect=1.6),
 'planting':dict(location=(2,-8,1.65),target=(5.2,-1,.7),lens=45,aspect=1.6),
 'road':dict(location=(-67,-27,1.65),target=(-42,-55,3.5),lens=24,aspect=1.8),
 'sign':dict(location=(-W/2-2,-D/2-8.5,1.65),target=(-W/2+4,-D/2+2,3.3),lens=45,aspect=1.2),
 'bridge':dict(location=(-4.6,-10,1.65),target=(0,-7.1,.5),lens=42,aspect=1.6),
 'clubhouse':dict(location=(0,p['clubhouse'][1]+10.65,1.65),target=(0,p['clubhouse'][1]+2.35,1.55),lens=42,aspect=1.6),
 }

def scene(seed,source=None):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 source=Path(source or f'export/Minigolf-{seed}.gltf');p=json.loads(source.with_suffix('.json').read_text())['plan']
 bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
 for ob in bpy.context.scene.objects:
  if 'Clubhouse__ServiceSash' in ob.name and ob.type=='EMPTY':ob.location.x=-1.4
 landscape=Path(f'export/Minigolf-{seed}-landscape.gltf')
 if landscape.exists():bpy.ops.import_scene.gltf(filepath=str(landscape.resolve()))
 ctx=context.make(p,omit_course_plants=landscape.exists());
 if landscape.exists():ctx['landscape_export']=dict(source=str(landscape),sha256=bundle(landscape))
 ctx['service_sash_pose_x_m']=-1.4
 # The presentation ground must leave the course's real excavation open.
 from mathutils.bvhtree import BVHTree
 vertices=[];faces=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not ob.parent or not ob.parent.name.startswith('Context terrain'):continue
  ob.data.calc_loop_triangles();off=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices);faces.extend(tuple(off+k for k in t.vertices) for t in ob.data.loop_triangles)
 terrain=BVHTree.FromPolygons(vertices,faces,all_triangles=True);probes=[]
 for x,y in ([(0,-6.8),(0,0),(0,5)] if p['water'] else [(-1.7,5)]):
  hit=terrain.ray_cast(Vector((x,y,water_level(y)+.002)),Vector((0,0,1)),5);assert hit[0] is None,('Context ground conceals course water',hit)
  probes.append([x,y,water_level(y)])
 ctx['context_terrain_clear_over_water']=probes

 return source,p,ctx

def render_one(name,shot,source,p,ctx,args):
 sc=bpy.context.scene;human_objects=[];human_proof=None;eye_proof=None
 if name.endswith('dusk'):shot=dict(shot,sun=(.8,.2,-.08),sun_energy=0,sky_strength=.65,exposure=.5)
 requested_camera=json.loads(json.dumps(shot))
 out=Path(args.out)/(name+'.png');receipt=out.with_suffix('.json')
 recipe=recipe_hash();digest=bundle(source)
 if out.exists() and receipt.exists():
  old=json.loads(receipt.read_text())
  if old.get('recipe_sha256')==recipe and old.get('sha256')==digest and old.get('width')==args.width and old.get('samples',0)>=args.samples and old.get('requested_camera')==requested_camera and old.get('context')==json.loads(json.dumps(ctx)):
   print('CURRENT FRAME',out,flush=True);return

 if shot.get('human'):
  from kit.studio import human
  from mathutils.bvhtree import BVHTree
  floor=Vector(shot['human']);verts=[];faces=[]
  root=next(o for o in sc.objects if o.get('module_kind')=='course')
  for ob in root.children_recursive:
   if ob.type!='MESH':continue
   ob.data.calc_loop_triangles();off=len(verts);verts.extend(ob.matrix_world@v.co for v in ob.data.vertices);faces.extend(tuple(off+k for k in t.vertices) for t in ob.data.loop_triangles)
  surface=BVHTree.FromPolygons(verts,faces,all_triangles=True);hit=surface.ray_cast(Vector((floor.x,floor.y,20)),Vector((0,0,-1)),30)
  assert hit[0] is not None,'Missing physical support for scale silhouette';floor.z=hit[0].z
  human_objects=human();offset=floor+Vector((1.03,-.24,0))
  for ob in human_objects:ob.location+=offset
  bpy.context.view_layer.update();q=[ob.matrix_world@v.co for ob in human_objects if ob.type=='MESH' for v in ob.data.vertices];height=max(v.z for v in q)-min(v.z for v in q);assert abs(height-1.8)<1e-5;human_proof=dict(measured_height_m=height,feet=list(floor),support='Actual imported course surface down ray')
 if name in ('classic-hero','adventure-hero','classic-dusk','adventure-dusk'):
  from mathutils.bvhtree import BVHTree
  vertices=[];faces=[];root=next(o for o in sc.objects if o.get('module_kind')=='course')
  for ob in root.children_recursive:
   if ob.type!='MESH':continue
   ob.data.calc_loop_triangles();off=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices);faces.extend(tuple(off+k for k in t.vertices) for t in ob.data.loop_triangles)
  support=BVHTree.FromPolygons(vertices,faces,all_triangles=True);eye=Vector(shot['location']);hit=support.ray_cast(eye,Vector((0,0,-1)),5)
  assert hit[0] is not None,(name,hit)
  eye.z=hit[0].z+1.65;shot=dict(shot,location=list(eye))
  assert 35<=shot['lens']<=50
  eye_proof=dict(eye_above_imported_support_m=eye.z-hit[0].z,support_world_m=list(hit[0]))
 sc.render.engine=getattr(args,'engine','CYCLES');
 if sc.render.engine=='CYCLES':enable();
 sc.cycles.samples=args.samples;sc.cycles.use_denoising=True;sc.cycles.seed=17
 for socket in [o for o in sc.objects if o.get('socket_kind')=='service_counter_light']:
  data=bpy.data.lights.new('Operating counter fluorescent','AREA');data.energy=90;data.color=(1,.92,.78);data.shape='RECTANGLE';data.size=1.14;data.size_y=.18;ob=bpy.data.objects.new('Operating counter fluorescent',data);sc.collection.objects.link(ob);ob.location=socket.matrix_world.translation
 if name.endswith('dusk'):
  shot=dict(shot,sun=(.8,.2,-.08),sun_energy=0,sky_strength=.65,exposure=.5)
  for socket in [o for o in sc.objects if o.get('socket_kind')=='light_emitter']:
   data=bpy.data.lights.new('Night-play flood','AREA');data.energy=1200;data.color=(1,.81,.58);data.shape='DISK';data.size=.65;ob=bpy.data.objects.new('Night-play flood',data);sc.collection.objects.link(ob);ob.location=socket.matrix_world.translation
 world(shot.get('sun',(.8,.2,.60)),shot.get('sun_energy',3.4),shot.get('sky_strength',.18));cam=camera(shot)
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=shot.get('exposure',-.10)
 sc.render.resolution_x=args.width;sc.render.resolution_y=round(args.width/shot.get('aspect',1.6));sc.render.resolution_percentage=100
 sc.render.image_settings.file_format='PNG';out=Path(args.out)/(name+'.png');out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
 meta=dict(source=str(source),sha256=bundle(source),engine=sc.render.engine,camera=shot,requested_camera=requested_camera,context=ctx,samples=args.samples,width=args.width,recipe_sha256=recipe,scale_silhouette=human_proof,eye_height=eye_proof)
 out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.data.objects.remove(cam,do_unlink=True)
 for ob in human_objects:bpy.data.objects.remove(ob,do_unlink=True)
 for ob in list(sc.objects):
  if ob.type=='LIGHT':bpy.data.objects.remove(ob,do_unlink=True)

def main(args):
 chosen=args.shots.split(',') if args.shots else None;requested_engine=args.engine
 for seed,kind in ((71,'classic'),(92,'adventure')):
  requested=['ground','above','hero','dusk','front','side','back','top']+(['tee','cup','border','waterfall','pond','fixture','bridge','clubhouse','lighthouse','castle','bank','planting','road','sign','eevee'] if kind=='adventure' else ['tee','cup','border'])
  if chosen:requested=[n for n in requested if n in chosen or kind+'-'+n in chosen]
  if not requested:continue
  source,p,ctx=scene(seed)
  for name in requested:
   args.engine='BLENDER_EEVEE' if name=='eevee' else requested_engine
   render_one((kind+'-'+name) if name in ('ground','above','hero','dusk','front','side','back','top') or kind=='classic' else name,views(p)['hero' if name=='dusk' else 'ground' if name=='eevee' else name],source,p,ctx,args)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source');parser.add_argument('--out',default='renders/lookdev');parser.add_argument('--width',type=int,default=1440);parser.add_argument('--samples',type=int,default=40);parser.add_argument('--shots');parser.add_argument('--engine',default='CYCLES');a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);main(a)
