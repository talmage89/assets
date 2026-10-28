"""Checkpoint presentation from exported GLB, with procedural kit studio."""
import argparse,sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import studio,gpu,weapon,weapon_presentation as presentation

def main(config,manifest):
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40)
 p.add_argument('--engine',default='CYCLES');p.add_argument('--shots',default=config.DEFAULT_SHOTS)
 p.add_argument('--camera-file');p.add_argument('--strip',help='Render a uniformly timed action strip at 15 fps');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 if getattr(config,'FINAL_STAGE',False) and source.suffix!='.glb':
  raise ValueError('Final gun presentation requires an exported GLB')
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=60
 if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source))
 else:bpy.ops.import_scene.gltf(filepath=str(source))
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and ob.name.startswith('Icosphere'):bpy.data.objects.remove(ob,do_unlink=True)
 arm=next((o for o in bpy.context.scene.objects if o.type=='ARMATURE'),None)
 # Imported bone axes may differ; imported actions carry their own conversion.
 cam=studio.add_studio(scale=.22,light_center=(0,.03,-.10),backdrop_color=(.30,.32,.34))
 floor=bpy.data.objects['Studio seamless'];floor.location.z=config.floor_height(source)
 sc=bpy.context.scene;sc.render.fps=60;sc.render.engine=a.engine
 if a.engine=='CYCLES':gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=7
 elif a.engine=='BLENDER_WORKBENCH':
  sh=sc.display.shading;sh.light='STUDIO';sh.color_type='SINGLE';sh.single_color=(.33,.35,.37);sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_shadows=False
  for ob in sc.objects:
   if ob.name.startswith('Studio black'):ob.hide_render=True
  sc.display.render_aa='16'
 else:
  sc.eevee.taa_render_samples=a.samples
  sc.eevee.use_raytracing=True
  sc.eevee.ray_tracing_options.resolution_scale='1'
  # Eevee does not honor Cycles' camera-ray visibility on reflection flags.
  for ob in sc.objects:
   if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
 if hasattr(config,'configure_scene'):config.configure_scene(sc,source)
 sc.view_settings.exposure=0;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 sc.render.resolution_percentage=100
 shots={name:dict(shot) for name,shot in config.SHOTS.items()}
 if a.camera_file:
  from guns.common.photo_matches import camera_shots
  shots.update(camera_shots(a.camera_file))
  for name,pose in config.PHOTO_POSES.items():
   if name in shots:shots[name].update(pose)
 baked=any(n.type=='TEX_IMAGE' for ob in sc.objects if ob.type=='MESH' for mat in ob.data.materials if mat and mat.use_nodes for n in mat.node_tree.nodes)
 metadata={}
 names=a.shots.split(',')
 if a.strip:
  CLIPS,FPS=manifest.CLIPS,manifest.FPS
  names=[]
  for i,(f,t) in enumerate(presentation.strip_samples(CLIPS[a.strip]['frames'],fps=FPS)):
   name=f'{a.strip}_{i:03d}';names.append(name)
   shots[name]=dict(config.STRIP_SHOT,action=a.strip,frame=f,time_s=t)
 for name in names:
  s=shots[name]
  if hasattr(config,'prepare_shot'):config.prepare_shot(sc,s)
  if arm:presentation.pose(arm,s.get('action'),s.get('frame',0),floor=floor)
  sc.view_settings.exposure=s.get('exposure',-.6)
  cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
  cam.rotation_euler.rotate_axis('Z',s.get('roll',0));cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
  cam.data.type='ORTHO' if 'ortho' in s else 'PERSP';cam.data.ortho_scale=s.get('ortho',1);cam.data.lens=s.get('lens',70)
  if s.get('aimed'):presentation.aimed_camera(cam,bpy.data.objects['Socket_Eye'])
  cam.data.clip_start=.001;cam.data.clip_end=20
  sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/s.get('aspect',1.35))
  sc.render.film_transparent=('ortho' in s or s.get('background')=='transparent' or bool(s.get('action')));floor.hide_render=sc.render.film_transparent
  sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
  metadata[name]=dict(s,source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),engine=a.engine,
    stage=getattr(config,'RENDER_STAGE','neutral baked atlas integration' if baked else 'unbaked form checkpoint'))
 (out/'shots.json').write_text(json.dumps(metadata,indent=2))
