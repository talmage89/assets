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
from town import setting,light_rooms
from delivery import bundle_hash
CONTEXT_TEMPLATES={}

def simple(name,col):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.8;return m

def setup(samples,engine='CYCLES'):
 sc=bpy.context.scene;sc.render.engine=engine
 if engine=='BLENDER_WORKBENCH':sc.display.shading.color_type='VERTEX';sc.display.shading.light='STUDIO';sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True
 if engine=='BLENDER_EEVEE':
  sc.eevee.use_raytracing=True;sc.eevee.use_fast_gi=True;sc.eevee.taa_render_samples=64
  for m in bpy.data.materials:
   if m.use_nodes and any(n.type=='BSDF_PRINCIPLED' and (n.inputs['Transmission Weight'].is_linked or n.inputs['Transmission Weight'].default_value>0) for n in m.node_tree.nodes):m.use_raytrace_refraction=True;m.use_screen_refraction=True
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
 G.box('Presentation ground',(0,0,-.32),(2000,2000,.20),simple('Distant town ground',(.085,.12,.050)),0)
 return camera

def source_materials():
 # Same original physical source fields used by the kit baker, before its
 # normal/color filtering. Reference images are never loaded as materials.
 fields=json.loads(Path('build/procedural/fields.json').read_text())
 for mat in bpy.data.materials:
  if not mat.use_nodes:continue
  key=next((k for k in fields if ('Downtown'+k) in mat.name),None)
  if not key:continue
  ns=mat.node_tree.nodes;ls=mat.node_tree.links
  for n in ns:
   if n.type=='TEX_IMAGE' and n.image:
    channel=next((c for c in ('BaseColor','ORM') if c in n.image.name),None)
    if channel:
     n.image=bpy.data.images.load(str((Path('build/procedural')/('T_Downtown'+key+'_'+channel+'.png')).resolve()),check_existing=True)
     n.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
  tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str((Path('build/procedural')/('T_Downtown'+key+'_Height.png')).resolve()),check_existing=True);tex.image.colorspace_settings.name='Non-Color'
  bump=ns.new('ShaderNodeBump');bump.inputs['Distance'].default_value=fields[key]['height_distance_m'];ls.new(tex.outputs['Color'],bump.inputs['Height'])
  p=next(n for n in ns if n.type=='BSDF_PRINCIPLED');ls.new(bump.outputs['Normal'],p.inputs['Normal'])

def apply_light(shot,p):
 sc=bpy.context.scene;dusk=shot.get('dusk',False)
 sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND')
 sky.sun_elevation=math.radians(3 if dusk else shot.get('sun_elevation',28));
 balance=sc.world.node_tree.nodes.get('Dusk sky balance')
 if balance is None:
  balance=sc.world.node_tree.nodes.new('ShaderNodeMixRGB');balance.name='Dusk sky balance';balance.blend_type='MULTIPLY';balance.inputs[0].default_value=1
  sc.world.node_tree.links.new(sky.outputs[0],balance.inputs[1]);sc.world.node_tree.links.new(balance.outputs[0],bg.inputs[0])
 balance.inputs[2].default_value=(.35,.55,1.3,1) if dusk else (1,1,1,1)
 overcast=sc.world.node_tree.nodes.get('Neutral overcast')
 if overcast is None:
  overcast=sc.world.node_tree.nodes.new('ShaderNodeMixRGB');overcast.name='Neutral overcast'
  sc.world.node_tree.links.new(balance.outputs[0],overcast.inputs[1]);sc.world.node_tree.links.new(overcast.outputs[0],bg.inputs[0])
 overcast.inputs[0].default_value=1 if shot.get('overcast') else 0;overcast.inputs[2].default_value=(.8,.8,.8,1)
 bg.inputs[1].default_value=.13 if dusk else shot.get('sky_strength',.16)
 sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN');sun.data.energy=.06 if dusk else shot.get('sun_energy',3)
 sun.rotation_euler=Vector(shot.get('sun_direction',(.7,.65,-.52))).to_track_quat('-Z','Y').to_euler()
 sc.view_settings.exposure=shot.get('exposure',.40 if dusk else -.35)
 for o in list(sc.objects):
  if o.type=='LIGHT' and o.name.startswith(('Shop fixture','Street lamp pool')):bpy.data.objects.remove(o,do_unlink=True)
 light_rooms(p,dusk)
 if dusk:
  bpy.context.view_layer.update()
  for i,emitter in enumerate([o for o in sc.objects if o.get('socket_kind')=='engine_light']):
   l=bpy.data.lights.new('Street lamp pool '+str(i),'AREA');l.energy=650;l.color=(1,.74,.46);l.size=.30
   o=bpy.data.objects.new(l.name,l);sc.collection.objects.link(o);o.location=emitter.matrix_world.translation
 for m in bpy.data.materials:
  if m.use_nodes and ('LED phosphor' in m.name or m.name.startswith(('Lamp','LED','Diffuser'))):
   q=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
   if q:q.inputs['Emission Strength'].default_value=100 if dusk else 0

def append_context(row,loc,yaw=0,scale=1):
 path=Path(row['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'];before=set(bpy.data.objects)
 if str(path) in CONTEXT_TEMPLATES:
  old=CONTEXT_TEMPLATES[str(path)];mapping={o:o.copy() for o in old}
  for a,o in mapping.items():
   bpy.context.collection.objects.link(o);o.parent=mapping.get(a.parent)
  obs=set(mapping.values())
 else:
  with bpy.data.libraries.load(str(path.resolve()),link=False) as (src,dst):dst.objects=src.objects
  for ob in dst.objects:
   if ob:bpy.context.collection.objects.link(ob)
  obs=set(bpy.data.objects)-before;CONTEXT_TEMPLATES[str(path)]=list(obs)
 root=bpy.data.objects.new('Context_'+row['name'],None);bpy.context.collection.objects.link(root)
 for ob in obs:
  if ob.parent is None:ob.parent=root
 root.location=loc;root.rotation_euler.z=math.radians(yaw);root.scale=(scale,)*3
 for ob in obs:
  ob['presentation_side']='opposite' if loc[1]<-12 else 'near'
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
 hero=dict(location=(-W/2-8,-p['walk']-p['road_width']-p['walk']*.60,1.60),target=(W*.25,-p['walk']-p['road_width']*.05,3.9),lens=38,aspect=1.8,context=True),
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

def render_block(region,out,width,samples,selected=None,camera_file=None,engine='CYCLES',source_look=False):
 source=Path('build/blocks')/region/'block.glb';p=json.loads(source.with_suffix('.json').read_text());digest=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.ops.wm.read_factory_settings(use_empty=True);CONTEXT_TEMPLATES.clear()
 for row in p['buildings']:
  before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(Path(row['source']).resolve()))
  for o in set(bpy.data.objects)-before:
   if o.parent is None:o.location=row['position']
 if source_look:source_materials()
 architecture=[o for o in bpy.context.scene.objects if o.type=='MESH']
 sheet,layout=generate(Path('build/signs'));root,street=build_street(p,palette(sheet))
 camera=setup(samples,engine);shots=views(p)
 from kit.studio import human
 silhouette=human();offset=Vector((p['lots'][1]['x']+1.03,-1.04,0))
 for o in silhouette:o.location+=offset;o.hide_render=True
 cm=next(v for v in p['lots'] if v['cornice']=='metal')
 shots['cornice_profile']=dict(location=(cm['x']+3.8,-5.4,cm['height']-1.3),target=(cm['x']-.55,0,cm['height']-.45),lens=42,aspect=1.5)
 if region=='northeast':
  hl=p['lots'][3];hx=hl['x']-hl['width']/2+hl['width']/8;hz=hl['floor_first']+hl['upper']+.65+1.15
  shots['hood']=dict(location=(hx+2.2,-4.2,hz-.10),target=(hx,0,hz),lens=45,aspect=.95)
 shots['scale']=dict(location=(p['lots'][1]['x']+4,-20,1.60),target=(p['lots'][1]['x'],0,4.2),lens=50,aspect=1.35)
 for n in ('across','above','rear'):shots[n]['context']=True
 shots['dusk']=dict(shots['hero'],dusk=True,location=(-p['width']/2-3,-p['walk']-p['road_width']-1,1.60),target=(-p['width']/2+20,0,3.8),lens=35)
 shots['awning']=dict(shots['storefront'],location=[p['lots'][1]['x']+1.2,-4.4,p['lots'][1]['floor_first']-.80],target=[p['lots'][1]['x'],0,p['lots'][1]['floor_first']-.95],lens=38,aspect=1.6)
 if camera_file:shots={k:v['shot'] for k,v in json.loads(camera_file.read_text()).items() if v.get('region',region)==region}
 names=selected.split(',') if selected else list(shots) if camera_file else (['hero','dusk','across','above','rear','storefront','window','cornice','corner','ghost','escape','awning','scale','cornice_profile'] if region=='midwest' else ['across','above','rear']+(['storefront','hood'] if region=='northeast' else [])+(['gallery'] if region=='southern' else []))
 context=[];manifest=Path('build/context/manifest.json')
 if manifest.exists():
  rows={r['name']:r for r in json.loads(manifest.read_text())}
  context=setting(p,palette(sheet),append_context,rows,street)
 out=Path(out)/region;out.mkdir(parents=True,exist_ok=True);report={}
 for view_index,name in enumerate(names):
  shot=shots[name]
  for o in silhouette:o.hide_render=name!='scale'
  apply_light(shot,p)
  for o in context:
   o.hide_render=False
   o.visible_camera=shot.get('context',False) and not (name=='across' and (o.get('town_group')=='Opposite block' or o.get('presentation_side')=='opposite'))
   o.visible_shadow=shot.get('context',False)
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
  report[name]=dict(source=str(source),sha256=digest,source_look=source_look,stage=('Original 4096 material fields on exported mesh' if source_look else p['stage']),engine=engine,camera=shot,street_triangles=street['triangles'],bundles=[dict(path=r['source'],sha256=bundle_hash(Path(r['source']))) for r in p['buildings']],context=json.loads(manifest.read_text()) if context and manifest.exists() else [],context_visibility=dict(camera=shot.get('context',False),shadow=shot.get('context',False),glossy=True,opposite_foreground_cutaway=name=='across'),lighting=dict(exposure=sc.view_settings.exposure,sky_strength=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value,sun_energy=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN').data.energy))
 old=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {};old.update(report);(out/'provenance.json').write_text(json.dumps(old,indent=2)+'\n');assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
 print('RENDERED',region,names,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--region');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--shots');p.add_argument('--camera-file',type=Path);p.add_argument('--engine',default='CYCLES');p.add_argument('--source-look',action='store_true');p.add_argument('--with-matches',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 regions=[a.region] if a.region else ['midwest','western','northeast','southern']
 if a.camera_file:
  requested={m['region'] for m in json.loads(a.camera_file.read_text()).values()}
  regions=[r for r in regions if r in requested]
 for region in regions:render_block(region,a.out,a.width,a.samples,a.shots,a.camera_file,a.engine,a.source_look)

 if a.with_matches:
  assert not a.camera_file
  from kit.photo_match import compose
  calibration=Path('build/cameras.json')
  for region in ('midwest','northeast'):render_block(region,Path('renders/matches'),a.width,a.samples,None,calibration,a.engine)
  compose(calibration,'renders/matches/raw','renders/matches')
  Path('renders/matches/.stamp').touch()

 if not a.region and not a.shots and not a.camera_file:(a.out/'.stamp').touch()
