"""Cycles checkpoint from fresh imported GLB/glTF, with dependency provenance.

Shared PBR maps and their native emission stay intact in day and blue hour;
own-library context remains presentation only and is never re-exported.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from mathutils import Vector,Matrix
from kit import gpu
from geometry import palette,root,box,M
from plan import BRANDS,rotate,PROOF_SEEDS
from siteworks import context_roads
from ground_adapter import FLOW
from context import bundle,recipe

def sha(p):return bundle(Path(p).resolve())['sha256'] if Path(p).suffix=='.gltf' else hashlib.sha256(Path(p).read_bytes()).hexdigest()


def setup(samples,engine='CYCLES'):
 sc=bpy.context.scene;sc.render.engine=engine
 if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
 if engine=='BLENDER_EEVEE':
  sc.eevee.use_raytracing=True;sc.eevee.ray_tracing_options.resolution_scale='1'
  for mat in bpy.data.materials:
   bs=mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
   if bs and bs.inputs['Transmission Weight'].default_value>0:
    mat.use_raytrace_refraction=True;mat.thickness_mode='SLAB'
    val=mat.node_tree.nodes.new('ShaderNodeValue');val.outputs[0].default_value=.004
    out=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL');mat.node_tree.links.new(val.outputs[0],out.inputs['Thickness'])
 sc.world=bpy.data.worlds.new('Original sky');sc.world.use_nodes=True
 ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links;ns.clear()
 sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(220);sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=.3
 saturation=ns.new('ShaderNodeHueSaturation');saturation.name='Sky chroma';saturation.inputs['Saturation'].default_value=1
 ls.new(sky.outputs[0],saturation.inputs['Color'])
 bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.025
 mix=ns.new('ShaderNodeMixRGB');mix.name='Ambient balance';mix.inputs[0].default_value=0;mix.inputs[2].default_value=(1,1,1,1)
 out=ns.new('ShaderNodeOutputWorld');ls.new(saturation.outputs[0],mix.inputs[1]);ls.new(mix.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
 ld=bpy.data.lights.new('Sun','SUN');ob=bpy.data.objects.new('Sun',ld);sc.collection.objects.link(ob)
 ld.energy=6;ld.angle=math.radians(.65);ld.color=(1,.97,.93)
 ob.rotation_euler=Vector((.5,.7,-1)).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(cam);sc.camera=cam
 cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_start=.025;cam.data.clip_end=4000
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.25
 sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=6500
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 return cam


def views(p):
 W,D=p['lot'];b=p['building'];c=p['canopy'];x,y=p['islands'][0]['center'];u,v=rotate((0,-.96),c['angle']);x+=u;y+=v
 # Authored local camera positions rotate with the corner, all street eyes 1.68m.
 shots=dict(
 hero=dict(location=(-W/2-24,-D/2-14.35,FLOW+.16764+1.60),target=(0,-3,FLOW+.16764+1.60),lens=40,aspect=2.65,shift_y=.025),
 street=dict(location=(-W/2-14.35,-D/2-24,FLOW+.16764+1.60),target=(0,-2,FLOW+.16764+1.60),lens=40,aspect=2.65,shift_y=.025),
 above=dict(location=(-W*.73,-D*.93,46),target=(0,-1,0),lens=35,aspect=1.42),
 dispenser=dict(location=(x+3.7,y-3.0,1.75),target=(x,y,1.36),lens=60,aspect=1.25),
 canopy=dict(location=(-c['width']/2-1,c['center'][1]-7.8,2.1),target=(-c['width']/2+2,c['center'][1]-.5,4.20),lens=45,aspect=1.45),
 column=dict(location=(p['islands'][0]['center'][0]+2.8,p['islands'][0]['center'][1]-2.0,1.70),target=(p['islands'][0]['center'][0],p['islands'][0]['center'][1]+.92,1.43),lens=48,aspect=1.25),
 entry=dict(location=(4.5,b['front']-8,1.70),target=(0,b['front'],1.65),lens=44,aspect=1.5),
 sign=dict(location=(p['sign_center'][0]+5,p['sign_center'][1]-8,1.68),target=(*p['sign_center'],2.25 if p['sign']=='monument' else 3.55),lens=48,aspect=1.25),
 rear=dict(location=(W/2+6,D/2+10,6.0),target=(2,12,2),lens=40,aspect=1.6),
 services=dict(location=(b['width']/2+5,b['front']+b['depth']*.20-3,2.0),target=(b['width']/2,b['front']+b['depth']*.20+1.9,1.7),lens=50,aspect=1.5),
 asphalt=dict(location=(x+4,y-4,3.1),target=(x+2.0,y-.2,.08),lens=48,aspect=1.5),
 landscape=dict(location=(W/2-4,D/2-8,1.5),target=(W/2-.65,D/2-3,.45),lens=50,aspect=1.5),
 dusk=dict(location=(-W/2-24,-D/2-14.35,1.60),target=(0,-3,1.60),lens=40,aspect=2.65,shift_y=.025,dusk=True,sky_strength=.4,sky_saturation=1,sun_elevation=-3,sun_energy=0,exposure=2.2),
 motion=dict(location=(3,b['front']-6,1.7),target=(0,b['front']+.2,1.55),lens=43,aspect=1.4),
 )
 result={k:{**v,'location':rotate(v['location'],p['yaw']),'target':rotate(v['target'],p['yaw'])} for k,v in shots.items()}
 # Common geographic overhead makes the four real corner orientations visible.
 result['above']=shots['above']
 result.update({k:dict(location=rotate(loc,p['yaw']),target=rotate((0,0,3.4),p['yaw']),ortho=max(W,D)+10,lens=45,aspect=5.2) for k,loc in (('front',(0,-90,3.4)),('back',(0,90,3.4)),('side',(90,0,3.4)))})
 result['top']=dict(location=(0,.001,100),target=(0,0,0),ortho=max(W,D)+11,aspect=1)
 result['scale']=dict(location=rotate((x+8,y-11,2.0),p['yaw']),target=rotate((x,y+1,2.0),p['yaw']),lens=38,aspect=1.65,human=True)
 # The hero light crosses the view: lit storefront, shaded side, and a
 # readable canopy shadow across its slab. Accepted detail/dusk recipes stay.
 for name in ('hero','street','above','scale','top'):
  result[name].update(sun_direction=rotate((-1.0,.30,-.75),p['yaw']),sun_energy=6.0,sky_strength=.035,exposure=.25)
 return result


def load_context(path,pivot):
 before=set(bpy.context.scene.objects)
 bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
 added=set(bpy.context.scene.objects)-before
 rt=root('CONTEXT_'+path.stem,pivot,kind='CONTEXT')
 for ob in added:
  if ob.parent not in added:ob.parent=rt
 return rt,added


def context(p):
 repo=HERE.parents[1];paths=[repo/'houses/export/HearthfieldSplit-51.gltf',repo/'cars/export/AlderC150.glb']
 for path in paths:
  if not path.exists():raise RuntimeError('Build same-worktree context first: '+str(path.relative_to(repo)))
 # A same-scale architectural comparison, parked pickup in front of store.
 house,obs=load_context(paths[0],(38,9,0))
 # Presentation grade must not bury the exported split's sunken driveway.
 # Cut an opening from its measured plan metadata; never edit the house mesh.
 from siteworks import flat
 drive=json.loads(paths[0].with_suffix('.json').read_text())['driveway']
 lo=38+drive['x']-drive['width']/2-.08;hi=38+drive['x']+drive['width']/2+.08
 front=9+drive['front']-.08;back=9+drive['back']+.08
 grade=bpy.data.objects.get('Distant grade');parent=grade.parent;bpy.data.objects.remove(grade,do_unlink=True)
 for i,bounds in enumerate(((-2000,lo,-2000,2000),(hi,2000,-2000,2000),(lo,hi,-2000,front),(lo,hi,back,2000))):
  flat('Distant grade '+str(i),bounds,'Green',parent,FLOW-.025)
 truck,tobs=load_context(paths[1],(8,-18,0))
 truck.rotation_euler.z=math.radians(90)
 return dict(location=(-46,-65,27),target=(14,0,2),ortho=90,aspect=2.25),[bundle(path) for path in paths]


def tone(path,camera,assets):
 from PIL import Image,ImageDraw
 import numpy as np
 from bpy_extras.object_utils import world_to_camera_view
 im=Image.open(path).convert('RGB');w,h=im.size
 mask=Image.new('L',(w,h));dr=ImageDraw.Draw(mask)
 for ob in assets:
  if ob.type!='MESH':continue
  # Paving excluded so architecture/equipment dark cavities are represented.
  if ob.get('asset_set') in ('SitePaving','Landscape') or 'SitePaving' in ob.name:continue
  ps=[world_to_camera_view(bpy.context.scene,camera,ob.matrix_world@v.co) for v in ob.data.vertices]
  for poly in ob.data.polygons:
   points=[ps[i] for i in poly.vertices]
   if all(v.z>0 for v in points):dr.polygon([(v.x*w,(1-v.y)*h) for v in points],fill=255)
 rgb=np.asarray(im)/255.;valid=np.asarray(mask)>0;y=rgb@np.array([.2126,.7152,.0722]);a=y[valid]
 bounds=mask.getbbox()
 result=dict(scope='Projected architectural/equipment geometry mask, paving and foliage excluded; visibility is a conservative polygon union',pixels=int(valid.sum()),projected_bounds_fraction=[bounds[0]/w,bounds[1]/h,bounds[2]/w,bounds[3]/h],projected_width_fraction=(bounds[2]-bounds[0])/w,Yprime_percentiles=dict(zip(('p1','p50','p95','p99'),map(float,np.percentile(a,[1,50,95,99])))),white_clip_fraction=float((rgb[valid].min(axis=-1)>.985).mean()))
 path.with_suffix('.tone.json').write_text(json.dumps(result,indent=2));mask.save(path.with_suffix('.mask.png'))


def frame_property(camera,assets):
 """Fit actual exported vertices, including public interfaces, inside 4% margins."""
 from bpy_extras.object_utils import world_to_camera_view
 points=[ob.matrix_world@v.co for ob in assets if ob.type=='MESH' for v in ob.data.vertices]
 for _ in range(4):
  bpy.context.view_layer.update()
  uv=[world_to_camera_view(bpy.context.scene,camera,p) for p in points]
  assert min(p.z for p in uv)>0,'Property behind above-view camera'
  lo=[min(p[k] for p in uv) for k in (0,1)];hi=[max(p[k] for p in uv) for k in (0,1)]
  factor=max((.5-min(lo))/.46,(max(hi)-.5)/.46)
  if factor<=1.00001:return dict(min_uv=lo,max_uv=hi,required_margin=.04,vertices=len(points))
  camera.data.lens/=factor*1.01
 raise AssertionError('Whole-property framing did not converge')


def render(source,out,names,width,samples,camera_file=None,engine='CYCLES'):
 neighborhood={'hero','street','above','scale','top'} if camera_file is None else set()
 near=[n for n in names if n in neighborhood];accepted=[n for n in names if n not in neighborhood]
 if near and accepted:
  return {**render(source,out,near,width,samples,camera_file,engine),**render(source,out,accepted,width,samples,camera_file,engine)}
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
 assets=set(bpy.context.scene.objects);meta=json.loads(source.with_suffix('.json').read_text())
 palette(BRANDS[meta['brand']],meta['building']['wall_color'])
 # Match site orientation. Context stays outside the diagnostic station GLB.
 if 'baked PBR' in meta['stage']:
  from presentation import ground
  road,ground_record=ground(meta,neighborhood=bool(near))
 else:
  road=context_roads(meta);road.rotation_euler.z=math.radians(meta['yaw']);ground_record=None
 camera=setup(samples,engine);shots=views(meta);ctx=[]
 figures=[]
 if 'scale' in names:
  import importlib.util
  spec=importlib.util.spec_from_file_location('_commercial_human',HERE.parents[1]/'houses/src/render.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  ix,iy=meta['islands'][0]['center'];xx,yy=rotate((ix+1.8,iy-2.4),meta['yaw'])
  hit,point,_,_,_,_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((xx,yy,.5)),Vector((0,0,-1)),distance=1)
  assert hit;figures=module.human((xx,yy,point.z))
  for ob in figures:ob.hide_render=True
 if 'context_scale' in names:
  if meta['yaw']!=0:raise ValueError('Scale comparison uses seed 101 canonical corner')
  shots['context_scale'],ctx=context(meta)
 if camera_file:shots={k:d['shot'] for k,d in json.loads(camera_file.read_text()).items()}
 out.mkdir(parents=True,exist_ok=True);records={}
 for name in names:
  shot=dict(shots[name]);camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
  for ob in figures:ob.hide_render=not shot.get('human',False)
  for ob in set(bpy.context.scene.objects)-assets-{camera,bpy.data.objects['Sun']}-set(figures):
   if ob.type=='MESH':ob.hide_render=name in ('front','side','back') or (name=='top' and ob.get('presentation_neighbor',False))
  eye=None;camera.data.shift_y=shot.get('shift_y',0)
  if name in ('hero','street') and camera_file is None:
   bpy.context.view_layer.update();hit,point,_,_,surface,_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((camera.location.x,camera.location.y,1000)),Vector((0,0,-1)))
   if not hit:raise AssertionError('Street eye has no road surface beneath it')
   camera.location.z=point.z+1.60
   shot['location']=tuple(camera.location);shot['target']=(shot['target'][0],shot['target'][1],camera.location.z)
   camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
   eye=dict(height_m=camera.location.z-point.z,surface_z_m=point.z,surface=surface.name)
  camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',40)
  if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
  if name=='motion':
   for n in ('Entry_Left','Entry_Right'):
    ob=bpy.data.objects.get(n)
    if ob:ob.rotation_mode='XYZ';ob.rotation_euler.z=math.radians(-65 if n=='Entry_Left' else 65)
  sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.5));sc.render.resolution_percentage=100;sc.render.film_transparent=shot.get('background')=='transparent'
  framing=None
  if name=='above':
   framing=frame_property(camera,assets);shot['lens']=float(camera.data.lens)
  bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=shot.get('sky_strength',.025)
  sc.world.node_tree.nodes['Ambient balance'].inputs[0].default_value=shot.get('neutral_ambient',0)
  sc.world.node_tree.nodes['Sky chroma'].inputs['Saturation'].default_value=shot.get('sky_saturation',1)
  direction=shot.get('sun_direction',(.35,.75,-.8))
  sun=bpy.data.objects['Sun'];sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
  sun.data.energy=shot.get('sun_energy',6)
  elevation=math.degrees(math.atan2(-direction[2],math.hypot(*direction[:2])));rotation=math.degrees(math.atan2(-direction[1],-direction[0]))
  sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=math.radians(shot.get('sun_elevation',-4 if shot.get('dusk') else elevation));sky.sun_rotation=math.radians(shot.get('sun_rotation',rotation))
  sc.view_settings.exposure=shot.get('exposure',.25)
  if engine=='BLENDER_EEVEE':
   # Eevee needs a local diffuse cache for sky/bounce light beneath the roof.
   # This is presentation lighting, never a substitute material or export.
   bpy.ops.object.lightprobe_add(type='VOLUME',location=(0,0,3.2));probe=bpy.context.object;probe.name='Station sky and bounce cache';probe.scale=(30,30,4)
   probe.data.resolution_x=16;probe.data.resolution_y=16;probe.data.resolution_z=5;probe.data.bake_samples=64
   probe.data.capture_world=True;probe.data.capture_indirect=True;probe.data.capture_emission=True
   bpy.ops.object.lightprobe_cache_bake(subset='ALL')
  path=out/(name+'.png');sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
  if name=='hero':tone(path,camera,assets)
  if name=='scale':
   points=[o.matrix_world@v.co for o in figures for v in o.data.vertices];height=max(q.z for q in points)-min(q.z for q in points);assert abs(height-1.8)<.001
   path.with_suffix('.scale.json').write_text(json.dumps(dict(measured_height_m=height,foot_surface_z_m=min(q.z for q in points),scope='Actual generated silhouette vertices and ray-hit support surface'),indent=2))
  records[name]=dict(source=str(source),sha256=sha(source),image_sha256=sha(path),camera=shot,lighting=dict(sun_energy=sun.data.energy,sun_direction=direction,sky_strength=bg.inputs['Strength'].default_value,sky_elevation_degrees=math.degrees(sky.sun_elevation),exposure=sc.view_settings.exposure),eye_measurement=eye,framing_measurement=framing,width=width,samples=samples,engine=engine,stage=meta['stage'],context=ctx,ground=ground_record,recipe_sha256=recipe())
 for row in ctx:
  if bundle(HERE.parents[1]/row['source'])!=row:raise AssertionError('Presentation changed a context export')
 old=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {};old.update(records)
 (out/'provenance.json').write_text(json.dumps(old,indent=2))
 return records

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path,default=Path('build/station-101.glb'));a.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a.add_argument('--width',type=int,default=1440);a.add_argument('--samples',type=int,default=40);a.add_argument('--shots',default='hero,above,dispenser,canopy,entry,sign,rear');a.add_argument('--camera-file',type=Path);a.add_argument('--family',action='store_true');a.add_argument('--engine',default='CYCLES');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 render(a.source,a.out,a.shots.split(','),a.width,a.samples,a.camera_file,a.engine)
 if a.family:
  for seed in PROOF_SEEDS:render(Path(f'export/CommercialGas-{seed}.gltf') if a.source.suffix=='.gltf' else a.source.parent/f'station-{seed}.glb',a.out/'seeds'/str(seed),['above','street'],a.width,a.samples)
