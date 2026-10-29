"""Geometry-only checkpoint normal projection; no finish, color or wear bake.

All source relief is authored mesh geometry. Independent target islands occupy
one shared 2048 inspection normal. Other surfaces sample its flat neutral patch.
These inspection UVs do not stand in for final atlas/texel-density acceptance.
"""
import argparse,sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import gpu,weapon as W
from kit.image_io import write_png
TARGETS={'Receiver_Sheet':(.02,.55,.98,.98),'PistolGrip_Sculpt':(.02,.02,.49,.52),
 'Sight_TangentLeaf':(.51,.02,.98,.39),
 'Sight_SliderButton-1':(.51,.42,.72,.52),'Sight_SliderButton1':(.75,.42,.98,.52)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source).resolve()
 bpy.ops.wm.open_mainfile(filepath=str(path));sc=bpy.context.scene;arm=bpy.data.objects['R39Armature'];W.pose(arm,None,0)
 objects=[o for o in sc.objects if o.type=='MESH' and o.get('asset_set') and not o.get('bake_only')]
 high=[o for o in sc.objects if o.type=='MESH' and o.get('bake_only')]
 # Initialize every non-target surface to an unused, neutral-normal texel.
 for ob in objects:
  uv=ob.data.uv_layers.new(name='FormUV')
  for row in uv.data:row.uv=(.995,.005)
 sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=1
 sc.render.bake.use_selected_to_active=True;sc.render.bake.cage_extrusion=.0008
 sc.render.bake.max_ray_distance=.003;sc.render.bake.margin=8
 image=bpy.data.images.new('Rill39 geometric form normal',4096,4096,alpha=False,float_buffer=True)
 image.colorspace_settings.name='Non-Color';rows=[];first=True
 for name,rect in TARGETS.items():
  target=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');target.select_set(True);bpy.context.view_layer.objects.active=target
  bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.uv.smart_project(angle_limit=1.05,island_margin=.025,correct_aspect=False)
  bpy.ops.object.mode_set(mode='OBJECT')
  for row in target.data.uv_layers.active.data:
   u,v=row.uv;row.uv=(rect[0]+u*(rect[2]-rect[0]),rect[1]+v*(rect[3]-rect[1]))
  sources=[o for o in high if o.get('low_target')==name]
  # A base skin supplies every ray outside the additive relief silhouettes.
  copy=target.copy();copy.data=target.data.copy();sc.collection.objects.link(copy)
  copy.parent=None;copy.modifiers.clear();copy.matrix_world=target.matrix_world.copy();copy.hide_render=False
  sources=[copy,*sources]
  original=list(target.data.materials);material=bpy.data.materials.new('Projection target '+name);material.use_nodes=True
  target.data.materials.clear();target.data.materials.append(material)
  node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;material.node_tree.nodes.active=node
  bpy.ops.object.select_all(action='DESELECT')
  for ob in sources:ob.hide_set(False);ob.hide_render=False;ob.select_set(True)
  target.select_set(True);bpy.context.view_layer.objects.active=target;sc.render.bake.use_clear=first
  sc.render.bake.cage_extrusion=.003 if name=='Receiver_Sheet' else .0018 if name=='PistolGrip_Sculpt' else .0008
  sc.render.bake.max_ray_distance=.006
  bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
  first=False;rows.append(dict(target=name,sources=[o.name for o in sources],rect=rect))
  target.data.materials.clear()
  for m in original:target.data.materials.append(m)
  bpy.data.objects.remove(copy,do_unlink=True)
  for ob in sources[1:]:ob.hide_render=True;ob.hide_set(True)
 values=np.empty(4096*4096*4,np.float32);image.pixels.foreach_get(values);values=values.reshape(4096,4096,4)
 # Vector-filter exactly 2x down, then renormalize. Work in +Y tangent space.
 vec=values[:,:,:3]*2-1;vec=vec.reshape(2048,2,2048,2,3).mean(axis=(1,3))
 length=np.linalg.norm(vec,axis=2,keepdims=True);vec/=np.maximum(length,1e-8)
 final=np.flipud((vec+1)/2);final[-24:,-24:]=(.5,.5,1)
 dest=path.parent/'T_Rill39_FormNormal.png';write_png(dest,final,bits=16)
 bpy.data.images.remove(image);image=bpy.data.images.load(str(dest));image.colorspace_settings.name='Non-Color';image.pack()
 for name in ('Inspection_paint','Inspection_blue','Inspection_grip'):
  m=bpy.data.materials[name];nt=m.node_tree;tex=nt.nodes.new('ShaderNodeTexImage');tex.image=image
  normal=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(tex.outputs['Color'],normal.inputs['Color'])
  nt.links.new(normal.outputs['Normal'],nt.nodes['Principled BSDF'].inputs['Normal'])
 for ob in high:ob.hide_render=True;ob.hide_set(True)
 W.pose(arm,'Idle',0);bpy.ops.wm.save_as_mainfile(filepath=str(path))
 sockets=[o for o in sc.objects if o.name.startswith('Socket_')]
 W.export(path.with_suffix('.glb'),[arm,*objects,*sockets])
 mp=[o for o in objects if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')]
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
  W.pose(arm,clip,0);ob=W.detachable(mp,arm,'Magazine','Magazine')
  W.export(path.parent/('magazine_'+state+'.glb'),[ob],animations=False);bpy.data.objects.remove(ob,do_unlink=True)
 report=dict(size=2048,source_size=4096,maps=1,stage='geometric normal only',targets=rows,
  sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size)
 (path.parent/'form-normal.json').write_text(json.dumps(report,indent=2));print('FORM NORMAL',report['sha256'])
if __name__=='__main__':main()
