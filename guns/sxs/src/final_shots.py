"""Baked-export studio; identical five-light setup to the finished field guns."""
import math,hashlib
from pathlib import Path
from shots import SHOTS as FORM,PHOTO_POSES,STRIP_SHOT,floor_height
FINAL_STAGE=True
RENDER_STAGE='look round one: exported GLB and baked 2048 PBR'
SHOTS={**FORM,
 'hero':dict(location=(1.70,-.15,.50),target=(0,.235,-.008),lens=51,aspect=2.8),
 'hero_left':dict(location=(-1.70,-.15,.50),target=(0,.235,-.008),lens=51,aspect=2.8),
 'back':dict(location=(0,-1.5,-.023),target=(0,.235,-.023),ortho=.20,aspect=1),
 'shooter_three_quarter':dict(location=(.25,-.19,.17),target=(0,.10,.045),lens=47,aspect=1.6),
 'wrist':dict(location=(.25,-.13,.080),target=(0,-.025,.004),lens=72,aspect=1.5),
 'scale':dict(location=(3.8,3.6,1.9),target=(.15,.15,.90),lens=62,aspect=1,scale=True),
}
for name,s in SHOTS.items():
 s['exposure']=-.15;s['background']='transparent'
 if name not in ('shell','hull'):s.setdefault('action','Idle');s.setdefault('frame',0)
 else:s['ammo_light']=True
DEFAULT_SHOTS='hero,hero_left,side,left,front,back,top,shooter_three_quarter,aimed,open,breech,action,wrist,forend,stock,muzzle,top_controls,triggers,scale'
LIGHTS={
 'Key softbox':((.65,.05,.72),38,.45,1.30),
 'Camera fill':((-.70,.12,.42),15,.55,1.1),
 'Right rim strip':((-.18,.90,.50),18,.10,1.0),
 'Left rim strip':((-.45,-.20,.35),7,.15,.80),
 'Overhead reflection card':((0,.22,.85),7,.32,1.0),
}
MASK=False

def configure_scene(sc,source):
 import bpy
 from mathutils import Vector
 from kit import studio
 sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.25,.25,1)
 sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.15
 for name,(loc,power,w,h) in LIGHTS.items():
  ob=sc.objects[name];ob.location=loc;ob.data.color=(1,1,1);ob.data.energy=power;ob.data.size=w;ob.data.size_y=h
  ob.rotation_euler=(Vector((0,.22,0))-ob.location).to_track_quat('-Z','Y').to_euler()
  ob['field_energy']=power;ob['field_location']=loc;ob['field_size']=(w,h)
 roots=[o for o in sc.objects if not o.get('studio') and o.parent is None and o.type not in ('LIGHT','CAMERA')]
 placement=bpy.data.objects.new('Display placement',None);sc.collection.objects.link(placement)
 for ob in roots:ob.parent=placement
 for ob in studio.human():ob.location.x+=.60;ob.hide_render=True;ob['human_scale']=True
 mat=bpy.data.materials.new('Aim neutral gray');mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear()
 e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(.18,.18,.18,1)
 out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],out.inputs['Surface'])
 from kit import model as M
 card=M.box('Aim neutral card',(0,1.1,.07),(4,.003,3),mat,0);M.apply(card);card.hide_render=True
 paper=bpy.data.materials.new('Comparison gray paper');paper.use_nodes=True;nt=paper.node_tree;nt.nodes.clear()
 diffuse=nt.nodes.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Color'].default_value=(.18,.18,.18,1)
 out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(diffuse.outputs[0],out.inputs['Surface'])
 paper_ob=M.box('Comparison paper',(-.06,.25,0),(.003,8,8),paper,0);M.apply(paper_ob);paper_ob.hide_render=True
 def before_render(scene):
  if scene.get('exact_aim'):scene.render.film_transparent=False;card.hide_render=False
  if scene.get('photo_comparison'):scene.render.film_transparent=False;paper_ob.hide_render=False
 bpy.app.handlers.render_pre.append(before_render)
 if MASK:
  import json
  parts=sorted([o for o in sc.objects if o.type=='MESH' and 'bone' in o],key=lambda o:o.get('part_name',o.name))
  ids={}
  for i,ob in enumerate(parts,1):
   ids[str(i)]=ob.get('part_name',ob.name)
   mat=bpy.data.materials.new('ID_'+str(i));mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear()
   e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(i/255,0,0,1)
   out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],out.inputs['Surface'])
   ob.data.materials.clear();ob.data.materials.append(mat)
   for f in ob.data.polygons:f.material_index=0
  (Path(__file__).resolve().parents[1]/'build/look-part-ids.json').write_text(json.dumps(ids,indent=2))
  sc.view_settings.view_transform='Raw';sc.view_settings.look='None'
  sc.render.dither_intensity=0

def prepare_shot(sc,s):
 import bpy
 from mathutils import Vector
 s['samples_used']=sc.cycles.samples if sc.render.engine=='CYCLES' else sc.eevee.taa_render_samples
 h=hashlib.sha256();base=Path(__file__).resolve().parent
 for path in [base/'final_render.py',base/'final_shots.py',base.parent.parent/'common/render.py']:h.update(path.read_bytes())
 s['renderer_signature']=h.hexdigest()
 scale=s.get('scale',False);placement=sc.objects['Display placement'];placement.location=(.80,0,1.02) if scale else (0,0,0)
 sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(*s.get('look_world_color',(.35,.35,.35)),1) if s.get('look_light') else (.25,.25,.25,1)
 sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=s.get('look_world',1.0) if s.get('look_light') else .15
 sc['photo_comparison']=bool(s.get('look_light'))
 sc.objects['Comparison paper'].active_material.node_tree.nodes['Diffuse BSDF'].inputs['Color'].default_value=(*s.get('look_paper',(.18,.18,.18)),1)
 sc.objects['Comparison paper'].hide_render=not sc['photo_comparison']
 sc.objects['Comparison paper'].location.x=s.get('look_paper_x',-.06)
 # An ordinary matte studio card controls the reflected field in the extra
 # deep-blue photographic view. The same card is used for source and export.
 reflection=sc.objects.get('Photo matte reflection card')
 if reflection:reflection.hide_render=True
 if s.get('look_reflection_card'):
  from kit import model as M
  settings=s['look_reflection_card']
  if reflection is None:
   mat=sc.objects['Comparison paper'].active_material.copy()
   reflection=M.box('Photo matte reflection card',settings['location'],settings['size'],mat,0)
   reflection.visible_camera=False
  reflection.location=settings['location'];reflection.dimensions=settings['size']
  reflection.active_material.node_tree.nodes['Diffuse BSDF'].inputs['Color'].default_value=(*settings['color'],1)
  reflection.hide_render=False
 for ob in sc.objects:
  if ob.name.startswith('Studio black reflection flag'):ob.hide_render=bool(s.get('look_light'))
 sc.camera.data.shift_x=s.get('shift_x',0);sc.camera.data.shift_y=s.get('shift_y',0)
 for ob in sc.objects:
  if ob.get('human_scale'):ob.hide_render=not scale
  if ob.get('bake_only'):ob.hide_render=True
  if ob.type!='LIGHT' or 'field_energy' not in ob:continue
  ob.location=ob['field_location'];ob.data.energy=ob['field_energy'];ob.data.size,ob.data.size_y=ob['field_size']
  ob.data.color=(1,1,1)
  if s.get('look_light'):
   # Matched-photo rig, one neutral key and broad fill. Per-photo settings
   # describe lights, never apply a value correction to a sampled finish.
   light=s['look_light'];index=list(LIGHTS).index(ob.name)
   colors=s.get('look_light_colors',[(1,1,1)]*len(light))
   if index<len(colors):ob.data.color=colors[index]
   if index<len(light):
    loc,energy,w,h=light[index];ob.location=loc;ob.data.energy=energy;ob.data.size=w;ob.data.size_y=h
   else:ob.data.energy=0
  if s.get('aimed') or s.get('first_person'):
   if ob.name=='Key softbox':ob.location=(.65,-.30,.60);ob.data.energy=16;ob.data.size=.50;ob.data.size_y=.70
   elif ob.name=='Camera fill':ob.location=(-.65,-.20,.35);ob.data.energy=4;ob.data.size=.50;ob.data.size_y=.70
   else:ob.data.energy=0
  if s.get('ammo_light'):
   index=list(LIGHTS).index(ob.name)
   if index==0:ob.location=(.10,-.10,.15);ob.data.energy=.85;ob.data.size=.12;ob.data.size_y=.15
   elif index==1:ob.location=(-.06,-.12,.05);ob.data.energy=.45;ob.data.size=.14;ob.data.size_y=.12
   elif index==2:ob.location=(.03,.13,.12);ob.data.energy=.9;ob.data.size=.08;ob.data.size_y=.14
   else:ob.data.energy=0
  if scale:ob.location+=Vector((0,0,1));ob.data.energy*=1.5
  ob.rotation_euler=(Vector(s.get('light_target',(0,.025,0) if s.get('ammo_light') else (0,.22,1.02 if scale else 0)))-ob.location).to_track_quat('-Z','Y').to_euler()
 # Optional photographed slit lights and ordinary negative-fill cards. They
 # affect every surface through the same light transport, never part grading.
 for ob in sc.objects:
  if ob.get('photo_auxiliary'):ob.hide_render=True
 for settings in s.get('look_strips',[]):
  name='Photo strip '+settings['name'];ob=sc.objects.get(name)
  if ob is None:
   data=bpy.data.lights.new(name,'AREA');data.shape='RECTANGLE'
   ob=bpy.data.objects.new(name,data);sc.collection.objects.link(ob);ob['photo_auxiliary']=True;ob['studio']=True
  ob.location=settings['location'];ob.data.energy=settings['power'];ob.data.size,ob.data.size_y=settings['size'];ob.data.color=(1,1,1)
  ob.rotation_euler=(Vector(settings['target'])-ob.location).to_track_quat('-Z','Y').to_euler();ob.hide_render=False
 for settings in s.get('look_flags',[]):
  from kit import model as M,studio
  name='Photo flag '+settings['name'];ob=sc.objects.get(name)
  if ob is None:
   mat=studio.studio_mat(name,(.003,.003,.003),.9)
   ob=M.box(name,settings['location'],settings['size'],mat,0);ob['photo_auxiliary']=True;ob['studio']=True;ob.visible_camera=False
  ob.location=settings['location'];ob.dimensions=settings['size'];ob.hide_render=False
 sc['exact_aim']=bool(s.get('aimed'));sc.objects['Aim neutral card'].hide_render=not sc['exact_aim']
 if MASK:s['exposure']=0
