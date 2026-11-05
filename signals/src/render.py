"""Cycles construction evidence, always reimported from checkpoint GLBs."""
import argparse,sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import gpu
from plan import *
from geometry import M
import setting
def setup(samples):
 sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=6
 sc.world=bpy.data.worlds.new('Procedural sky');sc.world.use_nodes=True
 ns=sc.world.node_tree.nodes;ls=sc.world.node_tree.links;ns.clear()
 sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(145);sky.sun_disc=False;sky.aerosol_density=.45
 bg=ns.new('ShaderNodeBackground');bg.inputs[1].default_value=.24
 out=ns.new('ShaderNodeOutputWorld');ls.new(sky.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
 ld=bpy.data.lights.new('Afternoon sun','SUN');o=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(o);ld.energy=3.4;ld.color=(1,.96,.89);ld.angle=math.radians(1.6);o.rotation_euler=Vector((-.6,.7,-1)).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_end=1000;cam.data.clip_start=.02
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.5
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 return cam,ld,bg,sky
def shots(seed):
 d=dict(above=dict(location=(36,-44,31),target=(0,0,1.7),lens=42,aspect=1.5),
 driver=dict(location=(LANE,-31,1.18),target=(2.3,9,3.5),lens=42,aspect=1.5))
 if seed==201:
  z=ARM_Z+(POLE_X-LANE-.2735)*.03492
  d.update(
   hero=dict(location=(8.0,-23,1.80),target=(0,7.0,4.4),lens=40,aspect=1.6),
   head_lit=dict(location=(LANE+1.15,POLE_Y-3.5,7.05),target=(LANE,POLE_Y-.42,z-.05+GRADE),lens=60,aspect=1.2),
   head_dark=dict(location=(LANE+1.15,POLE_Y-3.5,7.05),target=(LANE,POLE_Y-.42,z-.05+GRADE),lens=60,aspect=1.2,dark=True),
   connection=dict(location=(POLE_X-1.4,POLE_Y-2.5,7.3),target=(POLE_X-.24,POLE_Y,ARM_Z+.15),lens=60,aspect=1.3),
   base=dict(location=(POLE_X+1.3,POLE_Y-1.7,1.25),target=(POLE_X,POLE_Y,.48),lens=57,aspect=1.3),
   pedestrian=dict(location=(FACE-2.0,CROSS+2.30,2.05),target=(FACE+1.65,CROSS+2.30,2.1),lens=45,aspect=.95),
   button=dict(location=(FACE+2.1,CROSS-.5,1.50),target=(FACE+1.65,CROSS+2.13,1.52),lens=70,aspect=1.2),
   cabinet_open=dict(location=(13.4,11.6,2.35),target=(10.7,15.7,1.13),lens=52,aspect=1.2,door=-95),
   cabinet=dict(location=(13.4,11.6,2.35),target=(10.7,15.7,1.13),lens=52,aspect=1.2),
   dusk=dict(location=(8.0,-23,1.80),target=(0,7,4.4),lens=40,aspect=1.6,dusk=True))
 if seed==204:
  d['span_hanger']=dict(location=(1.9,-2.1,8.0),target=(.581, .8435,7.30),lens=65,aspect=1.3)
 return d
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--seeds',default='201');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24);p.add_argument('--shots');p.add_argument('--camera-file',type=Path);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 for seed in map(int,a.seeds.split(',')):
  source=a.source.parent/f'Signals-{seed}.glb'
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
  setting.ground();setting.audit_ground();provenance=[] if a.camera_file else setting.context(seed);cam,sun,bg,sky=setup(a.samples)
  views=shots(seed)
  if a.camera_file:
   data=json.loads(a.camera_file.read_text());views={k:v['shot'] for k,v in data.items() if v.get('seed',201)==seed}
  if a.shots:views={k:v for k,v in views.items() if k in a.shots.split(',')}
  target=a.out if a.camera_file else a.out/str(seed);target.mkdir(parents=True,exist_ok=True)
  sc=bpy.context.scene
  for name,shot in views.items():
   old={}
   for ob in bpy.context.scene.objects:
    if ob.type=='MESH' and ob.get('signal_lens') and shot.get('dark'):
     old[ob]=list(ob.data.materials);ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(bpy.data.materials['SharedLens_Off'])
   # Reset the day shader and independently pose the real operating leaf.
   for link in list(bg.inputs[0].links):sc.world.node_tree.links.remove(link)
   sc.world.node_tree.links.new(sky.outputs[0],bg.inputs[0])
   door=bpy.data.objects.get('Controller__Door')
   if door:door.rotation_mode='XYZ';door.rotation_euler.z=math.radians(shot.get('door',0))
   if shot.get('dusk'):
    for link in list(bg.inputs[0].links):sc.world.node_tree.links.remove(link)
    bg.inputs[0].default_value=(.12,.19,.30,1)
    sun.energy=.06;bg.inputs[1].default_value=.5;sc.view_settings.exposure=1.4
   elif shot.get('overcast'):
    sun.energy=.0;bg.inputs[1].default_value=.20;sky.sun_elevation=math.radians(18);sc.view_settings.exposure=-.8
   else:
    sun.energy=3.4;bg.inputs[1].default_value=.24;sky.sun_elevation=math.radians(35);sc.view_settings.exposure=-.5
   cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot.get('lens',42)
   sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
   sc.render.filepath=str((target/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
   for ob,mats in old.items():ob.data.materials.clear();[ob.data.materials.append(m) for m in mats]
   recipe=hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('render.py','setting.py','plan.py'))).hexdigest()
   report=dict(recipe_sha256=recipe,width=a.width,samples=a.samples,checkpoint=True,source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=shot,context=provenance,engine='CYCLES')
   (target/(name+'.json')).write_text(json.dumps(report,indent=2))
   print('RENDERED',seed,name,flush=True)
if __name__=='__main__':main()
