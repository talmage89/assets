"""Matched-view plain-horizon and stripe diagnostics of the actual source mesh.

The plain images retain source paint/wear and remove reflection proxies. The
stripe image substitutes only paint with a smooth diagnostic conductor.
"""
import argparse,hashlib,json,math,runpy,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
from render_checkpoint import stripe_world
import pickup_spec as S


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 cameras=json.loads(Path('build/used-cameras.json').read_text());config=runpy.run_path(str(Path(__file__).with_name('config.py')));metadata={}
 for name,shot in [('plain_aged_rear',cameras['aged_rear']['shot']),('plain_used_rear',cameras['used_rear']['shot']),('stripes_side',config['SHOTS']['stripes_side'])]:
  bpy.ops.wm.open_mainfile(filepath=str(source));sc=bpy.context.scene;camera=studio.add_studio(scale=3)
  if name.startswith('plain_'):
   from lighting import outdoor,conditions
   outdoor();conditions(name.removeprefix('plain_'))
   for ob in sc.objects:
    if ob.name.startswith('Comparison parked') or ob.name.startswith('Comparison irregular foliage'):ob.hide_render=True
   paint='Graphite' if 'aged_' in name else 'Carbon'
   for m in bpy.data.materials:
    if m.get('vehicle_paint'):
     m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*S.COLORS[paint],1)
     if 'Paint metallic' in m.node_tree.nodes:m.node_tree.nodes['Paint metallic'].outputs[0].default_value=S.PAINT_METAL[paint]
  else:
   stripe_world(sc)
   mat=studio.studio_mat('Smooth stripe diagnostic',(.32,.32,.32),.075);mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.8
   for ob in sc.objects:
    if ob.type=='MESH':
     for i,m in enumerate(ob.data.materials):
      if m.get('vehicle_paint'):ob.data.materials[i]=mat
  for ob in sc.objects:
   if ob.get('studio'):
    if name.startswith('stripes') or not ob.name.startswith('Comparison'):ob.hide_render=True
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
  camera.data.type='PERSP';camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.lens=shot['lens'];camera.data.clip_end=200
  sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=10;sc.cycles.transmission_bounces=8
  sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot['aspect']);sc.render.resolution_percentage=100;sc.render.film_transparent=True
  sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=shot.get('exposure',-.2)
  sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
  metadata[name]=dict(shot,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),mode='source paint with sky/ground only' if name.startswith('plain') else 'smooth paint replacement; procedural stripe dome')
 (out/'diagnostics.json').write_text(json.dumps(metadata,indent=2))

if __name__=='__main__':main()
