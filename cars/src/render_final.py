"""Studio and registered photo views of the exported, embedded-texture GLB only."""
import argparse,hashlib,json,math,runpy,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
import delivery_materials as D


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 p.add_argument('--stage',choices=['final'],default='final');p.add_argument('--config');p.add_argument('--fit-reference');p.add_argument('--shots',default='hero');p.add_argument('--camera-file');p.add_argument('--colors',action='store_true')
 p.add_argument('--width',type=int,default=1500);p.add_argument('--samples',type=int,default=64)
 p.add_argument('--engine',choices=['CYCLES','BLENDER_EEVEE'],default='CYCLES')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source)
 if source.suffix.lower()!='.glb':raise ValueError('Finals accept only an exported GLB')
 digest=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(source.resolve()));D.install()
 sc=bpy.context.scene;camera=studio.add_studio(scale=3,backdrop_color=(.20,.21,.22))
 for name in ['Right rim strip','Left rim strip']:bpy.data.objects[name].data.size*=4.5
 bpy.data.objects['Key softbox'].data.size*=1.6;bpy.data.objects['Key softbox'].data.size_y*=1.2
 bpy.data.objects['Overhead reflection card'].data.size*=1.5
 if a.camera_file:
  from lighting import outdoor
  outdoor()
 people=studio.human();bpy.context.view_layer.update()
 human_height=max((o.matrix_world@v.co).z for o in people if o.type=='MESH' for v in o.data.vertices)-min((o.matrix_world@v.co).z for o in people if o.type=='MESH' for v in o.data.vertices)
 config=runpy.run_path(str(Path(__file__).with_name('final_views.py')));shots=config['FINAL_VIEWS'].copy()
 if a.camera_file:shots={name:row['shot'] for name,row in json.loads(Path(a.camera_file).read_text()).items()}
 if a.colors:shots={'paint_'+name:dict(config['FINAL_VIEWS']['hero'],paint=name) for name in D.colors()}
 names=list(shots) if a.camera_file or a.colors else a.shots.split(',')
 rest={o:o.matrix_world.copy() for o in sc.objects if o.get('studio') and o!=camera}
 visibility={o:o.hide_render for o in rest};poses={o.name:o.matrix_basis.copy() for o in sc.objects if o.type=='EMPTY'}
 original_colors={m:m.diffuse_color[:] for m in bpy.data.materials}
 sc.render.engine=a.engine
 if a.engine=='CYCLES':
  gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=8
  sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.025
 else:
  sc.eevee.taa_render_samples=max(192,a.samples);sc.eevee.use_raytracing=True
  sc.eevee.ray_tracing_options.resolution_scale='1';sc.eevee.ray_tracing_options.screen_trace_quality=1
  sc.eevee.ray_tracing_options.screen_trace_thickness=.003
  D.eevee_glass()
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_percentage=100
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
 recipe=hashlib.sha256(b''.join(path.read_bytes() for path in [Path(__file__),Path(__file__).with_name('delivery_materials.py'),Path(__file__).with_name('config.py'),Path(__file__).with_name('final_views.py'),Path(__file__).with_name('lighting.py'),ROOT/'kit/studio.py'])).hexdigest()
 for name in names:
  shot=shots[name];preset=shot.get('paint','Atlantic');state=D.apply(preset,shot.get('lights',False))
  xf=Matrix.Rotation(math.radians(shot.get('studio_yaw',0)),4,'Z')
  for ob,matrix in rest.items():ob.matrix_world=xf@matrix;ob.hide_render=visibility[ob]
  for person in people:person.hide_render=not shot.get('human',False)
  if shot.get('human'):
   offset=Vector(shot.get('human_offset',(2.60,-1.0,0)))
   for person in people:person.matrix_world=rest[person].copy();person.matrix_world.translation+=offset
  for node,matrix in poses.items():bpy.data.objects[node].matrix_basis=matrix
  for node,pose in shot.get('parts',{}).items():
   bpy.data.objects[node].matrix_basis=poses[node]@Matrix.Rotation(math.radians(pose['angle']),4,pose['axis'])
  lighting='procedural studio with broadened diffusion panels'
  if a.camera_file:
   from lighting import conditions
   lighting=conditions(name)
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
  camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
  camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',6.7);camera.data.lens=shot.get('lens',57)
  camera.data.clip_start=.01;camera.data.clip_end=200
  sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.6))
  sc.render.film_transparent=bool(a.camera_file) or camera.data.type=='ORTHO';bpy.data.objects['Studio seamless'].hide_render=sc.render.film_transparent
  sc.view_settings.exposure=shot.get('exposure',-2.0);sc.render.filepath=str((out/(name+'.png')).resolve())
  bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
  meta[name]=dict(shot,source=str(source),source_sha256=digest,stage='final',paint=preset,paint_state=state,
    engine=a.engine,glass_model='thin-sheet Fresnel from embedded maps' if a.engine=='BLENDER_EEVEE' else 'nested transmission',samples=a.samples if a.engine=='CYCLES' else max(192,a.samples),width=sc.render.resolution_x,height=sc.render.resolution_y,
    exposure=sc.view_settings.exposure,render_recipe_sha256=recipe,lighting=lighting,human_measured_height_m=human_height if shot.get('human') else None)
  for ob in rest:
   if ob.type=='MESH':ob.hide_render=True
  for m in bpy.data.materials:m.diffuse_color=(1,1,1,1) if m.get('paint_decode') else (0,0,0,1)
  sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='MATERIAL'
  sc.display.shading.show_shadows=False;sc.display.shading.show_cavity=False;sc.display.shading.show_specular_highlight=False;sc.display.render_aa='16'
  sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.render.film_transparent=True
  sc.render.filepath=str((out/(name+'-mask.png')).resolve());bpy.ops.render.render(write_still=True)
  meta[name]['tonal_mask']=name+'-mask.png'
  for m,color in original_colors.items():m.diffuse_color=color
  sc.render.engine=a.engine;sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
  (out/'shots.json').write_text(json.dumps(meta,indent=2));print('GLB_RENDERED',name,flush=True)
if __name__=='__main__':main()
