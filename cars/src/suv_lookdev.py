"""Source checkpoint cameras, five factory factors and mechanical open poses."""
import argparse,sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
from suv_finishes import COLORS,PAINT_METAL
from suv_mechanics import update_supports
from suv_render import SHOTS as FORM_SHOTS
SHOTS={k:FORM_SHOTS[k] for k in ['front_three_quarter','rear_three_quarter','side']}
SHOTS.update(
 face=dict(location=(2.3,-5.5,1.65),target=(0,-1.95,.79),lens=95,aspect=1.6),
 lamp_unlit=dict(location=(1.6,-3.0,1.18),target=(.62,-2.03,.88),lens=85,aspect=1.6),
 lamp_lit=dict(location=(1.6,-3.0,1.18),target=(.62,-2.03,.88),lens=85,aspect=1.6,lights=True),
 wheel=dict(location=(2.1,-2.3,.70),target=(.80,-1.34,.37),lens=72,aspect=1.3),
 cladding=dict(location=(2.0,2.8,.83),target=(.68,1.94,.49),lens=65,aspect=1.6),
 interior_glass=dict(location=(1.65,-.55,1.45),target=(.03,-.10,1.08),lens=42,aspect=1.6),
 interior_dash=dict(location=(1.42,.08,1.65),target=(.12,-.48,.98),lens=38,aspect=1.6),
 cargo_open=dict(location=(-2.1,4.5,1.75),target=(0,1.55,1.04),lens=55,aspect=1.5,parts={'Liftgate':75}),
 underbody=dict(location=(1.5,-3.3,.08),target=(0,.2,.28),lens=32,aspect=1.65),
 underbody_layout=dict(location=(2.3,-3.4,-1.8),target=(0,.05,.35),lens=40,aspect=1.65),
 opened=dict(location=(7,-9,3.3),target=(0,0,1.0),lens=70,aspect=1.7,parts={'Door_FL':60,'Door_FR':-60,'Door_RL':60,'Door_RR':-60,'Hood':-65,'Liftgate':75}),
 gate_open=dict(location=(-4,6,2.4),target=(0,.9,1.2),lens=55,aspect=1.6,parts={'Liftgate':75,'FuelDoor':85}),
 steering=dict(location=(4.5,-6,1.3),target=(0,-.4,.65),lens=63,aspect=1.6,parts={'Steer_FL':35,'Steer_FR':35}),
)


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--shots',default='front_three_quarter,rear_three_quarter,face,wheel,interior_glass');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32);p.add_argument('--paint',default='Graphite');p.add_argument('--camera-file');p.add_argument('--colors',action='store_true');p.add_argument('--preview',action='store_true');p.add_argument('--masks',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
 recipe_files=[Path(__file__),Path(__file__).with_name('suv_lighting.py'),Path(__file__).with_name('lighting.py'),ROOT/'kit/studio.py']
 recipe_hash=hashlib.sha256(b''.join(p.read_bytes() for p in recipe_files)).hexdigest()
 def unchanged():
  if hashlib.sha256(src.read_bytes()).hexdigest()!=source_hash or hashlib.sha256(b''.join(p.read_bytes() for p in recipe_files)).hexdigest()!=recipe_hash:raise RuntimeError('Source or render recipe changed during this render batch; rerun the batch')
 shots=SHOTS
 if a.camera_file:shots={n:r['shot'] for n,r in json.loads(Path(a.camera_file).read_text()).items()}
 if a.colors:shots={f'{color}_{view}':dict(SHOTS[view],paint=color) for color in COLORS for view in ['front_three_quarter','rear_three_quarter']}
 names=list(shots) if a.colors or a.camera_file else a.shots.split(',');meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
 for name in names:
  unchanged()
  bpy.ops.wm.open_mainfile(filepath=str(src));sc=bpy.context.scene;shot=shots[name]
  camera=studio.add_studio(scale=2.5,backdrop_color=(.12,.13,.14))
  from suv_lighting import daylight
  daylight(overcast=True,reflections=True)
  sc.world.node_tree.nodes['Comparison environment'].inputs['Strength'].default_value=3.6
  if name in ['cargo_open','interior_glass','interior_dash','underbody','underbody_layout']:
   from suv_lighting import inspection_fill
   inspection_fill('underbody' if name=='underbody_layout' else name)
  if name=='underbody_layout':bpy.data.objects['Comparison ground'].hide_render=True
  for m in bpy.data.materials:
   if m.get('vehicle_paint'):
    paint=shot.get('paint',a.paint);m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*COLORS[paint],1);m.node_tree.nodes['Paint metallic'].outputs[0].default_value=PAINT_METAL[paint];m.node_tree.nodes['Paint flakes'].outputs[0].default_value=.55 if PAINT_METAL[paint]>0 else 0
   if m.get('lamp_lit_strength',0)>0:m.node_tree.nodes['SURFACE'].inputs['Emission Strength'].default_value=m['lamp_lit_strength'] if shot.get('lights') else 0
  for n,angle in shot.get('parts',{}).items():
   ob=bpy.data.objects[n];ob.matrix_basis=ob.matrix_basis@Matrix.Rotation(math.radians(angle),4,ob['pivot_axis'])
  update_supports()
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
  camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.sensor_width=36;camera.data.sensor_fit='HORIZONTAL';camera.data.lens=shot.get('lens',65);camera.data.ortho_scale=shot.get('ortho',5.4);camera.data.clip_start=.015;camera.data.clip_end=200
  sc.render.engine='BLENDER_EEVEE' if a.preview else 'CYCLES'
  if not a.preview:gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=8
  sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=shot.get('exposure',.6)
  sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.6));sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
  sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
  unchanged()
  meta[name]=dict(shot,source_sha256=source_hash,render_recipe_sha256=recipe_hash,samples=a.samples,stage='source detail and procedural look-dev; no bake',engine=sc.render.engine,paint=shot.get('paint',a.paint),exposure=sc.view_settings.exposure,width=a.width,height=sc.render.resolution_y)
  if a.masks:
   for ob in sc.objects:
    if ob.get('studio') and ob.type=='MESH':ob.hide_render=True
   for mat in bpy.data.materials:mat.diffuse_color=(1,1,1,1) if mat.get('vehicle_paint') else (0,0,0,1)
   sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=False;sc.display.shading.show_cavity=False;sc.display.shading.show_specular_highlight=False;sc.display.shading.show_object_outline=False;sc.display.render_aa='16'
   sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0
   sc.render.filepath=str((out/(name+'-mask.png')).resolve());bpy.ops.render.render(write_still=True)
   meta[name]['tonal_mask']=name+'-mask.png'
  (out/'shots.json').write_text(json.dumps(meta,indent=2));print('X220_LOOKDEV',name,flush=True)
if __name__=='__main__':main()
