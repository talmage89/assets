"""Cycles source checkpoint with tint factors, light state and tonal masks."""
import argparse,hashlib,json,math,runpy,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
import pickup_spec as S


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=48)
 p.add_argument('--shots',default='front_three_quarter,rear_three_quarter,side,front_detail,wheel_detail,lamps_lit')
 p.add_argument('--camera-file');p.add_argument('--paint',default='Atlantic',choices=list(S.COLORS));p.add_argument('--colors',action='store_true');p.add_argument('--masks',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();digest=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(source));sc=bpy.context.scene;camera=studio.add_studio(scale=3,backdrop_color=(.20,.21,.22))
 # A car-sized diffusion panel lowers reflected source luminance while
 # retaining key power; paint highlights must roll off, not clip.
 for light_name in ['Right rim strip','Left rim strip']:
  bpy.data.objects[light_name].data.size*=4.5
 bpy.data.objects['Key softbox'].data.size*=1.6
 bpy.data.objects['Key softbox'].data.size_y*=1.2
 bpy.data.objects['Overhead reflection card'].data.size*=1.5
 if a.camera_file:
  from lighting import outdoor
  outdoor()
 sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True
 sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=8
 sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.035
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-2.0
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_percentage=100
 config=runpy.run_path(str(Path(__file__).with_name('config.py')));shots=config['LOOKDEV_SHOTS']
 if a.camera_file:
  shots={name:dict(data['shot'],paint=data['shot'].get('paint','Carbon'),studio_yaw=0) for name,data in json.loads(Path(a.camera_file).read_text()).items()}
 if a.colors:
  shots={'paint_'+name:dict(config['LOOKDEV_SHOTS']['front_three_quarter'],paint=name) for name in S.COLORS}
 names=list(shots) if a.colors or a.camera_file else a.shots.split(',')
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
 bpy.context.view_layer.update()
 rest={o:o.matrix_world.copy() for o in sc.objects if o.get('studio') and o!=camera}
 studio_visibility={o:o.hide_render for o in rest}
 recipe=hashlib.sha256(b''.join(p.read_bytes() for p in [Path(__file__),Path(__file__).with_name('config.py'),Path(__file__).with_name('lighting.py'),Path(__file__).with_name('pickup_spec.py'),ROOT/'kit/studio.py'])).hexdigest()
 colors={m:m.diffuse_color[:] for m in bpy.data.materials}
 for name in names:
  shot=shots[name];paint=shot.get('paint',a.paint)
  lighting_description='procedural studio with broadened diffusion panels'
  for m in bpy.data.materials:
   if m.get('vehicle_paint'):
    m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*S.COLORS[paint],1)
    m.node_tree.nodes['Paint metallic'].outputs[0].default_value=S.PAINT_METAL[paint]
   if m.get('lamp_lit_strength',0)>0:
    m.node_tree.nodes['SURFACE'].inputs['Emission Strength'].default_value=m['lamp_lit_strength'] if shot.get('lights') else 0
  xf=Matrix.Rotation(math.radians(shot.get('studio_yaw',0)),4,'Z')
  for ob,matrix in rest.items():ob.matrix_world=xf@matrix
  if a.camera_file:
   from lighting import conditions
   lighting_description=conditions(name)
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
  camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
  camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',6.7);camera.data.lens=shot.get('lens',57)
  camera.data.clip_start=.01;camera.data.clip_end=100
  sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.6))
  sc.render.film_transparent=bool(a.camera_file) or camera.data.type=='ORTHO'
  bpy.data.objects['Studio seamless'].hide_render=sc.render.film_transparent
  sc.view_settings.exposure=shot.get('exposure',-2.0);sc.render.filepath=str((out/(name+'.png')).resolve())
  bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
  meta[name]=dict(shot,source=str(source),source_sha256=digest,stage='source detail and procedural look-dev; no bake',
      paint=paint,engine='CYCLES',samples=a.samples,width=sc.render.resolution_x,height=sc.render.resolution_y)
  meta[name].update(exposure=sc.view_settings.exposure,render_recipe_sha256=recipe,paint_linear_rgb=S.COLORS[paint],paint_metallic=S.PAINT_METAL[paint],lighting=lighting_description)
  if a.camera_file:
   sun=bpy.data.objects['Comparison sun']
   meta[name]['sun_ray_direction']=list(sun.matrix_world.to_quaternion()@Vector((0,0,-1)))
   meta[name]['environment_strength']=sc.world.node_tree.nodes['Comparison environment'].inputs['Strength'].default_value
  if a.masks:
   # Independent opaque geometry mask, plus a white paint-material mask.
   # This avoids counting the studio floor as the vehicle's tonal distribution.
   for ob in rest:
    if ob.type=='MESH':ob.hide_render=True
   for m in bpy.data.materials:m.diffuse_color=(1,1,1,1) if m.get('vehicle_paint') else (0,0,0,1)
   sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='MATERIAL'
   sc.display.shading.show_shadows=False;sc.display.shading.show_cavity=False;sc.display.shading.show_specular_highlight=False
   sc.display.render_aa='16';sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.render.film_transparent=True
   sc.render.filepath=str((out/(name+'-mask.png')).resolve());bpy.ops.render.render(write_still=True)
   for ob in rest:
    if ob.type=='MESH':ob.hide_render=studio_visibility[ob]
   for m,col in colors.items():m.diffuse_color=col
   sc.render.engine='CYCLES';sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
   meta[name]['tonal_mask']=name+'-mask.png'
  (out/'shots.json').write_text(json.dumps(meta,indent=2));print('LOOKDEV_RENDERED',name,flush=True)


if __name__=='__main__':main()
