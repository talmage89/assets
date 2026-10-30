"""Independent physical-light response of the actual GLB, for lighting fits."""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
import final_shots as F,interface
from guns.common.render import main
from guns.common.photo_matches import camera_shots
from kit import weapon_presentation as P
original=P.pose
def layered(arm,clip,frame,**kw):
 original(arm,clip,frame,**kw);keep={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
 for bone,(action,f) in F.ACTIVE_LAYERS.items():
  original(arm,action,f,**kw);keep[bone]=arm.pose.bones[bone].matrix_basis.copy()
 if F.ACTIVE_LAYERS:
  arm.animation_data.action=None
  for name,m in keep.items():arm.pose.bones[name].matrix_basis=m
  bpy.context.view_layer.update()
P.pose=layered
B=[dict(world=True)]
for x in (-.65,.65):
 for z in (-.35,.12,.75):
  B.append(dict(position=(x,.12,z),size=(.7,1.2)))
for y in (-.8,.95):
 for z in (-.25,.15,.65):B.append(dict(position=(0,y,z),size=(.6,.7)))
for x in (-.25,.25):
 for z in (.38,.80):B.append(dict(position=(x,.15,z),size=(.04,.65)))
B.extend([dict(position=(-.12,-.02,-.065),size=(.12,.15)),dict(position=(-.6,.15,.2),size=(.07,.8)),dict(position=(.6,.15,.2),size=(.07,.8))])

for x in (-.65,-.32):
 for z in (.20,.40,.70,1.0):B.append(dict(position=(x,.15,z),size=(.8,.025)))
def exr(sc,*args):
 sc.render.image_settings.file_format='OPEN_EXR';sc.render.image_settings.color_mode='RGBA';sc.render.image_settings.color_depth='32';sc.render.filepath=str(Path(sc.render.filepath).with_suffix('.exr'))
B.extend([dict(position=(-.08,.20,.32),size=(.16,.025)),dict(position=(-.16,.20,.40),size=(.20,.04)),dict(position=(-.15,.04,-.19),size=(.35,.30)),dict(position=(-.10,.04,-.12),size=(.15,.14))])
for x,z in ((.32,.22),(.60,.30),(.32,.30),(.60,.40)):
 B.append(dict(position=(x,.18,z),size=(.12,.035),target=(0,.16,.145)))
for x,y,z,size in ((0,.50,-.33,(.5,.4)),(-.18,.50,-.20,(.35,.3)),(.18,.50,-.20,(.35,.3)),(-.12,.62,.23,(.15,.04))):
 B.append(dict(position=(x,y,z),size=size,target=(0,y,.10)))
# Small physical cards near the measured front-crown reflection direction.
# They let a local lobe change without washing the complete cover or grip.
for y in (.205941036,.180941030,.230941042):
 B.append(dict(position=(-.030647019,y,.200168326),size=(.025,.006),target=(-.028261960,.190106541,.142344624)))
original_prepare=F.prepare_shot

def prepare(scene,shot):
 original_prepare(scene,shot)
 scene.cycles.use_denoising=False
 for ob in scene.objects:
  if ob.type=='LIGHT':ob.data.energy=0
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=0
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.25,.25,1)
 if 'Basis area' not in scene.objects:
  d=bpy.data.lights.new('Basis area','AREA');d.shape='RECTANGLE';o=bpy.data.objects.new('Basis area',d);scene.collection.objects.link(o)
 scene.objects['Basis area'].data.energy=0
 b=B[shot['basis_index']]
 if b.get('world'):scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 else:
  o=scene.objects['Basis area'];o.data.energy=1;o.data.color=(1,1,1);o.location=b['position'];o.data.size,o.data.size_y=b['size'];o.rotation_euler=(Vector(b.get('target',(0,.10,.07)))-o.location).to_track_quat('-Z','Y').to_euler()
 active=[ob.name for ob in scene.objects if ob.type=='LIGHT' and not ob.hide_render and ob.data.energy>0]
 assert active==([] if b.get('world') else ['Basis area']),('Contaminated light response',shot['basis_index'],active)
 shot['basis_fixture_audit']=dict(active_area_lights=active,world_strength=float(scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value))
 if exr not in bpy.app.handlers.render_pre:bpy.app.handlers.render_pre.append(exr)
F.prepare_shot=prepare
matches=camera_shots(BASE/'build/cameras.json');shots={}
requested=sys.argv[sys.argv.index('--sets')+1].split(',');k=sys.argv.index('--sets');del sys.argv[k:k+2]
indices=None
if '--indices' in sys.argv:
 k=sys.argv.index('--indices');indices={int(v) for v in sys.argv[k+1].split(',')};del sys.argv[k:k+2]
for name in requested:
 for i,b in enumerate(B):
  if indices is not None and i not in indices:continue
  shots[name+'__'+str(i)]=dict(matches[name],**F.PHOTO_POSES[name],basis_index=i)
F.SHOTS=shots;F.DEFAULT_SHOTS=','.join(shots)
out=Path(sys.argv[sys.argv.index('--out')+1]);old_meta={}
if indices is not None and (out/'shots.json').exists():
 old_meta=json.loads((out/'shots.json').read_text());old_bases=json.loads((out/'bases.json').read_text())
 assert old_bases==json.loads(json.dumps(B[:len(old_bases)])), 'Existing response bases changed; use a fresh output folder'
main(F,interface)
if old_meta:
 new_meta=json.loads((out/'shots.json').read_text());sha={r['sha256'] for r in new_meta.values()}
 assert {r['sha256'] for r in old_meta.values()}==sha,'Response batches use different GLBs'
 old_meta.update(new_meta);(out/'shots.json').write_text(json.dumps(old_meta,indent=2))
(out/'bases.json').write_text(json.dumps(B,indent=2))
for p in out.glob('*.png'):
 if p.read_bytes()[:4]==bytes((118,47,49,1)):p.rename(p.with_suffix('.exr'))
configs=[Path(bpy.utils.resource_path(k))/'datafiles/colormanagement/config.ocio' for k in ('LOCAL','SYSTEM')]
config=next(p for p in configs if p.exists());(out/'ocio-path.txt').write_text(str(config))

