"""Source checkpoint cameras; uses the family's procedural summer daylight."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup,human,simple


def shots(meta):
 m,g=meta['blocks'];side=1 if meta['spec']['garage']['side']=='right' else -1
 x=meta['door_x'];y=m['y0'];front=min(m['y0'],g['y0']);w=max(m['x1'],g['x1'])-min(m['x0'],g['x0'])
 picture=next(o for o in meta['openings'] if o.get('style')=='picture');wx=m['x0']+picture['u']
 z=meta['porch']['eave'];outer=m['x0'] if side==1 else m['x1'];floor=m['floor']
 from plan import generate
 plan=generate(meta['seed'],meta['spec'],house_type='ranch');roof=plan.get('roof_envelope') or plan['blocks'][0]
 rx=m['x0']+(m['x1']-m['x0'])*.52;ry=m['y0']+(m['y1']-m['y0'])*.70;rz=roof.height(rx,ry)
 return dict(hero=dict(location=(side*14,front-22,1.68),target=(0,0,1.65),lens=40,aspect=1.85),
  weather=dict(location=(rx+1.8,ry+3.0,rz+2.2),target=(rx,ry,rz),lens=50,aspect=1.5),
  front=dict(location=(0,-40,2),target=(0,0,2),ortho=w+3,aspect=2.25),
  rear=dict(location=(0,40,2),target=(0,0,2),ortho=w+3,aspect=2.25),
  side=dict(location=(side*40,0,2.4),target=(0,0,2.4),ortho=13,aspect=1.5),
  top=dict(location=(0,.35,40),target=(0,.35,0),ortho=w+6,aspect=1.6),
  back=dict(location=(side*14,25,7),target=(0,0,1.6),lens=43,aspect=1.85),
  roof=dict(location=(13,-18,23),target=(0,0,1.6),lens=38,aspect=1.65),
  eave=dict(location=(outer-side*2.3,y-3.0,1.75),target=(outer+side*.15,y-.10,m['eave']-.60),lens=42,aspect=1.2),
  window=dict(location=(wx+.6,y-4.5,1.75),target=(wx,y,m['floor']+1.4),lens=46,aspect=1.5),
  entry=dict(location=(x+1.7,y-4.9,1.90),target=(x,y-.4,m['floor']+1.10),lens=44,aspect=1.15),
  chimney=dict(location=(m['x0']+1,m['y0']-3,6.2),target=(m['x0']+(m['x1']-m['x0'])*.33,(m['y0']+m['y1'])/2+.13,5.0),lens=65,aspect=1.3),
  scale=dict(location=(x+3,y-9,2.1),target=(x,y-.6,m['floor']+1.0),lens=46,aspect=1.5,human=True))


def reflection_scenery(meta):
 """Original reflection-only studio scenery, excluded from the house and rays."""
 import random
 r=random.Random(624);m=meta['blocks'][0];green=simple('Reflection foliage',(.10,.14,.04))
 bark=simple('Reflection trunks',(.085,.052,.027))
 for x,y in [(-19,m['y0']-10),(-8,m['y0']-13),(3,m['y0']-15),(15,m['y0']-11),(24,m['y0']-7)]:
  verts=[];faces=[]
  for j in range(100):
   theta=r.uniform(0,math.tau);rr=math.sqrt(r.random())*2.4
   center=Vector((x+rr*math.cos(theta),y+rr*math.sin(theta),r.uniform(2.0,6.3)))
   for k in range(12):
    p=center+Vector(tuple(r.uniform(-.32,.32) for _ in range(3)))
    u=Vector(tuple(r.uniform(-1,1) for _ in range(3))).normalized()*r.uniform(.04,.08)
    v=u.cross(Vector((r.random(),r.random(),1))).normalized()*u.length*.45
    i=len(verts);verts.extend((p-u,p+v,p+u,p-v,p+u.cross(v).normalized()*.007))
    faces.extend((i+j,i+(j+1)%4,i+4) for j in range(4))
  me=bpy.data.meshes.new('Original reflection leaves');me.from_pydata(verts,[],faces);me.update()
  ob=bpy.data.objects.new('PresentationReflectionFoliage',me);bpy.context.collection.objects.link(ob);me.materials.append(green)
  ob.visible_camera=False;ob.visible_shadow=False;ob.visible_diffuse=False;ob.visible_transmission=False
  bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.13,depth=4,location=(x,y,2))
  ob=bpy.context.object;ob.name='PresentationReflectionTrunk';ob.data.materials.append(bark);ob.visible_camera=False;ob.visible_shadow=False;ob.visible_diffuse=False;ob.visible_transmission=False
 # A simple original neighboring volume gives the large pane something
 # built to reflect. It is studio scenery, never saved/exported with a house.
 wall=simple('Reflection neighbor wall',(.34,.32,.27));roof=simple('Reflection neighbor roof',(.15,.145,.12))
 x0,x1=-6.5,2.5;y0,y1=m['y0']-17.5,m['y0']-10.5;cy=(y0+y1)/2
 vs=[(x0,y0,0),(x1,y0,0),(x1,y1,0),(x0,y1,0),(x0,y0,2.7),(x1,y0,2.7),(x1,y1,2.7),(x0,y1,2.7),(x0,cy,3.8),(x1,cy,3.8)]
 theta=math.radians(35);vs=[(-2+(x+2)*math.cos(theta)-(y-cy)*math.sin(theta),cy+(x+2)*math.sin(theta)+(y-cy)*math.cos(theta),z) for x,y,z in vs]
 fs=[(0,1,5,4),(1,2,6,9,5),(2,3,7,6),(3,0,4,8,7),(4,5,9,8),(8,9,6,7)]
 me=bpy.data.meshes.new('Original reflection neighbor');me.from_pydata(vs,[],fs);me.update();me.materials.append(wall);me.materials.append(roof)
 for poly in me.polygons:poly.material_index=1 if poly.index>=4 else 0
 ob=bpy.data.objects.new('PresentationReflectionNeighbor',me);bpy.context.collection.objects.link(ob)
 ob.visible_camera=False;ob.visible_shadow=False;ob.visible_diffuse=False;ob.visible_transmission=False


def render(source,out,names='hero',width=1200,samples=32,engine='CYCLES',camera_file=None,comparison=False,colonial_source=None):
 from delivery_io import bundle_hash
 final=source.suffix=='.gltf'
 if final:
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
 else:bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
 meta=json.loads(source.with_suffix('.json').read_text())
 digest=bundle_hash(source) if final else hashlib.sha256(source.read_bytes()).hexdigest()
 material_hashes={bpy.path.abspath(im.filepath):hashlib.sha256(Path(bpy.path.abspath(im.filepath)).read_bytes()).hexdigest() for im in bpy.data.images if im.filepath and Path(bpy.path.abspath(im.filepath)).is_file()}
 camera=setup(engine,samples);reflection_scenery(meta);views=shots(meta)
 chimney=bpy.data.objects.get('Brick_Chimney')
 if chimney:
  points=[chimney.matrix_world@v.co for v in chimney.data.vertices];lo=Vector(tuple(min(p[k] for p in points) for k in range(3)));hi=Vector(tuple(max(p[k] for p in points) for k in range(3)))
  center=(lo+hi)/2;center.z=hi.z-.45
  views['chimney']=dict(location=tuple(center+Vector((3,-4,2.0))),target=tuple(center),lens=52,aspect=1.3)
 elif meta.get('chimney_camera'):
  views['chimney']=meta['chimney_camera']
 if camera_file:views={n:r['shot'] for n,r in json.loads(camera_file.read_text()).items()}
 figures=human((meta['door_x']-.20,meta['porch']['y0']+.5,meta['porch']['floor']))
 for o in figures:o.hide_render=True
 context=None
 if comparison:
  from delivery_io import bundle_hash
  colonial=colonial_source or (Path('export/Hearthfield-27.gltf') if Path('export/Hearthfield-27.gltf').exists() else Path('build/lookdev.blend'))
  context=dict(source=str(colonial),sha256=bundle_hash(colonial) if colonial.suffix=='.gltf' else hashlib.sha256(colonial.read_bytes()).hexdigest())
  # Authored colonial at the same meter scale, read-only within this clone.
  before=set(bpy.context.scene.objects)
  # Source tiling uses a minimal occlusion group. Reserve the importer's
  # canonical name so Blender can create its complete settings interface.
  group=bpy.data.node_groups.get('glTF Material Output')
  if group:group.name='HouseSource_Occlusion'
  if colonial.suffix=='.gltf':bpy.ops.import_scene.gltf(filepath=str(colonial.resolve()))
  else:
   with bpy.data.libraries.load(str(colonial.resolve()),link=False) as (src,dst):dst.objects=src.objects
   for ob in dst.objects:
    if ob and ob.name not in bpy.context.scene.objects:bpy.context.scene.collection.objects.link(ob)
  imported=set(bpy.context.scene.objects)-before
  # Import is in Blender coordinates, both grade datums are 0.
  for o in imported:
   if o.parent not in imported:o.location.x+=22
  views={'types':dict(location=(11,-70,14),target=(11,0,3.6),ortho=45,aspect=2.4)}
 out.mkdir(parents=True,exist_ok=True);reports={}
 for name in names.split(','):
  shot=views[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
  camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',45)
  if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
  for ob in figures:ob.hide_render=not shot.get('human',False)
  sc=bpy.context.scene
  # A sunny autumn photo under mature trees has lower sky/ground fill than
  # the open summer studio. Fit illumination, never paint its shadows in.
  light=dict(direction=(.4,1.,-.6),world=.008,grade=(.04,.048,.035)) if name=='ranch_sun_oblique' else dict(direction=(.6,.7,-1),world=.09,grade=(.16,.17,.15))
  if name=='hero':light=dict(direction=(.2,1.,-.74),world=.012,grade=(.055,.065,.05))
  bpy.data.objects['Afternoon sun'].rotation_euler=Vector(light['direction']).to_track_quat('-Z','Y').to_euler()
  next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=light['world']
  bpy.data.materials['Neutral warm gray grade'].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*light['grade'],1)
  sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
  sc.view_settings.look='AgX - Very High Contrast' if name=='ranch_sun_oblique' else 'AgX - Medium High Contrast'
  light['view_look']=sc.view_settings.look
  sc.view_settings.exposure=shot.get('exposure',-.35);sc.render.film_transparent=shot.get('background')=='transparent';sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
  if name=='hero':
   from PIL import Image,ImageDraw
   from bpy_extras.object_utils import world_to_camera_view
   import numpy as np
   mask=Image.new('L',(sc.render.resolution_x,sc.render.resolution_y));draw=ImageDraw.Draw(mask)
   for ob in sc.objects:
    if ob.type!='MESH' or not ob.get('asset_set'):continue
    points=[]
    for v in ob.data.vertices:
     uv=world_to_camera_view(sc,camera,ob.matrix_world@v.co);points.append((uv.x*mask.width,(1-uv.y)*mask.height))
    ob.data.calc_loop_triangles()
    for t in ob.data.loop_triangles:draw.polygon([points[i] for i in t.vertices],fill=255)
   rgb=np.asarray(Image.open(out/(name+'.png')).convert('RGB'))/255.;rgb=rgb[np.asarray(mask)>0];lum=rgb@np.array([.2126,.7152,.0722])
   tonal=dict(zip(('p1','p50','p95','p99'),map(float,np.quantile(lum,[.01,.5,.95,.99]))));tonal['clipped_white_fraction']=float(np.mean(np.min(rgb,axis=1)>.985))
   (out/'tonal.json').write_text(json.dumps(tonal,indent=2))
   if final and meta['seed']==12 and engine=='CYCLES':
    from ranch_shadow import measure
    measure(out/'hero.png',meta,camera,light['direction'])
  reports[name]=dict(lighting=light,context=context,material_sha256=material_hashes,source=str(source),source_sha256=digest,seed=meta['seed'],engine=engine,stage=meta['stage'],camera=shot)
 if context:
  cp=Path(context['source']);assert (bundle_hash(cp) if cp.suffix=='.gltf' else hashlib.sha256(cp.read_bytes()).hexdigest())==context['sha256']
 assert digest==(bundle_hash(source) if final else hashlib.sha256(source.read_bytes()).hexdigest())
 (out/'provenance.json').write_text(json.dumps(reports,indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('build/ranch/house-11.blend'));p.add_argument('--out',type=Path,default=Path('renders/ranch/pass1'))
 p.add_argument('--shots',default='hero');p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32);p.add_argument('--engine',default='CYCLES');p.add_argument('--camera-file',type=Path);p.add_argument('--comparison',action='store_true');p.add_argument('--colonial-source',type=Path)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);render(a.source,a.out,a.shots,a.width,a.samples,a.engine,a.camera_file,a.comparison,a.colonial_source)
