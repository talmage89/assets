"""Cycles evidence from exported shared-image glTF parts; source pairs are explicit."""
import argparse,sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import gpu
from plan import *
from layout import SITES
from geometry import M
import setting
def aim_sun(sun,sky,direction):
 d=Vector(direction).normalized();bpy.data.objects[sun.name].rotation_euler=d.to_track_quat('-Z','Y').to_euler()
 sky.sun_elevation=math.asin(-d.z);sky.sun_rotation=math.atan2(-d.y,-d.x)

def clear_photo_view(camera,points):
 """Hide only foreground presentation trees/lights that conceal measured parts.
 Shipped signal geometry is never filtered. Omissions are recorded per view.
 """
 sc=bpy.context.scene;hidden={};camera=Vector(camera);target=sum((Vector(p) for p in points),Vector())/len(points);distance=(target-camera).length
 for root in list(sc.objects):
  if root.parent is None and root.name.startswith('StreetLamp') and (root.location-camera).length<distance:
   for ob in [root,*root.children_recursive]:hidden[ob]=ob.hide_viewport;ob.hide_viewport=True;ob.hide_render=True
 for _ in range(20):
  bpy.context.view_layer.update();changed=False
  for point in points:
   delta=Vector(point)-camera;hit=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),camera,delta.normalized(),distance=delta.length-.02)
   if not hit[0]:continue
   ob=hit[4];root=ob
   while root.parent:root=root.parent
   if root.name.startswith(('StreetTree','House','CornerGasStation','WaitingVehicle')):
    for child in [root,*root.children_recursive]:hidden[child]=child.hide_viewport;child.hide_viewport=True;child.hide_render=True
    changed=True
  if not changed:break
 return hidden

def setup(samples):
 sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=6
 sc.world=bpy.data.worlds.new('Procedural sky');sc.world.use_nodes=True
 ns=sc.world.node_tree.nodes;ls=sc.world.node_tree.links;ns.clear()
 sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(145);sky.sun_disc=False;sky.aerosol_density=.45
 bg=ns.new('ShaderNodeBackground');bg.inputs[1].default_value=.12
 out=ns.new('ShaderNodeOutputWorld');ls.new(sky.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
 ld=bpy.data.lights.new('Afternoon sun','SUN');o=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(o);ld.energy=3.4;ld.color=(1,.96,.89);ld.angle=math.radians(1.6);aim_sun(ld,sky,(-.75,.95,-.65))
 cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_end=1000;cam.data.clip_start=.02
 sc.view_settings.view_transform='Khronos PBR Neutral';sc.view_settings.look='None';sc.view_settings.exposure=-.5
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 return cam,ld,bg,sky
def shots(seed):
 site=SITES[seed];px,py,pz=site.pole(0);dist=site.face(0)+1.02-site.positions(0)[0]
 hz=GRADE+ARM_Z+(dist-.2735)*.03492+.45
 h=(site.positions(0)[0],py-.42,hz-.75)
 d=dict(above=dict(location=(48,-61,53),target=(0,0,0),lens=42,aspect=1.5),
 driver=dict(location=(site.half(0)-LANE/2,-site.stop(2)-18,1.18),target=(1,site.core(0),4.4),lens=42,aspect=1.5))
 if seed==201:
  cp=site.cabinet()
  d.update(
   hero=dict(location=(-13.0,-7.0,1.7524),target=(3,site.core(0)-1,4.0),lens=40,aspect=1.5),
   head_lit=dict(location=(h[0]+1.05,h[1]-3.4,h[2]+.7),target=h,lens=60,aspect=1.2),
   head_dark=dict(location=(h[0]+1.05,h[1]-3.4,h[2]+.7),target=h,lens=60,aspect=1.2,dark=True),
   connection=dict(location=(px-1.4,py-2.5,7.3),target=(px-.24,py,ARM_Z+.15),lens=60,aspect=1.3),
   base=dict(location=(px+1.3,py-1.7,1.25),target=(px,py,.48),lens=57,aspect=1.3),
   pedestrian=dict(location=(site.face(0)-2,site.core(0)+3.824,2.05),target=(site.face(0)+1.65,site.core(0)+3.824,2.1),lens=45,aspect=.95),
   button=dict(location=(site.face(0)+2.1,site.core(0)+1.024,1.5),target=(site.face(0)+1.65,site.core(0)+3.654,1.52),lens=70,aspect=1.2),
   cabinet_open=dict(location=(cp[0]+2.9,cp[1]-4.2,2.35),target=(cp[0]+.2,cp[1]-.1,1.13),lens=52,aspect=1.2,door=-95),
   cabinet=dict(location=(cp[0]+2.9,cp[1]-4.2,2.35),target=(cp[0]+.2,cp[1]-.1,1.13),lens=52,aspect=1.2),
   dusk=dict(location=(-13.0,-7.0,1.7524),target=(3,site.core(0)-1,4.0),lens=45,aspect=1.5,dusk=True))
 if seed==204:d['span_hanger']=dict(location=(1.9,-2.1,8),target=(.581,.8435,7.3),lens=65,aspect=1.3)
 return d
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--seeds',default='201');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24);p.add_argument('--shots');p.add_argument('--camera-file',type=Path);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 for seed in map(int,a.seeds.split(',')):
  source=a.source.parent/('Signals-'+str(seed)+a.source.suffix)
  bpy.ops.wm.read_factory_settings(use_empty=True)
  if source.suffix=='.blend':
   bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
   for material in bpy.data.materials:
    if not material.use_nodes:continue
    for node in material.node_tree.nodes:
     if node.type!='TEX_IMAGE' or not node.image:continue
     name=Path(node.image.filepath).name
     if name in ('T_Signals_BaseColor.png','T_Signals_ORM.png','T_Signals_Normal.png'):
      folder=Path('textures/bake') if 'Normal' in name else Path('build/procedural');node.image=bpy.data.images.load(str((folder/name).resolve()),check_existing=True)
  else:bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
  setting.ground(seed);setting.audit_ground(seed);provenance=[]
  cam,sun,bg,sky=setup(a.samples)
  views=shots(seed)
  if a.camera_file:
   data=json.loads(a.camera_file.read_text());views={k:v['shot'] for k,v in data.items() if v.get('seed',201)==seed}
  if a.shots:views={k:v for k,v in views.items() if k in a.shots.split(',')}
  if a.camera_file or any(n in views for n in ('above','driver','hero','dusk')):provenance=setting.context(seed)
  target=a.out if a.camera_file else a.out/str(seed);target.mkdir(parents=True,exist_ok=True)
  sc=bpy.context.scene
  for name,shot in views.items():
   old={};omitted={}
   if shot.get('equipment_roots'):
    installation=bpy.data.objects.get('Signals_'+str(seed))
    for rt in list(installation.children):
     if rt.name in shot['equipment_roots']:continue
     for ob in [rt,*rt.children_recursive]:omitted[ob]=ob.hide_viewport;ob.hide_viewport=True;ob.hide_render=True
   for ob in bpy.context.scene.objects:
    if ob.type=='MESH' and ob.get('signal_lens') and (shot.get('dark') or shot.get('phase') and ob.get('signal_kind') not in ('hand','walk','countdown')):
     old[ob]=list(ob.data.materials);ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(bpy.data.materials['SharedLens_Lit' if shot.get('phase') and ob.get('signal_kind') in ('red','red_arrow') else 'SharedLens_Off'])
   # Reset the day shader and independently pose the real operating leaf.
   for link in list(bg.inputs[0].links):sc.world.node_tree.links.remove(link)
   sc.world.node_tree.links.new(sky.outputs[0],bg.inputs[0])
   door=bpy.data.objects.get('Controller__Door')
   if door:door.rotation_mode='XYZ';door.rotation_euler.z=math.radians(shot.get('door',0))
   if shot.get('dusk'):
    for link in list(bg.inputs[0].links):sc.world.node_tree.links.remove(link)
    bg.inputs[0].default_value=(.12,.19,.30,1)
    sun.energy=.015;bg.inputs[1].default_value=.65;sc.view_settings.exposure=.6
    for mat in bpy.data.materials:
     if not mat.use_nodes:continue
     p=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
     if p and mat.name.startswith('HouseGlass'):
      p.inputs['Emission Color'].default_value=(1,.58,.24,1);p.inputs['Emission Strength'].default_value=.28
    for ob in list(bpy.context.scene.objects):
     if ob.parent is None and ob.name.startswith('StreetLamp'):
      ld=bpy.data.lights.new(ob.name+' light','AREA');lo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(lo);lo.location=ob.location+Vector((0,0,7.7));ld.energy=125;ld.shape='DISK';ld.size=.4;ld.color=(1,.70,.43)
   elif shot.get('overcast'):
    sun.energy=.0;bg.inputs[1].default_value=.20;sky.sun_elevation=math.radians(18);sc.view_settings.exposure=-.8
   else:
    sun.energy=3.4;bg.inputs[1].default_value=.12;aim_sun(sun,sky,(-.75,.95,-.65));sc.view_settings.exposure=-.5
   if shot.get('sun_direction'):
    sun.energy=shot.get('sun_energy',3.4);sun.color=(1,.97,.91);aim_sun(sun,sky,shot['sun_direction']);bg.inputs[1].default_value=shot.get('sky_strength',.24);sc.view_settings.exposure=shot.get('exposure',-.5)
   cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot.get('lens',42)
   render_width=max(a.width,data[name]['crop'][2]-data[name]['crop'][0]) if a.camera_file else a.width
   sc.render.resolution_x=render_width;sc.render.resolution_y=round(render_width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
   hidden=clear_photo_view(cam.location,data[name]['landmarks_world_m']) if a.camera_file else {}
   hidden_names=[ob.name for ob in hidden if ob.parent is None]
   sc.render.filepath=str((target/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
   for ob,previous in hidden.items():ob.hide_viewport=previous;ob.hide_render=previous
   omitted_names=[ob.name for ob in omitted if ob.parent==installation] if omitted else []
   for ob,previous in omitted.items():ob.hide_viewport=previous;ob.hide_render=previous
   for ob,mats in old.items():ob.data.materials.clear();[ob.data.materials.append(m) for m in mats]
   recipe=hashlib.sha256(b''.join((Path(__file__).parent/n).read_bytes() for n in ('render.py','setting.py','plan.py'))).hexdigest()
   eye_surface=None
   ok,hit,normal,index,ob,_=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((cam.location.x,cam.location.y,cam.location.z-.01)),Vector((0,0,-1)))
   if ok:eye_surface=dict(mesh=ob.name,height_m=hit.z,eye_height_m=cam.location.z-hit.z)
   report=dict(presentation_omitted_equipment=omitted_names,presentation_hidden_context=hidden_names,eye_surface=eye_surface,recipe_sha256=recipe,width=sc.render.resolution_x,samples=a.samples,checkpoint=True,source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=shot,context=provenance,engine='CYCLES')
   if source.suffix=='.gltf':
    from deliver import bundle
    report['bundle_sha256']=bundle(source)
   (target/(name+'.json')).write_text(json.dumps(report,indent=2))
   print('RENDERED',seed,name,flush=True)
if __name__=='__main__':main()
