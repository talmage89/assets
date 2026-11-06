"""Reusable-part turnarounds, human scale and phase demonstration from delivery.

The source is always an external-image exported glTF. Studio construction and
lights use the shared kit. No material edits are saved to the delivery.
"""
import argparse,sys,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import studio,gpu,model as G
from deliver import bundle

def load(part):
 path=Path('export/parts')/(part+'.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
 roots=[o for o in bpy.context.scene.objects if not o.parent]
 points=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
 lo=Vector(tuple(min(p[i] for p in points) for i in range(3)));hi=Vector(tuple(max(p[i] for p in points) for i in range(3)))
 offset=Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,0 if part in ('MastArm','Pedestal','Cabinet') else -lo.z))
 for rt in roots:rt.location+=offset
 return path,roots,hi-lo

def main():
 p=argparse.ArgumentParser();p.add_argument('--parts',default='Head_three,Head_fya,PedHead,PushButton,MastArm,Pedestal,Cabinet');p.add_argument('--out',type=Path,default=Path('renders/final/gallery'));p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32);p.add_argument('--motion',action='store_true');p.add_argument('--scale',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 for part in a.parts.split(','):
  source,roots,size=load(part);sc=bpy.context.scene
  span=max(size);scale=max(.4,span/1.7);cam=studio.add_studio(scale=scale,backdrop_color=(.20,.21,.20))
  sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=6
  sc.view_settings.view_transform='Khronos PBR Neutral';sc.view_settings.look='None';sc.view_settings.exposure=-1.8
  sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_x=a.width;sc.render.resolution_y=a.width;sc.render.resolution_percentage=100
  cam.data.type='ORTHO';cam.data.ortho_scale=max(size.x,size.y,size.z)*1.22;cam.data.clip_end=1000
  center=Vector((0,0,size.z/2));out=a.out/part;out.mkdir(parents=True,exist_ok=True)
  views={'front':(0,-1,.10),'side':(1,0,.10),'back':(0,1,.10),'top':(0,0,1)}
  human_height=None
  if a.scale:
   people=studio.human();bpy.context.view_layer.update()
   for ob in people:ob.location.x-=1.0
   bpy.context.view_layer.update();vertices=[ob.matrix_world@v.co for ob in people if ob.type=='MESH' for v in ob.data.vertices];human_height=max(v.z for v in vertices)-min(v.z for v in vertices);assert abs(human_height-1.8)<1e-5
   views={'scale':(1.15,-2.5,1.0)};cam.data.ortho_scale=max(size.x+3,size.z,2.1)*1.23;center=Vector((-.7,0,size.z/2))
  if a.motion:
   views={name:(.35,-1,.17) for name in ('green_fya_on','green_fya_off','yellow','red')};out=a.out;out.mkdir(exist_ok=True,parents=True);sc.render.resolution_y=round(a.width*.75);cam.data.ortho_scale=3.0
   # A through face and separate FYA face, both from independent exports.
   first=roots[0];first.location=(-.50,0,2.0)
   bpy.ops.import_scene.gltf(filepath=str(Path('export/parts/Head_fya.gltf').resolve()));second=next(o for o in sc.objects if o.parent is None and o.get('part_kind')=='Head_fya');second.location=(.50,0,2.0)
   # Both real hanger origins sit on one original, presentation-only stand.
   stand=studio.studio_mat('Phase display stand',(.045,.055,.055),.38)
   G.box('Phase stand foot',(0,.12,.025),(.45,.55,.05),stand,.015,2)
   G.cylinder('Phase stand post',(0,.12,.05),(0,.12,2.04),.028,stand,16)
   G.cylinder('Phase stand return',(0,.12,2.04),(0,0,2.04),.022,stand,12)
   G.cylinder('Phase hanger bar',(-.80,0,2.04),(.80,0,2.04),.022,stand,12)
   center=Vector((0,0,1.05))
  bpy.context.view_layer.update()
  for ob in sc.objects:
   if ob.type=='LIGHT':ob.visible_camera=False;assert ob.matrix_world.translation.length>.1
  studio_rest={ob:ob.matrix_world.copy() for ob in sc.objects if ob.get('studio') and ob!=cam}
  for name,direction in views.items():
   for ob,world in studio_rest.items():
    yaw=0 if name in ('front','top','scale') or a.motion else math.pi/2 if name=='side' else math.pi
    ob.matrix_world=Matrix.Rotation(yaw,4,'Z')@world
   if a.motion:
    for ob in sc.objects:
     if not ob.get('signal_lens'):continue
     kind=ob.get('signal_kind');fya=ob.parent.get('part_kind')=='Head_fya';on=False
     if fya:
      on=(name=='red' and kind=='red_arrow') or (name=='yellow' and kind=='yellow_arrow' and not ob.get('flashing_yellow_arrow')) or (name=='green_fya_on' and ob.get('flashing_yellow_arrow'))
     else:on=kind==('green' if name.startswith('green') else name)
     ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(bpy.data.materials['SharedLens_Lit' if on else 'SharedLens_Off'])
   cam.location=center+Vector(direction).normalized()*span*3;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
   sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
   paths=[source,Path('export/parts/Head_fya.gltf')] if a.motion else [source]
   meta=dict(sources={str(path):bundle(path) for path in paths},engine='CYCLES',shot=name,part=part,width=a.width,samples=a.samples,recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),human_height_m=human_height)
   (out/(name+'.json')).write_text(json.dumps(meta,indent=2));print('GALLERY',part,name,flush=True)
if __name__=='__main__':main()
