"""Inspect the real shader's contact factor on shipping UVs, without color bias.

Emission projection only; this diagnostic never enters the three shipping maps.
Run under the shared GPU lock. Separate high/low receivers retain their rest
attributes, and the rest of the assembly is excluded from this mask projection.
"""
import json, sys
from pathlib import Path
import bpy, numpy as np
from PIL import Image
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import gpu, weapon as W

def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 W.pose(bpy.data.objects['LeverArmature'],None,0)
 low=bpy.data.objects['Receiver']
 with bpy.data.libraries.load(str(BASE/'build/delivery/high.blend'),link=False) as (src,dst):dst.objects=['Receiver']
 high=dst.objects[0];bpy.context.collection.objects.link(high)
 for ob in list(bpy.context.scene.objects):
  if ob.type=='MESH' and ob not in (low,high):bpy.data.objects.remove(ob,do_unlink=True)
 for ob in (low,high):
  for modifier in ob.modifiers:modifier.show_render=False;modifier.show_viewport=False
  ob.hide_set(False);ob.hide_render=False
 sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=4
 sc.render.bake.margin=12;sc.render.bake.use_selected_to_active=True
 sc.render.bake.cage_extrusion=.001;sc.render.bake.max_ray_distance=.004
 mat=high.data.materials[0];nt=mat.node_tree
 emit=nt.nodes.new('ShaderNodeEmission');nt.links.new(nt.nodes['OUT_wear'].outputs[0],emit.inputs['Color'])
 nt.links.new(emit.outputs[0],nt.nodes['OUT'].inputs['Surface'])
 image=bpy.data.images.new('Inspection contact factor',4096,4096,float_buffer=True)
 image.colorspace_settings.name='Non-Color'
 target=bpy.data.materials.new('Diagnostic mask target');target.use_nodes=True
 tex=target.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;target.node_tree.nodes.active=tex
 low.data.materials.clear();low.data.materials.append(target)
 low.data.uv_layers.active=low.data.uv_layers['BakeUV']
 bpy.ops.object.select_all(action='DESELECT');high.select_set(True);low.select_set(True);bpy.context.view_layer.objects.active=low
 bpy.ops.object.bake(type='EMIT')
 a=np.empty(4096*4096*4,dtype=np.float32);image.pixels.foreach_get(a)
 a=a.reshape(4096,4096,4)[::-1,:,0].copy().reshape(2048,2,2048,2).mean(axis=(1,3))
 out=BASE/'build/review';out.mkdir(exist_ok=True)
 np.save(out/'contact-mask.npy',a)
 Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/'contact-mask.png')
 (out/'contact-mask.json').write_text(json.dumps(dict(size=2048,baked_at=4096,
  purpose='Actual OUT_wear projected from source onto shipping receiver UVs. Diagnostic only; no extra delivered texture.',
  filter='2x2 arithmetic area average of a scalar contact factor',maximum=float(a.max())),indent=2))
 print('CONTACT FACTOR BAKED',float(a.max()),flush=True)
if __name__=='__main__':main()
