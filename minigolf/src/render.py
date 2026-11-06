"""Cycles checkpoint judgment from freshly imported external-image glTFs."""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
from kit.gpu import enable
import context
from plan import local,center,level

def world(sun=(.8,.2,.60),energy=3.4,sky_strength=.10):
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
 W,D=p['lot'];adv=p['kind']=='adventure';h=p['holes'][0];tee=h['tee'];cup=h['cup'];fx=next(q for q in p['holes'] if q['fixture']=='windmill');fcx,fcy=center(fx,.49);fcz=level(fx,fcx,.49)+.005;c=local(fx,fcx,fcy,fcz)
 def relative(pt,dx,dy,dz):return (pt[0]+dx,pt[1]+dy,pt[2]+dz)
 return {
 'ground':dict(location=(7.5,-12.5,1.65) if adv else (-15,-14,1.65),target=(0,9,1.65) if adv else (-4,9,1.65),lens=40,aspect=1.8,shift_y=-.035),
 'above':dict(location=(-58,-66,71) if adv else (-45,-55,61),target=(0,-2,0),lens=43,aspect=1.5),
 'hero':dict(location=(-6.4,15.4,2.275),target=(-1.0,-14.0,1.65),lens=40,aspect=1.9,shift_y=-.06),
 'tee':dict(location=relative(tee,-2.1,-2.7,1.85),target=relative(tee,-.65,.0,.65),lens=46,aspect=1.45),
 'cup':dict(location=relative(cup,.33,-.45,.39),target=relative(cup,.04,.03,.04),lens=55,aspect=1.35),
 'border':dict(location=relative(tee,-2.1,.45,.56),target=relative(tee,-1.0,.75,.05),lens=55,aspect=1.55),
 'waterfall':dict(location=(-1.2,5.4,1.65),target=(2.9,9.7,.62),lens=48,aspect=1.6),
 'fixture':dict(location=local(fx,fcx-3.5,fcy-8.5,fcz+1.65),target=relative(c,0,0,1.65),lens=48,aspect=1.35,human=local(fx,fcx+2.1,fcy,fcz-.13)),
 'bridge':dict(location=(-4.6,-7,1.65),target=(0,-4,.5),lens=42,aspect=1.6),
 'clubhouse':dict(location=(-7,-14,1.65),target=(0,p['clubhouse'][1],1.65),lens=45,aspect=1.6),
 }

def scene(seed):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 source=Path(f'export/Minigolf-{seed}.gltf');p=json.loads(source.with_suffix('.json').read_text())['plan']
 bpy.ops.import_scene.gltf(filepath=str(source.resolve()));ctx=context.make(p)
 return source,p,ctx

def render_one(name,shot,source,p,ctx,args):
 sc=bpy.context.scene;human_objects=[];human_proof=None
 if shot.get('human'):
  from kit.studio import human
  human_objects=human();offset=Vector(shot['human'])+Vector((1.03,-.24,0))
  for ob in human_objects:ob.location+=offset
  bpy.context.view_layer.update();q=[ob.matrix_world@v.co for ob in human_objects if ob.type=='MESH' for v in ob.data.vertices];height=max(v.z for v in q)-min(v.z for v in q);assert abs(height-1.8)<1e-5;human_proof=dict(measured_height_m=height,feet=shot['human'])
 sc.render.engine='CYCLES';enable();sc.cycles.samples=args.samples;sc.cycles.use_denoising=True;sc.cycles.seed=17
 world(shot.get('sun',(.8,.2,.60)),shot.get('sun_energy',3.4),shot.get('sky_strength',.10));cam=camera(shot)
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=shot.get('exposure',-.45)
 sc.render.resolution_x=args.width;sc.render.resolution_y=round(args.width/shot.get('aspect',1.6));sc.render.resolution_percentage=100
 sc.render.image_settings.file_format='PNG';out=Path(args.out)/(name+'.png');out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
 meta=dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),engine='CYCLES',camera=shot,context=ctx,samples=args.samples,scale_silhouette=human_proof)
 out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.data.objects.remove(cam,do_unlink=True)
 for ob in human_objects:bpy.data.objects.remove(ob,do_unlink=True)
 for ob in list(sc.objects):
  if ob.type=='LIGHT':bpy.data.objects.remove(ob,do_unlink=True)

def main(args):
 chosen=args.shots.split(',') if args.shots else None
 for seed,kind in ((71,'classic'),(92,'adventure')):
  requested=['ground','above']+(['hero','tee','cup','border','waterfall','fixture','bridge','clubhouse'] if kind=='adventure' else [])
  if chosen:requested=[n for n in requested if n in chosen or kind+'-'+n in chosen]
  if not requested:continue
  source,p,ctx=scene(seed)
  for name in requested:render_one((kind+'-'+name) if name in ('ground','above') else name,views(p)[name],source,p,ctx,args)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source');parser.add_argument('--out',default='renders/checkpoint');parser.add_argument('--width',type=int,default=1440);parser.add_argument('--samples',type=int,default=40);parser.add_argument('--shots');a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);main(a)
