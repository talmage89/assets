"""Cycles form review from fresh imported diagnostic GLBs, with provenance.

No source shader replacement and no baked-look claim. Context loads immutable
exports for the same-scale comparison only; no context is ever re-exported.
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

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def setup(samples,engine='CYCLES'):
 sc=bpy.context.scene;sc.render.engine=engine
 if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
 sc.world=bpy.data.worlds.new('Original sky');sc.world.use_nodes=True
 ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links;ns.clear()
 sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(220);sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=.3
 bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.13
 mix=ns.new('ShaderNodeMixRGB');mix.name='Ambient balance';mix.inputs[0].default_value=0;mix.inputs[2].default_value=(1,1,1,1)
 out=ns.new('ShaderNodeOutputWorld');ls.new(sky.outputs[0],mix.inputs[1]);ls.new(mix.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
 ld=bpy.data.lights.new('Sun','SUN');ob=bpy.data.objects.new('Sun',ld);sc.collection.objects.link(ob)
 ld.energy=3.3;ld.angle=math.radians(.6);ld.color=(1,.97,.92)
 ob.rotation_euler=Vector((.5,.7,-1)).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(cam);sc.camera=cam
 cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_start=.025;cam.data.clip_end=4000
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.15
 sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=6500
 sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 return cam


def views(p):
 W,D=p['lot'];b=p['building'];c=p['canopy'];x,y=p['islands'][0]['center'];u,v=rotate((0,-.96),c['angle']);x+=u;y+=v
 # Authored local camera positions rotate with the corner, all street eyes 1.68m.
 shots=dict(
 hero=dict(location=(-W/2-12,-D/2-10,FLOW+.00635+1.68),target=(0,-3,2.6),lens=39,aspect=1.85),
 street=dict(location=(-W/2-8,-D/2-6,FLOW+.00635+1.68),target=(0,-2,2.7),lens=35,aspect=1.85),
 above=dict(location=(-W*.73,-D*.93,46),target=(0,-1,0),lens=35,aspect=1.42),
 dispenser=dict(location=(x+3.7,y-3.0,1.75),target=(x,y,1.36),lens=60,aspect=1.25),
 canopy=dict(location=(-c['width']/2-1,c['center'][1]-7.8,2.1),target=(-c['width']/2+2,c['center'][1]-.5,4.20),lens=45,aspect=1.45),
 entry=dict(location=(4.5,b['front']-8,1.70),target=(0,b['front'],1.65),lens=44,aspect=1.5),
 sign=dict(location=(p['sign_center'][0]+5,p['sign_center'][1]-8,1.68),target=(*p['sign_center'],2.25 if p['sign']=='monument' else 3.55),lens=48,aspect=1.25),
 rear=dict(location=(W/2+6,D/2+10,6.0),target=(2,12,2),lens=40,aspect=1.6),
 motion=dict(location=(3,b['front']-6,1.7),target=(0,b['front']+.2,1.55),lens=43,aspect=1.4),
 )
 result={k:{**v,'location':rotate(v['location'],p['yaw']),'target':rotate(v['target'],p['yaw'])} for k,v in shots.items()}
 # Common geographic overhead makes the four real corner orientations visible.
 result['above']=shots['above']
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
  if ob.get('asset_set')=='SitePaving' or 'SitePaving' in ob.name:continue
  ps=[world_to_camera_view(bpy.context.scene,camera,ob.matrix_world@v.co) for v in ob.data.vertices]
  for poly in ob.data.polygons:
   points=[ps[i] for i in poly.vertices]
   if all(v.z>0 for v in points):dr.polygon([(v.x*w,(1-v.y)*h) for v in points],fill=255)
 rgb=np.asarray(im)/255.;valid=np.asarray(mask)>0;y=rgb@np.array([.2126,.7152,.0722]);a=y[valid]
 result=dict(scope='Projected geometry mask, static form GLB, paving excluded',pixels=int(valid.sum()),Yprime_percentiles=dict(zip(('p1','p50','p95','p99'),map(float,np.percentile(a,[1,50,95,99])))),white_clip_fraction=float((rgb[valid].min(axis=-1)>.985).mean()))
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
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
 assets=set(bpy.context.scene.objects);meta=json.loads(source.with_suffix('.json').read_text())
 palette(BRANDS[meta['brand']],meta['building']['wall_color'])
 # Match site orientation. Context stays outside the diagnostic station GLB.
 road=context_roads(meta);road.rotation_euler.z=math.radians(meta['yaw'])
 camera=setup(samples,engine);shots=views(meta);ctx=[]
 if 'scale' in names:
  if meta['yaw']!=0:raise ValueError('Scale comparison uses seed 101 canonical corner')
  shots['scale'],ctx=context(meta)
 if camera_file:shots={k:d['shot'] for k,d in json.loads(camera_file.read_text()).items()}
 out.mkdir(parents=True,exist_ok=True);records={}
 for name in names:
  shot=dict(shots[name]);camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
  eye=None
  if name in ('hero','street') and camera_file is None:
   bpy.context.view_layer.update();hit,point,_,_,surface,_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((camera.location.x,camera.location.y,1000)),Vector((0,0,-1)))
   if not hit:raise AssertionError('Street eye has no road surface beneath it')
   eye=dict(height_m=camera.location.z-point.z,surface_z_m=point.z,surface=surface.name)
   if abs(eye['height_m']-1.68)>.0001:raise AssertionError(eye)
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
  bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=shot.get('sky_strength',.13)
  sc.world.node_tree.nodes['Ambient balance'].inputs[0].default_value=shot.get('neutral_ambient',0)
  sun=bpy.data.objects['Sun'];sun.rotation_euler=Vector(shot.get('sun_direction',(.5,.7,-1))).to_track_quat('-Z','Y').to_euler()
  sc.view_settings.exposure=shot.get('exposure',-.15)
  path=out/(name+'.png');sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
  if name=='hero':tone(path,camera,assets)
  records[name]=dict(source=str(source),sha256=sha(source),image_sha256=sha(path),camera=shot,eye_measurement=eye,framing_measurement=framing,width=width,samples=samples,engine=engine,stage=meta['stage'],context=ctx,recipe_sha256=recipe())
 for row in ctx:
  if bundle(HERE.parents[1]/row['source'])!=row:raise AssertionError('Presentation changed a context export')
 old=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {};old.update(records)
 (out/'provenance.json').write_text(json.dumps(old,indent=2))
 return records

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path,default=Path('build/station-101.glb'));a.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a.add_argument('--width',type=int,default=1440);a.add_argument('--samples',type=int,default=40);a.add_argument('--shots',default='hero,above,dispenser,canopy,entry,sign,rear');a.add_argument('--camera-file',type=Path);a.add_argument('--family',action='store_true');a.add_argument('--engine',default='CYCLES');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 render(a.source,a.out,a.shots.split(','),a.width,a.samples,a.camera_file,a.engine)
 if a.family:
  for seed in PROOF_SEEDS:render(Path(f'build/station-{seed}.glb'),a.out/'seeds'/str(seed),['above','street'],a.width,a.samples)
