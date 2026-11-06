"""Cycles form review from reimported checkpoint exports; no context exported."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import gpu,tiling
from geometry import palette
from graphics import generate
from street import build_street

def simple(name,col):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.8;return m

def setup(samples,engine='CYCLES'):
 sc=bpy.context.scene;sc.render.engine=engine
 if engine=='BLENDER_WORKBENCH':sc.display.shading.color_type='VERTEX';sc.display.shading.light='STUDIO';sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True
 if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=12
 sc.world=bpy.data.worlds.new('Procedural afternoon sky');sc.world.use_nodes=True;n=sc.world.node_tree.nodes;l=sc.world.node_tree.links;n.clear()
 sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(28);sky.sun_rotation=math.radians(235);sky.aerosol_density=.25
 bg=n.new('ShaderNodeBackground');bg.inputs[1].default_value=.10;out=n.new('ShaderNodeOutputWorld');l.new(sky.outputs[0],bg.inputs[0]);l.new(bg.outputs[0],out.inputs[0])
 sun=bpy.data.lights.new('Raking afternoon sun','SUN');sun.energy=3.0;sun.angle=math.radians(.8);sun.color=(1,.94,.84)
 o=bpy.data.objects.new(sun.name,sun);sc.collection.objects.link(o);o.rotation_euler=Vector((.7,.65,-.52)).to_track_quat('-Z','Y').to_euler()
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.45
 camera=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(camera);sc.camera=camera
 camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.clip_end=2000;camera.data.clip_start=.03
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
 from kit import model as G
 G.box('Presentation ground',(0,0,-.32),(2000,2000,.20),simple('Neutral grade',(.15,.16,.12)),0)
 return camera

def append_context(row,loc,yaw=0,scale=1):
 path=Path(row['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'];before=set(bpy.data.objects)
 with bpy.data.libraries.load(str(path.resolve()),link=False) as (src,dst):dst.objects=src.objects
 for ob in dst.objects:
  if ob:bpy.context.collection.objects.link(ob)
 obs=set(bpy.data.objects)-before;root=bpy.data.objects.new('Context_'+row['name'],None);bpy.context.collection.objects.link(root)
 for ob in obs:
  if ob.parent is None:ob.parent=root
 root.location=loc;root.rotation_euler.z=math.radians(yaw);root.scale=(scale,)*3
 for ob in obs:
  if row['name'] in ('pickup','crossover','hatchback') and ob.type=='MESH':
   for m in ob.data.materials:
    if m and m.use_nodes and m.name.startswith('Clay body'):
     tint={'pickup':(.09,.16,.19),'crossover':(.23,.25,.21),'hatchback':(.28,.07,.035)}[row['name']]
     m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*tint,1)
  if row['name']=='light' and ob.type=='MESH':
   for m in ob.data.materials:
    if m and m.use_nodes:
     for p in m.node_tree.nodes:
      if p.type=='BSDF_PRINCIPLED':p.inputs['Emission Strength'].default_value=0
 return list(obs)+[root]

def views(p):
 W=p['width'];H=max(l['height'] for l in p['lots']);D=max(l['depth'] for l in p['lots']);l=p['lots'][1];x=l['x'];h=l['height'];d=l['depth'];cm=next((v for v in p['lots'] if v['cornice']=='metal'),l);side_length=p['lots'][0]['depth']-p['lots'][0]['chamfer'];gy=p['lots'][0]['depth']-min(side_length*.50,side_length-14.0)
 return dict(
 hero=dict(location=(-W/2-11,-p['walk']-p['road_width']-p['walk']*.60,1.68),target=(-W/2+17,0,3.8),lens=35,aspect=1.8,context=True),
 across=dict(location=(0,-p['walk']-p['road_width']-p['walk']*.60,H/2),target=(0,0,H/2),lens=(p['walk']+p['road_width']+p['walk']*.60)*36/(W*1.14),aspect=3.5),
 above=dict(location=(-W*.85,-W*.82,48),target=(0,D*.35,1.8),lens=43,aspect=1.65),
 rear=dict(location=(W*.75,D+W*.80,32),target=(0,D*.67,4),lens=43,aspect=1.8),
 storefront=dict(location=(x+3.0,-8.0,2.15),target=(x,0,2.1),lens=42,aspect=1.4),
 window=dict(location=(x+.7,-5.0,l['floor_first']+1.5),target=(x-.3,0,l['floor_first']+1.7),lens=62,aspect=1.15),
 cornice=dict(location=(cm['x']+1.8,-5.4,cm['height']-.35),target=(cm['x'],0,cm['height']-.40),lens=50,aspect=1.5),
 corner=dict(location=(-W/2-5.5,-7.5,2.0),target=(-W/2+.9,1,2.5),lens=40,aspect=1.3),
 ghost=dict(location=(-W/2-14,gy+2.0,3.8),target=(-W/2,gy,3.3),lens=43,aspect=1.65),
 escape=dict(location=(x+2,d+12,4.0),target=(x,d+1,3.0),lens=40,aspect=1.35),
 gallery=dict(location=(x+4,-9,3),target=(x,-1.2,3.4),lens=43,aspect=1.55))

def render_block(region,out,width,samples,selected=None,camera_file=None,engine='CYCLES'):
 source=Path('build/blocks')/region/'block.glb';p=json.loads(source.with_suffix('.json').read_text());digest=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
 architecture=[o for o in bpy.context.scene.objects if o.type=='MESH']
 sheet,layout=generate(Path('build/signs'));root,street=build_street(p,palette(sheet));tiling.export(Path('export')/('DowntownStreet_'+region+'.glb'),[root]+list(root.children_recursive))
 camera=setup(samples,engine);shots=views(p)
 if camera_file:shots={k:v['shot'] for k,v in json.loads(camera_file.read_text()).items() if v.get('region',region)==region}
 names=selected.split(',') if selected else list(shots) if camera_file else (['hero','across','above','rear','storefront','window','cornice','corner','ghost','escape'] if region=='midwest' else ['across','above','rear']+(['gallery'] if region=='southern' else []))
 context=[];manifest=Path('build/context/manifest.json')
 if manifest.exists() and any(shots[n].get('context') for n in names):
  rows={r['name']:r for r in json.loads(manifest.read_text())};spots=street['parking']
  for i,k in enumerate([i for i in range(len(spots)) if i%2==0][:8]):
   s=spots[k];context+=append_context(rows[('pickup','crossover','hatchback')[i%3]],(s['x'],s['y'],-.1524),s['yaw'])
  for i,pos in enumerate(street['pits']):
   context+=append_context(rows['maple'],pos,25*i,.55);context+=append_context(rows['light'],(pos[0]+2.2,pos[1]-.35,0))
 out=Path(out)/region;out.mkdir(parents=True,exist_ok=True);report={}
 for view_index,name in enumerate(names):
  shot=shots[name]
  if context and not shot.get('context',False) and not any(shots[n].get('context',False) for n in names[view_index:]):
   for ob in context:bpy.data.objects.remove(ob,do_unlink=True)
   context=[]
   for datablocks in (bpy.data.meshes,bpy.data.materials,bpy.data.images):
    for item in list(datablocks):
     if item.users==0:datablocks.remove(item)
  for o in context:o.hide_render=not shot.get('context',False)
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.lens=shot.get('lens',45)
  sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.6));sc.render.resolution_percentage=100
  if name in ('across','above','rear'):
   from bpy_extras.object_utils import world_to_camera_view
   bounds=[o.matrix_world@Vector(c) for o in architecture for c in o.bound_box]
   target=Vector(shot['target'])
   for iteration in range(80):
    bpy.context.view_layer.update();uv=[world_to_camera_view(sc,camera,v) for v in bounds]
    if all(.05<=v.x<=.95 and .07<=v.y<=.93 and v.z>0 for v in uv):break
    camera.location=target+(camera.location-target)*1.035
   else:raise ValueError('Cannot frame the complete architecture')
   shot=dict(shot,location=list(camera.location),framing='actual imported bounds inside 5% horizontal / 7% vertical margins')
  sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
  if camera_file:
   import shutil
   raw=out.parent/'raw';raw.mkdir(exist_ok=True);shutil.copyfile(out/(name+'.png'),raw/(name+'.png'))
  report[name]=dict(source=str(source),sha256=digest,stage=p['stage'],engine=engine,camera=shot,street_triangles=street['triangles'],context=json.loads(manifest.read_text()) if shot.get('context') and manifest.exists() else [])
 old=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {};old.update(report);(out/'provenance.json').write_text(json.dumps(old,indent=2)+'\n');assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
 print('RENDERED',region,names,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--region');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--shots');p.add_argument('--camera-file',type=Path);p.add_argument('--engine',default='CYCLES');p.add_argument('--with-matches',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 for region in ([a.region] if a.region else ['midwest','western','northeast','southern']):render_block(region,a.out,a.width,a.samples,a.shots,a.camera_file,a.engine)

 if a.with_matches:
  assert not a.camera_file
  from kit.photo_match import compose
  calibration=Path('build/cameras.json')
  for region in ('midwest','northeast'):render_block(region,Path('renders/matches'),a.width,a.samples,None,calibration,a.engine)
  compose(calibration,'renders/matches/raw','renders/matches')
  Path('renders/matches/.stamp').touch()

 if not a.region and not a.shots and not a.camera_file:(a.out/'.stamp').touch()
